import numpy as np
# import matplotlib.pyplot as plt
import scipy.optimize as opt
# import math as m

from sys import path as syspath

syspath.append('../model')
# import pelakModel as mdl
import swanModel as mdl


syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO

from statistics import mean


#########################
# links STICS - Pelak
#########################


def laiTocanopy(lai):
    return ( 1 - np.exp(- mdl.exLai * lai) )


def pelakClimatFromSTICS(tjul,climateFile):
    # t = np.arange(mdl.t0,mdl.tf+1)
    t = np.arange(tjul[0],tjul[-1]+1)
    mdl.Rain = mdl.fromCalendar(t, stiIO.readClimate('rain',climateFile)[ int(tjul[0])-1:int(tjul[-1]) ] ,interKind='previous')
    mdl.ET0 = mdl.fromCalendar(t, stiIO.readClimate('ET0',climateFile)[ int(tjul[0])-1:int(tjul[-1]) ] ,interKind='previous')


def pelakIrigFromStics(tjul, stiData, varModFile=None):
    irigvals= stiIO.readOutput("airg(n)", stiData, varModFile)
    # t = np.arange(mdl.t0,mdl.tf+1)
    t = np.arange(tjul[0],tjul[-1]+1)
    tiniStics = int(stiData[0,3])
    mdl.Irig = mdl.fromCalendar(t, irigvals[ int(tjul[0])-tiniStics:int(tjul[-1])-tiniStics+1])


def pelakFertiFromStics(tjul, stiData, varModFile=None, fertilizerEffeciency=0.7):
    ''' for fertigation '''
    ferti= stiIO.readOutput("anit(n)", stiData, varModFile) *fertilizerEffeciency     # kg/ha
    ferti = ferti /10                                           # g/m^2
    irig= stiIO.readOutput("airg(n)", stiData, varModFile)      # mm
    fertigation = np.zeros(irig.size)
    fertigation[irig>0] =  ferti[irig>0] / irig[irig>0]                 # g/m^2 mm = g/L
    # t = np.arange(mdl.t0,mdl.tf+1)
    t = np.arange(tjul[0],tjul[-1]+1)
    tiniStics = int(stiData[0,3])
    mdl.Cn = mdl.fromCalendar(t, fertigation[ int(tjul[0])-tiniStics:int(tjul[-1])-tiniStics+1])


def FertiSimpleFromStics(tjul, stiData, varModFile=None, fertilizerEffeciency=0.7):
    ''' for fertilisation (without irrigation) '''
    ferti= stiIO.readOutput("anit(n)", stiData, varModFile) *fertilizerEffeciency     # kg/ha
    ferti = ferti /10                                           # g/m^2
    t = np.arange(mdl.t0,mdl.tf+1)
    tiniStics = int(stiData[0,3])
    mdl.Ferti = mdl.fromCalendar(t, ferti[ int(tjul[0])-tiniStics:int(tjul[-1])-tiniStics+1])


################################
# loading data
#############################


def sticsLSNB(tjul,stiData, tecFile, varModFile=None):
    l = stiIO.readOutput("lai(n)",stiData,varModFile)           # lai [m^2/m^2]
    s = stiIO.swcMes(stiData, tecFile)                          # [mm/mm]
    n = stiIO.totalSoilVar("AZnit", stiData) /10                # kg/ha / 10 = g/m2
    b = stiIO.readOutput("masec(n)",stiData,varModFile) *100    # T/ha *1000 /10 = kg/ha /10= g/m2
    tiniStics = int(stiData[0,3])
    itimeStics = np.array(tjul-tiniStics-1, dtype=int)
    # print(n[itimeStics[0]-1])
    return l[itimeStics], s[itimeStics], n[itimeStics], b[itimeStics]


def loadSimu(stiFileorData, tecFile, varModFile=None):
    # load data if stiData is not given
    if isinstance(stiFileorData, str):
        stiData = stiIO.loadData(stiFileorData)
    elif isinstance(stiFileorData, np.ndarray):
        stiData = stiFileorData
    else:
        print('loadSimu error : stiFileorData must be string or np.ndarray')

    stages = stiIO.readStages_corn(stiData, varModFile)
    t0Jul = stages['lev']      # initial time as date ~ 'julian day'
    tfJul = stages['rec']     # final time as date
    tJul = np.arange(int(t0Jul),int(tfJul))

    # read stics variables
    l,s,n,b = sticsLSNB(tJul, stiData, tecFile, varModFile)

    return tJul,l,s,n,b


def loadSimu_fromSow(stiFileorData, tecFile, varModFile=None):
    # load data if stiData is not given
    if isinstance(stiFileorData, str):
        stiData = stiIO.loadData(stiFileorData)
    elif isinstance(stiFileorData, np.ndarray):
        stiData = stiFileorData
    else:
        print('loadSimu error : stiFileorData must be string or np.ndarray')

    stages = stiIO.readStages_corn(stiData, varModFile)
    t0Jul = stages['sow']      # initial time as date ~ 'julian day'
    tfJul = stages['rec']     # final time as date
    tJul = np.arange(int(t0Jul),int(tfJul))

    # read stics variables
    l,s,n,b = sticsLSNB(tJul, stiData, tecFile, varModFile)

    return tJul,l,s,n,b


def sticsTimes(stiFileorData, stage):
    # load data if stiData is not given
    if isinstance(stiFileorData, str):
        stiData = stiIO.loadData(stiFileorData)
    elif isinstance(stiFileorData, np.ndarray):
        stiData = stiFileorData
    else:
        print('loadSimu error : stiFileorData must be string or np.ndarray')

    stages = stiIO.readStages_corn(stiData, None)
    return stages[stage]

############################
## printing functions
##########################

def printParams(pnames):
    for p in pnames:
        print('mdl.'+ p + ' = ' + str(getattr(mdl, p)) )


def printRMSE(dataStics):
    ### print relative root mean square error on each variable
    varlist=('C','S','N','B')
    var_index = [0,1,2,3]
    rmse = relRMSE_pervar([], [], dataStics, var_index)
    print('rRMSE : \t' + '\t'.join(['{:<5}'.format(varlist[i]) for i in range(len(var_index))]))
    print('\t' * 3 + '\t'.join(['{:<5.2%}'.format(rmse[i]) for i in range(len(var_index))]))
    print('Mean rRMSE : ', '{:<5.2%}'.format(mean(rmse), len(var_index)))

def saveRMSE(dataStics, file, indx=''):
    ### save to file relative root mean square error on each variable
    var_index = [0,1,2,3]
    rmse = relRMSE_pervar([], [], dataStics, var_index)
    with open(file, 'a') as f :
        f.write(str(indx) + ', ' + ', '.join(['{:5.3}'.format(rmse[i]) for i in range(len(var_index))]) )
        f.write('\n')


###################
# error functions
###################

def paramErrorCSN(pVals,pNames,LsnbStics):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])

    # if 'phi' in pNames:
    #     mdl.Sw = outStics.totalSwp /mdl.phi
    # if 'rG' in pNames:
    #     mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * mdl.ET0ref

    LStc, sStc, nStc, bStc = LsnbStics

    mdl.IC=[mdl.c0, sStc[0]/mdl.phi, nStc[0], 0]
    tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1),tol=1e-4 )

    # error on variables
    # cErr = np.sum( (cStc-cPelak)**2 )
    # sErr = np.sum( (sStc - mdl.phi*sPelak)**2 )
    # nErr = np.sum( (nStc-nPelak)**2 )
    # bErr = np.sum( (bStc-bPelak)**2 )

    cErr = np.abs( laiTocanopy(LStc)-cPelak ) /max(laiTocanopy(LStc))
    sErr = np.abs( sStc - mdl.phi*sPelak ) /max(sStc)
    nErr = np.abs( nStc-nPelak ) /max(nStc)

    return cErr + sErr + nErr



def paramCerror(pVals,pNames,LsnbStics):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])
    # if 'rG' in pNames:
    #     mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * maxET0

    LStc, sStc, nStc, bStc = LsnbStics

    mdl.IC=[mdl.c0, sStc[0]/mdl.phi, nStc[0], 0]
    tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1),tol=1e-4 )

    # return np.sum( (cStc-cPelak)**2 )
    return laiTocanopy(LStc)-cPelak


def paramSerror(pVals,pNames,LsnbStics):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])

    # if 'phi' in pNames:
    #     mdl.Sw = outStics.totalSwp /mdl.phi
    #     mdl.Sfc = outStics.totalSfc /mdl.phi
    # if 'rG' in pNames:
    #     mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * mdl.ET0ref


    LStc, sStc, nStc, bStc = LsnbStics
    mdl.IC=[mdl.c0, sStc[0]/mdl.phi, nStc[0], 0]
    tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1),tol=1e-4 )

    # return np.sum( (sStc - mdl.phi*sPelak)**2 )
    return sStc - mdl.phi*sPelak


def paramNerror(pVals,pNames,LsnbStics):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])

    LStc, sStc, nStc, bStc = LsnbStics
    mdl.IC=[mdl.c0, sStc[0]/mdl.phi, nStc[0], 0]
    tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1),tol=1e-4 )

    # return np.sum( (nStc-nPelak)**2 )
    return nStc-nPelak


def paramBerror(pVals,pNames,LsnbStics):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])

    LStc, sStc, nStc, bStc = LsnbStics
    mdl.IC=[mdl.c0, sStc[0]/mdl.phi, nStc[0], 0]
    tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1),tol=1e-4 )

    # return np.sum( (bStc-bPelak)**2 )
    return bStc-bPelak





#### ---------- RMSE ----------------------


# pour penaliser certaines variables
weights = np.ones(9)

def relRMSE(pVals,pNames,data,varIndex,verbose=False):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])


    sim = mdl.simulate()[varIndex]

    nvar, ntdata = data.shape
    err=0
    for iv in range(nvar):
        err += weights[iv] * (np.sum( (sim[iv] - data[iv])**2 )/ntdata )**(1/2)  /mean(data[iv])  
        
    if verbose:
        print(err/nvar)
    
    return err/nvar



def relRMSE_pervar(pVals,pNames,data,varIndex):
    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pVals[iP])

    sim = mdl.simulate()[varIndex]

    nvar, ntdata = data.shape
    err = np.zeros(nvar)

    for iv in range(nvar):
        err[iv] = (np.sum( (sim[iv] - data[iv])**2 )/ntdata )**(1/2)  /mean(data[iv]) 
        # print(sim[iv],data[iv],err[iv])

    return err



##############################
## Constraint functions
#############################

def consMaxC(pvals=[], pNames=[]):
    # to have c at 'equilibrium' <1
    # unstressed, equilibrium is C = rG/rM * etaC * Kcb * ET0
    # so to have 1 >=0 C need 1 - rG/rM * etaC * Kcb * ET0 >=0

    for iP in range(len(pNames)):
        setattr(mdl, pNames[iP], pvals[iP])

    maxC = 0.983
    # return maxC - mdl.rG/mdl.rM * mdl.etaC *mdl.Kcb * mdl.ET0ref
    return maxC - mdl.rG/mdl.rM 



############################
# fitting functions
#########################


def fitPelak_ls(pNames,bnds,errFun,dataStics,varIndex=[0,1,2,3],pini=None, ptol=1e-8):
    if pini is None:
        pini = np.zeros(len(pNames))
        for iP in range(len(pNames)):
            pini[iP]=getattr(mdl, pNames[iP])

    mdl.printParams(pNames)
    res = opt.least_squares(errFun, pini, args=(pNames, dataStics,varIndex), bounds=bnds, method='dogbox', verbose=2, xtol=ptol)
    # res = opt.minimize(errFun, pini, args=(pNames, dataStics), bounds=bnds, method='L-BFGS-B', options={'iprint':1})
    print(res.message)
    mdl.printParams(pNames)





def fitPelak_min(pNames,bnds,errFun,dataStics,varIndex=[0,1,2,3],cons=(),pini=None, ptol=1e-8):
    if pini is None:
        pini = np.zeros(len(pNames))
        for iP in range(len(pNames)):
            pini[iP]=getattr(mdl, pNames[iP])

    mdl.printParams(pNames)
    res = opt.minimize(errFun, pini, args=(pNames, dataStics, varIndex), bounds=list(zip(*bnds)), method='SLSQP', options={'disp': True,'iprint':2}, constraints=cons)
    # res = opt.minimize(errFun, pini, args=(pNames, dataStics, varIndex), bounds=list(zip(*bnds)), method='L-BFGS-B', options={'iprint':1})
    print(res.message)
    mdl.printParams(pNames)







#
# if __name__ == "__main__":
#
#     import plotPelak as pltPlk
#
#
#     ## load stics data
#
#     t0Jul = outStics.tlev      # initial time as date ~ 'julian day'
#     tfJul = outStics.tharv     # final time as date
#     mdl.tf=tfJul-1-t0Jul
#     # mdl.tsen=218-t0Jul
#     tIniStics=int(outStics.simData[0,outStics.iday])       # date of begining of stics data
#     itimeStics=np.arange(t0Jul-tIniStics,tfJul-tIniStics,dtype=int)    # range of index oresponding to [t0,tf]
#     timeStics = np.arange(itimeStics.size)
#
#
#     LStics = outStics.simData[itimeStics,outStics.ilai]
#     # cStics=laiTocanopy(LStics)
#     sStics = outStics.sMes[itimeStics]
#     nStics = outStics.totalNO3[itimeStics] /10                  # kg/ha / 10 = g/m2
#     bStics = outStics.simData[itimeStics,outStics.imasecn] *100     # T/ha *1000 /10
#
#     dataStics = LStics, sStics, nStics, bStics
#
#     maxCstics = max(laiTocanopy(LStics))
#     maxET0 = max(outStics.climateData[int(t0Jul)-1:int(tfJul)-1,outStics.jET0])
#
#
#     #################
#     # setup ref case
#     ################
#
#     # setup ref case / initial guess
#     # S
#     mdl.phi = outStics.totalSfc +0.2            # 0.37 +0.2 = 0.57
#     mdl.Sw = outStics.totalSwp /mdl.phi         # 0.30
#     mdl.Sfc = outStics.totalSfc/mdl.phi         # 0.65
#     mdl.Sstar = (mdl.Sfc +mdl.Sw)/2             # 0.47
#     # printParams(['Sfc','Sw'])
#
#
#
#
#     # irrig and climate
#     # irigvals= outStics.simData[itimeStics,outStics.iirrig]
#     # mdl.Irig = mdl.fromCalendar(timeStics,irigvals)
#     rdStics.pelakIrigFromStics()
#     rdStics.pelakClimatFromSTICS(t0jul=t0Jul,tfjul=tfJul)
#
#     # mdl.IC=[mdl.c0, sStics[0]/mdl.phi, nStics[0], 0]
#
#
#     ### best params
#
#     # from stics
#     mdl.tsen=218-t0Jul          #90
#     mdl.Z=1000
#
#     mdl.gamma = 1e-5
#     mdl.exLai=0.6
#
#
#     ## no constraint on max C
#     mdl.phi = 0.6518
#     mdl.Sw = outStics.totalSwp /mdl.phi     # 0.26810
#     # print(mdl.Sw)
#     mdl.Sstar = 0.36757
#     mdl.d = 11.1079
#     mdl.etaC = 0.03186
#     mdl.Kcb = 1.47
#     mdl.rG = 0.7
#     mdl.rM = 0.15
#     mdl.Wstar = 25.141
#
#
#     ## to have max C = 1 with rM = rG * etaC * KCb * maxET0
#     # mdl.phi = 0.6420181706742826
#     # mdl.Sstar = 0.3466894706102225
#     # mdl.Sw = outStics.totalSwp /mdl.phi
#     # mdl.d = 11.511389278545426
#     # mdl.etaC = 0.02924276398710387
#     # mdl.Kcb = 1.4546621930734567
#     # mdl.rG = 0.7107236729197304
#     # mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * maxET0
#     # mdl.Wstar = 25.141
#
#
#     ### params unchanged from pelak
#     mdl.Kce=1.1
#     mdl.Sh=0.14
#     mdl.ksat=0.33*1000
#     mdl.a=1
#
#
#     ################ first fit to get an initial guess
#
#     # pname = ['phi','Sstar', 'd', 'Kcb', 'etaC', 'rG', 'rM' , 'exLai' ]
#     # lbnd =  [ 0.4 ,  0.1  ,  5 ,  0.5 ,  0.01 ,  0.1,  1e-4,  0.5  ]
#     # ubnd =  [ 0.7 ,  0.5  ,  15,   2  ,  0.1  ,  3  ,  1   ,  0.9 ]
#     # fitPelak(pname,(lbnd,ubnd),paramErrorCSN)
#
#     # mdl.phi = 0.7
#     # mdl.Sstar = 0.43523039617640585
#     # mdl.d = 8.684488694333506
#     # mdl.Kcb = 1.7033919160183537
#     # mdl.etaC = 0.0316939250859323
#     # mdl.rG = 0.44817854086264675
#     # mdl.rM = 0.03686756761638355
#
#
#     ################ second fit : each variable independently
#
#     # S
#     # pnameS = ['phi','Sstar', 'd']
#     # lbndS =  [ 0.3 ,  0.1  ,  5 ]
#     # ubndS =  [ 0.7 ,  0.5  ,  15]
#     # fitPelak(pnameS,(lbndS,ubndS),paramSerror,ptol=1e-10)
#     # mdl.phi = 0.6518041882138348
#     # mdl.Sstar = 0.3677575936748158
#     # mdl.d = 11.1079377150618
#
#
#     # N
#     # pnameN = ['etaC']
#     # lbndN = [1e-5]
#     # ubndN = [1]
#     # fitPelak(pnameN,(lbndN,ubndN),paramNerror,ptol=1e-10)
#     # # fitPelak(pnameN,list(zip(lbndN,ubndN)),paramNerror,ptol=1e-10)
#     # mdl.etaC = 0.031865009220130046
#
#     # C
#     # pnameC= ['rG', 'rM', 'Kcb']
#     # lbndC = [0   , 0   , 0.5  ]
#     # ubndC = [10  , 10  , 1.1  ]
#     # fitPelak(pnameC,(lbndC,ubndC),paramCerror)
#     # fitPelak(pnameC,(lbndC,ubndC),paramErrorCSN)
#     # mdl.rG = 1.5150527090819532
#     # mdl.rM = 0.13265357733891853
#     # mdl.Kcb = 0.6466566026594232
#
#     # to have c at 'equilibrium' <1
#     # mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * maxET0
#     # pnameC= ['rG', 'Kcb']
#     # lbndC = [0   , 0.5  ]
#     # ubndC = [2   , 3    ]
#     # # fitPelak(pnameC,(lbndC,ubndC),paramCerror)
#     # fitPelak(pnameC,(lbndC,ubndC),paramErrorCSN)
#
#
#
#     ### B
#     # pnameB= ['Wstar' ]
#     # lbndB = [0    ]
#     # ubndB = [100  ]
#     # fitPelak(pnameB,(lbndB,ubndB),paramBerror)
#     # mdl.Wstar = 25.141
#
#
#     ################
#     # final fit
#     ################
#
#     # pname = ['phi','Sstar', 'd', 'Kcb', 'etaC', 'rG' , 'rM' ]
#     # lbnd =  [ 0.4 ,  0.2  ,  5 ,  1   ,  0.01 ,  0.3 ,  1e-4 ]
#     # ubnd =  [ 0.8 ,  0.6  , 15 ,  2   ,  0.1  ,  3   ,  1  ]
#     # fitPelak(pname,(lbnd,ubnd),paramErrorCSN)
#
#     # mdl.phi = 0.6508089491906941
#     # mdl.Sstar = 0.3542301620031244
#     # mdl.Kcb = 1.3524608448004845
#     # mdl.etaC = 0.031082263894562017
#     # mdl.rG = 0.7607650210327137
#     # mdl.rM = 0.14152637325633793
#
#
#
#
#
#
#     # print('Max C = rG/rM * etaC * KCb * maxET0 = ', mdl.rG/mdl.rM * mdl.etaC * mdl.Kcb * maxET0  )
#
#
#
#
#     mdl.IC=[mdl.c0, sStics[0]/mdl.phi, nStics[0], 0]
#     tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=timeStics, tol=1e-4 )
#     # mdl.printSimuInfo(tPelak, cPelak, sPelak, nPelak, bPelak)
#
#     fig,ax = pltPlk.varproc_Setup_2x3()
#     pltPlk.varProc_2x3( ax, tPelak, cPelak, sPelak, nPelak, bPelak )
#     pltPlk.var_2x3( ax, timeStics, laiTocanopy(LStics), sStics/mdl.phi, nStics, bStics, sty='+', lbl=' stics')
#
#     ## add stics Process / stresses
#     ax[1,0].plot(timeStics,outStics.simData[itimeStics,outStics.iWstress],'-+', color='tab:blue', label='W stress Stics' )
#     ax[1,0].plot(timeStics,outStics.simData[itimeStics,outStics.iinns],'-+', color='tab:orange', label='N stress Stics' )
#     leakageStics = outStics.simData[itimeStics,outStics.idrain]
#     ax[1,1].plot(timeStics, -leakageStics, '+', color='k', label=r'L Stics')
#     NleachStics=outStics.Nleach[itimeStics] / 10        # kg/ha / 10 = g/m2
#     ax[1,2].plot(timeStics, -NleachStics, '+', color='k', label=r'NO$_3$ leaching Stics')
#
#
#     pltPlk.finalize_2d(ax)
#
#
#     plt.tight_layout()
#     plt.show()
