# StockTextMining

Fall 2020 Independent Study - Allegheny College. WIP text mining tool used to predict stock swings.

## Objectives

- Complete research in the area of the Stock Market and what text mining tools are being used to predict it's trends.
- Create a tool that downloads and archives news articles about specific stocks (chosen by the user) and then analyzes them to predict potential market swings.

## Running the Project

To run the project in it's current state, ensure `Python` and `pipenv` are installed on your machine. Then navigate to the project's `src` directory in your terminal window.

You can then run `pipenv lock` to install the necessary dependencies needed to run the project, in pipenv.

You can then run the project by using the command `pipenv run python3 results_generator.py` Currently the project is just working via command line interface and is outputting the results to a `results.csv` file and the terminal. More updates are coming on this project soon to add more functionality and a streamlined user interface.

<!-- You can then run the project by using the command `pipenv run streamlit run interface.py`. -->

### Running The Program Using Docker

It is easy to run the QAZPLM program on any machine as the project comes with included Docker files that set up environments specific to the user's machine.

First ensure Docker is installed! You can install [Docker from their website](https://www.docker.com).

Then navigate to the `src` directory of the project in your terminal window by running the command `cd src`.

You can then build the Docker container based on your machine.

#### Shortcut to running and building a working container

The following bash scripts simplify building the container.

| OS  | Building  | Running  |
|---|---|---|
| MacOS  		|  `./build_macOS.sh` |  `./run_macOS.sh` |
| Linux   	|  `./build_linux.sh` | `./run_linux.sh`  |
| Windows 	|  `build_win.bat` 		|  `run_win.bat` |


These files may be found in the directory, `docker/` and require the `DockerFile`, which is found in the `src` directory.

We show an example of how to build and run a container for **MacOS** below.

#### Example of and running a Docker container
Again, ensure you are in the `src` directory.

To build the container, `./docker/build_macOS.sh` and to run the container, `./docker/run_macOS.sh`.

### Running the Program using Pipenv
Make sure Python(3) and Pipenv are installed on your machine. Find information on installing pipenv [here](https://pipenv-fork.readthedocs.io/en/latest/install.html).

#### Pipenv

The project comes with a `Pipfile` in the `src` directory that will install the necessary packages for the program, making it easy for users with Pipenv to run the project on their machines.

First navigate to the `src` directory using `cd src`. Then run the command `pipenv lock` to install the necessary Python packages.

You can then run the command `pipenv run python3 run_tool.py` to run the program.
