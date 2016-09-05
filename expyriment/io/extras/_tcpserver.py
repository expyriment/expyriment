"""TCP server.

This module contains a class implementing a TCP network server.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import socket
import errno
from types import FunctionType

from ... import _internals
from ...misc._timer import get_time
from ..._internals import CallbackQuitEvent
from ...io._keyboard import Keyboard
from ...io._input_output import Input, Output
from . import _tcpserver_defaults as defaults



class TcpServer(Input, Output):
    """A class implementing a TCP network server for a single client."""

    def __init__(self, port, default_package_size=None, start_listening=True):
        """Create a TcpServer.

        Parameters:
        -----------
        port : int
            The port to connect to.
        default_package_size : int, optional
            The default size of the packages to be received.
        start_listening : bool
            If True, start listening on port immediately.

        """

        Input.__init__(self)
        Output.__init__(self)

        self._port = port
        if default_package_size is None:
            default_package_size = defaults.tcpserver_default_package_size
        self._default_package_size = default_package_size
        self._socket = None
        self._is_connected = False
        if start_listening is None:
            start_listening = defaults.tcpserver_start_listening
        if start_listening:
            self.listen()

    _getter_exception_message = "Cannot set {0} if connected!"

    @property
    def port(self):
        """Getter for port."""

        return self._port

    @port.setter
    def port(self, value):
        """Setter for port."""

        if self._is_connected:
            raise AttributeError(
                TcpServer._getter_exception_message.format("port"))
        else:
            self._port = value

    @property
    def default_package_size(self):
        """Getter for default_package_size."""

        return self._default_package_size

    @default_package_size.setter
    def default_package_size(self, value):
        """Setter for default_package_size."""

        if self._is_connected:
            raise AttributeError(
                TcpServer._getter_exception_message.format(
                    "default_package_size"))
        else:
            self._default_package_size = value

    @property
    def is_connected(self):
        """Getter for is_connected."""

        return self._is_connected

    def listen(self):
        """Listen for a connection on port."""

        if not self._is_connected:
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.bind(('', self._port))
                self._socket.listen(1)
                self._client = self._socket.accept()
                self._is_connected = True
            except socket.error:
                raise RuntimeError(
                    "Listening for TCP connection on port {0} failed!".format(
                        self._port))
            if self._logging:
                _internals.active_exp._event_file_log(
                    "TcpServer,client connected,{0}".format(self._client[1]))

    def send(self, data):
        """Send data.

        Parameters:
        -----------
        data : str
            The data to be sent.

        """

        self._socket.sendall(data)
        if self._logging:
                _internals.active_exp._event_file_log(
                    "TcpServer,sent,{0}".format(data))

    def wait(self, length, package_size=None, duration=None,
             callback_function=None, process_control_events=True):
        """Wait for data.

        Parameters
        ----------
        length : int
            The length of the data to be waited for in bytes.
            If not set, a single package will be waited for.
        package_size : int, optional
            The size of the package to be waited for, optional.
            If not set, the default package size will be used.
            If length < package_size, package_size = length.
        duration: int, optional
            The duration to wait in milliseconds.
        callback_function : function, optional
            function to repeatedly execute during waiting loop
        process_control_events : bool, optional
            process ``io.Keyboard.process_control_keys()`` and
            ``io.Mouse.process_quit_event()`` (default = True)

        Returns
        -------
        data : str
            The received data.
        rt : int
            The time it took to receive the data in milliseconds.

        Notes
        -----
        This will also by default process control events (quit and pause).
        Thus, keyboard events will be cleared from the cue and cannot be
        received by a Keyboard().check() anymore!

        """

        if _internals.skip_wait_methods:
            return None, None

        start = get_time()
        data = None
        rt = None

        if package_size is None:
            package_size = self._default_package_size
        if length is None:
            length = package_size
        elif length < package_size:
            package_size = length
        while True:
            try:
                if data is None:
                    data = self._client[0].recv(package_size)
                while len(data) < length:
                    if length - len(data) >= package_size:
                        data = data + self._client[0].recv(package_size)
                    else:
                        data = data + self._client[0].recv(length - len(data))
                    if duration:
                        if int((get_time() - start) * 1000) >= duration:
                            data = None
                            rt = None
                            break
                rt = int((get_time() - start) * 1000)
                break
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    if isinstance(callback_function, FunctionType):
                        callback_function()
                    if _internals.active_exp is not None and \
                    _internals.active_exp.is_initialized:
                        rtn_callback = _internals.active_exp._execute_wait_callback()
                        if isinstance(rtn_callback, CallbackQuitEvent):
                            data = rtn_callback
                            rt = int((get_time() - start) * 1000)
                            break
                        if process_control_events:
                            if _internals.active_exp.mouse.process_quit_event() or \
                            _internals.active_exp.keyboard.process_control_keys():
                                break
                        else:
                            _internals.pump_pygame_events()

            if duration:
                if int((get_time() - start) * 1000) >= duration:
                    data = None
                    rt = None
                    break

        if self._logging:
            _internals.active_exp._event_file_log(
                            "TcpServer,received,{0},wait".format(data))

        return data, rt


    def clear(self):
        """Read the stream empty."""

        try:
            self._socket.recv(1024000000000)
        except:
            pass
        if self._logging:
            _internals.active_exp._event_file_log(
                            "TcpServer,cleared,wait", 2)

    def close(self):
        """Close the connection to the client."""

        if self._is_connected:
            self._client[0].close()
            self._client = None
            self._is_connected = False
            if self._logging:
                _internals.active_exp._event_file_log(
                    "TcpServer,closed")
