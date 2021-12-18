#!/usr/bin/python

import nltk
import argparse
import os
import re
import json




def isValid(elem):
    res = False
    CUSTOMER_KEY = 'IsFromCustomer'
    if elem[CUSTOMER_KEY] == True:
        return res
    else:
        return True

def getText(elem):
    s = ""
    TEXT_KEY = 'Text'
    if isValid(elem) == True:
        s = elem[TEXT_KEY]
    return s



def readJson(fileName):
    obj = json.loads(file(fileName,"r").read())
    return obj


def preprocessStr(s):
    if s != "":
        fs = ""
        vals = re.findall("[A-Za-z0-9\;\'\-\s]+",s)
        try:
            #print vals
            for e in vals:
                if e != '':
                    fs = fs + e.lower().strip(" ")+"\n"
        except:
            pass
        if fs != "":
            s = fs
    #else:
    #s = s+"\n"
    return s




def createDataSet(obj):
    ds = ""
    ISSUES = 'Issues'
    MESSAGES = 'Messages'
    l = obj[ISSUES]
    

    for e in l:
        for m in e[MESSAGES]:
            ds = ds + preprocessStr(getText(m))
            #ds = ds + " "+getText(m)
    
    return (ds)

if __name__=='__main__':
    cmdline = argparse.ArgumentParser(description='Model training file Generator')
    cmdline.add_argument('json_infile', type=str, help='Sample Conversation Json file name and path, eg. ./sample_conversations.json')
    cmdline.add_argument('osent_file', type=str, help='name and path of output sentence training file, eg. ./utt.txt')
    args = cmdline.parse_args()

    js=readJson(args.json_infile)
    ofile = file(args.osent_file,"w")
    ofile.write(createDataSet(js))
    
    ofile.close()
    ifile = file(args.osent_file,"r")
    for line in ifile:
        for sentence in nltk.sent_tokenize(line):
            print(' '.join(nltk.word_tokenize(sentence)).lower())

    ifile.close()

    
