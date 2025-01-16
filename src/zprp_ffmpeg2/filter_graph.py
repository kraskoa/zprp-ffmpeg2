"""There is no general 'Node' class, because it doesn't work well with object relations, source and sink filters are kind of orthogonal.
It slightly violates DRY, but the parameter types are different. It is what it is"""

from collections import OrderedDict
from copy import deepcopy
from dataclasses import dataclass
from enum import Enum
from typing import Any
from typing import Dict
from typing import Iterable
from typing import List
from typing import Optional
from typing import Union

from ordered_set import OrderedSet


class FilterType(Enum):
    VIDEO = "AVMEDIA_TYPE_VIDEO"
    AUDIO = "AVMEDIA_TYPE_AUDIO"

    @classmethod
    def to_command_string(cls, value: Any) -> str:
        return ":v]" if value == FilterType.VIDEO.value else ":a]" if value == FilterType.AUDIO.value else ""


@dataclass
class FilterOption:
    name: str
    value: Any


@dataclass
class ComplexCommand:
    command: str = ""
    file: Optional[str] = None
    params: str = ""
    filter_type: str = ""
    filter_type_command: str = ""
    kwargs: str = ""


@dataclass
class MergeOutputCommand(ComplexCommand):
    inputs: str = ""
    outputs: str = ""


class Filter:
    """Filters can have many inputs and many outputs, holds the filter name and potential params"""

    def __init__(self, command: str, params: Optional[List[FilterOption]] = None, filter_type: str = FilterType.VIDEO.value):
        self._out: List[AnyNode] = []
        self._in: List[AnyNode | "Stream"] = []
        self.command = command
        self.params = params if params else []
        self.filter_type = filter_type

    def add_output(self, parent: "Filter | SinkFilter"):
        self._out.append(parent)

    def add_input(self, child: "Filter | SourceFilter | Stream"):
        self._in.append(child)

    def get_command(self):
        joined_params = ":".join(p.name + "=" + str(p.value) for p in self.params if p.value)
        if joined_params:  # if there was no option, leave empty string
            joined_params = "=" + joined_params
        filter_type_command = FilterType.to_command_string(self.filter_type)
        return ComplexCommand(
            command=self.command,
            params=joined_params,
            filter_type=self.filter_type,
            filter_type_command=filter_type_command,
        )


# names as per ffmpeg documentation
class SourceFilter:
    def __init__(self, in_path: str, **kwargs):
        self.in_path: str = in_path
        self._out: List[Union["Filter", "SinkFilter"]] = []
        self.kwargs = kwargs

    def add_output(self, parent: Union["Filter", "SinkFilter"]):
        self._out.append(parent)

    def add_input(self, child: "Filter"):
        raise NotImplementedError("This node can't have inputs")

    def get_command(self) -> ComplexCommand:
        return ComplexCommand(
            kwargs=convert_kwargs_to_cmd_args(self.kwargs),
            file=self.in_path,
        )


class SinkFilter:
    def __init__(self, out_path: str):
        self.out_path: str = out_path
        self._in: List[Union["Filter", "SourceFilter"]] = []
        self._out: List[Union["Filter", "MergeOutputFilter"]] = []

    def add_input(self, parent: Union["Filter", "SourceFilter"]):
        self._in.append(parent)

    def add_output(self, child: Union["Filter", "MergeOutputFilter"]):
        if isinstance(child, MergeOutputFilter):
            self._out.append(child)
        raise NotImplementedError("This node can't have outputs")

    def get_command(self) -> ComplexCommand:
        return ComplexCommand(
            file=self.out_path,
        )


# in python 3.12 there is 'type' keyword, but we are targetting 3.8
# https://stackoverflow.com/questions/76712720/typeerror-unsupported-operand-types-for-type-and-nonetype
# python >3.9 uses , instead of | idk if it works with python 3.12
AnyNode = Union[Filter, SourceFilter, SinkFilter]


class Stream:
    def __init__(self) -> None:
        self._nodes: List[Union[Filter, SourceFilter, SinkFilter]] = []
        self.global_options: List[str] = []

    def append(self, node: Union[Filter, SourceFilter, SinkFilter, "MergeOutputFilter"]) -> "Stream":
        # Create a deepcopy of the current instance
        new_stream = deepcopy(self)
        if len(new_stream._nodes) > 0:
            # Connect the last node to the new one
            if not isinstance(new_stream._nodes[-1], SinkFilter) and not isinstance(node, SourceFilter):
                new_stream._nodes[-1].add_output(node)
                node.add_input(new_stream._nodes[-1])
        # Append the new node
        new_stream._nodes.append(node)
        return new_stream  # Return the new instance

    def output(self, out_path: str) -> "Stream":
        # Add a SinkFilter and return a new Stream
        sink = SinkFilter(out_path)
        return self.append(sink)


class MergeOutputFilter:
    """Represents a filter that merges multiple streams into one.

    Attributes:
        streams (Iterable[Stream]): The streams to be merged.
        _in (List[Union[Filter, SourceFilter, SinkFilter]]): List of input nodes connected to this merge filter.
    """

    def __init__(self, streams: Iterable[Stream]):
        self.streams = streams
        self._in: List[Union["Filter", "SourceFilter", "SinkFilter"]] = []

    def add_output(self, parent: "Filter"):
        raise NotImplementedError("This node can't have outputs")

    def add_input(self, child: "Filter"):
        raise NotImplementedError("This node can't have inputs")

    def get_command(self) -> ComplexCommand:
        """Method only made for compatibility with other nodes in FilterParser.
        Returns empty command, which is not used in practice.
        """
        return MergeOutputCommand()


class FilterParser:
    def __init__(self):
        self.multi_input = ["concat", "overlay"]
        self.inputs_counter = 0
        self.outputs_counter = 0
        self.filter_counter = 0
        self.result_counter = 0
        self.merge_counter = 0

        self.inputs = []
        self.outputs = []
        self.filters = []
        self.input_file_to_index = OrderedDict()

    def generate_command(self, stream: Stream, last=None) -> str:  # type: ignore
        for node in stream._nodes:
            command_obj = node.get_command()
            command = command_obj.command
            filter_type_command = command_obj.filter_type_command
            params = command_obj.params
            map_cmd = "-map"
            i_cmd = "-i"
            file = command_obj.file

            # many inputs one output
            if any(filter_ in command for filter_ in self.multi_input):
                last_results = []
                for graph in node._in:  # type: ignore
                    last_results.append(self.generate_command(graph))  # type: ignore
                results = "".join([f"[{result}]" for result in last_results])
                self.filters.append(f"{results}{command}{params}[v{self.result_counter}];")
                last = f"v{self.result_counter}"
                self.result_counter += 1
            # input
            elif isinstance(node, SourceFilter):
                kwargs = command_obj.kwargs
                if file not in self.input_file_to_index:
                    self.input_file_to_index[file] = len(self.input_file_to_index)
                    self.inputs.append(f"{kwargs} {i_cmd} {file}")
                last = self.input_file_to_index[file]
                continue
            # output
            elif isinstance(node, SinkFilter):
                if last == 0 or (len(self.input_file_to_index) == 1 and isinstance(last, int)):
                    self.outputs.append(f"{file}")
                elif isinstance(last, int) and len(self.input_file_to_index) > 1:
                    self.outputs.append(f"{map_cmd} {last} {file}")
                elif len(self.input_file_to_index) > 1 or isinstance(last, str):
                    self.outputs.append(f"{map_cmd} [{last}] {file}")
                self.outputs_counter += 1
                continue
            # single input single output
            # merge output
            elif isinstance(node, MergeOutputFilter):
                merge_last = None
                for sub_stream in node.streams:
                    merge_last = self.generate_command(sub_stream, merge_last)
                    last = merge_last
                    self.outputs_counter = 0
                    self.filter_counter = 0
                    self.result_counter = 0
                self.merge_counter += 1
                continue
            else:
                if isinstance(last, int):
                    self.filters.append(f"[{last}{filter_type_command}{command}{params}[v{self.result_counter}];")
                else:
                    self.filters.append(f"[{last}{command}{params}[v{self.result_counter}];")
                last = f"v{self.result_counter}"
                self.result_counter += 1

        if len(self.filters) == 0 and not all(isinstance(node, (SourceFilter, SinkFilter)) for node in stream._nodes):
            return ""
        return last

    def generate_result(self, stream: Stream) -> str:
        self.generate_command(stream)

        if self.merge_counter == 1:
            for node in stream._nodes:
                if isinstance(node, MergeOutputFilter):
                    break
            if len(self.filters) == 0:
                return " ".join(list(OrderedSet(self.inputs))) + " " + " ".join(self.outputs) + " " + " ".join(stream.global_options)

            return (
                " ".join(list(OrderedSet(self.inputs)))
                + ' -filter_complex "'
                + " ".join(self.filters)[:-1]
                + '" '
                + " ".join(self.outputs)
                + " "
                + " ".join(stream.global_options)
            )

        elif len(self.filters) == 0:
            return " ".join(self.inputs) + " " + self.outputs[-1].split()[-1] + " " + " ".join(stream.global_options)

        return (
            " ".join(self.inputs)
            + ' -filter_complex "'
            + " ".join(self.filters)[:-1]
            + '" '
            + " ".join(self.outputs)
            + " "
            + " ".join(stream.global_options)
        )


def convert_kwargs_to_cmd_args(kwargs: Dict[str, Any]) -> str:
    """Converts keyword arguments to FFmpeg command-line arguments.

    Args:
        kwargs (Dict[str, Any]): Dictionary of keyword arguments.

    Returns:
        str: A string of command-line arguments suitable for FFmpeg.
    """
    args = []
    for k, v in kwargs.items():
        if isinstance(v, bool):
            prefix = "" if v else "no"
            args.append(f"-{prefix}{k}")
            continue
        args.append(f"-{k}")
        args.append(str(v))
    return " ".join(args)
