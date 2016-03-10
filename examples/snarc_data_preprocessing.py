#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Example analysis script for snarc_experiment.py

The current script produces two files for different analysis of the SNARC
effect (ANOVA vs. slopes analysis) using mean and median RTs

"""
from __future__ import print_function

from expyriment.misc import data_preprocessing, constants


agg = data_preprocessing.Aggregator(data_folder="./data/",
                                    file_name="snarc_experiment")

agg.set_subject_variables(["mapping_order"])
agg.set_computed_variables(["parity = digit % 2", #0:odd, 1:even
                      "size = digit > 5", #0:small, 1:large
                      "space = btn == {0}".format(constants.K_RIGHT) #0:left, 1:right
                      ])
# RTs: space x size
agg.set_exclusions(["RT > 1000", "RT < 200", "error == 1", "trial<0"])
agg.set_dependent_variables(["mean(RT)"])
agg.set_independent_variables(["size", "space"])
print(agg)
agg.aggregate(output_file="rt_size_space.csv")
# RTs: slopes analysis
agg.set_independent_variables(["digit"])
agg.aggregate(output_file="rt_digits.csv")
