from pathlib import Path

import zprp_ffmpeg as ffmpeg


def merge_outputs():
    # Ścieżka robocza (obecny katalog pliku)
    work_dir = Path(__file__).parent

    # Definicja pliku wejściowego
    input_video = ffmpeg.input(str(work_dir / "in.mp4"))

    # Zastosowanie filtra hflip na pliku wejściowym
    flipped_video = ffmpeg.hflip(input_video)

    # Definicja pierwszego pliku wyjściowego (oryginalny)
    out1 = ffmpeg.output(input_video, str(work_dir / "out1.mp4"))

    # Definicja drugiego pliku wyjściowego (odwrócony)
    out2 = ffmpeg.output(flipped_video, str(work_dir / "out2.mp4"))

    # Łączenie wyjść w jedną komendę
    merged = ffmpeg.merge_outputs(out1, out2)

    # Uruchomienie procesu FFmpeg z opcją nadpisania plików wyjściowych (-y)
    merged.run(extra_options="-y")


def main():
    merge_outputs()


if __name__ == "__main__":
    main()
