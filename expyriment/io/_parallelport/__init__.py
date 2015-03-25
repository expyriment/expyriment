"""
Input and output parallel port.

This module contains a class implementing parallel port input/output on Linux
and Windows.

This module is a modified version of the parallel module of PsychoPy
(www.psychopy.org).
The code in this file is heavily based on the original code.
The files '_dlportio.py', '_inpout32.py' and '_linux.py' are the original
files without modification.

Notes
-----
On Windows, the module will attempt to load whichever parallel port driver
(inpout32 or dlportio) is found first on the system.
On Linux, the PyParallel package is used.

Each instance of the class can provide access to a different parallel
port.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys

import expyriment
from expyriment.io._input_output import Input, Output

if sys.platform.startswith('linux'):
    try:
        from _linux import PParallelLinux
        _ParallelPort = PParallelLinux
    except ImportError:
        _ParallelPort = None
elif sys.platform == 'win32':
    from ctypes import windll
    if hasattr(windll, 'inpout32'):
        from _inpout32 import PParallelInpOut32
        _ParallelPort = PParallelInpOut32
    elif hasattr(windll, 'dlportio'):
        from _dlportio import PParallelDLPortIO
        _ParallelPort = PParallelDLPortIO
    else:
        _ParallelPort = None
else:
    _ParallelPort = None


class ParallelPort(Input, Output):
    """A class implementing a parallel port input and output.

    Notes
    -----
    CAUTION: On Windows, one of the following parallel port drivers needs to
    be installed: 'input32' (http://www.highrez.co.uk/Downloads/InpOut32/) or
    'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/).
    On Linux, the Python package 'PyParallel'
    (http://pyserial.sourceforge.net/pyparallel.html) has to be installed.

    """

    def __init__(self, address):
        """Create a parallel port input and output.

        Parameters
        ----------
        address : hex or str
            The address of the port to use.

        Notes
        -----
        On Windows, common port addresses are::
            LPT1 = 0x0378 or 0x03BC
            LPT2 = 0x0278 or 0x0378
            LPT3 = 0x0278

        On Linux, port addresses are in the following format::
            /dev/parport0

        """

        import types
        if type(_ParallelPort) is not types.TypeType:
            if sys.platform == "win32":
                _message = "Please install one of the following parallel port " + \
"drivers: 'input32' (http://www.highrez.co.uk/Downloads/InpOut32/) or " + \
"'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/)."
            elif sys.platform.startswith("linux"):
                _message = "Please install the Python package 'PyParallel'."
            else:
                _message = "Not available on your computer."
            message = "ParallelPort can not be initialized! {0}".format(
                _message)
            raise ImportError(message)

        Input.__init__(self)
        Output.__init__(self)
        if isinstance(address, basestring) and address.startswith('0x'):
            address = int(address, 16)
        self._address = address
        try:
            self._parallel = _ParallelPort(address=address)
        except:
            raise RuntimeError(
                "Could not initiate parallel port at {0}".format(address))
        self.input_history = False  # dummy

    @property
    def address(self):
        """Getter for port."""
        return self._address

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

    def read_data(self):
        """Read the data pins.

        Reads the data pins (2-9) on the parallel port.

        The received data is encoded in 8 bits, corresponding to the 8 pins::
            Pin:  9   7   6   5   4   3   2   1
                  |   |   |   |   |   |   |   |
            Bit: 128  64  32  16  8   4   2   1

        Returns:
        --------
        data : int
            The value of the data pins.


        """

        data = self._parallel.readData()
        if self._logging:
            expyriment._active_exp._event_file_log(
                    "ParallelPort,received,{0},read_data".format(data))
        return data

    def read_status(self):
        """Read data from the status pins.

        Reads all status pins (10, 11, 12, 13, 15).

        The received data is encoded in 5 bits, corresponding to the 5 pins::

            Pin: 10  11  12  13  15
                  |   |   |   |   |
            Bit: 16   8   4   2   1

        Returns
        -------
        data : int (0-32)
            The value of the status pins.

        """

        bits = "{0}{1}{2}{3}{4}".format(int(self.read_pin(10)),
                                        int(self.read_pin(11)),
                                        int(self.read_pin(12)),
                                        int(self.read_pin(13)),
                                        int(self.read_pin(15)))
        data = int(bits, 2)
        if self._logging:
            expyriment._active_exp._event_file_log(
                    "ParallelPort,received,{0},read_data".format(data), 2)
        return data

    def poll(self):
        """Poll the parallel port.

        This will read both the data pins (2-9) and status pins
        (10, 11, 12, 13, 15).

        The received data is encoded in 13 bits, corresponding to the 13 pins::

            Pin:  10   11   12   13   15    9    8    7    6    5    4    3    2
                   |    |    |    |    |    |    |    |    |    |    |    |    |
            Bit: 4096 2048 1024  512  256  128  64   32   16    8    4    2    1

        Returns
        -------
        data : int (0-8192)
            The value of all input pins.

        """

        d = self.read_data()
        s = self.read_status()

        data = d * s + s
        if self._logging:
            expyriment._active_exp._event_file_log(
                    "ParallelPort,received,{0},poll".format(data), 2)

    def read_pin(self, pin):
        """Determine whether an input pin is set high(True) or low(False).

        Parameters
        ----------
        pin : int
            The number of the input pin to read (2-13 and 15)

        Returns
        -------
        set : bool
            Whether the pin is set high(True) or low(False)

        """

        return self._parallel.readPin(pin)

    def send(self, data):
        """Send data via data pins.

        Sets the data pins (2-9) on the parallel port.

        The data is encoded in 8 bits, corresponding to the 8 pins::

            Pin:  9   7   6   5   4   3   2   1
                  |   |   |   |   |   |   |   |
            Bit: 128  64  32  16  8   4   2   1

        Parameters
        ----------
        data : int (0-255)
            The data to be send via the data bits.

        """

        self._parallel.setData(data)
        if self._logging:
            expyriment._active_exp._event_file_log(
                                    "ParallelPort,send,{0}".format(data), 2)

    def set_pin(self, pin, state):
        """Set a desired output pin to be high(True) or low(False).

        Parameters
        ----------
        pin : int
            The number of the output pin to set (2-9).
        state : bool
            Whether the pin is to be set high(True) or low(False).

        """

        self._parallel.setPin(pin, int(state))
