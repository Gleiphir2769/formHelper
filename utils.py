import os
import sys

import pandas as pd


def correct_csv_garbled(file_list):
    for file in file_list:
        df = pd.read_csv(file, encoding='utf-8')
        df.to_csv(file, encoding='utf-8-sig', mode='w', index=False)


def items_dir(root_path):
    l = []
    for main_dir, dirs, file_name_list in os.walk(root_path):
        for file in file_name_list:
            file_path = os.path.join(main_dir, file)
            l.append(file_path)
    return l

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("ERR wrong number of arguments，")
        sys.exit(-1)
    root_path = sys.argv[1]
    file_list = items_dir(root_path)
    try:
        correct_csv_garbled(file_list)
    except:
        print("ERR unknown error, maybe files have be corrected.")