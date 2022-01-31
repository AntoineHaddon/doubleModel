import scipy.integrate as integrate
import scipy.interpolate as interpolate
import numpy as np
import matplotlib.pyplot as plt
import scipy.ndimage as filter
# import scipy.signal as filter

import sys
sys.path.append('/home/ahaddon/bin')
import readValsFromFile as rdvl
sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
import swanModel as mdl
import plotSwan as pltSwan


def readBocopResults(dirname):

    # bocop HJB
    timeBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.times')
    timeBocop=timeBocop[:,0]

    ctrlBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.controls')
    It=np.append(ctrlBocop[:,0],ctrlBocop[-1,0])

    # case control 2 : cn
    # Ndose=np.append(ctrlBocop[:,1],ctrlBocop[-1,1])

    # case control 2 : I*cn
    CNt=np.zeros(It.size)
    for i in range(It.size-1):
        if It[i]>0:
            CNt[i]=ctrlBocop[i,1]/ctrlBocop[i,0]
        else:
            CNt[i]=0
    CNt[-1]=CNt[-2]

    stateBocop = rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.states')
    Ct=stateBocop[:,0]
    St=stateBocop[:,1]
    Nt=stateBocop[:,2]

    return timeBocop, Ct, St, Nt, It, CNt




def readBocopResultsBio(dirname):

    # bocop HJB
    timeBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.times')
    timeBocop=timeBocop[:,0]

    ctrlBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.controls')
    It=np.append(ctrlBocop[:,0],ctrlBocop[-1,0])

    # case control 2 : cn
    # Ndose=np.append(ctrlBocop[:,1],ctrlBocop[-1,1])

    # case control 2 : I*cn
    CNt=np.zeros(It.size)
    for i in range(It.size-1):
        if It[i]>0:
            CNt[i]=ctrlBocop[i,1]/ctrlBocop[i,0]
        else:
            CNt[i]=0
    CNt[-1]=CNt[-2]

    stateBocop = rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.states')
    Ct=stateBocop[:,0]
    St=stateBocop[:,1]
    Nt=stateBocop[:,2]
    Bt=stateBocop[:,3]

    return timeBocop, Ct, St, Nt, Bt, It, CNt



def readBocopResultsFixIrrig(dirname):

    # bocop HJB
    timeBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.times')
    timeBocop=timeBocop[:,0]

    ctrlBocop=rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.controls')
    ICnt=np.append(ctrlBocop[:,0],ctrlBocop[-1,0])

    stateBocop = rdvl.readVals(dirname+'/trajectory/simulatedTrajectory.states')
    Ct=stateBocop[:,0]
    St=stateBocop[:,1]
    Nt=stateBocop[:,2]

    # Irig : MRAP
    # It = mdl.ImrapV(timeBocop, x=np.array((St,Ct)).T )

    return timeBocop, Ct, St, Nt, ICnt






def simPelakBocop(timBcp,Ibcp,CNbcp):
    # redefine controls
    # bocophjb
    mdl.Irig=interpolate.interp1d(timBcp, Ibcp,kind='previous' )
    mdl.Cn=interpolate.interp1d(timBcp, CNbcp,kind='previous' )

    # return mdl.simPelak()
    return mdl.simulate()


def rainBocop(rainFile):
    rain = rdvl.readVals(rainFile)
    t=np.arange(rain.size)
    # mdl.Rain = mdl.fromCalendar(t, rain[:,0] ,interKind='previous')
    mdl.Rain = interpolate.interp1d(t, rain[:,0],kind='previous' )

def ET0Bocop(ET0File):
    et0 = rdvl.readVals(ET0File)
    t=np.arange(et0.size)
    mdl.ET0 = interpolate.interp1d(t, et0[:,0],kind='previous' )




# FNs = [5,6,7,8,9,10]
# FNs = [0,1,2,3,4,5,6,7,8,9,10,11,12]
FNs = np.arange(20+1)

for indx,FN in enumerate(FNs):

# if __name__ == "__main__":

    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 18})


    # # bocop HJB
    maindir='/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/'

    ### mlus
    # # dir='maxBio_TotFerConstr_mlus/maxTotFertig/14/'
    # dir='maxBio_TotFerConstr_mlus/maxTotFertig_highN0/10/'
    # # # dir='maxBio_TotFerConstr_mlus/maxTotFertig/'+str(FN)+'/'
    # paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fiti'
    # rainBocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/data/rain_mlus96')
    # ET0Bocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/data/ET0_mlus96')

    ### corn2013
    # dir='maxBio_TotFerConstr_corn2013/maxTotFertig/7/'
    # dir='maxBio_TotFerConstr_corn2013/maxTotFertig/'+str(FN)+'/'
    # dir='maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar12/'+str(FN)+'/'
    dir='maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN)+'/'
    paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/params_swan_Iref_Corn2013'
    rainBocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/rain_corn2013')
    ET0Bocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/ET0_corn2013')




    #################################
    # plot single trajectory
    #################################


    # timeBocop, Ctbocop, Stbocop, Ntbocop, Btbocop, Itbocop, CNtbocop = readBocopResultsBio(maindir+dir)
    timeBocop, Ctbocop, Stbocop, Ntbocop, Itbocop, CNtbocop = readBocopResults(maindir+dir)

    mdl.t0= timeBocop[0]
    mdl.tf=timeBocop[-1]
    mdl.times = timeBocop

    

    mdl.readParams(paramFile)
    # mdl.ET0 = interpolate.interp1d([0, mdl.tf] , [mdl.ET0ref, mdl.ET0ref] ,kind='previous' )


    mdl.c0=Ctbocop[0]
    mdl.s0=Stbocop[0]
    mdl.n0=Ntbocop[0]
    mdl.b0=0


    # times, Can, SoilM, Nitro, Biom = simPelakBocop(timeBocop, filter.median_filter(Itbocop, size=20), filter.median_filter(CNtbocop, size=20) , IC)
    Can, SoilM, Nitro, Biom = simPelakBocop(timeBocop, Itbocop, CNtbocop)
    mdl.printSimuInfo(mdl.times, Can, SoilM, Nitro, Biom)



    # fig,ax = pltSwan.varproc_Setup_2x3()

    # pltSwan.varProc_2x3( ax, mdl.times, Can, SoilM, Nitro, Biom)
    # # pltSwan.var_2x3( ax, timeBocop, Ctbocop, Stbocop, Ntbocop, np.zeros(timeBocop.shape), sty='.', lbl=' bocop')

    # pltSwan.finalize_2d(ax)

    # plt.tight_layout()
    # # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/presentation/controlOptReuse/img/bcpHJB-minNitromass-Canconstr.pdf')
    # plt.show()

    

    ################################
    #### write irrig calendar
    ###############################

    sys.path.append('/home/ahaddon/bin')
    import writeVals as wrt
    dirCtrl = maindir+dir

    ## corn2013
    tSti = np.arange(128,247)
    wrt.writeValstoFile(dirCtrl+ "corn2013-bcp-I-Ni7.csv", np.array( [tSti, mdl.Irig(tSti-tSti[0]) ]).T   )
    wrt.writeValstoFile(dirCtrl + "corn2013-bcp-Cn-Ni7.csv", np.array( [tSti, mdl.Cn(tSti-tSti[0]) ]).T   )

    ## mlus
    # tSti = np.arange(138,311)
    # wrt.writeValstoFile(dirCtrl+ "mlus96-bcp-I.csv", np.array( [tSti, mdl.Irig(tSti-tSti[0]) ]).T   )
    # wrt.writeValstoFile(dirCtrl + "mlus96-bcp-Cn.csv", np.array( [tSti, mdl.Cn(tSti-tSti[0]) ]).T   )




    #################################
    # plot several scenarios together
    #################################

    # dir='maxBio/valueFunction-cnmax35-Imax10-tf140/'
    # Tf=140
    # dir='maxBio/valueFunction-cnmax0.05-tf100/'
    # Tf=100
    #
    # fig,ax=mdl.plotPelakVertSetup(Tf)
    #
    # n0 = (1,8.2,15)
    # lsty=('k','b','k--')
    #
    # # sosFilter = filter.butter(1, 0.1, output='sos')
    #
    # for in0 in range(3):
    #
    #     timeBocop, Ctbocop, Stbocop, Ntbocop, Itbocop, CNtbocop = readBocopResults(maindir+dir+'n'+str(n0[in0])+'/')
    #     C0=Ctbocop[0]
    #     S0=Stbocop[0]
    #     N0=Ntbocop[0]
    #     IC = [C0,S0,N0,0]
    #
    #     times, Can, SoilM, Nitro, Biom = simPelakBocop(timeBocop, filter.median_filter(Itbocop, size=20), filter.median_filter(CNtbocop, size=20) , IC)
    #
    #     mdl.plotPelakVert(ax,times, Can, SoilM, Nitro, Biom, sty=lsty[in0])
    #     print('\n\nN(0)='+str(n0[in0]))
    #     mdl.printSimuInfo(times, Can, SoilM, Nitro, Biom)
    #
    #
    # ax[0].legend(('Scenario 1','Scenario 2','Scenario 3'))
    # # ax[0].legend(('Scenario 4','Scenario 5','Scenario 6'))#, loc="lower right", bbox_to_anchor=(1.05,0))
    # plt.tight_layout()
    # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/Ctrl4Reuse ADCHEM21/figs/Crop-Scenarios-FNmax35.pdf')
    # plt.show()
    #
    #





    # plt.plot(times,leacht, label='Leaching',linewidth=3.0)
    # plt.title(r"N leaching [kg/m2 d]")
    # plt.xlabel("Time[d]")
    # plt.grid()
    # plt.tight_layout()
    # plt.show()



    # # write initial guess for BocopNLP
    # import writeInitBocopNLP as wrt
    # initIrrigDir = "/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/pelak/bocop/maxBio/init/"
    # # irrig
    # wrt.writeBocopInit(initIrrigDir+"control.0.init", times, mdl.Irig(times) )
    # # i *cn
    # wrt.writeBocopInit(initIrrigDir+"control.1.init", times, mdl.Irig(times) *mdl.Cn(times) )
    # # canopy
    # wrt.writeBocopInit(initIrrigDir+"state.0.init", times, Can )
    # # s soil moisture
    # wrt.writeBocopInit(initIrrigDir+"state.1.init", times, SoilM )
    # # N nitrogen
    # wrt.writeBocopInit(initIrrigDir+"state.2.init", times, Nitro )
    # # biomass
    # wrt.writeBocopInit(initIrrigDir+"state.3.init", times, Biom )
