#!/usr/bin/env python

"""
The Expyriment documentation

This script contains an API reference browser and search GUI interface (TK), as
well as a function to call this browser or the online documentation.

"""

__author__ = 'Florian Krause <florian@expyriment.org> \
Oliver Lindemann <oliver@expyriment.org>'
__version__ = ''
__revision__ = ''
__date__ = ''


import os
import sys
from pydoc import getdoc as _getdoc
import inspect as _inspect
from types import ModuleType, MethodType, FunctionType

import expyriment
from ._internals import get_version


try:
    import tkinter as _tk  # future (Python 3)
except Exception:
    _tk = None

try:
    import tkinter.ttk as _ttk
    # for OS X, if there is no Tile support
    _root = _ttk.Tk()
    _root.destroy()
except Exception:
    _ttk = _tk  # for Python < 2.7 # TODO Python 3 support only

def _get_doc_and_function(obj):
    rtn = []
    for var in dir(obj):
        if not var.startswith("_"):
            rtn.append(var)
    return _getdoc(obj), rtn

def _read_module(mod, doc_dict):
    doc_dict[mod.__name__], classes = _get_doc_and_function(mod)

    p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0], '..'))
    sys.path.insert(0, p)

    import expyriment
    namespace = locals()
    for cl in classes:
        cl = "{0}.{1}".format(mod.__name__, cl)
        exec("_x =" + cl, namespace)
        doc_dict[cl], functions = _get_doc_and_function(namespace['_x'])
        for fnc in functions:
            fnc = "{0}.{1}".format(cl, fnc)
            exec("_y =" + fnc, namespace)
            doc_dict[fnc], _tmp = _get_doc_and_function(namespace['_y'])

def _search_doc(search_str, doc_dict):
    """Search the documentation.

    Parameters
    ----------
    search_str : string
        string to search for (str)
    doc_dict : dict
        documentation dict to search in(dict

    """

    rtn = []
    for k in list(doc_dict.keys()):
        if k.lower().find(search_str.lower()) > -1 or\
            doc_dict[k].lower().find(search_str.lower()) > -1:
            rtn.append(k)
    return rtn

def _get_members(item_str):
    members = []
    for member in _inspect.getmembers(eval(item_str)):
        if not member[0].startswith("_"):
            members.append(item_str + "." + member[0])
    return members

def show_GUI():
    """Show the GUI."""

    from types import ModuleType
    import expyriment
    import expyriment.io.extras
    import expyriment.design.extras
    import expyriment.stimuli.extras
    import expyriment.misc.extras

    if not isinstance(_tk, ModuleType):
        raise ImportError("""API Reference Tool could not be started.
The Python package 'Tkinter' is not installed""")

    # Create the documentation dict
    doc_dict = {}
    _read_module(expyriment, doc_dict)
    _read_module(expyriment.control, doc_dict)
    _read_module(expyriment.design, doc_dict)
    _read_module(expyriment.design.extras, doc_dict)
    _read_module(expyriment.misc, doc_dict)
    _read_module(expyriment.misc.extras, doc_dict)
    _read_module(expyriment.misc.data_preprocessing, doc_dict)
    _read_module(expyriment.io, doc_dict)
    _read_module(expyriment.io.extras, doc_dict)
    _read_module(expyriment.stimuli, doc_dict)
    _read_module(expyriment.stimuli.extras, doc_dict)

    # Create e root window
    root = _tk.Tk()
    root.title("Expyriment ({0}) API Reference Tool".format(
        expyriment.__version__))
    root.minsize(996, 561)

    # Create the GUI elements
    left_frame = _ttk.Frame(root)
    search_frame = _ttk.Frame(left_frame)
    label = _ttk.Label(search_frame, text="Search:")

    search_text = _tk.StringVar()
    entry = _ttk.Entry(search_frame, textvariable=search_text, takefocus=0)
    entry.delete(0, _tk.END)

    list_frame_outer = _ttk.Frame(left_frame)
    list_frame_inner = _ttk.Frame(list_frame_outer)
    listbox = _tk.Listbox(list_frame_inner, width=40, font=("Courier", 10,
                                                           "bold"))
    scroll1 = _ttk.Scrollbar(list_frame_inner, orient=_tk.HORIZONTAL, takefocus=0)
    scroll1.config(command=listbox.xview)
    listbox.configure(xscrollcommand=scroll1.set)
    scroll2 = _ttk.Scrollbar(list_frame_outer, takefocus=0)
    scroll2.config(command=listbox.yview)
    listbox.configure(yscrollcommand=scroll2.set)

    right_frame = _ttk.Frame(root)
    text_frame_outer = _ttk.Frame(right_frame)
    text_frame_inner = _ttk.Frame(text_frame_outer)
    text = _tk.Text(text_frame_inner, width=80, background='white',
                   font=("Courier", 10), wrap=_tk.NONE, state=_tk.DISABLED,
                   takefocus=1)
    scroll3 = _ttk.Scrollbar(text_frame_inner, orient=_tk.HORIZONTAL, takefocus=0)
    scroll3.config(command=text.xview)
    text.configure(xscrollcommand=scroll3.set)
    scroll4 = _ttk.Scrollbar(text_frame_outer, takefocus=0)
    scroll4.config(command=text.yview)
    text.configure(yscrollcommand=scroll4.set)

    def update_search(_event):
        """Update the search.

        This will update the list of found items after each typed letter.

        Parameters
        ----------
        _event : dummy
            dummy argument, necessary for callbacks

        """

        global last_sel
        listbox.delete(0, _tk.END)
        value = search_text.get()
        if value == "":
            items = ["expyriment", ]
        else:
            items = _search_doc(value, doc_dict)
        for index, item in enumerate(items):
            if isinstance(eval(item), ModuleType):
                items[index] = "# " + item
            elif isinstance(eval(item), type): ##
                items[index] = "+ " + item
            elif isinstance(eval(item), MethodType):
                items[index] = "- " + item
            elif isinstance(eval(item), FunctionType):
                items[index] = "= " + item
            else:
                items[index] = "@ " + item
        items = sorted(items)
        if items == []:
            text.config(state=_tk.NORMAL)
            text.delete(1.0, _tk.END)
            text.config(state=_tk.DISABLED)
            last_sel = None
        for index, item in enumerate(items):
            listbox.insert(_tk.END, item)
            if isinstance(eval(item[2:]), (type, ModuleType)):
                listbox.itemconfig(index, fg="blue", selectforeground="blue")
        listbox.selection_set(_tk.ACTIVE)
        return True

    def poll():
        """Poll the GUI.

        This will update the documentation according to the selected item.

        """

        global last_sel
        text.after(100, poll)
        sel = listbox.curselection()
        if sel != ():
            item = listbox.get(int(sel[0]))
            if last_sel != item:
                last_sel = item
                if item == "..":
                    text.config(state=_tk.NORMAL)
                    text.delete(1.0, _tk.END)
                    text.config(state=_tk.DISABLED)
                if item != "..":
                    item = item[2:]
                    text.config(state=_tk.NORMAL)
                    text.delete(1.0, _tk.END)
                    text.tag_config("heading", font=("Courier", 12, "bold"))
                    text.insert(_tk.END, item, "heading")
                    text.insert(_tk.END, "\n\n")
                    if isinstance(eval(item), type):
                        text.insert(_tk.END, doc_dict[item])
                        definition = "".join(_inspect.getsourcelines(
                            eval(item))[0])
                        start = definition.find("def __init__(self") + 17
                        end = definition.find(")", start)
                        if definition[start] == ",":
                            call = "(" + \
                                    definition[start + 1:end].lstrip() + ")"
                        else:
                            call = "()"
                        call = call.replace(" " * 16,
                                            " " * len(item.split(".")[-1]))
                        text.insert(_tk.END, "\n\n\n\n")
                        text.tag_config("item",
                                        font=("Courier", 10, "bold"))
                        text.tag_config("call", font=("Courier", 10,
                                                      "italic"))
                        text.insert(_tk.END, item.split(".")[-1], "item")
                        text.insert(_tk.END, call, "call")
                        text.insert(_tk.END, "\n\n")
                        text.insert(_tk.END, _getdoc(
                            eval(item + "." + "__init__")))
                    elif isinstance(eval(item), FunctionType):
                        definition = "".join(_inspect.getsourcelines(
                            eval(item))[0])
                        text.tag_config("item",
                                        font=("Courier", 10, "bold"))
                        start = definition.find("(") + 1
                        end = definition.find(")", start)
                        call = "(" + definition[start:end].lstrip() + ")"
                        call = call.replace(
                            "    " + " "*len(item.split(".")[-1]) + " ",
                            " "*len(item.split(".")[-1] + " "))
                        text.tag_config("call", font=("Courier", 10, "italic"))
                        text.insert(_tk.END, item.split(".")[-1], "item")
                        text.insert(_tk.END, call, "call")
                        text.insert(_tk.END, "\n\n")
                        text.insert(_tk.END, doc_dict[item])
                    elif isinstance(eval(item), MethodType):
                        definition = "".join(_inspect.getsourcelines(
                            eval(item))[0])
                        text.tag_config("item",
                                        font=("Courier", 10, "bold"))
                        start = definition.find("(self") + 1
                        end = definition.find(")", start)
                        if definition[start + 4] == ",":
                            call = "(" + \
                                    definition[start + 5:end].lstrip() + ")"
                        else:
                            call = "()"
                        call = call.replace(
                            "        " + " "*len(item.split(".")[-1]) + " ",
                            " "*len(item.split(".")[-1]) + " ")
                        text.tag_config("call", font=("Courier", 10, "italic"))
                        text.insert(_tk.END, item.split(".")[-1], "item")
                        text.insert(_tk.END, call, "call")
                        text.insert(_tk.END, "\n\n")
                        text.insert(_tk.END, doc_dict[item])
                    elif isinstance(eval(item), (int, bytes,bool, list,
                                              tuple, dict)):
                        pass
                    else:
                        if isinstance(eval(item), property):
                            if eval(item).fset is None:
                                text.insert(_tk.END, "Read-only!")
                        else:
                            text.insert(_tk.END, doc_dict[item])

                    text.config(state=_tk.DISABLED)

    def member_list(_event, member=None):
        """Show a list of members of an item.

        This will show_GUI the list of all members (modules, classes, methods, ...)
        for a given item. If no item is given, it will take the currently
        selected one.

        Parameters
        ----------
        _event : dummy
            dummy argument, necessary for callbacks
        member : string, optional
            item to show_GUI members for

        """

        global last_item
        if member is not None:
            item = member
        else:
            try:
                item = listbox.get(int(listbox.curselection()[0]))
                if item == "..":
                    tmp = item = last_item
                else:
                    item = item[2:]
                    tmp = item
                if item == "":
                    update_search(None)
                else:
                    if isinstance(eval(item), (type, ModuleType)):
                        s = tmp.split(".")
                        if len(s) >= 1:
                            last_item = ".".join(s[0:-1])
                        else:
                            last_item = None
                        items = _get_members(item)
                        items.insert(0, "..")
                        entry.delete(0, _tk.END)
                        listbox.delete(0, _tk.END)
                        for index, item in enumerate(items):
                            if item != "..":
                                if isinstance(eval(item), ModuleType):
                                    items[index] = "# " + item
                                elif isinstance(eval(item), type):
                                    items[index] = "+ " + item
                                elif isinstance(eval(item), MethodType):
                                    items[index] = "- " + item
                                elif isinstance(eval(item), FunctionType):
                                    items[index] = "= " + item
                                else:
                                    items[index] = "@ " + item
                        tmp = items
                        items = []
                        items.append(tmp[0])
                        items.extend(sorted(tmp[1:]))
                        for index, item in enumerate(items):
                            listbox.insert(_tk.END, item)
                            if item == ".." or \
                                    isinstance(eval(item[2:]), (type, ModuleType)):
                                listbox.itemconfig(index, fg="blue",
                                                   selectforeground="blue")
                        listbox.selection_set(0)
            except Exception:
                pass

    # Position the GUI elements
    left_frame.pack(side=_tk.LEFT, expand=1, fill=_tk.BOTH)
    search_frame.pack(side=_tk.TOP, fill=_tk.BOTH)
    label.pack(side=_tk.LEFT)
    entry.pack(side=_tk.LEFT, expand=1, fill=_tk.X)
    list_frame_outer.pack(side=_tk.BOTTOM, expand=1, fill=_tk.BOTH)
    list_frame_inner.pack(side=_tk.LEFT, expand=1, fill=_tk.BOTH)
    listbox.pack(side=_tk.TOP, expand=1, fill=_tk.BOTH)
    scroll1.pack(side=_tk.BOTTOM, fill=_tk.X)
    scroll2.pack(side=_tk.LEFT, fill=_tk.Y)
    right_frame.pack(side=_tk.RIGHT, expand=2, fill=_tk.BOTH)
    text_frame_outer.pack(side=_tk.BOTTOM, expand=2, fill=_tk.BOTH)
    text_frame_inner.pack(side=_tk.LEFT, expand=2, fill=_tk.BOTH)
    text.pack(side=_tk.TOP, expand=2, fill=_tk.BOTH)
    scroll3.pack(side=_tk.BOTTOM, fill=_tk.X)
    scroll4.pack(side=_tk.LEFT, fill=_tk.Y)

    # Create Keybindings
    root.bind("<Control-f>", lambda x: entry.focus())
    root.bind("<Control-q>", lambda x: root.quit())
    root.bind("<F1>", lambda x: show_help())
    listbox.bind("<Double-Button-1>", member_list)
    listbox.bind("<Return>", member_list)
    entry.bind("<KeyRelease>", update_search)

    def show_about():
        """Show the about dialogue window"""

        aboutdialogue = _tk.Toplevel(root, padx=5, pady=5)
        aboutdialogue.title("About")
        aboutdialogue.transient(root)
        aboutdialogue.grab_set()
        aboutdialogue.focus_set()
        aboutdialogue.bind("<Button-1>", lambda x: aboutdialogue.destroy())
        aboutdialogue.bind("<Escape>", lambda x: aboutdialogue.destroy())
        aboutdialogue.bind("<Return>", lambda x: aboutdialogue.destroy())
        aboutlabel1 = _ttk.Label(aboutdialogue,
                               text="Expyriment API Reference Tool",
                               font=("Arial", "15", "bold"))
        aboutlabel1.pack()
        aboutlabel2 = _ttk.Label(aboutdialogue,
                               text="Expyriment {0}".format(
                                   expyriment.get_version()),
                               font=("Arial", "8", "italic"))
        aboutlabel2.pack()
        aboutlabel3 = _ttk.Label(aboutdialogue,
                               text="",
                               font=("Arial", "11"))
        aboutlabel3.pack()
        aboutlabel4 = _ttk.Label(aboutdialogue,
                        text="Florian Krause <florian@expyriment.org>",
                               font=("Arial", "9"))
        aboutlabel4.pack()
        aboutlabel5 = _ttk.Label(aboutdialogue,
                        text="Oliver Lindemann <oliver@expyriment.org>",
                               font=("Arial", "9"))
        aboutlabel5.pack()

    def show_help():
        """Show the help dialogue window"""

        helpdialogue = _tk.Toplevel(root, width=200, height=300, padx=5,
                                   pady=5)
        helpdialogue.title("Help Contents")
        helpdialogue.transient(root)
        helpdialogue.grab_set()
        helpdialogue.bind("<Escape>", lambda x: helpdialogue.destroy())
        helpdialogue.bind("<Return>", lambda x: helpdialogue.destroy())

        helpframe = _ttk.Frame(helpdialogue)
        helpframe.pack()
        helptextbox = _tk.Text(helpframe, highlightthickness=0, wrap=_tk.WORD,
                               font=("Courier", 10))
        documentation = """The Expyriment API Reference Tool allows you to browse and search the Expyriment API.

Double clicking on blue coloured items will show their content.
Double clicking on ".." will go up one level.

The search is instant, which means every typed letter will update the results immediately.

The following symbols are used to denote the type of an item:

    # Module
    + Class
    - Method
    = Function
    @ Attribute"""
        helptextbox.insert('1.0', documentation)
        helptextbox.pack(side=_tk.LEFT)
        helptextbox.focus_set()
        scrollbar = _ttk.Scrollbar(helpframe, takefocus=False,
                                 command=helptextbox.yview)
        scrollbar.pack(side=_tk.RIGHT, fill=_tk.Y)
        helptextbox.config(state=_tk.DISABLED,
                           yscrollcommand=scrollbar.set)
        closebutton = _ttk.Button(helpdialogue, text="Close",
                                takefocus=_tk.FALSE,
                                command=helpdialogue.destroy)
        closebutton.pack()

    # Create a menu
    menubar = _tk.Menu(root)
    filemenu = _tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Quit", command=root.quit, accelerator="Ctrl+Q")
    menubar.add_cascade(label="File", menu=filemenu)
    helpmenu = _tk.Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Contents", command=show_help, accelerator="F1")
    helpmenu.add_command(label="About", command=show_about)
    menubar.add_cascade(label="Help", menu=helpmenu)

    root.config(menu=menubar)

    # Start the main loop
    global last_item
    last_item = None
    update_search(None)

    global last_sel
    last_sel = None
    poll()

    entry.focus()

    _tk.mainloop()


def show_documentation(docu_type=None):
    """Show the Expyriment documentation.


    Parameters
    ----------
    docu_type : int
        the documentation type:
        1 = open online documentation
        2 = open online API reference
        3 = open API reference and search tool

    """

    def call_info():
        print("")
        print("Call show_documentation with the following arguments to get further information:")
        print("     show_documentation(1) -- Open online documentation in web browser")
        print("     show_documentation(2) -- Open API Reference Tool")
        print("")

    import subprocess
    import os
    import sys
    import webbrowser

    f = os.path.abspath(__file__)
    path = os.path.abspath(os.path.join(os.path.split(f)[0], ".."))
    if docu_type is None:
        print("Welcome to Expyriment {0}".format(get_version()))
        print("")
        author = __author__.replace(",", ",\n        ")
        print("Website: http://expyriment.org")
        print("License: GNU GPL v3")
        print("Authors: {0}".format(author))
        call_info()
    elif docu_type == 1:
        webbrowser.open(
            "http://docs.expyriment.org/",
            new=1)
    elif docu_type == 2:
        python_executable = sys.executable.replace("pythonw.exe", "python.exe")
        call = '"' + "{0}".format(python_executable) + \
                '" -m expyriment._api_reference_tool'
        _proc = subprocess.Popen(
            call,
            shell=True,
            stdin=None,
            stdout=None,
            cwd=path)
    else:
        print("Unknown documentation type")
        call_info()

if __name__ == "__main__":
    show_GUI()
