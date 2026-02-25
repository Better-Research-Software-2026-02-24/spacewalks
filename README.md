# Spacewalks

## Overview
Spacewalks is a python analysis tool for generating a plot of the cumulative time spent by astronauts and cosmonauts on extravehicular activities.

## Features
Key features of spacewalks:

- Generates a CSV table of summary statistics
- Generates a plot of the cumulative duration spent on spacewalks over time

## Prerequisites
Spacewalks was developed using python 3.12

To install and run spacewalks, you Python >= 3.12. You will also need the libraries included in requirements.txt:

- [numpy] (https://www.numpy.org)
- [matplotlib] (https://matplotlib.org/stable/index.html)
- [pytest] (https://docs.pytest.org)
- [pandas] (https://pandas.pydata.org)

## Installation instructions
You can obtain Spacewalks from [github] (https://github.com/laurajascott/spacewalks)

Once you have cloned the repository or unzipped the download as needed, create a virtual environment, activate it, and install the necessary python packages in the requirements.txt before running the code as explained in the usage example.

## Usage example
Spacewalks can be run with the default data set (in the data/ subdirectory) like so:

`python eva_data_analysis.py`

You own input and output can be defined as command line arguments:

`python eva_data_analysis.py data/input_file results/output_file`