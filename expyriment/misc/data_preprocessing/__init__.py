"""Data Preprocessing Module.

This module contains several classes and functions that help
to handle, preprocessing and aggregate Expyriment data files.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


from ._data_preprocessing import (
    Aggregator,
    get_experiment_duration,
    read_datafile,
    write_concatenated_data,
    write_csv_file,
)
