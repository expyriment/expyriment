# We deliberately delay importing the pyparallel module until we try
# to use it - this allows us to import the class on machines
# which don't have it and then worry about dealing with
# using the right one later

# This is necessary to stop the local parallel.py masking the module
# we actually want to find!
from __future__ import absolute_import, print_function, division
from builtins import *

# We duck-type the parallel port objects
class PParallelLinux(object):
    """
    This class provides read/write access to the parallel port for linux using
    pyparallel.

    Note that you must have the lp module removed and the ppdev module loaded
    to use this code::
        sudo rmmod lp
        sudo modprobe ppdev
    """
    def __init__(self, address='/dev/parport0'):
        """Set the device node of your parallel port

        common port addresses::

            LPT1 = /dev/parport0
            LPT2 = /dev/parport1
            LPT3 = /dev/parport2"""
        import parallel as pyp

        if not hasattr(pyp, 'Parallel'):
            # We failed to import pyparallel properly
            # We probably ended up with psychopy.parallel instead...
            raise Exception('Failed to import pyparallel - is it installed?')

        self.port = pyp.Parallel(address)
        self.reverse = False
        self.status = None

    def __del__(self):
        if hasattr(self, 'port'):
            del self.port

    @property
    def reverse(self):
        """Getter for reverse."""

        return self._reverse

    @reverse.setter
    def reverse(self, value):
        """Setter for reverse."""

        if value:
            self.port.PPDATADIR(False)
            self._reverse = True
        else:
            self.port.PPDATADIR(True)
            self._reverse = False

    def setData(self, data):
        """Set the data to be presented on the parallel port (one ubyte).
        Alternatively you can set the value of each pin (data pins are pins
        2-9 inclusive) using :func:`~psychopy.parallel.setPin`

        examples::

            p.setData(0) #sets all pins low
            p.setData(255) #sets all pins high
            p.setData(2) #sets just pin 3 high (remember that pin2=bit0)
            p.setData(3) #sets just pins 2 and 3 high

        you can also convert base 2 to int v easily in python::

            parallel.setData( int("00000011",2) )#pins 2 and 3 high
            parallel.setData( int("00000101",2) )#pins 2 and 4 high
        """
        self.port.setData(data)

    def setPin(self, pinNumber, state):
        """Set a desired pin to be high(1) or low(0).

        Only pins 2-9 (incl) are normally used for data output::

            p.setPin(3, 1)#sets pin 3 high
            p.setPin(3, 0)#sets pin 3 low
        """
        # I can't see how to do this without reading and writing the data
        if state:
            if pinNumber in range(2, 10):
                self.port.setData(self.port.PPRDATA() | (2**(pinNumber-2)))
            elif pinNumber==1:
                self.port.PPWCONTROL(self.port.PPRCONTROL() | 1)
            elif pinNumber==14:
                self.port.PPWCONTROL(self.port.PPRCONTROL() | 2)
            elif pinNumber==16:
                self.port.PPWCONTROL(self.port.PPRCONTROL() | 4)
            elif pinNumber==17:
                self.port.PPWCONTROL(self.port.PPRCONTROL() | 8)
        else:
            if pinNumber in range(2, 10):
                self.port.setData(self.port.PPRDATA() & (255 ^ 2**(pinNumber-2)))
            elif pinNumber==1:
                self.port.PPWCONTROL(self.port.PPRCONTROL() & (255 ^ 1))
            elif pinNumber==14:
                self.port.PPWCONTROL(self.port.PPRCONTROL() & (255 ^ 2))
            elif pinNumber==16:
                self.port.PPWCONTROL(self.port.PPRCONTROL() & (255 ^ 4))
            elif pinNumber==17:
                self.port.PPWCONTROL(self.port.PPRCONTROL() & (255 ^ 8))

    def readData(self):
        """Return the value currently set on the data pins (2-9)"""
        return (self.port.PPRDATA())

    def readPin(self, pinNumber):
        """Determine whether a desired (input) pin is high(1) or low(0).

        Pins 1-17 are currently read here """
        if pinNumber==10:
            return self.port.getInAcknowledge()
        elif pinNumber==11:
            return self.port.getInBusy()
        elif pinNumber==12:
            return self.port.getInPaperOut()
        elif pinNumber==13:
            return self.port.getInSelected()
        elif pinNumber==15:
            return self.port.getInError()
        elif pinNumber>=2 and pinNumber <=9:
            return (self.port.PPRDATA() >> (pinNumber - 2)) & 1
        elif pinNumber==1:
            return (self.port.PPRCONTROL() >> 0) & 1 # 0 = STROBE
        elif pinNumber==14:
            return (self.port.PPRCONTROL() >> 1) & 1 # 0 = LineFeed
        elif pinNumber==16:
            return (self.port.PPRCONTROL() >> 2) & 1 # 0 = RESET
        elif pinNumber==17:
            return (self.port.PPRCONTROL() >> 3) & 1 # 0 = Select Printer
        else:
            print('Pin %i cannot be read (by PParallelLinux.readPin() yet)' % (pinNumber))
