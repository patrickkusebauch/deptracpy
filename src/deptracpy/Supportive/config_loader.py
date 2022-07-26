import pathlib
from typing import Tuple

import yaml

from deptracpy.Contract.argument_parser import ArgumentParser
from deptracpy.Contract.config import (
    DeptracConfig,
    CollectorConfig,
    LayerConfig,
    RulesetConfig,
)
from returns.result import Failure, Success, Result


def load_from_yaml_file(file: str) -> DeptracConfig:
    try:
        config = yaml.safe_load(open(file, "r"))
        layers = []
        for layer in config.get("layers"):
            collectors = []
            for collector in layer["collectors"]:
                collectors.append(CollectorConfig(collector["type"], collector["path"]))
            layers.append(LayerConfig(layer["name"], collectors))
        rulesets = []
        for ruleset_name, target_layers in config.get("rulesets").items():
            rulesets.append(RulesetConfig(ruleset_name, target_layers))

        return DeptracConfig(
            config.get("paths"), layers, rulesets, config.get("hidden_layers")
        )
    except yaml.YAMLError as exc:
        raise RuntimeError("Could not load config file") from exc


def load_config(
    args: ArgumentParser,
) -> Result[Tuple[ArgumentParser, DeptracConfig], str]:
    extension: str = pathlib.Path(args.config).suffix
    match extension:
        case (".yaml" | ".yml"):
            return Success((args, load_from_yaml_file(args.config)))
        case _:
            return Failure(f"Unrecognized config file extension: {extension}")
