# DepTracPy

DepTracPy is a static code analysis tool for Python that helps you communicate, visualize and enforce architectural
decisions in your projects. You can freely define your architectural layers over modules and which rules should apply 
to them. It is a sister project to a same tool written for PHP - [Deptrac](https://github.com/qossmic/deptrac).

For example, you can use DepTracPy to ensure that packages/modules in your project are truly independent of each other 
to make them easier to test and reuse.

DepTracPy can be used in a CI pipeline to make sure a pull request does not violate any of the architectural rules you
defined. With the optional Graphviz formatter you can visualize your layers, rules and violations.

- [User docs](docs/index.md)
- [Contributing](docs/CONTRIBUTING.md)
