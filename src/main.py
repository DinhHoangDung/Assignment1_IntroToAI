from Node import Node, EMPTY, TREE, TENT
from Clue import Clue
from Searching import Searching
import time
from Utils import readInputFromFile, writeOutputToFile

def main():
    inputFile = readInputFromFile("../testcase/testcase1.txt")
    outputFile = open("../output.txt", "w")
    total = 0
    
    while True:
        print("\nChoose algorithm:")
        print("1. A* Search")
        print("2. Breadth First Search")
        choice = input("Enter your selection (1 or 2): ")
        
        if choice in ['1', '2']:
            break
        print("Invalid selection. Please select 1 or 2.")

    print("Loading...")
    for test_case in inputFile:
        start = time.time()
        clue, size, matrix = test_case
        srch = Searching(clue, size, matrix)
        
        if choice == '1':
            ans = srch.aStarSearch()
        else:
            ans = srch.breadthFirstSearch()
            
        end = time.time()
        writeOutputToFile(ans, outputFile, end - start)
        total = total + (end - start)
    
    outputFile.write("Total execution time:\n " + str(total) + "seconds\n")
    outputFile.write("-------------------------***-------------------------\n")
    outputFile.close()
    print("Done!")


if __name__ == "__main__":
    main()