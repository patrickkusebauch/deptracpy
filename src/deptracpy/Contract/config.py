from dataclasses import dataclass


@dataclass(frozen=True)
class CollectorConfig:
    type: str
    path: str


@dataclass(frozen=True)
class LayerConfig:
    name: str
    collectors: list[CollectorConfig]


@dataclass(frozen=True)
class RulesetConfig:
    source_layer: str
    target_layers: list[str]


@dataclass(frozen=True)
class DeptracConfig:
    paths: list[str]
    layers: list[LayerConfig]
    rulesets: list[RulesetConfig]
    hidden_layers: list[str]
