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

    def __init__(self, host, port, default_package_size=None, connect=None):
        """Create a TcpClient and connect to it.

        Parameters:
        -----------
        host : str
            The hostname or IPv4 address of the server to connect to.
        port : int
            The port to connect to.
        default_package_size : int
            The default size of the packages to be received.
        connect : bool, optional
            If True, connect immediately.

        """

        Input.__init__(self)
        Output.__init__(self)

        self._host = host
        self._port = port
        if default_package_size is None:
            default_package_size = defaults.tcpclient_default_package_size
        self._default_package_size = default_package_size
        self._socket = None
        self._is_connected = False
        if connect is None:
            connect = defaults.tcpclient_connect
        if connect:
            self.connect()

    _getter_exception_message = "Cannot set {0} if connected!"

    @property
    def host(self):
        """Getter for host."""

        return self._host

    @host.setter
    def host(self, value):
        """Setter for host."""

        if self._is_connected:
            raise AttributeError(
                TcpClient._getter_exception_message.format("host"))
        else:
            self._host = value

    @property
    def port(self):
        """Getter for port."""

        return self._port

    @port.setter
    def port(self, value):
        """Setter for port."""

        if self._is_connected:
            raise AttributeError(
                TcpClient._getter_exception_message.format("port"))
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
                TcpClient._getter_exception_message.format(
                    "default_package_size"))
        else:
            self._default_package_size = value

    @property
    def is_connected(self):
        """Getter for is_connected."""

        return self._is_connected

    def connect(self):
        """Connect to the server."""

        if not self._is_connected:
            try:
                self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self._socket.connect((self._host, self._port))
                self._is_connected = True
                self._socket.settimeout(0)
            except socket.error:
                raise RuntimeError(
                    "TCP connection to {0}:{1} failed!".format(self._host,
                                                               self._port))
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "TcpClient,connected,{0}:{1}".format(self._host,
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

    def wait(self, package_size=None, duration=None,
             check_control_keys=True):
        """Wait for data.

        Parameters:
        -----------
        package_size : int, optional
            The size of the package to be received, optional.
            If not set, the default package size will be used.
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

        See Also
        --------
        design.experiment.register_wait_callback_function

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
                if data is None:
                    data = self._socket.recv(package_size)
                while len(data) < package_size:
                    data = data + self._socket.recv(package_size)
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
                            "TcpClient,received,{0},wait".format(data))
        return data, rt


    def clear(self):
        """Read the stream empty."""

        try:
            self._socket.recv(1024000000000)
        except:
            pass

        if self._logging:
            expyriment._active_exp._event_file_log(
                            "TcpClient,cleared,wait", 2)

    def close(self):
        """Close the connection to the server."""

        if self._is_connected:
            self._socket.close()
            self._socket = None
            self._is_connected = False
            if self._logging:
                expyriment._active_exp._event_file_log(
                    "TcpClient,closed")