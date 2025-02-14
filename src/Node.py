import copy

EMPTY = 0
TREE = 1
TENT = 2

class Node: 
    #size: int 
    #state: List<list> 
    #prevNode: Node
    #numOfCurTents: int
    #curTentsRow: List<int>
    #curTentsCol: List<int>
    #assignLocation: Tuple<int, int>

    #Init the game state with size, matrix, and previous node
    def __init__(self, size: int, matrix: list, prevNode):
        self.size = size
        self.state = matrix
        self.prevNode = prevNode
        self.assignLocation = None

        if self.prevNode is None: 
            self.numOfCurTents = 0
            self.curTentsRow = [0] * size
            self.curTentsCol = [0] * size
        else: 
            self.numOfCurTents = self.prevNode.numOfCurTents + 1
            self.curTentsRow = copy.deepcopy(self.prevNode.curTentsRow)
            self.curTentsCol = copy.deepcopy(self.prevNode.curTentsCol)

    #Compare the current state with other state
    def __eq__(self, otherNode):
        if (type(otherNode) != Node):
            return False
        
        for i in range(self.size):
            for j in range(self.size):
                if self.state[i][j] != otherNode.state[i][j]:
                    return False
        return True
    
    #Return true if current state's tents are less than other state's tents
    def __lt__(self, otherNode):
        return self.numOfCurTents < otherNode.numOfCurTents
    
    #Assign tent to the Position
    def assignTentTo(self, position: tuple):
        self.state[position[0]][position[1]] = TENT
        self.numOfCurTents = self.prevNode.numOfCurTents + 1
        self.curTentsRow[position[0]] += 1
        self.curTentsCol[position[1]] += 1
        self.assignLocation = position

    #Return the list of ancestors
    def getAncestors(self):
        ancestors = [self]
        runner = self 
        while runner.prevNode is not None:
            ancestors = [runner.prevNode] + ancestors
            runner = runner.prevNode
        return ancestors
    
    def __hash__(self):
        return hash(tuple(map(tuple, self.state)))