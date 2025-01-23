from pathlib import Path

import zprp_ffmpeg2
import zprp_ffmpeg2.filter_graph

work_dir = Path(__file__).parent


stream = zprp_ffmpeg2.input(str(work_dir / "jelly.mp4"), t=5)
stream = zprp_ffmpeg2.dblur(stream)
stream2 = zprp_ffmpeg2.input(str(work_dir / "jelly.mp4"), t=5)
stream2 = zprp_ffmpeg2.edgedetect(stream2)
stream = zprp_ffmpeg2.concat((stream, stream2))
out1 = zprp_ffmpeg2.output(stream, str(work_dir / "new_out1.mp4"))
stream = zprp_ffmpeg2.fade(stream, type="in", start_frame=0, nb_frames=30)
out2 = zprp_ffmpeg2.output(stream, str(work_dir / "new_out2.mp4"))
stream = zprp_ffmpeg2.hflip(stream)
out3 = zprp_ffmpeg2.output(stream, str(work_dir / "new_out3.mp4"))
merged = zprp_ffmpeg2.merge_outputs(out1, out2, out3)
zprp_ffmpeg2.view(merged)
# zprp_ffmpeg2.run(merged, extra_options=" -y")
