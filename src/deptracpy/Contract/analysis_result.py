from dataclasses import dataclass
from typing import List, Set


@dataclass(frozen=True)
class Reference:
    source_token: str
    target_token: str


@dataclass(frozen=True)
class Dependency:
    reference: Reference
    source_layer: str
    target_layer: str


@dataclass(frozen=True)
class Error:
    name: str
    text: str


class AnalysisResult:
    allowed: List[Dependency]
    uncovered: Set[tuple[str, str]]  # target_token, type
    violations: List[Dependency]
    errors: List[Error]

    def __init__(self) -> None:
        self.allowed = []
        self.uncovered = set()
        self.violations = []
        self.errors = []

    def add_allowed(self, dependency: Dependency) -> None:
        self.allowed.append(dependency)

    def add_uncovered(self, target_token: str, type: str) -> None:
        self.uncovered.add((target_token, type))

    def add_violation(self, dependency: Dependency) -> None:
        self.violations.append(dependency)

    def add_error(self, error: Error) -> None:
        self.errors.append(error)
