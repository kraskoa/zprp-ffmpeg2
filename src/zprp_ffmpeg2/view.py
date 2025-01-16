import dataclasses
from collections import UserList
from collections import defaultdict
from enum import Enum
from typing import Any
from typing import Iterable
from typing import List
from typing import Optional

from .filter_graph import AnyNode
from .filter_graph import Filter
from .filter_graph import MergeOutputFilter
from .filter_graph import SinkFilter
from .filter_graph import SourceFilter
from .filter_graph import Stream


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
        sep = ""
        if self.path:
            sep = ";"
        return f"{self.path}{sep}{self.name}"

    def prev_node(self) -> List[str] | None:
        if not self.path:
            return None
        return [path.split(";")[-1] for path in self.path.split("|")]


class PrepNodeList(UserList):
    def __init__(self) -> None:
        super().__init__()
        self.counter = defaultdict(int)

    def append(self, item: Any) -> None:
        if not isinstance(item, (PrepNode, PrepNodeList)):
            raise ValueError("Only PrepNode and PrepNodeList objects and can be added to PrepNodeList")
        if isinstance(item, PrepNode):
            if item not in self.data:
                self.counter[item.name] += 1
            if (c := self.counter[item.name]) > 1:
                item = PrepNode(f"{item.name}({c})", item.color, item.path)
        self.data.append(item)

    def extend(self, iterable: Iterable) -> None:
        for element in iterable:
            self.append(element)


def create_graph_connections(parent_node: AnyNode | "Stream", previous: PrepNodeList) -> None:
    new_connections = PrepNodeList()
    nodes = None
    if isinstance(parent_node, Filter):
        nodes = parent_node._in
    else:
        nodes = parent_node._nodes
    for node in nodes:
        if isinstance(node, SourceFilter):
            new_connections.append(PrepNode(node.in_path.split("/")[-1], NodeColors.INPUT, ""))
        elif isinstance(node, SinkFilter):
            new_connections.append(PrepNode(node.out_path.split("/")[-1], NodeColors.OUTPUT, new_connections[-1].create_path_for_next()))
        elif isinstance(node, Filter):
            path = ""
            if not new_connections:
                create_graph_connections(node, previous)
                paths = []
                streams = []
                for _ in range(len(node._in)):
                    processed_stream = previous.pop()
                    paths.append(processed_stream[-1].create_path_for_next())
                    streams.append(processed_stream)
                for stream in streams:
                    previous.extend(stream)
                path = "|".join(paths)
            else:
                path = new_connections[-1].create_path_for_next()
            new_connections.append(PrepNode(node.command, NodeColors.FILTER, path))
        elif isinstance(node, MergeOutputFilter):
            for stream in node.streams:
                create_graph_connections(stream, previous)
            return
        elif isinstance(node, Stream):
            create_graph_connections(node, previous)
    if isinstance(parent_node, Stream):
        previous.append(new_connections)
    else:
        previous.extend(new_connections)


def flatten_graph_connections(graph_connection: PrepNodeList) -> PrepNodeList:
    flat_graph_connection = []

    # This whole process could be shortened to more-itertools
    # package's collapse
    for element in graph_connection:
        if isinstance(element, PrepNodeList):
            flat_graph_connection.extend(element)
        else:
            flat_graph_connection.append(element)
    return list(dict.fromkeys(flat_graph_connection))


def view(graph: Stream, filename: Optional[str] = None) -> None:
    "Creates a graph of filters"

    import networkx as nx  # type: ignore
    from matplotlib import pyplot as plt  # type: ignore

    G = nx.DiGraph()

    graph_connection = PrepNodeList()
    create_graph_connections(graph, graph_connection)
    graph_connection = flatten_graph_connections(graph_connection)

    # Adding nodes
    for pre_node in graph_connection:
        G.add_node(pre_node.name, color=pre_node.color)

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
