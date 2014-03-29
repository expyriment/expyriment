#!/usr/bin/env python

"""A command line interface for Expyriment.

Use this to start the Expyriment Reference Tool, or to run the Expyriment Test
Suite or any Python script with predefined Expyriment default settings.
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys, os, subprocess
import expyriment

short_info = """You must specify an option.
Try '-h' or '--help' for more information."""

info = """
Usage: python -m expyriment.cli [OPTIONS] [EXPYRIMENT SCRIPT]

The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.

    OPTIONS:
      -g              No OpenGL
      -t              No time stamps for output files
      -w              Window mode
      -f              Fast mode (no initialize delay and fast quitting)
      -a              Auto create subject ID
      -i              Intensive logging (log level 2)
      -d              Develop mode (equivalent to -gwfat)
      -C              Create Expyriment template
      -J              Join data files to one single csv file
      -S              Print system information
      -T              Run the Expyriment Test Suite
      -A              Start the Expyrimnent API Reference Tool
      -B              Open browser with API refelence
      -h              Show this help
"""

unknown_option = "Unknown option '{0}' (use --help for information)"

def create_templet():
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
    if sys.platform.startswith("linux"):
        print template_file
    else:
        print "Created template_expyriment.py in the current folder"
        f = open('template_expyriment.py','w')
        f.write(template_file)
        f.close()

def join_data():
    from expyriment.misc import data_preprocessing
    print "Joining data"
    sys.stdout.write(" data subfolder [optional, default=data]? ")
    folder = raw_input()
    if len(folder)<=0:
        folder = "data"
    start_with = raw_input(" data files start with [optional]? ")
    output =""
    while len(output)<=1:
        output = raw_input(" name of output csv file? ")
    d = data_preprocessing.Aggregator(folder, start_with)
    d.write_concatenated_data(output)


if __name__ == "__main__":

    if len(sys.argv) <= 1:
        print short_info
        sys.exit()

    script = None
    if len(sys.argv) > 1:
        for args in sys.argv[1:]:
            if args.startswith("-"):

                # long options
                if args.startswith("--"):
                     if args == "--help":
                        print info
                        sys.exit()
                     elif args == "--version":
                        pass
                     else:
                        print unknown_option.format(args)

                #short options
                else:
                    #sort args (capital letters last)
                    arguments = list(args[1:])
                    arguments.sort(reverse=True)

                    for arg in arguments:
                        if arg == 'd':
                            expyriment.control.set_develop_mode(True)
                        elif arg == 'i':
                            print "* Intensive logging"
                            expyriment.io.defaults.event_logging = 2
                        elif arg == 'f':
                            print "* Fast mode"
                            expyriment.control.defaults.initialize_delay = 0
                            expyriment.control.defaults.fast_quit = False
                        elif arg == 'w':
                            print "* Window mode (No OpenGL)"
                            expyriment.control.defaults.open_gl = False
                            expyriment.control.defaults.window_mode = True
                        elif arg == 'g':
                            print "* No OpenGL"
                            expyriment.control.defaults.open_gl = False
                        elif arg == 't':
                            print "* No time stamps"
                            expyriment.io.defaults.argvoutputfile_time_stamp =\
                                    False
                        elif arg == 'a':
                            print "* Auto create subject id"
                            expyriment.control.defaults.auto_create_subject_id\
                                             = True
                        elif arg == "S":
                            print "System Info"
                            print expyriment.get_system_info(as_string=True)
                            sys.exit()
                        elif arg == "T":
                            print "Run Test Suite"
                            expyriment.control.run_test_suite()
                            sys.exit()
                        elif arg == "B":
                            expyriment.show_documentation(2)
                            sys.exit()
                        elif arg == "A":
                            print "Start API Reference Tool"
                            expyriment.show_documentation(3)
                            sys.exit()
                        elif arg == "C":
                            create_templet()
                            sys.exit()
                        elif arg == "J":
                            join_data()
                            sys.exit()
                        elif arg == 'h':
                            print info
                            sys.exit()
                        else:
                            print unknown_option.format(arg)
                            sys.exit()

            #args starts not with "-"
            elif args.endswith(".py"):
                script = args

    if script is not None:
        sys.argv[0] = script # expyriment expect sys.argv[0] as main filename
        expyriment._secure_hash = "" # recalc secure hash
        print("File: {0} ({1})".format(script,
                expyriment.get_experiment_secure_hash()))
        execfile(script)
