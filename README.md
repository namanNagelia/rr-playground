# Airplane Strike Analysis

This project contains a Streamlit dashboard for exploring the airplane-strike dataset. It summarizes incidents by year, state, species, and flight phase, and visualizes the distribution of strike and damage fields, including a map of incidents by state.

## Dataset

The dashboard reads `Airplane Strikes Dataset.csv`, which is checked into this repository. `i.py` locates the CSV relative to its own file, so the app does not depend on the current working directory or a remote dataset URL. Keep the CSV beside `i.py` when running the dashboard.

## Environment setup

The project uses Pipenv and targets Python 3.9. Install the runtime and development dependencies from the Pipfile and lockfile with:

```sh
pipenv install --dev
```

## Run the dashboard

Launch Streamlit from the project environment:

```sh
pipenv run streamlit run i.py
```

Streamlit prints a local URL where the dashboard can be viewed in a browser.

## Run tests

Run the pytest suite, which covers local data loading and the analysis helpers:

```sh
pipenv run pytest
```
