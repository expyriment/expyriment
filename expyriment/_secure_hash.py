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
from copy import copy

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

    if secure_hashes.has_key(main_file):
        return secure_hashes[main_file]
    else:
        return None

def get_module_hash_dictionary():
    """Returns a dictionary with the fingerprints of all modules imported
    from the local folded.

    Returns
    -------
    hashes: dict
        hash dict with all imported modules
        keys = file names, values = sha hashes

    Notes
    -----
    See get_experiment_secure_hash() for further information about Expyriment
    secure hashes.

    """
    if secure_hashes.has_key(main_file):
        rtn = copy(secure_hashes)
        rtn.pop(main_file)
    return rtn

def _make_hash_dict():
    """get all imported py modules from local directory"""
    global main_file
    rtn = {main_file : _make_secure_hash(main_file)}
    try:
        with open(main_file) as f:
            for line in f:
                if line.startswith("import") or line.startswith("from"):
                    pyfl = line.strip().split(" ")[1] + ".py"
                    sha = _make_secure_hash(pyfl)
                    if sha is not None:
                        rtn[pyfl] = sha
    except:
        pass
    return rtn

def module_hashes_as_string():
    """helper function that converts dict to str"""
    if len(secure_hashes)>1:
        txt = ""
        for fl, sha in get_module_hash_dictionary().iteritems():
            txt += "{0} ({1}), ".format(fl, sha)
        return txt[:-2]
    else:
        return ""

def cout_hashes():
    """helper function that prints hash information"""
    if get_experiment_secure_hash() is not None:
        print("Main file: {0} ({1})".format(main_file,
                            get_experiment_secure_hash()))
        if len(secure_hashes)>1:
            print "Modules: " + module_hashes_as_string()

# print hash information when imported
main_file = sys.argv[0]
secure_hashes = _make_hash_dict()
cout_hashes()
