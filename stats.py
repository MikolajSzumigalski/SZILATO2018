import matplotlib.pyplot as plt
import numpy as np
import sys
from math import exp

avg = []
max = []
index = []

filename = sys.argv[1]

with open(filename, 'r', encoding='utf-8') as infile:
    for line in infile:
        if line[0] == '#': continue
        line = list(map(int, line.split(' ')))
        index.append(line[0])
        avg.append(line[2])
        max.append(line[1])

plt.plot(index, max)
plt.plot(index, avg)
plt.show()
