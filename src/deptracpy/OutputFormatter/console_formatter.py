from typing import List, Dict

from rich.console import Console
from rich.table import Table

from deptracpy.Contract.analysis_result import AnalysisResult, Dependency
from returns.result import Success


def format_console(result: AnalysisResult) -> Success[AnalysisResult]:
    console = Console(color_system="standard")

    # Warnings
    for token, coverage_type in result.uncovered:
        console.print(
            f"[yellow]Warning: [/yellow] Uncovered {coverage_type}: '{token}'\n"
        )

    # Errors
    for message in result.errors:
        console.print(f"[red]Error: [/red] {message}\n")

    # Violations
    violations: Dict[str, List[Dependency]] = {}
    for dependency in result.violations:
        if dependency.source_layer not in violations.keys():
            violations[dependency.source_layer] = []
        violations[dependency.source_layer].append(dependency)

    for source_layer, dependencies in violations.items():
        table = Table(title=source_layer, title_style="bold", show_header=False)
        for dependency in dependencies:
            table.add_row(
                "[red]Violation",
                f"[b]{dependency.target_layer}:[/b] [b yellow]{dependency.reference.source_token}[/b yellow] cannot "
                f"depend on [b yellow]{dependency.reference.target_token}[/b yellow].",
            )
        console.print(table)

    # Final results
    table = Table("", "Count", title="Results", title_style="green")
    table.add_row("[green]Allowed", str(len(result.allowed)))
    table.add_row("[yellow]Warning", str(len(result.uncovered)))
    table.add_row("[red]Violations", str(len(result.violations)))
    table.add_row("[red]Errors", str(len(result.errors)))
    console.print(table)
    return Success(result)
