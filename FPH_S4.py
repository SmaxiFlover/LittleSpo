import xml.sax
from constants import *
from harmony import *
import os

rng = [(0, 0), (0, 0), (0, 0), (0, 0)]

class FPHHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.name = ""
        self.left = 0
        self.right = 0

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "range":
            self.name = attributes["name"]

    def endElement(self, tag):
        if self.CurrentData == "soprano":
            rng[3] = (self.left, self.right)
        elif self.CurrentData == "alto":
            rng[2] = (self.left, self.right)
        elif self.CurrentData == "tenor":
            rng[1] = (self.left, self.right)
        elif self.CurrentData == "bass":
            rng[0] = (self.left, self.right)
        self.CurrentData = ""

    def calLeftAndRight(self, strng):
        temp_str = strng.split(',')
        self.left = keyToInt(temp_str[0])
        self.right = keyToInt(temp_str[1])

    def characters(self, content):
        if self.CurrentData == "soprano":
            self.calLeftAndRight(content)
        elif self.CurrentData == "alto":
            self.calLeftAndRight(content)
        elif self.CurrentData == "tenor":
            self.calLeftAndRight(content)
        elif self.CurrentData == "bass":
            self.calLeftAndRight(content)

def read4PHRange():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = FPHHandler()
    parser.setContentHandler( Handler )
    parser.parse("FPH_range.xml")

s4ph = []

def outputS4PH(os4ph):
    for i in os4ph:
        print intToKey(i),
    print

def generateS4PH():
    readHarmony()
    tmps4ph = [0, 0, 0, 0]
    hmny = H_ARR[0]
    #print rng

    def isSuitableKey(i, key):
        res = False
        if (i == 0):
            res = ((key - hmny.root) % 12 == 0)
        else:
            for ik in hmny.keys:
                if ((key - ik) % 12 == 0):
                    res = True
        '''
        if (res and hmny.root != 0):
            hmny.output()
            print i, intToKey(key), key
            print hmny.keys
            print key - hmny.root
            print res
            print
            os.system("pause")
        '''

        return res

    def checkS4PH():
        for i in hmny.importance:
            impk = hmny.keys[i]
            flag = False
            for j in tmps4ph:
                if ((j - impk) % 12 == 0):
                    flag = True
                    break
            if (not flag):
                return False
        d1 = tmps4ph[1] - tmps4ph[0]
        d2 = tmps4ph[2] - tmps4ph[1]
        d3 = tmps4ph[3] - tmps4ph[2]
        kset = set()
        for i in tmps4ph:
            kset.add(i % 12)
        ksz = len(kset)
        if not (((d2 <= 6) and (d3 <= 6)) or ((d2 >= 5) and (d3 >= 5))):
            return False
        if (d2 > 12 or d3 > 12):
            return False
        if (ksz <= 2 and tmps4ph[0] < keyToInt("C2") and d1 <= 5):
            return False
#        if (d1 == 0):
#            return True
#        if (tmps4ph[1] > keyToInt("G2")):
#            return True
#        if (d2 + 6 < d3 or d1 + 6 < d3):
#            return False
        return True

    def dfsS4PH(i, bf):
        if (i == 4):
            if (checkS4PH()):
                s4ph[hmny.idx].append(tuple(tmps4ph))
            #    print "=============="
            #    hmny.output()
            #    print toKeyName(tmps4ph)
            return
        for tmps4ph[i] in range(max(bf, rng[i][0]), rng[i][1]+1):
            if (isSuitableKey(i, tmps4ph[i])):
                dfsS4PH(i+1, tmps4ph[i])

    for hmny in H_ARR:
        s4ph.append([])
        tmpS4PH = [0, 0, 0, 0]
        dfsS4PH(0, 0)

    #print s4ph

def FPHS4():
    read4PHRange()
    '''
    for i in rng:
        print i
        print intToKey(i[0]), intToKey(i[1])
    '''
    generateS4PH()

if ( __name__ == "__main__"):
    FPHS4()
