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

from ..._internals import is_base_string
from ...design.randomize import rand_int, rand_element
from ...design import Block, Trial
from ...misc import unicode2byte, byte2unicode, create_colours


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
        """Find a condition by its name."""

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

        if isinstance(condition, int):
            pos = condition
        elif is_base_string(condition):
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

    def export_to_brainvoyager(self, exp_name, filename):
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
            colours = create_colours(len(self._conditions))
            for c, condition in enumerate(self._conditions):
                f.write(unicode2byte("\n"))
                f.write(unicode2byte(condition["name"] + "\n"))
                f.write(unicode2byte(repr(len(condition["events"])) + "\n"))
                for event in condition["events"]:
                    f.write(unicode2byte("{0} {1} {2}\n".format(
                        repr(event["begin"]).rjust(rjust),
                        repr(event["end"]).rjust(rjust),
                        repr(event["weight"]).rjust(2))))
                f.write(unicode2byte("Color: {0} {1} {2}\n".format(colours[c][0],
                                                                   colours[c][1],
                                                                   colours[c][2])))

    def export2brainvoyager(self, exp_name, filename):
        """Convert the stimulation protocol to BrainVoyager '.prt' format.

        DEPRECATED: Use ``export_to_brainvoyager``.
        
        Parameters
        ----------
        exp_name : str
            The name of the Experiment
        filename : str
             The name of the file to write

        """
        
        self.export_to_brainvoyager(exp_name, filename)
        
    def import_from_brainvoyager(self, prt_file):
        """Import prt file as stimulation protocol.

        ATTENTION: This will overwrite all data in the current protocol!

        Parameters
        ----------
        prt_file : str
            the prt file to import

        """

        data = []
        with open(prt_file) as f:
            for line in f:
                data.append(byte2unicode(line.rstrip('\r\n')))
        in_body = False
        in_condition = False
        for idx, line in enumerate(data):
            if line.startswith(u"ResolutionOfTime:"):
                if line.endswith(u"msec"):
                    if self._conditions != [] and self._timing != u"msec":
                        raise RuntimeError("Protocol contains data in other unit!")
                    self._timing = "time"
                else:
                    if self._conditions !=[] and self._timing != u"volume":
                        raise RuntimeError("Protocol contains data in other unit!")
                    self._timing = u"volume"
            if line.startswith(u"NrOfConditions:"):
                in_body = True
                continue
            if in_body:
                if line == u"":
                    current_condition = data[idx + 1]
                    self.add_condition(current_condition)
                    start = idx + 3
                    end = start + int(data[idx + 2])
                    for x in range(start, end):
                        event = [i for i in data[x].split(" ") if i != u""]
                        if len(event) == 2:
                            event.append(1)
                        self.add_event(current_condition, int(event[0]), int(event[1]), int(event[2]))
                if idx in range(start, end + 1):
                        continue

    def get_as_experimental_block(self, name=None, block=None):
        """Create an experimental block from a stimulation protocol.

        Each stimulation becomes a trial in the block. Trials are ordered
        according to the stimulation onset time.

        If 'block' is an experimental block with the same amount of unique
        trials as the stimulation protocol, and has a factor called
        "condition" or "Condition", with the the factor level names
        corresponding to the condition names of the protocol, then the
        returned block will be a copy of the experimental block, with the
        order of trials randomized, but in line with the order of conditions
        specified in the protocol.

        The resulting block will have the following trial factors:

            "condition" - the name of the condition
            "begin"     - the stimulation onset in milliseconds
            "end"       - the stimulation offset in milliseconds
            "weight"    - the parametric weight

        Parameters
        ----------
        name : str, optional
            the name of the block
        block : expyriment.design.Block object, optional

        Returns
        -------
        block : expyriment.design.Block object
            the experimental block

        """

        onsets = []
        for condition in self._conditions:
            onsets.extend([event['begin'] for event in condition['events']])
        onsets = list(set(onsets))
        onsets.sort()

        if block is None:
            b = Block(name=name)
        else:
            b = block.copy()
            conditions = [x["name"] for x in self.conditions]
            c1 = [t.get_factor("Condition") in conditions for t in b.trials]
            c2 = [t.get_factor("condition") in conditions for t in b.trials]
            if False in c1 and False in c2:
                raise RuntimeError("All trials need matching conditions!")
            if len(set(b.trials)) != len(b.trials):
                raise RuntimeError("Trials have to be unique!")
            if len(b.trials) != len(onsets):
                raise RuntimeError("Amount of trials needs to match amount of events!")
            if name is not None:
                b._name = name
            trial_indices = list(range(0, len(b.trials)))
            cnt = 0

        for onset in onsets:
            for condition in self._conditions:
                for event in condition['events']:
                    if event['begin'] == onset:
                        if block is None:
                            t = Trial()
                        else:
                            while True:
                                idx = rand_element(trial_indices)
                                t = b.trials[idx]
                                if t.get_factor("Condition") == condition['name'] or \
                                    t.get_factor("condition") == condition['name']:
                                    b.swap_trials(cnt, idx)
                                    trial_indices.pop(trial_indices.index(cnt))
                                    cnt += 1
                                    break

                        t.set_factor("condition", condition['name'])
                        t.set_factor("begin", event['begin'])
                        t.set_factor("end", event['end'])
                        t.set_factor("weight", event['weight'])

                        if block is None:
                            b.add_trial(t)
        return b
