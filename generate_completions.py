#!/usr/bin/python
import db
import argparse
import os



if __name__=='__main__':
    cmdline = argparse.ArgumentParser(description='generate sentence completions')
    cmdline.add_argument('key_entry', type=str, help='Partial key type to generate sentence completion for')
    
    if os.path.isfile("./utt.txt") == False:
        SystemError("generate_completions.py : expected sentence completion utterence file ./utt.txt; Pls use parse.py to generate file and place in current directory")

    if os.path.isfile("./utt.arpa") == False:
        SystemError("generate_completions.py : expected Language model file ./utt.arpa; Pls use parse.py to generate file with kenlm and place in current directory")

    print "Initializing model"
    (db.NGRAM,db.UTT) = db.init("./utt.arpa","./utt.txt")
    args = cmdline.parse_args()    
    print "init done ..."
    print ""

    
    print "generate_completions('"+args.key_entry+"') => "+str(db.generate_completions(args.key_entry))



        
