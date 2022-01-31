import numpy as np
import subprocess as sproc

import sticsIOutils as sticsIO



JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'


def runUSM(wdir,usm):
    return sproc.run(["java", "-jar", "JavaSticsCmd.exe", "--run", wdir, usm], cwd=JavaSticsDir)





if __name__ == "__main__":

    wDir_corn2013 = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'

    # set irragation calendar
    cropmgntFile_corn2013 = wDir_corn2013 + "maize_reuse_tec.xml"
    irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
    # irrigCal_corn2013 = np.array([ range(200,230) , 30*[5.0]]).T
    sticsIO.writeIrrigCal(cropmgntFile_corn2013, irrigCal_corn2013)

    # rum STICS simulation
    usm_corn2013 = "maize_reuse_2013"
    print(runUSM(wDir_corn2013, usm_corn2013))
