import dataclasses
from enum import Enum
from re import sub
from typing import List, Optional, Union

from .filter_graph import AnyNode, Filter, MergeOutputFilter, SinkFilter, SourceFilter, Stream


class NodeColors(Enum):
    INPUT = "#99cc00"
    OUTPUT = "#99ccff"
    FILTER = "#ffcc00"


@dataclasses.dataclass(eq=True, frozen=True)
class PrepNode:
    name: str
    color: NodeColors
    path: str

    def create_path_for_next(self) -> str:
        if "|" in self.path:
            return self.name
        sep = ";" if self.path else ""
        return f"{self.path}{sep}{self.name}"

    def prev_node(self) -> Optional[List[str]]:
        if not self.path:
            return None
        return [path.split(";")[-1] for path in self.path.split("|")]

    @property
    def id(self) -> int:
        if (string := sub(r"\w+\((\d+)\)", r"\1", self.name)) == self.name or "." in self.name:
            return 1
        return int(string)

    @property
    def command(self) -> str:
        return self.name if "." in self.name else sub(r"(\w+)\(\d+\)", r"\1", self.name)


def create_graph_connections(parent_node: Union[AnyNode, Stream], previous: List[PrepNode]) -> None:
    """Creates list of PrepNode objects that contain stream data to later transform it into a graph."""
    new_connections: List[PrepNode] = []

    # Ensuring correct node access
    if isinstance(parent_node, Filter):
        nodes: List[Union[SourceFilter, SinkFilter, Filter]] = parent_node._in
    elif isinstance(parent_node, Stream):
        nodes: List[Union[SourceFilter, SinkFilter, Filter]] = parent_node._nodes  # Ensure Stream has _nodes
    else:
        return  # Avoid processing unknown types

    for node in nodes:
        if isinstance(node, SourceFilter):
            new_connections.append(PrepNode(node.in_path.split("/")[-1], NodeColors.INPUT, ""))
        elif isinstance(node, SinkFilter):
            if new_connections:
                new_connections.append(
                    PrepNode(node.out_path.split("/")[-1], NodeColors.OUTPUT, new_connections[-1].create_path_for_next())
                )
        elif isinstance(node, Filter):
            path = ""
            if not new_connections:
                create_graph_connections(node, previous)
                paths = []
                for stream in node._in:
                    last_node = stream._nodes[-1] if hasattr(stream, "_nodes") else None
                    if isinstance(last_node, Filter):
                        parent_prep_node = next(
                            prep_node for prep_node in previous
                            if (prep_node.command, prep_node.id) == (last_node.command, getattr(last_node, "_id", -1))
                        )
                    elif isinstance(last_node, SourceFilter):
                        parent_prep_node = next(
                            prep_node for prep_node in previous if prep_node.name == last_node.in_path
                        )
                    else:
                        continue
                    paths.append(parent_prep_node.create_path_for_next())
                path = "|".join(paths)
            else:
                path = new_connections[-1].create_path_for_next()

            suffix = f"({getattr(node, '_id', 1)})" if getattr(node, "_id", 1) >= 2 else ""
            new_connections.append(PrepNode(f"{node.command}{suffix}", NodeColors.FILTER, path))
        elif isinstance(node, MergeOutputFilter):
            for stream in node.streams:
                create_graph_connections(stream, previous)
            return
        elif isinstance(node, Stream):
            create_graph_connections(node, previous)

    previous.extend(new_connections)


def view(graph: Stream, filename: Optional[str] = None) -> None:
    """Creates a graph of filters."""

    import networkx as nx  # type: ignore
    from matplotlib import pyplot as plt  # type: ignore

    G = nx.DiGraph()

    graph_connection: List[PrepNode] = []
    create_graph_connections(graph, graph_connection)
    graph_connection = list(dict.fromkeys(graph_connection))  # Remove duplicates while keeping order

    # Adding nodes
    for pre_node in graph_connection:
        G.add_node(pre_node.name, color=pre_node.color.value)

    # Adding edges
    for pre_node in graph_connection:
        if (prev := pre_node.prev_node()) is not None:
            for p in prev:
                G.add_edge(p, pre_node.name)

    pos = nx.circular_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_shape="s",
        node_size=3000,
        node_color=[node.color.value for node in graph_connection],
        font_weight="bold",
    )

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
