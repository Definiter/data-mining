from pylab import *
import csv
import random
import matplotlib.pyplot as plt

data = []
attribute = [[] for i in range(4)]
with open('iris.data') as inputFile:
    csvData = csv.reader(inputFile)
    for line in csvData:
        for i in range(4):
            attribute[i].append(float(line[i]))

plt.scatter(attribute[0], attribute[1])

plt.show()
