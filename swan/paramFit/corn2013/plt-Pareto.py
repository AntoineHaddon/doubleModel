import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate

import sys
sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
import swanModel as mdl
# import plotPelak as pltPlk

sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit')
import swanFitStics as swanSti

sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO

sys.path.append('/home/ahaddon/bin')
import readValsFromFile as rdvl






## stics files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
sti_corn2013 = stiIO.dirStics + 'mod_smaize_reuse_2013.sti'
tec_corn2013 = stiIO.dirStics + "maize_reuse_tec.xml"
cli_corn2013 = stiIO.dirStics + 'sitej.2013'        
# cli_corn2013 = stiIO.dirStics + 'meteo-site2-1994.2013'
usm_corn2013 = "maize_reuse_2013"
# set initial conditons file
stiIO.setIniFile(usm_corn2013,"maize_ini.xml")


### model parameters  irrig ref, 
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/params_swan_Iref_Corn2013'
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
### ref N0 = 12.8...
######################################################

FN0 = 80

# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])
# FN = np.arange(8,15,2)
FN = np.arange(0,21)


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
Crmse, Srmse, Nrmse, Brmse = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)



for indx in range(len(FN)):

    print('FN = ', FN[indx])
    
    #### Controls from bocop
    dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN[indx])+'/'
    # ref N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    ### and add first intervention before sowing
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,80.0], axis=0 )
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
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim)
# ax[0].plot(FN0+swanNtot, swanBiof,  color=clCtrl)

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clCtrl, label =lbCtrl)

# ax[2].plot(stiLeach, stiBiof,  color=clSim)
# ax[2].plot(swanLeach, swanBiof,  color=clCtrl)
ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)

ax[3].plot(swanItot, stiLeach,  color=clSim)

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
### med N0 =10.022 
##########################################################

FN0 = 40


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
    dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN[indx])+'/'
    # med N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    # med N0
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,40.0], axis=0 )
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
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim)
# ax[0].plot(FN0+swanNtot, swanBiof,  color=clCtrl)

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clCtrl, label =lbCtrl)

# ax[2].plot(stiLeach, stiBiof,  color=clSim)
# ax[2].plot(swanLeach, swanBiof,  color=clCtrl)
ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)

ax[3].plot(swanItot, stiLeach,  color=clSim)


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
### low N0 =7.22 
##########################################################

FN0 = 0


# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])
# FN = np.arange(0,21,2)
# FN = np.arange(0,21)


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
Crmse, Srmse, Nrmse, Brmse = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)



for indx in range(len(FN)):

    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN[indx])+'/'
    # low N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
    # low N0
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,0.0], axis=0 )
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

# ax[0].plot(FN*10, stiBiof,  color=clSim)
# ax[0].plot(FN*10, swanBiof,  color=clCtrl)
ax[0].plot(FN0+swanNtot, stiBiof,  color=clSim)
# ax[0].plot(swanNtot, swanBiof,  color=clCtrl)

ax[1].plot(swanItot, stiBiof,  color=clSim, label=lbSim)
# ax[1].plot(swanItot, swanBiof,  color=clCtrl, label =lbCtrl)

# ax[2].plot(stiLeach, stiBiof,  color=clSim)
# ax[2].plot(swanLeach, swanBiof,  color=clCtrl)
ax[2].plot(FN0+swanNtot, stiLeach,  color=clSim)

ax[3].plot(swanItot, stiLeach,  color=clSim)


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
legend_elements = [ Line2D([0], [0], color='tab:orange', marker='1', label='F$_{N0}$=80 kg ha$^{-1}$'), 
                    Line2D([0], [0], color='tab:blue', marker='x', label= 'F$_{N0}$=40 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:gray', marker='+', label= 'F$_{N0}$=0 kg ha$^{-1}$')   ]

fig.legend(handles=legend_elements,loc='lower center', ncol=3)
# fig.subplots_adjust(bottom=0.75)   
fig.tight_layout(rect=[0,0.05,1,1])


# fig.legend(handles=legend_elements,loc='upper left', bbox_to_anchor=(0.65, 0.35))
# fig.tight_layout()







##### only Ntot |-> Bio
# fig3,ax3 = plt.subplots()

# ax3.plot(plkNtot, stiBiof,  marker='+', color='tab:orange', linestyle='')
# ax3.plot(plkNtot, plkBiof,  marker='o', color='tab:blue', linestyle='')
# ax3.set(xlabel='Total Fertilization [kg/ha]',ylabel='Final Biomass [T/ha]')
# ax3.legend(['Simulation model', 'Control Model'],loc='lower center',bbox_to_anchor=(0.5, -.35), ncol=2)

# fig3.tight_layout()





plt.show()
