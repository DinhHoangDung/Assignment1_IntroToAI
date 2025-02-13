from Node import Node, EMPTY, TREE, TENT
from Clue import Clue
import copy

def generateNextNodes(curNode: Node, clue: Clue):
    rtNodes = []

    for i in range(curNode.size):
        if curNode.curTentsRow[i] == clue.rowClue[i]:
            continue
        for j in range(curNode.size):
            if curNode.curTentsCol[j] == clue.colClue[j]:
                continue
            if canAssignTent(curNode, (i, j)):
                nextNode = Node(curNode.size, copy.deepcopy(curNode.state), curNode)
                nextNode.assignTentTo((i, j))
                rtNodes.append(nextNode)

    return rtNodes


def canAssignTent(curNode, position: tuple):
    rowIdx, colIdx = position

    if curNode.state[rowIdx][colIdx] != EMPTY:
        return False

    lowRow = max(0, rowIdx - 1)
    upperRow = min(curNode.size, rowIdx + 2)
    lowCol = max(0, colIdx - 1)
    upperCol = min(curNode.size, colIdx + 2)
    havingTrees = False
    curState = curNode.state

    for i in range(lowRow, upperRow):
        for j in range(lowCol, upperCol):
            if i == rowIdx or j == colIdx:
                if curState[i][j] == TREE:
                    havingTrees = True
                if curState[i][j] == TENT:
                    return False
            elif curState[i][j] == TENT:
                return False

    return havingTrees

def haveOneToOne(idx, pairedTrees: set, tentToTrees: dict, tentsPos: list):
    if idx == len(tentToTrees):
        return True

    trees = tentToTrees.get(tentsPos[idx])
    for treeIdx in range(len(trees)):
        tree = trees[treeIdx]
        if tree not in pairedTrees:
            pairedTrees.add(tree)
            if haveOneToOne(idx + 1, pairedTrees, tentToTrees, tentsPos):
                return True
            pairedTrees.remove(tree)
    return False

def readInputFromFile(filename):
    with open(filename, "r") as f:
        numInput = int(f.readline().strip())
        inputs = []
        for _ in range(numInput):
            size = int(f.readline().strip())
            rowClue = list(map(int, f.readline().strip().split()))
            colClue = list(map(int, f.readline().strip().split()))
            matrix = []
            for _ in range(size):
                matrix.append(
                    list(
                        map(
                            lambda x: TREE if x == "TREE" else EMPTY,
                            f.readline().strip().split(),
                        )
                    )
                )
            inputs.append((Clue(rowClue, colClue), size, matrix))
    return inputs


def writeOutputToFile(goalNode, fileObject, execTime):
    if goalNode is None:
        fileObject.write("No solution\n")
    else:
        ancestors = goalNode.getAncestors()
        fileObject.write("Path to the goal state:\n")
        for ancestor in ancestors[1:]:
            fileObject.write(" " + str(ancestor.assignLocation))
        fileObject.write("\n")
        fileObject.write("Goal state:\n")
        for row in goalNode.state:
            for cell in row:
                if cell == EMPTY:
                    fileObject.write(" EMPTY")
                elif cell == TREE:
                    fileObject.write(" TREE")
                else:
                    fileObject.write(" TENT")
            fileObject.write("\n")
    fileObject.write("Execution time:\n " + str(execTime) + " seconds\n")
    fileObject.write("--------------------------***--------------------------\n")