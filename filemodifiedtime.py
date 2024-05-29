import os
from pathlib import Path

steam_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")


def file_path(mod_file_path):
    return steam_dir / Path(mod_file_path)


files = [
    "2507209632\\gui\\window_character.gui",
    "2797936557\\gui\\window_character.gui",
]


print([
    os.path.getmtime(file_path(f)) for f in files
])
