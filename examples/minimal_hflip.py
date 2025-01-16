import zprp_ffmpeg2

stream = zprp_ffmpeg2.input("input.mp4")
stream = zprp_ffmpeg2.hflip(stream)
stream = zprp_ffmpeg2.output(stream, "output.mp4")
zprp_ffmpeg2.run(stream)
