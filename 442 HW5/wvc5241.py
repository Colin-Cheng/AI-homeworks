############################################################
# CMPSC 442: Homework 5
############################################################

student_name = "Wei Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import string
import random
import math

############################################################
# Section 1: Markov Models
############################################################

def tokenize(text):
    start = 0
    res = []
    
    for i in range(len(text)):
        if (text[i] == ' ' or text[i] == '\n') and (start == i):
            start = i+1
            continue
        elif (text[i] == ' 'or text[i] == '\n') and (start != i):
            res.append(text[start:i])
            start = i+1
        elif (text[i] in string.punctuation) and (start == i):
            res.append(text[i])
            start = i+1
        elif (text[i] in string.punctuation) and (start != i):
            res.append(text[start:i])
            res.append(text[i])
            start = i+1

    if (start<=i):
        res.append(text[start:])
        
    return res
             

def ngrams(n, tokens):
    res = []
    for i in range(len(tokens)):
        inner_tuple = []
        for j in range(i-n+1,i):
            if j<0:
                inner_tuple.append('<START>')
            else:
                inner_tuple.append(tokens[j])
        res.append((tuple(inner_tuple),tokens[i]))
    inner_tuple = []
    for i in range(len(tokens)-n+1,len(tokens)):
        if i<0:
            inner_tuple.append('<START>')
        else:
            inner_tuple.append(tokens[i])
    res.append((tuple(inner_tuple),'<END>'))
    return res
            

class NgramModel(object):

    def __init__(self, n):
        self.n = n
        self.data = {}
        self.total = {}

    def update(self, sentence):
        tokens = tokenize(sentence)
        l = ngrams(self.n, tokens)
        for c,t in l:
            if c in self.data:
                self.total[c] += 1
                if t in self.data[c]:
                    self.data[c][t] += 1
                else:
                    self.data[c][t] = 1
            else:
                self.data[c] = {t:1}
                self.total[c] = 1

    def prob(self, context, token):
        if context not in self.data:
            return 0
        elif token not in self.data[context]:
            token_count = 0
            total_count = self.total[context]
        else:
            token_count = self.data[context][token]
            total_count = self.total[context]
        prob = token_count/total_count
        return prob

    def random_token(self, context):
        T = sorted(self.data[context].keys())
        prob_sum = 0
        r = random.random()
        for i in range(len(T)):
            prob_sum += self.prob(context,T[i])
            if prob_sum > r:
                return T[i]

    def random_text(self, token_count):
        res = []
        n = self.n
        context = ['<START>' for i in range(n-1)]
        for i in range(token_count):
            rt = self.random_token(tuple(context))
            res.append(rt)
            if n==1:
                continue
            if rt == '<END>':
                context = ['<START>' for i in range(n-1)]
            else:
                context.pop(0)
                context.append(rt)
        return ' '.join(res)

    def perplexity(self, sentence):
        tokens = tokenize(sentence)
        m = len(tokens)
        l = ngrams(self.n, tokens)

        prob_log = 0
        for c,t in l:
            prob_log -= math.log(self.prob(c,t))

        perplex = math.pow(math.exp(prob_log),1/(m+1))
        return perplex

def create_ngram_model(n, path):
    m = NgramModel(n)
    file = open(path,'r')
    lines = file.readlines()

    for line in lines:
        m.update(line)
        
    return m

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5 hours
"""

feedback_question_2 = """
It was sometimes hard to understand the problem. There was no
significant stumbling blocks.
"""

feedback_question_3 = """
I like the assignment helped me review markov model. I think
more test cases can be given to help us understand the problem.
"""
