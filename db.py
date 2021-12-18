import sqlite3 as lite
import os
import re
import string
import kenlm




DB_SENTENCE_RECORD_FIELDS = "sent text"
DB_UNIGRAM_RECORD_FIELDS = "score double, unigram text"

NGRAM = None
UTT = None

class LModel:
    model = None     
def mycmp(a,b):
    return -1*(cmp(LModel.model.score(a,bos=True,eos=False),LModel.model.score(b,bos=True,eos=False)))



class BaseDb:

    def __init__(self,dbName):
        pass

    def populate(self,tblName,fileName):
        raise SystemError("BaseDB::populate abstract class, implementation not implemented!")

    def getData(self,tblName,term):
        raise SystemError("BaseDB::getData abstract class, implementation not implemented!")
        


class UniDb(BaseDb):
    

    ONEGRAM = "1-grams"
    TWOGRAM = "2-grams"
    THREEGRAM = "3-grams"
    FOURGRAM = "4-grams"
    FIVEGRAM = "5-grams"
    
    def __init__(self,dbName,tblName=""):
        self.con_ = lite.connect("./"+dbName)
        self.cur_ = self.con_.cursor()
        self.tblName = tblName
        self.dbName = dbName

    def populate(self,tblName,fileName):
        if os.path.isfile(fileName) == False:
            raise SystemError("UniDb::populate : Not a valid file")

        self.tblName = tblName
        infile = file(fileName, "r")
        self.cur_.execute("drop table if exists "+tblName)
        self.cur_.execute("create table "+tblName+"("+DB_UNIGRAM_RECORD_FIELDS+")")
        
        dat = []

        
        while infile.readline().find(UniDb.THREEGRAM) == -1:
            pass

        line = infile.readline()
        

        while line.find("-grams") == -1 and line != "":
            
            l = re.findall("[0-9a-z\.-<>\\\/]+",line)
            
            if len(l) == 5:
                #dat.append((l[0],l[1]))
                dat.append((l[0],l[1]+" "+l[2]+" "+l[3]))
            line = infile.readline()
            #print line
        

        for e in dat:
            self.cur_.execute("insert into "+tblName+" values"+str(e))

        infile.close()
        self.con_.commit()
        self.con_.close()

    def getData(self,term):

        self.con_ = lite.connect("./"+self.dbName)
        self.cur_ = self.con_.cursor()

        orig_term = term.split(" ")
        if len(orig_term) < 4:
            orig_term = ""
            t = term
        else:
            try:
               #t = orig_term.pop()
                t = orig_term[2:len(orig_term)]
                t = string.join(t)
                orig_term = orig_term[0:2]
                orig_term=string.join(orig_term)+" "
            except:
                t = term
                orig_term=""


   
        self.cur_.execute("select unigram from "+self.tblName+" where unigram like '"+t+"%' order by score desc limit 4")

        rows = self.cur_.fetchall()
        res = []
        for e in rows:
            res.append(orig_term+str(e[0]))

        self.con_.close()
        return (res)



class SentenceDb(BaseDb):

    def __init__(self,dbName,tblName=""):
        self.con_ = lite.connect("./"+dbName)
        self.cur_ = self.con_.cursor()
        self.tblName = tblName
        self.dbName = dbName

    def populate(self,tblName,fileName):
        if os.path.isfile(fileName) == False:
            raise SystemError("SentenceDb::populate : Not a valid file")
        self.tblName = tblName
        infile = file(fileName, "r")
        self.cur_.execute("drop table if exists "+tblName)
        self.cur_.execute("create table "+tblName+"("+DB_SENTENCE_RECORD_FIELDS+")")
        
        dat = []

        line = infile.readline()
        #print line

        while line != "":
            tmp = []
            tmp.append(line.strip("\n"))
            dat.append(tuple(tmp))
            line = infile.readline()
            #print line
                
        for e in dat:
            #print "insert into "+tblName+" values("+e[0]+")"
            self.cur_.execute("insert into "+tblName+" values(\""+e[0]+"\")")

        infile.close()
        self.con_.commit()
        self.con_.close()



    def getData(self,term):

        self.con_ = lite.connect("./"+self.dbName)
        self.cur_ = self.con_.cursor()

        self.cur_.execute("select sent, count(sent) as cnt from "+self.tblName+" where sent like '"+term+"%' group by sent order by cnt desc limit 4")

        rows = self.cur_.fetchall()
        res = []
        for e in rows:
            res.append(str(e[0]))

        self.con_.close()
        return (res)
    


def init(ngram,utterences):
    if os.path.isfile("./mygram") == False:
        NGRAM = UniDb("mygram","ngram")
        NGRAM.populate("ngram",ngram)
        UTT = SentenceDb("myutt","utterences")
        UTT.populate("utterences",utterences)
    else:
        NGRAM = UniDb("mygram","ngram")
        UTT = SentenceDb("myutt","utterences")        

    LModel.model = kenlm.Model(ngram)

    return (NGRAM,UTT)


def generate_completions_(dbs,term):
    res = []
    for e in dbs:
        res = res + e.getData(term)
    

    res.sort(mycmp)


    return (res)



def generate_completions(term):
    return generate_completions_((NGRAM,UTT),term.lower())

