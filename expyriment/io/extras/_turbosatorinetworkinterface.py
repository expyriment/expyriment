"""Turbo-Satori network interface.

This module contains a class implementing a network interface for Turbo-Satori
(see www.brainvoyager.com/products/turbosatori.html).

"""
from __future__ import absolute_import, print_function, division
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import struct

from . import _turbosatorinetworkinterface_defaults as defaults
from ...misc._timer import get_time
from ...misc._miscellaneous import byte2unicode
from ...io._input_output import Input, Output
from ...io.extras._tcpclient import TcpClient


class TurbosatoriNetworkInterface(Input, Output):
    """A class implementing a network interface to Turbo-Satori.

    See http://www.brainvoyager.com/products/turbosatori.html
    for more information.

     """

    def __init__(self, host, port, timeout=None, connect=None):
        """Create a TurbosatoriNetworkInterface.

        Parameters:
        -----------
        host : str
            The hostname or IPv4 address of the TBV server to connect to.
        port : int
            The port on the Turbo-Satori server to connect to.
        timeout : int, optional
            The maximal time to wait for a response from the server for each
            request.
        connect : bool, optional
            If True, connect immediately.

        """

        Input.__init__(self)
        Output.__init__(self)

        self._host = host
        self._port = port
        self._is_connected = False
        self._turbosatori_plugin_version = None
        self._tcp = TcpClient(host, port, None, False)
        if timeout is None:
            timeout = defaults.turbosatorinetworkinterface_timeout
        self._timeout = timeout
        if connect is None:
            connect = defaults.turbosatorinetworkinterface_connect
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
                TurbosatoriNetworkInterface._getter_exception_message.format("host"))
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
                TurbosatoriNetworkInterface._getter_exception_message.format("port"))
        else:
            self._port = value

    @property
    def is_connected(self):
        """Getter for is_connected."""

        return self._is_connected

    @property
    def turbosatori_plugin_version(self):
        """Getter for turbosatori_plugin_version."""

        return self._turbosatori_plugin_version

    @property
    def timeout(self):
        """Getter for timeout."""

        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """Setter for timeout."""

        if self._is_connected:
            raise AttributeError(
                TurbosatoriNetworkInterface._getter_exception_message.format(
                    "timeout"))
        else:
            self._timeout = value

    def connect(self):
        """Connect to the TBV server."""

        if not self._is_connected:
            self._tcp.connect()
            data, rt = self.request_data("Request Socket")
            try:
                self._turbosatori_plugin_version = (
                    struct.unpack('!i', data[:4])[0],
                    struct.unpack('!i', data[4:8])[0],
                    struct.unpack('!i', data[8:])[0])
            except:
                raise RuntimeError("Requesting a socket failed!")
            self._is_connected = True
            if self._logging:
                _globals.active_exp._event_file_log(
                    "TurbosatoriNetworkInterface,connected,{0}:{1}".format(
                        self._host, self._port))

    def _send(self, message, *args):
        length = len(message)
        arg_length = 0
        if len(args) > 0:
            for arg in args:
                arg_length += len(arg)
        data = struct.pack('!q', length + 5 + arg_length) + \
            "\x00\x00\x00{0}{1}\x00".format(chr(length + 1), message)
        if len(args) > 0:
            for arg in args:
                data += arg
        self._tcp.send(data)

    def _wait(self):
        receive, rt = self._tcp.wait(package_size=8, duration=self.timeout,
                                     check_control_keys=False)
        data = None
        if receive is not None:
            length = struct.unpack('!q', receive)[0]
            data, rt = self._tcp.wait(package_size=length, duration=self._timeout,
                                      check_control_keys=False)
        if receive is None or data is None:
            return None
        else:
            return data[4:]

    def request_data(self, request, *args):
        """Request data from Turbo-Satori.

        Parameters:
        -----------
        request : str
            The request to be sent to Turbo-Satori.

        Returns:
        --------
        data : str
            The byte string of the received data.
        rt : int
            The time it took to get the data.

        """

        start = get_time()
        self._tcp.clear()
        self._send(request, *args)
        data = self._wait()
        if data is None:
            return None, None
        elif data[0:len(request)] != request:
            return data, None
        else:
            return data[len(request) + 1:], int((get_time() - start) * 1000)

    def close(self):
        """Close the connection."""

        self._tcp.close()
        self._is_connected = False

    # Basic Project Queries
    def get_current_time_point(self):
        """Get the current time point.

        Returns:
        --------
        time_point : int
            The current time point.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetCurrentTimePoint")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!i', data)[0], rt

    def get_nr_of_channels(self):
        """Get the number of channels.

        Returns:
        --------
        nr_channels : int
            The number of channels.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetNrOfChannels")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!i', data)[0], rt

    def get_values_feedback_folder(self):
        """Get the feedback folder for the values.

        Returns:
        --------
        folder : str
            The feedback folder.
        rt : int
            The time it took to get the data.

        """

        folder, rt = self.request_data("tGetValuesFeedbackFolder")
        if folder is None:
            return None, rt
        elif folder[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(folder[19:-1]))
        else:
            return byte2unicode(folder[4:-1]), rt

    def get_images_feedback_folder(self):
        """Get the feedback folder for the images.

        Returns:
        --------
        folder : str
            The feedback folder.
        rt : int
            The time it took to get the data.

        """

        folder, rt = self.request_data("tGetImagesFeedbackFolder")
        if folder is None:
            return None, rt
        elif folder[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(folder[19:-1]))
        else:
            return byte2unicode(folder[4:-1]), rt

    def get_nr_of_selected_channels(self):
        """Get the number of selected channels.

        Returns:
        --------
        nr_selected_channels : int
            The number of selected channels.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetNrOfSelectedChannels")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!i', data)[0], rt

    def get_selected_channels(self):
        """Get the selected channels.

        Returns:
        --------
        channels : list
            The selected channels.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetSelectedChannels")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return ([struct.unpack('!i', data[x * 4:x * 4 + 4])[0]
                     for x in range(0, len(data) // 4)], rt)

    def get_raw_data_scale_factor(self):
        """Get the scale factor set in the GUI for raw data.

        Returns:
        --------
        scale_factor : float
            The scale factor.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetRawDataScaleFactor")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data)[0], rt

    def get_raw_data_wl1(self, channel, frame):
        """Get raw data for wavelength 1.

        Parameters:
        ----------
        channel : int
            The channel.
        frame : int
            The time point.

        Returns:
        --------
        data : float
            The raw data.
        rt : int
            The time it took to get the data.

        """

        channel = struct.pack('!i', channel)
        frame = struct.pack('!i', frame)
        data, rt = self.request_data("tGetRawDataWL1", channel, frame)
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data[8:])[0], rt

    def get_raw_data_wl2(self, channel, frame):
        """Get raw data for wavelength 2.

        Parameters:
        ----------
        channel : int
            The channel.
        frame : int
            The time point.

        Returns:
        --------
        data : float
            The raw data.
        rt : int
            The time it took to get the data.

        """

        channel = struct.pack('!i', channel)
        frame = struct.pack('!i', frame)
        data, rt = self.request_data("tGetRawDataWL2", channel, frame)
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data[8:])[0], rt

    def is_data_oxy_deoxy_converted(self):
        """Check if oxy/deoxy values are requested and have been calculated.

        Returns:
        --------
        is_converted : bool
            True if oxy/deoxy converted, False otherwise
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tIsDataOxyDeoxyConverted")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return bool(struct.unpack('!i', data)[0]), rt

    def get_oxy_data_scale_factor(self):
        """Get the scale factor set in the GUI for oxy/deoxy data.

        Returns:
        --------
        scale_factor : float
            The scale factor.
        rt : int
            The time it took to get the data.

        """

        data, rt = self.request_data("tGetOxyDataScaleFactor")
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data)[0], rt

    def get_data_oxy(self, channel, frame):
        """Get oxy data.

        Parameters:
        ----------
        channel : int
            The channel.
        frame : int
            The time point.

        Returns:
        --------
        data : float
            The raw data.
        rt : int
            The time it took to get the data.

        """

        channel = struct.pack('!i', channel)
        frame = struct.pack('!i', frame)
        data, rt = self.request_data("tGetDataOxy", channel, frame)
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data[8:])[0], rt

    def get_data_deoxy(self, channel, frame):
        """Get deoxy data.

        Parameters:
        ----------
        channel : int
            The channel.
        frame : int
            The time point.

        Returns:
        --------
        data : float
            The raw data.
        rt : int
            The time it took to get the data.

        """

        channel = struct.pack('!i', channel)
        frame = struct.pack('!i', frame)
        data, rt = self.request_data("tGetDataDeoxy", channel, frame)
        if data is None:
            return None, rt
        elif data[:14] == "Wrong request!":
            raise Exception("Wrong request!: '{0}'".format(data[19:-1]))
        else:
            return struct.unpack('!f', data[8:])[0], rt