from pathlib import Path

import zprp_ffmpeg
import zprp_ffmpeg.filter_graph

work_dir = Path(__file__).parent


# stream = zprp_ffmpeg.input(str(work_dir / "input.mp4"))
# stream = zprp_ffmpeg.scale(stream, w="20", h="20")
# stream = zprp_ffmpeg.hflip(stream)
# stream = zprp_ffmpeg.output(stream, str(work_dir / "output.mp4"))
# zprp_ffmpeg.view(stream)

in_ = zprp_ffmpeg.input("in.mp4")
stream = zprp_ffmpeg.hflip(in_)
out1 = stream.output("out.mp4")
zprp_ffmpeg.view(out1)

in_ = zprp_ffmpeg.input("in.mp4")
stream = zprp_ffmpeg.hflip(in_)
stream = zprp_ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
out1 = stream.output("out1.mp4")
stream = zprp_ffmpeg.hflip(stream)
out2 = stream.output("out2.mp4")
merged = zprp_ffmpeg.merge_outputs(out1, out2)
zprp_ffmpeg.view(merged)

stream = zprp_ffmpeg.input("in.mp4", t=5)
stream2 = zprp_ffmpeg.input("in2.mp4")
stream = zprp_ffmpeg.fade(stream, type="in", start_frame=0, nb_frames=30)
stream = zprp_ffmpeg.concat((stream, stream2))
stream = zprp_ffmpeg.output(stream, "out.mp4")
zprp_ffmpeg.view(stream)
