#!/usr/bin/env python

"""A command line interface for Expyriment.

The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.
"""
from __future__ import absolute_import, print_function, division
from builtins import *

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys, os
from importlib import import_module

from . import control, io, show_documentation
from .misc import _secure_hash, get_system_info


def create_template():
    template_file = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This file is an automatically created template (via python -m expyriment.cli -C)
for an experiment with Expyriment.

"""

from expyriment import control, design, misc, io, stimuli

control.set_develop_mode(True)
exp = design.Experiment(name="My experiment")

## initialize ##
control.initialize(exp)

## start ##
control.start(exp)

stimuli.TextScreen("The experiment is running", "press any key").present()
exp.keyboard.wait()

## end ##
control.end()
'''
    print("Created template_expyriment.py")
    f = open('template_expyriment.py','w')
    f.write(template_file)
    f.close()

def join_data():
    from .misc import data_preprocessing
    print("Joining data")
    sys.stdout.write(" data subfolder [optional, default=data]? ")
    folder = input()
    if len(folder)<=0:
        folder = "data"
    start_with = input(" data files start with [optional]? ")
    d = data_preprocessing.Aggregator(folder, start_with)
    return d


cli_documentaion = """
python -m expyriment.cli [OPTIONS] [EXPYRIMENT SCRIPT]

The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.

    OPTIONS:
      -g | -0         No OpenGL (no vsync / no blocking)
      -1              OpenGL (vsync / no blocking)
      -2              OpenGL (vsync / blocking)
      -3              OpenGL (vsync / alternative blocking)
      -t              No time stamps for output files
      -w              Window mode
      -f              Fast mode (no initialize delay and fast quitting)
      -a              Auto create subject ID
      -i              Intensive logging (log level 2)
      -d              Develop mode (equivalent to -wfat)
      -b              Alternative blocking mode (blocking mode 2)

      -C              Create Expyriment template
      -J              Join data files to one single csv file
      -R              Join data files and create R data frame (in RDS file)
      -S              Print system information
      -T              Run the Expyriment Test Suite
      -A              Start the Expyrimnent API Reference Tool
      -B              Open browser with API reference
      -h              Show this help
"""

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="""The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.""",
            epilog="(c) F. Krause & O. Lindemann")

    parser.add_argument("SCRIPT", action='store_const', const=None,
                    help="The expyriment script to be executed")

    parser.add_argument("-g", "-0", action="store_true",
                    help="No OpenGL (no vsync / no blocking)")

    parser.add_argument("-1", action="store_true",
                    help="OpenGL (vsync / no blocking)")

    parser.add_argument("-2", action="store_true",
                    help="OpenGL (vsync / blocking)")

    parser.add_argument("-3", action="store_true",
                    help="OpenGL (vsync / alternative blocking)")

    parser.add_argument("-t", action="store_true",
                    help="No time stamps for output files")

    parser.add_argument("-w", action="store_true",
                    help="Window mode")

    parser.add_argument("-f", action="store_true",
                    help="Fast mode (no initialize delay and fast quitting)")

    parser.add_argument("-a", action="store_true",
                    help="Auto create subject ID")

    parser.add_argument("-i", action="store_true",
                    help="Intensive logging (log level 2)")

    parser.add_argument("-d", action="store_true",
                    help="Develop mode (equivalent to -wfat)")

    parser.add_argument("-b", action="store_true",
                    help="Alternative blocking mode (blocking mode 2)")

    parser.add_argument("-C", action="store_true",
                    help="Create Expyriment template")

    parser.add_argument("-J", action="store_true",
                    help="Join data files to one single csv file")

    parser.add_argument("-R", action="store_true",
                    help="Join data files and create R data frame (in RDS file)")

    parser.add_argument("-S", action="store_true",
                    help="Print system information")

    parser.add_argument("-T", action="store_true",
                    help="Run the Expyriment Test Suite")

    parser.add_argument("-A", action="store_true",
                    help="Start the Expyrimnent API Reference Tool")

    parser.add_argument("-B", action="store_true",
                    help="Open browser with API reference")

    parser.add_argument("--version", action="store_true",
                    help="Print version")

    #parse
    args = vars(parser.parse_args())

    if args['d']:
        control.set_develop_mode(True)
    elif args['i']:
        print("* Intensive logging")
        control.defaults.event_logging = 2
    elif args['f']:
        print("* Fast mode")
        control.defaults.initialize_delay = 0
        control.defaults.fast_quit = False
    elif args['w']:
        print("* Window mode")
        control.defaults.window_mode = True
    elif args['g']:
        print("* No OpenGL (no vsync / no blocking)")
        control.defaults.open_gl = False
    elif args['1']:
        print("* OpenGL (vsync / no blocking)")
        control.defaults.open_gl = 1
    elif args['2']:
        print("* OpenGL (vsync / blocking)")
        control.defaults.open_gl = 2
    elif args['3']:
        print("* OpenGL (vsync / alternative blocking)")
        control.defaults.open_gl = 3
    elif args['t']:
        print("* No time stamps")
        io.defaults.outputfile_time_stamp = False
    elif args['a']:
        print("* Auto create subject id")
        control.defaults.auto_create_subject_id = True
    elif args["S"]:
        print("System Info")
        print(get_system_info(as_string=True))
        sys.exit()
    elif args["T"]:
        print("Run Test Suite")
        control.run_test_suite()
        sys.exit()
    elif args["B"]:
        show_documentation(2)
        sys.exit()
    elif args["A"]:
        print("Start API Reference Tool")
        show_documentation(3)
        sys.exit()
    elif args["C"]:
        create_template()
        sys.exit()
    elif args["J"]:
        d = join_data()
        output =""
        while len(output) <= 1:
            output = input(" name of output csv file? ")
        d.write_concatenated_data(output)
        sys.exit()
    elif args["R"]:
        d = join_data()
        output =""
        while len(output) <= 1:
            output = input(" name of RDS file? ")
        d.write_concatenated_data_to_R_data_frame(output)
        sys.exit()

    # run script
    if args["SCRIPT"] is not None:
        script = os.path.abspath(args["SCRIPT"])
        if not os.path.isfile(script):
            print("Can't find {0}!".format(args["SCRIPT"]))
            exit()
        path, pyfile = os.path.split(script)
        os.chdir(path)
        sys.argv[0] = script # expyriment expect sys.argv[0] as main filename
        _secure_hash.main_file = script
        secure_hashes = {script : _secure_hash._make_secure_hash(script)}
        secure_hashes = _secure_hash.\
                    _append_hashes_from_imported_modules(secure_hashes, script)
        _secure_hash.secure_hashes = secure_hashes
        _secure_hash.cout_hashes()

        import_module(os.path.splitext(pyfile)[0])
