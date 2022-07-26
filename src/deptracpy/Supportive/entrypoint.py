import logging
import sys
from typing import List

from deptracpy.Contract.analysis_result import AnalysisResult
from deptracpy.Contract.argument_parser import ArgumentParser
from deptracpy.OutputFormatter.format import format_output
from deptracpy.Supportive.config_loader import load_config
from deptracpy.Core.Analyser.default_analyser import analyse

from returns.result import Failure, Success, Result
from returns.pipeline import is_successful

_logger = logging.getLogger(__name__)


def parse_args(args: List[str]) -> ArgumentParser:
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


def determine_exit_code(result: AnalysisResult) -> Result[AnalysisResult, str]:
    num_of_errors = len(result.errors)
    num_of_violations = len(result.violations)
    if num_of_errors > 0 or num_of_violations > 0:
        return Failure(
            f"{num_of_errors} errors and {num_of_violations} violations found in the analysis."
        )
    return Success(result)


def main(args: List[str]) -> None:
    container: Result[List[str], str] = Success(args)
    result = (
        container.map(parse_args)
        .map(setup_logging)
        .bind(load_config)
        .bind(analyse)
        .bind(format_output)
        .bind(determine_exit_code)
    )

    if not is_successful(result):
        print(result.failure())
        sys.exit(1)


def run() -> None:
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
