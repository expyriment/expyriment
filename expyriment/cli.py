#!/usr/bin/env python

"""A command line interface for Expyriment.

The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys, os
from importlib import import_module
import expyriment

short_info = """You must specify an option.
Try '-h' or '--help' for more information."""

info = """
Usage: python -m expyriment.cli [OPTIONS] [EXPYRIMENT SCRIPT]

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

unknown_option = "Unknown option '{0}' (use --help for information)"

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
    print "Created template_expyriment.py"
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
    d = data_preprocessing.Aggregator(folder, start_with)
    return d


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
                            expyriment.control.defaults.event_logging = 2
                        elif arg == 'f':
                            print "* Fast mode"
                            expyriment.control.defaults.initialize_delay = 0
                            expyriment.control.defaults.fast_quit = False
                        elif arg == 'w':
                            print "* Window mode"
                            expyriment.control.defaults.window_mode = True
                        elif arg == 'g' or arg == '0':
                            print "* No OpenGL (no vsync / no blocking)"
                            expyriment.control.defaults.open_gl = False
                        elif arg == '1':
                            print "* OpenGL (vsync / no blocking)"
                            expyriment.control.defaults.open_gl = 1
                        elif arg == '2':
                            print "* OpenGL (vsync / blocking)"
                            expyriment.control.defaults.open_gl = 2
                        elif arg == '3':
                            print "* OpenGL (vsync / alternative blocking)"
                            expyriment.control.defaults.open_gl = 3
                        elif arg == 't':
                            print "* No time stamps"
                            expyriment.io.defaults.outputfile_time_stamp =\
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
                            create_template()
                            sys.exit()
                        elif arg == "J":
                            d = join_data()
                            output =""
                            while len(output) <= 1:
                                output = raw_input(" name of output csv file? ")
                            d.write_concatenated_data(output)
                            sys.exit()
                        elif arg == "R":
                            d = join_data()
                            output =""
                            while len(output) <= 1:
                                output = raw_input(" name of RDS file? ")
                            d.write_concatenated_data_to_R_data_frame(output)
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
        script = os.path.abspath(script)
        path, pyfile = os.path.split(script)
        os.chdir(path)
        sys.argv[0] = script # expyriment expect sys.argv[0] as main filename
        expyriment._secure_hash.main_file = script
        secure_hashes = {script : expyriment._secure_hash._make_secure_hash(script)}
        secure_hashes = expyriment._secure_hash.\
                    _append_hashes_from_imported_modules(secure_hashes, script)
        expyriment._secure_hash.secure_hashes = secure_hashes
        expyriment._secure_hash.cout_hashes()

        import_module(os.path.splitext(pyfile)[0])
