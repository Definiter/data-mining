import math
import random
import copy
import csv
import ipdb

testDataPercentage = 0.2

def normalize(l):
    sumL = sum(l)
    return [float(x) / sumL for x in l]

def entropy(l):
    l = normalize(l)
    return -sum([x * math.log(x, 2) for x in l if x != 0])

def gini(l):
    l = normalize(l)
    return 1 - sum([x * x for x in l])

def clfError(l):
    l = normalize(l)
    return 1 - max(l)

class Vector:
    v = []
    num = 0
    category = ''
    def __init__ (self, v, num = 0, category = -1):
        self.v = v
        self.num = num
        self.category = category


class TreeNode:
    children = []
    father = -1
    label = ''
    testCondition = (0, 0)
    num = 0

#iris
def inputData():
    data = []
    with open('iris.data') as inputFile:
        csvData = csv.reader(inputFile)
        for i, line in enumerate(csvData):
            data.append(Vector(map(float, line[0:4]), i, line[4]))
    trainingData = []
    testingData = []
    for vector in data:
        if random.randint(0, 1000) / 1000.0 <= testDataPercentage:
            testingData.append(vector)
        else:
            trainingData.append(vector)
    return (trainingData, testingData)
featureSum = 4
'''
#wine
def inputData():
    data = []
    with open('wine.data') as inputFile:
        csvData = csv.reader(inputFile)
        for i, line in enumerate(csvData):
            data.append(Vector(map(float, line[1:]), i, line[0]))
    trainingData = []
    testingData = []
    for vector in data:
        if random.randint(0, 1000) / 1000.0 <= testDataPercentage:
            testingData.append(vector)
        else:
            trainingData.append(vector)
    return (trainingData, testingData)
featureSum = 13
'''

def canStop(data, father):
    assert(len(data))

    #test branch's used feature
    count = [0 for i in range(featureSum)]
    now = father
    while now != -1:
        count[now.testCondition[0]] = 1
        now = now.father
    if sum(count) == featureSum:
        return True

    same = True
    for i in range(featureSum):
        if count[i] == 0:
            for vector in data:
                if vector.v[i] != data[0].v[i]:
                    same = False
                    break
    if same:
        return True

    #test if all date belong to same category
    cat = data[0].category
    for vector in data:
        if cat != vector.category:
            return False

    return True

def classify(data):
    count = {}
    for vector in data:
        if not vector.category in count:
            count[vector.category] = 0
        count[vector.category] += 1
    maxCount = 0
    maxCategory = ''
    for cat in count:
        if maxCount < count[cat]:
            maxCount = count[cat]
            maxCategory = cat
    return cat

def findBestSplit(data, node):
    bestFeature = 0
    bestSplitPoint = 0
    minI = 1 << 20
    
    usedFeature = [0 for i in range(featureSum)]
    now = node.father
    while now != -1:
        #print now.num, now.testCondition[0]
        usedFeature[now.testCondition[0]] = 1
        now = now.father
    #print usedFeature
    
    for feature in range(len(data[0].v)):
        if usedFeature[feature] == 1:
            continue
        tempData = copy.deepcopy(data)
        tempData.sort(key = lambda x: x.v[feature])

        l = {}
        r = {}
        for vector in tempData:
            if not vector.category in r:
                r[vector.category] = 0
            l[vector.category] = 0
            r[vector.category] += 1

        #for vector in tempData:
        #    print vector.num, vector.category, vector.v
        
        for (i, vector) in enumerate(tempData):
            if i == len(tempData) - 1:
                break
            l[vector.category] += 1
            r[vector.category] -= 1
            if tempData[i].v[feature] == tempData[i + 1].v[feature]:
                continue
            ls = [l[x] for x in l]
            rs = [r[x] for x in r]
            I = entropy(ls) * sum(ls) / len(tempData) + \
                entropy(rs) * sum(rs) / len(tempData)

            if minI >= I:
                minI = I
                bestFeature = feature
                bestSplitPoint = (tempData[i].v[feature] + tempData[i + 1].v[feature]) / 2.0
    return (bestFeature, bestSplitPoint)

def treeGrowth(data, num, father):
    #print num
    #for vector in data:
    #    print vector.num, vector.category, vector. v
    if canStop(data, father):
        leaf = TreeNode()
        leaf.num = num
        leaf.label = classify(data)
        leaf.father = father
        return leaf
    else:
        root = TreeNode()
        root.father = father
        root.testCondition = findBestSplit(data, root)
        #print root.testCondition
        root.num = num
        childData = [[], []]
        for vector in data:
            if vector.v[root.testCondition[0]] < root.testCondition[1]:
                childData[0].append(vector)
            else:
                childData[1].append(vector)
        root.children = [0, 0]
        for i in range(2):
            if len(childData[i]) != 0:
                root.children[i] = treeGrowth(childData[i], num * 2 + i + 1, root)
            else:
                root.children[i] = TreeNode()
                root.children[i].label = classify(data)
                root.children[i].father = root
        return root


def trainModule(trainingData):
    return treeGrowth(trainingData, 0, -1)

def printModule(now, depth):
    if depth > 0:
        print '|' * depth,
    if now.label != '':
        print now.num, now.label
        return
    print now.num, 'feature', now.testCondition[0], '<', now.testCondition[1]
    printModule(now.children[0], depth + 1)
    if depth > 0:
        print '|' * depth,
    print now.num, 'feature', now.testCondition[0], '>', now.testCondition[1]
    printModule(now.children[1], depth + 1)
    

def classifyData(module, testingData):
    correctClassify = 0
    errorClassify = 0
    for vector in testingData:
        now = module
        while now.label == '':
            if vector.v[now.testCondition[0]] < now.testCondition[1]:
                now = now.children[0]
            else:
                now = now.children[1]
        #print vector.num, vector.category, '->', now.label
        if vector.category == now.label:
            correctClassify += 1
        else:
            errorClassify += 1
    return correctClassify / float(correctClassify + errorClassify)
    



#main
avgResult = 0.0
for i in range(100):
    (trainingData, testingData) = inputData()
    module = trainModule(trainingData)
    #printModule(module, 0)
    result = classifyData(module, testingData)
    avgResult += result
avgResult /= 100
print avgResult

