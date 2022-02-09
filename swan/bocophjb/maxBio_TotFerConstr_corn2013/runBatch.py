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

def setTrajDir(dirname):
    try:
        os.mkdir(dirname)
    except OSError as error:
        pass
    bcpUtls.setInDef('simulatedTrajectory.output.path', dirname+'/trajectory/','')


# BT=0.4
# #
# setDir('BT/'+str(BT))
# #
# # # change value in .def file
# bcpUtls.setInDef('constant.0','biomassT',str(BT))



# # # build executable and run executable
clean=0
debug=0
verbose=1
maxtime=10000
# bcpUtls.buildProblem(clean,debug,verbose)
# bcpUtls.launchProblem(clean,maxtime,verbose)



maxFNbar = 20
maxI=30
maxCN=5
setDir('maxTotFertig/maxFNbar'+str(maxFNbar)+'-I'+str(maxI)+'-CN'+str(maxCN))

# FN(T)=<maxFNbar
bcpUtls.setInDef('state.3.upperbound', '',str(maxFNbar))

bcpUtls.setInDef('control.0.upperbound', '',str(maxI))
bcpUtls.setInDef('control.1.upperbound', '',str(maxI*maxCN/100))
bcpUtls.setInDef('constant.0', 'cnMax',str(maxCN/100))



############################
# value function computation
###########################


# bcpUtls.setInDef('simulatedTrajectory.computation', '', 'after_valueFunction')

# bcpUtls.buildProblem(0,0,0)
# bcpUtls.launchProblem(0,100000,1)







# ###########################
# # trajectory computation
# ##########################



maxTotFertig =  np.arange(maxFNbar+1)

for FNbar in maxTotFertig:

    print('\n\n\n maxTotFertig ' + str(FNbar) + '\n\n')

    setTrajDir( 'maxTotFertig/maxFNbar'+str(maxFNbar)+'-I'+str(maxI)+'-CN'+str(maxCN)+'/'+str(FNbar))


    # trajectory computation
    bcpUtls.setInDef('simulatedTrajectory.computation', '', 'read_valueFunction')

    # FN(t) = FN(0)+ \int_0^t I*Cn dt
    # constraint on total fertig : \int_0^Tf I*Cn dt<=FNbar -> FN(Tf) - FN(0)=<FNbar
    # imposed with FN(0) = maxFNbar - FNbar and FN(T)=<maxFNbar
    bcpUtls.setInDef('simulatedTrajectory.starting.state.3', '', str(maxFNbar-FNbar) )
    if FNbar == 0:
        bcpUtls.setInDef('simulatedTrajectory.starting.state.3', '', str(maxFNbar-0.00001) )
    if FNbar == maxFNbar:
        bcpUtls.setInDef('simulatedTrajectory.starting.state.3', '', str(0.00001) )

    #N0
    # bcpUtls.setInDef('simulatedTrajectory.starting.state.2', '', str(12.824) )
    # bcpUtls.setInDef('simulatedTrajectory.starting.state.2', '', str(10.022) )
    # bcpUtls.setInDef('simulatedTrajectory.starting.state.2', '', str(7.221) )
    bcpUtls.setInDef('simulatedTrajectory.starting.state.2', '', str(18.428) )


    bcpUtls.buildProblem(0,0,0)
    bcpUtls.launchProblem(0,100000,1)
