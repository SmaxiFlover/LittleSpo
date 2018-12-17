from constants import *
from harmony import *
from FPH_S4 import *

h = []
a = []
res = []
n = 0
inputstr1 = ""

task_name = ""

def readTaskName():
    tfile = open("task_name.txt", "r")
    global task_name
    task_name = tfile.readline()
    while (task_name[len(task_name) - 1] == "\n"):
        task_name = task_name[ : len(task_name)-1]

def inputData():
    input_file = open("test/"+task_name+".txt", "r")
    tmp_str = input_file.readline()
    global inputstr1
    inputstr1 = tmp_str
    tmp_str = tmp_str[ : len(tmp_str)-1]
    cnt = 0
    for i in tmp_str.split('\t'):
        if (i == "-"):
            h.append(h[cnt - 1])
        else:
            h.append(H_N_MAP[i])
        cnt += 1
    global n
    n = len(h)

    tmp_str = input_file.readline()
    tmp_str = tmp_str[ : len(tmp_str)-1]
    cnt = 0
    for i in tmp_str.split('\t'):
        if (i == "-"):
            a.append(a[cnt - 1])
        else:
            a.append([-1, -1, -1, keyToInt(i)])
        cnt += 1

    for j in range(2, -1, -1):
        tmp_str = input_file.readline()
        if (len(tmp_str) > 1):
            tmp_str = tmp_str[ : len(tmp_str)-1]
            k = 0
            for i in tmp_str.split('\t'):
                if (i == "-"):
                    a[k][j] = a[k-1][j]
                elif (len(i) > 1):
                    a[k][j] = keyToInt(i)
                k += 1

    input_file.close()

f = []
nxt = []

def outputResult(error_k):
    output_file = open("test/"+task_name+"__.txt", "w")
    tn = n
    if (error_k >= 0):
        output_file.write("T_T I cannot do it >_<\n")
        output_file.write("T_T I found difficulty at #" + str(error_k+1) + " harmony/melody >_<\n")
        tn = error_k

    f_min = N_PIANO_KEYS * tn
    h_min = (0, 0, 0, 0)
    for hi, fi in f[tn-1].items():
        if (fi < f_min):
            f_min = fi
            h_min = hi

    global res
    res = a

    for i in range(tn-1, 0, -1):
        res[i] = h_min
        h_min = nxt[i][h_min]

    res[0] = h_min

    output_file.write(inputstr1)
    for j in range(3, -1, -1):
        for i in range(0, tn):
            if (i > 0 and res[i][j] == res[i-1][j]):
                output_file.write("-\t")
            else:
                output_file.write(intToKey(res[i][j])+"\t")
        output_file.write("\n")
    output_file.close()

def isCertain(keyarr):
    for i in keyarr:
        if (i == -1):
            return False
    return True

def hasKey(keyarr, hmny):
    for i in range(0, 4):
        if (keyarr[i] >= 0 and keyarr[i] != hmny[i]):
            return False
    return True

def checkF4PHConnection(h1, h2):
    if (not (h2[0] <= h1[1])):
        return False
    if (not (h2[1] <= h1[2] and h2[1] >= h1[0])):
        return False
    if (not (h2[2] <= h1[3] and h2[2] >= h1[1])):
        return False
    if (not (h2[3] >= h1[2])):
        return False

    d = [0, 0, 0, 0]
    for i in range(0, 4):
        d[i] = h2[i] - h1[i]
    if (d[0] < 0 and d[1] < 0 and d[2] < 0 and d[3] < 0):
        return False
    if (d[0] > 0 and d[1] > 0 and d[2] > 0 and d[3] > 0):
        return False

    if (d[0] > 7):
        return False

    return True

def distBetweenF4PH(h1, h2):
    dst = 0
    for i in range(0, 4):
        dst += abs(h1[i] - h2[i])
    return dst

def dynamicProgramming():
    f.append({})
    nxt.append({})
    flag = False

    if (isCertain(a[0])):
        f[0][tuple(a[0])] = 0
        flag = True
    else:
        for i in s4ph[h[0].idx]:
            if (hasKey(a[0], i)):
                f[0][i] = 0
                flag = True

    if (not flag):
        outputResult(0)
        return

    for i in range(1, n):
        #print toKeyName(a[i])
        f.append({})
        nxt.append({})
        flag = False

        if (isCertain(a[i]) and isCertain(a[i-1])):
            hi = tuple(a[i])
            hj = tuple(a[i-1])
            f[i][hi] = f[i-1][hj] + distBetweenF4PH(hj, hi)
            nxt[i][hi] = hj
            flag = True
            continue

        if (isCertain(a[i])):
            hi = tuple(a[i])
            for hj, fj in f[i-1].items():
                if (checkF4PHConnection(hj, hi)):
                    df = fj + distBetweenF4PH(hj, hi)
                    flag = True
                    if (hi in f[i]):
                        if (df < f[i][hi]):
                            f[i][hi] = df
                            nxt[i][hi] = hj
                    else:
                        f[i][hi] = df
                        nxt[i][hi] = hj
            if (not flag):
                outputResult(i)
                return
            continue

        for hi in s4ph[h[i].idx]:
            if (not hasKey(a[i], hi)):
                continue
            for hj, fj in f[i-1].items():
                if (checkF4PHConnection(hj, hi)):
                    df = fj + distBetweenF4PH(hj, hi)
                    flag = True
                    if (hi in f[i]):
                        if (df < f[i][hi]):
                            f[i][hi] = df
                            nxt[i][hi] = hj
                    else:
                        f[i][hi] = df
                        nxt[i][hi] = hj
        '''
        print "======",i,"====="
        for hi, fi in f[i].items():
            print toKeyName(hi), ":", fi
        '''
        if (not flag):
            outputResult(i)
            return

    outputResult(-1)

if ( __name__ == "__main__"):
    readTaskName()
    FPHS4()
    inputData()
    dynamicProgramming()
    print "Done."
