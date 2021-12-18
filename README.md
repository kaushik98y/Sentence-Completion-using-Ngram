## Sentence Completion using Ngram 

An NLP implementation of a sentence completion with language model.


### Requirements
-------------------------------------------------------
sqlite3, kenlm, nltk




### --------------------------------------------

1.) Offline data processing - create language model and sentence completion
                  

    EXECUTE:
    python parse.py ./sample_conversations.json ./utt.txt | ./lmplz -S 20% -o 5 > utt.arpa

    REQUIRES : json conversation training file, kenlm binary, 'lmplz' in 
                current directory

2.) Autocomplete -  perform sentence completion estimation from partial
                             words/phrases.

    EXECUTE:
    python generate_completions.py "is there"

    REQUIRES : './utt.txt' and '/utt.arpa' 

3.) Autocomplete server   - realtime autocomplete in an HTTP server,GET requests


     EXECUTE:
     python webs.py 13000 127.0.0.1 ./utt.arpa ./utt.txt

     http://localhost:13000/autocomplete?q=what

     REQUIRES:  './utt.txt' and '/utt.arpa' 
	       
