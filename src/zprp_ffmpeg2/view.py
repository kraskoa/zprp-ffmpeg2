import dataclasses
from collections import UserList
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
from re import sub


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

    @property
    def id(self):
        if "(" in self.name:
            return int(self.name[self.name.find("(")+1:self.name.find(")")])
        else:
            return 1

    @property
    def command(self):
        return sub(r"(\w+)\(\d+\)", r'\1', self.name)


class PrepNodeList(UserList):
    def append(self, item: Any) -> None:
        if not isinstance(item, (PrepNode, PrepNodeList)):
            raise ValueError("Only PrepNode and PrepNodeList objects and can be added to PrepNodeList")
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
                # streams = []
                for stream in node._in:
                    last_node = stream._nodes[-1]
                    parent_prep_node = None
                    if isinstance(last_node, Filter):
                        parent_prep_node = next((n for n in previous if (n.command, n.id) == (last_node.command, last_node._id)))
                    else:
                        parent_prep_node = next((n for n in previous if n.name == last_node.in_path))
                    paths.append(parent_prep_node.create_path_for_next())
                path = "|".join(paths)
            else:
                path = new_connections[-1].create_path_for_next()
            suffix = "" if node._id < 2 else f"({node._id})"
            new_connections.append(PrepNode(f"{node.command}{suffix}", NodeColors.FILTER, path))
        elif isinstance(node, MergeOutputFilter):
            for stream in node.streams:
                create_graph_connections(stream, previous)
            return
        elif isinstance(node, Stream):
            create_graph_connections(node, previous)
    previous.extend(new_connections)


def view(graph: Stream, filename: Optional[str] = None) -> None:
    "Creates a graph of filters"

    import networkx as nx  # type: ignore
    from matplotlib import pyplot as plt  # type: ignore

    G = nx.DiGraph()

    graph_connection = PrepNodeList()
    create_graph_connections(graph, graph_connection)
    graph_connection = list(dict.fromkeys(graph_connection))

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
