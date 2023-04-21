from io import open
from rich.console import Console
from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.config import DeptracConfig
from typing import Dict, List, Tuple
from returns.result import Success


class Node:
    name: str

    def __init__(self, name: str) -> None:
        self.name = name


class Edge:
    source: str
    target: str
    label: str | int
    color: str

    def __init__(
        self, source: str, target: str, label: str | int, color: str = "black"
    ) -> None:
        self.source = source
        self.target = target
        self.label = label
        self.color = color


class Graph:
    nodes: List[Node]
    edges: List[Edge]

    def __init__(self) -> None:
        self.nodes = []
        self.edges = []

    def add_node(self, node: Node) -> None:
        self.nodes.append(node)

    def add_edge(self, edge: Edge) -> None:
        self.edges.append(edge)

    def write(self, path: str) -> None:
        string_builder = ["digraph G {\n"]

        for node in sorted(self.nodes, key=self.__node_sort):
            string_builder.append(f"\t{node.name};\n")

        string_builder.append(f"\n")  # newline between nodes and edges

        for edge in sorted(self.edges, key=self.__edge_sort):
            string_builder.append(
                f"\t{edge.source} -> {edge.target} [color={edge.color}, label={edge.label}];\n"
            )

        string_builder.append("}\n")
        output = "".join(string_builder)
        with open(path, mode="wt", encoding=None) as f:
            f.write(output)


    @staticmethod
    def __node_sort(node: Node) -> str:
        return node.name

    @staticmethod
    def __edge_sort(edge: Edge) -> Tuple[str, str]:
        return edge.source, edge.target


def format_dot(
    result: AnalysisResult, config: DeptracConfig
) -> Success[AnalysisResult]:
    graph = Graph()

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
