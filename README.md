# Rocket-Elevators-Python-Controller

### Description

This program serve as an elevator controller for application in the residential department, coded in Python

#### Exemple:

On a request call from any floor of the building, the controller will first select the best elevator available.
Selection is based on the status, direction and distance of each elevator to the target floor.
Once an elevator have been selected, it is sent to the corresponding floor to pick up the user and move him to the floor of his choice


### Installation

First, depending on your python version, make sure to install the Package Installer for Python (PIP) if needed:

https://pip.pypa.io/en/stable/installing/

Next, install Pytest:

https://docs.pytest.org/en/6.2.x/getting-started.html

### Running the tests

To launch the tests:

`pytest`

You can also get more details about each test by adding the `-v` flag: 

`pytest -v` 

