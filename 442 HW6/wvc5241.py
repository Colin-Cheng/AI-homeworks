############################################################
# CMPSC 442: Homework 6
############################################################

student_name = "Wei Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from math import log,exp

############################################################
# Section 1: Hidden Markov Models
############################################################

def load_corpus(path):
    res = []
    corpus = open(path,'r')
    lines = corpus.readlines()

    for line in lines:
        line = line.strip()
        l = line.split(" ")
        for i in range(len(l)):
            l[i] = tuple(l[i].split("="))
        res.append(l[:])
    return res 

def init_tag_prob(sentences):
    smoothing = 1e-10
    pi = {'NOUN':smoothing,'VERB':smoothing,'ADJ':smoothing,\
          'ADV':smoothing,'PRON':smoothing,'DET':smoothing,\
          'ADP':smoothing,'NUM':smoothing,'CONJ':smoothing,\
          'PRT':smoothing,'.':smoothing,'X':smoothing}
    
    sentences_count = len(sentences)
    
    for l in sentences:
        t = l[0][1]
        pi[t] += 1
            
    for t in pi:
        pi[t] = log(pi[t]/(sentences_count + 12*smoothing))
    return pi

def trans_prob(sentences,tags):
    res = {}
    smoothing = 1e-10
    all_tags = {'NOUN':smoothing,'VERB':smoothing,'ADJ':smoothing,\
                'ADV':smoothing,'PRON':smoothing,'DET':smoothing,\
                'ADP':smoothing,'NUM':smoothing,'CONJ':smoothing,\
                'PRT':smoothing,'.':smoothing,'X':smoothing,\
                '<TOTAL>':smoothing*12}
    
    for t in tags:
        res[t] = all_tags.copy()
        
    for l in sentences:
        i = 0
        while i+1 < len(l):
            t1 = l[i][1]
            t2 = l[i+1][1]
            res[t1][t2] += 1
            res[t1]['<TOTAL>'] += 1
            i += 1
            
    for t1 in res:
        total = res[t1].pop('<TOTAL>')
        
        for t2 in res[t1]:
            res[t1][t2] = log(res[t1][t2] / total)
    return res
            
def emission_prob(sentences):
    smoothing = 1e-10
    res = {'NOUN':{'<UNK>':0,'<TOTAL>':0},'VERB':{'<UNK>':0,'<TOTAL>':0},\
           'ADJ':{'<UNK>':0,'<TOTAL>':0},'ADV':{'<UNK>':0,'<TOTAL>':0},\
           'PRON':{'<UNK>':0,'<TOTAL>':0},'DET':{'<UNK>':0,'<TOTAL>':0},\
           'ADP':{'<UNK>':0,'<TOTAL>':0},'NUM':{'<UNK>':0,'<TOTAL>':0},\
           'CONJ':{'<UNK>':0,'<TOTAL>':0},'PRT':{'<UNK>':0,'<TOTAL>':0},\
           '.':{'<UNK>':0,'<TOTAL>':0},'X':{'<UNK>':0,'<TOTAL>':0}}
    
    for l in sentences:
        for t in l:
            tag_dic = res[t[1]]
            if t[0] in tag_dic:
                tag_dic[t[0]] += 1
            else:
                tag_dic[t[0]] = 1
            tag_dic['<TOTAL>'] += 1

    for tag in res:
        tag_dic = res[tag]
        total_word_count = tag_dic.pop('<TOTAL>')
        word_type_count = len(tag_dic)
    
        for w in tag_dic:
            tag_dic[w] = log((tag_dic[w] + smoothing) / (total_word_count + word_type_count*smoothing))

    return res
    
class Tagger(object):

    def __init__(self, sentences):
        self.tags = {'NOUN','VERB','ADJ','ADV','PRON','DET','ADP','NUM','CONJ','PRT', '.','X'}
        self.init_tag_prob = init_tag_prob(sentences)
        self.trans_prob = trans_prob(sentences,self.tags)
        self.emission_prob = emission_prob(sentences)
    
    def most_probable_tags(self, tokens):
        res = []

        for word in tokens:
            max_emis_prob = 0
            max_tag = None
            
            for t in self.tags:
                
                if word in self.emission_prob[t]:
                    emis_prob = exp(self.emission_prob[t][word])
                else:
                    emis_prob = exp(self.emission_prob[t]['<UNK>'])

                if emis_prob > max_emis_prob:
                    max_emis_prob = emis_prob
                    max_tag = t
                    
            res.append(max_tag)
        return res
            
    def find_max(self, delta, curtag, i):
        max_value = 0
        max_last_tag = None

        for t in self.tags:
            cur_value = exp(delta[i-1][t] + self.trans_prob[t][curtag])
            if cur_value > max_value:
                max_value = cur_value
                max_last_tag = t
                
        return log(max_value),max_last_tag
        
    def viterbi_tags(self, tokens):

        #initialization
        delta = {}
        path = {}
        tag = {'NOUN':0,'VERB':0,'ADJ':0,'ADV':0,'PRON':0,'DET':0,\
               'ADP':0,'NUM':0,'CONJ':0,'PRT':0,'.':0,'X':0}

        for i in range(len(tokens)):
            delta[i] = tag.copy()
            path[i] = tag.copy()
            
        for t in self.tags:
            if tokens[0] in self.emission_prob[t]:
                delta[0][t] = self.init_tag_prob[t] + self.emission_prob[t][tokens[0]]
            else:
                delta[0][t] = self.init_tag_prob[t] + self.emission_prob[t]['<UNK>']

        #calculate delta and path
        for i in range(1,len(tokens)):
            for t in self.tags:
                max_value,max_last_tag = self.find_max(delta, t, i)
                if tokens[i] in self.emission_prob[t]:
                    delta[i][t] = max_value + self.emission_prob[t][tokens[i]]
                else:
                    delta[i][t] = max_value + self.emission_prob[t]['<UNK>']
                path[i][t] = max_last_tag
                
        #backtrack
        res = []
        last = len(tokens)-1
        max_value = 0
        last_tag = None
        
        for t in self.tags:
            cur_value = exp(delta[last][t])
            if cur_value > max_value:
                max_value = cur_value
                last_tag = t
                
        res.append(last_tag)
        for i in range(last,0,-1):
            cur_tag = path[i][last_tag]
            res.insert(0,cur_tag)
            last_tag = cur_tag
        
        return res

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5 hours
"""

feedback_question_2 = """
I think the most challenging part of this assignment
is to implement the Viterbi decoding algorithm.
"""

feedback_question_3 = """
I think this is great. There is nothing to change.
"""
