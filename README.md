# Fortune's Algorithm in Python

This repository contains an implementation of Fortune's Algorithm, a well-known algorithm for generating Voronoi diagrams. The implementation is done in Python and utilizes a double linked list to represent the beachline, instead of an AVL tree. The AVL tree file exists in the repository but is not used in this initial implementation.

## Overview

Fortune's Algorithm is a sweep line algorithm for constructing Voronoi diagrams, a fundamental structure in computational geometry. This implementation aims to efficiently compute the Voronoi diagram by maintaining a dynamic beachline using a double linked list.

## Features

- Implementation of Voronoi diagram generation using Fortune's Algorithm.
- Utilizes a double linked list for the beachline representation.
- Includes handling for site events and circle events.
- Test suite to ensure correctness of the implementation.

## Repository Structure

- `utils/`: Contains utility classes and functions, including the beachline and AVL tree implementations.
- `tests/`: Contains unit tests for the various components of the algorithm.
- `main.py`: Main entry point for running the algorithm.
- `test_voronoi_visual.py`: Script for visualizing the Voronoi diagram generation process.

## Usage

You probably want a venv or conda environment to install the dependencies
```
pip install -r requirements.txt
```

To run the algorithm, execute the `main.py` script. This will process a predefined set of sites and output the resulting Voronoi diagram.

```bash
python main.py
```

To visualize the Voronoi diagram generation process, run the `test_voronoi_visual.py` script.

```bash
python test_voronoi_visual.py
```

## Testing

The repository includes a suite of unit tests to verify the correctness of the algorithm. To run the tests, use the following command:

```bash
python -m unittest discover -s tests/ -p "*_tests.py"
```
followed by 
```bash
python -m coverage html
```
to get the html coverage report if desired.

Alternatively, one can use the `run_tests.bat` script to run the tests.

## Future Work

- Optimize the implementation by integrating the AVL tree for the beachline.
- Remove some rendundant checks and calculations
- Enhance the visualization tool for better interaction and analysis.