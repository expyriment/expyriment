"""
File input and output.

This module contains classes implementing file input and output.

"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import atexit
import os
try:
    import locale
except ImportError:
    locale = None  # Does not exist on Android
import codecs
import re
import sys
import uuid
import time
from time import strftime
from platform import uname
from itertools import combinations

from . import defaults
from .. import _internals
from .. import misc
from ..misc._timer import get_time
from ..misc import unicode2byte, byte2unicode, get_experiment_secure_hash, module_hashes_as_string
from ..misc import statistics
from ._input_output import Input, Output


class InputFile(Input):
    """A class implementing an input file."""

    def __init__(self, filename, encoding=None):
        """Create an input file.

        All lines in the specified text file will be read into a list of
        strings.

        Parameters
        ----------
        filename : str, optional
            name of the input file

        encoding : str, optional
            the encoding used to read the content of the file

        """

        self._filename = filename
        self._current_line = 1
        self._lines = []
        if not(os.path.isfile(self._filename)):
            raise OSError("The input file '{0}' does not exist.".format(
                self._filename))

        if encoding is None:
            with open(filename, 'r') as fl:
                first_line = fl.readline()
                encoding = re.findall(r"coding[:=]\s*([-\w.]+)", first_line)
                if encoding == []:
                    second_line = fl.readline()
                    encoding = re.findall(r"coding[:=]\s*([-\w.]+)",
                                          second_line)
                    if encoding == []:
                        encoding = [None]
        else:
            encoding = [encoding]
        with codecs.open(self._filename, 'rb', encoding[0],
                         errors='replace') as f:
            for line in f:
                self._lines.append(byte2unicode(line).rstrip('\r\n'))

    @property
    def filename(self):
        """Getter for filename."""

        return self._filename

    @property
    def current_line(self):
        """Getter for current_line."""

        return self._current_line

    @property
    def n_lines(self):
        """Getter for n_lines."""

        return len(self._lines)

    @property
    def lines(self):
        """Getter for lines."""

        return self._lines

    def get_line(self, line=None):
        """Get a specific line.

        If no line is given, the current line will be returned and the value
        of current_line will be increased by one. First line is line 1.

        Parameters
        ----------
        line : int, optional
            number of the line to get

        Returns
        -------
        line : str
            line as string or None if line does not exist

        """

        if line is not None and (line < 1 or line > len(self._lines)):
            return None

        if line is not None:
            return self._lines[line - 1]
        else:
            current_line = self._current_line
            if current_line != len(self._lines):
                self._current_line += 1
            return self._lines[current_line - 1]


class OutputFile(Output):
    """A class implementing an output file."""

    def __init__(self, suffix, directory, comment_char=None,
                 time_stamp=None):
        """Create an output file.

        Filename: {MAINFILE_NAME}_{SUBJECT_ID}_{TIME_STAMP}{suffix}

        Parameters
        ----------
        suffix : str
            file suffix/extension (str)
        directory : str
            create file in given directory
        comment_char : str, optional
            comment character
        time_stamp : bool, optional
            using time stamps, based on the experiment start time,
            not the current time

        """

        Output.__init__(self)
        self._suffix = suffix
        self._directory = directory
        if comment_char is not None:
            self._comment_char = comment_char
        else:
            self._comment_char = defaults.outputfile_comment_char
        if time_stamp is not None:
            self._time_stamp = time_stamp
        else:
            self._time_stamp = defaults.outputfile_time_stamp
        self._buffer = []
        if not os.path.isdir(directory):
            os.mkdir(directory)
        self._filename = self.standard_file_name
        self._fullpath = directory + "{0}{1}".format(os.path.sep, self._filename)

        atexit.register(self.save)

        # Create new file
        fl = open(self._fullpath, 'w+')
        fl.close()
        try:
            locale_enc = locale.getdefaultlocale()[1]
        except Exception:
            locale_enc = "UTF-8"
        self.write_comment("Expyriment {0}, {1}-file, coding: {2}".format(
            _internals.get_version(), self._suffix,
            locale_enc))
        if _internals.active_exp.is_initialized:
            self.write_comment("date: {0}".format(time.strftime(
                               "%a %b %d %Y %H:%M:%S",
                               _internals.active_exp.clock.init_localtime)))

    @property
    def fullpath(self):
        """Getter for fullpath"""
        return self._fullpath

    @property
    def filename(self):
        """Getter for filename"""
        return self._filename

    @property
    def directory(self):
        """Getter for directory"""
        return self._directory

    @property
    def suffix(self):
        """Getter for directory"""
        return self._suffix

    @property
    def comment_char(self):
        """Getter for comment_char"""
        return self._comment_char

    @property
    def standard_file_name(self):
        """Getter for the standard expyriment outputfile name.

        Filename: {MAINFILE_NAME}_{SUBJECT_ID}_{TIME_STAMP}{suffix}

        """

        rtn = os.path.split(sys.argv[0])[1].replace(".py", "")
        if _internals.active_exp.is_started:
            rtn = rtn + '_' + repr(_internals.active_exp.subject).zfill(3)
        if self._time_stamp:
            rtn = rtn + '_' + strftime(
                "%Y%m%d%H%M", _internals.active_exp.clock.init_localtime)
        return rtn + self.suffix

    def save(self):
        """Save file to disk."""

        start = get_time()
        if self._buffer != []:
            buffer = [unicode2byte(x) for x in self._buffer]
            with open(self._fullpath, 'ab') as f:
                f.write(b"".join(buffer))
            self._buffer = []
        return int((get_time() - start) * 1000)

    def write(self, content):
        """Write to file.

        Parameters
        ----------
        content : str
            content to be written (anything, will be casted to str)

        """

        # NOTE: Do not print here recursion due to std_out logging

        if not isinstance(content, (str, bytes)):
            content = str(content)
        self._buffer.append(content)


    def write_line(self, content):
        """Write a text line to files.

        Parameters
        ----------
        content : str
            content to be written (anything, will be casted to str)

        """
        self.write(content)
        self.write(defaults.outputfile_eol)

    def write_list(self, list_):
        """Write a list in a row. Data are separated by a delimiter.

        Parameters
        ----------
        list_ : list
            list to be written

        """

        for elem in list:
            self.write(elem)
            self.write(',')
        self.write(defaults.outputfile_eol)
        # self.write_line(repr(list_)[1:-1].replace(" ", ""))

    def write_comment(self, comment):
        """Write a comment line to files.

        (i.e., text is proceeded by comment char).

        Parameters
        ----------
        comment : str
            comment to be written (anything, will be casted to str)

        """

        self.write(self.comment_char)
        self.write_line(comment)

    def rename(self, new_filename):
        """Renames the output file."""
        self.save()
        new_fullpath = self.directory + "{0}{1}".format(os.path.sep, new_filename)
        if os.path.isfile(new_fullpath):
            cnt = 1
            while True:
                old = new_fullpath[:-4] + f"_bak{cnt}" + new_fullpath[-4:]
                cnt += 1
                if not os.path.isfile(old):
                    os.rename(new_fullpath, old)
                    break
        os.rename(self._fullpath, new_fullpath)
        self._filename = new_filename
        self._fullpath = new_fullpath

    @staticmethod
    def get_next_subject_number():
        """Return the next subject number based on the existing data and event files."""

        subject_number = 1
        file_list = []
        if os.path.isdir(defaults.datafile_directory):
            file_list.extend(os.listdir(defaults.datafile_directory))
        if os.path.isdir(defaults.eventfile_directory):
            file_list.extend(os.listdir(defaults.eventfile_directory))

        if len(file_list)>0:
            mainfile_name = os.path.split(sys.argv[0])[1].replace(".py", "")
            for filename in file_list:
                if filename.startswith(mainfile_name) and \
                        filename.endswith((DataFile._file_suffix, EventFile._file_suffix)):
                    tmp = filename.replace(mainfile_name, "")\
                                  .replace(DataFile._file_suffix, "")\
                                  .replace(EventFile._file_suffix, "")
                    tmp = tmp.split('_')
                    try:
                        num = int(tmp[1])
                        if num >= subject_number and num<200000000000:
                            # large numbers are probably timestamps (normally the current event has no subject id
                            # yet and only a timestamp)
                            subject_number = num + 1
                    except Exception:
                        pass
        return subject_number


class DataFile(OutputFile):
    """A class implementing a data file."""

    _file_suffix = ".xpd"

    def __init__(self, additional_suffix, directory=None, delimiter=None,
                 time_stamp=None):
        """Create a data file.

        Filename: {MAINFILE_NAME}_{SUBJECT_ID}_{TIME_STAMP}{ADD_SUFFIX}.xpd

        Parameters
        ----------
        additional_suffix : str
            additional suffix
        directory : str, optional
            directory of the file
        delimiter : str, optional
            symbol between variables
        time_stamp : bool, optional
            using time stamps, based on the experiment start time,
            not the current time

        """

        if _internals.active_exp.is_initialized:
            self._subject = _internals.active_exp.subject
        else:
            self._subject = None
        if directory is None:
            directory = defaults.datafile_directory
        if additional_suffix is None:
            additional_suffix = ''
        if len(additional_suffix) > 0:
            suffix = ".{0}{1}".format(additional_suffix, self._file_suffix)
        else:
            suffix = self._file_suffix
        OutputFile.__init__(self, suffix, directory, time_stamp=time_stamp)
        if delimiter is not None:
            self._delimiter = delimiter
        else:
            self._delimiter = defaults.datafile_delimiter

        self._subject_info = []
        self._experiment_info = []
        self._variable_names = []

        self.write_comment("--EXPERIMENT INFO")
        self.write_comment("e mainfile: {0}".format(os.path.split(
                                                    sys.argv[0])[1]))

        self.write_comment("e sha1: {0}".format(
                                    get_experiment_secure_hash()))
        self.write_comment("e modules: {0}".format(
                            module_hashes_as_string()))
        self.write_comment("--SUBJECT INFO")
        self.write_comment("s id: {0}".format(self._subject))
        self.write_comment("#")
        self._variable_names_changed = True
        self.save()

    @property
    def delimiter(self):
        """Getter for delimiter"""
        return self._delimiter

    def add(self, data):
        """Add data.

        Parameters
        ----------
        data : string or numeric or list
            data to be added

        """

        self.write(str(self._subject) + self.delimiter)
        if isinstance(data, (list, tuple)):
            line = ""
            for counter, elem in enumerate(data):
                if counter > 0:
                    line = line + self.delimiter
                if not isinstance(elem, (str, bytes)):
                    elem = str(elem)
                if '"' in byte2unicode(elem):
                    elem = byte2unicode(elem).replace('"', '""')
                if ',' in byte2unicode(elem):
                    elem = '"{0}"'.format(byte2unicode(elem))
                line = line + elem
            self.write_line(line)
        else:
            if not isinstance(data, (str, bytes)):
                data = str(data)
            self.write_line(data)

    def add_subject_info(self, text):
        """Adds a text the subject info header.

        Subject information can be extracted afterwards using
        misc.data_preprocessing.read_data_file. To defined between subject
        variables use a syntax like this: "gender = female" or
        "handedness : left"

        Parameters
        ----------
        text : str
            subject information to be added to the file header

        Notes
        -----
        The next data.save() might take longer!


        """

        self._subject_info.append("{0}s {1}{2}".format(
            self.comment_char, text, defaults.outputfile_eol))

    def add_experiment_info(self, text):
        """Adds a text the subject info header.

        Parameters
        ----------
        text : str
            experiment information to be added to the file header

        Notes
        -----
        The next data.save() might take longer!

        """

        for line in text.splitlines():
            self._experiment_info.append("{0}e {1}{2}".format(
                self.comment_char, line, defaults.outputfile_eol))

    @property
    def variable_names(self):
        """Getter for variable_names."""

        vn = self.delimiter.join(self._variable_names)
        return "subject_id,{0}".format(vn)

    def clear_variable_names(self):
        """Remove all variable names from data file.

        Notes
        -----
        The next data.save() might take longer!

        """

        self._variable_names = []
        self._variable_names_changed = True

    def add_variable_names(self, variable_names):
        """Add data variable names to the data file.

        Notes
        -----
        The next data.save() might take longer!

        Parameters
        ----------
        variables : str or list of str
            variable names

        """

        if variable_names is None:
            return
        try:
            variable_names = list(variable_names)
        except Exception:
            variable_names = [variable_names]
        self._variable_names.extend(variable_names)
        self._variable_names_changed = True

    def save(self):
        """Save the new data to data-file.

        Returns
        -------
        time : int
            the time it took to execute this method

        """


        start = get_time()
        if len(self._subject_info) > 0 or len(self._experiment_info) > 0  \
                or self._variable_names_changed:
            # Re-write header and varnames
            tmpfile_name = "{0}{1}{2}".format(self.directory, os.path.sep, uuid.uuid4())
            os.rename(self._fullpath, tmpfile_name)
            fl = open(self._fullpath, 'wb+')
            tmpfl = open(tmpfile_name, 'r')
            section = None
            while True:
                line = tmpfl.readline()
                if not line:
                    break
                if line.startswith(self.comment_char + "e"):
                    section = "e"
                elif line.startswith(self.comment_char + "s"):
                    section = "s"
                else:
                    if section == "e":  # Previous line was last #e
                        if len(self._experiment_info) > 0:
                            fl.write(unicode2byte("".join(self._experiment_info)))
                            self._experiment_info = []
                        section = None
                    elif section == "s":  # Previous line was last #s
                        if len(self._subject_info) > 0:
                            fl.write(unicode2byte("".join(self._subject_info)))
                            self._subject_info = []
                        section = None

                        # Re-write variable names after #s-section
                        fl.write(unicode2byte(
                            self.variable_names + defaults.outputfile_eol))
                        self._variable_names_changed = False
                        line = ''  # Skip old varnames
                fl.write(unicode2byte(line))
            tmpfl.close()
            fl.close()

            os.remove(tmpfile_name)
            self._subject_info = []
            self._experiment_info = []

        if self._buffer != []:
            OutputFile.save(self)
            if self._logging:
                _internals.active_exp._event_file_log("Data,saved")

        return int((get_time() - start) * 1000)


class EventFile(OutputFile):
    """A class implementing an event file."""

    _file_suffix = ".xpe"

    def __init__(self, additional_suffix, directory=None, delimiter=None,
                 clock=None, time_stamp=None):
        """Create an event file.

        Filename: {MAINFILE_NAME}_{SUBJECT_ID}_{TIME_STAMP}{ADD_SUFFIX}.xpd

        Parameters
        ----------
        additional_suffix : str
            additional suffix
        directory : str, optional
            directory of the file
        delimiter : str, optional
            symbol between timestamp and event
        clock : expyriment.Clock, optional
            an experimental clock
        time_stamp : bool, optional
            using time stamps, based on the experiment start time,
            not the current time

        """

        if directory is None:
            directory = defaults.eventfile_directory
        if additional_suffix is None:
            additional_suffix = ''
        if len(additional_suffix) > 0:
            suffix = ".{0}{1}".format(additional_suffix, self._file_suffix)
        else:
            suffix = self._file_suffix
        OutputFile.__init__(self, suffix, directory, time_stamp=time_stamp)
        if delimiter is not None:
            self._delimiter = delimiter
        else:
            self._delimiter = defaults.eventfile_delimiter
        if clock is not None:
            self._clock = clock
        else:
            if not _internals.active_exp.is_initialized:
                raise RuntimeError(
                    "Cannot find a clock. Initialize Expyriment!")
            self._clock = _internals.active_exp.clock

        try:
            display = repr(_internals.active_exp.screen.window_size)
            window_mode = repr(_internals.active_exp.screen.window_mode)
            opengl = repr(_internals.active_exp.screen.opengl)
        except Exception:
            display = "unknown"
            window_mode = "unknown"
            opengl = "unknown"

        self.write_comment("sha1: {0}".format(
                                    get_experiment_secure_hash()))
        self.write_comment("modules: {0}".format(
                            module_hashes_as_string()))
        self.write_comment("display: size={0}, window_mode={1}, opengl={2}".format(
            display, window_mode, opengl))
        self.write_comment("os: {0}".format(uname()))

        self.write_line("Time,Type,Event,Value,Detail,Detail2")
        self.save()

        self._inter_event_intervall_log = _InterEventIntervallLog()
        atexit.register(self._write_inter_event_intervall_summary)

    @property
    def clock(self):
        """Getter for clock"""
        return self._clock

    @property
    def delimiter(self):
        """Getter for delimiter"""
        return self._delimiter

    def log(self, event, log_event_tag=None):
        """Log an event.

        Parameters
        ----------
        event : anything
            the event to be logged (anything, will be casted to str)
        log_event_tag : numeral or string, optional
            if log_event_tag is defined, event file logs the inter-event-intervalls
            and adds a summary of the intervals at the end of the file

        Returns
        -------
        log_time : int
            the time of logging

        """

        log_time = self._clock.time
        if not isinstance(event, (str, bytes)):
            event = str(event)
        self.write_line(repr(log_time) + self.delimiter + event)
        if log_event_tag is not None:
            self._inter_event_intervall_log.add_event(log_event_tag, log_time)
        return log_time

    def warn(self, message):
        """Log a warning message.

        Parameters
        ----------
        message : str
            warning message to log

        """

        line = "WARNING: " + message
        self.write_line(line)

    def _write_inter_event_intervall_summary(self):
        """appending the inter event interval summary to event file, if log_event_tag have been set while presentation
        this function will be called at exit"""

        for l in self._inter_event_intervall_log.summary():
            self.write_comment(l)



class _InterEventIntervallLog:
    """This class is used to log the intervals of tagged events to get a
    summary of the timing at the end of the event file
    """

    def __init__(self):
        self.clear()


    def clear(self):
        """clear logging queue"""
        self.log_dict = {}


    def add_event(self, event_tag, time):
        """add event for logging"""

        try:
            self.log_dict[event_tag].append(time)
        except Exception:
            self.log_dict[event_tag] = [time]


    def _get_iei_intervalls(self, from_tag, to_tag):
        """helper function: get the intervals between two events"""

        rtn = []
        try:
            time_from = sorted(self.log_dict[from_tag])
            time_to = sorted(self.log_dict[to_tag])
        except Exception:
            return rtn

        for f in time_from:
            # find first larger to time and add different to list
            for t in time_to:
                if t>=f:
                    rtn.append(t-f)
                    break
        return rtn


    def summary(self):
        """The summary as string array

        Returns
        -------
        txt : string array

        """

        rtn = []
        for a, b in combinations(self.log_dict.keys(), 2):
            for reverse in [False, True]:
                if reverse:
                    tmp = b
                    b = a
                    a = tmp
                iei = self._get_iei_intervalls(a, b)
                txt = "{0} --> {1}: n={2}".format(a,b, len(iei))
                if len(iei)>0:
                    txt += ", mean={0}, median={1}, std={2}".format(
                                misc.round(statistics.mean(iei),2),
                                misc.round(statistics.median(iei),2),
                                misc.round(statistics.std(iei),2),
                                )
                rtn.append(txt)
        return rtn
