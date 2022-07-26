from rich.console import Console

from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.config import DeptracConfig
from pydot import Node, Edge, Dot
from typing import Dict
from returns.result import Success


def format_dot(
    result: AnalysisResult, config: DeptracConfig
) -> Success[AnalysisResult]:
    graph = Dot()

    for layer in config.layers:
        if layer.name not in config.hidden_layers:
            graph.add_node(Node(layer.name))

    # source -> (target -> (count, has_violation))
    edges: Dict[str, Dict[str, tuple[int, bool]]] = {}
    for dependency in result.allowed:
        if dependency.source_layer not in edges.keys():
            edges[dependency.source_layer] = {}
        if dependency.target_layer not in edges[dependency.source_layer].keys():
            edges[dependency.source_layer][dependency.target_layer] = (0, False)
        count, has_violation = edges[dependency.source_layer][dependency.target_layer]
        edges[dependency.source_layer][dependency.target_layer] = (
            count + 1,
            has_violation,
        )
    for dependency in result.violations:
        if dependency.source_layer not in edges.keys():
            edges[dependency.source_layer] = {}
        if dependency.target_layer not in edges[dependency.source_layer].keys():
            edges[dependency.source_layer][dependency.target_layer] = (0, True)
        count, _ = edges[dependency.source_layer][dependency.target_layer]
        edges[dependency.source_layer][dependency.target_layer] = (count + 1, True)

    for edge_source, edge_targets in edges.items():
        for edge_target, (count, has_violation) in edge_targets.items():
            if not has_violation and (
                edge_source in config.hidden_layers
                or edge_target in config.hidden_layers
            ):
                continue
            match has_violation:
                case True:
                    graph.add_edge(
                        Edge(edge_source, edge_target, color="red", label=count)
                    )
                case False:
                    graph.add_edge(
                        Edge(edge_source, edge_target, color="black", label=count)
                    )

    filename: str = "deptracpy.dot"
    graph.write(filename)
    console = Console(color_system="standard")
    console.print(f"Dot file outputted into '{filename}'")

    return Success(result)
