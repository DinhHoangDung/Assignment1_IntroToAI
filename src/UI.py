import tkinter as tk
from tkinter import messagebox
from Searching import *
from PIL import Image, ImageTk
from collections import deque
from Node import TREE, TENT
from Utils import readInputFromFile

def createBoard(parentFrame, size, state, wCell, hCell, tree_image):
    board_frame = tk.Frame(parentFrame)
    board_frame.grid(row=1, column=1)

    for i in range(size):
        for j in range(size):
            cell_color = "green" if state[i][j] == TREE else "white"
            cell = tk.Label(
                board_frame,
                width=wCell,
                height=hCell,
                borderwidth=1,
                relief="solid",
                foreground=cell_color,
                bg='white'
            )
            if state[i][j] == TREE:
                cell.config(image=tree_image)
                cell.image = tree_image
            cell.grid(row=i, column=j, sticky="nsew")
    return board_frame


def updateBoard(board_frame, assignPos, tent_image):
    i, j = assignPos
    cell = board_frame.grid_slaves(row=i, column=j)[0]
    cell.config(image=tent_image, foreground="red")
    cell.image = tent_image


def update_board_recursively(window, board_frame, ancestors, index, tent_image):
    if index < len(ancestors):
        node = ancestors[index]
        updateBoard(board_frame, node.assignLocation, tent_image)
        window.after(
            1000,
            update_board_recursively,
            window,
            board_frame,
            ancestors,
            index + 1,
            tent_image,
        )


def createNewBoard(parentFrame, size, newState, wCell, hCell, curBoard, tent_image, tree_image):
    for i in range(size):
        for j in range(size):
            valueHere = newState[i][j]
            if valueHere == TREE:
                cell_image = tree_image
                cell_color = "green"
            elif valueHere == TENT:
                cell_image = tent_image
                cell_color = "red"
            else:
                cell_image = ""
                cell_color = "white"
            cell = curBoard.grid_slaves(row=i, column=j)[0]
            cell.config(image=cell_image, foreground=cell_color)
            cell.image = cell_image
    return curBoard



class UI(Searching):
    def __init__(self, clue, size, matrix, widthCell, heightCell):
        self.window = tk.Tk()
        self.clue = clue
        self.initNode = Node(size, matrix, None)
        self.totalTents = sum(clue.rowClue)
        self.wCell = widthCell
        self.hCell = heightCell
        self.answer = None

        self.tree_image = self.load_and_resize_image("../img/tree.jpg", widthCell * 10, heightCell * 10)
        self.tent_image = self.load_and_resize_image("../img/tent.jpg", widthCell * 10, heightCell * 10)

    def load_and_resize_image(self, path, width, height):
        image = Image.open(path)
        image = image.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(image)

    def select_algorithm(self, algorithm, board_frame):
        if algorithm == "astar":
            self.aStarSearchBt.config(state=tk.DISABLED, relief=tk.SUNKEN)
            self.bfsSearchBt.config(state=tk.DISABLED)
            self.aStarSearch(board_frame)
        elif algorithm == "bfs":
            self.bfsSearchBt.config(state=tk.DISABLED, relief=tk.SUNKEN)
            self.aStarSearchBt.config(state=tk.DISABLED)
            self.breadthFirstSearch(board_frame)

    def enable_print_solution(self):
        self.printSolutionBt.config(state=tk.NORMAL)

    def printSolution(self, board_frame):
        if self.answer is None:
            messagebox.showinfo("Result", "No solution found")
        else:
            ancestors = self.answer.getAncestors()
            createNewBoard(
                self.window, self.initNode.size, self.initNode.state, 6, 3, board_frame, self.tent_image, self.tree_image
            )
            update_board_recursively(self.window, board_frame, ancestors, 1, self.tent_image)

    def breadthFirstSearch(self, board_frame):
        visited = set()
        queue = deque([self.initNode])

        def updateBoardInSearch():
            if queue:
                curNode = queue.popleft()
                createNewBoard(self.window, self.initNode.size, curNode.state, self.wCell, self.hCell, board_frame, self.tent_image, self.tree_image)
                if self.isGoalState(curNode):
                    self.answer = curNode
                    messagebox.showinfo("Result", "Solution found")
                    self.enable_print_solution()
                else:
                    neighborNodes = generateNextNodes(curNode, self.clue)
                    visited.add(curNode)
                    for node in neighborNodes:
                        if node not in visited:
                            queue.append(node)
                    self.window.after(300, updateBoardInSearch)

        updateBoardInSearch()

    def aStarSearch(self, board_frame):
        openList = OpenList()
        closeList = []
        openList.push((0, self.initNode))

        def updateBoardInSearch():
            if openList.getLength() > 0:
                curNode = openList.pop()
                createNewBoard(self.window, self.initNode.size, curNode.state, self.wCell, self.hCell, board_frame, self.tent_image, self.tree_image)
                if self.isGoalState(curNode):
                    self.answer = curNode
                    messagebox.showinfo("Result", "Solution found")
                    self.enable_print_solution()
                else:
                    neighborNodes = generateNextNodes(curNode, self.clue)
                    for node in neighborNodes:
                        if node not in closeList:
                            openList.push((self.aStarFunction(node), node))
                    closeList.append(curNode)
                    self.window.after(300, updateBoardInSearch)

        updateBoardInSearch()

    def createUI(self):
        self.window.title("Tents Game")
        self.window.geometry("800x600")

        main_frame = tk.Frame(self.window)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        top_clues_frame = tk.Frame(main_frame)
        top_clues_frame.grid(row=0, column=1, pady=(0, 0))
        for j, clue in enumerate(self.clue.colClue):
            label = tk.Label(
                top_clues_frame, text=str(clue), width=self.wCell, height=self.hCell
            )
            label.grid(row=0, column=j)

        left_clues_frame = tk.Frame(main_frame)
        left_clues_frame.grid(row=1, column=0, padx=(0, 0))
        for i, clue in enumerate(self.clue.rowClue):
            label = tk.Label(
                left_clues_frame, text=str(clue), width=self.wCell, height=self.hCell
            )
            label.grid(row=i, column=0)
        
        board_frame = createBoard(main_frame, self.initNode.size, self.initNode.state, self.wCell, self.hCell, self.tree_image)
        board_frame.grid(row=1, column=1) 

        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=1, pady=20)

        self.aStarSearchBt = tk.Button(
            button_frame,
            text="A* Search",
            command=lambda: self.select_algorithm("astar", board_frame),
            width=10,
            bg="red",
        )
        self.aStarSearchBt.grid(row=0, column=0, padx=10)

        self.bfsSearchBt = tk.Button(
            button_frame,
            text="BFS Search",
            command=lambda: self.select_algorithm("bfs", board_frame),
            width=10,
            bg="yellow",
        )
        self.bfsSearchBt.grid(row=0, column=1, padx=10)

        self.printSolutionBt = tk.Button(
            button_frame,
            text="Print",
            command=lambda: self.printSolution(board_frame),
            state=tk.DISABLED,
            width=10,
        )
        self.printSolutionBt.grid(row=0, column=2, padx=10)

        self.window.mainloop()

def main():
    input = readInputFromFile("../testcase/input.txt")
    clue, size, matrix = input[0]
    widthCell = 6
    heightCell = 3
    ui = UI(clue, size, matrix, widthCell, heightCell)
    ui.createUI()


if __name__ == "__main__":
    main()
