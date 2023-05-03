import logging
import sys

from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.argument_parser import ArgumentParser
from deptracpy.Contract.config import DeptracConfig
from deptracpy.OutputFormatter.format import format_output
from deptracpy.Supportive.config_loader import load_config
from deptracpy.Core.Analyser.default_analyser import analyse

from returns.result import Failure, Success, Result
from returns.pipeline import is_successful

_logger = logging.getLogger(__name__)


def parse_args(args: list[str]) -> ArgumentParser:
    parser = ArgumentParser(description="Dependency tracker for Python")
    return parser.parse_args(args)


def setup_logging(parser: ArgumentParser) -> ArgumentParser:
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=parser.loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    return parser


def load_config_wrapper(
    args: ArgumentParser,
) -> Result[tuple[ArgumentParser, DeptracConfig], str]:
    match load_config(args):
        case Success(config):
            return Success((args, config))  # type: ignore
        case Failure(text):
            return Failure(text)  # type: ignore


def analyse_wrapper(
    args: tuple[ArgumentParser, DeptracConfig]
) -> Result[tuple[ArgumentParser, DeptracConfig, AnalysisResult], str]:
    parser, config = args
    result = analyse(config)
    match result:
        case Success(analysis_result):
            return Success((parser, config, analysis_result))  # type: ignore
        case _:
            return result  # type: ignore


def format_output_wrapper(
    args: tuple[ArgumentParser, DeptracConfig, AnalysisResult]
) -> Result[AnalysisResult, str]:
    parser, config, analysis_result = args
    format_output(parser, config, analysis_result)
    return Success(analysis_result)


def determine_exit_code(result: AnalysisResult) -> Result[None, str]:
    num_of_errors = len(result.errors)
    num_of_violations = len(result.violations)
    if num_of_errors > 0 or num_of_violations > 0:
        return Failure(
            f"{num_of_errors} errors and {num_of_violations} violations found in the analysis."
        )
    return Success(None)


def main(args: list[str]) -> None:
    container: Result[list[str], str] = Success(args)
    result = (
        container.map(parse_args)
        .map(setup_logging)
        .bind(load_config_wrapper)
        .bind(analyse_wrapper)
        .bind(format_output_wrapper)
        .bind(determine_exit_code)
    )

    if not is_successful(result):
        print(result.failure())
        sys.exit(1)


def run() -> None:
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
