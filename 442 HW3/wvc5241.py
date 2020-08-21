############################################################
# CMPSC 442: Homework 3
############################################################

student_name = "Wei Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math
import random
from queue import PriorityQueue


############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    board = []
    for i in range(rows):
        row = []
        for j in range(cols):
            row.append(j+i*cols+1)
        board.append(row[:])
    board[-1][-1] = 0
    return TilePuzzle(board)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.r = len(board)
        self.c = len(board[0])
        self.dim = self.r, self.c
        for i in range(self.r):
            for j in range(self.c):
                if self.board[i][j] == 0:
                    self.empty = (i,j)

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        directions = ['up','down','left','right']

        if direction not in directions:
            return False

        i,j = self.empty

        if direction == 'up':
            if i == 0:
                return False
            else:
                self.empty = (i-1, j)
                self.board[i][j], self.board[i-1][j] = self.board[i-1][j], self.board[i][j]
                return True
        elif direction == 'down':
            if i == self.r-1:
                return False
            else:
                self.empty = (i+1, j)
                self.board[i][j], self.board[i+1][j] = self.board[i+1][j], self.board[i][j]
                return True  
        elif direction == 'left':
            if j == 0:
                return False
            else:
                self.empty = (i, j-1)
                self.board[i][j], self.board[i][j-1] = self.board[i][j-1], self.board[i][j]
                return True                  
        elif direction == 'right':
            if j == self.c-1:
                return False
            else:
                self.empty = (i, j+1)
                self.board[i][j], self.board[i][j+1] = self.board[i][j+1], self.board[i][j]
                return True  



    def scramble(self, num_moves):
        directions = ['up','down','left','right']
        for i in range(num_moves):
            direct = random.choice(directions)
            self.perform_move(direct)

    def is_solved(self):
        r,c = self.dim
        for i in range(r):
            for j in range(c):
                if (i == r-1) and (j == c-1):
                    return (self.board[i][j] == 0)
                if self.board[i][j] != j+i*c+1:
                    return False

    def copy(self):
        new_board = []
        for l in self.board:
            new_board.append(l[:])
        return TilePuzzle(new_board)


    def successors(self):
        directions = ['up','down','left','right']
        for move in directions:
            new_p = self.copy()
            if new_p.perform_move(move):
                yield (move, new_p)

    def iddfs_helper(self, states, visited):
        new_states = {}
        solved = False
        solved_move = []
        for p,m in states.items():
            for move,new_p in p.successors():
                if new_p.is_solved():
                    solved = True
                    solved_move.append(m+[move])
                elif not solved:
                    if tuple(map(tuple, new_p.board)) not in visited:
                        new_states[new_p] = m+[move]
                        visited.add(tuple(map(tuple, new_p.board)))
        if solved:
            return solved,solved_move,visited
        else:
            return solved,new_states,visited


    # Required
    def find_solutions_iddfs(self):
        states = {self.copy():[]}
        visited = set()
        visited.add(tuple(map(tuple, self.board)))
        while True:
            solved,states,visited = self.iddfs_helper(states,visited)
            if solved:
                for i in states:
                    yield i
                break

    def h(self):
        total_dis = 0
        r,c = self.dim
        for i in range(r):
            for j in range(c):
                n = self.board[i][j]
                if n == 0:
                    x = r-1
                    y = c-1
                else:
                    x = (n-1) // c
                    y = n - c*x - 1
                dis = abs(x - i) + abs(y - j)
                total_dis += dis
        return total_dis

    # Required
    def find_solution_a_star(self):
        visited = set()
        PQ = PriorityQueue()
        PQ.put((self.h(),[],self.copy()))
        visited.add(tuple(map(tuple, self.board)))
        while not PQ.empty():
            h,m,p = PQ.get()
            if p.is_solved():
                return m
            for move, new_p in p.successors():
                if tuple(map(tuple, new_p.board)) not in visited:
                    PQ.put((new_p.h()+len(m)+1,m+[move],new_p))
                    visited.add(tuple(map(tuple, p.board)))


############################################################
# Section 2: Grid Navigation
############################################################

def Euclidean_dis(cur_pos, goal):
    a, b = cur_pos
    c, d = goal
    return math.sqrt((a-c)**2 + (b-d)**2)

def pos_valid(pos, scene):
    r, c = len(scene), len(scene[0])
    i,j = pos
    if (i<0) or (i>=r):
        return False
    if (j<0) or (j>=c):
        return False
    if scene[i][j]:
        return False
    return True

def find_path_succ(cur_pos, scene):
    r, c = len(scene), len(scene[0])
    res = []
    i, j =cur_pos
    succ = [(i-1,j-1), (i-1,j), (i-1, j+1), (i,j-1), (i,j+1), (i+1,j-1),(i+1,j),(i+1,j+1)]
    for p in succ:
        if pos_valid(p,scene):
            res.append(p)
    return res


def find_path(start, goal, scene):
    r, c = len(scene), len(scene[0])
    visited = set()
    PQ = PriorityQueue()
    PQ.put((Euclidean_dis(start,goal),[start]))
    visited.add(start)
    while (not PQ.empty()):
        h,m = PQ.get()
        cur_pos = m[-1]
        if cur_pos == goal:
            return m
        for s in find_path_succ(cur_pos, scene):
            if s not in visited:
                PQ.put((Euclidean_dis(s,goal)+len(m),m+[s]))
                visited.add(cur_pos)
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
def next_states_distinct(cur_state):
    length = len(cur_state)
    res = []
    for i in range(length):
        next_state = cur_state[:]
        if cur_state[i] == -1:
            continue
        if (i+1 < length) and (cur_state[i+1] == -1):
            move = (i, i+1)
            next_state[i] = -1
            next_state[i+1] = cur_state[i]
            res.append((next_state[:], move))
            next_state = cur_state[:]

        if (i-1 >= 0) and (cur_state[i-1] == -1):
            move = (i, i-1)
            next_state[i] = -1
            next_state[i-1] = cur_state[i]
            res.append((next_state[:], move))
            next_state = cur_state[:]

        if (i+2 < length) and (cur_state[i+1] != -1) and (cur_state[i+2] == -1):
            move = (i,i+2)
            next_state[i] = -1
            next_state[i+2] = cur_state[i]
            res.append((next_state[:], move))
            next_state = cur_state[:]

        if (i-2 >= 0) and (cur_state[i-1] != -1) and (cur_state[i-2] == -1):
            move = (i,i-2)
            next_state[i] = -1
            next_state[i-2] = cur_state[i]
            res.append((next_state[:], move))
            next_state = cur_state[:]
    return res

def distinct_disks_h(state):
    length = len(state)
    h = 0
    for i in range(length):
        if state[i] != -1:
            h += abs(i - (length - 1 -state[i]))
    return h


def solve_distinct_disks(length, n):
    start = [i for i in range(n)] + [-1 for i in range(length-n)]
    end = [-1 for i in range(length-n)] + [i for i in range(n-1,-1,-1)]
    PQ = PriorityQueue()
    PQ.put((distinct_disks_h(start), start,[]))
    visited = set()
    visited.add(tuple(start))
    while not (PQ.empty()):
        h,s,m = PQ.get()
        if s == end:
            return m
        for state,move in next_states_distinct(s):
            if tuple(state) not in visited:
                PQ.put((distinct_disks_h(state)+len(m)+1, state,m + [move]))
                visited.add(tuple(state))



############################################################
# Section 4: Dominoes Game
############################################################

def create_dominoes_game(rows, cols):
    board = []
    row = [False for i in range(cols)]
    for i in range(rows):
        board.append(row[:])
    return DominoesGame(board)

class DominoesGame(object):

    # global variable
    leaf_nodes = 0

    # Required
    def __init__(self, board):
        self.board = board
        self.r = len(board)
        self.c = len(board[0])
        self.dim = self.r , self.c
        self.best_move = None

    def get_board(self):
        return self.board

    def reset(self):
        rows, cols = self.dim
        board = []
        row = [False for i in range(cols)]
        for i in range(rows):
            board.append(row[:])
        self.board = board

    def is_legal_move(self, row, col, vertical):
        r,c = self.dim
        if (row<0) or (row >= r):
            return False
        if (col<0) or (col>=c):
            return False
        if self.board[row][col]:
                return False
        if vertical:
            if (row+1 >= r):
                return False
            if self.board[row+1][col]:
                return False
        else:
            if (col+1 >= c):
                return False
            if self.board[row][col+1]:
                return False  
        return True       


    def legal_moves(self, vertical):
        r,c = self.dim
        for i in range(r):
            for j in range(c):
                if self.is_legal_move(i,j,vertical):
                    yield (i,j)


    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row+1][col] = True
        else:
            self.board[row][col+1] = True

    def game_over(self, vertical):
        moves = list(self.legal_moves(vertical))
        if len(moves) == 0:
            return True
        else:
            return False

    def copy(self):
        board = []
        for l in self.board:
            board.append(l[:])
        return DominoesGame(board)

    def successors(self, vertical):
        for m in self.legal_moves(vertical):
            i,j = m
            new_g = self.copy()
            new_g.perform_move(i,j,vertical)
            yield (m,new_g)

    def get_random_move(self, vertical):
        moves = list(self.legal_moves(vertical))
        return random.choice(moves)

    def value(self, vertical):
        moves = list(self.legal_moves(vertical))
        oppo_moves = list(self.legal_moves(not vertical))
        return len(moves) - len(oppo_moves)

    def min_value(self, alpha, beta, vertical,limit):
        if self.game_over(vertical) or limit == 0:
            DominoesGame.leaf_nodes += 1
            return self.value(not vertical)
        limit -= 1    
        min_v = math.inf
        for m,new_g in self.successors(vertical):
            v = new_g.max_value(alpha, beta, not vertical, limit)
            if v < min_v:
                min_v = v
                self.best_move = m
            if min_v<= alpha:
                return min_v
            beta = min(beta,min_v)
        return min_v

    def max_value(self, alpha, beta, vertical,limit):
        
        if self.game_over(vertical) or limit == 0:
            DominoesGame.leaf_nodes += 1
            return self.value(vertical)
        limit -= 1
        max_v = -math.inf
        for m,new_g in self.successors(vertical):
            v = new_g.min_value(alpha, beta, not vertical, limit)
            if v > max_v:
                max_v = v
                self.best_move = m
            if max_v >= beta:
                return max_v
            alpha = max(alpha, max_v)
        return max_v

    # Required
    def get_best_move(self, vertical, limit):
        v = self.max_value(-math.inf, math.inf, vertical,limit)
        return (self.best_move, v, DominoesGame.leaf_nodes)

############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
8 hours
"""

feedback_question_2 = """
It is hard to meet the time limit of the autograder. I spent 
a lot of time on improving performance. Also, the code of alpha
and beta pruning and min max search is difficult. I spent a lot of 
time understanding the psudocode in the lecture note.
"""

feedback_question_3 = """
I like that for each problem, we can generate a GUI to test our code.
I think more public test cases can be given, so that we know whether 
our code works and whether there are some corner cases not addressed
by our code. 
"""
