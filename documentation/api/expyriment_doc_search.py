from __future__ import print_function
import expyriment
from pydoc import getdoc
x = None
y = None


def _get_doc_and_function(obj):
    rtn = []
    for var in dir(obj):
        if not var.startswith("_"):
            rtn.append(var)
    return getdoc(obj), rtn

def _read_module(mod, doc_dict):
    doc_dict[mod.__name__], classes = _get_doc_and_function(mod)
    for cl in classes:
        cl = "{0}.{1}".format(mod.__name__, cl)
        exec("x =" + cl)
        doc_dict[cl], functions = _get_doc_and_function(x)
        for fnc in functions:
            fnc = "{0}.{1}".format(cl, fnc)
            exec("y =" + fnc)
            doc_dict[fnc], _tmp = _get_doc_and_function(y)

def search_doc(search_str, doc_dict):

    for k in doc_dict.keys():
        if k.lower().find(search_str.lower()) > 0 or\
            doc_dict[k].lower().find(search_str.lower()) > 0:
            print("\n-------------------------------------------------------------------------------")
            print("[ {0} ]\n".format(k))
            #print "-------------------------------------------------------------------------------"
            print("{0}".format(doc_dict[k]))



doc_dict = {}
_read_module(expyriment.io, doc_dict)
_read_module(expyriment.stimuli, doc_dict)
_read_module(expyriment.design, doc_dict)
_read_module(expyriment.misc, doc_dict)

while True:
    search = raw_input("New search (q=quit): ")
    if search == "q":
        break
    else:
        search_doc(search, doc_dict)
        print("\n")

