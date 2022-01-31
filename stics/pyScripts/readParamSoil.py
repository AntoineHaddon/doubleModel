import numpy as np
import matplotlib.pyplot as plt
import sys
syspath.append('../../utils')
import readValsFromFile as rdvl


dirStics = '../corn/'

soilParam = rdvl.readLine(dirStics+'param.sol', 0)

print(soilParam)

layerParam = rdvl.readVals(dirStics + 'param.sol',firstLine=3)


#colums indices
jthickness=1         # of layer
jsfc=2               # soil water content at field capacity (in %)
jsh=3                # soil water content t wilting point (%)
jbulkDensity=4       # g/cm3


totalDepth=np.sum(layerParam[:,jthickness])
print(totalDepth)

print(layerParam[:,jbulkDensity])
