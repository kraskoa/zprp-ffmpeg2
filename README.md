# ZPRP 24Z project repository
# Further development of zprp-ffmpeg library

## Design proposal

### Schedule
- (27.10 - 03.11) Getting to know current functionalities of the zprp-ffmpeg library
- (03.11 - 17.11) Extending test coverage of existing functionalities to potentially uncover errors
- (17.11 - 24.11) Fixing the string-based outputs processing from Node.get_command()
- (24.11 - 08.12) Working on multiple input sources support like in ffmpeg-python
- (24.11 - 08.12) Working on support for merging multiple output streams, also like in ffmpeg-python
- (08.12 - 22.12) Working on covering the missing full compatibility with ffmpeg-python API
- (22.12 - 12.01) Writing tests to cover newly added functionalities
- (12.01 - 19.01) Updating documentation to fix shortcomings and cover new functions

### Planned changes to the existing library

- Further improvements to cover all the functionality of the ffmpeg-python API
- Add multi-input sources support (ffmpeg.input())
- Add multi-output merging support (ffmpeg.merge_outputs())
- Extend existing testing to cover more functionality of the ffmpeg-python library
- Achieve full compatibility with ffmpeg-python library tests
- In [filters source file](src/zprp_ffmpeg/filter_graph.py) change the way outputs from get_command() are processed - refrain from returning strings
- Updating the documentation to include implemented changes
- Adding more detailed architecture description to explain the responsibilities of different components

### Technological stack remains the same as the one used in zprp-python