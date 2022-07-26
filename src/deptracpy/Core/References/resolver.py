from typing import List

from deptracpy.Contract.analysis_result import Reference
from deptracpy.Core.Ast.ast_map import AstMap


def resolve_references(ast_map: AstMap) -> List[Reference]:
    """

    :rtype: object
    """
    references = []
    for file_reference in ast_map.file_references:
        for target_dependency in file_reference.dependencies:
            references.append(
                Reference(
                    source_token=path_to_token(file_reference.path),
                    target_token=target_dependency.target,
                )
            )
    return references


def path_to_token(path: str) -> str:
    return path[:-3].replace("/", ".")
