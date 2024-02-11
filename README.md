# Project Name

This is a Python project that uses the Ursina game engine to create a GUI for a Rubik's Cube. The project also includes a solver that uses the Thistlethwaite algorithm.

## Project Structure

The project is structured as follows:

### Main Application Files
- [`main.py`](./main.py): 
- [`MainMenu.py`](./MainMenu.py): 
- [`InputMenu.py`](./InputMenu.py):
- [`cube.py`](./cube.py): 
- [`GUICube.py`](./GUICube.py): 
- [`solutionTools.py`](./solutionTools.py): 
- [`thistlepruningtables.py`](./thistlepruningtables.py): 
- [`thistlethwaite.py`](./thistlethwaite.py): 
### Building and Packaging Files
- [`setup.py`](./setup.py): This file is used for building the application.
- [`requirements.txt`](./requirements.txt): This file lists the Python dependencies required by the application.

## Installation
To install the project, you need to have Python installed on your system. You can then install the required dependencies by running:

```sh
pip install -r requirements.txt
```

## Building
To build the project, run the following command:
```sh
python setup.py build_apps
```
## Running
To run the project without building it, use the following command:
```sh
python main.py
```
