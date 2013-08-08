#!/usr/bin/env python

"""A command line interface for Expyriment.

Use this to start the Expyriment Reference Tool, or to run the Expyriment Test
Suite or any Python script with predefined Expyriment default settings.

Usage: python -m expyriment.cli [EXPYRIMENT SCRIPT] [OPTIONS]

OPTIONS:
      -g              No OpenGL
      -t              No time stamps for output files
      -w              Window mode
      -f              Fast mode (no initialize delay and fast quitting)
      -a              Auto create subject ID
      -i              Intensive logging (log level 2)
      -d              Develop mode (equivalent to -gwfat)
      -T              Run the Expyriment Test Suite
      -A              Start the Expyrimnent API Reference Tool
      -h              Show this help
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


if __name__ == "__main__":

    import sys, os, subprocess

    import expyriment


    script = None
    if len(sys.argv) > 1:
        if sys.argv[1].endswith(".py"):
            script = sys.argv[1]
        for args in sys.argv[1:]:
            if args.startswith("-"):
                for arg in args[1:]:
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
                        expyriment.io.defaults.outputfile_time_stamp = False
                    elif arg == 'a':
                        print "* Auto create subject id"
                        expyriment.control.defaults.auto_create_subject_id = \
                                True
                    elif arg == "T":
                        print "Run Test Suite"
                        expyriment.control.run_test_suite()
                        sys.exit()
                    elif arg == "A":
                        print "Start API Reference Tool"
                        expyriment.show_documentation(3)
                        sys.exit()
                    elif arg == 'h':
                            print """
Usage: python -m expyriment.cli [EXPYRIMENT SCRIPT] [OPTIONS]

    OPTIONS:
          -g              No OpenGL
          -t              No time stamps for output files
          -w              Window mode
          -f              Fast mode (no initialize delay and fast quitting)
          -a              Auto create subject ID
          -i              Intensive logging (log level 2)
          -d              Develop mode (equivalent to -gwfat)
          -T              Run Test Suite
          -A              Start API Reference Tool
          -h              Show this help
"""
                            sys.exit()

    if script is not None:
        execfile(script)
# FIXME cli.py in online docu?
