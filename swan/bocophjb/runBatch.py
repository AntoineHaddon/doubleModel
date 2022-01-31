import numpy as np
import sys
sys.path.append('/home/ahaddon/Programs/bocop/BocopHJB-1.1.0-Linux/scripts/python/')
import BocopHJBUtils as bcpUtls
import os


#set ouput dir for val function and trajectory
def setDir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as error:
        pass
    bcpUtls.setInDef('valueFunction.output.path', dirname+'/valueFunction/','')
    bcpUtls.setInDef('simulatedTrajectory.output.path', dirname+'/trajectory/','')



# BT=0.4
# #
# setDir('BT/'+str(BT))
# #
# # # change value in .def file
# bcpUtls.setInDef('constant.0','biomassT',str(BT))
# #
# # # build executable and run executable
# clean=0
# debug=0
# verbose=1
# maxtime=10000
# bcpUtls.buildProblem(clean,debug,verbose)
# bcpUtls.launchProblem(clean,maxtime,verbose)



for maxTotFertig in [0.009,0.01,0.011,0.012,0.013]:

    print('\n\n\n\n\n maxTotFertig ' + str(maxTotFertig) + '\n\n\n\n')

    setDir('maxTotFertig/'+str(maxTotFertig))
    bcpUtls.setInDef('constant.0','maxTotFertig',str(maxTotFertig))
    # bcpUtls.setInDef('state.3.upperbound', '',str(maxTotFertig))

    bcpUtls.buildProblem(0,0,0)
    bcpUtls.launchProblem(0,100000,1)
