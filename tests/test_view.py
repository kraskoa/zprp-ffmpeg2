
import pytest

import zprp_ffmpeg2 as ffmpeg
from zprp_ffmpeg2._api_compat import Filter
from zprp_ffmpeg2.view import NodeColors
from zprp_ffmpeg2.view import PrepNode
from zprp_ffmpeg2.view import create_graph_connections


@pytest.fixture(autouse=True)
def run_before():
    Filter._filter_counter.clear()


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


def test_create_graph_connections_simple_chain():
    in_ = ffmpeg.input("in.mp4")
    stream = ffmpeg.hflip(in_)
    out1 = stream.output("out.mp4")
    graph_connection = []
    create_graph_connections(out1, graph_connection)
    assert len(graph_connection) == 3
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("hflip", NodeColors.FILTER, "in.mp4")
    node3 = PrepNode("out.mp4", NodeColors.OUTPUT, "in.mp4;hflip")
    assert graph_connection[0] == node1
    assert graph_connection[1] == node2
    assert graph_connection[2] == node3


def test_create_graph_connections_merged_outputs_chain():
    in_ = ffmpeg.input("in.mp4")
    stream = ffmpeg.fade(in_, type="in", start_frame=0, nb_frames=30)
    out1 = stream.output("out1.mp4")
    stream = ffmpeg.hflip(stream)
    out2 = stream.output("out2.mp4")
    merged = ffmpeg.merge_outputs(out1, out2)
    nodes = []
    create_graph_connections(merged, nodes)
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("fade", NodeColors.FILTER, "in.mp4")
    node3 = PrepNode("hflip", NodeColors.FILTER, "in.mp4;fade")
    node4 = PrepNode("out1.mp4", NodeColors.OUTPUT, "in.mp4;fade")
    node5 = PrepNode("out2.mp4", NodeColors.OUTPUT, "in.mp4;fade;hflip")
    nodes_set = set(nodes)
    twin_strim = set([node1, node2, node3, node4, node5])
    assert len(nodes_set) == 5
    assert nodes_set == twin_strim


def test_create_graph_connections_concat():
    stream = ffmpeg.input("in.mp4", t=5)
    stream2 = ffmpeg.input("in2.mp4")
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream2))
    stream = ffmpeg.output(stream, "out.mp4")
    nodes = []
    create_graph_connections(stream, nodes)
    node1 = PrepNode("in.mp4", NodeColors.INPUT, "")
    node2 = PrepNode("in2.mp4", NodeColors.INPUT, "")
    node3 = PrepNode("fade", NodeColors.FILTER, "in.mp4")
    node4 = PrepNode("concat", NodeColors.FILTER, "in.mp4;fade|in2.mp4")
    node5 = PrepNode("out.mp4", NodeColors.OUTPUT, "concat")
    assert len(nodes) == 5
    stream1 = []
    stream1.extend([node1, node2, node3, node4, node5])
    assert set(nodes) == set(stream1)
