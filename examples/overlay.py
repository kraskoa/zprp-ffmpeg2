from pathlib import Path

import zprp_ffmpeg2
import zprp_ffmpeg2.filter_graph

work_dir = Path(__file__).parent


stream = zprp_ffmpeg2.input(str(work_dir / "in.mp4"))
image = zprp_ffmpeg2.input(str(work_dir / "ffmpeg_logo.jpg"))
stream = zprp_ffmpeg2.overlay(stream, image, x="20", y="20")
stream = zprp_ffmpeg2.output(stream, str(work_dir / "output.mp4"))
zprp_ffmpeg2.run(stream, extra_options=" -y")
