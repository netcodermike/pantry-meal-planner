# Validation

Authoring date: November 6, 2026. Host: Windows. Target: Windows, macOS, Linux desktop.

## Local result

Two Python unit tests passed on the Windows authoring host. Tkinter interactions remain manual.

## Reproducible checks

The GitHub Actions workflow builds/runs the following on `ubuntu-latest`:

```sh
python -m unittest -v
```

## Manual acceptance

Create a fresh store, add ingredients, select multiple recipes, export a shopping list, restart, remove an ingredient, and confirm ranking changes.

A workflow file is not evidence of a passing run. Observed CI run links and source commits are recorded after publication. Native GUI, sound, sleep/resume, and platform permissions require direct target-platform acceptance even when model tests pass.
