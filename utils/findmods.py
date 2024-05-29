import os
import re
from pathlib import Path

steam_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")

# find mods with this file
file = "99_background_graphics_buildings.txt"

def search_files(directory):
    found_files = []

    # Walk through the directory recursively
    for dirpath, _, filenames in os.walk(directory):

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            if os.path.isfile(file_path):
                relative_path = os.path.relpath(file_path, directory)
                found_files.append(relative_path)

    return found_files


files = search_files(steam_dir)

for each in files:
    if each.endswith(file):
        file_path = steam_dir / Path(each)
        desc = steam_dir / file_path.relative_to(steam_dir).parents[-2] / 'descriptor.mod'
        try:
            with open(desc) as f:
                c = f.read()
        except Exception as err:
            print(err)

        regex = r'name="([^"]+)"'
        match = re.search(regex, c)

        if match:
            name_value = match.group(1)
            print(name_value)
