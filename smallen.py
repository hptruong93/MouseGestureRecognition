
import os
import random
import argparse
from config import *

random.seed(69)

def minimize_test_samples(args):
    for label_name in os.listdir(out_dir):
        if args.label != 'all' and label_name != args.label:
            print "Nope %s" % label_name
            continue

        current_path = os.path.join(out_dir, label_name)

        for file_name in os.listdir(current_path):
            file_path = os.path.join(current_path, file_name)

            should_keep = random.random() < (args.percent if label_name != 'random' else 1 * args.percent)
            if not should_keep:
                os.remove(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Make the test data smaller for experiemental purpose')
    parser.add_argument('-s', '--percent', dest = 'percent', default = 0.4, help = 'Percent of samples to keep. Enter number < 1', type = float)
    parser.add_argument('-l', '--label', dest = 'label', default = 'all', help = 'Label to minimize', type = str)

    args = parser.parse_args()
    minimize_test_samples(args)