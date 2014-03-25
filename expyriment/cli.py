#!/usr/bin/env python

"""A command line interface for Expyriment.

Use this to start the Expyriment Reference Tool, or to run the Expyriment Test
Suite or any Python script with predefined Expyriment default settings.

Usage: python -m expyriment.cli [OPTIONS] [EXPYRIMENT SCRIPT]
OPTIONS:
      -g              No OpenGL
      -t              No time stamps for output files
      -w              Window mode
      -f              Fast mode (no initialize delay and fast quitting)
      -a              Auto create subject ID
      -i              Intensive logging (log level 2)
      -d              Develop mode (equivalent to -gwfat)
      -C              Create Expyriment template file
      -S              Print system information
      -T              Run the Expyriment Test Suite
      -A              Start the Expyrimnent API Reference Tool
      -h              Show this help
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

info = """
Usage: python -m expyriment.cli [OPTIONS] [EXPYRIMENT SCRIPT]

    OPTIONS:
      -g              No OpenGL
      -t              No time stamps for output files
      -w              Window mode
      -f              Fast mode (no initialize delay and fast quitting)
      -a              Auto create subject ID
      -i              Intensive logging (log level 2)
      -d              Develop mode (equivalent to -gwfat)
      -C              Create Expyriment template file
      -S              Print system information
      -T              Run the Expyriment Test Suite
      -A              Start the Expyrimnent API Reference Tool
      -h              Show this help
"""

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


if __name__ == "__main__":

    import sys, os, subprocess
    import expyriment

    if len(sys.argv) <= 1:
        sys.argv.append("-h")

    script = None
    if len(sys.argv) > 1:
        for args in sys.argv[1:]:
            if args.startswith("-"):
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
                        expyriment.io.defaults.argvoutputfile_time_stamp = False
                    elif arg == 'a':
                        print "* Auto create subject id"
                        expyriment.control.defaults.auto_create_subject_id = \
                                True
                    elif arg == "S":
                        print "System Info"
                        print expyriment.get_system_info(as_string=True)
                        sys.exit()
                    elif arg == "T":
                        print "Run Test Suite"
                        expyriment.control.run_test_suite()
                        sys.exit()
                    elif arg == "A":
                        print "Start API Reference Tool"
                        expyriment.show_documentation(3)
                        sys.exit()
                    elif arg == "C":
                        print "Created template_expyriment.py in the current folder"
                        f = open('template_expyriment.py','w')
                        f.write(template_file)
                        sys.exit()
                    elif arg == 'h':
                            print info
                            sys.exit()

            elif args.endswith(".py"):
                script = args

    if script is not None:
        sys.argv[0] = script # expyriment expect sys.argv[0] as main filename
        expyriment._secure_hash = "" # recalc secure hash
        print("File: {0} ({1})".format(script,
                expyriment.get_experiment_secure_hash()))
        execfile(script)
