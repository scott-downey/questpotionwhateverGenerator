#!/usr/bin/python3
import random
import argparse
import re
import os
import sys

parser = argparse.ArgumentParser(description='Load files and generate adventure!')
parser.add_argument('-l','--list', nargs='+', help="""Takes a list of files. From those files random entries are selected. If no subfolder is specified the program
will search 'src' and if it doesn't find said file there it will look in 'general'""")
parser.add_argument('-n','--number', type=int, help="""Takes a number. Executes the program 'number' times.""", default=1)
parser.add_argument('-s','--subfolder', help='Takes subfolder. This allows you to specify a subfolder in src.', default="")
parser.add_argument('-m','--matchStarting', help='Allows the program to match all files starting with list-item text.', action='store_true', default=False)
args = parser.parse_args()
general_path = "src/general/"
def bold(str):
    return "\033[1m" + str + "\033[0m"

def rollDie(n, sides, modificator):
    summation = modificator
    for elem in range(int(n)):
        current = random.randint(1, int(sides))
        summation+=current
    return summation

def parseDie(text):
    modificator = 0
    arguments = text.split("-")
    if(len(arguments)>=2):
        for elem in arguments[1:]:
            modificator-=int(elem)
        text = arguments[0]
    else:
        arguments = text.split("+")
        if(len(arguments)>=2):
            for elem in arguments[1:]:
                modificator+=int(elem)
            text = arguments[0]
    if(text[0].isdigit()):
        values = text.lower().split("d")
        return rollDie(values[0],values[1], modificator)

def parse(text):
    if(text[0].isdigit()):   
        return parseDie(text)
    else:
        return getRListElement(text)

def findToParse(text):
    return re.sub(r"\{(.*?)\}|([0-9])+[dD]([0-9])+", lambda match: "{0}".format(parse(match.group().strip("{}"))), text)

def printError(filename):
    print(bold("general"))
    print('\n'.join(sorted([elem for elem in os.listdir(general_path) if args.list[0].lower() in elem.lower()], key=str.lower)))
    print("")
    print(bold("src/"+args.subfolder))
    print('\n'.join(sorted([elem for elem in os.listdir("src/"+args.subfolder) if args.list[0].lower() in elem.lower()], key=str.lower)))
    print("\nNeither general nor {} matched with {}. Partial matches with first list entry are shown above".format(args.subfolder, filename))
    sys.exit(0)

def printAll():
    print(bold("general"))
    print('\n'.join(sorted(os.listdir(general_path), key=str.lower)))
    print("")
    print(bold("src/"+args.subfolder))
    print('\n'.join(sorted(os.listdir("src/"+args.subfolder), key=str.lower)))

def loadFile(filename): # loads a file and makes a random choice
    filepath = "src/"+args.subfolder+filename
    if(not os.path.exists(filepath)):
        filepath = (general_path+filename)
    if(not os.path.exists(filepath)):
        printError(filename)
    with open(filepath) as file_in:
        lines = []
        line_weight = []
        for rawline in file_in:
            line = findToParse(rawline.rstrip("\n").strip(" "))
            splitted = line.split("|")
            if(len(splitted) == 1):
                lines.append(splitted[0])
                line_weight.append(100)
            else:
                lines.append(splitted[0])
                line_weight.append(int(splitted[1]))
    return random.choices(population=lines,weights=line_weight)[0]

def evaluate(elem, functionBound): # evaluates and creates string formating
    if(len(functionBound)>1): # is a function there? '_'
        return ("{:<7} : {:<10} - {}".format(elem,functionBound[0],doEntireListAsOne(functionBound[1:])))  
    else:
        return functionBound[0]

def getRListElement(elem):
    result=""
    result = loadFile(elem)
    functionBound = result.split("_")
    return evaluate(elem, functionBound)

def doEntireListAsOne(fileList): # does the entire list and creates the string in one line
    result = []
    for elem in fileList:
        result.append(getRListElement(elem))
    return " ".join(result)

def doEntireList(fileList): # does the entire list and adds one by one
    for elem in fileList:
        if(args.matchStarting):
            matches = [loadFile(file) for dirpath, dirnames, filenames in os.walk("src/"+args.subfolder) for file in filenames if file.lower().startswith(elem.lower())]
            if(matches):
                print('\n'.join(matches))
            else:
                printError(elem)
        else:
            print(getRListElement(elem))

def main():
    if(args.subfolder and not args.subfolder.endswith("/")):
        args.subfolder=args.subfolder+"/"
    if(args.list):
        for number in range(args.number):
            doEntireList(args.list)
    else:
        printAll()

if __name__ == "__main__":
    main()