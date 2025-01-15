# test if the package structure matches
import json
from pathlib import Path

import pytest

import zprp_ffmpeg as ffmpeg


def test_input():
    # example from readme
    stream = ffmpeg.input("input.mp4")
    stream = ffmpeg.hflip(stream)
    stream = ffmpeg.output(stream, "out.mp4")
    ffmpeg.run(stream)


def test_filter_custom():
    """https://github.com/kkroening/ffmpeg-python/blob/df129c7ba30aaa9ffffb81a48f53aa7253b0b4e6/ffmpeg/tests/test_ffmpeg.py#L569"""
    stream = ffmpeg.input("dummy.mp4")
    stream = ffmpeg.filter(stream, "custom_filter", "a", "b", kwarg1="c")
    stream = ffmpeg.output(stream, "dummy2.mp4")
    assert stream.get_args() == [
        "-i",
        "dummy.mp4",
        "-filter_complex",
        '"[0:v]custom_filter=kwarg1=c[v0]"',
        "-map",
        "[v0]",
        "dummy2.mp4",
    ]


def test_filter_custom_fluent():
    """https://github.com/kkroening/ffmpeg-python/blob/df129c7ba30aaa9ffffb81a48f53aa7253b0b4e6/ffmpeg/tests/test_ffmpeg.py#L584"""
    stream = (
        ffmpeg.input("dummy.mp4")
        .filter("custom_filter", "a", "b", kwarg1="c")
        .output("dummy2.mp4")
    )
    assert stream.get_args() == [
        "-i",
        "dummy.mp4",
        "-filter_complex",
        '"[0:v]custom_filter=kwarg1=c[v0]"',
        "-map",
        "[v0]",
        "dummy2.mp4",
    ]

def test_compile():
    """https://github.com/kkroening/ffmpeg-python/blob/df129c7ba30aaa9ffffb81a48f53aa7253b0b4e6/ffmpeg/tests/test_ffmpeg.py#L456"""
    stream = ffmpeg.input("dummy.mp4").hflip().output("dummy2.mp4")
    assert stream.compile() == [
        "ffmpeg",
        "-i",
        "dummy.mp4",
        "-filter_complex",
        '"[0:v]hflip[v0]"',
        "-map",
        "[v0]",
        "dummy2.mp4",
    ]
    assert stream.compile(cmd="ffmpeg.old") == [
        "ffmpeg.old",
        "-i",
        "dummy.mp4",
        "-filter_complex",
        '"[0:v]hflip[v0]"',
        "-map",
        "[v0]",
        "dummy2.mp4",
    ]


def test_get_args_simple():
    """https://github.com/kkroening/ffmpeg-python/blob/df129c7ba30aaa9ffffb81a48f53aa7253b0b4e6/ffmpeg/tests/test_ffmpeg.py#L135"""
    out_file = ffmpeg.input("dummy.mp4").hflip().output("dummy2.mp4")
    assert out_file.get_args() == ["-i", "dummy.mp4", "-filter_complex", '"[0:v]hflip[v0]"', "-map", "[v0]", "dummy2"
                                                                                                             ".mp4"]


def test_get_args_overwrite():
    out_file = ffmpeg.input("dummy.mp4").hflip().output("dummy2.mp4")
    assert out_file.get_args(True) == ["-i", "dummy.mp4", "-filter_complex", '"[0:v]hflip[v0]"', "-map", "[v0]",
                                       "dummy2.mp4", "-y"]


def test_global_args():
    out_file = (
        ffmpeg.input("dummy.mp4")
        .hflip()
        .output("dummy2.mp4")
        .global_args("-progress", "someurl")
    )
    assert out_file.get_args() == [
        "-i",
        "dummy.mp4",
        "-filter_complex",
        '"[0:v]hflip[v0]"',
        "-map",
        "[v0]",
        "dummy2.mp4",
        "-progress",
        "someurl",
    ]

def test_overwrite():
    stream = ffmpeg.input("something.avi")
    stream = ffmpeg.overwrite_output(stream)
    stream = ffmpeg.output(stream, "output.avi")
    args = ffmpeg.get_args(stream)
    assert "-y" in args # c

def test_probe():
    with pytest.raises(Exception, match="ffprobe"):
        _ = ffmpeg.probe("doesntexist.mp4")

    out = ffmpeg.probe(str(Path(__file__).parent / "assets/in.mp4"), pretty=None, v=1) # can pass any kwargs with value, or with "None" as a plain option
    assert isinstance(out, str)

    # try to decode, by default it's json
    obj = json.loads(out)
    assert "streams" in obj



# def test__multi_output_scaling():
#     in_ = ffmpeg.input('in.mp4')
#     out1 = in_.output('out1.mp4', vf='scale=1280:720')
#     out2 = in_.output('out2.mp4', vf='scale=640:360')
#     merged = ffmpeg.merge_outputs(out1, out2)
#
#     # Validate the arguments for the combined command
#     assert merged.get_args() == [
#         '-i', 'in.mp4',
#         '-vf', 'scale=1280:720', 'out1.mp4',
#         '-vf', 'scale=640:360', 'out2.mp4',
#     ]
#
# def test__multi_output_scaling():
#     in_ = ffmpeg.input("in.mp4")
#     out1 = in_.output("out1.mp4")
#     out2 = in_.output("out2.mp4")
#     merged = ffmpeg.merge_outputs(out1, out2)
#
#     # Validate the arguments for the combined command
#     assert merged.get_args() == [
#         "-i", "in.mp4",
#     ]

def test__merge_outputs_with_filters():
    in_ = ffmpeg.input("in.mp4")
    in_flip = ffmpeg.hflip(in_)
    out1 = in_.output("out1.mp4")
    assert out1.get_args() == ["-i", "in.mp4", "out1.mp4"]
    out2 = in_flip.output("out2.mp4")
    assert out2.get_args() == ["-i", "in.mp4", "-filter_complex", '"[0:v]hflip[v0]"', "-map", "[v0]", "out2.mp4"]
    assert ffmpeg.merge_outputs(out1, out2).get_args() == [
        "-i",
        "in.mp4",
        "-filter_complex",
        "[0]hflip[v0];",
        "out1.mp4",
        "-map",
        "[v0]",
        "out2.mp4",
    ]
    # assert ffmpeg.get_args([out1, out2]) == ["-i", "in.mp4", "out2.mp4", "out1.mp4"]
#
def test__merge_outputs():
    in_ = ffmpeg.input("in.mp4")
    out1 = in_.output("out1.mp4")
    assert out1.get_args() == ["-i", "in.mp4", "out1.mp4"]
    out2 = in_.output("out2.mp4")
    assert out2.get_args() == ["-i", "in.mp4", "out2.mp4"]
    merged = ffmpeg.merge_outputs(out1, out2)
    assert merged.get_args() == ["-i", "in.mp4", "out1.mp4", "out2.mp4"]

    assert (ffmpeg.merge_outputs(out1, out2).get_args() == [
        "-i",
        "in.mp4",
        "out1.mp4",
        "out2.mp4",
    ])
    # assert ffmpeg.get_args([out1, out2]) == ["-i", "in.mp4", "out2.mp4", "out1.mp4"]

def test_deep_copy():
    in_ = ffmpeg.input("in.mp4")
    in_flip = ffmpeg.hflip(in_)
    out1 = in_.output("out1.mp4")
    assert out1.get_args() == ["-i", "in.mp4", "out1.mp4"]
    out2 = in_flip.output("out2.mp4")
    assert out2.get_args() == ["-i", "in.mp4", "-filter_complex", '"[0:v]hflip[v0]"', "-map", "[v0]", "out2.mp4"]
