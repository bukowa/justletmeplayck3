import os
from pathlib import Path

steam_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")


def file_path(mod_file_path):
    return steam_dir / Path(mod_file_path)


files = [
    "2975514448\\common\\on_action\\travel_on_actions.txt",
    "3082182371\\common\\on_action\\travel_on_actions.txt",
]


print([
    os.path.getmtime(file_path(f)) for f in files
])
