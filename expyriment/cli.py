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

#from . import control, io, show_documentation
#from .misc import _secure_hash, get_system_info, download_from_stash

print("")
print("Expyriment command line interface")
print("")

def create_template():
    template_file = '''# -*- coding: utf-8 -*-

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
    if len(folder) <= 0:
        folder = "data"
    start_with = input(" data files start with [optional]? ")
    d = data_preprocessing.Aggregator(folder, start_with)
    return d


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="""
The Expyriment command line interface provides a convenient way to run
experiment scripts and apply default settings, as well as access to a
selection of other common functionality.

Note: non-capitalized letter arguments are (chainable) options, capitalized
letter arguments run single commands""",
        epilog="(c) F. Krause & O. Lindemann",
        add_help=False)

    parser.add_argument("SCRIPT", action='store', default=None,
                        help="the experiment script to be executed",
                        nargs='?')
    parser.add_argument("-h", "--help", action="store_true",
                        help=argparse.SUPPRESS)

    parser.add_argument("-0", "-g", action="store_true",
                        help="no OpenGL (no vsync / no blocking)")

    parser.add_argument("-1", action="store_true",
                        help="OpenGL (vsync / no blocking)")

    parser.add_argument("-2", action="store_true",
                        help="OpenGL (vsync / blocking)")

    parser.add_argument("-3", action="store_true",
                        help="OpenGL (vsync / alternative blocking)")

    parser.add_argument("-a", action="store_true",
                        help="auto create subject ID")

    parser.add_argument("-d", action="store_true",
                        help="develop mode (equivalent to -wfat)")

    parser.add_argument("-f", action="store_true",
                        help="fast mode (no initialize delay and fast quitting)")

    parser.add_argument("-i", action="store_true",
                        help="intensive logging (log level 2)")

    parser.add_argument("-t", action="store_true",
                        help="no time stamps for output files")

    parser.add_argument("-w", action="store_true",
                        help="window mode")

    parser.add_argument("-A", action="store_true",
                        help="start the API reference tool")

    parser.add_argument("-B", action="store_true",
                        help="open browser with API reference")

    parser.add_argument("-C", action="store_true",
                        help="create experiment template")

    parser.add_argument("-D", action="store_true",
                        help="download from Expyriment stash")

    parser.add_argument("-I", action="store_true",
                        help="start an interactive session")

    parser.add_argument("-J", action="store_true",
                        help="join data files to one single csv file")

    parser.add_argument("-S", action="store_true",
                        help="print system information")

    parser.add_argument("-T", action="store_true",
                        help="run the Expyriment test suite")

    # parse
    args = vars(parser.parse_args())
    if len(sys.argv[1:]) == 0 or args['help']:
        parser.print_help()
        parser.exit()

    import expyriment as xpy

    # options
    if args['d']:
        xpy.control.set_develop_mode(True)
    if args['i']:
        print("* Intensive logging")
        xpy.control.defaults.event_logging = 2
    if args['f']:
        print("* Fast mode")
        xpy.control.defaults.initialize_delay = 0
        xpy.control.defaults.fast_quit = False
    if args['w']:
        print("* Window mode")
        xpy.control.defaults.window_mode = True
    if args['0']:
        print("* No OpenGL (no vsync / no blocking)")
        xpy.control.defaults.open_gl = False
    if args['1']:
        print("* OpenGL (vsync / no blocking)")
        xpy.control.defaults.open_gl = 1
    if args['2']:
        print("* OpenGL (vsync / blocking)")
        xpy.control.defaults.open_gl = 2
    if args['3']:
        print("* OpenGL (vsync / alternative blocking)")
        xpy.control.defaults.open_gl = 3
    if args['t']:
        print("* No time stamps")
        xpy.io.defaults.outputfile_time_stamp = False
    if args['a']:
        print("* Auto create subject id")
        xpy.control.defaults.auto_create_subject_id = True

    # commands
    if args["S"]:
        print("System info")
        print(xpy.misc.get_system_info(as_string=True))
    elif args["T"]:
        print("Run test suite")
        xpy.control.run_test_suite()
    elif args["B"]:
        xpy.show_documentation(2)
    elif args["A"]:
        print("Start API reference tool")
        xpy.show_documentation(3)
    elif args["C"]:
        create_template()
    elif args["D"]:
        print("Download from stash")
        what = ""
        while what not in ["all", "examples", "extras", "tools"]:
            sys.stdout.write(" what to download ([all]/examples/extras/tools)? ")
            what = input()
            if what == "":
                what = "all"
        branches = ["master"]
        if __version__ != "":
            branches.append(__version__)
        branch = ""
        while branch not in branches:
            if len(branches) == 1:
                sys.stdout.write(" from which branch? ([master])? ")
            else:
                sys.stdout.write(" from which branch? (master/[{0}])? ".format(
                branches[1]))
            branch = input()
            if branch == "":
                if len(branches) == 1:
                    branch = "master"
                else:
                    branch = branches[1]
        xpy.misc.download_from_stash(what, branch)
    elif args["J"]:
        d = join_data()
        output = ""
        while len(output) <= 1:
            sys.stdout.write(" name of output csv file? ")
            output = input()
        d.write_concatenated_data(output)
    elif args["I"]:
        print("Interactive session")
        print("")
        expyriment = xpy
        #exp = xpy.control.initialize()
        banner = """Expyriment is available as both 'expyriment' and 'xpy'.
Run 'exp = xpy.control.initialize()' to quickly initialize a new experiment."""
        try:
            import readline
        except Exception:
            pass
        try:
            import IPython
            IPython.embed(header=banner)
        except Exception:
            import code
            code.interact(local=locals(), banner=banner)

    # run script
    elif args["SCRIPT"] is not None:
        script = os.path.abspath(args["SCRIPT"])
        if not os.path.isfile(script):
            print("Can't find {0}!".format(args["SCRIPT"]))
            exit()
        path, pyfile = os.path.split(script)
        os.chdir(path)
        sys.argv[0] = script # expyriment expect sys.argv[0] as main filename
        xpy.misc._secure_hash.main_file = script
        secure_hashes = {script : xpy.misc._secure_hash._make_secure_hash(
            script)}
        secure_hashes = xpy.misc._secure_hash.\
                    _append_hashes_from_imported_modules(secure_hashes, script)
        xpy.misc._secure_hash.secure_hashes = secure_hashes
        xpy.misc._secure_hash.cout_hashes()

        def execfile(filepath, globals=None, locals=None):
            if globals is None:
                globals = {}
            globals.update({
                "__file__": filepath,
                "__name__": "__main__",
            })
            with open(filepath, 'rb') as file:
                exec(compile(file.read(), filepath, 'exec'), globals, locals)
        execfile(pyfile)

    sys.exit()


if __name__ == "__main__":
    main()
