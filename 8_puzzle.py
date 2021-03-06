import copy
import queue
import heapq
import math
import datetime
import itertools

class Game(object):

    def __init__(self):
        self.visitSet = set()
        self.path = []
        self.expandedList = []
        self.paths = []
        self.row = [0, 0, -1, 1]
        self.col = [1, -1, 0, 0]
        self.maxSearchDepth = 0
        self.bfsPath = {}
    
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
    
    def getEIdx(self, puzzle, e):
        zi = -1
        zj = -1
        i = -1
        j=-1
        for r in puzzle:
            i+=1
            j=-1
            for c in r:
                j+=1
                if c == e:
                    zi, zj = i, j
                    break
        return zi, zj

    def manhattanH(self, puzzle):
        total = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                val = puzzle[i][j]
                if val is 0:
                    continue
        
                distance = abs(i - int(val/3)) + abs(j - val%3)
                #print(distance)
                total += distance

        return total

    def euclideanH(self, puzzle):
        total = 0
        for i in range(len(puzzle)):
            for j in range(len(puzzle)):
                val = puzzle[i][j]
                if val is 0:
                    continue
        
                distance = math.sqrt(pow(i - int(val/3),2) + pow(j - val%3, 2))
                #print(distance)
                total += distance

        return total

    def hasChildren(self, puzzle):
        zi, zj = game.getEIdx(puzzle, 0)
        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, puzzle)
                if game.isVisited(p) == False:
                    return True
        return False
    
    def addToPathMap(self, key, value):
        keyPuzzle = tuple(tuple(x) for x in key)
        valuePuzzle = tuple(tuple(x) for x in value)
        self.bfsPath[keyPuzzle] = valuePuzzle

    def setPath(self, state):
        goalState = tuple(tuple(x) for x in state)
        st = goalState
        print(st)
        while st in self.bfsPath:
            self.path.append(st)
            st = self.bfsPath[st]
            print(st)
        self.path.reverse()

    def isSolvable(self, puzzle):
        array = list(itertools.chain.from_iterable(puzzle))
        print(array)
        invCount = 0
        for i in range(8):
            for j in range(i + 1, 9):
                if array[j] != 0 and array[i] != 0 and array[i] > array[j]:
                    invCount += 1
        print("cnt:",invCount)
        return invCount % 2 == 0


class State(object):    
    def __init__(self, puzz, val):
        self.puzzle = puzz
        self.value = val
        self.distance = 0

    def __lt__(self, other):
        return self.value < other.value

    def _eq_(self, other):
        return self.puzzle == other.puzzle

def dfs(puzzle, game):
    frontier = []
    frontier.append(puzzle)

    maxDepth = 0

    while len(frontier) != 0:
        state = frontier.pop()

        if game.isVisited(state) == True:
            continue

        game.addToVisitSet(state)
        game.addToExpandedList(state)
        game.addToPath(state)

        if game.isFinalState(state):
            return True

        zi, zj = game.getEIdx(state,0)

        st = game.path[len(game.path) - 1]
        while game.hasChildren(st) == False:
            game.path.pop()
            st = game.path[len(game.path) - 1]

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                frontier.append(p)
            
    return False

def bfs(puzzle, game):
    frontier = queue.Queue()
    frontier.put(puzzle)

    while frontier.empty() == False:
        state = frontier.get()

        if game.isVisited(state) == True:
            continue

        game.addToVisitSet(state)
        game.addToExpandedList(state)

        if game.isFinalState(state):
            game.setPath(state)
            return True

        zi, zj = game.getEIdx(state,0)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                frontier.put(p)
                if game.isVisited(p) == False:
                    game.addToPathMap(p, state)

    return False

def aStar(puzzle, game, func):
    frontier = []
    heapq.heapify(frontier)
    
    heapq.heappush(frontier, State(puzzle, func(puzzle)))
    cost = 0
    while len(frontier) != 0:
        state = heapq.heappop(frontier)

        if game.isVisited(state.puzzle) == True:
            continue

        game.addToVisitSet(state.puzzle)
        game.addToExpandedList(state.puzzle)

        if game.isFinalState(state.puzzle):
            print("STATE:", state.value)
            print("cost:", cost)
            game.setPath(state.puzzle)
            return True

        cost+=1
        
        zi, zj = game.getEIdx(state.puzzle,0)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state.puzzle)
                st = State(p,0)
                st.distance = state.distance + 1
                st.value = st.distance + func(p)
                heapq.heappush(frontier, st)
                if game.isVisited(p) == False:
                    game.addToPathMap(p, state.puzzle)
    return False

#puzz = [[7,2,4], [5,0,6], [8,3,1]]
#puzz = [[0,1,2], [3,4,5], [6,7,8]]
puzz = [[8,1,2], [0,4,3], [7,6,5]]
game = Game()

if game.isSolvable(puzz):
    zi, zj = game.getEIdx(puzz,0)
    cost = 0
    #print(game.manhattanH(puzz))
    #dfs(puzz, game)

    a = datetime.datetime.now()
    print(aStar(puzz,game,game.manhattanH))
    b = datetime.datetime.now()
    c = b-a
    print(c.total_seconds())
    print("-----")
    """
    i=0
    for r in game.expandedList:
    i+=1
    print(f"{i}: {r}")
    """
    print(len(game.expandedList))
    print(len(game.visitSet))
    print(len(game.path))
    print(game.path.pop())
else:
    print("unsolvable")
