from typing import Tuple

from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.config import DeptracConfig
from .console_formatter import format_console
from .dot_formatter import format_dot
from returns.result import Result, Failure

from deptracpy.Contract.argument_parser import ArgumentParser


# todo: @Investigate: Can I validate formatter type at start-up instead? By now a lot of work has been done that goes
#  to waste otherwise (patrick @ 2023-03-25)
def format_output(
    args: Tuple[ArgumentParser, DeptracConfig, AnalysisResult]
) -> Result[AnalysisResult, str]:
    parser, config, result = args
    match parser.formatter:
        case "console":
            return format_console(result)
        case "dot":
            return format_dot(result, config)
        case _:
            return Failure(f"Unrecognized formatter '{parser.formatter}'")
