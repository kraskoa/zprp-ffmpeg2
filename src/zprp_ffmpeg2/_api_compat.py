"""compatibility layer to match the kkroening library.
@TODO: better docstrings"""

from functools import singledispatch
from typing import List
from typing import Tuple

from zprp_ffmpeg2.base_connector import BaseConnector

from .filter_graph import Filter
from .filter_graph import FilterOption
from .filter_graph import MergeOutputFilter
from .filter_graph import SinkFilter
from .filter_graph import SourceFilter
from .filter_graph import Stream
from .process_connector import ProcessConnector


# this one is unique, creates the Stream object
def input(filename: str, **kwargs) -> Stream:
    source = SourceFilter(filename, **kwargs)
    return Stream().append(source)


def filter(stream_spec: Stream, filter_name: str, *args, **kwargs) -> Stream:
    """Applies a custom filter"""
    options = []
    for arg in args:
        options.append(FilterOption(arg, None))
    for name, value in kwargs.items():
        options.append(FilterOption(name, value))
    new_stream = stream_spec.append(Filter(filter_name, params=options))
    return new_stream


def output(stream: Stream, filename: str) -> Stream:
    sink = SinkFilter(filename)
    new_stream = stream.append(sink)
    return new_stream


def global_args(stream: Stream, *args) -> Stream:
    new_args: List[str] = []
    for arg in args:
        new_args.append(str(arg))
    stream.global_options = new_args
    return stream


@singledispatch
def get_args(arg):
    return "Unknown type"


@get_args.register(Stream)
def _(stream: Stream, overwrite_output: bool = False) -> List[str]:
    """Build command-line arguments to be passed to ffmpeg."""
    args = ProcessConnector.compile(stream).split()
    if overwrite_output:
        args += ["-y"]
    return args


@get_args.register(list)
def _(streams: list[Stream], overwrite_output: bool = False) -> List[str]:
    """Build command-line arguments to be passed to ffmpeg."""
    args = []
    for stream in streams:
        args.extend(ProcessConnector.compile(stream).split())
    if overwrite_output:
        args += ["-y"]
    return args


def compile(stream: Stream, cmd: str = "ffmpeg", overwrite_output: bool = False) -> List[str]:
    """Returns command-line for invoking ffmpeg split by space"""
    return [cmd, *get_args(stream, overwrite_output)]


# this api always uses process
def run(stream: Stream, extra_options: str = "") -> Tuple[bytes, bytes]:
    """Returns (stdout,stderr) tuple"""
    return ProcessConnector.run(stream, extra_options).communicate()


# this api always uses process
def run_async(stream: Stream) -> BaseConnector:
    """Returns handle to a process. Can raise an exception if script tries to terminate before ffmpeg is done."""
    return ProcessConnector.run(stream)


def overwrite_output(stream: Stream) -> Stream:
    stream.global_options.append("-y")
    return stream


def merge_outputs(*streams: Stream) -> Stream:
    """Include all given outputs in one ffmpeg command line"""
    return Stream().append(MergeOutputFilter(streams))
