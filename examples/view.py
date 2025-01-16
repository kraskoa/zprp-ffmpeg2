from pathlib import Path

import zprp_ffmpeg2
import zprp_ffmpeg2.filter_graph

work_dir = Path(__file__).parent


stream = zprp_ffmpeg2.input(str(work_dir / "input.mp4"))
stream = zprp_ffmpeg2.scale(stream, w="20", h="20")
stream = zprp_ffmpeg2.output(stream, str(work_dir / "output.mp4"))

zprp_ffmpeg2.view(stream, filename="a.png")
