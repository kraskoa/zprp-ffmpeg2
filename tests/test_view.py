from copy import copy

import pytest

import zprp_ffmpeg2 as ffmpeg
from zprp_ffmpeg2.view import NodeColors
from zprp_ffmpeg2.view import PrepNode
from zprp_ffmpeg2.view import PrepNodeList
from zprp_ffmpeg2.view import create_graph_connections
from zprp_ffmpeg2.view import flatten_graph_connections


def test_prep_node_create_path_for_next():
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    assert node1.create_path_for_next() == "in.mp4"
    node2 = PrepNode("hflip", NodeColors.FILTER, node1.create_path_for_next())
    assert node2.create_path_for_next() == "in.mp4;hflip"
    node3 = PrepNode("concat", NodeColors.FILTER, "in.mp4;hflip|in2.mp4")
    assert node3.create_path_for_next() == node3.name


def test_prep_node_prev_node():
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    assert node1.prev_node() is None
    node2 = PrepNode("hflip", NodeColors.FILTER, node1.create_path_for_next())
    assert node2.prev_node() == ["in.mp4"]
    node3 = PrepNode("concat", NodeColors.FILTER, "in.mp4;hflip|in2.mp4")
    assert node3.prev_node() == ["hflip", "in2.mp4"]


def test_prep_node_list_append():
    nodes = PrepNodeList()
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    nodes.append(node1)
    assert len(nodes) == 1
    assert nodes.counter["in.mp4"] == 1
    counter_state = copy(nodes.counter)
    assert nodes[0] == node1
    nodes2 = PrepNodeList()
    nodes.append(nodes2)
    assert len(nodes) == 2
    assert nodes.counter == counter_state
    node2 = PrepNode("filter", NodeColors.FILTER, "in.mp4")
    nodes.append(node2)
    assert len(nodes) == 3
    assert nodes.counter != counter_state
    not_node = NodeColors.FILTER
    with pytest.raises(ValueError, match="Only PrepNode and PrepNodeList objects and can be added to PrepNodeList"):
        nodes.append(not_node)


def test_prep_node_list_append_same_filter_twice():
    nodes = PrepNodeList()
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    nodes.append(node1)
    assert nodes.counter["beau_filter"] == 0
    node2 = PrepNode(
        "beau_filter",
        NodeColors.FILTER,
        nodes[-1].create_path_for_next()
    )
    nodes.append(node2)
    assert nodes.counter["beau_filter"] == 1
    node3 = PrepNode(
        node2.name,
        NodeColors.FILTER,
        nodes[-1].create_path_for_next()
    )
    nodes.append(node3)
    assert nodes.counter["beau_filter"] == 2
    assert nodes[-1].name == "beau_filter(2)"


def test_prep_node_list_extend():
    nodes = PrepNodeList()
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode(
        "test",
        NodeColors.FILTER,
        node1.create_path_for_next()
    )
    nodes.append(node1)
    nodes.append(node2)
    nodes2 = PrepNodeList()
    node3 = PrepNode("test2", NodeColors.FILTER, "")
    node4 = PrepNode(
        "test",
        NodeColors.FILTER,
        node3.create_path_for_next()
    )
    nodes2.append(node3)
    nodes2.append(node4)
    nodes.extend(nodes2)
    assert nodes.counter["test"] == 2
    assert nodes[-1].name == "test(2)"


def test_create_graph_connections_simple_chain():
    in_ = ffmpeg.input("in.mp4")
    stream = ffmpeg.hflip(in_)
    out1 = stream.output("out.mp4")
    graph_connection = PrepNodeList()
    create_graph_connections(out1, graph_connection)
    assert len(graph_connection) == 1
    assert len(graph_connection[0]) == 3
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("hflip", NodeColors.FILTER, "in.mp4")
    node3 = PrepNode("out.mp4", NodeColors.OUTPUT, "in.mp4;hflip")
    node_stream = graph_connection[0]
    assert node_stream[0] == node1
    assert node_stream[1] == node2
    assert node_stream[2] == node3


def test_create_graph_connections_merged_outputs_chain():
    in_ = ffmpeg.input("in.mp4")
    stream = ffmpeg.fade(in_, type="in", start_frame=0, nb_frames=30)
    out1 = stream.output("out1.mp4")
    stream = ffmpeg.hflip(stream)
    out2 = stream.output("out2.mp4")
    merged = ffmpeg.merge_outputs(out1, out2)
    nodes = PrepNodeList()
    create_graph_connections(merged, nodes)
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("fade", NodeColors.FILTER, "in.mp4")
    node3 = PrepNode("hflip", NodeColors.FILTER, "in.mp4;fade")
    node4 = PrepNode("out1.mp4", NodeColors.OUTPUT, "in.mp4;fade")
    node5 = PrepNode("out2.mp4", NodeColors.OUTPUT, "in.mp4;fade;hflip")
    stream1 = PrepNodeList()
    stream2 = PrepNodeList()
    stream1.extend([node1, node2, node4])
    stream2.extend([node1, node2, node3, node5])
    assert len(nodes) == 2
    assert stream1 == nodes[0]
    assert stream2 == nodes[1]


def test_create_graph_connections_concat():
    stream = ffmpeg.input("in.mp4", t=5)
    stream2 = ffmpeg.input("in2.mp4")
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream2))
    stream = ffmpeg.output(stream, "out.mp4")
    nodes = PrepNodeList()
    create_graph_connections(stream, nodes)
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("in2.mp4", NodeColors.INPUT, "")
    node3 = PrepNode("fade", NodeColors.FILTER, "in.mp4")
    node4 = PrepNode("concat", NodeColors.FILTER, "in2.mp4|in.mp4;fade")
    node5 = PrepNode("out.mp4", NodeColors.OUTPUT, "concat")
    assert len(nodes) == 4
    stream1 = PrepNodeList()
    stream1.extend([node1, node2, node3, node4, node5])
    nodes = flatten_graph_connections(nodes)
    assert set(nodes) == set(stream1)


def test_flatten_graph_connections_simple():
    nodes = PrepNodeList()
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("in2.mp4", NodeColors.INPUT, "")
    nodes.extend([node1, node2])
    assert nodes == flatten_graph_connections(nodes)


def test_flatten_graph_connections_with_lists():
    nodes = PrepNodeList()
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("in2.mp4", NodeColors.INPUT, "")
    node3 = PrepNode("flip", NodeColors.FILTER, "in2.mp4")
    nodes.append(node1)
    inner_nodes = PrepNodeList()
    inner_nodes.extend([node2, node3])
    nodes.append(inner_nodes)
    flat = flatten_graph_connections(nodes)
    assert len(flat) == 3
    assert flat[0] == node1
    assert flat[1] == node2
    assert flat[2] == node3
