from Node import Node
from collections import deque, defaultdict
from Node import EMPTY, TREE, TENT
from Utils import generateNextNodes, haveOneToOne
from OpenList import OpenList
# from memory_profiler import profile

class Searching: 
    #clue: Clue
    #initNode: Node
    #totalTents: int

    #Init the searching with clue, size, and matrix
    def __init__(self, clue, size, matrix):
        self.clue = clue
        self.initNode = Node(size, matrix, None)
        self.totalTents = sum(clue.rowClue)

    #Check if the current state is the goal state
    def isGoalState(self, curNode: Node):
        if curNode.numOfCurTents != self.totalTents:
            return False
        tentsPos = []
        tentToTrees = defaultdict(list)
        pairedTrees = set()
        for i in range(curNode.size):
            for j in range(curNode.size):
                if curNode.state[i][j] == TENT:
                    tentsPos.append((i, j))
                    for x, y in [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]:
                        if (
                            0 <= x < curNode.size
                            and 0 <= y < curNode.size
                            and curNode.state[x][y] == TREE
                        ):
                            tentToTrees[(i, j)].append((x, y))
        return haveOneToOne(0, pairedTrees, tentToTrees, tentsPos)

    #Breath First Search
    # @profile
    def breadthFirstSearch(self):
        visited = set()
        queue = deque([self.initNode])

        while queue:
            curNode = queue.popleft()
            if self.isGoalState(curNode):
                ans = curNode
                return ans
            visited.add(curNode)

            nextNodes = generateNextNodes(curNode, self.clue)
            for nextNode in nextNodes:
                if nextNode not in visited:
                    queue.append(nextNode)

        return None
    
    #A* Search
    def aStarSearch(self):
        answer = None
        openList = OpenList()
        closeList = []
        openList.push((0, self.initNode))

        while openList.getLength() > 0:
            curNode = openList.pop()
            if self.isGoalState(curNode):
                answer = curNode
                return answer
            neighborNodes = generateNextNodes(curNode, self.clue)
            for node in neighborNodes:
                if node in closeList:
                    continue
                openList.push((self.aStarFunction(node), node))
            closeList.append(curNode)

        return answer

    def heuristicFunction(self, curNode):
        unsatisfiedRowAndCol = 0
        for i in range(curNode.size):
            if curNode.curTentsRow[i] != self.clue.rowClue[i]:
                unsatisfiedRowAndCol += 1
            if curNode.curTentsCol[i] != self.clue.colClue[i]:
                unsatisfiedRowAndCol += 1
        return unsatisfiedRowAndCol

    def aStarFunction(self, curNode):
        return curNode.numOfCurTents + 24 * self.heuristicFunction(curNode)
