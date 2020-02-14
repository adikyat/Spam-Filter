'''
Created on Aug 5, 2019

@author: Aditya Kyatham
'''
import os
from collections import Counter
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split as tts
from sklearn.metrics import accuracy_score
import cPickle as c #used serialization of objects , for saving & loading program


def save(clf, name):
    with open(name, 'wb') as fp: #wb write in binary
        c.dump(clf, fp)
    print "saved"
    

def make_dict():

    direc="C:/email-data/"
    
    files = os.listdir(direc)
  
    emails = [direc + email for email in files] #all email files in an array
    
    words=[]
    
    c =  len(emails)
    
    for email in emails:
        f = open(email) #each email file is opened
        blob = f.read()
        words+= blob.split() #each email files words are stored
        print c
        c-=1
    for i in range(len(words)):
        if not words[i].isalpha(): #non-alphabets are distinguished as ""
            words[i] = ""    
    dictionary = Counter(words) 
    del dictionary[""] #non-alphabets are deleted
    return dictionary.most_common(3000) #3000 frequently occuring words are picked.

def make_dataset(dictionary):
    direc="C:/email-data/"
    
    files = os.listdir(direc) #again extracting
    emails = [direc + email for email in files]
    
    feature_set =[]
    labels=[]
    
    c =  len(emails)
    
    for email in emails: #for each email file
        data=[]
        f = open(email)
        words = f.read().split(' ')
        for entry in dictionary:
            data.append(words.count(entry[0])) #each common word in dictionary is compared with each word in a single email file and 
            #concentration of that word in that particular email file is known.
        feature_set.append(data)#hence this set will contain concentration of various common words among various email files , thus these r features
        if "ham" in email:
            labels.append(0) # now at the same time , for one email file , features are appended to feature_set, and whether it is spam or not 
            # that  is info is appended to labels.
        if "spam" in email:
            labels.append(1)
        print c
        c=c-1
    
    return feature_set,labels
d = make_dict()
features, labels = make_dataset(d)

x_train, x_test, y_train, y_test = tts(features, labels, test_size=0.2) #test data is 20% and training is 80%

clf = MultinomialNB()
clf.fit(x_train,y_train) #here the classifier will see first the concentration of a word in a email file and then check whether that email file is
# is a spam or ham , if spam then it will learn it and blacklist it and viceversa.

preds = clf.predict(x_test)# machine started running its algorithm based upon its learning.
print accuracy_score(y_test, preds)#Some words could appear in both ham and spam , so sometimes there would be mismatch eg:"the".
#So, to calc accuracy , here preds is our machine's prediction and y_test is the actual answer key.

save(clf, "text-classifier.mdl") #saves all the work of spam/not spam
            
    
    
