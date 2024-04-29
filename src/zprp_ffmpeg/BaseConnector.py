from abc import ABC
from abc import abstractmethod

from .FilterGraph import Stream


class BaseConnector(ABC):
    """
    Abstract class for talking with ffmpeg.

    A connector always needs a `run` method to execute something user wants.
    """

    # this is basically a named constructor
    @abstractmethod
    @classmethod
    def run(cls, graph: Stream) -> "BaseConnector":
        """Executes given fliter graph
        :param graph: filter graph describing user operations.

        :return: a handle to read output from ffmpeg, for example stdout from process."""

    @abstractmethod
    def communicate(self):
        pass