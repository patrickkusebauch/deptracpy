# Configuration

The configuration file describes your [layers, ruleset](concepts.md) and adjusts
output formatting.

We suggest you also check out [Deptracpy's own configuration](https://github.com/patrickkusebauch/deptracpy/blob/main/deptracpy.yaml)
for checking its own architecture as it uses most available options.

## DepTracPy

### `src`

Defines a list of directories that DepTracPy should analyse

### `layers`

Defines [layers](concepts.md#layers).

### `rulesets`

Defines [rulesets](concepts.md#rulesets).

### `hidden_layers`

Defines a list of names that should not be displayed when using the [GraphViz dot formatter](formatters.md#graphviz-formatters).

