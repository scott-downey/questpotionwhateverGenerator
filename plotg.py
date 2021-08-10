#!/usr/bin/python3
import random
import argparse

parser = argparse.ArgumentParser(description='Load files and generate adventure!')
parser.add_argument('-l','--list', nargs='+', help='File pools', required=True)
args = parser.parse_args()


def loadFile(filename):
    with open("src/"+filename) as file_in:
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

def evaluate(elem, functionBound):
    if(len(functionBound)>1):
        return ("{:<7} : {:<10} - {}".format(elem,functionBound[0],doEntireListAsOne(functionBound[1:])))  
    else:
        return ("{:<7} : {:<10}".format(elem, functionBound[0]))

def getRListElement(elem):
    result = loadFile(elem)
    functionBound = result.split("_")
    return evaluate(elem, functionBound)

def doEntireListAsOne(fileList):
    result = []
    for elem in fileList:
        result.append(getRListElement(elem))
    return " ".join(result)

def doEntireList(fileList):
    for elem in fileList:
        print(getRListElement(elem))

def main():
    doEntireList(args.list)

if __name__ == "__main__":
    main()
