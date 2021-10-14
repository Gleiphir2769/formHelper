import json
import os
import sys


def json_read(filename):
    if os.path.exists(filename):
        if sys.version_info.major > 2:
            f = open(filename, 'r', encoding='utf-8')
        else:
            f = open(filename, 'r')
        dict_data = json.load(f)

        return dict_data

if __name__ == '__main__':
    dd = json_read("config.json")
    print(dd)
