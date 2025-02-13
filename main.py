from Node import Node, EMPTY, TREE, TENT
from Clue import Clue
from Searching import Searching
import time
from Utils import readInputFromFile, writeOutputToFile

def main():
    inputs = readInputFromFile("input.txt")
    outputFile = open("output.txt", "w")
    print("Loading...")
    for input in inputs:
        start = time.time()
        clue, size, matrix = input
        srch = Searching(clue, size, matrix)
        ans = srch.aStarSearch()
        #ans = srch.breadthFirstSearch()
        end = time.time()
        writeOutputToFile(ans, outputFile, end - start)
    outputFile.close()
    print("Done!")


if __name__ == "__main__":
    main()