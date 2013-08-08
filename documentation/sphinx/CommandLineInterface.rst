Command line interface
======================
The command line interface can be used to start the Expyriment Reference Tool, 
or to run the Expyriment test suite or any Python script with predefined 
Expyriment default settings.

Usage::

    python -m expyriment.cli [EXPYRIMENT SCRIPT] [OPTIONS]

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
