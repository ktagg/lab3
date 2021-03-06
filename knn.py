import csv
import random
import math
import operator

def loader(filename, split, trainer = [], test = []):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        data = list(lines)
        for x in range(len(data) - 1):
            for y in range(4):
                data[x][y] = float(data[x][y])
            if random.random() < split:
                trainer.append(data[x])
            else:
                test.append(data[x])

def loader2(filename, split, trainer = [], test = []):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        data = list(lines)
        for x in range(len(data) - 1):
            for y in range(7):
                data[x][y] = float(data[x][y])
            if random.random() < split:
                trainer.append(data[x])
            else:
                test.append(data[x])

def loader3(filename, split, trainer = [], test = []):
    with open(filename, 'rt') as csvfile:
        lines = csv.reader(csvfile)
        data = list(lines)
        for x in range(len(data) - 1):
            for y in range(23):
                print(data[x])
                data[x][y] = float(ord(data[x][y]))
            if random.random() < split:
                trainer.append(data[x])
            else:
                test.append(data[x])

def distance(i1, i2, length):
    distancer = 0
    for x in range(length):
        distancer += pow((i1[x] - i2[x]), 2)
    return math.sqrt(distancer)

def neighbors(training, tester, k):
    distances = []
    length = len(tester) - 1
    for x in range(len(training)):
        dist = distance(tester, training[x], length)
        distances.append((training[x], dist))
    distances.sort(key = operator.itemgetter(1))
    neighbor = []
    for x in range(k):
        neighbor.append(distances[x][0])
    return neighbor

def response(neighbor):
    classer = {}
    for x in range(len(neighbor)):
        resp = neighbor[x][-1]
        if resp in classer:
            classer[resp] += 1
        else:
            classer[resp] = 1
    sorter = sorted(classer.items(), key = operator.itemgetter(1), reverse = True)
    return sorter[0][0]

def accuracy(tester, predictions):
    correct = 0
    for x in range(len(tester)):
        if tester[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(tester))) * 100.00

def main():
    trainer = []
    tester = []
    split = 0.7
    loader('iris.data', split, trainer, tester)
    print('--------------Trainer------------')
    for i in trainer:
        print(i)
    print('---------------------------------')
    print('Train set: {}'.format(repr(len(trainer))))
    print('-------------Tester--------------')
    for i in tester:
        print(i)
    print('---------------------------------')
    print('Test set: {}'.format(repr(len(tester))))
    predictions = []
    k = 3
    for x in range(len(tester)):
        neighbor = neighbors(trainer, tester[x], k)
        result = response(neighbor)
        predictions.append(result)
    print('--------------Predictions--------------')
    for i in predictions:
        print(i)
    print('---------------------------------------')
    acc = accuracy(tester, predictions)
    print('Accuracy: {}'.format(acc))
    print('###############################Second Set############################')
    trainer = []
    tester = []
    split = 0.76
    loader2('seeds_dataset.csv', split, trainer, tester)
    print('--------------Trainer------------')
    for i in trainer:
        print(i)
    print('---------------------------------')
    print('Train set: {}'.format(repr(len(trainer))))
    print('-------------Tester--------------')
    for i in tester:
        print(i)
    print('---------------------------------')
    print('Test set: {}'.format(repr(len(tester))))
    predictions = []
    k = 3
    for x in range(len(tester)):
        neighbor = neighbors(trainer, tester[x], k)
        result = response(neighbor)
        predictions.append(result)
    print('--------------Predictions--------------')
    for i in predictions:
        print(i)
    print('---------------------------------------')
    acc = accuracy(tester, predictions)
    print('Accuracy: {}'.format(acc))
    print('############################Third Set######################')
    tester = []
    trainer = []
    split = 0.65
    loader3('agaricus-lepiota.data.csv', split, trainer, tester)
    print('--------------Trainer------------')
    for i in trainer:
        print(i)
    print('---------------------------------')
    print('Train set: {}'.format(repr(len(trainer))))
    print('-------------Tester--------------')
    for i in tester:
        print(i)
    print('---------------------------------')
    print('Test set: {}'.format(repr(len(tester))))
    predictions = []
    k = 3
    for x in range(len(tester)):
        neighbor = neighbors(trainer, tester[x], k)
        result = response(neighbor)
        predictions.append(result)
    print('--------------Predictions--------------')
    for i in predictions:
        print(i)
    print('---------------------------------------')
    acc = accuracy(tester, predictions)
    print('Accuracy: {}'.format(acc))



main()
