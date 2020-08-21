############################################################
# CMPSC442: Homework 4
############################################################

student_name = "Wei Cheng"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import email
import math
import os

############################################################
# Section 1: Spam Filter
############################################################

def load_tokens(email_path):
    tokens = []
    file_obj = open(email_path,'r')
    message = email.message_from_file(file_obj)
    for line in email.iterators.body_line_iterator(message):
        l = line.split()
        tokens.extend(l)
    return tokens

def log_probs(email_paths, smoothing):
    p = {}
    total_count = 0
    for ep in email_paths:
        tokens = load_tokens(ep)
        total_count += len(tokens)
        for t in tokens:
            if t in p:
                p[t] += 1
            else:
                p[t] = 1
    v = len(p)
    for t,count in p.items():
        p[t] = math.log((count+smoothing)\
                        /(total_count + smoothing * (v+1)))
    p["<UNK>"] = math.log(smoothing\
                        /(total_count + smoothing * (v+1)))
    return p
        
    

class SpamFilter(object):

    def __init__(self, spam_dir, ham_dir, smoothing):
        spams = []
        hams = []
        for i in os.listdir(spam_dir):
            spams.append(spam_dir + '/' + i)
        for i in os.listdir(ham_dir):
            hams.append(ham_dir + '/' + i)
            
        self.spam_log_probs = log_probs(spams,smoothing)
        self.ham_log_probs = log_probs(hams,smoothing)
        self.spam_prob = len(spams) / (len(spams) + len(hams))
        self.ham_prob = len(hams) / (len(spams) + len(hams))
    
    def is_spam(self, email_path):
        tokens = load_tokens(email_path)
        spam_p = math.log(self.spam_prob)
        ham_p = math.log(self.ham_prob)

        for t in tokens:
            if t in self.spam_log_probs:
                spam_p += self.spam_log_probs[t]
            else:
                spam_p += self.spam_log_probs["<UNK>"]
        
            if t in self.ham_log_probs:
                ham_p += self.ham_log_probs[t]
            else:
                ham_p += self.ham_log_probs["<UNK>"]
        if spam_p >= ham_p:
            return True
        else:
            return False
                
    def most_indicative_spam(self, n):
        res = []
        indications = []
        for w in self.spam_log_probs:
            if (w in self.ham_log_probs) and (w != "<UNK>"):
                indi_value = math.log((math.exp(self.spam_log_probs[w]))\
                                      / ((self.spam_prob * math.exp(self.spam_log_probs[w]))+(self.ham_prob * math.exp(self.ham_log_probs[w]))))
                indications.append([indi_value,w])
                
        indications.sort(reverse=True)

        for i in range(n):
            res.append(indications[i][1])
        return res

    def most_indicative_ham(self, n):
        res = []
        indications = []
        for w in self.spam_log_probs:
            if (w in self.ham_log_probs) and (w != "<UNK>"):
                indi_value = math.log((math.exp(self.ham_log_probs[w]))\
                                      / ((self.spam_prob * math.exp(self.spam_log_probs[w]))+(self.ham_prob * math.exp(self.ham_log_probs[w]))))
                indications.append([indi_value,w])
                
        indications.sort(reverse=True)

        for i in range(n):
            res.append(indications[i][1])
        return res

############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
5 hours
"""

feedback_question_2 = """
I find it is sometimes hard to understand what the problems are
asking for. I spent a lot of time on understanding the problems
and how to compute the value I want.
"""

feedback_question_3 = """
I like we have those real data available.
I think more detailed problem description and more test cases can
be given, to help us better understand the problem.
"""
