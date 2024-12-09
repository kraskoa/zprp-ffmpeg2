# test if the package structure matches
import json
import sys
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


def test_compile_no_filters():
    out_file = ffmpeg.input("dummy.mp4").output("dummy2.mp4")
    with pytest.raises(ValueError, match="No filters selected"):
        out_file.compile()


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
    args = ffmpeg.get_args(stream)
    assert "-y" in args # technically this test can pass when it shouldn't, but that's too nitpicky

def test_probe():
    with pytest.raises(Exception, match="ffprobe"):
        _ = ffmpeg.probe("doesntexist.mp4")

    out = ffmpeg.probe(str(Path(__file__).parent / "assets/in.mp4"), pretty=None, v=1) # can pass any kwargs with value, or with "None" as a plain option
    assert isinstance(out, str)

    # try to decode, by default it's json
    obj = json.loads(out)
    assert "streams" in obj

def test_fluent_output():
    ffmpeg.input('dummy.mp4').trim(start_frame=10, end_frame=20).output('dummy2.mp4')

def test_fluent_equality():
    base1 = ffmpeg.input('dummy1.mp4')
    base2 = ffmpeg.input('dummy1.mp4')
    base3 = ffmpeg.input('dummy2.mp4')
    t1 = base1.trim(start_frame=10, end_frame=20)
    t2 = base1.trim(start_frame=10, end_frame=20)
    t3 = base1.trim(start_frame=10, end_frame=30)
    t4 = base2.trim(start_frame=10, end_frame=20)
    t5 = base3.trim(start_frame=10, end_frame=20)
    print(t1, t2, t3, t4, t5)
    assert t1 == t2
    assert t1 != t3
    assert t1 == t4
    assert t1 != t5

def test_escape_chars():
    assert ffmpeg._utils.escape_chars('a:b', ':') == r'a\:b'
    assert ffmpeg._utils.escape_chars('a\\:b', ':\\') == 'a\\\\\\:b'
    assert (
        ffmpeg._utils.escape_chars('a:b,c[d]e%{}f\'g\'h\\i', '\\\':,[]%')
        == 'a\\:b\\,c\\[d\\]e\\%{}f\\\'g\\\'h\\\\i'
    )
    assert ffmpeg._utils.escape_chars(123, ':\\') == '123'

def test_repeated_args():
    out_file = ffmpeg.input('dummy.mp4').output(
        'dummy2.mp4', streamid=['0:0x101', '1:0x102']
    )
    assert out_file.get_args() == [
        '-i',
        'dummy.mp4',
        '-streamid',
        '0:0x101',
        '-streamid',
        '1:0x102',
        'dummy2.mp4',
    ]

def test__get_args__simple():
    out_file = ffmpeg.input('dummy.mp4').output('dummy2.mp4')
    assert out_file.get_args() == ['-i', 'dummy.mp4', 'dummy2.mp4']

def test__output__bitrate():
    args = (
        ffmpeg.input('in')
        .output('out', video_bitrate=1000, audio_bitrate=200)
        .get_args()
    )
    assert args == ['-i', 'in', '-b:v', '1000', '-b:a', '200', 'out']

@pytest.mark.parametrize('video_size', [(320, 240), '320x240'])
def test__output__video_size(video_size):
    args = ffmpeg.input('in').output('out', video_size=video_size).get_args()
    assert args == ['-i', 'in', '-video_size', '320x240', 'out']
