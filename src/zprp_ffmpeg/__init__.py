__version__ = "1.2.0"
# from . import longest
from inspect import getmembers
from inspect import isfunction

from zprp_ffmpeg import _api_compat
from zprp_ffmpeg import generated_filters

from ._api_compat import input
from ._api_compat import filter
from ._api_compat import output
from ._api_compat import get_args
from ._api_compat import compile
from ._api_compat import run
from ._api_compat import run_async
from .FilterGraph import Stream
from .filters import hflip
from .generated_filters import *  # noqa: F403 this is impossible to avoid
from .probe import probe
from .view import view

# This is for `from xyz import *`, but also to make linter shut up
__all__ = ["input", "filter", "output", "get_args", "compile", "run", "run_async", "hflip", "probe", "view"]

stream_modules = [generated_filters, _api_compat]

for module in stream_modules:
    for name, func in getmembers(module, isfunction):
        setattr(Stream, name, func)
