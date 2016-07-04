import sys
import os
import time
import pickle
import random
import argparse
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split

import normalizer
from config import *

random.seed(69)

X = [] # Training set
y = [] # Label set

def time_it(message, action):
    now = time.time()
    value = action()
    print "{0} took {1} seconds".format(message, time.time() - now)
    return value

###################################################################################################

def process_data_row(label, file_name):
    data = np.genfromtxt(file_name, delimiter=', ', dtype = int)
    data = normalizer.normalize(data)

    X.append(data)
    y.append(LABELS[label])


def traverse_labels(args, label_path):
    for label_name in os.listdir(label_path):
        print "Loading samples for label {0}...".format(label_name)
        inspecting_dir = os.path.join(label_path, label_name)
        if not os.path.isdir(inspecting_dir):
            continue

        if len(WHITE_LIST) != 0 and (label_name not in WHITE_LIST and label_name != 'random'):
            print "Not whitelisted {0}.Ignoring...".format(label_name)
            continue

        if label_name in BLACK_LIST:
            print "Black listed {0}. Ignoring...".format(label_name)
            continue

        count = 0
        for file_name in os.listdir(inspecting_dir):
            count += 1
            full_file_name = os.path.join(inspecting_dir, file_name)
            should_keep = random.random() < args.percent

            process_data_row(label_name, full_file_name)
            print "\rCounted %s" % count,
            sys.stdout.flush()

        print ""
    print "Total number of samples is {0}".format(len(X))

###################################################################################################

def get_model(args):
    if args.load and os.path.isfile(model_file):
        with open(model_file, 'r') as f:
            model = pickle.load(f)
        return model

    model = LogisticRegression(C = 0.9)
    return model

def save_model(model, args):
    if not args.save:
        return

    with open(model_file, 'w') as f:
        pickle.dump(model, f)

def train_and_evaluate(args):
    model = get_model(args)

    if not args.load:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 69)
        model.fit(X_train, y_train)

        print "Accuracy is {0}".format(model.score(X_test, y_test))
        save_model(model, args)
    else:
        print "Loaded model"
        print "Accuracy is {0}".format(model.score(X, y))
        print model.predict(X[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Train and evaluate model')
    parser.add_argument('-s', '--save', dest = 'save', default = False, action = 'store_true', help = 'Save model after run')
    parser.add_argument('-l', '--load', dest = 'load', default = False, action = 'store_true', help = 'Load model before run')
    parser.add_argument('-r', '--retrieve', dest = 'retrieve', default = False, action = 'store_true', help = 'Retrieve sample data from disk')
    parser.add_argument('-p', '--percent', dest = 'percent', default = 1.0, help = 'Percent of samples to operate on. Enter number < 1', type = float)

    args = parser.parse_args()

    stage1 = lambda : traverse_labels(args, out_dir)
    stage2 = lambda : train_and_evaluate(args)

    if args.retrieve:
        time_it('Retrieving data', stage1)

    time_it('Training and evaluation', stage2)
