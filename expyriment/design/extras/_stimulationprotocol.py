#!/usr/bin/env python

"""
A stimulation protocol.

This module contains a class implementing a stimulation protocol.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import locale
import re
import codecs
from ...design.randomize import rand_int
from ...misc import unicode2byte, byte2unicode


class StimulationProtocol(object):
    """A class implementing a stimulation protocol."""

    def __init__(self, unit):
        """Create a stimulation protocol.
        
        Parameters
        ----------
        
        unit : str
            The unit of the stimulation protocol ('time' or 'volume')
                    
        """

        if unit in ["time", "volume"]:
            self._unit = unit
        else:
            raise ValueError("'unit' only takes the values 'time' or 'volume'")
        self._conditions = []

    def __str__(self):
        rtn = "unit = {0}\n".format(self._unit)

        for condition in self._conditions:
            rtn += "{0} ({1}):\n".format(condition["name"],
                    len(condition["events"]))
            for event in condition["events"]:
                begin = repr(event["begin"]).rjust(8)
                end = repr(event["end"]).rjust(8)
                weight = repr(event["weight"]).rjust(3)
                rtn += "  {0} {1} {2}\n".format(begin, end, weight)
        return rtn

    def _find_condition_by_name(self, name):
        """Find a condition in by its name."""

        for c,x in enumerate(self._conditions):
            if x["name"] == name:
                return c
            else:
                pass
        return None

    @property
    def conditions(self):
        return self._conditions

    @property
    def unit(self):
        return self._unit

    def add_condition(self, name):
        """Add a condition to the stimulation protocol.
        
        Parameters
        ----------
        
        name : str
            The name of the condition to add
            
        """

        if self._find_condition_by_name(name) is None:
            self._conditions.append({"name":name, "events":[]})
        else:
            raise ValueError(
                    "A condition with the name '{0}' already exists!".format(
                        name))

    def add_event(self, condition, begin, end, weight=1):
        """Add an event to a condition.
        
        Parameters
        ----------
        
        condition : str or int
            The name or index of the condition to add the event to
        begin : int
            The beginning time of the event
        end : int
            The end time of the event
        weight : int, optional
            A weight for parametric modulation (default = 1)

        """

        if type(condition) == int:
            pos = condition
        elif type(condition) == str or str:
            pos = self._find_condition_by_name(condition)
            if pos is None:
                raise ValueError("No condition with name '{0}' found!".format(
                    condition))
        self._conditions[pos]["events"].append(
                {"begin":begin, "end":end, "weight":weight})

    def save(self, filename):
        """Save the stimulation protocol to a csv file.
        
        Parameters
        ----------
        
        filename : str
            The name of the file to save the protocol to
            
        """

        with open(filename, 'wb') as f:
            try:
                locale_enc = locale.getdefaultlocale()[1]
            except:
                locale_enc = "UTF-8"
            f.write(unicode2byte("# -*- coding: {0} -*-\n".format(locale_enc)))
            f.write(unicode2byte("#unit={0}\n".format(self._unit)))
            f.write(unicode2byte("condition,begin,end,weight\n"))
            for condition in self._conditions:
                for event in condition["events"]:
                    f.write(unicode2byte("{0},{1},{2},{3}\n".format(
                        unicode2byte(condition["name"]),
                        event["begin"],
                        event["end"],
                        event["weight"])))

    def load(self, filename, encoding=None):
        """Load a stimulation protocol from a csv file.

        Parameters
        ----------
        
        filename : str
            The filename to read the protocol from
        encoding : str, optional
            The encoding to be used when reading from the file
            
        """

        self._conditions = []
        self._unit = None

        if encoding is None:
            with open(filename, 'r') as f:
                first_line = f.readline()
                encoding = re.findall("coding[:=]\s*([-\w.]+)", first_line)
                if encoding == []:
                    second_line = f.readline()
                    encoding = re.findall("coding[:=]\s*([-\w.]+)",
                                          second_line)
                    if encoding == []:
                        encoding = [None]
        else:
            encoding = [encoding]
        with codecs.open(filename, 'rb', encoding[0], errors='replace') as f:
            for line in f:
                line = byte2unicode(line)
                if line.startswith("#"):
                    if line.startswith("#unit="):
                        self._unit = line[6:].strip('\n')
                elif line.startswith("condition,begin,end,weight"):
                    pass
                else:
                    data = line.split(",")
                    if self._find_condition_by_name(data[0]) is None:
                        self.add_condition(data[0])
                    self.add_event(data[0], int(data[1]), int(data[2]),
                                   int(data[3]))

    def export2brainvoyager(self, exp_name, filename):
        """Convert the stimulation protocol to BrainVoyager '.prt' format.
        
        Parameters
        ----------
        exp_name : str
            The name of the Experiment
        filename : str
             The name of the file to write
             
        """

        if not filename.endswith(".prt"):
            filename = filename + ".prt"

        with open(filename, 'wb') as f:
            f.write(unicode2byte("\n"))
            f.write(unicode2byte("FileVersion:        3\n"))
            f.write(unicode2byte("\n"))
            if self._unit == 'time':
                f.write(unicode2byte("ResolutionOfTime:   msec\n"))
            elif self._unit == 'volume':
                f.write(unicode2byte("ResolutionOfTime:   Volume\n"))
            f.write(unicode2byte("\n"))
            f.write(unicode2byte("Experiment:         {0}\n".format(exp_name)))
            f.write(unicode2byte("\n"))
            f.write(unicode2byte("BackgroundColor:    0 0 0\n"))
            f.write(unicode2byte("TextColor:          255 255 255\n"))
            f.write(unicode2byte("TimeCourseColor:    255 255 255\n"))
            f.write(unicode2byte("TimeCourseThick:    4\n"))
            f.write(unicode2byte("ReferenceFuncColor: 0 0 80\n"))
            f.write(unicode2byte("ReferenceFuncThick: 3\n"))
            f.write(unicode2byte("\n"))
            f.write(unicode2byte("ParametricWeights:  1\n"))
            f.write(unicode2byte("\n"))
            f.write(unicode2byte("NrOfConditions:     {0}\n".format(len(self._conditions))))
            if self._unit == "time":
                rjust = 8
            elif self._unit == "volume":
                rjust = 4
            for condition in self._conditions:
                f.write(unicode2byte("\n"))
                f.write(unicode2byte(condition["name"] + "\n"))
                f.write(unicode2byte(repr(len(condition["events"])) + "\n"))
                for event in condition["events"]:
                    f.write(unicode2byte("{0} {1} {2}\n".format(
                        repr(event["begin"]).rjust(rjust),
                        repr(event["end"]).rjust(rjust),
                        repr(event["weight"]).rjust(2))))
                f.write(unicode2byte("Color: {0} {1} {2}\n".format(rand_int(0,255),
                                                      rand_int(0,255),
                                                      rand_int(0,255))))

