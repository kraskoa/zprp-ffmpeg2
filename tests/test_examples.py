
import zprp_ffmpeg2 as ffmpeg
import zprp_ffmpeg2.filter_graph
from zprp_ffmpeg2 import get_args


def test_concat_fade_duplicate():
    stream = ffmpeg.input("input.mp4")
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream))
    stream = ffmpeg.output(stream, "output.mp4")
    assert get_args(stream) == [
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0];',
        "[0:v]fade=type=in:nb_frames=30[v1];",
        '[v0][v1]concat[v2]"',
        "-map",
        "[v2]",
        "output.mp4"
    ]


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
        '"[0:v]hflip[v0]"',
        "-map",
        "[v0]",
        "out2.mp4",
        "out1.mp4",
    ]
    assert ffmpeg.get_args([out1, out2]) == [
        "-i",
        "in.mp4",
        "-filter_complex",
        '"[0:v]hflip[v0]"',
        "-map",
        "[v0]",
        "out2.mp4",
        "out1.mp4",
    ]


def test__merge_outputs():
    print("in_")
    in_ = ffmpeg.input("in.mp4")
    print("out1")
    out1 = in_.output("out1.mp4")
    # assert out1.get_args() == ["-i", "in.mp4", "out1.mp4"]
    print("out2")
    out2 = in_.output("out2.mp4")
    # assert out2.get_args() == ["-i", "in.mp4", "out2.mp4"]
    merged = ffmpeg.merge_outputs(out1, out2)
    assert merged.get_args() == ["-i", "in.mp4", "out1.mp4", "out2.mp4"]

    assert (ffmpeg.merge_outputs(out1, out2).get_args() == [
        "-i",
        "in.mp4",
        "out1.mp4",
        "out2.mp4",
    ])
    assert ffmpeg.get_args([out1, out2]) == ["-i", "in.mp4", "out2.mp4", "out1.mp4"]


def test_deep_copy():
    in_ = ffmpeg.input("in.mp4")
    in_flip = ffmpeg.hflip(in_)
    out1 = in_.output("out1.mp4")
    assert out1.get_args() == ["-i", "in.mp4", "out1.mp4"]
    out2 = in_flip.output("out2.mp4")
    assert out2.get_args() == ["-i", "in.mp4", "-filter_complex", '"[0:v]hflip[v0]"', "-map", "[v0]", "out2.mp4"]


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
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0];',
        "[0:v]fade=type=in:nb_frames=30[v1];",
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
        "-filter_complex",
        '"[0][0]concat[v0]"',
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
