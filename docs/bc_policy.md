# Backwards Compatibility Policy

DepTracPy adheres to [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).
That means, we will not introduce any breaking change in a minor or patch
release starting with the first stable release 1.0.0. Within the 0.x.y major
release, we may introduce breaking changes in minor releases.

> Given a version number MAJOR.MINOR.PATCH, increment the:
>
> 1. MAJOR version when you make incompatible API changes
> 2. MINOR version when you add functionality in a backwards compatible manner
> 3. PATCH version when you make backwards compatible bug fixes

## Security

Security fixes may break backwards compatibility at any point. For more details
on security related issues, please refer to the [Security Guide](SECURITY.md).