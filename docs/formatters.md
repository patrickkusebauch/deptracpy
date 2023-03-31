# Formatters

DepTracPy has support for different output formatters with various options.

## Console Formatter

This formatter dumps basic information to *STDOUT*,

## Graphviz Formatter

```
--formatter=dot        Saves the output to a .dot file
```

#### Hide layers in output

Under `hidden_layers` you can define a list of `layers` you do not want to include when using the `dot` output formatter.
The generated image will not contain these layers (unless there is a violation), but they will be part of the analysis.

There are 2 main use-cases for this feature:

- Hiding a generic/general domains like the `vendor` folder
- Having multiple "views" for your architecture. You can define a shared file
  with all your `layers` and a `ruleset` and then have multiple config files for
  the different `hidden_layers`. Using the `dot` formatter with these files
  will then generate graphs focusing on only the relevant layers.

```yaml
paths:
  - src

layers:
  - name: Contract
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Contract'
  - name: Models
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Models'
  - name: Controllers
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Controllers'
ruleset:
  Controllers:
    - Models
    - Contract
  Models:
    - Contract

hidden_layers:
  - Contract
```