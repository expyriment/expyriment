"""
Input and output parallel port.

This module contains a class implementing parallel port input/output.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


from types import ModuleType
from sys import platform
from os import listdir

try:
    import parallel
except:
    parallel = None

from ... import _internals
from  ...io._input_output  import Input, Output


class SimpleParallelPort(Input, Output):
    """A class implementing a parallel port input and output.

    Notes
    -----
    CAUTION: Under Windows (starting from 2000) direct I/O is blocked.
    Install http://sourceforge.net/projects/pyserial/files/pyparallel/giveio/

    """

    def __init__(self, port=None):
        """Create a parallel port input and output.

        Parameters:
        -----------
        port : int, optional
            The port to use.

        """

        if not isinstance(parallel, ModuleType):
            message = """SimpleParallelPort can not be initialized.
The Python package 'pyParallel' is not installed."""
            raise ImportError(message)

        if float(parallel.VERSION) < 0.2:
            raise ImportError("Expyriment {0} ".format(__version__) +
                    "is not compatible with PyParallel {0}.".format(
                        parallel.VERSION) +
                      "\nPlease install PyParallel 0.2 or higher.")

        Input.__init__(self)
        Output.__init__(self)
        if port is None:
            port = 0
        self._port = port
        self._parallel = parallel.Parallel(self._port)
        self.input_history = False # dummy

    @property
    def port(self):
        """Getter for port."""
        return self._port

    @property
    def parallel(self):
        """Getter for parallel"""
        return self._parallel

    @property
    def has_input_history(self):
        """Returns always False, because ParallelPort has no input history."""

        return False

    def clear(self):
        """Clear the parallel port.

        Dummy method required for port interfaces (see e.g. ButtonBox)

        """

        pass

    def poll(self):
        """Poll the parallel port.

        The parallel port will be polled and the result will be returned.
        The parallel module for Python can only read three of the status
        lines.
        The result is thus coded in three bits:

        Acknowledge Paper-Out Selected

        Example: '4' means only Selected is receiving data ("001").

        To send out data the actual data lines are used.

        """

        bits = "{2}{1}{0}".format(int(self._parallel.getInAcknowledge()),
                                  int(self._parallel.getInPaperOut()),
                                  int(self._parallel.getInSelected()))
        code = int(bits, 2)
        if self._logging:
            _internals.active_exp._event_file_log(
                    "SimpleParallelPort,received,{0},poll".format(code), 2)
        return code

    @staticmethod
    def get_available_ports():
        """Return an array of strings representing the available parallel ports.

        If pyparallel is not installed, 'None' will be returned.

        Returns
        -------
        ports : list
            array of strings representing the available parallel ports

        """

        if not isinstance(parallel, ModuleType):
            return None
        ports = []
        if platform.startswith("linux"): #for Linux operation systems
            dev = listdir('/dev')
            for p in dev:
                if p.startswith("parport"):
                    ports.append(p)
        elif platform == "dawin": #for MacOS
            pass
        else: #for windows, os2
            for p in range(256):
                try:
                    p = parallel.Parallel(p)
                    ports.append("LTP{0}".format(p + 1))
                except:
                    pass
        ports.sort()

        return ports

    def send(self, data):
        """Send data.

        Parameters
        ----------
        data : int
            data to be sent

        """

        self.parallel.setData(data)
        if self._logging:
            _internals.active_exp._event_file_log(
                                    "SimpleParallelPort,sent,{0}".format(data), 2)
