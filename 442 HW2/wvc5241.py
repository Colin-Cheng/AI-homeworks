############################################################
# CMPSC 442: Homework 2
############################################################

student_name = "Wei Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random


############################################################
# Section 1: N-Queens
############################################################

def num_placements_all(n):
    res = 1
    for i in range(n):
        res *= (n*n) - i
    return res

def num_placements_one_per_row(n):
    res = 1
    for i in range(n):
        res *= n
    return res


def n_queens_valid(board):
    for i in range(len(board)):
        for j in range(len(board)):
            # check column
            if (board[i] == board[j]) and (i!=j):
                return False
            # check diagonal
            if (abs(board[i] - board[j]) == abs(i - j)) and (i!=j):
                return False
    return True


def n_queens_helper(n, board):
    for i in range(n-1,-1,-1):
        new_board = board[:]
        new_board.append(i)
        if n_queens_valid(new_board):
            yield new_board


def n_queens_solutions(n):
    start = []
    stack = []
    stack.append(start)

    while stack:
        cur = stack.pop()
        if len(cur) == n:
            yield cur
        for b in n_queens_helper(n,cur):
            stack.append(b)

############################################################
# Section 2: Lights Out
############################################################

class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.dim = len(board) , len(board[0]) # board dimension

    def get_board(self):
        return self.board

    # check whether the point is on the board
    def on_board(self, row, col):
        m,n = self.dim
        if (row >= m) or (row < 0):
            return False
        elif (col >= n) or (col < 0):
            return False
        else:
            return True

    # get the neighbor of the point
    def get_neighbor(self, row, col):
        neighbor = []
        if self.on_board(row-1,col):
            neighbor.append([row-1,col])
        if self.on_board(row+1,col):
            neighbor.append([row+1,col])
        if self.on_board(row,col-1):
            neighbor.append([row,col-1])
        if self.on_board(row,col+1):
            neighbor.append([row,col+1])
        return neighbor

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        for p in self.get_neighbor(row,col):
            self.board[p[0]][p[1]] = not self.board[p[0]][p[1]]

    def scramble(self):
        m,n = self.dim
        for row in range(m):
            for col in range(n):
                if random.random() < 0.5:
                    self.perform_move(row,col)

    def is_solved(self):
        m,n = self.dim
        for row in range(m):
            for col in range(n):
                if self.board[row][col]:
                    return False
        return True

    def copy(self):
        b = [x[:] for x in self.board]
        return LightsOutPuzzle(b)

    def successors(self):
        m,n = self.dim
        for row in range(m):
            for col in range(n):
                p = self.copy()
                p.perform_move(row,col)
                move = (row,col)
                yield move, p
    
    # convert a state to tuple representation         
    def convert_to_tuple(self):
        b = [x[:] for x in self.board]
        m,n = self.dim
        for i in range(m):
            b[i] = tuple(b[i])
        return tuple(b)

    # return whether self state has been visited
    def in_visited(self, visited):
        if self.convert_to_tuple() in visited:
            return True
        else:
            return False

    # return every move from start state to end state
    def backtrace(self, parent, start, end):
        path = []
        current = end
        while current != start:
            last, move = parent[current]
            path.append(move)
            current = last
        path.reverse()
        return path
    
    def find_solution(self):
        visited = set()
        parent = {}
        queue = []
        start = self.convert_to_tuple()
        queue.append(self)
        while queue:
            p = queue.pop(0)
            visited.add(p.convert_to_tuple())
            for move, new_p in p.successors():
                if not new_p.in_visited(visited):
                    queue.append(new_p)
                    if new_p.convert_to_tuple() not in parent:
                        parent[new_p.convert_to_tuple()] = (p.convert_to_tuple(), move)
                    if new_p.is_solved():
                        end = new_p.convert_to_tuple()
                        return self.backtrace(parent, start, end)

        return None
        
        
def create_puzzle(rows, cols):
    b = []
    row = [False for i in range(cols)]
    for i in range(rows):
        b.append(row[:])
    return LightsOutPuzzle(b)

############################################################
# Section 3: Linear Disk Movement
############################################################
def next_states_identical(length, cur_state):
    res = []
    for i in cur_state:
        next_state = cur_state.copy()
        if ((i+1) not in cur_state) and (i+1) < length:
            move = (i,i+1)
            next_state.remove(i)
            next_state.add(i+1)
            res.append((next_state.copy(),move)) 
            next_state = cur_state.copy()

        if ((i-1) not in cur_state) and (i-1) >= 0:
            move = (i,i-1)
            next_state.remove(i)
            next_state.add(i-1)
            res.append((next_state.copy(),move)) 
            next_state = cur_state.copy() 

        if ((i+1) in cur_state) and ((i+2) not in cur_state) and (i+2) < length:
            move = (i,i+2)
            next_state.remove(i)
            next_state.add(i+2)
            res.append((next_state.copy(),move)) 
            next_state = cur_state.copy()

        if ((i-1) in cur_state) and ((i-2) not in cur_state) and (i-2) >=0:
            move = (i,i-2)
            next_state.remove(i)
            next_state.add(i-2)
            res.append((next_state.copy(),move)) 
            next_state = cur_state.copy()
    return res

def disks_backtrace(parent, start, end):
    path = []
    current = end
    while current != start:
        last, move = parent[tuple(current)]
        path.append(move)
        current = last
    path.reverse()
    return path

def solve_identical_disks(length, n):
    # use a set of index whcih is filled by disk to represent each state
    start = set([i for i in range(n)])
    end = set([i for i in range(length-n,length)])
    queue = []
    visited = set()
    parent = {}
    queue.append(start)

    while queue:
        cur_state = queue.pop(0)
        visited.add(tuple(cur_state))
        for s, move in next_states_identical(length, cur_state):
            s = tuple(s)
            if s not in visited:
                queue.append(set(s))
                if s not in parent:
                    parent[s] = (cur_state,move)
                if set(s) == end:
                    return disks_backtrace(parent, start, end)
                    

def next_states_distinct(length, cur_state):
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

def solve_distinct_disks(length, n):
    # use a list to represent the row of cells
    # use number 0 through n-1 to represent each disk
    # -1 means that cell is empty
    start = [i for i in range(n)] + [-1 for i in range(length-n)]
    end = [-1 for i in range(length-n)] + [i for i in range(n-1,-1,-1)]
    queue = []
    visited = set()
    parent = {}
    queue.append(start)

    while queue:
        cur_state = queue.pop(0)
        visited.add(tuple(cur_state))
        for s, move in next_states_distinct(length, cur_state):
            s = tuple(s)
            if s not in visited:
                queue.append(list(s))
                if s not in parent:
                    parent[s] = (cur_state,move)
                if list(s) == end:
                    return disks_backtrace(parent, start, end)

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
approximately 3 hours
"""

feedback_question_2 = """
I think the most challenging part for me is to use backtracing to 
find the path. I spent a lot of time on it and finally figured out.
"""

feedback_question_3 = """
I like that problem has a GUI which can help us debug and play with.
Some of the describtion in the handout is not very clear, I think it can be improved.
"""
