import random as rand
import math as m

class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "<{},{}>".format(self.x, self.y)

class EggCarton(object):
    
    def __init__(self, M, N, K):
        self.M = M
        self.N = N
        self.K = K
        self.Tmax = 1.0
        self.dT = 1e-5
        self.Ftarget = 0

    def __repr__(self):
        return "EggCarton({}, {}, {})".format(self.M, self.N, self.K)

    def initBoard(self, n):
        if n > self.M * self.N:
            raise ValueError("Too many eggs")

        left = n
        board = []
        for y in range(int(m.ceil(n / self.N))):
            for x in range(min(left, self.M)):
                p = Point(x, y)
                board.append(p)
            left = max(left - self.M, 0)

        

        return board

    def evalBoard(self, board):
        # Horizontal
        xs = {k: 0 for k in range(self.M)}
        # Vertical
        ys = {k: 0 for k in range(self.N)}
        # Diagonal
        ds1 = {k: 0 for k in range(self.M+self.N-1)}
        ds2 = {k: 0 for k in range(self.M+self.N-1)}
        
        # Compute each point
        for p in board:
            xs[p.x] += 1
            ys[p.y] += 1
            ds1[p.x+p.y] += 1
            ds2[(self.M+self.N-1)//2+p.x-p.y] += 1 

        # Calculate objective function value and return
        F = lambda ss: sum(max(v-self.K,0) for v in ss.values())
        straigt_penalty = 0.9
        diag_penalty    = 0.1

        cumsum =  sum(map(F, [xs, ys]))   * straigt_penalty
        cumsum += sum(map(F, [ds1, ds2])) * diag_penalty

        return self.Ftarget - cumsum

    def genNeighbors(self, board):
        newBoards = []
        # For each point
        for p in board:
            # Generate all neighboring points
            for newy in range(self.N):
                if newy == p.y:
                    continue

                newp = Point(p.x, newy)
                if newp not in board:
                    newboard = board[:]
                    newboard[newboard.index(p)] = newp
                    newBoards.append(newboard)

        return newBoards

    def printBoard(self, board):
        for y in range(self.N):
            for x in range(self.M):
                if Point(x,y) in board:
                    print('X ', end='')
                else:
                    print('. ', end='')
            print()

    def simulated_annealing(self, numEggs):
        # Create initial board
        P = self.initBoard(numEggs)
        T = self.Tmax

        iteration = 0
        FP = self.evalBoard(P)

        while FP != self.Ftarget and T > self.dT:
            neighbors = self.genNeighbors(P)
            Pmax = None
            FPmax = -float('inf')

            for neighbor in neighbors:
                FPn = self.evalBoard(neighbor)
                if FPn > FPmax:
                    FPmax = FPn
                    Pmax = neighbor

            q = max(0, float(FPmax - FP))
            p = min(1.0, m.e**(-q / T))
            x = rand.random()

            if x > p:
                P = Pmax
            else:
                P = rand.choice(neighbors)
            FP = self.evalBoard(P)

            T -= self.dT

            iteration += 1

        print("Finished in {} iterations".format(iteration))

        return FP, P