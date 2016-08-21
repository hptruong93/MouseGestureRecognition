
import pickle
import numpy as np
import random
import os
import struct

from config import *

def binary(num):
    """
        Float to IEEE-754 single precision binary string.
    """
    return ''.join(bin(ord(c)).replace('0b', '').rjust(8, '0') for c in struct.pack('!f', num))

def test_manual_classification(model):
    """
        Perform classification manually to see if we can replicate scikit learn logistic regression.
    """
    print model
    print model.intercept_
    print model.classes_

    c = model.coef_
    print c.shape

    for i in xrange(1000000):
        # x = [float(r) / 100 for r in reversed(list(range(70)))]
        x = [random.random() for i in xrange(70)]

        true_value = model.predict(x)[0]

        result = np.dot(c, x) + model.intercept_
        my_value = model.classes_[result.argmax()]

        if true_value != my_value:
            print "Predicted %s and my prediction is %s" % (true_value, my_value)
            break


def dump_model(model, out_dir = 'model_dump'):
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)

    with open(os.path.join(out_dir, 'intercept'), 'w') as f:
        joiner = ''
        for floaat in model.intercept_:
            f.write(joiner)
            joiner = '\n'
            f.write(binary(floaat))

    with open(os.path.join(out_dir, 'coefficient'), 'w') as f:
        row_joiner = ''
        for row in model.coef_:
            f.write(row_joiner)
            row_joiner = '\n'

            joiner = ''
            for floaat in row:
                f.write(joiner)
                joiner = '\n'
                f.write(binary(floaat))

    with open(os.path.join(out_dir, 'labels'), 'w') as f:
        joiner = ''
        for label in model.classes_:
            f.write(joiner)
            joiner = '\n'
            f.write(LABEL_LIST[label])

if __name__ == "__main__":
    model = None
    with open('model.pickle', 'r') as f:
        model = pickle.load(f)

    test_manual_classification(model)
