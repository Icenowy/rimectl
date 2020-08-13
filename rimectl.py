#! /usr/bin/python3

import argparse
import os
import os.path
import sys
import yaml

installations = {
    "fcitx": "{home}/.config/fcitx/rime"
}

def format_rime_installation():
    for inst in installations:
        installations[inst] = installations[inst].format(home = os.getenv("HOME"))

def detect_rime_installation():
    ret = set()
    for inst in installations:
        path = installations[inst] + "/installation.yaml"
        if os.path.isfile(path):
            ret.add(inst)

    return ret

def flush_schema_list(schema_list):
    custom_yaml_file = None
    if os.path.isfile(installations[target_installation] + "/build/default.custom.yaml"):
        custom_yaml_file = open(installations[target_installation] + "/build/default.custom.yaml", "r")
    if custom_yaml_file != None:
        custom_yaml = yaml.load(custom_yaml_file, Loader = yaml.FullLoader)
    else:
        custom_yaml = dict()

    custom_yaml["schema_list"] = list()
    for i in schema_list:
        custom_yaml["schema_list"].append({"schema": i})

    custom_yaml_file = open(installations[target_installation] + "/build/default.custom.yaml", "w")
    yaml.dump(custom_yaml, custom_yaml_file)
    custom_yaml_file.close()

format_rime_installation()
existing_installations = detect_rime_installation()

argparser = argparse.ArgumentParser(description = 'Rime installation configurator.')

argparser.add_argument('--list-installation', action = 'store_true', help = 'Listing installed Rime installations of this user.')
argparser.add_argument('-I', '--installation', nargs = 1, help = 'Specify the installation that the program will operate on.')
argparser.add_argument('-l', '--list', action = 'store_true', help = 'Listing currently enabled schemas.')
argparser.add_argument('-L', '--list-available', action = 'store_true', help = 'Listing available schemas.')

args = argparser.parse_args()

if args.list_installation:
    for i in existing_installations:
        print(i)

target_installation = args.installation

if (len(existing_installations) > 1):
    if target_installation == None:
        sys.exit("Multiple Rime installation found, please specify one with --installation.")
elif (len(existing_installations) < 1):
    sys.exit("No Rime installation found.")
else:
    if target_installation == None:
        target_installation = existing_installations.copy().pop()

# Reading back the original schema list
original_schema_list_yaml_file = None
if os.path.isfile(installations[target_installation] + "/build/default.custom.yaml"):
    original_schema_list_yaml_file = open(installations[target_installation] + "/build/default.custom.yaml", "r")
if original_schema_list_yaml_file == None:
    if os.path.isfile(installations[target_installation] + "/build/default.yaml"):
        original_schema_list_yaml_file = open(installations[target_installation] + "/build/default.yaml", "r")
if original_schema_list_yaml_file == None:
    sys.exit("Cannot find the file that contains the current enabled schema list!")

original_schema_list_yaml = yaml.load(original_schema_list_yaml_file, Loader = yaml.FullLoader)
original_schema_list_yaml_file.close()

original_schema_list = list()

for i in original_schema_list_yaml["schema_list"]:
    original_schema_list.append(i["schema"])

schema_list = original_schema_list

if args.list:
    noop = False
    for i in schema_list:
        print(i)
    sys.exit(0)

if args.list_available:
    True

argparser.print_help()
sys.exit(1)
