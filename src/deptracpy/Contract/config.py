from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class CollectorConfig:
    type: str
    path: str


@dataclass(frozen=True)
class LayerConfig:
    name: str
    collectors: List[CollectorConfig]


@dataclass(frozen=True)
class RulesetConfig:
    source_layer: str
    target_layers: List[str]


@dataclass(frozen=True)
class DeptracConfig:
    paths: List[str]
    layers: List[LayerConfig]
    rulesets: List[RulesetConfig]
    hidden_layers: List[str]
