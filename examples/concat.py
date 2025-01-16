from pathlib import Path

import zprp_ffmpeg2
import zprp_ffmpeg2.filter_graph

work_dir = Path(__file__).parent


stream = zprp_ffmpeg2.input(str(work_dir / "input.mp4"), t=5)
stream = zprp_ffmpeg2.fade(stream, type="in", start_frame=0, nb_frames=30)
stream = zprp_ffmpeg2.concat((stream, stream))
stream = zprp_ffmpeg2.output(stream, str(work_dir / "output.mp4"))
zprp_ffmpeg2.run(stream, extra_options=" -y")
