"""Data Preprocessing Module.

This module contains several classes and functions that help
to handle, preprocessing and aggregate Expyriment data files.

"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import os as _os
try:
    import locale as _locale
except ImportError:
    _locale = None  # Does not exist on Android
import sys as _sys
from types import ModuleType
from tempfile import mkstemp as _mkstemp
from copy import copy as _copy
import codecs as _codecs
import re as _re
try:
    import numpy as _np
except:
    _np = None
from ..misc import unicode2byte as _unicode2str
from ..misc import byte2unicode as _str2unicode


def read_datafile(filename, only_header_and_variable_names=False, encoding=None,
                  read_variables=None):
    """Read an Expyriment data file.

    Returns the data, the variable names, the subject info & the comments:

    Parameters
    ----------
    filename : str
        name (fullpath) of the Expyriment data file
    only_header_and_variable_names : bool, optional
        if True the function reads only the header and variable names
        (default=False)
    encoding : str, optional
        the encoding with which the contents of the file will be read
    read_variables : array of str, optional
        array of variable names, read only the specified variables

    Returns
    -------
    data : list of list
        data array
    variables : list of str
        variable names list
    subject_info : dict
        dictionary with subject information (incl. date and between
        subject factors)
    comments : str
        string with remaining comments

    """

    delimiter = ","
    variables = None
    subject_info = {}
    comments = ""
    data = []

    if encoding is None:
        with open(filename, 'r') as fl:
            first_line = fl.readline()
            encoding = _re.findall("coding[:=]\s*([-\w.]+)", first_line)
            if encoding == []:
                second_line = fl.readline()
                encoding = _re.findall("coding[:=]\s*([-\w.]+)",
                                       second_line)
                if encoding == []:
                    encoding = [None]
    else:
        encoding = [encoding]

    read_in_columns = None
    fl = _codecs.open(filename, 'rb', encoding[0], errors='replace')
    for ln in fl:
        # parse infos
        ln = _str2unicode(ln.strip())
        if not(ln.startswith("#")):
            if variables is None:
                variables = ln.split(delimiter)
                if only_header_and_variable_names:
                    break
                if read_variables is not None:
                    read_in_columns = [variables.index(x) for x in read_variables]
                    variables = [variables[x] for x in read_in_columns]
            else:
                row =ln.split(delimiter)
                if read_in_columns is not None:
                    row = [row[x] for x in read_in_columns]
                data.append(row)
        else:
            if ln.startswith("#s"):
                ln = ln.replace("#s", "")
                tmp = ln.replace("=", ":")
                tmp = tmp.split(":")
                if len(tmp) == 2:
                    subject_info[tmp[0].strip()] = tmp[1].strip()
                else:
                    subject_info["#s{0}".format(len(subject_info))] = ln.strip()
            elif ln.startswith("#date:"):
                ln = ln.replace("#date:", "")
                subject_info["date"] = ln.strip()
            else:
                comments = comments + "\n" + ln
    fl.close()
    # strip variables
    variables = [x.strip() for x in variables]
    return data, variables, subject_info, comments


def write_csv_file(filename, data, varnames=None, delimiter=','):
    """Write 2D data array to csv file.

    Parameters
    ----------
    filename : str
        name (fullpath) of the data file
    data : list of list
        2D array with data (list of list)
    varnames : list of str, optional
        array of strings representing variable names
    delimiter : str, optional
        delimiter character (default=",")

    """

    _sys.stdout.write("write file: {0}".format(filename))
    try:
        _locale_enc = _locale.getdefaultlocale()[1]
    except:
        _locale_enc = "UTF-8"
    with open(filename, 'wb') as f:
        header = "# -*- coding: {0} -*-\n".format(_locale_enc)
        f.write(_unicode2str(header))
        if varnames is not None:
            for c, v in enumerate(varnames):
                if c > 0:
                    f.write(_unicode2str(delimiter))
                f.write(_unicode2str(v))
            f.write(_unicode2str("\n"))
        cnt = 0
        for row in data:
            for c, v in enumerate(row):
                if c > 0:
                    f.write(_unicode2str(delimiter))
                f.write(_unicode2str(v))
                cnt += 1
            f.write(_unicode2str("\n"))

    print(" ({0} cells in {1} rows)".format(cnt, len(data)))


def write_concatenated_data(data_folder, file_name, output_file=None,
                            delimiter=',', to_R_data_frame=False):
    """Concatenate data and write it to a csv file.

    All files that start with this name will be considered for the
    analysis (cf. aggregator.data_files)

    Notes
    -----
    The function is useful to combine the experimental data and prepare for
    further processing with other software.
    It basically wraps Aggregator.write_concatenated_data.

    Parameters
    ----------
    data_folder : str
        folder which contains of data of the subjects (str)
    file_name : str
        name of the files
    output_file : str, optional
        name of data output file.  If no specified data will the save
        to {file_name}.csv
    delimiter : str, optional
        delimiter character (default=",")
    to_R_data_frame: bool, optional
        if True, data will be converted to a R data frame that is saved
        in a RDS file

    """

    if to_R_data_frame:
        return Aggregator(data_folder=data_folder, file_name=file_name)\
        .write_concatenated_data_to_R_data_frame(output_file=output_file)
    else:
        return Aggregator(data_folder=data_folder, file_name=file_name)\
        .write_concatenated_data(output_file=output_file, delimiter=delimiter)



def get_experiment_duration(event_filename):
    """Extracts the experiment duration from event file and returns the time in
    minutes.

    Parameters
    ----------
    info_filename : str
        name (fullpath) of the Expyriment event file

    Returns
    -------
    minutes : float
        experiment duration in minutes

    """

    data, _, _, _ = read_datafile(event_filename)

    start = end = None
    for r in data:
        if r[1] == "Experiment":
            if r[2]=="started":
                start = int(r[0])
            elif r[2]=="ended":
                stop = int(r[0])

    sec = (stop-start) / 1000.0
    return sec / 60.0


class Aggregator(object):
    """A class implementing a tool to aggregate Expyriment data.

    This class is used to handle the multiple data files of a Experiment
    and process (i.e, aggregate) the data for further analysis

    Examples
    --------
    This tool helps, for instance, to aggregate your data for certain combinations
    of independent variables. E.g., data of a numerical magnitude judgement
    experiment. The code below makes a file with mean and median RTs and a
    second file with the errors and the number of trials::

        from expyriment.misc import data_preprocessing
        agg = data_preprocessing.Aggregator(data_folder= "./mydata/",
                                file_name = "MagnitudeJudgements")
        agg.set_computed_variables(["parity = target_number % 2",
                       "size = target_number > 65"])
        agg.set_independent_variables(["hand", "size" , "parity"])

        agg.set_exclusions(["trial_counter < 0",
                            "error != 0",
                            "RT < 2*std",
                            "RT > 2*std" # remove depending std in iv factor
                                         # combination for each subject
                            ])
        agg.set_dependent_variables(["mean(RT)", "median(RT)"])
        agg.aggregate(output_file="rts.csv")

        agg.set_exclusions(["trial_counter < 0"])
        agg.set_dependent_variables(["sum(error)", "n_trials"])
        agg.aggregate(output_file="errors.csv")

    """

    _relations = ["==", "!=", ">", "<", ">=", "<=", "=>", "<="]
    _operations = ["+", "-", "*", "/", "%"]
    _dv_functions = ["mean", "median", "sum", "std", "n_trials"]

    _default_suffix = ".xpd"

    def __init__(self, data_folder, file_name, suffix=_default_suffix,
                 read_variables=None):
        """Create an aggregator.

        Parameters
        ----------
        data_folder :str
            folder which contains of data of the subjects
        file_name : str
            name of the files. All files that start with this name will
            be considered for the analysis (cf. aggregator.data_files)
        suffix : str, optional
            if specified only files that end with this particular
            suffix will be considered (default=.xpd)
        read_variables : array of str, optional
            array of variable names, read only the specified variables

        """

        if not isinstance(_np, ModuleType):
            message = """Aggregator can not be initialized.
The Python package 'Numpy' is not installed."""
            raise ImportError(message)

        _version = _np.version.version.split(".")
        if not _version[0] == 1 and _version[1] < 6:
            raise ImportError("Expyriment {0} ".format(__version__) +
                              "is not compatible with Numpy {0}.".format(
                                  _np.version.version) +
                              "\nPlease install Numpy 1.6 or higher.")

        print("** Expyriment Data Preprocessor **")
        self.reset(data_folder, file_name, suffix, read_variables)

    def __str__(self):
        """Getter for the current design as text string."""
        design_str = "Data\n"
        design_str = design_str + u"- file name: " + self._file_name + "\n"
        design_str = design_str + u"- folder: " + self._data_folder + "\n"
        design_str = design_str + u"- {0} subject_data sets\n".format(
            len(self._data_files))
        design_str = design_str + u"- {0} variables: {1}\n".format(
            len(self.variables), self.variables)
        design_str = design_str + u"- recoded variables: {0}\n".format(
            self._recode_txt)
        design_str = design_str + u"- computed variables: {0}\n".format(
            self._computes_txt)
        design_str = design_str + u"Design\n"
        design_str = design_str + u"- independent Variables: {0}\n".format(
            self._iv_txt)
        design_str = design_str + u"- dependent Variables: {0}\n".format(
            self._dv_txt)
        design_str = design_str + u"- exclude: {0}\n".format(
            self._exclusions_txt)
        return design_str

    def _parse_syntax(self, syntax, throw_exception):
        """Preprocess relation and operation syntax.

        Returns relation array.

        """

        rels_ops = _copy(self._relations)
        rels_ops.extend(self._operations)
        found = None
        for ro in rels_ops:
            if syntax.find(ro) > 0:
                found = ro
                break
        if found is None:
            if throw_exception:
                raise RuntimeError("Incorrect syntax: '{0}'".format(
                    _unicode2str(syntax)))
            else:
                return None
        else:
            syntax = syntax.split(found)
            var_id = self._get_variable_id(syntax[0].strip(), True)
            return [var_id, found, syntax[1].strip()]

    def _get_variable_id(self, variables, throw_exception=False):
        for cnt, v in enumerate(self.variables):
            if variables == v:
                return cnt
        if (throw_exception):
            raise RuntimeError("Unknown variable name '{0}'".format(
                _unicode2str(variables)))
        return None

    def _add_independent_variable(self, variable):
        var_id = self._get_variable_id(variable, True)
        self._iv.append(var_id)

    def _add_dependent_variable(self, variable):
        if variable == "n_trials":
            self._dv.append([variable, 0])
        else:
            tmp = variable.replace(")", "").split("(")
            dv_fnc = tmp[0].strip()
            try:
                dv_txt = tmp[1].strip()
            except:
                raise RuntimeError(
                    "Incorrect syntax for DV: '{0}'".format(
                        _unicode2str(variable)))
            var_id = self._get_variable_id(dv_txt, True)
            if dv_fnc in self._dv_functions:
                self._dv.append([dv_fnc, var_id])
            else:
                raise RuntimeError("Unknown function for dependent variable:" +
                                   " '{0}'".format(_unicode2str(dv_fnc)))

    def _add_compute_variable(self, compute_syntax):
        """Add a new variable to be computed."""

        tmp = compute_syntax.replace("==", "@@")  # avoid confusion = & ==
        tmp = tmp.replace("!=", "##")  # avoid confusion = & ==
        tmp = tmp.split("=")
        variable_name = tmp[0].strip()
        try:
            syntax = tmp[1].strip()
            syntax = syntax.replace("@@", "==")
            syntax = syntax.replace("##", "==")
        except:
            raise RuntimeError("Incorrect compute syntax: '{0}'".format(
                _unicode2str(compute_syntax)))

        variable_def = self._parse_syntax(syntax, throw_exception=True)
        if variable_def is None:
            variable_def = self._parse_operation(syntax, throw_exception=True)
        if self._get_variable_id(variable_name) is not None:
            raise RuntimeError("Variable already defined '{0}'".format(
                _unicode2str(variable_name)))
        else:
            self._variables.append(variable_name)
            self._computes.append([variable_name, variable_def])

    def _add_exclusion(self, relation_syntax):
        """Add an exclusion."""

        relation = self._parse_syntax(relation_syntax, throw_exception=True)
        if relation[1] in self._relations:
            self._exclusions.append(relation)
        else:
            raise RuntimeError("Incorrect exclusion syntax: '{0}'".format(
                _unicode2str(relation_syntax)))

    def _add_variable_recoding(self, recode_syntax):
        """Add a new variable recoding rule."""

        error = False
        tmp = recode_syntax.split(":")
        if len(tmp) == 2:
            var_id = self._get_variable_id(tmp[0].strip(), True)
            excl_array = []
            for rule in tmp[1].split(","):
                rule = rule.split("=")
                if len(rule) == 2:
                    excl_array.append([rule[0].strip(), rule[1].strip()])
                else:
                    error = True
        else:
            error = True

        if error:
            raise RuntimeError("Incorrect recoding syntax: '{0}'".format(
                _unicode2str(recode_syntax)))
        else:
            self._recode.append([var_id, excl_array])

    def _find_idx(self, data, column_id, relation, value):
        """Find the indices of elements in a data column.

        Notes
        -----
        It compares of column elements with a value or the elements of a second
        column, if value is a name of variable.
        The method deals with numerical and string comparisons and throws an
        exception for invalid string comparisons.

        Parameters
        ----------
        data : numpy.array
            the data
        column_id : int
            id of column to compare
        relation : str
            relation as string.  possible relations:
            "==", "!=", ">", "<", ">=", "<=", "=>", "<="
        value : numeric or string
            value to find or a variable name

        """

        # is value a variable name
        second_var_id = self._get_variable_id(value, False)

        # _add_exclusion
        try:
            col = _np.float64(data[:, column_id])
        except:
            # handling strings
            col = data[:, column_id]
        try:
            if second_var_id is not None:
                val = _np.float64(data[:, second_var_id])
            else:
                val = _np.float64(value)
        except:
            # handling strings
            if second_var_id is not None:
                val = data[:, second_var_id]
            else:
                val = value

        if value.endswith("std") and (value.find("*") > 0):
            # remove relative depending std
            tmp = value.split("*")
            fac = float(tmp[0])

            mean_stds = self._dv_mean_std(data, column_id)
            idx = []
            if relation not in [">", "<", "=>", ">=", "=<", "<="]:
                raise RuntimeError("Incorrect syntax for " +
                                   "exception: '{0} {1}'".format(
                                       _unicode2str(relation),
                                       _unicode2str(value)))
            for cnt, row in enumerate(data):
                #find name of combination
                combi_str = self.variables[column_id]
                for iv in self._iv:
                    if isinstance(row[iv], str):
                        _row_data = _unicode2str(row[iv])
                    else:
                        _row_data = row[iv]
                    combi_str = combi_str + "_" + \
                        "{0}{1}".format(_unicode2str(self.variables[iv]),
                                        _row_data)
                deviation = float(row[column_id]) - mean_stds[combi_str][0]
                if (relation == ">" and
                    deviation > fac * mean_stds[combi_str][1]) or \
                   (relation == "=>" or relation == ">=" and
                    deviation >= fac * mean_stds[combi_str][1]) or \
                   (relation == "<" and
                    deviation < -fac * mean_stds[combi_str][1]) or \
                   (relation == "=<" or relation == "<=" and
                        deviation <= -fac * mean_stds[combi_str][1]):
                        idx.append(cnt)
            return idx
        else:
            if relation == "!=":
                comp = (col != val)
            elif relation == "==":
                comp = (col == val)
            elif relation == "<":
                comp = (col < val)
            elif relation == ">":
                comp = (col > val)
            elif relation == "=<" or relation == "<=":
                comp = (col <= val)
            elif relation == "=>" or relation == ">=":
                comp = (col >= val)
            else:
                comp = None  # should never occur
            if isinstance(comp, bool):
                raise RuntimeError(
                    "Incorrect syntax for " + "exception: '{0} {1}'".format(
                        _unicode2str(relation), _unicode2str(value)))
            return _np.flatnonzero(comp)

    def _dv_mean_std(self, data, column_dv_id):
        """ returns dict with std for iv_combinations """
        # get all iv values
        iv_values = []
        for iv in self._iv:
            tmp = list(set(data[:, iv]))
            tmp.sort()
            iv_values.append(tmp)

        new_variable_names, combinations = self._get_new_variables(iv_values)
        if len(combinations) == 0:
            combinations = ["total"]
        result = {}
        for cnt, fac_cmb in enumerate(combinations):
            if fac_cmb == "total":
                idx = list(range(0, data.shape[0]))
            else:
                # find idx of combinations
                idx = None
                for c, iv in enumerate(self._iv):
                    tmp = _np.array(data[:, iv] == fac_cmb[c])
                    if idx is None:
                        idx = tmp.copy()
                    else:
                        idx = idx & tmp
            # calc std over idx
            if len(idx) > 0:
                result[new_variable_names[cnt+1]] = [
                    _np.mean(_np.float64(data[idx, column_dv_id])),
                    _np.std(_np.float64(data[idx, column_dv_id]))]
                    # ignore first new var name, which is subject_id
        return result

    def _get_new_variables(self, iv_values):
        """Return the new variables names and factor_combinations.

        Requires the values for all independent variables iv_values: 2d array.
        Adds furthermore the defined the subject variables.

        """

        def increase_combination(comb, maxima, pos=None):
            """Recursive helper function.

            Returns None if end reached.

            """

            if pos is None:
                pos = len(comb) - 1
            comb[pos] += 1  # increase last position
            if comb[pos] > maxima[pos]:
                if pos <= 0:  # end reached
                    return None
                else:
                    for x in range(pos, len(comb)):  # set to zero & all pos. behind
                        comb[x] = 0
                    return increase_combination(comb, maxima, pos - 1)  # increase position before
            else:
                return comb

        # calc n levels
        n_levels = []
        for x in iv_values:
            n_levels.append(len(x) - 1)

        # build new variables names
        factor_combinations = []
        names = []
        if len(iv_values) > 0:
            tmp_comb = _np.zeros(len(self._iv), dtype=int)
            while tmp_comb is not None:
                txt = ""
                comb_values = []
                for c, x in enumerate(tmp_comb):
                    comb_values.append(iv_values[c][x])
                    if len(txt) > 0:
                        txt = txt + "_"
                    txt = txt + u"{0}{1}".format(self.variables[self._iv[c]],
                                comb_values[-1])
                names.append(txt)
                factor_combinations.append(comb_values)
                tmp_comb = increase_combination(tmp_comb, n_levels)

        new_variable_names = ["subject_id"]
        for sv in self.subject_variables:
            new_variable_names.append(u"{0}".format(sv))

        for dv in self._dv:
            if dv[0] == "n_trials":
                dv_txt = "ntr"
            else:
                dv_txt = self.variables[dv[1]]
            if len(names) > 0:
                for n in names:
                    new_variable_names.append(u"{0}_{1}".format(dv_txt, n))
            else:
                new_variable_names.append(u"{0}_total".format(dv_txt))

        return new_variable_names, factor_combinations

    def reset(self, data_folder, file_name, suffix=_default_suffix, variables=None):
        """Reset the aggregator class and clear design.

        Parameters
        ----------
        data_folder : str
            folder which contains of data of the subjects
        file_name : str
            name of the files. All files that start with this name
            will be considered for the analysis (cf. aggregator.data_files)
        suffix : str, optional
            if specified only files that end with this particular suffix
            will be considered (default=.xpd)
        variables : array of str, optional
            array of variable names, process only the specified variables


        """

        self._data_folder = data_folder
        self._file_name = file_name
        self._data_files = []
        self._variables = []
        self._dv = []
        self._dv_txt = []
        self._iv = []
        self._iv_txt = []
        self._exclusions = []
        self._exclusions_txt = []
        self._computes = []
        self._computes_txt = []
        self._recode_txt = []
        self._recode = []
        self._subject_variables = []
        self._last_data = []
        self._added_data = []
        self._added_variables = []
        self._suffix = suffix

        for flname in _os.listdir(_os.path.dirname(self._data_folder + "/")):
            if flname.endswith(self._suffix) and \
                    flname.startswith(self._file_name):
                _data, vnames, _subject_info, _comments = \
                    read_datafile(self._data_folder + "/" + flname,
                                  read_variables=variables)

                if len(self._variables) < 1:
                    self._variables = vnames
                else:
                    if vnames != self._variables:
                        message = u"Different variables in ".format(flname)
                        message = message + u"\n{0}".format(vnames)
                        message = message + u"\ninstead of\n{0}".format(
                            self._variables)
                        raise RuntimeError(_unicode2str(message))
                self._data_files.append(flname)

        if len(self._data_files) < 1:
            raise Exception("No data files found in {0}".format(
                _unicode2str(self._data_folder)))

        print("found {0} subject_data sets".format(len(self._data_files)))
        print("found {0} variables: {1}".format(len(self._variables),
                                                [_unicode2str(x) for x
                                                 in self._variables]))

    @property
    def data_folder(self):
        """Getter for data_folder."""

        return self._data_folder

    @property
    def data_files(self):
        """Getter for data_files.

        The list of the data files considered for the analysis.

        """

        return self._data_files

    @property
    def file_name(self):
        """Getter for file_name."""

        return self._file_name

    @property
    def variables(self):
        """Getter for variables.

        The specified variables including the new computer variables and
        between subject variables and added variables.

        """

        variables = _copy(self._variables)
        variables.extend(self._subject_variables)
        variables.extend(self._added_variables)
        return variables

    @property
    def added_variables(self):
        """Getter for added variables."""

        return self._added_variables

    @property
    def computed_variables(self):
        """Getter for computed variables."""

        return self._computes_txt

    @property
    def variable_recodings(self):
        """Getter for variable recodings."""

        return self._recode_txt

    @property
    def subject_variables(self):
        """Getter for subject variable."""

        return self._subject_variables

    @property
    def exclusions(self):
        """Getter for exclusions."""

        return self._exclusions_txt

    @property
    def dependent_variables(self):
        """Getter for dependent variables."""

        return self._dv_txt

    @property
    def independent_variables(self):
        """Getter for independent_variables."""

        return self._iv_txt

    def get_data(self, filename, recode_variables=True,
                 compute_new_variables=True, exclude_trials=True):
        """Read data from from a single Expyriment data file.

        Notes
        -----
        The function can be only applied on data of aggregator.data_files,
        that is, on the files in the defined data folder that start with
        the experiment name. According to the defined design, the result
        contains recoded data together with the new computed variables, and the
        subject variables from the headers of the Expyriment data files.

        Parameters
        ----------
        filename : str
            name of the Expyriment data file
        recode_variables : bool, optional
            set to False if defined variable recodings should not be applied
            (default=True)
        compute_new_variables : bool, optional
            set to False if new defined variables should not be computed
            (default=True)
        exclude_trials : bool, optional
            set to False if exclusion rules should not be applied
            (default=True)

        Returns
        -------
        data : numpy.array
        var_names : list
            list of variable names
        info : str
            subject info
        comment : str
            comments in data

        """

        # check filename
        if filename not in self._data_files:
            raise RuntimeError("'{0}' is not in the data list\n".format(
                _unicode2str(filename)))

        data, _vnames, subject_info, comments = \
            read_datafile(self._data_folder + "/" + filename)
        print("   reading {0}".format(_unicode2str(filename)))

        if recode_variables:
            for var_id, recoding in self._recode:
                for old, new in recoding:
                    for row in range(len(data)):
                        if data[row][var_id] == old:
                            data[row][var_id] = new

        data = _np.array(data, dtype='|U99')
        # compute new defined variables and append
        if compute_new_variables:
            for new_var_name, var_def in self._computes:
                if var_def[1] in self._relations:
                    # relations are true or false
                    col = _np.zeros([data.shape[0], 1], dtype=int)
                    idx = self._find_idx(data, var_def[0],
                                         var_def[1], var_def[2])
                    col[idx, 0] = 1
                else:
                    # operations
                    try:
                        a = _np.float64([data[:, var_def[0]]]).transpose()
                        second_var_id = self._get_variable_id(var_def[2],
                                                              False)
                        if second_var_id is not None:
                            b = _np.float64(
                                [data[:, second_var_id]]).transpose()
                        else:
                            b = _np.float64(var_def[2])
                    except:
                        msg = "Error while computing new variable {0}. " + \
                              "Non-number in variables of {1}"
                        msg.format(new_var_name, filename)
                        raise RuntimeError(msg)
                    if var_def[1] == "+":
                        col = a + b
                    elif var_def[1] == "-":
                        col = a - b
                    elif var_def[1] == "*":
                        col = a * b
                    elif var_def[1] == "/":
                        col = a / b
                    elif var_def[1] == "%":
                        col = a % b
                data = _np.concatenate((data, col), axis=1)

        # add subject information
        for sv in self.subject_variables:
            try:
                info = subject_info[sv]
            except:
                info = "nan"
            col = _np.array([[info for _x in range(data.shape[0])]])
            data = _np.c_[data, col.transpose()]

        # _add_exclusion trials
        if exclude_trials:
            for exl in self._exclusions:
                idx = self._find_idx(data, exl[0], exl[1], exl[2])
                if len(idx) > 0:
                    data = _np.delete(data, idx, axis=0)

        var = _copy(self._variables)
        var.extend(self._subject_variables)
        return [data, var, subject_info, comments]

    @property
    def concatenated_data(self):
        """Getter for concatenated_data.

        Notes
        -----
        Returns all data of all subjects as numpy.array and all variables
        names (including added variables). According to the defined design, the
        result contains the new computed variables and the subject variables
        from the headers of the Expyriment data files.

        If data have been loaded and no new variable or exclusion has been
        defined the concatenated_data will merely return the previous data
        without re-processing.

        Returns
        -------
        data : numpy.array
        variables : list of str

        """

        if len(self._last_data) > 0:  # data are already loaded and unchanged
            cdata = self._last_data
        else:
            cdata = None
            for flname in self._data_files:
                tmp = self.get_data(flname)[0]
                if cdata is None:
                    cdata = tmp
                else:
                    cdata = _np.concatenate((cdata, tmp), axis=0)
            self._last_data = cdata

        # append added data
        if len(self._added_variables) > 0:
            if cdata is not None:
                cdata = _np.concatenate((cdata, self._added_data), axis=1)
            else:
                cdata = self._added_data

        return [cdata, self.variables]

    def get_variable_data(self, variables):
        """Returns the column of data as numpy array.

        Parameters
        ----------
        variables : list of str
            names of the variables to be extracted

        Returns
        -------
        data : numpy.array

        """

        if not isinstance(variables, (list, tuple)):
            variables = [variables]

        cols = []
        for v in variables:
            cols.append(self._get_variable_id(v, throw_exception=True))

        data = self.concatenated_data[0]
        try:
            data = _np.float64(data[:, cols])
        except:
            data = data[:, cols]

        return data

    def add_variables(self, variable_names, data_columns):
        """Adds a new variable to the data.

        Notes
        -----
        The amount of variables and added columns must match. The added data
        must also match the number of rows. Note, manually added variables
        will be lost if cases will be excluded afterwards via a call of
        the method `set_exclusions`.

        Parameters
        ----------
        variable_names : str
            name of the new variable(s)
        data_columns : numpy.array
            the new data columns as numpy array

        """

        d = _np.array(data_columns)
        data_shape = _np.shape(d)
        if len(data_shape) < 2:
            d = _np.transpose([d])
            data_shape = (data_shape[0], 1)
        if not isinstance(variable_names, (list, tuple)):
            variable_names = [variable_names]

        if len(variable_names) != data_shape[1]:
            raise RuntimeError(
                "Amount of variables and added colums doesn't fit.")
        if data_shape[0] != _np.shape(self.concatenated_data[0])[0]:
            raise RuntimeError("Number of rows doesn't match.")

        self._added_variables.extend(variable_names)
        if len(self._added_data) == 0:
            self._added_data = d
        else:
            self._added_data = _np.concatenate((self._added_data, d), axis=1)
        self._last_data = []

    def write_concatenated_data(self, output_file=None, delimiter=','):
        """Concatenates data and writes it to a csv file.

        Parameters
        ----------
        output_file : str, optional
            name of data output file
            If not specified data will the save to {file_name}.csv
        delimiter : str
            delimiter character (default=",")

        """

        if output_file is None:
            output_file = u"{0}.csv".format(self.file_name)

        data = self.concatenated_data
        write_csv_file(filename=output_file, data=data[0], varnames=data[1],
                       delimiter=delimiter)

    def write_concatenated_data_to_R_data_frame(self, output_file):
        """Creates a R data frame of the concatenated data and stores it in a
        RDS file.

        Parameters
        ----------
        output_file : str, optional
            name of RDS output file
            If not specified data will the save to {file_name}.csv

        Notes
        -----
        This method requires R and the Python package 'Rpy2'.

        """

        try:
            import rpy2.robjects as robjects
        except:
            message = "Saving data to R data frame requires the " +\
                    "Python package 'Rpy2', which is not installed."""
            raise ImportError(message)

        if output_file is None:
            output_file = u"{0}.rds".format(self.file_name)
        fl, tmp_file_name = _mkstemp()
        _os.close(fl)
        self.write_concatenated_data(output_file=tmp_file_name, delimiter=',')

        robjects.r('''data = read.csv("{0}", comment.char="#",
        na.strings=c("NA", "None"))'''.format(tmp_file_name))
        robjects.r('''str(data)''')
        print("write file: {0}".format(output_file))
        robjects.r('''saveRDS(data, file="{0}")'''.format(output_file))
        try:
            _os.remove(tmp_file_name)
        except:
            pass

    def set_independent_variables(self, variables):
        """Set the independent variables.

        Parameters
        ----------
        variables : str or list
            the name(s) of one or more data variables (aggregator.variables)

        """

        if not isinstance(variables, (list, tuple)):
            self._iv_txt = [variables]
        else:
            self._iv_txt = variables
        self._iv = []
        for v in self._iv_txt:
            self._add_independent_variable(v)
        self._last_data = []

    def set_dependent_variables(self, dv_syntax):
        """Set dependent variables.

        Parameters
        ----------
        dv_syntax : str or list
            syntax describing the dependent variable by a function and variable,
            e.g. mean(RT)

        Notes
        -----
        Syntax::

            {function}({variable})
                {function} -- mean, median, sum, std or n_trials
                              Note: n_trials counts the number of trials
                              and does not require a variable as argument
                {variable} -- a defined data variable

        """

        if not isinstance(dv_syntax, (list, tuple)):
            self._dv_txt = [dv_syntax]
        else:
            self._dv_txt = dv_syntax
        self._dv = []
        for v in self._dv_txt:
            self._add_dependent_variable(v)
        self._last_data = []

    def set_exclusions(self, rule_syntax):
        """Set rules to exclude trials from the analysis.

        The method indicates the rows, which are ignored while reading
        the data files. It can therefore not be applied on variables that have
        been added later via `add_variables` and results in a loss of all
        manually added variables. Setting exclusions requires re-reading of
        the data files and might be therefore time consuming. Thus, call this
        method always at the beginning of your analysis script.

        Parameters
        ----------
        rule_syntax : str or list
            A string or a list of strings that represent the rules
            to exclude trials

        Notes
        -----
        Rule syntax::

            {variable} {relation} {variable/value}
                {variable}  -- a defined data variable
                {relation}  --  ==, !=, >, <, >=, <=, => or <=
                {value}     -- string or numeric

                If value is "{numeric} * std", trails are excluded in which
                the variable is below or above {numeric} standard deviations
                from the mean. The relations "==" and "!=" are not allow in
                this case. The exclusion criterion is apply for each subject
                and factor combination separately.

        """

        if not isinstance(rule_syntax, (tuple, list)):
            self._exclusions_txt = [rule_syntax]
        else:
            self._exclusions_txt = rule_syntax
        self._exclusions = []
        for r in self._exclusions_txt:
            self._add_exclusion(r)
        self._last_data = []
        self._added_data = []
        self._added_variables = []

    def set_variable_recoding(self, recoding_syntax):
        """Set syntax to recode variables.

        The method defines the variables, which will recoded.  It can not
        be applied on variables that have been added later via
        `add_variables`. Recoding variables requires re-reading of the data
        files and might be therefore time consuming.

        Parameters
        ----------
        rule_syntax : str or list
            A string or a list of strings that represent the variable
            recoding syntax

        Notes
        -----
        Recoding syntax::

           {variable}: {old_value1} = {new_value1}, {old_value2} = {new_value2},...

        """

        if not issubclass(recoding_syntax (list, tuple)):
            self._recode_txt = [recoding_syntax]
        else:
            self._recode_txt = recoding_syntax
        self._recode = []
        for syntax in self._recode_txt:
            self._add_variable_recoding(syntax)
        self._last_data = []

    def set_subject_variables(self, variables):
        """Set subject variables to be considered for the analysis.

        The method sets the subject variables. Subject variables are between
        subject factors or other variables defines in the subject information
        section (#s) of the Expyriment data file. The method requires a
        re-reading of the data files and might be therefore time consuming.

        Parameters
        ----------
        variables : str or list
            A string or a list of strings that represent the subject
            variables

        """

        if not isinstance(variables, (list, tuple)):
            self._subject_variables = [variables]
        else:
            self._subject_variables = variables
        self._last_data = []

    def set_computed_variables(self, compute_syntax):
        """Set syntax to compute new variables.

        The method defines the variables, which will be computed. It can not
        be applied on variables that have been added manually via
        `add_variables`. The method requires a re-reading of the data files
        and might be therefore time consuming.

        Parameters
        ----------
        compute_syntax : str or list
            A string or a list of strings that represent the syntax to
            compute the new variables

        Notes
        -----
        Compute Syntax::

            {new-variable} = {variable} {relation/operation} {variable/value}
                {new-variable} -- a new not yet defined variable name
                {variable}     -- a defined data variable
                {relation}     --  ==, !=, >, <, >=, <=, => or <=
                {operation}    -- +, -, *, / or %
                {value}        -- string or numeric

        """

        if not issubclass(compute_syntax, (list, tuple)):
            self._computes_txt = [compute_syntax]
        else:
            self._computes_txt = compute_syntax

        self._computes = []
        self._variables = read_datafile(self._data_folder + "/" +
                                        self._data_files[0],
                                        only_header_and_variable_names=True)[1]  # original variables
        for syntax in self._computes_txt:
            self._add_compute_variable(syntax)
        self._last_data = []

    def print_n_trials(self, variables):
        """Print the number of trials in the combinations of the independent
        variables.

        Notes
        -----
        The functions is for instance useful to quickly check the experimental
        design.

        Parameters
        ----------
        variables : str or list
            A string or a list of strings that represent the names of one or
            more data variables (aggregator.variables)

        """

        old_iv = self._iv
        old_dv = self._dv
        self.set_dependent_variables("n_trials")
        self.set_independent_variables(variables)
        result, varnames = self.aggregate()
        for row in result:
            print("Subject {0}".format(row[0]))
            for cnt, var in enumerate(varnames):
                if cnt > 0:
                    if isinstance(row[cnt], str):
                        _row_data = _unicode2str(row[cnt])
                    else:
                        _row_data = row[cnt]
                    print("\t{0}:\t{1}".format(var[4:], _row_data))
        print("\n")
        self._dv = old_dv
        self._iv = old_iv

    def aggregate(self, output_file=None, column_subject_id=0):
        """Aggregate the data as defined by the design.

        The design will be printed and the resulting data will be return as
        numpy.array together with the variable names.

        Parameters
        ----------
        output_file : str, optional
            name of data output file. If this output_file is defined the
            function write the results as csv data file
        column_subject_id : int, optional
            data column containing the subject id (default=0)

        Returns
        -------
        result : numpy.array
        new_variable_names : list of strings

        """

        data, _variables = self.concatenated_data
        subjects = list(set(data[:, column_subject_id]))
        subjects.sort()
        # get all iv values
        iv_values = []
        for iv in self._iv:
            tmp = list(set(data[:, iv]))
            tmp.sort()
            iv_values.append(tmp)

        new_variable_names, combinations = self._get_new_variables(iv_values)
        if len(combinations) == 0:
            combinations = ["total"]
        # calculate subject wise
        result = None
        for sub in subjects:
            mtx = data[data[:, column_subject_id] == sub, :]
            row = [sub]
            # subject info
            for sv in self.subject_variables:
                row.append(mtx[0, self._get_variable_id(sv)])
            for dv in self._dv:
                for fac_cmb in combinations:
                    if fac_cmb == "total":
                        idx = list(range(0, mtx.shape[0]))
                    else:
                        # find idx of combinations
                        idx = None
                        for c, iv in enumerate(self._iv):
                            tmp = _np.array(mtx[:, iv] == fac_cmb[c])
                            if idx is None:
                                idx = tmp.copy()
                            else:
                                idx = idx & tmp
                    # calc mean over idx
                    if len(idx) > 0:
                        values = mtx[idx, dv[1]]
                        if dv[0] == "median":
                            row.append(_np.median(_np.float64(values)))
                        elif dv[0] == "mean":
                            row.append(_np.mean(_np.float64(values)))
                        elif dv[0] == "sum":
                            row.append(_np.sum(_np.float64(values)))
                        elif dv[0] == "std":
                            row.append(_np.std(_np.float64(values)))
                        elif dv[0] == "n_trials":
                            row.append(values.shape[0])
                        else:
                            row.append(_np.NaN)
                    else:
                        row.append(_np.NaN)
            if result is None:
                result = _np.array([row], dtype='|U99')
            else:
                result = _np.r_[result, [row]]

        if output_file is not None:
            write_csv_file(output_file, result, new_variable_names)

        return result, new_variable_names
