import random
import copy
import csv
import ipdb
import math

testDataPercentage = 0.27182818

class Vector:
    v = []
    num = 0
    category = ''
    def __init__ (self, v, num = 0, category = -1):
        self.v = v
        self.num = num
        self.category = category

class Distribution:
    sigma = 0.0
    mu = 0.0
    def __init__ (self, sigma = 0.0, mu = 0.0):
        self.sigma = sigma
        self.mu = mu
    def calc(self, x):
        return (1 / (math.sqrt(2 * math.pi) * self.sigma)) * math.exp(-((x - self.mu) ** 2) / (2 * (self.sigma ** 2)))

'''
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

def trainModule(data):
    #calc prior
    prior = {}
    categoryCount = {}
    for vector in data:
        if not vector.category in prior:
            prior[vector.category] = 0
        prior[vector.category] += 1
    categoryCount = copy.deepcopy(prior)
    for p in prior:
        prior[p] /= float(len(data))
    #calc likelihood
    likelihood = {}
    #calc mean
    for vector in data:
        if not vector.category in likelihood:
            likelihood[vector.category] = [Distribution(0.0, 0.0) for i in range(featureSum)]
        for (i, feature) in enumerate(vector.v):
            likelihood[vector.category][i].mu += feature
    for category in likelihood:
        for i in range(featureSum):
            likelihood[category][i].mu /= float(categoryCount[category])
    #calc standard divation
    for vector in data:
        for (i, feature) in enumerate(vector.v):
            likelihood[vector.category][i].sigma += (feature - likelihood[vector.category][i].mu) ** 2
    for category in likelihood:
        for i in range(featureSum):
            likelihood[category][i].sigma /= float(categoryCount[category])
            likelihood[category][i].sigma = math.sqrt(likelihood[category][i].sigma)
    return (prior, likelihood)

def classifyData(module, data):
    (prior, likelihood) = module
    correctClassify = 0
    errorClassify = 0
    for vector in data:
        posterior = {}
        for category in prior:
            posterior[category] = math.log(prior[category])
            for (i, feature) in enumerate(vector.v):
                if likelihood[category][i].calc(feature) == 0:
                    posterior[category] = 0
                    break
                posterior[category] += math.log(likelihood[category][i].calc(feature))
        maxPosterior = - 1 << 20
        resultCategory = ''
        for category in posterior:
            if maxPosterior < posterior[category]:
                maxPosterior = posterior[category]
                resultCategory = category
        print vector.num, vector.category, '->', resultCategory
        if vector.category == resultCategory:
            correctClassify += 1
        else:
            errorClassify += 1
    return correctClassify / float(correctClassify + errorClassify)

(trainingData, testingData) = inputData()
module = trainModule(trainingData)
result = classifyData(module, testingData)
print result
