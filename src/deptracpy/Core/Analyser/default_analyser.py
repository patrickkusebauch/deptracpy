from typing import List, Tuple

from returns.pipeline import is_successful

from deptracpy.Core.Analyser.input_loader import load_files
from deptracpy.Core.Ast.ast_map import build_ast_map, AstMap
from deptracpy.Core.References.resolver import resolve_references
from deptracpy.Core.Layer.layer_resolver import get_layers_for_token
from deptracpy.Contract.config import DeptracConfig, RulesetConfig, LayerConfig
from deptracpy.Contract.analysis_result import (
    AnalysisResult,
    Dependency,
    Error,
    Reference,
)
from deptracpy.Contract.argument_parser import ArgumentParser

from returns.result import Result, Success, Failure


# todo: @Note: Cannot use `returns.curry.partial` as filter: https://github.com/dry-python/returns/issues/1433 (
#  patrick @ 2023-03-26)
# todo: @Investigate: It would have been nicer is rulesets were a dictionary (patrick @ 2023-03-25)
def is_allowed(source: str, target: str, rulesets: List[RulesetConfig]) -> bool:
    for ruleset in rulesets:
        if match_ruleset_name(source, ruleset):
            return target in ruleset.target_layers
    return False


def match_ruleset_name(source: str, rule: RulesetConfig) -> bool:
    return rule.source_layer == source


def doesnt_depend_on_its_own_layer(dependency: Dependency) -> bool:
    return dependency.source_layer != dependency.target_layer


def analyse(
    args: Tuple[ArgumentParser, DeptracConfig]
) -> Result[Tuple[ArgumentParser, DeptracConfig, AnalysisResult], str]:
    parser, config = args

    ast_map: AstMap = get_ast_map(config)
    references: List[Reference] = resolve_references(ast_map)

    resolution = resolve_dependencies(config.layers, references)
    if not is_successful(resolution):
        return Failure(resolution.failure())
    dependencies, uncovered, errors = resolution.unwrap()

    result = AnalysisResult()
    for dependency in filter(doesnt_depend_on_its_own_layer, dependencies):
        match is_allowed(
            dependency.source_layer, dependency.target_layer, config.rulesets
        ):
            case True:
                result.add_allowed(dependency)
            case False:
                result.add_violation(dependency)

    for token, coverage_type in uncovered:
        result.add_uncovered(token, coverage_type)

    for error in errors:
        result.add_error(error)

    return Success((parser, config, result))


# todo: @Note: Cannot use `returns.curry.partial` as to bake `layers` into `get_layers_for_token`:
#  https://github.com/dry-python/returns/issues/1433 (patrick @ 2023-03-26)
def resolve_dependencies(
    layers: List[LayerConfig], references: List[Reference]
) -> Result[tuple[List[Dependency], List[tuple[str, str]], List[Error]], str]:
    dependencies: List[Dependency] = []
    uncovered: List[tuple[str, str]] = []
    errors: List[Error] = []

    for reference in references:
        # source layer processing
        source_layers_result = get_layers_for_token(layers, reference.source_token)
        if not is_successful(source_layers_result):
            return Failure(source_layers_result.failure())
        source_layers = source_layers_result.unwrap()

        if not source_layers:
            uncovered.append((reference.source_token, "source file"))
            continue

        if len(source_layers) > 1:
            errors.append(
                Error(
                    "Multiple source layers",
                    f"Token '{reference.source_token}' is part of multiple layers.",
                )
            )
            continue

        # target layer processing
        target_layers_result = get_layers_for_token(layers, reference.target_token)
        if not is_successful(target_layers_result):
            return Failure(target_layers_result.failure())
        target_layers = target_layers_result.unwrap()

        if not target_layers:
            uncovered.append((reference.target_token, "target token"))
            continue

        # generate dependencies
        for target_layer in target_layers:
            dependencies.append(
                Dependency(reference, source_layers.pop(), target_layer)
            )

    return Success((dependencies, uncovered, errors))


# todo: @Incomplete: Add caching (patrick @ 2023-03-02)
def get_ast_map(config: DeptracConfig) -> AstMap:
    return build_ast_map(load_files(config.paths))
