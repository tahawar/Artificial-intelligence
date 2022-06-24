from os import stat
import sys

class Node:
    def __init__(self, state, parent, action) -> None:
        self.state = state
        self.parent = parent
        self.action = action

class BFS:
    def __init__(self) -> None:
        self.frontier = []

    def add(self,node):
        self.frontier.append(node)
    
    def empty(self):
        return len(self.frontier)==0

    def containState(self, state):
        return any(node.state == state for node in self.frontier)

    def remove(self):
        if self.empty():
            raise Exception("Queue is Empty")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class DFS(BFS):
    def remove(self):
        if self.empty():
            raise Exception("Stack is Empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Maze:
    def __init__(self, filename) -> None:

        self.actions = []
        self.cells = []

        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Number of start state should be exactly one")
        if contents.count("B") != 1:
            raise Exception("Number of goal state should be exactly one")

        contents = contents.splitlines()

        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        self.walls = []

        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:    
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None

    def Print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()


    def neighbors(self, state):

        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1)),
        ]

        result = []

        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        print(result)
        return result

    def solve(self):

        self.numExploredStates = 0
        initialState = Node(state=self.start, parent=None, action=None)

        # frontier = BFS()
        frontier = DFS()

        frontier.add(initialState)

        self.exploredStates = set()

        while True:
            if frontier.empty():
                raise Exception("Solution doesn't exists")

            node = frontier.remove()
            self.numExploredStates += 1
            
            if node.state == self.goal:
                while node.parent is not None:
                    self.actions.append(node.action)
                    self.cells.append(node.state)
                    node = node.parent
                self.actions.reverse()
                self.cells.reverse()
                self.solution = (self.actions, self.cells)
                return

            self.exploredStates.add(node.state)

            for action, state in self.neighbors(node.state):
                if not frontier.containState(state) and state not in self.exploredStates:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def cost(self):
        return len(self.actions)

    def __del__(self):
        self.Print()
        print(f"Explored States: {self.numExploredStates}")
        print("\nSoltion: \n")
        print(f"Optimal path from initial state: {self.actions}")
        print(f"Optimal states: {self.cells}")
        print(f"Cost of the path: {self.cost()}")


m = Maze(sys.argv[1])
print("Maze:")
m.Print()
print("Solving...")
m.solve()
m.Print()