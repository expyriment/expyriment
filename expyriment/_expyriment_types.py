"""
The miscellaneous module.

This module contains miscellaneous functions for expyriment.

All classes in this module should be called directly via expyriment.misc.*:

"""
from __future__ import absolute_import, print_function, division
from builtins import *


class Expyriment_object(object):
    """A class implementing a general Expyriment object.
       Parent of all stimuli and IO objects

    """

    def __init__(self):
        """Create an Expyriment object."""
        self._logging = True

    def set_logging(self, onoff):
        """Set logging of this object on or off

        Parameters
        ----------
        onoff : bool
            set logging on (True) or off (False)

        Notes
        -----
        See also design.experiment.set_log_level fur further information about
        event logging.

    """

        self._logging = onoff

    @property
    def logging(self):
        """Getter for logging."""

        return self._logging



class CallbackQuitEvent(object): # TODO check Docu (also import at old place in expyriment.control)
    """A CallbackQuitEvent

    If a callback function returns a CallbackQuitEvent object the currently processed
    the wait or event loop function will be quited.
    """

    def __init__(self, data=None):
        """Init CallbackQuitEvent

        Parameter
        ---------
        data: any data type, optional
            You might use this variable to return data or values from your callback
            function to your main function, since the quited wait or event loop function
            will return this CallbackQuitEvent.

        See Also
        --------
        experiment.register_wait_callback_function()

        """

        self.data = data

    def __str__(self):
        return "CallbackQuitEvent: data={0}".format(self.data)
