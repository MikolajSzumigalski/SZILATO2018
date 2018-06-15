from id3 import Id3Estimator, export_graphviz, export_text
import numpy as np
import linecache
import csv
def Tree():
    names = [
        "tarcza",
        "czy lata",
        "wiek",
        "zbroja",
        "hp",
        "level",
        "potwor"
    ]

    count = len(open('przypadki.txt', 'rU').readlines())
    x = []

    for i in range (1, count):
        line = linecache.getline('przypadki.txt', i).split(" ")
        line[6] = str(line[6][0])
        x.append(line)
    X = np.asarray(x)
    print(X)

    y = np.array([int(i) for i in linecache.getline('wyniki.txt', 1)[:-2]])
    yd = [int(i) for i in linecache.getline('wyniki.txt', 1)[:-2]]
    d = []
    d.append(names)
    d[0].append("wynik")
    for i in range(0, len(yd)):
        d.append(x[i] + [yd[i]])
    print(d)
    clf = Id3Estimator()
    clf.fit(X, y, check_input=True)
    #d = np.array([['0', '0', '39', '1', '9', '0','1', 't']])
    #print(d)
    #c = clf.predict(d)
    #print(c)

    export_graphviz(clf.tree_, "out.dot", names)
    print(export_text(clf.tree_, names))
    return clf
