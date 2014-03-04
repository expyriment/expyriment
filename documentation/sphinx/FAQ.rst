Frequently Asked Questions (FAQs)
==================================

Version control
----------------

**How do I figure out which version of Expyriment is installed?**

    If you ``import expyriment`` in a Python shell (e.g., IDLE or IPython), the 
    version number will be displayed. The version number also appears at the 
    Expyriment start screen and in all output files. (see also 
    ``expyriment.get_version()``).

**How can ensure I that the correct version of my experiment py-file has been 
used in the lab?**

    Expyriment uses fingerprints (i.e., SHA1 hash codes) of the your main 
    python file to track, which version of your expyriment was used while the 
    experimental run.  The secure hash code is displayed at on start screen and 
    printed in all output files. Please see the documentation for 
    ``expyriment.get_experiment_secure_hash()``.
