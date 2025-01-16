from pathlib import Path

import zprp_ffmpeg2
import zprp_ffmpeg2.filter_graph

work_dir = Path(__file__).parent


# stream = zprp_ffmpeg2.input(str(work_dir / "input.mp4"))
# stream = zprp_ffmpeg2.scale(stream, w="20", h="20")
# stream = zprp_ffmpeg2.hflip(stream)
# stream = zprp_ffmpeg2.output(stream, str(work_dir / "output.mp4"))
# zprp_ffmpeg2.view(stream)

in_ = zprp_ffmpeg2.input("in.mp4")
stream = zprp_ffmpeg2.hflip(in_)
out1 = stream.output("out.mp4")
zprp_ffmpeg2.view(out1)

in_ = zprp_ffmpeg2.input("in.mp4")
stream = zprp_ffmpeg2.hflip(in_)
stream = zprp_ffmpeg2.fade(stream, type="in", start_frame=0, nb_frames=30)
out1 = stream.output("out1.mp4")
stream = zprp_ffmpeg2.hflip(stream)
out2 = stream.output("out2.mp4")
merged = zprp_ffmpeg2.merge_outputs(out1, out2)
zprp_ffmpeg2.view(merged)

stream = zprp_ffmpeg2.input("in.mp4", t=5)
stream2 = zprp_ffmpeg2.input("in2.mp4")
stream = zprp_ffmpeg2.fade(stream, type="in", start_frame=0, nb_frames=30)
stream = zprp_ffmpeg2.concat((stream, stream2))
stream = zprp_ffmpeg2.output(stream, "out.mp4")
zprp_ffmpeg2.view(stream)
