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



# # # build executable and run executable
# clean=0
# debug=0
# verbose=1
# maxtime=10000
# bcpUtls.buildProblem(clean,debug,verbose)
# bcpUtls.launchProblem(clean,maxtime,verbose)





vals =  [3,7,12,14]
# vals =  [1,2,3,4]
# vals =  [5,10]

for maxTotFertig in vals:

    print('\n\n\n maxTotFertig ' + str(maxTotFertig) + '\n\n')

    setDir('maxTotFertig/'+str(maxTotFertig))
    bcpUtls.setInDef('constant.0','maxTotFertig',str(maxTotFertig))
    bcpUtls.setInDef('state.3.upperbound', '',str(maxTotFertig))

    # trajectory computation
    # bcpUtls.setInDef('simulatedTrajectory.computation', '', 'read_valueFunction')
    # bcpUtls.setInDef('simulatedTrajectory.starting.state.2', '', str(9) )


    bcpUtls.buildProblem(0,0,0)
    bcpUtls.launchProblem(0,100000,1)
