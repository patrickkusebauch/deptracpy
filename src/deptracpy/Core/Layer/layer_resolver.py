from typing import List

from deptracpy.Contract.config import LayerConfig

from returns.result import Result, Success, Failure


# todo: @Investigate: Can we make this work with regex instead? (patrick @ 2023-03-17)
def module_collector_match(token: str, path: str) -> bool:
    if not token.startswith(path):
        return False
    reduced = token.removeprefix(path)[1:]  # remove leading '.'
    return reduced.count(".") == 0


# todo: @Investigate: Can we make this work with regex instead? (patrick @ 2023-03-17)
def recursive_module_collector_match(token: str, path: str) -> bool:
    return token.startswith(path)


# todo: @Investigate: Can I check if all collectors exist at start-up instead? This might be harder to do with
#  dynamic collectors registered as plugins (patrick @ 2023-03-25)


# todo: @Incomplete: caching (patrick @ 2023-03-17)
def get_layers_for_token(
    layer_definitions: List[LayerConfig], token: str
) -> Result[List[str], str]:
    layers: List[str] = []
    for layer_definition in layer_definitions:
        is_matching = False
        for collector in layer_definition.collectors:
            match collector.type:
                case "Module":
                    is_matching = is_matching or module_collector_match(
                        token, collector.path
                    )
                case "ModuleRecursive":
                    is_matching = is_matching or recursive_module_collector_match(
                        token, collector.path
                    )
                case _:
                    return Failure(f"Unrecognized collector type `{collector.type}`")
        if is_matching:
            layers.append(layer_definition.name)

    return Success(layers)
