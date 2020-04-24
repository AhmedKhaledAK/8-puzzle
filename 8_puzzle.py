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


class State(object):    
    def __init__(self, puzzle, val):
        self.state = puzzle
        self.value = val
        self.distance = 0
        self.zOld = -1

    def __lt__(self, other):
        return self.value <= other.value

    def _eq_(self, other):
        return self.state == other.state

def dfs(puzzle, game):
    frontier = []
    frontier.append(puzzle)

    while len(frontier) != 0:
        state = frontier.pop()

        game.addToVisitSet(state)
        game.addToExpandedList(state)

        if game.isFinalState(state):
            return True

        zi, zj = game.getEIdx(state,0)

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

        zi, zj = game.getEIdx(state,0)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state)
                if game.isVisited(p) == False:
                    frontier.put(p)

    return False

def aStar(puzzle, game):
    frontier = []
    heapq.heapify(frontier)
    
    heapq.heappush(frontier, State(puzzle, game.manhattanH(puzzle)))

    while len(frontier) != 0:
        state = heapq.heappop(frontier)

        if game.isVisited(state.state) == True:
            continue

        game.addToVisitSet(state.state)
        game.addToExpandedList(state.state)

        if game.isFinalState(state.state):
            print("STATE:", state.value)
            return True
        
        zi, zj = game.getEIdx(state.state,0)

        for i in range(4):
            newzi = zi + game.row[i]
            newzj = zj + game.col[i]
            if game.isValidIdx(newzi, newzj):
                p = game.createChild(zi, zj, newzi, newzj, state.state)
                st = State(p,0)
                st.distance = state.distance + 1
                st.value = st.distance + game.manhattanH(p)
                heapq.heappush(frontier, st)
    return False

puzz = [ [7,2,4], [5,0,6], [8,3,1] ]
game = Game()

zi, zj = game.getEIdx(puzz,0)

#print(game.manhattanH(puzz))
#dfs(puzz, game)

print(aStar(puzz,game))
print("-----")
"""
i=0
for r in game.expandedList:
    i+=1
    print(f"{i}: {r}")
"""
