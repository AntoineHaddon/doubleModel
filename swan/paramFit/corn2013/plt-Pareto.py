import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate


from os import getcwd
cwd = getcwd()

from sys import path as syspath
syspath.append(cwd+'/../../model')
import swanModel as mdl
import plotSwan as pltSwan
syspath.append(cwd+'/..')
import swanFitStics as swanSti
syspath.append(cwd+'/../../../stics/pyScripts')
import sticsIOutils as stiIO


syspath.append(cwd+'/../../../utils')
import readValsFromFile as rdvl





## stics files
stiIO.dirStics = cwd+'/../../../stics/corn/'
sti_corn2013 = stiIO.dirStics + 'mod_smaize_reuse_2013.sti'
tec_corn2013 = stiIO.dirStics + "maize_reuse_tec.xml"
cli_corn2013 = stiIO.dirStics + 'sitej.2013'        
# cli_corn2013 = stiIO.dirStics + 'meteo-site2-1994.2013'
usm_corn2013 = "maize_reuse_2013"
# set initial conditons file
stiIO.setIniFile(usm_corn2013,"maize_ini.xml")


### model parameters  irrig ref, 
paramFile = cwd+'/params_swan_Iref_Corn2013'
mdl.readParams(paramFile)


##### setup plots
plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})
plt.rcParams.update({'lines.linewidth' : 2.0})
# plt.rcParams.update({'lines.markersize': 4})

##### setup plot pareto fronts
# fig,ax = plt.subplots(1,3,figsize=(15,5))
fig,ax = plt.subplots(2,2,figsize=(10,9))
ax=np.ravel(ax)


ax[0].set(xlabel='Total Fertilization [kg/ha]',ylabel='Final Biomass [T/ha]')
ax[1].set(xlabel='Total Irrigation [mm]',ylabel='Final Biomass [T/ha]')
# ax[2].set(xlabel='Total Leaching [kg/ha]',ylabel='Final Biomass [T/ha]')
ax[2].set(xlabel='Total Fertilization [kg/ha]',ylabel='Total Leaching [kg/ha]')
ax[3].set(xlabel='Total Irrigation [mm]',ylabel='Total Leaching [kg/ha]')

clr=['b','r','g','tab:blue','y','tab:pink','tab:brown','tab:purple','xkcd:puke','xkcd:navy blue','tab:orange','c','tab:olive']
mkrsty=['.','o','v','^','<','>']


# remove 4th graph
# ax[3].set_axis_off()




########################################################
### 1
######################################################

FN0=80
Imax=30
CNmax=5


# FN =  np.array([1])
FN = np.arange(0,21,2)


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
Crmse, Srmse, Nrmse, Brmse = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)



for indx in range(len(FN)):
    print('FN = ', FN[indx])
    
    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    if FN0==160: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni18.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni18.csv")
    if FN0==80: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    if FN0==40: # med FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    if FN0==0: # low FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]


    #### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    #Final Biomass (STICS)  
    stiBiof[indx]= Bsti[-1]/100 # T/ha
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    totalIrrig = np.trapz(mdl.Irig(mdl.times), x=mdl.times)
    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)
    totalLeach = np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times)

    swanBiof[indx]= bSwan[-1]/100      # T/ha
    swanNtot[indx]= totalNfert*10    # kg/ha
    swanItot[indx]= totalIrrig       # mm
    swanLeach[indx]= totalLeach*10   # kg/ha





###### plot pareto front
clSim = 'tab:orange'
clCtrl = 'tab:green'
lbSim = 'Simulation model, FN$_0$=80 kg ha$^{-1}$'
lbSim = 'FN$_0$=80 kg ha$^{-1}$'
lbCtrl = 'Control model, FN$_0$=80 kg ha$^{-1}$'

# ax[0].plot(FN0+FN*10, stiBiof,  color=clSim)
# ax[0].plot(FN0+FN*10, swanBiof,  color=clCtrl)
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim, label='$F_{N0}$= '+str(FN0)+', $I_{max}$ = '+str(Imax)+', $C_{Nmax}$ = '+str(CNmax*10))
# ax[0].plot(FN0+swanNtot, swanBiof,  color=clSim, ls='--')

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clSim, ls='--')

ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)
# ax[2].plot(FN0+swanNtot, swanLeach,  color=clSim, ls='--')

ax[3].plot(swanItot, stiLeach,  color=clSim)
# ax[3].plot(swanItot, swanLeach,  color=clSim, ls='--')

for i in range(len(FN)):
    cl = clr[i%13]
    mkrSim='1'
    # ax[0].plot(FN0+FN[i]*10, stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN0+FN[i]*10, swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[0].plot(FN0+swanNtot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN0+swanNtot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    ax[1].plot(swanItot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[1].plot(swanItot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    # ax[2].plot(stiLeach[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[2].plot(swanLeach[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[2].plot(FN0+swanNtot[i], stiLeach[i],  marker=mkrSim, color=cl, linestyle='')

    ax[3].plot(swanItot[i], stiLeach[i], marker=mkrSim, color=cl, linestyle='')










##########################################################
### 2
##########################################################

FN0=40
Imax=30
CNmax=5


# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])
# FN = np.arange(0,19,2)
# FN = np.arange(0,21)


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
Crmse, Srmse, Nrmse, Brmse = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)



for indx in range(len(FN)):
    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    if FN0==160: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni18.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni18.csv")
    if FN0==80: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    if FN0==40: # med FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    if FN0==0: # low FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    #### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    #Final Biomass (STICS)  
    stiBiof[indx]= Bsti[-1]/100 # T/ha
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    totalIrrig = np.trapz(mdl.Irig(mdl.times), x=mdl.times)
    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)
    totalLeach = np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times)

    swanBiof[indx]= bSwan[-1]/100      # T/ha
    swanNtot[indx]= totalNfert*10    # kg/ha
    swanItot[indx]= totalIrrig       # mm
    swanLeach[indx]= totalLeach*10   # kg/ha



########### plot pareto fronts
clSim = 'tab:blue'
clCtrl = 'tab:purple'
lbSim = 'Simulation model, FN$_0$=40 kg ha$^{-1}$'
lbSim = 'FN$_0$=40 kg ha$^{-1}$'
lbCtrl = 'Control model, FN$_0$=40 kg ha$^{-1}$'

# ax[0].plot(FN0+FN*10, stiBiof,  color=clSim)
# ax[0].plot(FN0+FN*10, swanBiof,  color=clCtrl)
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim, label='$F_{N0}$= '+str(FN0)+', $I_{max}$ = '+str(Imax)+', $C_{Nmax}$ = '+str(CNmax*10))
# ax[0].plot(FN0+swanNtot, swanBiof,  color=clSim, ls='--')

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clSim, ls='--')

ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)
# ax[2].plot(FN0+swanNtot, swanLeach,  color=clSim, ls='--')

ax[3].plot(swanItot, stiLeach,  color=clSim)
# ax[3].plot(swanItot, swanLeach,  color=clSim, ls='--')

for i in range(len(FN)):
    cl = clr[i%13]
    mkrSim='x'
    # ax[0].plot(FN0+FN[i]*10, stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN0+FN[i]*10, swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[0].plot(FN0+swanNtot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN0+swanNtot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    ax[1].plot(swanItot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[1].plot(swanItot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    # ax[2].plot(stiLeach[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[2].plot(swanLeach[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[2].plot(FN0+swanNtot[i], stiLeach[i],  marker=mkrSim, color=cl, linestyle='')

    ax[3].plot(swanItot[i], stiLeach[i], marker=mkrSim, color=cl, linestyle='')











##########################################################
### 3
##########################################################

FN0=0
Imax=30
CNmax=5


# FN =  np.array([1])
# FN = np.arange(0,21,2)

for indx in range(len(FN)):
    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    if FN0==160: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni18.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni18.csv")
    if FN0==80: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    if FN0==40: # med FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    if FN0==0: # low FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    #### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    #Final Biomass (STICS)  
    stiBiof[indx]= Bsti[-1]/100 # T/ha
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    totalIrrig = np.trapz(mdl.Irig(mdl.times), x=mdl.times)
    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)
    totalLeach = np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times)

    swanBiof[indx]= bSwan[-1]/100      # T/ha
    swanNtot[indx]= totalNfert*10    # kg/ha
    swanItot[indx]= totalIrrig       # mm
    swanLeach[indx]= totalLeach*10   # kg/ha



########### plot pareto fronts
clSim = 'tab:gray'
clCtrl = 'tab:red'
lbSim = 'Simulation model, FN$_0$=0 kg ha$^{-1}$'
lbSim = 'FN$_0$=0 kg ha$^{-1}$'
lbCtrl = 'Control model, FN$_0$=0 kg ha$^{-1}$'

# ax[0].plot(FN0+FN*10, stiBiof,  color=clSim)
# ax[0].plot(FN0+FN*10, swanBiof,  color=clCtrl)
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim, label='$F_{N0}$= '+str(FN0)+', $I_{max}$ = '+str(Imax)+', $C_{Nmax}$ = '+str(CNmax*10))
# ax[0].plot(FN0+swanNtot, swanBiof,  color=clSim, ls='--')

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clSim, ls='--')

ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)
# ax[2].plot(FN0+swanNtot, swanLeach,  color=clSim, ls='--')

ax[3].plot(swanItot, stiLeach,  color=clSim)
# ax[3].plot(swanItot, swanLeach,  color=clSim, ls='--')

for i in range(len(FN)):
    cl = clr[i%13]
    mkrSim='+'
    # ax[0].plot(FN[i]*10, stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN[i]*10, swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[0].plot(FN0+swanNtot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(swanNtot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    ax[1].plot(swanItot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[1].plot(swanItot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    # ax[2].plot(stiLeach[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[2].plot(swanLeach[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[2].plot(FN0+swanNtot[i], stiLeach[i],  marker=mkrSim, color=cl, linestyle='')

    ax[3].plot(swanItot[i], stiLeach[i], marker=mkrSim, color=cl, linestyle='')









##########################################################
### 4
##########################################################

FN0=160
Imax=30
CNmax=5


FN =  np.array([0])
# FN = np.arange(0,21,2)

for indx in range(len(FN)):
    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    if FN0==160: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni18.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni18.csv")
    if FN0==80: # hi FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    if FN0==40: # med FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    if FN0==0: # low FN0
        irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
        fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    #### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    #Final Biomass (STICS)  
    stiBiof[indx]= Bsti[-1]/100 # T/ha
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    totalIrrig = np.trapz(mdl.Irig(mdl.times), x=mdl.times)
    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)
    totalLeach = np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times)

    swanBiof[indx]= bSwan[-1]/100      # T/ha
    swanNtot[indx]= totalNfert*10    # kg/ha
    swanItot[indx]= totalIrrig       # mm
    swanLeach[indx]= totalLeach*10   # kg/ha



########### plot pareto fronts
clSim = 'tab:red'
clCtrl = 'tab:red'
lbSim = 'Simulation model, FN$_0$=0 kg ha$^{-1}$'
lbSim = 'FN$_0$=0 kg ha$^{-1}$'
lbCtrl = 'Control model, FN$_0$=0 kg ha$^{-1}$'

# # ax[0].plot(FN0+FN*10, stiBiof,  color=clSim)
# # ax[0].plot(FN0+FN*10, swanBiof,  color=clCtrl)
# ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim, label='$F_{N0}$= '+str(FN0)+', $I_{max}$ = '+str(Imax)+', $C_{Nmax}$ = '+str(CNmax*10))
# # ax[0].plot(FN0+swanNtot, swanBiof,  color=clSim, ls='--')

# ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# # ax[1].plot(swanItot, swanBiof,  color=clSim, ls='--')

# ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)
# # ax[2].plot(FN0+swanNtot, swanLeach,  color=clSim, ls='--')

# ax[3].plot(swanItot, stiLeach,  color=clSim)
# # ax[3].plot(swanItot, swanLeach,  color=clSim, ls='--')

for i in range(len(FN)):
    cl = clr[i%13]
    mkrSim='d'
    # ax[0].plot(FN[i]*10, stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(FN[i]*10, swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[0].plot(FN0+swanNtot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[0].plot(swanNtot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    ax[1].plot(swanItot[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[1].plot(swanItot[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    
    # ax[2].plot(stiLeach[i], stiBiof[i],  marker=mkrSim, color=cl, linestyle='')
    # ax[2].plot(swanLeach[i], swanBiof[i],  marker='o', color=cl, linestyle='')
    ax[2].plot(FN0+swanNtot[i], stiLeach[i],  marker=mkrSim, color=cl, linestyle='')

    ax[3].plot(swanItot[i], stiLeach[i], marker=mkrSim, color=cl, linestyle='')









# ########################################################
# ### ref scenario used for fit
# ######################################################



# # #####ref scenario : used for fit
# irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
# fertiCal_corn2013 = np.array([ [120,80.0] ])
# stiIO.setIniFile(usm_corn2013,"maize_ini.xml")
# # set initial conditons file
# stiIO.setIniFile(usm_corn2013,"maize_ini.xml")


# #### STICS simulation
# # set irragation calendar
# stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
# # set fertilizer calendar
# stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
# # rum simulation
# stiIO.runUSM(usm_corn2013)
# ## load data
# stiData_corn2013 = stiIO.loadData(sti_corn2013)
# tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
# Csti = swanSti.laiTocanopy(Lsti)
# #Final Biomass (STICS)  
# stiBiof= Bsti[-1]/100 # T/ha
# # N leached (STICS) 
# stiLeach= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha

# ### SWAN model simulation
# mdl.t0=tSti[0]
# mdl.tf=tSti[-1]
# mdl.times = tSti
# mdl.s0 = Ssti[0]
# mdl.n0 = Nsti[0]
# # set climate (ET0 and rain)
# swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
# ## set irragation
# swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
# ## set fertigation
# swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
# ## run simulation 
# cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

# totalIrrig = np.trapz(mdl.Irig(mdl.times), x=mdl.times)
# totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)
# totalLeach = np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times)
# swanBiof= bSwan[-1]/100      # T/ha
# swanNtot= totalNfert*10    # kg/ha
# swanItot= totalIrrig       # mm
# swanLeach= totalLeach*10   # kg/ha




# ########### pareto front
# ax[0].plot([0], stiBiof,  'k+')
# ax[0].plot([0], swanBiof,  'ko')
    
# ax[1].plot(swanItot, stiBiof,  'k+', label = 'Simulation model, reference')
# ax[1].plot(swanItot, swanBiof,  'ko', label = 'Control model, reference')
    
# ax[2].plot(stiLeach, stiBiof,  'k+')
# ax[2].plot(swanLeach, swanBiof,  'ko')










########## finish pareto front plot

from matplotlib.lines import Line2D
legend_elements = [ 
                    Line2D([0], [0], color='b', marker='d', ls='', label= 'F$_{N0}$=160 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:orange', label='F$_{N0}$=80 kg ha$^{-1}$'), 
                    Line2D([0], [0], color='tab:blue', label= 'F$_{N0}$=40 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:gray', label= 'F$_{N0}$=0 kg ha$^{-1}$')   
                    ]

fig.legend(handles=legend_elements,loc='lower center', ncol=2)
# fig.subplots_adjust(bottom=0.75)   
fig.tight_layout(rect=[0,0.1,1,1])




# handles, labels = ax[0].get_legend_handles_labels()
# fig.legend(handles, labels,loc='lower center', ncol=2)
# fig.tight_layout(rect=[0,0.1,1,1])










plt.show()
