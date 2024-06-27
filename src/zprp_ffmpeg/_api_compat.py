"""compatibility layer to match the kkroening library.
@TODO: better docstrings"""

from typing import List, Union, Unpack
from typing import Tuple

from zprp_ffmpeg.BaseConnector import BaseConnector

from .FilterGraph import Filter
from .FilterGraph import FilterOption
from .FilterGraph import SinkFilter
from .FilterGraph import SourceFilter
from .FilterGraph import Stream
from .ProcessConnector import ProcessConnector


# this one is unique, creates the Stream object
def input(filename: str):
    source = SourceFilter(filename)
    return Stream().append(source)


def filter(stream_spec: Stream, filter_name: str, *args, **kwargs):
    """Applies a custom filter"""
    options = []
    for arg in args:
        options.append(FilterOption(arg, None))
    for name, value in kwargs.items():
        options.append(FilterOption(name, value))
    return stream_spec.append(Filter(filter_name, params=options))


T = tuple[Unpack[tuple[Stream, ...]], str]


def output(*streams_and_filename: Unpack[T]) -> Stream:
    *streams, filename = streams_and_filename
    sink = SinkFilter(filename)
    nodes = []
    for stream in streams:
        sink.add_input(stream)
    nodes.append(sink)
    s = Stream()
    s._nodes = nodes
    return s


def global_args(stream: Stream, *args):
    new_args: List[str] = []
    for arg in args:
        new_args.append(str(arg))
    stream.global_options = new_args
    return stream


def get_args(stream: Stream, overwrite_output: bool = False) -> List[str]:
    """Build command-line arguments to be passed to ffmpeg."""
    args = ProcessConnector.compile(stream).split()
    if overwrite_output:
        args += ["-y"]
    return args


def compile(stream: Stream, cmd: str = "ffmpeg", overwrite_output: bool = False) -> List[str]:
    """Returns command-line for invoking ffmpeg split by space"""
    return [cmd, *get_args(stream, overwrite_output)]


# this api always uses process
def run(stream: Stream, extra_options: str = "") -> Tuple[str, str]:
    """Returns (stdout,stderr) tuple"""
    return ProcessConnector.run(stream, extra_options).communicate()


# this api always uses process
def run_async(stream: Stream) -> BaseConnector:
    """Returns handle to a process. Can raise an exception if script tries to terminate before ffmpeg is done."""
    return ProcessConnector.run(stream)
