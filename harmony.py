import xml.sax
from constants import *

def keyToInt(keystr):
    patch = 0
    if (keystr[0] == "#"):
        patch = 1
        keystr = keystr[1:]
    elif (keystr[0] == "b"):
        patch = -1
        keystr = keystr[1:]
    return patch + KEYN_TO_N[keystr[0]] + int(keystr[1]) * KEYN_NUMBER

def intToKey(keynum):
    keyn = keynum % KEYN_NUMBER
    leveln = keynum // KEYN_NUMBER
    return N_TO_KEYN[keyn] + str(leveln)

def toKeyName(tp):
    tmp = []
    for i in tp:
        tmp.append(intToKey(i))
    return tuple(tmp)

class HarmonyType:
    def __init__(self, name, type, keys, importance):
        self.name = name
        self.type = type
        self.keys = keys
        self.importance = importance

    def output(self):
        print "Name : ", self.name
        print "Type : ", self.type
        print "Keys : ",
        for key in self.keys:
            print KEY_NAME_123[self.type][key],
        print
        print "Importance : ",
        for i in self.importance:
            print KEY_NAME_123[self.type][self.keys[i]],
        print
        print

ht_arr = []

def printHArr():
    for i in ht_arr:
        i.output()

class HarmonyHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.CurrentData = ""
        self.name = ""
        self.type = ""
        self.keys = []
        self.importance = []

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "harmony":
            self.name = attributes["name"]

    def endElement(self, tag):
        if self.CurrentData == "importance":
            ht_arr.append(HarmonyType(self.name, self.type, self.keys, self.importance))
        self.CurrentData = ""

    def characters(self, content):
        if self.CurrentData == "type":
            self.type = content
        elif self.CurrentData == "keys":
            temp_str = content.split(',')
            self.keys = []
            for i in temp_str:
                self.keys.append(int(i))
        elif self.CurrentData == "importance":
            temp_str = content.split(',')
            self.importance = []
            for i in temp_str:
                self.importance.append(int(i))

class Harmony:
    def __init__(self, root, ht):
        self.idx = 0
        #self.root = root
        self.ht = ht
        self.name = KEY_NAME_ABC[root] + ht.name
        self.keys = []
        for i in ht.keys:
            self.keys.append((root + i) % KEY_NUMBER)
        self.root = self.keys[0]
        self.importance = ht.importance

    def output(self):
        print "Name : ", self.name
        print "Root : ", N_TO_KEYN[self.root]
        print "Keys : ",
        for key in self.keys:
            print KEY_NAME_ABC[key],
        print
        print "Importance : ",
        for i in self.importance:
            print KEY_NAME_ABC[self.keys[i]],
        print
        print

H_ARR = []
H_N_MAP = {}

def generateHarmonyNameMap():
    for i in H_ARR:
        pn = ""
        if (i.name.find('/') == -1):
            pn = i.name
        else:
            s = i.name.split('/')
            k = i.root
            c = N_TO_KEYN[k]
            s[1] = c
            pn = s[0] + "/" + s[1]

    #    print pn, ":"
    #    i.output()
        H_N_MAP[pn] = i

def readHarmony():
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = HarmonyHandler()
    parser.setContentHandler( Handler )
    parser.parse("harmony_database.xml")

    k = 0
    for i in range(0, 12):
        for j in ht_arr:
            H_ARR.append(Harmony(i, j))
            H_ARR[k].idx = k
            k += 1

    generateHarmonyNameMap()
    #Harmony(i, j).output()

if ( __name__ == "__main__"):
    readHarmony()
