# Collectors

Collectors decide if a node (typically a file) is part of a layer. You can use
multiple different collectors for a layer.

## `ModuleRecursive` Collector

The `ModuleRecursive` collector finds all files in the given module and all its submodules

```yaml
layers:
  - name: Contract
    collectors:
      - type: Module
        path: 'deptracpy'
```

## `Module` Collector

The `Module` collector finds all files in the given module but does NOT search through submodules/subdirectories. 

```yaml
layers:
  - name: Contract
    collectors:
      - type: Module
        path: 'deptracpy'
```