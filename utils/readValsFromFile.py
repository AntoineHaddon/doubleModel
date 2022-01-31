import numpy as np
import re

def fileLen(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def readLine(fname,lineNb):
    """
        Reads float values from line of a file
        return numpy vector of floats
    """
    with open(fname) as f:
        for i in range(lineNb):
            f.readline()
        return np.array(
                [ float(s) for s in re.findall(r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", f.readline() ) ]
                    )


def readVals(filename,firstLine=0):
    """
        Reads float values from a file
        return matrix with numerical values like file
    """
    num_lines = fileLen(filename)-firstLine
    f = open(filename, "r")

    for i in range(firstLine):
        f.readline()

    valsPerLine = len([
                    float(s) for s in re.findall
                        (r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", f.readline())
                    ])
    vals = np.zeros((num_lines, valsPerLine))

    f.seek(0)
    for i in range(firstLine):
        f.readline()

    for il, line in enumerate(f):
        vals[il, :] = [
                    float(s) for s in re.findall
                            (r"[+-]? *(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?", line)
                        ]
    return vals
