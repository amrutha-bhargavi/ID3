import sys
import math
import numpy as np
from scipy.stats import entropy
from math import log, e
import pandas as pd

import timeit
from collections import Counter

if(len(sys.argv) != 4) :
    print(sys.argv[0], ": takes 3 arguments, not ", len(sys.argv)-1, ".")
    print("Expecting arguments: dataset.txt partition-input.txt partition-output.txt.")
    sys.exit()

datasetfile = str(sys.argv[1])
partition_input = str(sys.argv[2])
partition_output = str(sys.argv[3])

print('dataset:', datasetfile)
print('partition_input:',partition_input)
print('partition_output:', partition_output)

with open(datasetfile) as inputfile:
    rows = [line.split() for line in inputfile]

with open(partition_input) as inputfile:
    rowsPartition1 = [line.split() for line in inputfile]

def entropy1(labels, base=2):
  value,counts = np.unique(labels, return_counts=True)
  return entropy(counts, base=base)

target = []
entropyTotal = []
maxGains = []
examples = int(rows[0][0])
features = int(rows[0][1])-1
minConditionalEntropy = []
divisionFactor = []
for x in rows[1:]:
   target.append(x[int(rows[0][1])-1])
for eachFeature in rowsPartition1:
    entropySets = []
    for eachSetElement in eachFeature[1:]:
        entropySets.append(target[int(eachSetElement)-1])
    divisionFactor.append((len(eachFeature)-1)/examples)
    #print(divisionFactor)
    entropyTotal.append(entropy1(entropySets))

# for eachFeature in rowsPartition1:
#     for eachSetElement in eachFeature[1:]:
#         conditionalFeatures = []
#         conditionalTargets = []
#         conditionalFeatures.append(rows[][])

class Tree(object):
     def entropy(Y):
        e = 0.
        total = len(Y)
        if total <= 1:
            return 0
        for num in Counter(Y).values():
            p = num/total
            e -= p * math.log2(p)
        return e

     def conditional_entropy(Y, X):
         def indices(v, X):
             return [i for i, j in enumerate(X) if j == v]

         ce = 0.
         total = len(Y)
         for label in Counter(X).keys():
             sv = [Y[i] for i in indices(label, X)]
             e = Tree.entropy(sv)
             ce += e * len(sv) / total
         # print("Conditional Entropy",format(ce))
         return ce
# y = np.array(labels)
# x = np.array(label1)
# ce = Tree.conditional_entropy(y,x)
maxGain = []
maximumGain = 0
feature = 0
i=0
while i<features:
    maxGain = []
    j = 0
    for eachFeature in rowsPartition1:
        #print(eachFeature)
        conditionalFeatures = []
        conditionalTargets = []
        for eachSetElement in eachFeature[1:]:
            conditionalFeatures.append(rows[int(eachSetElement)][int(i)])
            conditionalTargets.append(rows[int(eachSetElement)][int(rows[0][1])-1])
        maxGain.append((entropyTotal[int(j)]-(Tree.conditional_entropy(np.array(conditionalTargets),np.array(conditionalFeatures))))*divisionFactor[j])
        for gain in maxGain:
            if gain >= maximumGain:
                maximumGain = gain
                index = j+1
                feature = i+1
        j += 1
    i += 1
toSplit = rowsPartition1[index-1]
listName = []

dictonaryNaming = {}
for elements in toSplit[1:]:
    dictonaryNaming[elements] = rows[int(elements)][feature - 1]
    listName.append(rows[int(elements)][feature - 1])

print("Partition ",rowsPartition1[index-1][0],"was replaced using Feature ",feature," with the following partitions:")
mySet = {}
mySetKeys = []
a=1
while a<=len(set(listName)):
    print(rowsPartition1[index-1][0],a)
    mySetKeys.append(rowsPartition1[index-1][0]+str(a))
    a+=1
rowsPartition1.remove(toSplit)
splitDictionary = {}
listToSet = []
for elements in toSplit[1:]:
    splitDictionary[elements]=rows[int(elements)][feature-1]
    listToSet.append(rows[int(elements)][feature-1])
setSplit = set(listToSet)
listSplit = list(setSplit)

finalList = []

t=0
for ele in listSplit:
    stri = ""
    for key, value in splitDictionary.items():
        #print(key, value)
        if value == ele:
            #print("true", key)
            if stri != "":
                stri = stri + key + " "
            else:
                stri = key + " "

    finalList.append(mySetKeys[t] + " "+stri)
    t += 1

with open(partition_output, 'w') as f:
    for item in rowsPartition1:
        str=""
        for ele in item:
            str+=ele+" "
        f.write("%s\n" % str)
    for items in finalList:
        f.write("%s\n" % items)
# labels = [0,0,1,1,0,0,1,1,0,1]
# label1 = [0,0,0,1,1,1,1,0,0,0]
labels = [0,1,1,1]
label1 = [0,1,2,2]
print("Entropy",entropy1(labels))
#y = np.array(labels)
#x = np.array(label1)

print("conditional Entropy",Tree.conditional_entropy(np.array(labels),np.array(label1)))
print("Gain : ",((entropy1(labels)) - (Tree.conditional_entropy(np.array(labels),np.array(label1)))))






