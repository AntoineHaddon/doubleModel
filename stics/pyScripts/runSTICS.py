import numpy as np
import subprocess as sproc
from os import getcwd

import sticsIOutils as sticsIO



# directory with files to run STICS simulation (parameter files, initial condition, weather , etc... )
dirStics = getcwd() + '/../corn/'

# directory with STICS program files 
# needs to be changed to the local path 
JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'



def runUSM(wdir,usm):
    return sproc.run(["java", "-jar", "JavaSticsCmd.exe", "--run", wdir, usm], cwd=JavaSticsDir)





if __name__ == "__main__":


    # set irragation calendar
    cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"
    irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
    # irrigCal_corn2013 = np.array([ range(200,230) , 30*[5.0]]).T
    sticsIO.writeIrrigCal(cropmgntFile_corn2013, irrigCal_corn2013)

    # rum STICS simulation
    usm_corn2013 = "maize_reuse_2013"
    print(runUSM(dirStics, usm_corn2013))
