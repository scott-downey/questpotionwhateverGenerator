#!/usr/bin/python3
import random
import argparse
import re
import os
import sys

parser = argparse.ArgumentParser(description='Load files from folder and prepares them for plotg.py!')
parser.add_argument('-f','--folder', help='The folder from which all files are taken recursively (this means: It will access subfolders!)', required=True)
#parser.add_argument('-n','--keepNumbers', help='Keeps numbers at the beginning', action='store_true')
#parser.add_argument('-s','--keepSpaces', help='Keeps trailing and leading spaces', action='store_true')
#parser.add_argument('-e','--keepEnumeration', help='Keeps leading 0123456789.-', action='store_true')
#parser.add_argument('-t','--keepTabs', help='If set tabs will be kept. Otherwise tabs will be replaced by newlines', action='store_true')
#parser.add_argument('-k','--keepDuplicates', help='Will keep duplicates', action='store_true')
args = parser.parse_args()

newlist = []
files = []

def main():
    for path, subdirs, files in os.walk(args.folder):
        print("All files found:",files)
        if(input("Ok? Write 'yes'. Files will be overriden! ") == "yes"):
            for name in files:
                with open(os.path.join(path, name),'r') as file_in:
                    newlist = [word.lstrip('0123456789.-').strip(' \n') for line in file_in for word in line.split("\t")]
                with open(os.path.join(path, name),'w') as file_in:
                    file_in.write("\n".join(set(newlist)))
    print("Done! {} rewritten 'nd ready to go!".format(len(files)))

if __name__ == "__main__":
    main()
