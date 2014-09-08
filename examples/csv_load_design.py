#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Load design from csv file

see also: csv_save_design.py
"""

from expyriment import design

exp = design.Experiment()
exp.load_design("design.csv")
print exp
