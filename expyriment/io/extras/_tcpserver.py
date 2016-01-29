"""TCP server.

This module contains a class implementing a TCP network server.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import socket
import errno

import _tcpserver_defaults as defaults
import expyriment
from expyriment.misc._timer import get_time
from expyriment.io._keyboard import Keyboard
from expyriment.io._input_output import Input, Output


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
                expyriment._active_exp._event_file_log(
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
                expyriment._active_exp._event_file_log(
                    "TcpServer,sent,{0}".format(data))

    def wait(self, length, package_size=None, duration=None,
             check_control_keys=True):
        """Wait for data.

        Parameters:
        -----------
        length : int
            The length of the data to be waited for in bytes.
            If not set, a single package will be waited for.
        package_size : int, optional
            The size of the package to be waited for, optional.
            If not set, the default package size will be used.
            If length < package_size, package_size = length.
        duration: int, optional
            The duration to wait in milliseconds.
        process_control_keys : bool, optional
            Check if control key has been pressed (default = True).

        Returns:
        --------
        data : str
            The received data.
        rt : int
            The time it took to receive the data in milliseconds.
        """

        if expyriment.control.defaults._skip_wait_functions:
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
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    rtn_callback = expyriment._active_exp._execute_wait_callback()
                    if isinstance(rtn_callback,
                                      expyriment.control.CallbackQuitEvent):
                        return rtn_callback, int((get_time() - start) * 1000)

                    if check_control_keys:
                        if Keyboard.process_control_keys():
                            break
            if duration:
                if int((get_time() - start) * 1000) >= duration:
                    data = None
                    rt = None
                    break

        if self._logging:
            expyriment._active_exp._event_file_log(
                            "TcpServer,received,{0},wait".format(data))

        return data, rt


    def clear(self):
        """Read the stream empty."""

        try:
            self._socket.recv(1024000000000)
        except:
            pass
        if self._logging:
            expyriment._active_exp._event_file_log(
                            "TcpServer,cleared,wait", 2)

    def close(self):
        """Close the connection to the client."""

        if self._is_connected:
            self._client[0].close()
            self._client = None
            self._is_connected = False
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "TcpServer,closed")
