# StockTextMining

Fall 2020 Independent Study - Allegheny College. WIP text mining tool used to predict stock swings.

## Objectives

- Complete research in the area of the Stock Market and what text mining tools are being used to predict it's trends.
- Create a tool that downloads and archives news articles about specific stocks (chosen by the user) and then analyzes them to predict potential market swings.

## Running the Program using Pipenv
Make sure Python(3) and Pipenv are installed on your machine. Find information on installing pipenv [here](https://pipenv-fork.readthedocs.io/en/latest/install.html).

### Pipenv

The project comes with a `Pipfile` in the `src` directory that will install the necessary packages for the program, making it easy for users with Pipenv to run the project on their machines.

First navigate to the `src` directory using `cd src`. Then run the command `pipenv lock` to install the necessary Python packages.

You can then run the command `pipenv run python3 run_tool.py` to run the program. You will be presented with the option to run either the UI web interface or the Command Line Interface.
