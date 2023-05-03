import argparse
import os
from tap import Tap
from deptracpy import __version__
from typing_extensions import Literal
import logging


def file_exists_for_argparse(x: str) -> str:
    if not os.path.exists(x):
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


class ArgumentParser(Tap):
    loglevel: int = logging.ERROR
    config: str
    formatter: Literal["console", "dot"]

    def configure(self) -> None:
        self.add_argument(
            "--version",
            action="version",
            version=f"deptracpy {__version__}",
        )
        self.add_argument(
            "config",
            help="path to config file",
            type=file_exists_for_argparse,
            metavar="config_file",
            default="deptracpy.yaml",
            nargs="?",
        )
        self.add_argument(
            "-f",
            "--formatter",
            dest="formatter",
            help="formatter",
            default="console",
            nargs="?",
        )
