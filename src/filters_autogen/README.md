# Automatyczne wykrywanie filtrów

Ta część kodu nie należy do paczki, generuje część kodu na podstawie kodu źródłowego FFmpeg.

Aby wygenerować filtry należy sklonować repozytorium pycparser (potrzebne są dodatkowe nagłówki) oraz ffmpeg w odpowiedniej wersji:
```
git clone https://github.com/FFmpeg/FFmpeg.git
cd FFmpeg
git checkout n7.0

git clone https://github.com/eliben/pycparser.git
```

Następnie usunąć/zmienić nazwę `libavutil/thread.h` (TODO: czy jest lepsze rozwiązanie?)

```
rm FFmpeg/libavutil/thread.h
```



Następnie uruchomić `generate_filters.py`
