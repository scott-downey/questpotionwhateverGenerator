#!/usr/bin/python3
import random
import argparse

parser = argparse.ArgumentParser(description='Load files and generate adventure!')
parser.add_argument('-l','--list', nargs='+', help='File pools', required=True)
parser.add_argument('-n','--number', type=int, help='Number of times a random entry should be created', default=1)
parser.add_argument('-s','--subfolder', help='Is used when the files are in a subfolder', default="")
args = parser.parse_args()


def loadFile(filename): # loads a file and makes a random choice
    with open("src/"+args.subfolder+filename) as file_in:
        lines = []
        line_weight = []
        for rawline in file_in:
            line = rawline.rstrip("\n")
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
        return ("{:<7} : {:<10}".format(elem, functionBound[0]))

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
