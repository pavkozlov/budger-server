import re


def name_str_to_dict(s):
    m = re.search('(.+ .+ .+?) - (.+)', s)
    return {'name': m.group(1), 'position': m.group(2)} if m else s
