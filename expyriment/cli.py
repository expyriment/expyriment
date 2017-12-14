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
from .misc import _secure_hash, get_system_info, download_from_stash


cli_documentation = """
expyriment [OPTIONS] [EXPYRIMENT SCRIPT]

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

    -C              Create experiment template
    -J              Join data files to one single csv file
    -R              Join data files and create R data frame (in RDS file)
    -S              Print system information
    -T              Run the Expyriment Test Suite
    -A              Start the Expyrimnent API Reference Tool
    -B              Open browser with API reference
    -h              Show this help
"""

def create_template():
    template_file = '''#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This file is an automatically created template for an Expyriment experiment.

It has been created by calling `expyriment -C`.

"""


import expyriment as xpy


# SETTINGS
#xpy.control.set_develop_mode()


# DESIGN
exp = xpy.design.Experiment(name="My Experiment")

xpy.control.initialize(exp)


# RUN
xpy.control.start()

xpy.stimuli.TextScreen("Hello World!", "[Press any key to continue]").present()
exp.keyboard.wait()

xpy.control.end(goodbye_text="Thank you for participating!")
'''
    print("Created experiment_template.py")
    f = open('experiment_template.py','w')
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

def main():
    import argparse
    parser = argparse.ArgumentParser(description="""The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.""",
            epilog="(c) F. Krause & O. Lindemann")
    
    if len(sys.argv[1:])==0:
        parser.print_help()
        parser.exit()

    parser.add_argument("SCRIPT", action='store', default=None,
                    help="The expyriment script to be executed",
                        nargs='?')

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
                    help="Create experiment template")
    
    parser.add_argument("-D", action="store_true",
                    help="Download from Expyriment stash")

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
    if args['i']:
        print("* Intensive logging")
        control.defaults.event_logging = 2
    if args['f']:
        print("* Fast mode")
        control.defaults.initialize_delay = 0
        control.defaults.fast_quit = False
    if args['w']:
        print("* Window mode")
        control.defaults.window_mode = True
    if args['g']:
        print("* No OpenGL (no vsync / no blocking)")
        control.defaults.open_gl = False
    if args['1']:
        print("* OpenGL (vsync / no blocking)")
        control.defaults.open_gl = 1
    if args['2']:
        print("* OpenGL (vsync / blocking)")
        control.defaults.open_gl = 2
    if args['3']:
        print("* OpenGL (vsync / alternative blocking)")
        control.defaults.open_gl = 3
    if args['t']:
        print("* No time stamps")
        io.defaults.outputfile_time_stamp = False
    if args['a']:
        print("* Auto create subject id")
        control.defaults.auto_create_subject_id = True
    if args["S"]:
        print("System Info")
        print(get_system_info(as_string=True))
        sys.exit()
    if args["T"]:
        print("Run Test Suite")
        control.run_test_suite()
        sys.exit()
    if args["B"]:
        show_documentation(2)
        sys.exit()
    if args["A"]:
        print("Start API Reference Tool")
        show_documentation(3)
        sys.exit()
    if args["C"]:
        create_template()
        sys.exit()
    if args["D"]:
        print("Download from stash")
        what = ""
        while what not in ["all", "examples", "extras", "tools"]:
            what = input(" what to download ([all]/examples/extras/tools)? ")
            if what == "":
                what = "all"
        branches = ["master"]
        if __version__ != "":
            branches.append(__version__)
        branch = ""
        while branch not in branches:
            branch = input(" from which branch? ([master]{0})? ".format(
                "/".join(branches[1:])))
            if branch == "":
                branch = "master"
        download_from_stash(what, branch)
    if args["J"]:
        d = join_data()
        output =""
        while len(output) <= 1:
            output = input(" name of output csv file? ")
        d.write_concatenated_data(output)
        sys.exit()
    if args["R"]:
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

        execfile(pyfile)


if __name__ == "__main__":
    main()
