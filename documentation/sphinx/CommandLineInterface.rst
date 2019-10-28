Command line interface
======================

The Expyriment command line interface provides a convenient way to run
experiment scripts and apply default settings, as well as access to a
selection of other common functionality.

Usage
-----

::
    
    expyriment [-h] [-g] [-1] [-2] [-3] [-t] [-w] [-f] [-a] [-i] [-d] [-b]
               [-C] [-D] [-J] [-R] [-S] [-T] [-A] [-B] [--version]
               [SCRIPT]

    positional arguments:
      SCRIPT      The expyriment script to be executed

    optional arguments:
      -h, --help  show this help message and exit
      -g, -0      No OpenGL (no vsync / no blocking)
      -1          OpenGL (vsync / no blocking)
      -2          OpenGL (vsync / blocking)
      -3          OpenGL (vsync / alternative blocking)
      -t          No time stamps for output files
      -w          Window mode
      -f          Fast mode (no initialize delay and fast quitting)
      -a          Auto create subject ID
      -i          Intensive logging (log level 2)
      -d          Develop mode (equivalent to -wfat)
      -b          Alternative blocking mode (blocking mode 2)
      -C          Create experiment template
      -D          Download from Expyriment stash
      -J          Join data files to one single csv file
      -R          Join data files and create R data frame (in RDS file)
      -S          Print system information
      -T          Run the Expyriment Test Suite
      -A          Start the Expyriment API Reference Tool
      -B          Open browser with API reference
      --version   Print version
