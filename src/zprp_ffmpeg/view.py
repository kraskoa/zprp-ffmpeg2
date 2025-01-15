from .filter_graph import (
    Filter,
    SinkFilter,
    SourceFilter,
    Stream,
    MergeOutputFilter
)
from enum import Enum
import dataclasses
from typing import List
import itertools
import networkx as nx  # type: ignore
from matplotlib import pyplot as plt  # type: ignore
from collections import UserList, defaultdict


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
        sep = ""
        if self.path:
            sep = ";"
        return f"{self.path}{sep}{self.name}"

    def prev_node(self) -> str:
        if not self.path:
            return None
        else:
            return self.path.split(";")[-1]


class PrepNodeList(UserList):
    def __init__(self) -> None:
        super().__init__()
        self.counter = defaultdict(int)

    def append(self, item) -> None:
        if not isinstance(item, PrepNode):
            raise ValueError(
                "Only PrepNode object can be added to PrepNodeList"
            )
        if (item.name, item.path) not in [(element.name, element.path) for element in self.data]:
            self.counter[item.name] += 1
        if (c := self.counter[item.name]) > 1:
            item = PrepNode(
                f"{item.name}({c})",
                item.color,
                item.path
            )
        self.data.append(item)


def create_graph_connections(graph: Stream, previous: List[PrepNode]) -> None:
    new_connections = PrepNodeList()
    for node in graph._nodes:
        if isinstance(node, SourceFilter):
            new_connections.append(
                PrepNode(
                    node.in_path.split("/")[-1],
                    NodeColors.INPUT.value,
                    ""
                )
            )
        elif isinstance(node, SinkFilter):
            new_connections.append(
                PrepNode(
                    node.out_path.split("/")[-1],
                    NodeColors.OUTPUT.value,
                    new_connections[-1].create_path_for_next()
                )
            )
        elif isinstance(node, Filter):
            new_connections.append(
                PrepNode(
                    node.command,
                    NodeColors.FILTER.value,
                    new_connections[-1].create_path_for_next()
                )
            )
        elif isinstance(node, MergeOutputFilter):
            for stream in node.streams:
                create_graph_connections(stream, previous)
            return
    previous.append(new_connections)


def view(graph: Stream, filename: str = None) -> None:
    "Creates graph of filters"

    G = nx.DiGraph()

    graph_connection = []
    create_graph_connections(graph, graph_connection)
    unique_nodes = list(
        dict.fromkeys(
            itertools.chain.from_iterable(
                graph_connection
            )
        )
    )

    # Adding nodes
    for pre_node in unique_nodes:
        G.add_node(pre_node.name, color=pre_node.color)

    # Adding edges
    for pre_node in unique_nodes:
        if (prev := pre_node.prev_node()) is not None:
            G.add_edge(prev, pre_node.name)

    pos = nx.planar_layout(G)
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_shape="s",
        node_size=3000,
        node_color=[node.color for node in unique_nodes],
        font_weight="bold"
    )

    if filename:
        plt.savefig(filename)
    else:
        plt.show()
