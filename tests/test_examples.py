from pathlib import Path

import zprp_ffmpeg as ffmpeg
import zprp_ffmpeg.filter_graph
from zprp_ffmpeg import get_args


def test_concat_fade_duplicate():
    stream = ffmpeg.input(str("input.mp4"))
    stream = ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
    stream = ffmpeg.concat((stream, stream))
    stream = ffmpeg.output(stream, str("output.mp4"))
    assert get_args(stream) == [
        "-i",
        "input.mp4",
        "-i",
        "input.mp4",
        "-filter_complex",
        '"[0:v]fade=type=in:nb_frames=30[v0];',
        '[1:v]fade=type=in:nb_frames=30[v1];',
        '[v0][v1]concat[v2]"',
        '-map',
        '[v2]',
        'output.mp4'
    ]

