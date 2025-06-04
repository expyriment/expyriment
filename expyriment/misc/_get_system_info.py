"""
info["hardware_displays"] =
Get System Information.
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'

import sys
import os
import glob
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
    _com_port_list = _list_com_ports()
except ImportError:
    _serial = None
    _com_port_list = []
try:
    import parallel as _parallel
except ImportError:
    _parallel = None
except OSError:
    _parallel = None
try:
    import numpy as _numpy
except Exception:
    _numpy = None
try:
    import mediadecoder as _mediadecoder
except Exception:
    _mediadecoder = None
try:
    import sounddevice as _sounddevice
except Exception:
    _sounddevice = None
try:
    import PIL.Image as _pil
except Exception:
    _pil = None
import pygame

from .._internals import get_version


def _get_registry_subkeys(key, subkey):
    try:
        import winreg as _winreg
    except Exception:
        return ""

    key_id = getattr(_winreg, key)
    handle = _winreg.OpenKey(key_id, subkey)
    subkeys = []
    i = 0
    while True:
        try:
            subkeys.append(str(_winreg.EnumKey(handle, i)))
            i += 1
        except OSError:
            break
    return subkeys


def _get_registry_value(key, subkey, value):
    try:
        import winreg as _winreg
    except Exception:
        return ""

    key = getattr(_winreg, key)
    handle = _winreg.OpenKey(key, subkey)
    (value, type) = _winreg.QueryValueEx(handle, value)
    return str(value)


def get_system_info(as_string=False):
    """Print system information to standard out and return as a dictionary.

    Parameters
    ----------
    as_string : boolean, optional
        Print as string instead of dict (default = False)

    """

    from ..io import SerialPort, ParallelPort
    from .._internals import get_settings_folder
    from ._miscellaneous import get_display_info
    try:
        from platform import linux_distribution
    except Exception:
        try:
            from distro import linux_distribution #TODO: only available for Linux, should it be a suggested package dependency?
        except Exception:
            def linux_distribution():
                name = ""
                version = ""
                name_found = False
                version_found = False
                files = [x for x in ("/etc/os-release", "/etc/lsb-release") \
                         if os.path.isfile(x)]
                for release_file in files:
                    with open(release_file) as f:
                        for line in f:
                            if not name_found and \
                                    line.startswith(("NAME=", "DISTRIB_ID=")):
                                name = line.split("=")[-1].strip().strip('"')
                                name_found = True
                            if not version_found and \
                                    line.startswith(("VERSION_ID=", "DISTRIB_RELEASE=")):
                                version = line.split("=")[-1].strip().strip('"')
                                version_found = True
                return (name, version)

    info = {}

    # Get platform specific info for Linux
    if sys.platform.startswith("linux"):
        os_platform = "Linux"
        os_name = linux_distribution()[0]
        os_version = linux_distribution()[1]

        details = []
        if "XDG_CURRENT_DESKTOP" in os.environ:
            details.append(os.environ["XDG_CURRENT_DESKTOP"])
        elif "DESKTOP_SESSION" in os.environ:
            details.append(os.environ["DESKTOP_SESSION"])
        else:
            pass
        if "WAYLAND_DISPLAY" in os.environ:
            details.append(os.environ["WAYLAND_DISPLAY"])
        if "DISPLAY" in os.environ:
            details.append(os.environ["DISPLAY"])

        if details != []:
            os_details = ", ".join(details)
        else:
            os_details = ""

        try:
            hardware_cpu_details = ""
            with open('/proc/cpuinfo') as f:
                for line in f:
                    if line.startswith("model name"):
                        hardware_cpu_details = line.split(":")[1].strip()
        except Exception:
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

        except Exception:
            hardware_memory_total = ""
            hardware_memory_free = ""

        try:
            hardware_audio_card = ""
            p = subprocess.Popen(['lspci'], stdout=subprocess.PIPE, text=True)
            cards = [
                line.split(":")[-1].strip()
                for line in p.stdout
                if "Audio" in line
            ]
            p.wait()
            if cards:
                hardware_audio_card = cards
        except Exception:
            try:
                hardware_audio_card = ""
                with open('/proc/asound/cards') as f:
                    cards = [
                        line.split(":")[1].strip()
                        for line in f
                        if line.startswith(" 0")
                    ]
                if cards:
                    hardware_audio_card = cards
            except Exception:
                hardware_audio_card = ""

        try:
            current_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]
            s = os.statvfs(current_folder)
            disk_total = int((s.f_frsize * s.f_blocks) // 1024 ** 2)
            disk_free = int((s.f_frsize * s.f_bavail) // 1024 ** 2)
            hardware_disk_space_total = str(disk_total) + " MB"
            hardware_disk_space_free = str(disk_free) + " MB"
        except Exception:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        try:
            hardware_video_card = ""
            cards = []
            p = subprocess.Popen(['lspci'], stdout=subprocess.PIPE, text=True)
            for line in p.stdout:
                if "VGA" in line:
                    cards.append(line.split(":")[-1].strip())
            p.wait()
            if cards != []:
                hardware_video_card = cards
        except Exception:
            hardware_video_card = ""

    # Get platform specific info for Windows
    elif sys.platform.startswith("win"):
        os_platform = "Windows"
        os_name = "Windows"
        os_details = platform.win32_ver()[2]
        os_version = platform.win32_ver()[1]

        hardware_cpu_details = _get_registry_value(
            "HKEY_LOCAL_MACHINE",
            "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
            "ProcessorNameString")

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
                    return super().__init__()

            stat = MEMORYSTATUSEX()
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
            hardware_memory_total = str(stat.ullTotalPhys // 1024 ** 2) + " MB"
            hardware_memory_free = str(stat.ullAvailPhys // 1024 ** 2) + " MB"
        except Exception:
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
        except Exception:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        video_cards = []
        subkeys = _get_registry_subkeys(
            "HKEY_LOCAL_MACHINE",
            "SYSTEM\\CurrentControlSet\\Control\\Video")
        for x in subkeys:
            try:
                found = _get_registry_value(
                    "HKEY_LOCAL_MACHINE",
                    f"SYSTEM\\CurrentControlSet\\Control\\Video\\{x}\\Video",
                    "DeviceDesc")
                video_cards.append(found.split(";")[-1])
            except Exception:
                pass

        if video_cards != []:
            hardware_video_card = video_cards
        else:
            hardware_video_card = ""

        audio_cards = []
        capture_subkeys = dict.fromkeys(_get_registry_subkeys(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\Capture"),
                                        "Capture")
        render_subkeys = dict.fromkeys(_get_registry_subkeys(
            "HKEY_LOCAL_MACHINE",
            "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\Render"),
                                       "Render")

        for x,y in {**capture_subkeys, **render_subkeys}.items():
            try:
                active = _get_registry_value(
                    "HKEY_LOCAL_MACHINE",
                    f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\{y}\\{x}",
                    "DeviceState")
                if active != "1":
                    continue
                found_description = _get_registry_value(
                    "HKEY_LOCAL_MACHINE",
                    f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\{y}\\{x}\\Properties",
                    "{a45c254e-df1c-4efd-8020-67d146a850e0},2")
                found_name = _get_registry_value(
                    "HKEY_LOCAL_MACHINE",
                    f"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\MMDevices\\Audio\\{y}\\{x}\\Properties",
                    "{b3f8fa53-0004-438e-9003-51a46e139bfc},6")

                audio_cards.append(f"{found_description} ({found_name})")
            except Exception:
                pass

        if audio_cards != []:
            hardware_audio_card = audio_cards
        else:
            hardware_audio_card = ""


    # Get platform specific info for MacOS
    elif sys.platform.startswith("darwin"):
        os_platform = "Darwin"
        os_name = "MacOS"
        os_details = platform.mac_ver()[1][1]
        os_version = platform.mac_ver()[0]
        try:
            proc = subprocess.Popen(['sysctl', '-a', 'hw.model'],
                                    text=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            hardware_cpu_details = \
                    proc.stdout.readline().split(":")[1].strip()
        except Exception:
            hardware_cpu_details = ""
        try:
            proc = subprocess.Popen(['sysctl', '-a', 'hw.memsize'],
                                    text=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            mem_total = int(proc.stdout.readline().split(":")[1].strip()) // 1024 ** 2
            hardware_memory_total = str(mem_total) + " MB"
        except Exception:
            hardware_memory_total = ""

        try:
            import re
            proc = subprocess.Popen(['vm_stat'],
                                    text=True,
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            output = proc.stdout.read().split("\n")
            for item in output:
                a = item.find("page size of")
                b = item.find("Anonymous pages:")
                c = item.find("Pages purgeable:")
                d = item.find("Pages wired down:")
                e = item.find("Pages occupied by compressor:")
                if a > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    page = int(non_decimal.sub('', item).strip("."))
                if b > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    anonymous = int(non_decimal.sub('', item).strip("."))
                if c > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    purgeable = int(non_decimal.sub('', item).strip("."))
                if d > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    wired = int(non_decimal.sub('', item).strip("."))
                if e > -1:
                    non_decimal = re.compile(r'[^\d.]+')
                    compressed = int(non_decimal.sub('', item).strip("."))

            hardware_memory_free = str(mem_total - (((anonymous - purgeable) + wired + compressed) * page) // 1024 ** 2) + " MB"

        except Exception:
            hardware_memory_free = ""

        try:
            current_folder = os.path.split(os.path.realpath(sys.argv[0]))[0]
            s = os.statvfs(current_folder)
            disk_total = int((s.f_frsize * s.f_blocks) // 1024 ** 2)
            disk_free = int((s.f_frsize * s.f_bavail) // 1024 ** 2)
            hardware_disk_space_total = str(disk_total) + " MB"
            hardware_disk_space_free = str(disk_free) + " MB"
        except Exception:
            hardware_disk_space_total = ""
            hardware_disk_space_free = ""

        try:
            import plistlib
            proc = subprocess.Popen(['system_profiler', 'SPAudioDataType',
                                     '-xml'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            pl = plistlib.loads(proc.stdout.read())
            hardware_audio_card = []
            for x in pl[0]['_items']:
                for card in x['_items']:
                    hardware_audio_card.append(card['_name'])

        except Exception:
            hardware_audio_card = ""

        try:
            import plistlib
            proc = subprocess.Popen(['system_profiler', 'SPDisplaysDataType',
                                     '-xml'],
                                    stdout=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            pl = plistlib.loads(proc.stdout.read())
            hardware_video_card = []
            for card in pl[0]['_items']:
                hardware_video_card.append(card['sppci_model'])
        except Exception:
            hardware_video_card = ""

    # Fill in info
    info["os_architecture"] = platform.architecture()[0]
    info["os_name"] = os_name
    info["os_details"] = os_details
    info["os_platform"] = os_platform
    info["os_release"] = platform.release()
    info["os_version"] = os_version
    info["settings_folder"] = get_settings_folder()
    info["python_expyriment_version"] = get_version().split(" ")[0]
    if _numpy is not None:
        numpy_version = _numpy.version.version
    else:
        numpy_version = ""
    info["python_numpy_version"] = numpy_version
    if _mediadecoder is not None:
        mediadecoder_version = _mediadecoder.__version__
    else:
        mediadecoder_version = ""
    info["python_mediadecoder_version"] = mediadecoder_version
    if _sounddevice is not None:
        sounddevice_version = _sounddevice.__version__
    else:
        sounddevice_version = ""
    info["python_sounddevice_version"] = sounddevice_version
    if _pil is not None:
        pil_version = _pil.__version__
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
    display_info = get_display_info()
    info["hardware_displays"] = get_display_info()
    try:
        socket.gethostbyname("google.com")
        hardware_internet_connection = "Yes"
    except Exception:
        hardware_internet_connection = "No"
    info["hardware_internet_connection"] = hardware_internet_connection
    info["hardware_memory_total"] = hardware_memory_total
    info["hardware_memory_free"] = hardware_memory_free
    info["hardware_ports_parallel"] = \
            ParallelPort.get_available_ports()
    info["hardware_ports_parallel_driver"] = ParallelPort.get_driver()
    try:
        info["hardware_ports_serial"] = [x.device for x in _com_port_list]
    except Exception:
        info["hardware_ports_serial"] = _com_port_list
    info["hardware_video_card"] = hardware_video_card

    # sort output
    info = dict(sorted(info.items()))

    if as_string:
        longest = 0
        for key in info.keys():
            longest = max(len(key), longest)

        rtn = ""
        for key in info:
            tabs = " " * (longest - len(key)) + "\t"
            rtn += key + ":" + tabs + repr(info[key]) + "\n"

    else:
        rtn = info

    return rtn
