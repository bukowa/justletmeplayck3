import os
from pathlib import Path

steam_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")


def file_path(mod_file_path):
    return steam_dir / Path(mod_file_path)


files = [
    "2712590542/gui/interaction_declare_war.gui",
    "3089046758/gui/interaction_declare_war.gui",
]


print([
    os.path.getmtime(file_path(f)) for f in files
])
