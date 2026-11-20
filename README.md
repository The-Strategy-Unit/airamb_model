# Simulation Accelerator Showcase - Air Ambulance Model 

This repository contains the Python code for the Showcase Air Ambulance Model, an open source implementation of Discrete Event Simulation (DES) for the Strategic Commissioning Intelligence Centre's (SCIC) Simulation Accelerator.

## How to run the model locally

### Clone the repository
[Clone a copy](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository) of the repository to your local machine

### Run the model using uv

Our preferred tool for dependency management is [uv](https://github.com/astral-sh/uv). If using this tool:

1. Run the model using `uv run -m airamb_model.main`

### Run the model without uv

1. Open the repository folder. Install the package using `pip install .`
1. Run the model using `python -m airamb_model.main`

## How to run the model using codespaces

This repository can be opened in GitHub Codespaces which allows you to run the model in a cloud container without having to have python installed locally or manage the environment. The Codespace will open with the environment active you can see the environment using pip list. Click the buttone below to open your codespace. You can then run the model using `uv run -m airamb_model.main`.

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/codespaces/new?hide_repo_select=true&ref=main&repo=The-Strategy-Unit/airamb_model).

### Results

Results will be visible in the terminal.
