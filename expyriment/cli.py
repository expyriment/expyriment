#!/usr/bin/env python

"""A command line interface for Expyriment.

The Expyriment command line interface provides a collection of convenient
methods helpful for the development and testing of experiments as well as
functions to join the data output.
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'


import sys, os
from importlib import import_module
from importlib.util import find_spec

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
        add_help=True)

    parser.add_argument("SCRIPT", action='store', default=None,
                        help="the experiment script to be executed",
                        nargs='?')
    # DEPRECATED
    parser.add_argument("-0", "-g", "--no-opengl", action="store_true",
                        help="DEPRECATED: no OpenGL (no vsync / no blocking)")

    parser.add_argument("-1", "--no-blocking", action="store_true",
                        help="DEPRECATED: OpenGL (vsync / no blocking)")

    parser.add_argument("-2", "--blocking", action="store_true",
                        help="DEPRECATED: OpenGL (vsync / blocking)")

    parser.add_argument("-3", "--alternative-blocking",
                        action="store_true",
                        help="DEPRECATED: OpenGL (vsync / alternative blocking)")
    # END DEPRECATED

    parser.add_argument("-a", "--auto-subject-id",
                        action="store_true",
                        help="auto create subject ID")

    parser.add_argument("-d", "--develop-mode",
                        action="store_true",
                        help="develop mode (equivalent to -wfat)")

    parser.add_argument("-f", "--fast-mode",
                        action="store_true",
                        help="fast mode (no initialize delay and fast quitting)")

    parser.add_argument("-i", "--intensive-logging",
                        action="store_true",
                        help="intensive logging (log level 2)")

    parser.add_argument("-t", "--no-time-stamps",
                        action="store_true",
                        help="no time stamps for output files")

    parser.add_argument("-w", "--window-mode",
                        action="store_true",
                        help="window mode")

    parser.add_argument("--display", metavar="INDEX", type=int,
                        help="show the screen on specific display (multi-monitor setting)")

    parser.add_argument("--display-resolution", metavar="WIDTHxHEIGHT",
                        help="set the display resolution (only in fullscreen mode)")

    parser.add_argument("--opengl", metavar="MODE", type=int,
                        help="set the OpenGL mode: "\
                        "0 = No OpenGL (no vsync / no blocking), " +\
                        "1 = OpenGL (vsync / no blocking), "\
                        "2 = OpenGL (vsync / blocking)")

    parser.add_argument("--window-size", metavar="WIDTHxHEIGHT",
                        help="set the window size (only in window mode)")

    parser.add_argument("-A", "--Api",
                        action="store_true",
                        help="start the API reference tool")

    parser.add_argument("-B", "--Browser-api",
                        action="store_true",
                        help="open browser with API reference")

    parser.add_argument("-C", "--Create-exp",
                        action="store_true",
                        help="create experiment template")

    parser.add_argument("-D", "--Download-stash",
                        action="store_true",
                        help="download from Expyriment stash")

    parser.add_argument("-I", "--Interactive",
                        action="store_true",
                        help="start an interactive session")

    parser.add_argument("-J", "--Join-data",
                        action="store_true",
                        help="join data files to one single csv file")

    parser.add_argument("-S", "--System-info",
                        action="store_true",
                        help="print system information")

    parser.add_argument("-T", "--Test-suite",
                        action="store_true",
                        help="run the Expyriment test suite")

    # parse
    args = vars(parser.parse_args())
    import expyriment as xpy

    # options
    if args['develop_mode']:
        xpy.control.set_develop_mode(True)

    if args['intensive_logging']:
        print("* Intensive logging")
        xpy.control.defaults.event_logging = 2

    if args['fast_mode']:
        print("* Fast mode")
        xpy.control.defaults.initialize_delay = 0
        xpy.control.defaults.fast_quit = False

    if args['window_mode']:
        print("* Window mode")
        xpy.control.defaults.window_mode = True

    for x in ['no_opengl', 'no_blocking', 'blocking', 'alternative_blocking']:
        if args[x] is True:
            raise DeprecationWarning(
                "'{0}' is deprecated! Please use 'opengl'. " +\
                "See '-h' or '--help' for more information".format(x))

    if args['opengl'] is not None:
        mode = args['opengl']
        if mode == 0:
            xpy.control.defaults.opengl = 0
            print("* No OpenGL (no vsync / no blocking)")
        elif mode == 1:
            xpy.control.defaults.opengl = 1
            print("* OpenGL (vsync / no blocking)")
        elif mode == 2:
            xpy.control.defaults.opengl = 2
            print("* OpenGL (vsync / blocking")

    if args['no_time_stamps']:
        print("* No time stamps")
        xpy.io.defaults.outputfile_time_stamp = False

    if args['auto_subject_id']:
        print("* Auto create subject id")
        xpy.control.defaults.auto_create_subject_id = True

    if args["display"] is not None and args["display"] >= 0:
        print("* Using display #{0}".format(args["display"]))
        xpy.control.defaults.display = args["display"]

    if args["display_resolution"] is not None:
        res = [int(x) for x in args["display_resolution"].split("x")]
        xpy.control.defaults.display_resolution = res
        print("* Setting display resolution to {0}".format(
            args["display_resolution"]))

    if args["window_size"] is not None:
        res = [int(x) for x in args["window_size"].split("x")]
        xpy.control.defaults.display_resolution = res
        print("* Setting window size to {0}".format(
            args["window_size"]))

    # commands
    if args["System_info"]:
        print("System info")
        print(xpy.misc.get_system_info(as_string=True))

    elif args["Test_suite"]:
        print("Run test suite")
        xpy.control.run_test_suite()

    elif args["Browser_api"]:
        xpy.show_documentation(1)

    elif args["Api"]:
        print("Start API reference tool")
        xpy.show_documentation(2)

    elif args["Create_exp"]:
        create_template()

    elif args["Download_stash"]:
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

    elif args["Join_data"]:
        d = join_data()
        output = ""
        while len(output) <= 1:
            sys.stdout.write(" name of output csv file? ")
            output = input()
        d.write_concatenated_data(output)

    elif args["Interactive"]:
        print("Interactive session")
        print("")
        expyriment = xpy
        xpy.control.defaults.window_mode = True
        xpy.control.defaults.stdout_logging = False
        #exp = xpy.control.initialize()
        banner = """Expyriment is available as both 'expyriment' and 'xpy'.
Run 'exp = xpy.control.initialize()' to quickly initialize a new experiment."""
        if find_spec("readline") is not None:
            import readline
        if find_spec("IPython") is not None:
            import IPython
            IPython.embed(header=banner)
        else:
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

    else:
        parser.print_usage()

    sys.exit()


if __name__ == "__main__":
    main()
