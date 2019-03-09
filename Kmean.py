import pandas as pd
from random import randint, seed
from math import sqrt
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import numpy as np

def pick_seeds(data,k):

    centroids = []
    observedIndices = set()
    for i in range(k):
        tempIndex = randint(0, len(data))
        while(tempIndex in observedIndices):
                tempIndex = randint(0, len(data))
        centroids.append(data.iloc[tempIndex])
        observedIndices.add(tempIndex)

    return centroids

def recalcCentroids(clusters, data, dataHeaders,k):

    newCentroids = []
    for i in range(k):
        averages = dict(zip(dataHeaders,[0]*len(dataHeaders)))
        for item in clusters[i]:
            for h in dataHeaders:
                averages[h]+=data.loc[item,h]
        for h in dataHeaders:
            averages[h]=float(averages[h])/(len(clusters[i]))
            #if empty cluster, this could create div by 0 error
        newCentroids.append(averages)

    return newCentroids

def pickClosest(dp, centroids, dataHeaders):

    minDist = None
    index = 0
    count = 0
    for c in centroids:
        tempDist = 0
        for h in dataHeaders:
            tempDist+=(c[h]-dp[h])**2
        tempDist = sqrt(tempDist)
        if minDist == None or tempDist<minDist:
            index = count
            minDist = tempDist
        count+=1

    return index

def cluster(data, centroids, dataHeaders, k):

    done = False
    old=[[] for i in range(k)]
    count = 0
    while not done:
        done=True
        count+=1
        for j in range(k):
            clusters = [[] for i in range(k)]
            for i in range(len(data)):
                clusters[pickClosest(data.iloc[i],
                            centroids, dataHeaders)].append(i)
            if (set(old[j])!=set(clusters[j])):
                done = False
        old = clusters
        centroids=recalcCentroids(clusters, data, dataHeaders, k)

    generatePlot(old, data)

def generatePlot(clusters, data):
    colors = iter(cm.rainbow(np.linspace(0, 1, k)))
    for group in clusters:
        x = [data.loc[i][0] for i in group]
        y = [data.loc[i][1] for i in group]
        plt.scatter(x, y, color=next(colors))
    plt.show()

if __name__=="__main__":
    seed()
    print('hello')
    df = pd.read_csv("dummyData2.csv")
    names = list(df.columns)
    k = 4
    centroids = pick_seeds(df, k)
    cluster(df, centroids, names, k)
