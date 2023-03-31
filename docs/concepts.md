# Core concepts

At the heart of DepTracPy are three main concepts:

* [**Layers**](#layers) are groups of files that you define
* [**Rulesets**](#rulesets) describe which layers a layer can communicate with
* **Violations** show when a layer uses files from another
  layer that is forbidden by the currently configured rulesets.

## Layers

DepTracPy allows you to group different tokens(files) into *layers*. Technically layers are nothing more than a
collection of those tokens.

Each layer has a unique name and a list of one or more collectors, which will
look for tokens should be assigned to this layer.

If you want to ensure your application follows the MVC architecture pattern then
you can create a config file that makes sure a `View` does not directly interact
with a `Controller` or that `Models` are independent of both `Views` and `Controllers`.

DepTracPy allows you to visualize and enforce a ruleset based on such layer
information.

**By default, all dependencies between layers are forbidden!**

### Collecting Layers

If your application has `Controllers` and `Models`, DepTracPy allows you to group
them into layers.

```yaml
paths:
  - src

layers:
  - name: Models
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Models'
  - name: Controllers
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Controllers'
ruleset: [ ]
```

At first, lets take a closer look at the first layer (named **Models**).

Here we decided that our software has some kind of layer called **Models**. You
assign tokens to this layer with the help of [*Collectors*](collectors.md).

Collectors are responsible for taking a closer look at your code and decide if a
token is part of a layer. By using the `ModuleRecursive` collector you can define a module prefix.
File in that module and its submodules becomes part of the assigned layer. In this
example we define that every file in the `myapp.Models` module will be a
part of the **Model** layer.

Every file matching `myapp.Controllers` module will become a part of the **Controller** layer.

As we defined our layers, we can generate a dependency graph for the example configuration:
(Make sure [*Graphviz*](index.md#optional-dependency-graphviz) (dot) is installed on your system)

```bash
deptracpy --formatter=dot
```

## Rulesets

Allowed dependencies between layers are configured in a *ruleset*.

By default, DepTracPy will raise a violation for every dependency between layers.
In real software you want to allow dependencies between different kinds of
layers.

As a lot of architectures define some kind of *controllers*, *services* and
*repositories*, a natural approach for this would be to define these rules:

- *Controllers* may access *services*, but not *repositories*.
- *Services* may access *repositories*, but not *controllers*.
- *Repositories* neither may access services nor *controllers*.

We can define this using the following configuration:

```yaml
# deptracpy.yaml
paths:
  - src

layers:
  - name: Controllers
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Controller'
  - name: Service
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Service'
  - name: Repository
    collectors:
      - type: ModuleRecursive
        path: 'myapp.Repository'
ruleset:
  Controller:
    - Service
  Service:
    - Repository
  Repository: ~
```

Take a closer look at the ruleset. We allow the *Controller* layer to access
*Service* and *Service* can access *Repository*, but *Repository* may not access
any of the two other layers.

### Different Layers and Different Views

In the example above we defined 3 different layers (*controller*, *repository*
and *service*). DepTracPy gives architects the power to define what kind of layers
exist.

Typical use cases are:

- caring about layers in different architectures (tier, hexagonal, ddd, ...)
- caring about dependencies between different kinds of services (infrastructure
  services / domain services / entities / DTOs / ...)
- caring about coupling to third party code like composer vendors, frameworks,
  ...
- enforcing naming conventions
- ...

Typically, software has more than just one view. **It is possible to use multiple
config files, to take care about different architectural views.**
