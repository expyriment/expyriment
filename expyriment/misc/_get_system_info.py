"""
Get System Information.
"""
from __future__ import absolute_import, print_function, division
from future import standard_library
standard_library.install_aliases()
from builtins import *


__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys
import os
import platform
import subprocess
import socket
try:
    import OpenGL as _ogl
except ImportError:
    _ogl = None
try:
    import serial as _serial
    from serial.tools.list_ports import comports as _list_com_ports
except ImportError:
    _serial = None
try:
    import parallel as _parallel
except ImportError:
    _parallel = None
try:
    import numpy as _numpy
except:
    _numpy = None
try:
    import PIL.Image as _pil
except:
    _pil = None
import pygame

from .._internals import PYTHON3

def _get_registry_value(key, subkey, value):
    if PYTHON3:
        import winreg as _winreg  # TODO check me on Windows
    else:
        import _winreg
    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return value


def get_system_info(as_string=False):
    """Print system information to standard out and return as a dictionary.

    Parameters
    ----------
    as_string : boolean, optional
        Print as string instead of dict (default = False)

    """

    from ..io import SerialPort, ParallelPort
    from .._internals import get_settings_folder

    info = {}

    # Get platform specific info for Linux
    if sys.platform.startswith("linux"):
        os_platform = "Linux"
        os_name = platform.linux_distribution()[0]
        details = []
        if "XDG_CURRENT_DESKTOP" in os.environ:
            details.append(os.environ["XDG_CURRENT_DESKTOP"])
        if "DESKTOP_SESSION" in os.environ:
            details.append(os.environ["DESKTOP_SESSION"])
        if details != []:
            os_details = ", ".join(details)
        else:
            os_details = ""
        os_version = platform.linux_distribution()[1]

        try:
            hardware_cpu_details = ""
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.startswith("model name"):
                        hardware_cpu_details = line.split(":")[1].strip()
        except:
            hardware_cpu_details = ""

        try:
            with open('/proc/meminfo') as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        mem_total = \
                            int(line.split(":")[1].strip()[:-2].strip()) // 1024
                    if line.startswith("MemFree"):
                        mem_free = \
                            int(line.split(":")[1].strip()[:-2].strip()) // 1024
                    if line.startswith("Buffers"):
                        mem_buffers = \
                            int(line.split(":")[1].strip()[:-2].strip()) // 1024
                    if line.startswith("Cached"):
                        mem_cached = \
                            int(line.split(":")[1].strip()[:-2].strip()) // 1024
            hardware_memory_total = str(mem_total) + " MB"
            hardware_memory_free = str(mem_free + mem_buffers + mem_cached) + \
                                   " MB"

        except:
            hardware_memory_total = ""
            hardware_memory_free = ""

        try:
            hardware_audio_card = ""
            cards = []
            p = subprocess.Popen(['lspci'], stdout=subprocess.PIPE)
            for line in p.stdout:
                if "Audio" in line:
                    cards.append(line.split(":")[-1].strip())
            p.wait()
            hardware_audio_card = ", ".join(cards)
        except:
            try:
                hardware_audio_card = ""
                cards = []
                with open('/proc/asound/cards') as f:
                    for line in f:
                        if line.startswith(" 0"):
                            cards.append(line.split(":")[1].strip())
                hardware_audio_card = ", ".join(cards)
            except:
                hardware_audio_card = ""

        try:
            current_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]
            s = os.statvfs(current_folder)
            disk_total = int((s.f_frsize * s.f_blocks) // 1024 ** 2)
            disk_free = int((s.f_frsize * s.f_bavail) // 1024 ** 2)
            hardware_disk_space_total = str(disk_total) + " MB"
            hardware_disk_space_free = str(disk_free) + " MB"
        except:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        try:
            hardware_video_card = ""
            cards = []
            p = subprocess.Popen(['lspci'], stdout=subprocess.PIPE)
            for line in p.stdout:
                if "VGA" in line:
                    cards.append(line.split(":")[-1].strip())
            p.wait()
            hardware_video_card = ", ".join(cards)
        except:
            hardware_video_card = ""

    # Get platform specific info for Windows
    elif sys.platform.startswith("win"):
        os_platform = "Windows"
        os_name = "Windows"
        os_details = platform.win32_ver()[2]
        os_version = platform.win32_ver()[1]

        try:
            hardware_cpu_details = str(_get_registry_value(
                "HKEY_LOCAL_MACHINE",
                "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
                "ProcessorNameString"))
        except:
            hardware_cpu_details = ""

        try:
            import ctypes
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_uint),
                            ("dwMemoryLoad", ctypes.c_uint),
                            ("ullTotalPhys", ctypes.c_ulonglong),
                            ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong),
                            ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong),
                            ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong), ]

                def __init__(self):
                    # Initialize this to the size of MEMORYSTATUSEX
                    self.dwLength = 2 * 4 + 7 * 8  # size = 2 ints, 7 longs
                    return super(MEMORYSTATUSEX, self).__init__()

            stat = MEMORYSTATUSEX()
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            hardware_memory_total = str(stat.ullTotalPhys // 1024 ** 2) + " MB"
            hardware_memory_free = str(stat.ullAvailPhys // 1024 ** 2) + " MB"
        except:
            hardware_memory_total = ""
            hardware_memory_free = ""

        try:
            current_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]
            _, disk_total, disk_free = ctypes.c_int64(), ctypes.c_int64(), \
                                       ctypes.c_int64()
            ret = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                str(current_folder), ctypes.byref(_),
                ctypes.byref(disk_total), ctypes.byref(disk_free))
            hardware_disk_space_total = str(disk_total.value // 1024 ** 2) + " MB"
            hardware_disk_space_free = str(disk_free.value // 1024 ** 2) + " MB"
        except:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        try:
            tmp = str(_get_registry_value("HKEY_LOCAL_MACHINE",
                                          "HARDWARE\\DEVICEMAP\\VIDEO",
                                          "\Device\Video0"))
            idx = tmp.find("System")
            card = str(_get_registry_value("HKEY_LOCAL_MACHINE",
                                           tmp[idx:].replace("\\", "\\\\"),
                                           "Device Description"))
            hardware_video_card = card
        except:
            hardware_video_card = ""

        hardware_audio_card = ""  # TODO

    # Get platform specific info for OS X
    elif sys.platform.startswith("darwin"):
        os_platform = "Darwin"
        os_name = "Mac OS X"
        os_details = platform.mac_ver()[1][1]
        os_version = platform.mac_ver()[0]
        try:
            proc = subprocess.Popen(['sysctl', '-a', 'hw.model'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            hardware_cpu_details = \
                    proc.stdout.readline().split(":")[1].strip()
        except:
            hardware_cpu_details = ""
        try:
            proc = subprocess.Popen(['sysctl', '-a', 'hw.memsize'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            mem_total = int(proc.stdout.readline().split(":")[1].strip()) // 1024 ** 2
            hardware_memory_total = str(mem_total) + " MB"
        except:
            hardware_memory_total = ""

        try:
            import re
            proc = subprocess.Popen(['vm_stat'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            output = proc.stdout.read().split("\n")
            for item in output:
                x = item.find("Pages active:")
                y = item.find("page size of")
                if x > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    active = int(non_decimal.sub('', item).strip("."))
                if y > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    page = int(non_decimal.sub('', item).strip("."))
            hardware_memory_free = str(mem_total - (active * page) // 1024 ** 2) + " MB"

        except:
            hardware_memory_free = ""

        try:
            current_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]
            s = os.statvfs(current_folder)
            disk_total = int((s.f_frsize * s.f_blocks) // 1024 ** 2)
            disk_free = int((s.f_frsize * s.f_bavail) // 1024 ** 2)
            hardware_disk_space_total = str(disk_total) + " MB"
            hardware_disk_space_free = str(disk_free) + " MB"
        except:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        try:
            proc = subprocess.Popen(['system_profiler', 'SPAudioDataType'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            hardware_audio_card = \
                proc.stdout.read().split("\n")[2].strip(":").strip()
        except:
            hardware_audio_card = ""

        try:
            import plistlib
            proc = subprocess.Popen(['system_profiler', 'SPDisplaysDataType',
                                     '-xml'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            pl = plistlib.readPlist(proc.stdout)
            hardware_video_card = []
            for card in pl[0]['_items']:
                hardware_video_card.append(card['sppci_model'])
        except:
            hardware_video_card = ""

    # Fill in info
    info["os_architecture"] = platform.architecture()[0]
    info["os_name"] = os_name
    info["os_details"] = os_details
    info["os_platform"] = os_platform
    info["os_release"] = platform.release()
    info["os_version"] = os_version
    info["settings_folder"] = get_settings_folder()
    info["python_expyriment_build_date"] = __date__
    info["python_expyriment_revision"] = __revision__
    info["python_expyriment_version"] = __version__
    if _numpy is not None:
        numpy_version = _numpy.version.version
    else:
        numpy_version = ""
    info["python_numpy_version"] = numpy_version
    if _pil is not None:
        pil_version = _pil.VERSION
    else:
        pil_version = ""
    info["python_pil_version"] = pil_version
    info["python_pygame_version"] = pygame.version.ver
    if _ogl is not None:
        pyopengl_version = _ogl.version.__version__
    else:
        pyopengl_version = ""
    info["python_pyopengl_version"] = pyopengl_version
    if _parallel is not None:
        parallel_version = _parallel.VERSION
    else:
        parallel_version = ""
    info["python_pyparallel_version"] = parallel_version
    if _serial is not None:
        serial_version = _serial.VERSION
    else:
        serial_version = ""
    info["python_pyserial_version"] = serial_version
    info["python_version"] = "{0}.{1}.{2}".format(sys.version_info[0],
                                                  sys.version_info[1],
                                                  sys.version_info[2])

    info["hardware_audio_card"] = hardware_audio_card
    info["hardware_cpu_architecture"] = platform.machine()
    info["hardware_cpu_details"] = hardware_cpu_details
    info["hardware_cpu_type"] = platform.processor()
    info["hardware_disk_space_free"] = hardware_disk_space_free
    info["hardware_disk_space_total"] = hardware_disk_space_total
    try:
        socket.gethostbyname("expyriment.googlecode.com")
        hardware_internet_connection = "Yes"
    except:
        hardware_internet_connection = "No"
    info["hardware_internet_connection"] = hardware_internet_connection
    info["hardware_memory_total"] = hardware_memory_total
    info["hardware_memory_free"] = hardware_memory_free
    info["hardware_ports_parallel"] = \
            ParallelPort.get_available_ports()
    info["hardware_ports_serial"] = \
            _list_com_ports()
    info["hardware_video_card"] = hardware_video_card

    if as_string:
        sorted_keys = list(info.keys())
        sorted_keys.sort()
        rtn = ""
        for key in sorted_keys:
            tabs = "\t" * (4 - int((len(key) + 1) // 8))
            try:
                rtn += key + ":" + tabs + info[key] + "\n"
            except TypeError:
                rtn += key + ":" + tabs + repr(info[key]) + "\n"
    else:
        rtn = info

    return rtn
