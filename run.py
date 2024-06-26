import itertools
import json
import os
from pathlib import Path

steam_dir = Path(r"C:\Program Files (x86)\Steam\steamapps\workshop\content\1158310")


def mod_dir(mod_path):
    return steam_dir / Path(mod_path)


with open('modlist.json') as f:
    x = sorted(json.load(f)['mods'], key=lambda d: d['position'])

with open('modlist.json', 'r+') as f:
    obj = json.load(f)
    f.seek(0); f.truncate()
    json.dump(obj, f, indent='\t')


unique = {}
for mod in x:
    if unique.get(mod['steamId']):
        raise Exception(mod['steamId'])
    unique[mod['steamId']] = True


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


def filter_out_file(_f):
    _p = Path(_f)
    if '.git' in _p.parts:
        return False
    if any(__p.endswith('.md') for __p in _p.parts):
        return False
    if _p.parents[0].name == '.git':
        return False
    if _f.lower() in [
        'descriptor.mod',
        'thumbnail.png',
        '.gitattributes',
        'gui\\toolspropertytypes.gui',
        'gui\\tool_property_randomizable_types.gui'
    ]:
        return False
    if _f.endswith('.info'):
        return False
    return True


for i, mod in enumerate(x):
    mod['files'] = search_files(mod_dir(mod['steamId']))
    mod['files'] = list(filter(filter_out_file, mod['files']))
    x[i] = mod

count = {}
[count.update({_f: count.get(_f, 0) + 1}) for _mod in x for _f in _mod['files']]
count_sorted = dict(sorted(count.items(), key=lambda item: item[1], reverse=True))
count_modified = dict(filter(lambda item: item[1] > 1, count_sorted.items()))

count_final = list(map(lambda _f: {
    'file': _f[0],
    'count': _f[1],
    'mods': [],
}, count_modified.items()))

count_modified_list = list(count_modified.keys())

for mod in x:
    for f in mod['files']:
        if count_modified.get(f):
            iof = count_modified_list.index(f)

            cmods = count_final[iof]['mods']
            cmods.append(mod['displayName'])
            count_final[iof]['mods'] = cmods

            csteamIds = count_final[iof].get('steamIds', [])
            csteamIds.append(mod['steamId'])
            count_final[iof]['steamIds'] = csteamIds


with open('rules.json') as f:
    rules = json.load(f)


# modify rules, instead of implementing
# algorithm for matching cuz I am lazy for now
for rule in rules[:]:
    new_rules = []
    for i in range(1, len(rule) + 1):
        new_rules.append(rule[:i])
    rules.extend(new_rules)


count_final_dict = dict(enumerate(count_final))


with open('rules_filemodifiedtime.json') as f:
    rules_filemodifiedtime = json.load(f)


for i, f in enumerate(count_final[:]):

    for rule in rules:

        # exact rule match
        if f['mods'] == rule:
            count_final_dict.pop(i)
            break

    for rule in rules_filemodifiedtime:

        if f['mods'] == rule['mods']:

            for mindex, mtime in enumerate(rule['modified']):
                if mtime == '':
                    continue
                mtime = float(mtime)
                fmfile = mod_dir(f['steamIds'][mindex]) / Path(f['file'])
                fmtime = os.path.getmtime(fmfile)

                if fmtime != mtime:
                    raise Exception([rule, f"bad modified time: {mtime} != {fmtime}"])

            count_final_dict.pop(i)


with open('conflict.json', 'w') as f:
    json.dump(count_final_dict, f, indent='\t')
