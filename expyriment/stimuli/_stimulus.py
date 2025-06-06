#!/usr/bin/env python

"""
This module contains the base classes for stimuli.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

from copy import deepcopy

from .. import _internals
from .._internals import Expyriment_object
from ..misc import byte2unicode


class Stimulus(Expyriment_object):
    """A class implementing a very general experimental stimulus.

    All other stimulus classes are based on this one.
    If a new stimulus is to be created, (at least) this class should be
    subclassed.

    """

    _id_counter = 0

    def __init__(self, log_comment=None):
        """Create a stimulus.

        Parameters
        ----------
        log_comment : str, optional
            comment for the event log file

        """

        Expyriment_object.__init__(self)
        self._id = Stimulus._id_counter
        Stimulus._id_counter += 1

        log_txt = u"Stimulus,created,{0},{1}".format(self.id,
                                                    self.__class__.__name__)

        if log_comment is not None:
            log_txt = u"{0},{1}".format(log_txt, byte2unicode(log_comment))
        if self._logging:
            _internals.active_exp._event_file_log(log_txt, 2)


    @property
    def id(self):
        """Getter for id."""

        return self._id

    def copy(self):
        """Return a deep copy of the stimulus."""

        copy = deepcopy(self)
        copy._id = Stimulus._id_counter
        Stimulus._id_counter += 1

        if self._logging:
            _internals.active_exp._event_file_log(
                    "Stimulus,created,{0},{1},copied from {2}".format(
                    copy.id, copy.__class__.__name__, self.id))
        return copy
