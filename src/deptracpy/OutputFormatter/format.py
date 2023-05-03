from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.config import DeptracConfig
from .console_formatter import format_console
from .dot_formatter import format_dot

from deptracpy.Contract.argument_parser import ArgumentParser


def format_output(
    parser: ArgumentParser, config: DeptracConfig, result: AnalysisResult
) -> None:
    match parser.formatter:
        case "console":
            format_console(result)
        case "dot":
            format_dot(result, config)
