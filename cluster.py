import csv
import math
import random
import copy
import itertools

clusterSum = 3

class Vector:
    v = []
    num = 0
    category = ''
    cluster = -1
    def __init__ (self, v, num = 0, category = -1):
        self.v = v
        self.num = num
        self.category = category
    def normalize(self):
        length = 0
        for feature in self.v:
            length += feature * feature
        length = length ** 0.5
        if length != 0:
            for i in range(len(self.v)):
                self.v[i] /= length
        else:
            print 'Zero vector found.'
    def euclideanDistance(self, vector2):
        distance = 0
        for i in range(len(self.v)):
            distance += (self.v[i] - vector2.v[i]) ** 2
        distance = distance ** 0.5
        return distance
    def cosineDistance(self, vector2):
        distance = 0
        for i in range(len(self.v)):
            distance += self.v[i] * vector2.v[i]
        return distance

'''
#iris
def inputData():
    data = []
    with open('iris.data') as inputFile:
        csvData = csv.reader(inputFile)
        for i, line in enumerate(csvData):
            data.append(Vector(map(float, line[0:4]), i, line[4]))
    return data
'''
#wine
def inputData():
    data = []
    with open('wine.data') as inputFile:
        csvData = csv.reader(inputFile)
        for i, line in enumerate(csvData):
            data.append(Vector(map(float, line[1:]), i, line[0]))
    return data


def pretreatData(data):
    return data

def calcRSS(data, clusterCenter):
    RSS = [0 for i in range(clusterSum)]
    for vector in data:
        RSS[vector.cluster] += clusterCenter[vector.cluster].euclideanDistance(vector) ** 2
    totalRSS = 0
    for rss in RSS:
        totalRSS += rss
    return rss

def calcFMeasure(data):
    categoryToIndex = {}
    for vector in data:
        categoryToIndex[vector.category] = 0
    for (i, category) in enumerate(categoryToIndex):
        categoryToIndex[category] = i

    categoryCount = [0 for i in range(clusterSum)]
    clusterCount = [0 for i in range(clusterSum)]
    for vector in data:
        categoryCount[categoryToIndex[vector.category]] += 1
        clusterCount[vector.cluster] += 1
    #category -> cluster bipartite graph
    precision = [[0] * clusterSum for i in range(clusterSum)]
    f = [[0] * clusterSum for i in range(clusterSum)]
    for vector in data:
        precision[categoryToIndex[vector.category]][vector.cluster] += 1
    recall = copy.deepcopy(precision)
    for i in range(len(precision)):
        for j in range(len(recall)):
            precision[i][j] /= float(clusterCount[j])
            recall[i][j] /= float(categoryCount[i])
            if precision[i][j] + recall[i][j] != 0:
                f[i][j] = 2 * precision[i][j] * recall[i][j] / (precision[i][j] + recall[i][j])
            else:
                f[i][j] = 0
    possible = list(itertools.permutations(range(clusterSum)))
    maxF = 0
    for categoryToCluster in possible:
        F = 0
        for i in range(clusterSum):
            F += f[i][categoryToCluster[i]] * categoryCount[i]
        F /= float(len(data))
        if maxF < F:
            maxF = F
    return maxF

def clusterData(data):
    #random initial seeds
    clusterCenter = [0 for i in range(clusterSum)]
    seeds = []
    for i in range(clusterSum):
        seed = random.randint(0, len(data) - 1)
        while seed in seeds:
            seed = random.randint(0, len(data) - 1)
        data[seed].cluster = i
        seeds.append(seed)
        clusterCenter[i] = copy.deepcopy(data[seed])
    #k-means cluster
    rssThreshold = 1e-10
    count = 0
    while True:
        count += 1
        print 'round', count, ':'
        preRSS = calcRSS(data, clusterCenter)
        #assign cluster
        for i in range(len(data)):
            minDistance = 1e10
            for center in clusterCenter:
                distance = center.euclideanDistance(data[i])
                if minDistance > distance:
                    minDistance = distance
                    closestCenter = center
            data[i].cluster = copy.deepcopy(closestCenter.cluster)
        nowRSS = calcRSS(data, clusterCenter)
        print preRSS, nowRSS, abs(preRSS - nowRSS)
        if abs(preRSS - nowRSS) < rssThreshold:
            break
        #find new center
        newCenter = [Vector([0 for i in range(len(data[0].v))]) for i in range(clusterSum)]
        clusterCount = [0 for i in range(clusterSum)]
        for vector in data:
            clusterCount[vector.cluster] += 1
            for i, feature in enumerate(vector.v):
                newCenter[vector.cluster].v[i] += feature
        for i in range(len(newCenter)):
            assert clusterCount[i] != 0
            for j in range(len(newCenter[i].v)):
                newCenter[i].v[j] /= clusterCount[i]
        for i in range(len(clusterCenter)):
            newCenter[i].cluster = i
            clusterCenter[i] = copy.deepcopy(newCenter[i])
    F = calcFMeasure(data)
    print '\nF Measure =', F
    return data

def aftertreatResult(result):
    return result

def outputResult(result):
    resultFile = open('cluster result.txt', 'w+')
    cluster = [[] for i in range(clusterSum + 1)]
    for vector in result:
        if vector.cluster != -1:
            cluster[vector.cluster].append(vector)
        else:
            cluster[clusterSum].append(doc)
    for i, c in enumerate(cluster):
        resultFile.write(str(i) + ':\n')
        for vector in c:
            resultFile.write(str(vector.num).zfill(3) + ' - ' + vector.category + '\n')
    resultFile.close()

#main
data = inputData()
data = pretreatData(data)
result = clusterData(data)
'''
maxF = 0
for i in range(1000):
    tempdata = copy.deepcopy(data)
    temp = clusterData(tempdata)
    F = temp[1]
    if maxF < F:
        maxF = F
        result = temp[0]
    print i, F

print maxF
'''
result = aftertreatResult(result)
outputResult(result)

