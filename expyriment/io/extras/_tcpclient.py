"""TCP client.

This module contains a class implementing a TCP network client.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import socket
import errno

import _tcpclient_defaults as defaults
import expyriment
from expyriment.misc._timer import get_time
from expyriment.io._keyboard import Keyboard
from expyriment.io._input_output import Input, Output


class TcpClient(Input, Output):
    """A class implementing a TCP network client."""

    def __init__(self, ip, port, default_package_size=None, connect=None):
        """Create a TcpClient and connect to it.

        Parameters:
        -----------
        ip : str
            The IP address of the server to connect to.
        port : int
            The port to connect to.
        default_package_size : int
            The default size of the packages to be received.
        connect : bool, optional
            If True, connect immediately.

        """

        Input.__init__(self)
        Output.__init__(self)

        self._ip = ip
        self._port = port
        if default_package_size is None:
            default_package_size = defaults.tcpclient_default_package_size
        self._default_package_size = default_package_size
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.settimeout(0)
        self._is_connected = False
        if connect is None:
            connect = defaults.tcpclient_connect
        if connect:
            self._socket.connect(self._ip, self._port)
            self._is_connected = True


    @property
    def ip(self):
        """Getter for ip."""

        return self._ip


    @property
    def port(self):
        """Getter for port."""

        return self._port


    @property
    def default_package_size(self):
        """Getter for default_package_size."""

        return self._default_package_size


    @property
    def is_connected(self):
        """Getter for is_connected."""

        return self._is_connected


    def connect(self):
        """Connect to the server."""

        if not self._is_connected:
            try:
                self._socket.connect(self._ip, self._port)
                self._is_connected = True
            except:
                raise RuntimeError(
                    "TCP connection to {0}:{1} failed!".format(self._ip,
                                                               self._port))
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "TcpClient,connected,{0}:{1}".format(self._ip,
                                                         self._port))


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
                            "TcpClient,sent,{0}".format(data))


    def wait(self, package_size=None):
        """Wait for data.

        Parameters:
        -----------
        package_size : int
            The size of the package to be received, optional.
            If not set, the default package size will be used.

        Returns:
        --------
        data : str
            The received data.

        """

        if expyriment.control.defaults._skip_wait_functions:
            return None, None

        start = get_time()
        data = None
        rt = None

        if package_size is None:
            package_size = self._default_package_size
        while True:
            try:
                data = self._socket.recv(package_size)
                rt = int((get_time() - start) * 1000)
                break
            except socket.error, e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    expyriment._active_exp._execute_wait_callback()
                    if Keyboard.process_control_keys():
                        break
        if self._logging:
            expyriment._active_exp._event_file_log(
                            "TcpClient,received,{0},wait".format(data))
        return data, rt


    def close(self):
        """Close the connection to the server."""

        if self._is_connected:
            self._socket.close()
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "TcpClient,closed")