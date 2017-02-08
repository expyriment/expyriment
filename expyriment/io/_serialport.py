"""
Input and output serial port.

This module contains a class implementing serial port input/output.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import atexit
from types import ModuleType, FunctionType

try:
    import serial
    from serial.tools.list_ports import comports as list_com_ports
except:
    serial = None
    list_com_ports = None

from . import defaults
from ._input_output import Input, Output
from .. import _internals, misc
from .._internals import CallbackQuitEvent


class SerialPort(Input, Output):
    """A class implementing a serial port input and output."""

    def __init__(self, port, baudrate=None, bytesize=None, parity=None,
                 stopbits=None, timeout=None, xonxoff=None, rtscts=None,
                 dsrdtr=None, input_history=None, os_buffer_size=None,
                 clock=None):
        """Create a serial port input and output.

        The port argument will accept the number of the port (e.g. 0 for COM1)
        as well as a string describing the full port location ("COM1" or
        "/dev/ttyS0").

        Notes
        -----
        An input_history can be used to overcome the size limitation of the
        receive buffer of the operating system. An input_history consists of a
        misc.ByteBuffer instance.
        In order to not miss any input, the serial port has to be updated
        regularly (i.e. calling read_input() or clear() before the receive
        buffer will be full). If the receive buffer size is set correctly, a
        warning will be given, when the input_history was not updated fast
        enough.
        Importantly, the fuller the receive buffer is, the longer clearing
        and polling will take (this can be more than 1 ms!), since all the
        bytes have to be transfered to the input_history.

        Parameters
        ----------
        port : int or str
            the port name
        baudrate : int, optional
        bytesize : int, optional
        parity : str, optional
            'E'=even, 'O'=odd, 'N'=none
        stopbits : int, optional
        timeout : int, optional
            the timeout for read(): -1=block
        xonxoff : int, optional
        rtscts : int, optional
        dsrdtr : int, optional
        input_history : bool, optional
            True if an input_history should be used
        os_buffer_size : int, optional
            the size of the receive input_history provided by the operating
            system in bytes
        clock : misc.Clock, optional
            an experimental clock
                            (optional)

        """

        if not isinstance(serial, ModuleType):
            message = """SerialPort can not be initialized.
The Python package 'pySerial' is not installed."""
            raise ImportError(message)

        serial_version = tuple(map(lambda x: int(x), serial.VERSION.split(".")))
        if serial_version < (2, 5):
            raise ImportError("Expyriment {0} ".format(__version__) +
                    "is not compatible with PySerial {0}.".format(
                        serial.VERSION) +
                      "\nPlease install PySerial 2.5 or higher.")

        Input.__init__(self)
        Output.__init__(self)
        if baudrate is None:
            baudrate = defaults.serialport_baudrate
        if bytesize is None:
            bytesize = defaults.serialport_bytesize
        if parity is None:
            parity = defaults.serialport_parity
        if stopbits is None:
            stopbits = defaults.serialport_stopbits
        if timeout is None:
            timeout = defaults.serialport_timeout
        if timeout == -1:
            timeout = None
        if xonxoff is None:
            xonxoff = defaults.serialport_xonxoff
        if rtscts is None:
            rtscts = defaults.serialport_rtscts
        if dsrdtr is None:
            dsrdtr = defaults.serialport_dsrdtr
        if clock is not None:
            self._clock = clock
        else:
            if _internals.active_exp.is_initialized:
                self._clock = _internals.active_exp.clock
            else:
                self._clock = misc.Clock()
        if input_history is None:
            input_history = defaults.serialport_input_history
        if input_history is True:
            self._input_history = misc.ByteBuffer(
                name="SerialPortBuffer (Port {0})".format(repr(port)),
                clock=self._clock)
        else:
            self._input_history = False
        if os_buffer_size is None:
            os_buffer_size = defaults.serialport_os_buffer_size
        self._os_buffer_size = os_buffer_size

        self._serial = serial.Serial(port, baudrate, bytesize, parity,
                                    stopbits, timeout, xonxoff, rtscts,
                                    dsrdtr)
        if not self._serial.isOpen():
            raise IOError("Could not open serial port")

        atexit.register(self.close)

    @property
    def input_history(self):
        """Getter for input_history."""

        return self._input_history

    @property
    def clock(self):
        """Getter for clock."""
        return self._clock

    @property
    def serial(self):
        """Getter for serial."""
        return self._serial

    @property
    def os_buffer_size(self):
        """Getter for os_buffer_size."""
        return self._os_buffer_size

    @property
    def baudrate(self):
        """Getter for baudrate."""

        return self._serial.baudrate

    @baudrate.setter
    def baudrate(self, value):
        """Setter for baudrate."""

        self._serial.baudrate = value

    @property
    def bytesize(self):
        """Getter for bytesize."""

        return self._serial.bytesize

    @bytesize.setter
    def bytesize(self, value):
        """Setter for bytesize."""

        self._serial.bytesize = value

    @property
    def parity(self):
        """Getter for parity."""

        return self._serial.parity

    @parity.setter
    def parity(self, value):
        """Setter for parity."""

        self._serial.parity = value

    @property
    def stopbits(self):
        """Getter for stopbits."""

        return self._serial.stopbits

    @stopbits.setter
    def stopbits(self, value):
        """Setter for stopbits."""

        self._serial.stopbits = value

    @property
    def timeout(self):
        """Getter for timeout."""

        return self._serial.timeout

    @timeout.setter
    def timeout(self, value):
        """Setter for timeout."""

        self._serial.timeout = value

    @property
    def xonxoff(self):
        """Getter for xonxoff."""

        return self._serial.xonxoff

    @xonxoff.setter
    def xonxoff(self, value):
        """Setter for xonxoff."""

        self._serial.xonxoff = value


    @property
    def rtscts(self):
        """Getter for rtscts."""

        return self._serial.rtscts

    @rtscts.setter
    def rtscts(self, value):
        """Setter for rtscts."""

        self._serial.rtscts = value

    @property
    def dsrdtr(self):
        """Getter for dsrdtr."""

        return self._serial.dsrdtr

    @dsrdtr.setter
    def dsrdtr(self, value):
        """Setter for dsrdtr."""

        self._serial.dsrdtr = value

    def close(self):
        """Close the serial port."""

        try:
            self._serial.close()
        except:
            pass

    @property
    def has_input_history(self):
        """Returns if a input_history exists or not (True / False)."""

        return isinstance(self._input_history, misc.ByteBuffer)

    def clear(self, skip_input_history=False):
        """Clear the serial port.

        Notes
        -----
        If an input_history is used, all data in the receive buffer, will be
        added to the history before clearing (via read_input()).
        Note: The copy process might take a few milliseconds. If you need a
        very fast clearing of the device buffer, you should skip copying the
        data into the input_history using the skip_input_history parameter.

        Parameters
        ----------
        skip_input_history : bool, optional
            if True available data will not be copied to the input_history.
            (default = False)

        """

        if self.has_input_history and not skip_input_history:
            self.read_input()
        else:
            self._serial.flushInput()
        if self._logging:
            _internals.active_exp._event_file_log("SerialPort {0},cleared".\
                           format(repr(self._serial.port)), 2)

    def read_input(self):
        """Read all input from serial port.

        If a input_history is used, all received data will be added.

        Returns
        -------
        out : list of bytes

        """

        read_time = self._clock.time
        read = self._serial.read(self._serial.inWaiting())
        if len(read) > 0:
            read = list(map(ord, list(read)))
            if self.has_input_history:
                if len(self._input_history.memory):
                    last_time = self._input_history.memory[-1][1]
                else:
                    last_time = 0 #first time
                self._input_history.add_events(read)
                if len(read) >= (self._os_buffer_size - 1) and last_time:
                    warn_message = "{0} not updated for {1} ms!".format(
                                        self._input_history.name,
                                        read_time - last_time)
                    print("Warning: " + warn_message)
                    _internals.active_exp._event_file_warn(warn_message)
            if self._logging:
                _internals.active_exp._event_file_log(
                        "SerialPort {0}, read input, {1} bytes".format(
                        repr(self._serial.port), len(read)), 2)
            return read
        return []

    def poll(self):
        """Poll the serial port.

        If a input_history is used, it will be added.

        Returns
        -------
        out : byte
             one byte only will be returned
        """

        poll_time = self._clock.time
        read = self._serial.read()
        if read != "":
            if self.has_input_history:
                last = self._input_history.get_last_event()
                self._input_history.add_event(ord(read))
                if last[1] > 0: # if input_history is empty
                    if self._serial.inWaiting() >= (self._os_buffer_size - 1):
                        warn_message = "{0} not updated for {1} ms!".format(
                                            self._input_history.name,
                                            poll_time - last[1])
                        print("Warning: " + warn_message)
                        _internals.active_exp._event_file_warn(warn_message)
            if self._logging:
                _internals.active_exp._event_file_log(
                        "SerialPort {0},received,{1},poll".format(
                        repr(self._serial.port), ord(read)), 2)
            return ord(read)
        return None

    def read_line(self, duration=None, callback_function=None,
                  process_control_events=True):
        """Read a line from serial port (until newline) and return string.

        The function is waiting for input. Use the duration parameter
        to avoid too long program blocking.

        Parameters
        ----------
        duration : int, optional
            try to read for given amount of time (default=None)
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        line : str

        Notes
        -----
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        See Also
        --------
        design.experiment.register_wait_callback_function

        """

        if _internals.skip_wait_methods:
            return

        rtn_string = ""
        if duration is not None:
            timeout_time = self._clock.time + duration

        if self._logging:
            _internals.active_exp._event_file_log(
                    "SerialPort {0}, read line, start".format(
                    repr(self._serial.port)), 2)

        while True:
            if isinstance(callback_function, FunctionType):
                rtn_callback = callback_function()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    rtn_string = rtn_callback
                    break
            if _internals.active_exp is not None and \
               _internals.active_exp.is_initialized:
                rtn_callback = _internals.active_exp._execute_wait_callback()
                if isinstance(rtn_callback, CallbackQuitEvent):
                    rtn_string = rtn_callback
                    break
                if process_control_events:
                    if _internals.active_exp.mouse.process_quit_event() or \
                       _internals.active_exp.keyboard.process_control_keys():
                        break
                else:
                    _internals.pump_pygame_events()

            byte = self.poll()
            if byte:
                byte = chr(byte)
                if byte != '\n' and byte != '\r':
                    rtn_string = rtn_string + byte
                elif byte == '\n':
                    break
                elif byte == '\r':
                    pass
            elif duration is not None and self._clock.time >= timeout_time:
                break
        if self._logging:
            _internals.active_exp._event_file_log("SerialPort {0}, read line, end"\
                                .format(repr(self._serial.port)), 2)
        return rtn_string

    @staticmethod
    def get_available_ports():
        """Return a list of strings representing the available serial ports.

        Notes
        -----
        If pyserial is not installed, 'None' will be returned.

        Returns
        -------
        arr : list
            list of strings representing the available serial ports

        """

        if not isinstance(serial, ModuleType):
            return None
        ports = sorted([x[0] for x in list_com_ports()])
        return ports

    def send(self, data):
        """Send data via the serial port.

        Parameters
        ----------
        data : int
            data to be send (int)

        """

        self._serial.write(chr(data))
        if self._logging:
            _internals.active_exp._event_file_log("SerialPort {0},sent,{1}"\
                                .format(repr(self._serial.port), data), 2)


    @staticmethod
    def _self_test(exp):
        """Test the serial port"""

        from .. import io, stimuli
        def int2bin(n, count=8):
            return "".join([str((n >> y) & 1) for y in range(count - 1, -1, -1)])

        result = {}
        result["testsuite_serial_port"] = ""
        result["testsuite_serial_baudrate"] = ""
        result["testsuite_serial_parity"] = ""
        result["testsuite_serial_stopbits"] = ""
        result["testsuite_serial_success"] = "No"

        ports = io.SerialPort.get_available_ports()
        if ports is None:
            stimuli.TextScreen(
                            "The Python package 'pySerial' is not installed!",
                               "[Press RETURN to continue]").present()
            exp.keyboard.wait(misc.constants.K_RETURN)
            return result

        elif ports == []:
            stimuli.TextScreen("No serial ports found!",
                               "[Press RETURN to continue]").present()
            exp.keyboard.wait(misc.constants.K_RETURN)
            return result

        else:
            import serial

            idx = io.TextMenu("Select Serial Port", ports, width=200,
                                         justification=1, scroll_menu=5).get()
            comport = ports[idx]

            rates = [0, 50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400,
                     4800, 9600, 19200, 38400, 57600, 115200, 230400, 460800,
                     500000, 576000, 921600, 1000000, 1152000, 1500000, 2000000,
                     2500000, 3000000, 3500000, 4000000]
            idx = io.TextMenu("Select Baudrate", [repr(x) for x in rates],
                                         width=200, justification=1,
                                         scroll_menu=2).get(preselected_item=14)
            baudrate = rates[idx]

            parities = ["N", "E", "O"]
            idx = io.TextMenu("Select Parity", parities, width=200,
                                         justification=1, scroll_menu=2).get(
                                             preselected_item=0)
            parity = parities[idx]

            stopbits = [0, 1, 1.5, 2]
            idx = io.TextMenu("Select Stopbits", [repr(x) for x in stopbits],
                                         width=200, justification=1,
                                         scroll_menu=2).get(preselected_item=1)
            stopbit = stopbits[idx]

            stimuli.TextScreen("Serial Port {0}".format(comport),
                                                                "").present()
            try:
                ser = io.SerialPort(port=comport, baudrate=baudrate,
                                               parity=parity, stopbits=stopbit,
                                               input_history=True)
            except serial.SerialException:
                stimuli.TextScreen("Could not open {0}!".format(comport),
                                   "[Press RETURN to continue]").present()
                exp.keyboard.wait(misc.constants.K_RETURN)
                result["testsuite_serial_port"] = comport
                result["testsuite_serial_baudrate"] = baudrate
                result["testsuite_serial_parity"] = parity
                result["testsuite_serial_stopbits"] = stopbit
                result["testsuite_serial_success"] = "No"
                return result
            cnt = 0
            while True:
                read = ser.read_input()
                if len(read) > 0:
                    byte = read[-1]
                    cnt = ser.input_history.get_size()
                    if byte is not None:
                        stimuli.TextScreen("Serial Port {0}".format(comport),
                                      "{0}\n {1} - {2}".format(cnt, byte,
                                       int2bin(byte))).present()
                key = exp.keyboard.check()
                if key:
                    break

            result["testsuite_serial_port"] = comport
            result["testsuite_serial_baudrate"] = baudrate
            result["testsuite_serial_parity"] = parity
            result["testsuite_serial_stopbits"] = stopbit
            result["testsuite_serial_success"] = "Yes"
            return result
