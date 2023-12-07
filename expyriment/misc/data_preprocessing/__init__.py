"""Data Preprocessing Module.

This module contains several classes and functions that help
to handle, preprocessing and aggregate Expyriment data files.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._data_preprocessing import read_datafile, get_experiment_duration
from ._data_preprocessing import write_csv_file, write_concatenated_data
from ._data_preprocessing import Aggregator
