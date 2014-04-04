"""
Secure hashes from files
"""

__author__ = 'Florian Krause <florian@expyriment.org>, \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''

import sys
from hashlib import sha1

experiment_secure_hash = ""
experiment_files = [sys.argv[0]]

def _make_secure_hash(filename):
    """returns secure hash from file or None, if not possile"""
    try:
        with open(filename) as f:
            return sha1(f.read()).hexdigest()[:6]
    except:
        return None

def get_experiment_secure_hash():
    """Returns the fingerprint, that is, the first six places of the secure
    hash (sha1) of the main file of the current experiment.

    Returns
    -------
    hash: string or None
        first six places of the experiment secure hash or None, if no main
        file can be found

    Notes
    -----
    Fingerprints of experiments help to ensure that the correct version is
    running in the lab. Hash codes are written to all output files and
    printed in the command line output. If you want to check post hoc the
    version of your experiment, create the secure hash (sha1) of your
    expyriment .py-file and compare the first six place with the code in the
    output file.

    """

    global experiment_secure_hash
    if experiment_secure_hash != "":
        return experiment_secure_hash
    experiment_secure_hash = _make_secure_hash(experiment_files[0])
    return get_experiment_secure_hash()

# print hash information when imported
if get_experiment_secure_hash() is not None:
    print("File: {0} ({1})".format(sys.argv[0], get_experiment_secure_hash()))


