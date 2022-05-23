import csv
from math import sqrt
import random
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.cluster.hierarchy import dendrogram, linkage #imported for testing

def load_data(filepath):
    data = []
    counter = 0
    with open(filepath) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (counter < 20):
                data.append({'#': int(row['#']), 'Name' : row['Name'], 'Type 1': row['Type 1'], 'Type 2': row['Type 2'], 'Total': int(row['Total']), 'HP': int(row['HP']), 'Attack': int(row['Attack']), 'Defense': int(row['Defense']), 'Sp. Atk': int(row['Sp. Atk']), 'Sp. Def': int(row['Sp. Def']), 'Speed': int(row['Speed'])})
                counter = counter + 1
    return data

def calculate_x_y(stats):
    x = stats.get("Attack") + stats.get("Sp. Atk")+ stats.get("Speed")
    y = stats.get("Defense") + stats.get("Sp. Def") + stats.get("HP")
    thistuple = (x, y)
    return thistuple

def dist(x1, x2, y1, y2): #used to check value in math.dist
    dist1 = x2 - x1
    dist2 = y2 - y1
    dist1 = dist1 * dist1
    dist2 = dist2 * dist2
    distTotal = dist1 + dist2
    distActual = sqrt(distTotal)
    return distActual


def random_x_y(m):
    x = 0
    y = 0
    tuplelist = []
    i = 0
    if (m > 0):
        while(i < m):
            x = random.randint(0, 360) #creates random value between 0 and 360 for both x and y in tuple
            y = random.randint(0, 360)
            thistuple = (x, y)
            tuplelist.append(thistuple)
            i = i + 1
    return tuplelist

def hac(dataset):
    dataset = [i for i in dataset if not math.isnan(i[0]) and math.isfinite(i[0]) 
        and not math.isnan(i[1]) and math.isfinite(i[1])] #eliminating nan and inf values
    m = len(dataset)
    point_set = {}
    for i in range(m):
        point_set[str(i)] = None #creating a list of points equating to numbers
    Z = [[None for x in range(4)] for y in range(m-1)]
    used = [[None for x in range(3)] for y in range(m-1)]

    for row in range(m - 1):
        pts = [math.inf, math.inf, math.inf]
        for i in range(m):
            for j in range(m):
                  if ((point_set[str(i)] != point_set[str(j)]) or (point_set[str(i)] == None and point_set[str(j)] == None)):
                    duplicate = False
                    d = math.dist(dataset[i], dataset[j])
                    for k in range(row):
                        if ((i == used[k][1] and j == used[k][2]) or 
                            (i == used[k][2] and j == used[k][1])):
                            duplicate = True #duplicate check         
                    if (i != j and d < pts[0] and not duplicate): #if i and j dont equal and d is less than min
                        pts[0] = d 
                        pts[1] = i
                        pts[2] = j
                    elif (i != j and d == pts[0] and not duplicate): #tie breaker
                        if ((i < pts[1] and i < pts[2]) or ((j < pts[1] and j < pts[2]))):
                            pts[0] = d
                            pts[1] = i
                            pts[2] = j
                        elif ((i < pts[2] and i == pts[1] and j < pts[2])or
                            (i < pts[1] and i == pts[2] and j < pts[1]) or
                            (j < pts[1] and j == pts[2] and i < pts[1]) or
                            (i < pts[2] and j == pts[1] and j < pts[2])):
                            pts[0] = d
                            pts[1] = i
                            pts[2] = j     
        used[row][0] = pts[0]
        used[row][1] = pts[2]
        used[row][2] = pts[1]
        c1 = point_set[str(pts[1])]
        c2 = point_set[str(pts[2])]
        p1 = 0
        p2 = 0
        total = 2
        if (c1 == None):
            p1 = pts[1]
            point_set[str(pts[1])] = row
        else:
            p1 = c1 + m
            total = total + Z[c1][3] - 1
            for num in point_set:
                if (point_set[num] == c1):
                    point_set[num] = row
        if (c2 == None):    
            p2 = pts[2]
            point_set[str(pts[2])] = row
        else:
            p2 = c2 + m
            total = total + Z[c2][3] - 1
            for num in point_set:
                if (point_set[num] == c2):
                    point_set[num] = row
        if (p1 < p2):
            Z[row][0] = p1
            Z[row][1] = p2
        else:
            Z[row][1] = p1
            Z[row][0] = p2
        Z[row][2] = pts[0]
        Z[row][3] = total

    return np.array(Z)

def imshow_hac(dataset):
    Z = hac(dataset)
    m = len(Z) + 1
    fig, ax= plt.subplots(1, 1, figsize=(9,4))
    scatter = np.transpose(dataset)
    edge_set = Z
    ax.scatter(scatter[0], scatter[1])

    for row in range(m - 1):
        indices = [set(), set()]
        x1 = int(Z[row, 0])
        x2 = int(Z[row, 1])
        while (x1 >= m): #recurse the the point until it is less than m, means pt was apart of a cluster
            x1 = x1-m
        while (x2 >= m):
            x2 = x2 - m
        if (x1 < m):
            indices[0].add(x1) 
        if (x2 < m):
            indices[1].add(x2) 
        found = False
        for i in indices[0]: 
            for j in indices[1]: 
                xi = int(i)
                xj = int(j)
                arr1 = np.array([math.dist(dataset[xi], dataset[xj])])
                arr2 = np.array([Z[row, 2]])
                if (arr1 == arr2): #iterating through the arrays to find the equal distance between the points in order of dataset and hac
                    found = True
                    points = np.transpose(np.array([dataset[xi], dataset[xj]]))
                    ax.plot(points[0], points[1])
                    plt.pause(0.3)
                    break 
            if (found):
                break
    plt.show()
    return None

