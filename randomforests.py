import random
from csv import reader
from math import sqrt

def csv_loader(filename):
    data = list()
    with open(filename, 'r') as file:
        readers = reader(file)
        for row in readers:
            if not row:
                continue
            data.append(row)
    return data

def colfloat(data, column):
    for row in data:
        row[column] = float(row[column].strip())

def colint(data, column):
    classvals = [row[column] for row in data]
    own = set(classvals)
    search = dict()
    for i, value in enumerate(own):
        search[value] = i
    for row in data:
        row[column] = search[row[column]]
    return search

def eval(data, algorithm, n_folds, *args):
    folds = validationsplit(data, n_folds)
    scores = list()
    for fold in folds:
        trainer = list(folds)
        trainer.remove(fold)
        trainer = sum(trainer, [])
        tester = list()
        for row in fold:
            rcopy = list(row)
            tester.append(rcopy)
            rcopy[-1] = None
        predicted = algorithm(trainer, tester, *args)
        actual = [row[-1] for row in fold]
        accuracy = accuracy(actual, predicted)
        scores.append(accuracy)
    return scores

def getsplit(data, n_features):
    cvalues = list(set(row[-1] for row in data))
    bin, bval, bsco, bgro = 999, 999, 999, None
    features = list()
    while len(features) < n_features:
        index = random.randrange(len(data[0]) - 1)
        if index not in features:
            features.append(index)
    for index in features:
        for row in dataset:
            groups = testsplit(index, row[index], data)
            gini = gini_index(groups, cvalues)
            if gini < bsco:
                bin, bval, bsco, bgro = index, row[index], gini, groups
    return {'index': bin, 'value': bval, 'group': bgro}

def split(node, max_depth, min_size, n_features, depth):
    left, right = node['groups']
    del(node['groups'])
    if not left or not right:
        node['left'] = node['right'] = terminal(left + right)
        return
    if depth >= max_depth:
        node['left'], node['right'] = terminal(left), terminal(right)
        return
    if len(left) <= min_size:
        node['left'] = terminal(left)
    else:
        node['left'] = getsplit(left, n_features)
        split(node['left'], max_depth, min_size, n_features, depth + 1)
    if len(right) <= min_size:
        node['right'] = terminal(right)
    else:
        node['right'] = getsplit(right, n_features)
        split(node['right'], max_depth, min_size, n_features, depth+1)

def testsplit(index, value, data):
    left = list()
    right = list()
    for row in data:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right

def validationsplit(data, n_folds):
    split = list()
    datacopy = list(data)
    fsize = len(data) / n_folds
    for i in range(n_folds):
        fold = list()
        while len(fold) < fsize:
            index = random.randrange(len(datacopy))
            fold.append(datacopy.pop(index))
        split.append(fold)
    return split

def accuracy(actual, pred):
    correct = 0
    for i in range(len(actual)):
        if actual[i] == pred[i]:
            correct += 1
    return correct / float(len(actual)) * 100.0

def gini_index(groups, cvalue):
    gini = 0.0
    for c in cvalue:
        for group in groups:
            size = len(group)
            if size == 0:
                continue
            proportion = [row[-1] for row in group].count(c) / float(size)
            gini += (proportion * (1.0 - proportion))
    return gini

def terminal(group):
    out = [row[-1] for row in group]
    return max(set(out), key = out.count)

def builder(train, depth, min_size, n_features):
    root = getsplit(dataset, n_features)
    split(root, depth, min_size, n_features, 1)
    return root

def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']

def sample(data, ratio):
    sample = list()
    nsample = round(len(data) * ratio)
    while len(sample) < nsample:
        index = random.randrange(len(data))
        sample.append(data[index])
    return sample

def bagging(trees, rows):
    predictions = [predict(tree, rows) for tree in trees]
    return max(set(predictions), key = predictions.count)

def random_forest(train, test, max_depth, min_size, sample_size, n_trees, n_features):
    trees = list()
    for i in range(n_trees):
        sample = sample(train, sample_size)
        tree = builder(sample, max_depth, min_size, n_features)
        trees.append(tree)
    predictions = [bagging(trees, row) for row in test]
    return predictions

if __name__ == '__main__':
    random.seed(1)
    filename = 'csv' ################
    dataset = csv_loader(filename)
    for i in range(0, len(dataset[0]) - 1):
        colfloat(dataset, i)
    colint(dataset, len(dataset[0]) - 1)
    n_folds = 5
    max_depth = 10
    min_size = 1
    sample_size = 1.0
    n_features = int(sqrt(len(dataset[0]) - 1))
    for n_trees in [1, 5, 10]:
        scores = eval(dataset, random_forest, n_folds, max_depth, min_size, sample_size, n_trees, n_features)
        print('Trees: {}'.format(n_trees))
        print('Scores: {}'.format(scores))
        print('Mean Accuracy: {}'.format(sum(scores)/ float(len(scores))))