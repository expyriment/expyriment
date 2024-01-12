import os
import sys
from datetime import datetime

p = os.path.abspath(os.path.join(os.path.split(sys.argv[0])[0]))
sys.path.insert(0, p)

from expyriment import __version__

def replace_changes_version_number(changes_file = "CHANGES.md",
                                   upcoming_tag="Coming up"):
    search_tag = True
    version_str = f"{__version__} ({datetime.today().strftime('%d %b %Y')})"
    bkp_file = changes_file +".bak"

    try:
        os.remove(bkp_file)
    except FileNotFoundError:
        pass
    os.rename(changes_file, bkp_file)

    with open(changes_file, 'w') as flb:
        with open(bkp_file, 'r') as fla:
            for l in fla:
                if search_tag and (l.startswith(upcoming_tag) or l.find(".dev")>=0):
                    flb.write(f"{version_str}\n")
                    search_tag = False
                else:
                    if l.startswith("------"):
                        flb.write("-"*len(version_str)+"\n")
                        search_tag = True
                    else:
                        flb.write(l)



if __name__ == "__main__":
    replace_changes_version_number()
    #os.rename(bkp, CHANGES)
