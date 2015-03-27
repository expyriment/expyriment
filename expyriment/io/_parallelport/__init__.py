"""
Input and output parallel port.

This module contains a class implementing parallel port input/output on Linux
and Windows.

This module is a modified version of the parallel module of PsychoPy
(www.psychopy.org).
The code in this file is heavily based on the original code.
The file '_inpout32.py' was only slightly modified to remove numpy dependency.
The files '_dlportio.py 'and '_linux.py' are the original files without
modification.

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
import os

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

        data = (int('{:05b}'.format(s)[::-1], 2) << 8) + d
        if self._logging:
            expyriment._active_exp._event_file_log(
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

        result = {}
        result["testsuite_parallel_port"] = ""
        result["testsuite_parallel_success"] = "No"

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

            expyriment.stimuli.TextScreen(
                "ParallelPort can not be initialized!",
                _message + "\n\n[Press RETURN to continue]").present()
            exp.keyboard.wait(expyriment.misc.constants.K_RETURN)
            return result

        else:
            text = "This will test if parallel port " \
                   "communication works correctly.\n\n" \
                   "You will be asked to enter a port address. " \
                   "On Windows this will be a hexadecimal number (e.g. " \
                   "'0x0378', which is ofter the address of LPT1). " \
                   "On Linux it will be of the form '/dev/parportX', "\
                   "where X denotes the number of the port.\n\n" \
                   "Once the port is opened, a list of status and data " \
                   "pins is presented. Bright green lights indicate " \
                   "input activity of a pin. Bright red lights indicate " \
                   "output activity of a pin. With the number keys on the " \
                   "keyboard, sending can be toggled on and off for each " \
                   "data pin.\n\n\n\n" \
                   "[Press RETURN to continue]"
            t = expyriment.stimuli.TextScreen("ParallelPort test", text)
            t.present()
            exp.keyboard.wait(expyriment.misc.constants.K_RETURN)

            address = expyriment.io.TextInput("Port address:").get()
            try:
                pp = expyriment.io.ParallelPort(address=address)
            except:
                expyriment.stimuli.TextScreen(
                    "Could not open port address {0}!".format(address),
                    "[Press RETURN to continue]").present()
                exp.keyboard.wait(expyriment.misc.constants.K_RETURN)
                return result

            pin_canvas = expyriment.stimuli.Canvas((600, 400))
            poll = expyriment.stimuli.TextLine("Total",
                                               position=[0, 175])
            poll.plot(pin_canvas)
            poll_line = expyriment.stimuli.Rectangle((500, 2),
                                                       position=[0, 135])
            poll_line.plot(pin_canvas)
            status = expyriment.stimuli.TextLine("Status",
                                                 text_colour=expyriment.misc.constants.C_EXPYRIMENT_PURPLE,
                                                 position=[-160, 95])
            status.plot(pin_canvas)
            status_line = expyriment.stimuli.Rectangle((180, 2),
                                                       colour=expyriment.misc.constants.C_EXPYRIMENT_PURPLE,
                                                       position=[-160, 50])
            status_line.plot(pin_canvas)
            data = expyriment.stimuli.TextLine("Data",
                                               text_colour=expyriment.misc.constants.C_EXPYRIMENT_ORANGE,
                                               position=[100, 95])
            data.plot(pin_canvas)
            data_line = expyriment.stimuli.Rectangle((300, 2),
                                                     colour=expyriment.misc.constants.C_EXPYRIMENT_ORANGE,
                                                     position=[100, 50])
            data_line.plot(pin_canvas)

            pins = {}
            inputs = {}
            outputs = {}
            x_pos = -240
            for pin in [10, 11, 12, 13, 15, 9, 8, 7, 6, 5, 4, 3, 2]:
                inputs[pin] = expyriment.stimuli.Circle(10,
                                                        anti_aliasing=10,
                                                        position=[x_pos, 30])
                if pin < 10:
                    colour = expyriment.misc.constants.C_EXPYRIMENT_ORANGE
                else:
                    colour = expyriment.misc.constants.C_EXPYRIMENT_PURPLE

                stim = expyriment.stimuli.TextLine(repr(pin),
                                                   text_font="freemono",
                                                   text_colour=colour,
                                                   position=[x_pos, 0])
                stim.plot(pin_canvas)
                pins[pin] = stim
                if pin < 10:
                    outputs[pin] = expyriment.stimuli.Rectangle(
                        (20, 20), position=[x_pos, -30])
                x_pos += 40

            instruction = expyriment.stimuli.TextLine(
                "Toggle sending to data pins 2-9 with number keys",
                position=[0, -120])
            instruction.plot(pin_canvas)

            end = expyriment.stimuli.TextLine(
                "[Press RETURN to end the test]",
                position=[0, -160])
            end.plot(pin_canvas)

            pin_canvas.present()
            pin_canvas.present()
            pin_canvas.present()

            def _update(inputs_states, outputs_states, read_status,
                        read_data, read_poll):
                for pin in inputs.keys():
                    if inputs_states[pin] == True:
                        inputs[pin].colour = [0, 255, 0]
                    else:
                        inputs[pin].colour = [0, 30, 0]
                    inputs[pin].present(clear=False, update=False)
                    inputs[pin].present(clear=False, update=False)
                    inputs[pin].present(clear=False, update=False)

                for pin in outputs.keys():
                    if outputs_states[pin] == True:
                        outputs[pin].colour = [255, 0, 0]
                    else:
                        outputs[pin].colour = [30, 0, 0]
                    outputs[pin].present(clear=False, update=False)
                    outputs[pin].present(clear=False, update=False)
                    outputs[pin].present(clear=False, update=False)

                results_canvas = expyriment.stimuli.Canvas(
                    (600, 20),
                    colour=expyriment._active_exp.background_colour,
                    position=[0, 70])

                rs = expyriment.stimuli.TextLine(
                    "({0})".format(read_status),
                    text_colour=[100, 100, 100],
                    position=[-160, 0])
                rs.plot(results_canvas)

                rd = expyriment.stimuli.TextLine(
                    "({0})".format(read_data),
                    text_colour=[100, 100, 100],
                    position=[100, 0])
                rd.plot(results_canvas)

                poll_canvas = expyriment.stimuli.Canvas(
                    (100, 20),
                    colour=expyriment._active_exp.background_colour,
                    position=[0, 150])

                pd = expyriment.stimuli.TextLine(
                    "({0})".format(read_poll),
                    text_colour=[100, 100, 100])
                pd.plot(poll_canvas)

                poll_canvas.present(clear=False, update=False)
                poll_canvas.present(clear=False, update=False)
                poll_canvas.present(clear=False, update=False)

                results_canvas.present(clear=False, update=False)
                results_canvas.present(clear=False, update=False)
                results_canvas.present(clear=False, update=False)

                exp.screen.update()

            inputs_states = {2:False, 3:False, 4:False, 5:False, 6:False,
                              7:False, 8:False, 9:False, 10:False, 11:False,
                              12:False, 13:False, 15:False}

            outputs_states = {2:False, 3:False, 4:False, 5:False, 6:False,
                              7:False, 8:False, 9:False}

            pp.send(0)
            initial_poll = pp.poll()

            while True:
                s = pp.read_status()
                d = pp.read_data()
                p = pp.poll()

                if p != initial_poll:
                    result["testsuite_serial_success"] = "Yes"

                for pin, bit in {2:1, 3:2, 4:4, 5:8, 6:16, 7:32, 8:64,
                                 9:128, 10:256, 11:512, 12:1024, 13:2048,
                                 15:4096}.iteritems():
                    if bit & p > 0:
                        inputs_states[pin] = True
                    else:
                        inputs_states[pin] = False

                key = exp.keyboard.check()
                if key == expyriment.misc.constants.K_2 or \
                                key == expyriment.misc.constants.K_KP2:
                    outputs_states[2] =  not outputs_states[2]
                    pp.set_pin(2, outputs_states[2])
                elif key == expyriment.misc.constants.K_3 or \
                                key == expyriment.misc.constants.K_KP3:
                    outputs_states[3] = not outputs_states[3]
                    pp.set_pin(3, outputs_states[3])
                elif key == expyriment.misc.constants.K_4 or \
                                key == expyriment.misc.constants.K_KP4:
                    outputs_states[4] = not outputs_states[4]
                    pp.set_pin(4, outputs_states[4])
                elif key == expyriment.misc.constants.K_5 or \
                                key == expyriment.misc.constants.K_KP5:
                    outputs_states[5] = not outputs_states[5]
                    pp.set_pin(5, outputs_states[5])
                elif key == expyriment.misc.constants.K_6 or \
                                key == expyriment.misc.constants.K_KP6:
                    outputs_states[6] = not outputs_states[6]
                    pp.set_pin(6, outputs_states[6])
                elif key == expyriment.misc.constants.K_7 or \
                                key == expyriment.misc.constants.K_KP7:
                    outputs_states[7] = not outputs_states[7]
                    pp.set_pin(7, outputs_states[7])
                elif key == expyriment.misc.constants.K_8 or \
                                key == expyriment.misc.constants.K_KP8:
                    outputs_states[8] = not outputs_states[8]
                    pp.set_pin(8, outputs_states[8])
                elif key == expyriment.misc.constants.K_9 or \
                                key == expyriment.misc.constants.K_KP9:
                    outputs_states[9] = not outputs_states[9]
                    pp.set_pin(9, outputs_states[9])
                elif key == expyriment.misc.constants.K_RETURN:
                    result["testsuite_serial_port"] = address
                    return result
                _update(inputs_states, outputs_states, s, d, p)
