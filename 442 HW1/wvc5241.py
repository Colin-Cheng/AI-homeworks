############################################################
# CMPSC 442: Homework 1
############################################################

student_name = "Wei Cheng"

############################################################
# Section 1: Python Concepts
############################################################

python_concepts_question_1 = """
Strongly typed means that every object has a fixed type, interpreter 
doesn’t allow things incompatible with that type.
example: >>>'foo' + 2 
         this will give type error

Dynamically typed means that the type of the object a variable will 
name is not specified at compile time.
example: >>> x = "foo"
         >>> x = 2
         this is fine in python
"""

python_concepts_question_2 = """
The problem is that the keys of a dictionary must be immutable types.
However, in this case, list is a mutable type. 
One solution is to use tuple instead of list, because tuple is immutable.
"""

python_concepts_question_3 = """
concatenate2 is better.
Because that strings are immutable and can't be changed in place.
So, concatenate1 generates a lot of new strings. 
However, concatenate2 only generates one new string by inserting spaces.
"""

############################################################
# Section 2: Working with Lists
############################################################

def extract_and_apply(l, p, f):
    return [f(x) for x in l if p(x)]

def concatenate(seqs):
    return [y for x in seqs for y in x]

def transpose(matrix):
    m = len(matrix)
    n = len(matrix[0])
    row = [0 for x in range(m)]
    transpose = [row[:] for x in range(n)]
    for i in range(m):
        for j in range(n):
            transpose[j][i] = matrix[i][j]
    return transpose


############################################################
# Section 3: Sequence Slicing
############################################################

def copy(seq):
    return seq[:]

def all_but_last(seq):
    return seq[:-1]

def every_other(seq):
    return seq[::2]

############################################################
# Section 4: Combinatorial Algorithms
############################################################

def prefixes(seq):
    for i in range(len(seq)+1):
        yield seq[:i]

def suffixes(seq):
    for i in range(len(seq)+1):
        yield seq[i:]

def slices(seq):
    for i in range(len(seq)+1):
        for j in range(i+1,len(seq)+1):
            yield seq[i:j]

############################################################
# Section 5: Text Processing
############################################################

def normalize(text):
    ans = ''
    text = text.strip().lower()
    for i in text:
        if i != ' ' or ans[-1] != ' ':
            ans += i
    return ans 

def no_vowels(text):
    ans = ''
    vowels = ['a','e','i','o','u']
    for i in text:
        if i.lower() not in vowels:
            ans += i
    return ans


def digits_to_words(text):
    ans = []
    num = {'0':'zero', '1':'one', '2':'two', '3':'three', '4':'four',\
           '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}
    for i in text:
        if i in num:
            ans.append(num[i])
    ans = ' '.join(ans)
    return ans 


def to_mixed_case(name):
    n = name.split('_')
    for i in n[:]:
        if i == '':
            n.remove(i)

    for i in range(len(n)):
        if i == 0:
            n[i] = n[i].lower()
        else:
            n[i] = n[i].capitalize()

    return ''.join(n)



############################################################
# Section 6: Polynomials
############################################################
class Polynomial(object):

    def __init__(self, polynomial):
        self.polynomial = []
        for i in polynomial:
            self.polynomial.append(tuple(i))
        self.polynomial = tuple(self.polynomial)
        
    def get_polynomial(self):
        return self.polynomial

    def __neg__(self):
        new = []
        for x,y in self.polynomial:
            new.append((-x,y))
        return Polynomial(new)

    def __add__(self, other):
        new = self.polynomial + other.polynomial
        return Polynomial(new)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        new = []
        for a,b in self.polynomial:
            for c,d in other.polynomial:
                new.append((a*c,b+d))
        return Polynomial(new)

    def __call__(self, x):
        ans = 0
        for a,b in self.polynomial:
            ans += a* (x**b)
        return ans

    def simplify(self):
        new = []
        dic = {}
        for c,p in self.polynomial:
            if p in dic:
                dic[p] += c
            else:
                dic[p] = c
        for p,c in dic.items():
            if c!=0:
                new.append([p,c])
        new.sort()
        new.reverse()
        self.polynomial = []
        for p,c in new:
            self.polynomial.append((c,p))
            
        if len(self.polynomial) == 0:
            self.polynomial.append((0,0))
            
        self.polynomial = tuple(self.polynomial)

    def __str__(self):
        ans = []
        for c,p in self.polynomial:
            if p == 0 and c == 0:
                continue
            
            if c>=0:
                sign = '+'
            else:
                sign = '-'

            ans.append(sign)

            if c == 1 or c == -1:
                if p == 0:
                    term = '1'
                elif p == 1:
                    term = 'x'
                else:
                    term = 'x^' + str(p)
            else:   
                if p == 0:
                    term = str(abs(c))
                elif p == 1:
                    term = str(abs(c)) + 'x'
                else:
                    term = str(abs(c)) + 'x^' + str(p)
                    
            ans.append(term)

        if ans[0] == '+':
            ans.pop(0)
        elif ans[0] == '-':
            ans.pop(0)
            ans[0] = '-' + ans[0]
            
        ans = ' '.join(ans)
        return ans

############################################################
# Section 7: Feedback
############################################################

feedback_question_1 = """
two hours
"""

feedback_question_2 = """
I spent most of the time on problem 6. It took some time to
take all the cornor cases into consideration.
"""

feedback_question_3 = """
I like this assignment includes a lot of concepts in Python.
I think problems about *args, **kwargs and higer order function can also be added.
"""

