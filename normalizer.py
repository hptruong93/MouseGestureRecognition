
import numpy as np

from config import *

def _trim_cut(data):
    return data[0:MIN_LENGTH, :] #Only take first MIN_LENGTH rows

def _trim_cut_reversed(data):
    return data[-MIN_LENGTH:, :] #Only take last MIN_LENGTH rows

def _trim_definition(data): #Cut down by leaving out an element every once in a while
    data_length = len(data)
    if data_length == MIN_LENGTH:
        return data

    leave_out_period = float(data_length) / (data_length - MIN_LENGTH)

    result = []
    previous = -1
    for index in xrange(data.shape[0]):
        if index == 0:
            previous = 0
            result.append(data[0, :])
            continue

        new = int((index + 1) / leave_out_period)
        if new == previous:
            result.append(data[index, :])

        previous = new

    output = np.array(result)
    output = _trim_cut(output)
    return output

trim_data = _trim_definition



def normalize(data):
    data = trim_data(data)

    min_x, min_y = np.amin(data, 0)
    max_x, max_y = np.amax(data, 0)

    # print "Minimums {0} and maximum {1}".format((min_x, min_y, ), (max_x, max_y, ))

    width = max_x - min_x
    if width == 0:
        width = 1

    height = max_y - min_y
    if height == 0:
        height = 1

    #Fit this into a square box. Center the appropriate dimension
    if height > width:
        mid_x = (max_x + min_x) / float(2)
        sub_x = mid_x - height / float(2)
        sub_y = min_y
    elif width > height:
        sub_x = min_x
        mid_y = (max_y + min_y) / float(2)
        sub_y = mid_y - width / float(2)
    else:
        sub_x = min_x
        sub_y = min_y

    subtract_matrix = np.array([-sub_x, -sub_y])
    # print "Subtracting %s" % subtract_matrix
    data = data + subtract_matrix

    #Now make it into a square box of size 1
    size = max(width, height)
    data = data / float(size)
    return data.flatten()
