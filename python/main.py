import re
import os
import sys
import yaml
import logging
import argparse
import collections

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--flypy', help='flypy_chars.dict.yaml file path', required=True)
    parser.add_argument('-t', '--tiger', help='tiger.dict.yaml file path', required=True)
    args = parser.parse_args()
    return args

def get_tiger_dict(tiger_file):
    tiger_dict = collections.OrderedDict()
    with open(tiger_file, 'r', encoding='utf-8') as f:
        for line in f.readlines()[11:]:
            line = line.strip()
            if not line:
                continue
            line_list = line.split()
            # if list[1] is longer than 2, cut it
            if len(line_list[1]) > 2:
                line_list[1] = line_list[1][:2]
            tiger_dict[line_list[0]] = line_list[1]
    return tiger_dict

def get_flypy_dict(flypy_file):
    flypy_dict = collections.OrderedDict()
    flypy_frequency = []
    with open(flypy_file, 'r', encoding='utf-8') as f:
        for line in f.readlines()[11:]:
            line = line.strip()
            if not line:
                continue
            line_list = line.split()
            flypy_dict[line_list[0]] = line_list[1]
            # save frequency of flypy to a list
            flypy_frequency.append(line_list[2])
    return flypy_dict, flypy_frequency

def transfer(flypy_dict, tiger_dict):
    for flypy_key, flypy_value in flypy_dict.items():
        flypy_value_list = flypy_value.split(';')
        if len(flypy_value_list) != 2:
            continue
        flypy_value_list[1] = tiger_dict.get(flypy_key, '')
        flypy_dict[flypy_key] = ';'.join(flypy_value_list)
    return flypy_dict

def write_to_file(flypy_dict, flypy_file):
    with open(flypy_file, 'w', encoding='utf-8') as f:
        for flypy_key, flypy_value in flypy_dict.items():
            f.write(f'{flypy_key}\t{flypy_value}\n')

# write to a new file instead of the original file
def write_to_new_file(flypy_dict, flypy_file, flypy_frequency):
    flypy_file_path = os.path.dirname(flypy_file)
    flypy_file_name = os.path.basename(flypy_file)
    flypy_file_name_list = flypy_file_name.split('.')
    flypy_file_name_list.insert(-1, 'new')
    flypy_file_name = '.'.join(flypy_file_name_list)
    flypy_file = os.path.join(flypy_file_path, flypy_file_name)
    with open(flypy_file, 'w', encoding='utf-8') as f:
        for flypy_key, flypy_value in flypy_dict.items():
            frequency = flypy_frequency.pop(0)
            f.write(f'{flypy_key}\t{flypy_value}\t{frequency}\n')


def main():
    args = get_args()
    # flypy_dict = get_flypy_dict(args.flypy)
    flypy_dict, flypy_frequency = get_flypy_dict(args.flypy)
    tiger_dict = get_tiger_dict(args.tiger)
    flypy_dict = transfer(flypy_dict, tiger_dict)
    write_to_new_file(flypy_dict, args.flypy, flypy_frequency)
    # write_to_file(flypy_dict, args.flypy)

if __name__ == '__main__':
    main()
