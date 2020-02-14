'''
Created on Aug 6, 2019

@author: Aditya Kyatham
'''
# detector is for detecting email spam or not as it is received in 
# in real time.
import cPickle as c
import os
from sklearn import *
from collections import Counter

def load(clf_file):
    with open(clf_file) as fp:
        clf = c.load(fp)
    return clf

def make_dict():
    direc = "C:/email-data/"
    files = os.listdir(direc)
    emails = [direc + email for email in files]
    words = []
    c = len(emails)

    for email in emails:
        f = open(email)
        blob = f.read()
        words += blob.split(" ")
        print c
        c -= 1

    for i in range(len(words)):
        if not words[i].isalpha():
            words[i] = ""

    dictionary = Counter(words)
    del dictionary[""]
    return dictionary.most_common(3000)

clf = load("text-classifier.mdl") #uses this data for detection

d = make_dict() #for again getting most common words and alpha.

while True:
    features = []
    inp = raw_input(">").split() 
    if inp[0] == "exit":
        break
    for word in d:
        features.append(inp.count(word[0])) # checking the concentration
        #of a word of dict in inp and append as feature.
    res = clf.predict([features]) #if features contains blacklisted 
    # word then it is spam as here clf has all the data of blacklisted words.
    
    print ["Not Spam", "Spam!"][res[0]]







