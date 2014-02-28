"""A high-resolution monotonic timer

This module provides a high-resolution timer via the function get_time()

Thanks to Luca Filippin for the code examples.

Credits and references:
      http://stackoverflow.com/questions/1205722/how-do-i-get-monotonic-time-durations-in-python
      http://stackoverflow.com/questions/1824399/get-mach-absolute-time-uptime-in-nanoseconds-in-python
      https://mail.python.org/pipermail/python-dev/2009-October/093173.html
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

try:
    import ctypes
except:
    ctypes = None  # Does not exist on Android
import os
from sys import platform

_use_time_module = False

if platform == 'darwin':
    # MAC
    try:
        class _TimeBase(ctypes.Structure):
            _fields_ = [
                ('numer', ctypes.c_uint),
                ('denom', ctypes.c_uint)
            ]

        _libsys_c = ctypes.CDLL('/usr/lib/system/libsystem_c.dylib')
        _libsys_kernel = ctypes.CDLL('/usr/lib/system/libsystem_kernel.dylib')
        _mac_abs_time = _libsys_c.mach_absolute_time
        _mac_timebase_info = _libsys_kernel.mach_timebase_info
        _time_base = _TimeBase()
        if (_mac_timebase_info(ctypes.pointer(_time_base)) != 0):
            _use_time_module = True

        def get_time():
            """Get high-resolution monotonic time stamp (float) """
            _mac_abs_time.restype = ctypes.c_ulonglong
            return float(_mac_abs_time()) * _time_base.numer / (_time_base.denom * 1e9)
        get_time()
    except:
        _use_time_module = True

elif platform.startswith('linux'):
    # real OS
    _CLOCK_MONOTONIC = 4  # actually CLOCK_MONOTONIC_RAW see <linux/time.h>

    try:
        class _TimeSpec(ctypes.Structure):
            _fields_ = [
                ('tv_sec', ctypes.c_long),
                ('tv_nsec', ctypes.c_long)
            ]

        _librt = ctypes.CDLL('librt.so.1', use_errno=True)
        _clock_gettime = _librt.clock_gettime
        _clock_gettime.argtypes = [ctypes.c_int, ctypes.POINTER(_TimeSpec)]

        def get_time():
            """Get high-resolution monotonic time stamp (float) """
            t = _TimeSpec()
            if _clock_gettime(_CLOCK_MONOTONIC, ctypes.pointer(t)) != 0:
                errno_ = ctypes.get_errno()
                raise OSError(errno_, os.strerror(errno_))
            return t.tv_sec + t.tv_nsec * 1e-9
        get_time()
    except:
        _use_time_module = True

elif platform == 'win32':
    # win32. Code adapted from the psychopy.core.clock source code.
    try:
        _fcounter = ctypes.c_int64()
        _qpfreq = ctypes.c_int64()
        ctypes.windll.Kernel32.QueryPerformanceFrequency(ctypes.byref(_qpfreq))
        _qpfreq = float(_qpfreq.value)
        _winQPC = ctypes.windll.Kernel32.QueryPerformanceCounter

        def get_time():
            """Get high-resolution monotonic time stamp (float) """
            _winQPC(ctypes.byref(_fcounter))
            return  _fcounter.value/_qpfreq
        get_time()
    except:
        _use_time_module = True
else:
    # Android or something else
    _use_time_module = True


if _use_time_module:
    import time
    warn_message = "Failed to initialize monotonic timer. Python's time module will be use."
    print("Warning: " + warn_message)
    if platform == 'win32':
        def get_time():
            """Get high-resolution time stamp (float) """
            return time.clock()
    else:
        def get_time():
            """Get high-resolution time stamp (float) """
            return time.time()

if __name__ == "__main__":
    print get_time()
