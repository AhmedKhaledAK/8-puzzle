import copy
import queue
import heapq

class Game(object):

    def __init__(self):
        self.visitSet = set()
        self.path = []
        self.expandedList = []
        self.paths = []
        self.row = [0, 0, -1, 1]
        self.col = [1, -1, 0, 0]
    
    def createChild(self, zi, zj, ei, ej, puzzle):
        newPuzzle = copy.deepcopy(puzzle)
        newPuzzle[zi][zj], newPuzzle[ei][ej] = newPuzzle[ei][ej], newPuzzle[zi][zj]
        return newPuzzle

    def addToVisitSet(self, puzzle):
        keyPuzzle = tuple(tuple(x) for x in puzzle)
        self.visitSet.add(keyPuzzle)

    def isVisited(self, puzzle):
        keyPuzzle = tuple(tuple(x) for x in puzzle)
        return keyPuzzle in self.visitSet

    def isFinalState(self, puzzle):
        return puzzle == [ [0,1,2], [3,4,5], [6,7,8] ]
    
    def addToPath(self, puzzle):
        self.path.append(puzzle)

    def addToExpandedList(self, puzzle):
        self.expandedList.append(puzzle)
    
    def addToPaths(self, puzzle):
        self.paths.append(puzzle)
    
    def isValidIdx(self, i, j):
        return i >= 0 and i <= 2 and j >= 0 and j <= 2
    
    def getZeroIdx(self, puzzle):
        zi = -1
        zj = -1
        i = -1
        j=-1
        for r in puzzle:
            i+=1
            j=-1
            for c in r:
                j+=1
                if c == 0:
                    zi, zj = i, j
                    break
        return zi, zj

class State(object):
    def __init__(self):
        self.state = []
        self.value = 0
        self.zOld = -1

    def __le__(self, other):
        return self.value <= other.value

def dfs(puzzle, game):
    frontier = []
    frontier.append(puzzle)

    while len(frontier) != 0:
        state = frontier.pop()

        game.addToVisitSet(state)
        game.addToExpandedList(state)

        if game.isFinalState(state):
            return True

        zi, zj = game.getZeroIdx(state)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                if game.isVisited(p) == False:
                    frontier.append(p)
            
    return False

def bfs(puzzle, game):
    frontier = queue.Queue()
    frontier.put(puzzle)

    while frontier.empty() == False:
        state = frontier.get()

        game.addToVisitSet(state)
        game.addToExpandedList(state)

        if game.isFinalState(state):
            return True

        zi, zj = game.getZeroIdx(state)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                if game.isVisited(p) == False:
                    frontier.put(p)

    return False

puzz = [ [1,2,5], [3,4,0], [6,7,8] ]
game = Game()

zi, zj = game.getZeroIdx(puzz)

#dfs(puzz, game)
print(bfs(puzz,game))
print("-----")

i=0
for r in game.expandedList:
    i+=1
    print(f"{i}: {r}")
