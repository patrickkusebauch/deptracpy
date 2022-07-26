from __future__ import annotations

from typing import List, Dict
from dataclasses import dataclass

import libcst as cst
import libcst.metadata.scope_provider as scope_provider


@dataclass
class AstMap:
    file_references: List[AstFile]


@dataclass(frozen=True)
class AstFile:
    path: str
    root: str
    dependencies: List[AstReference]


@dataclass(frozen=True)
class AstReference:
    target: str


class AstFileBuilder:
    path: str
    root: str
    dependencies: Dict[str, AstReference]

    def __init__(self, path: str, root: str):
        self.path = path
        self.root = root
        self.dependencies = {}

    def build(self) -> AstFile:
        return AstFile(self.path, self.root, list(self.dependencies.values()))


def references_from_fqn_provider(wrapper: cst.metadata.MetadataWrapper) -> List[str]:
    references: List[str] = []

    fq_names = wrapper.resolve(cst.metadata.FullyQualifiedNameProvider)
    for node, qualified_names in fq_names.items():
        for qualified_name in qualified_names:
            if qualified_name.source == cst.metadata.QualifiedNameSource.IMPORT:
                references.append(qualified_name.name)
    return references


# todo: @Clean-up: This function is currently unused, but might be useful (patrick @ 2023-03-25)
def references_from_scope_provider(wrapper: cst.metadata.MetadataWrapper) -> List[str]:
    references: List[str] = []
    scopes: set[scope_provider.Scope] = set(wrapper.resolve(cst.metadata.ScopeProvider).values())  # type: ignore
    for scope in scopes:
        for assignment in scope.assignments:
            if isinstance(assignment, scope_provider.ImportAssignment) and isinstance(
                assignment.node, (cst.Import, cst.ImportFrom)
            ):
                match type(assignment.node):
                    case cst.Import:
                        references.append(assignment.node.names[0].evaluated_name)  # type: ignore
                    case cst.ImportFrom:
                        references.append(assignment.get_module_name_for_import())
    return references


def build_ast_map(files_in_paths: Dict[str, List[str]]) -> AstMap:
    ast_map = AstMap([])
    for root_path, files in files_in_paths.items():
        repo_manager = cst.metadata.FullRepoManager(
            root_path, files, {cst.metadata.FullyQualifiedNameProvider}
        )
        for file in files:
            reference_builder = AstFileBuilder(path=file, root=root_path)
            wrapper: cst.metadata.MetadataWrapper = (
                repo_manager.get_metadata_wrapper_for_path(file)
            )

            for name in references_from_fqn_provider(wrapper):
                reference_builder.dependencies[name] = AstReference(target=name)

            ast_map.file_references.append(reference_builder.build())
    return ast_map
