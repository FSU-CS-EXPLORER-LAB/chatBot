#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 03:03:37 2020

@author: saptarshibhowmik
"""

#Meet Robo: your friend

#import necessary libraries
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import socket
import re

try:
    from urllib import quote, urlopen, urlencode  # Python 2.X
except ImportError:
    from urllib.parse import quote, urlencode  # Python 3+
    from urllib.request import urlopen  # Python 3+
    
warnings.filterwarnings('ignore')

import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
nltk.download('punkt') # first-time use only
nltk.download('wordnet') # first-time use only

#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]


REPEAT_INPUTS = ("don't","understand", "sorry", "pardon me")
REPEAT_RESPONSES = ["hi I am glad! You are talking to me, I will repeat", "will go over the things again"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)
        
def repeating(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in REPEAT_INPUTS:
            return random.choice(REPEAT_RESPONSES)


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


    
    
def submitInformation(url,parameters):
    encodedParams  = dictionary2URI(parameters);    # encode the parameters
    encodedParams = encodedParams.encode('utf-8')
    net = urlopen(url,encodedParams);        # Post the data.
    return(net.read());                             # return the result.


def dictionary2URI(theDictionary) :

    encoded = '';           # Initialize the string to return
    for key, value in theDictionary.items():

        # Encode each item in the dictionary.
        encoded += quote(key)+"="+quote(value)+"&";
    remove = re.compile('&$')             # Remove the trailing ampersand.
    encoded = remove.sub('',encoded);
    return(encoded);
    
def parseRecvMsg(info):
        append_flag = ''
        messages = ''
        allMsg = []
        allMsg = info.split('~')
        append_flag = allMsg[0]
        messages = allMsg[1]
#        append_flag.append(.split(':')[0])
#        messages.append(i.split(':')[1])
        return (append_flag,messages)

def nlpAnalyzer(sentence, append=0):
    user_response = sentence
    user_response=user_response.lower()
    flag=True
    nlp_analyzer_output = []
    if append == 1:
        with open("chatbot.txt", "a") as myfile:
            myfile.write("\n"+ user_response)
        
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            nlp_analyzer_output = ['You are welcome..']
        else:
            if(greeting(user_response)!=None):
                nlp_analyzer_output = [greeting(user_response)]
                nlp_analyzer_output.append('/320001 -greeting')
            elif(repeating(user_response)!=None):  
                nlp_analyzer_output = [repeating(user_response)]
                nlp_analyzer_output.append('/320001 -repeat')
            else:
                statement = response(user_response)
                sent_tokens.remove(user_response)
                if statement == "I am sorry! I don't understand you":
                    nlp_analyzer_output = ["If you know the answer then type in the answer else type NO", '/320002']
                        
    else:
        flag=False
        nlp_analyzer_output = ['Bye! take care..']
    

url = ''
print("Please enter the url and name for the npc")
url = input('Enter the URL : ')
start_flag = 0




while(1):
    if start_flag == 0:
        start_flag = 1
        full_msg = 'Hi TA lets starts todays class, so can you tell me what do you want to do?'
        command = '00001'
        command_status = '1'
        parameters = {
                  'message':full_msg,
                  'command_status':command_status,
                  'command_message':command
                  }
        info = submitInformation(url,parameters);
        if info:
            info = info.decode("utf-8").strip()
            append_flag, msg = parseRecvMsg(info)
            nlp_output = nlpAnalyzer(msg, append_flag)
            if len(nlp_output) == 1:
                parameters = {
                  'message':nlp_output[0],
                  'command_status':'0',
                  'command_message':'0'
                  }
                info = submitInformation(url,parameters);
            elif len(nlp_output) == 2:
                parameters = {
                  'message':nlp_output[0],
                  'command_status':'1',
                  'command_message':nlp_output[1]
                  }
                info = submitInformation(url,parameters);
        
        
        

# Keyword Matching
'''
print('Start')
flag=True
while(flag==True):
    user_response = input()
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag=False
            print("ROBO: You are welcome..")
        else:
            if(greeting(user_response)!=None):
                print("ROBO: "+greeting(user_response))
            elif(repeating(user_response)!=None):  
                print("ROBO: "+repeating(user_response))
                print('next command by facil : /320001 -repeat')
            else:
                print("ROBO: ",end="")
                statement = response(user_response)
                print(statement)
                sent_tokens.remove(user_response)
                if statement == "I am sorry! I don't understand you":
                    print("If you know the answer then type in the answer else type NO")
                    answer = input()
                    if answer != 'NO':
                        with open("chatbot.txt", "a") as myfile:
                            myfile.write("\n"+ user_response + ' is ' + answer)
                        
    else:
        flag=False
        print("ROBO: Bye! take care..")  # -*- coding: utf-8 -*-
'''
