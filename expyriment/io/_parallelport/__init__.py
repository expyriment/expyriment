"""
Input and output parallel port.

This module contains a class implementing parallel port input/output on Linux
and Windows.

The module is a modified version of the parallel module of PsychoPy
(www.psychopy.org).
The code in this file, as well as in the files '_inpout32.py', '_dlportio.py'
and '_linux.py' are heavily based on the original code.

Notes
-----
On Windows, the module will attempt to load whichever parallel port driver
(inpout32 or dlportio) is found first on the system.
On Linux, the PyParallel package is used.

Each instance of the class can provide access to a different parallel
port.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import sys
import os

from ... import _internals, misc
from ...io._input_output import Input, Output

if sys.platform.startswith('linux'):
    try:
        from ._linux import PParallelLinux
        _ParallelPort = PParallelLinux
        _ParallelPort._driver = "pyparallel"
    except:
        _ParallelPort = None
elif sys.platform == 'win32':
    try:
        from ._inpout32 import PParallelInpOut32
        _ParallelPort = PParallelInpOut32
        from ctypes import windll
        try:
            windll.inpout32
            _ParallelPort._driver = "inpout32"
        except:
            windll.inpoutx64
            _ParallelPort._driver = "inpoutx64"
    except:
        try:
            from ._dlportio import PParallelDLPortIO
            _ParallelPort = PParallelDLPortIO
            from ctypes import windll
            windll.dlportio
            _ParallelPort._driver = "dlportio"
        except:
            _ParallelPort = None
else: # MAC
    _ParallelPort = None
    # class PP(object):
    #     def __init__(self, address):
    #         self.address = address
    #     def read_data(self):
    #         return 255
    #     def read_status(self):
    #         return 32
    #     def read_control(self):
    #         return 16
    #     def set_control(self):
    #         pass
    #     def poll(self):
    #         return 8192
    #     def setData(self, data):
    #         pass
    #     def readData(self):
    #         return 100
    #     def readPin(self, pin):
    #         return False
    #     def setPin(self, pin, state):
    #         pass
    # _ParallelPort = PP


class ParallelPort(Input, Output):
    """A class implementing a parallel port input and output.

    Notes
    -----
    CAUTION: On Windows, one of the following parallel port drivers needs to
    be installed: 'inpout32' (http://www.highrez.co.uk/Downloads/InpOut32/) or
    'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/).
    On Linux, the Python package 'PyParallel'
    (http://pyserial.sourceforge.net/pyparallel.html) has to be installed.

    """
    
    def __init__(self, address, reverse=False):
        """Create a parallel port input and output.

        Parameters
        ----------
        address : hex or str
            The address of the port to use.
        reverse : bool
            Whether the port should be in reverse mode (default=False).
            Reverse mode enables to read from the data pins.

        Notes
        -----
        On Windows, common port addresses are::
            
            LPT1 = 0x0378 or 0x03BC
            LPT2 = 0x0278 or 0x0378
            LPT3 = 0x0278
            
        On Linux, port addresses are in the following format::
            
            /dev/parport0
            

        """

        if _ParallelPort is None:
            if sys.platform == "win32": # TODO to be tested for Windows 7 and 10
                _message = "Please install one of the following parallel port " + \
"drivers: 'inpout32' (http://www.highrez.co.uk/Downloads/InpOut32/) or " + \
"'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/)."
            elif sys.platform.startswith("linux"):
                _message = "Please install the Python package 'PyParallel'."
            else:
                _message = "Not available on your computer."
            message = "ParallelPort cannot be initialized! {0}".format(
                _message)
            raise ImportError(message)

        Input.__init__(self)
        Output.__init__(self)
        if isinstance(address, str) and address.startswith('0x'):
            address = int(address, 16)
        self._address = address
        try:
            self._parallel = _ParallelPort(address=address)
        except:
            raise RuntimeError(
                "Could not initiate parallel port at {0}".format(address))
        self.input_history = False  # dummy
        self._reverse = reverse

    @property
    def address(self):
        """Getter for address."""
        return self._address

    @property
    def parallel(self):
        """Getter for parallel"""
        return self._parallel

    @property
    def has_input_history(self):
        """Returns always False, because ParallelPort has no input history."""

        return False

    @property
    def reverse(self):
        """Getter for reverse."""

        return self._parallel.reverse

    @reverse.setter
    def reverse(self, value):
        """Setter for reverse."""

        self._parallel.reverse = value

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
            _internals.active_exp._event_file_log(
                    "ParallelPort,received,{0},read_data".format(data))
        return data

    def read_status(self):
        """Read data from the status pins.

        Reads all status pins (10, 11, 12, 13, 15).

        The received data is encoded in 5 bits, corresponding to the 5 pins::

            Pin: 11  10  12  13  15
                  |   |   |   |   |
            Bit: 16   8   4   2   1

        Returns
        -------
        data : int (0-31)
            The value of the status pins.

        """

        # TODO: Proper implementation that does not rely on single pins!

        bits = "{0}{1}{2}{3}{4}".format(int(self.read_pin(11)),
                                        int(self.read_pin(10)),
                                        int(self.read_pin(12)),
                                        int(self.read_pin(13)),
                                        int(self.read_pin(15)))
        data = int(bits, 2)
        if self._logging:
            _internals.active_exp._event_file_log(
                    "ParallelPort,received,{0},read_status".format(data), 2)
        return data

    def read_control(self):
        """Read data from the control pins.

        Reads control pins 1, 14, 16, 17.

        The received data is encoded in 4 bits, corresponding to the 4 pins::

            Pin: 17  16  14   1
                  |   |   |   |
            Bit:  8   4   2   1

        Returns
        -------
        data : int (0-15)
            The value of the control pins.

        """

        # TODO: Proper implementation that does not rely on single pins!

        bits = "{0}{1}{2}{3}".format(int(self.read_pin(17)),
                                     int(self.read_pin(16)),
                                     int(self.read_pin(14)),
                                     int(self.read_pin(1)))
        data = int(bits, 2)
        if self._logging:
            _internals.active_exp._event_file_log(
                    "ParallelPort,received,{0},read_control".format(data), 2)
        return data

    def poll(self):
        """Poll the parallel port.

        This will read the status pins (11, 10, 12, 13, 15), the data pins (2-9),
        and control pins (1, 14, 16, 17).

        The received data is encoded in 17 bits, corresponding to the 17 pins::

            Pin:  17    16    14     1     9     8     7     6     5
                   |     |     |     |     |     |     |     |     |
            Bit: 65536 32768 16384 8192  4096  2048  1024   512   256
             
            Pin:  4    3    2   11   10   12   13   15
                  |    |    |    |    |    |    |    |
            Bit: 128  64   32   16    8    4    2    1
             
        Returns
        -------
        data : int (0-65535)
            The value of all input pins.

        """

        c = self.read_control()
        d = self.read_data()
        s = self.read_status()

        data = (int('{:04b}'.format(c)[::1], 2) << 13) + \
               (int('{:08b}'.format(d)[::1], 2) << 5) + \
               s
        if self._logging:
            _internals.active_exp._event_file_log(
                    "ParallelPort,received,{0},poll".format(data), 2)
        return data

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

    def set_data(self, data):
        """Send data via data pins.

        Sets the data pins (2-9) on the parallel port.

        The data is encoded in 8 bits, corresponding to the 8 pins::

            Pin:  9   7   6   5   4   3   2   1
                  |   |   |   |   |   |   |   |
            Bit: 128  64  32  16  8   4   2   1

        Parameters
        ----------
        data : int (0-255)
            The data to be send via the data pins.

        """

        self._parallel.setData(data)
        if self._logging:
            _internals.active_exp._event_file_log(
                                    "ParallelPort,set_data,{0}".format(data), 2)

    def set_control(self, data):
        """Send data via control pins.

        Sets the control pins (1, 14, 16, 17) on the parallel port.

        The data is encoded in 8 bits, corresponding to the 4 pins::

            Pin: 17  16  14   1
                  |   |   |   |
            Bit:  8   4   2   1

        Parameters
        ----------
        data : int (0-15)
            The data to be send via the control pins.

        """

        # TODO: Proper implementation that does not rely on single pins!

        self._parallel.setPin(1, data & 1)
        self._parallel.setPin(14, data & 2)
        self._parallel.setPin(16, data & 4)
        self._parallel.setPin(17, data & 8)
        if self._logging:
            _internals.active_exp._event_file_log(
                                    "ParallelPort,set_control,{0}".format(data), 2)

    def send(self, data):
        """Send data via all output pins.

        Sets the data pins (2-9) and the control pins (1, 14, 16, 17) on the
        parallel port.

        The data is encoded in 12 bits, corresponding to the 12 pins::

            Pin:  17   16   14    1    9    8    7    6    5    4    3    2
                   |    |    |    |    |    |    |    |    |    |    |    |
            Bit: 2048 1024  512  256  128  64   32   16    8    4    2    1

        Parameters
        ----------
        data : int (0-2047)
            The data to be send via the output pins.

        """

        # TODO: Proper implementation that does not rely on single pins!

        d = data & 255
        c = data & 2048 >> 8
        self._parallel.setData(d)
        self._parallel.setPin(1, c & 1)
        self._parallel.setPin(14, c & 2)
        self._parallel.setPin(16, c & 4)
        self._parallel.setPin(17, c & 8)
        if self._logging:
            _internals.active_exp._event_file_log(
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

    @staticmethod
    def get_driver():
        """Return the driver used for interacting with parallel ports.
        
        On Windows, one of the following parallel port drivers needs to
        be installed: 'input32' (http://www.highrez.co.uk/Downloads/InpOut32/) or
        'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/).
        On Linux, the Python package 'PyParallel'
        (http://pyserial.sourceforge.net/pyparallel.html) has to be installed.
    
        """
        
        if _ParallelPort is not None:
            return _ParallelPort._driver
        
    @staticmethod
    def get_available_ports():
        """Return an array of strings representing available parallel ports.

        Returns
        -------
        ports : list
            array of strings representing the available parallel ports

        Notes
        -----
        This method does only work on Linux.

        """

        ports = []
        if sys.platform.startswith("linux"):
            dev = os.listdir('/dev')
            for p in dev:
                if p.startswith("parport"):
                    ports.append(p)
        else:
            pass
        ports.sort()

        return ports

    @staticmethod
    def _self_test(exp):
        """Test the parallel port."""

        from ... import stimuli, io
        result = {}
        result["testsuite_parallel_port"] = ""
        result["testsuite_parallel_success"] = "No"

        if _ParallelPort is None:
            if sys.platform == "win32":
                _message = "Please install one of the following parallel port " + \
"drivers: 'inpout32' (http://www.highrez.co.uk/Downloads/InpOut32/) or " + \
"'dlportio' (http://real.kiev.ua/2010/11/29/dlportio-and-32-bit-windows/)."
            elif sys.platform.startswith("linux"):
                _message = "Please install the Python package 'PyParallel'."
            else:
                _message = "Not available on your computer."

            stimuli.TextScreen(
                "ParallelPort cannot be initialized!",
                _message + "\n\n[Press RETURN to continue]").present()
            exp.keyboard.wait(misc.constants.K_RETURN)
            return result

        else:
            text = "This will test if parallel port " \
                   "communication works correctly.\n\n" \
                   "You will be asked to enter a port address. " \
                   "On Windows this will be a hexadecimal number (e.g. " \
                   "'0x0378', which is ofter the address of LPT1). " \
                   "On Linux it will be of the form '/dev/parportX', "\
                   "where X denotes the number of the port.\n\n" \
                   "Once the port is opened, a list of control, status and " \
                   "data pins is presented. Bright green lights indicate " \
                   "input activity of a pin. Bright red lights indicate " \
                   "output activity of a pin. With the number keys on the " \
                   "keyboard, sending can be toggled on and off for each " \
                   "data pin. Reverse mode can be toggled on an of with " \
                   "the 'r' key.\n\n\n\n" \
                   "[Press RETURN to continue]"
            t = stimuli.TextScreen("ParallelPort test", text)
            t.present()
            exp.keyboard.wait(misc.constants.K_RETURN)

            address = io.TextInput("Port address:").get()
            try:
                pp = io.ParallelPort(address=address)
            except:
                stimuli.TextScreen(
                    "Could not open port address {0}!".format(address),
                    "[Press RETURN to continue]").present()
                exp.keyboard.wait(misc.constants.K_RETURN)
                return result

            pin_canvas = stimuli.Canvas((800, 600))
            poll = stimuli.TextLine("Poll",
                                               text_colour=[255, 255, 255],
                                               position=[0, 165])
            poll.plot(pin_canvas)
            poll_line = stimuli.Rectangle((660, 2),
                                                     colour=[255, 255, 255],
                                                     position=[0, 120])
            poll_line.plot(pin_canvas)
            control = stimuli.TextLine("Control",
                                                  text_colour=[100, 100, 100],
                                                  position=[-260, 95])
            control.plot(pin_canvas)
            control_line = stimuli.Rectangle((140, 2),
                                                        colour=[100, 100, 100],
                                                        position=[-260, 50])
            control_line.plot(pin_canvas)
            data = stimuli.TextLine(
                "Data",
                text_colour=misc.constants.C_EXPYRIMENT_ORANGE,
                position=[-20, 95])
            data.plot(pin_canvas)
            data_line = stimuli.Rectangle(
                (300, 2),
                colour=misc.constants.C_EXPYRIMENT_ORANGE,
                position=[-20, 50])
            data_line.plot(pin_canvas)
            status = stimuli.TextLine(
                "Status",
                text_colour=misc.constants.C_EXPYRIMENT_PURPLE,
                position=[240, 95])
            status.plot(pin_canvas)
            status_line = stimuli.Rectangle(
                (180, 2),
                colour=misc.constants.C_EXPYRIMENT_PURPLE,
                position=[240, 50])
            status_line.plot(pin_canvas)

            pins = {}
            inputs = {}
            outputs = {}
            x_pos = -320
            for pin in [17, 16, 14, 1, 9, 8, 7, 6, 5, 4, 3, 2, 11, 10, 12, 13, 15]:
                inputs[pin] = stimuli.Circle(10,
                                                        anti_aliasing=10,
                                                        position=[x_pos, 30])
                if 1 < pin < 10:
                    colour = misc.constants.C_EXPYRIMENT_ORANGE
                elif pin in [10, 11, 12, 13, 15]:
                    colour = misc.constants.C_EXPYRIMENT_PURPLE
                else:
                    colour = [100, 100, 100]
                if pin in [11, 1, 14, 17]:
                    bg = stimuli.Rectangle((25, 20), colour=colour,
                                                      position=[x_pos, 0])
                    bg.plot(pin_canvas)
                    colour = _internals.active_exp._background_colour
                stim = stimuli.TextLine(repr(pin),
                                                   text_font="freemono",
                                                   text_colour=colour,
                                                   position=[x_pos, 0])
                stim.plot(pin_canvas)
                pins[pin] = stim
                if pin < 10 or pin in [14, 16, 17]:
                    outputs[pin] = stimuli.Rectangle(
                        (20, 20), position=[x_pos, -30])
                x_pos += 40

            control2 = stimuli.TextLine("Control",
                                                   text_colour=[100, 100, 100],
                                                   position=[-260, -95])
            control2.plot(pin_canvas)
            control2_line = stimuli.Rectangle((140, 2),
                                                         colour=[100, 100, 100],
                                                         position=[-260, -50])
            control2_line.plot(pin_canvas)

            data2 = stimuli.TextLine(
                "Data",
                text_colour=misc.constants.C_EXPYRIMENT_ORANGE,
                position=[-20, -95])
            data2.plot(pin_canvas)
            data2_line = stimuli.Rectangle(
                (300, 2),
                colour= misc.constants.C_EXPYRIMENT_ORANGE,
                position=[-20, -50])
            data2_line.plot(pin_canvas)

            send = stimuli.TextLine("Send",
                                               text_colour=[255, 255, 255],
                                               position=[-100, -165])
            send.plot(pin_canvas)
            send_line = stimuli.Rectangle((460, 2),
                                                     colour=[255, 255, 255],
                                                     position=[-100, -120])

            send_line.plot(pin_canvas)

            end = stimuli.TextLine(
                "[Press RETURN to end the test]",
                position=[0, -240])
            end.plot(pin_canvas)

            pin_canvas.present()
            pin_canvas.present()
            pin_canvas.present()

            def _update(inputs_states, outputs_states, read_control,
                        read_data, read_status, read_poll):
                for pin in list(inputs.keys()):
                    if inputs_states[pin] == True:
                        inputs[pin].colour = [0, 255, 0]
                    else:
                        inputs[pin].colour = [0, 30, 0]
                    inputs[pin].present(clear=False, update=False)
                    inputs[pin].present(clear=False, update=False)
                    inputs[pin].present(clear=False, update=False)

                send = 0
                for pin in list(outputs.keys()):
                    if outputs_states[pin][0] == True:
                        send += outputs_states[pin][1]
                        outputs[pin].colour = [255, 0, 0]
                    else:
                        outputs[pin].colour = [30, 0, 0]
                    outputs[pin].present(clear=False, update=False)
                    outputs[pin].present(clear=False, update=False)
                    outputs[pin].present(clear=False, update=False)

                results_canvas = stimuli.Canvas(
                    (600, 20),
                    colour=_internals.active_exp.background_colour,
                    position=[0, 70])

                rc = stimuli.TextLine(
                    "{0}".format(read_control),
                    text_colour=[0, 255, 0],
                    position=[-260, 0])
                rc.plot(results_canvas)

                rd = stimuli.TextLine(
                    "{0}".format(read_data),
                    text_colour=[0, 255, 0],
                    position=[-20, 0])
                rd.plot(results_canvas)

                rs = stimuli.TextLine(
                    "{0}".format(read_status),
                    text_colour=[0, 255, 0],
                    position=[240, 0])
                rs.plot(results_canvas)

                poll_canvas = stimuli.Canvas(
                    (100, 20),
                    colour=_internals.active_exp.background_colour,
                    position=[0, 140])

                pd = stimuli.TextLine(
                    "{0}".format(read_poll),
                    text_colour=[0, 255, 0])
                pd.plot(poll_canvas)

                poll_canvas.present(clear=False, update=False)
                poll_canvas.present(clear=False, update=False)
                poll_canvas.present(clear=False, update=False)

                results_canvas.present(clear=False, update=False)
                results_canvas.present(clear=False, update=False)
                results_canvas.present(clear=False, update=False)

                results_canvas2 = stimuli.Canvas(
                    (600, 20),
                    colour=_internals.active_exp.background_colour,
                    position=[0, -70])

                if send > 255:
                    c = (send ^ 255) >> 8
                else:
                    c = 0
                sc = stimuli.TextLine(
                    "{0}".format(c),
                    text_colour=[255, 0, 0],
                    position=[-260, 0])
                sc.plot(results_canvas2)

                sd = stimuli.TextLine(
                    "{0}".format(send & 255),
                    text_colour=[255, 0, 0],
                    position=[-20, 0])
                sd.plot(results_canvas2)

                send_canvas = stimuli.Canvas(
                    (100, 20),
                    colour=_internals.active_exp.background_colour,
                    position=[-100, -140])

                ss = stimuli.TextLine(
                    "{0}".format(send),
                    text_colour=[255, 0, 0])
                ss.plot(send_canvas)

                if pp.reverse is True:
                    r = stimuli.Rectangle(
                        (150, 30),
                        line_width=1,
                        colour=misc.constants.C_EXPYRIMENT_ORANGE,
                        position=[240, -95])
                    reverse = stimuli.TextLine(
                        "Reverse Mode",
                        text_colour=misc.constants.C_EXPYRIMENT_ORANGE,
                        background_colour=_internals.active_exp.background_colour)
                    reverse.plot(r)
                else:
                    r = stimuli.Rectangle(
                        (150, 30),
                        line_width=1,
                        colour=_internals.active_exp.background_colour,
                        position=[240, -95])
                    reverse = stimuli.TextLine(
                        "Reverse Mode",
                        text_colour=_internals.active_exp.background_colour,
                        background_colour=_internals.active_exp.background_colour)
                    reverse.plot(r)

                r.present(clear=False, update=False)
                r.present(clear=False, update=False)
                r.present(clear=False, update=False)

                send_canvas.present(clear=False, update=False)
                send_canvas.present(clear=False, update=False)
                send_canvas.present(clear=False, update=False)

                results_canvas2.present(clear=False, update=False)
                results_canvas2.present(clear=False, update=False)
                results_canvas2.present(clear=False, update=False)

                exp.screen.update()

            inputs_states = {1: False, 2:False, 3:False, 4:False, 5:False,
                             6:False, 7:False, 8:False, 9:False, 10:False,
                             11:False, 12:False, 13:False, 14:False, 15:False,
                             16:False, 17:False}

            outputs_states = {1:[False, 256], 2:[False, 1], 3:[False, 2],
                              4:[False, 4], 5:[False, 8], 6:[False, 16],
                              7:[False, 32], 8:[False, 64], 9:[False, 128],
                              14:[False, 512], 16:[False, 1024],
                              17:[False, 2048]}

            pp.send(0)
            initial_poll = pp.poll()

            while True:
                c = pp.read_control()
                d = pp.read_data()
                s = pp.read_status()
                p = pp.poll()

                if p != initial_poll:
                    result["testsuite_serial_success"] = "Yes"

                for pin, bit in {15:1, 13:2, 12:4, 10:8, 11:16, 2:32, 3:64,
                                 4:128, 5:256, 6:512, 7:1024, 8:2048,
                                 9:4096, 1:8192, 14:16384, 16:32768,
                                 17:65536}.items():
                    if bit & p > 0:
                        inputs_states[pin] = True
                    else:
                        inputs_states[pin] = False

                keys = exp.keyboard.read_out_buffered_keys()
                if misc.constants.K_1 in keys or \
                                misc.constants.K_KP1 in keys:
                    if misc.constants.K_4 in keys or \
                                misc.constants.K_KP4 in keys:
                        outputs_states[14][0] =  not outputs_states[14][0]
                        pp.set_pin(14, outputs_states[14][0])
                    elif misc.constants.K_6 in keys or \
                                misc.constants.K_KP6 in keys:
                        outputs_states[16][0] =  not outputs_states[16][0]
                        pp.set_pin(16, outputs_states[16][0])
                    elif misc.constants.K_7 in keys or \
                                misc.constants.K_KP7 in keys:
                        outputs_states[17][0] =  not outputs_states[17][0]
                        pp.set_pin(17, outputs_states[17][0])
                    else:
                        outputs_states[1][0] =  not outputs_states[1][0]
                        pp.set_pin(1, outputs_states[1][0])
                elif misc.constants.K_2 in keys or \
                                misc.constants.K_KP2 in keys:
                    outputs_states[2][0] =  not outputs_states[2][0]
                    pp.set_pin(2, outputs_states[2][0])
                elif misc.constants.K_3 in keys or \
                                misc.constants.K_KP3 in keys:
                    outputs_states[3][0] = not outputs_states[3][0]
                    pp.set_pin(3, outputs_states[3][0])
                elif misc.constants.K_4 in keys or \
                                misc.constants.K_KP4 in keys:
                    outputs_states[4][0] = not outputs_states[4][0]
                    pp.set_pin(4, outputs_states[4][0])
                elif misc.constants.K_5 in keys or \
                                misc.constants.K_KP5 in keys:
                    outputs_states[5][0] = not outputs_states[5][0]
                    pp.set_pin(5, outputs_states[5][0])
                elif misc.constants.K_6 in keys or \
                                misc.constants.K_KP6 in keys:
                    outputs_states[6][0] = not outputs_states[6][0]
                    pp.set_pin(6, outputs_states[6][0])
                elif misc.constants.K_7 in keys or \
                                misc.constants.K_KP7 in keys:
                    outputs_states[7][0] = not outputs_states[7][0]
                    pp.set_pin(7, outputs_states[7][0])
                elif misc.constants.K_8 in keys or \
                                misc.constants.K_KP8 in keys:
                    outputs_states[8][0] = not outputs_states[8][0]
                    pp.set_pin(8, outputs_states[8][0])
                elif misc.constants.K_9 in keys or \
                                misc.constants.K_KP9 in keys:
                    outputs_states[9][0] = not outputs_states[9][0]
                    pp.set_pin(9, outputs_states[9][0])
                elif misc.constants.K_r in keys:
                    pp.reverse = not pp.reverse
                elif misc.constants.K_RETURN in keys:
                    result["testsuite_serial_port"] = address
                    return result
                _update(inputs_states, outputs_states, c, d, s, p)


if __name__ == "__main__":
    from .. import control
    control.set_develop_mode(True)
    control.defaults.event_logging = 0
    exp = control.initialize()
    ParallelPort._self_test(exp)
