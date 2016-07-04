
import os
import sys
import subprocess
import argparse
import numpy as np
from config import *


def get_data(file_name):
    data = np.genfromtxt(file_name, delimiter=', ', dtype=int)
    the_len = len(data)
    if the_len == 0:
        return None

    if the_len < MIN_LENGTH:
        return None

    return data

def write_out(data, dst_path):
    write_out.count += 1
    file_name = str(write_out.count) + '.txt'
    file_name = os.path.join(dst_path, file_name)
    # np.savetxt(file_name, data.astype(int),  delimiter=", ", fmt='%i')
    np.savetxt(file_name, data,  delimiter=", ", fmt='%i')

def group_random_file(file_name, dst_path = os.path.join(out_dir, 'random')):
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)

    data = get_data(file_name)

    #Group in group of MIN_LENGTH
    total = 0
    index = 0
    output = np.array([[]])

    while index < len(data):
        rows = []
        current_count = 0

        while current_count < MIN_LENGTH and index < len(data):
            rows.append(data[index])
            current_count += 1
            index += 1

        if len(rows) < MIN_LENGTH:
            break

        new_data = np.vstack(rows)

        # total += 1
        # write_out(new_data, dst_path)
        total += augment_data(new_data, dst_path)

    print "Random data augmented to be {0}".format(total)

def augment_data_from_file(file_name, dst_path):
    data = get_data(file_name)
    return augment_data(data, dst_path)

def augment_data(data, dst_path):
    if data is None:
        return 0

    count = 0
    changed_index = -2
    while changed_index < min(len(data) - 1, MIN_LENGTH - 1):
        changed_index += 1
        if changed_index < 0:
            write_out(data, dst_path)
            continue

        for i in xrange(1, 2):
            data[changed_index] = np.array([data[changed_index][0] + i, data[changed_index][1]])
            write_out(data, dst_path)
            data[changed_index] = np.array([data[changed_index][0] - i, data[changed_index][1]])

            data[changed_index] = np.array([data[changed_index][0], data[changed_index][1] + i])
            write_out(data, dst_path)
            data[changed_index] = np.array([data[changed_index][0], data[changed_index][1] - i])

            data[changed_index] = np.array([data[changed_index][0] - i, data[changed_index][1] + i])
            write_out(data, dst_path)
            data[changed_index] = np.array([data[changed_index][0] + i, data[changed_index][1] - i])

            data[changed_index] = np.array([data[changed_index][0] + i, data[changed_index][1] - i])
            write_out(data, dst_path)
            data[changed_index] = np.array([data[changed_index][0] - i, data[changed_index][1] + i])

        count += 4

    return count


def generate_data(src_path, dst_path):
    count = 0
    for file_name in os.listdir(src_path):
        count += augment_data_from_file(os.path.join(src_path, file_name), dst_path)

    print "Counting {0} files...".format(count)


def traverse_labels(args):
    for label in os.listdir(test_dir):
        if args.label is not None and args.label != label:
            continue

        if label in BLACK_LIST:
            print "Black listed {0}. Ignoring...".format(label)
            continue

        src_path = os.path.join(test_dir, label)
        if not os.path.isdir(src_path):
            continue

        dst_path = os.path.join(out_dir, label)
        if not os.path.exists(dst_path):
            os.makedirs(dst_path)

        print "Generating {0}...".format(src_path)
        generate_data(src_path, dst_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'Generate training samples')
    parser.add_argument('-l', '--label', dest = 'label', default = None, help = 'Label to generate data', type=str)

    args = parser.parse_args()

    cleaning_dir = os.path.join(out_dir, args.label) if args.label is not None else out_dir
    cmd = 'rm -rf %s/*' % cleaning_dir
    print "$" + cmd
    subprocess.check_call(cmd, shell = True)

    print "Done cleaning"

    write_out.count = 0

    traverse_labels(args)

    if args.label is None or args.label == 'random':
        group_random_file(os.path.join(test_dir, 'random.txt'))
