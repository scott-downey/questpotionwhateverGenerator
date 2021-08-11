#!/usr/bin/python3
import random
import argparse
import re

parser = argparse.ArgumentParser(description='Load files and generate adventure!')
parser.add_argument('-l','--list', nargs='+', help='File pools', required=True)
parser.add_argument('-n','--number', type=int, help='Number of times a random entry should be created', default=1)
parser.add_argument('-s','--subfolder', help='Is used when the files are in a subfolder', default="")
args = parser.parse_args()

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
        values = text.split("d")
        return rollDie(values[0],values[1], modificator)

def parse(text):
    if(text[0].isdigit()):   
        return parseDie(text)
    else:
        return getRListElement(text)
    #raise ValueError("Brackets are for die roll only {2d6+2} for example is k {hans} is not.")

def findToParse(text):
    return re.sub(r"\{(.*?)\}", lambda match: "{0}".format(parse(match.group(1))), text)

def loadFile(filename): # loads a file and makes a random choice
    with open("src/"+args.subfolder+filename) as file_in:
        lines = []
        line_weight = []
        for rawline in file_in:
            line = findToParse(rawline.rstrip("\n"))
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
        print(getRListElement(elem))

def main():
    for number in range(args.number):
        doEntireList(args.list)

if __name__ == "__main__":
    main()