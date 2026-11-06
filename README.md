# Pantry Meal Planner

Match recipes against your pantry, build a meal selection, and export the ingredients you still need.

[![Build and verify](https://github.com/netcodermike/pantry-meal-planner/actions/workflows/verify.yml/badge.svg)](https://github.com/netcodermike/pantry-meal-planner/actions/workflows/verify.yml)

**Language:** Python · **Platform:** Windows, macOS, Linux desktop · **App type:** Desktop planning app

First-release learning implementation, with explicit scope below. This is one independently runnable app, not a placeholder in a combined repository.

## Features

- Add and remove pantry ingredients.
- Rank built-in/custom recipes by missing ingredient count.
- Select several meals and export a deduplicated shopping list.
- Save inventory and recipes to a local JSON store.

## Requirements

Python 3.11+ with Tkinter. Python installers for Windows/macOS normally include Tkinter; some Linux distributions package it separately as python3-tk.

## Quick start

```sh
git clone https://github.com/netcodermike/pantry-meal-planner.git
cd pantry-meal-planner
python planner.py
# Optional separate store:
python planner.py --store sample-pantry.json
```

Commands run from the repository root. Lines marked for a particular operating system apply only there. Language tools are prerequisites, not installed by the app. Close desktop windows normally; terminal/server apps stop with Ctrl+C unless their usage notes say otherwise.

## Example workflow

Add `pasta`, `tomato`, and `olive oil`. Tomato pasta should rank first and show “ready to cook.” Select chickpea salad and export a shopping list; it should contain chickpea and cucumber if tomato is already present. Add a custom recipe through the dialog, restart, and verify it persists.

## Architecture, configuration, and data

`planner.py` contains the normalized ingredient matcher, schema validator, atomic JSON writer, and Tkinter view. `test_planner.py` checks recipe ranking, missing ingredients, invalid recipe data, and file round trips. Recipe ranking first minimizes missing ingredients, then maximizes matches, then sorts by name. Data never leaves the machine. The default store is `pantry.json` in the working directory; `--store` changes it. Writes replace a temporary file in the same directory.

## Verification

Build with the quick-start command where needed, then run:

```sh
python -m unittest -v
```

Manual acceptance: Create a fresh store, add ingredients, select multiple recipes, export a shopping list, restart, remove an ingredient, and confirm ranking changes.

See [validation record](docs/VALIDATION.md) for observed checks and their limits. CI results verify only what the workflow runs; they do not establish native GUI correctness or production readiness.

## Limitations and next steps

Ingredient presence is tracked, not quantities, nutritional content, allergens, expiry dates, or portions. Matching is exact after trimming/case folding; no plural or synonym recognition. The app does not provide cooking instructions. Only one instance should edit a store. Failed saves show an error but the in-memory form may retain changes; retry before closing. Shopping exports are text files and may replace the file you choose.

## Troubleshooting

If Tkinter is missing, install the Tk package matching your Python. Start from a graphical desktop. A corrupt store fails explicitly instead of silently resetting it; keep a backup before editing JSON. Choose a writable --store path if saving fails.

## Source map

- `planner.py`
- `test_planner.py`

## Development and license

Read [contributing](CONTRIBUTING.md) before changing the app, and [security/privacy](SECURITY.md) before supplying private data. Use synthetic fixtures for tests. No telemetry, paid API key, or account is required by the app itself. Dependencies, when present, are stated in Requirements.

[MIT license](LICENSE), copyright 2026 netcodermike.
