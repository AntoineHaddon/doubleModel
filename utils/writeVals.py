


def writeValstoFile(filename,vals,forma=''):

    f = open(filename, "w")

    lines,cols = vals.shape

    for l in range(lines):
        for c in range(cols):
            f.write( format(vals[l,c], forma) + ", " )
        f.write("\n")





if __name__ == "__main__":

    import numpy as np

    mat = np.array ( [ [1.3, 1], [2, 3] ] )

    print(mat)

    writeValstoFile("test.dat", mat)
