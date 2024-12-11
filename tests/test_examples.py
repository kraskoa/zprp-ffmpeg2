
import zprp_ffmpeg as ffmpeg
import zprp_ffmpeg.filter_graph
from zprp_ffmpeg import get_args


def test_concat_fade_duplicate():
    stream = ffmpeg.input("input.mp4")
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream))
    stream = ffmpeg.output(stream, "output.mp4")
    assert get_args(stream) == [
        "-i",
        "input.mp4",
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0];',
        "[1:v]fade=type=in:nb_frames=30[v1];",
        '[v0][v1]concat[v2]"',
        "-map",
        "[v2]",
        "output.mp4"
    ]


def test_concat_fade_duplicate_with_time_parameter5():
    stream = ffmpeg.input("input.mp4", t=5)
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream))
    stream = ffmpeg.output(stream, "output.mp4")
    assert get_args(stream) == [
        "-t",
        "5",
        "-i",
        "input.mp4",
        "-t",
        "5",
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0];',
        "[1:v]fade=type=in:nb_frames=30[v1];",
        '[v0][v1]concat[v2]"',
        "-map",
        "[v2]",
        "output.mp4"
    ]


def test_concat_bool_kwarg_true():
    stream = ffmpeg.input("input.mp4", foo=True)
    stream = ffmpeg.concat((stream, stream))
    stream = ffmpeg.output(stream, "output.mp4")
    assert get_args(stream) == [
        "-foo",
        "-i",
        "input.mp4",
        "-foo",
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0][1]concat[v0]"',
        "-map",
        "[v0]",
        "output.mp4"
    ]

def test_fade_bool_kwargs_false():
    stream = ffmpeg.input("input.mp4", foo=False)
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.output(stream, "output.mp4")
    assert get_args(stream) == [
        "-nofoo",
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0]"',
        "-map",
        "[v0]",
        "output.mp4"
    ]
