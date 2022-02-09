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
plt.rcParams.update({'font.size': 12})
plt.rcParams.update({'lines.linewidth' : 2.0})



##### setup plot
fig,ax = plt.subplots(figsize=(8,5))
ax.set(xlabel='Total Fertilization [kg/ha]',ylabel='[kgN ha$^{-1}$ mm$^{-1}$]', title='Overall N concentration leached')





# FN =  np.array([1])
FN = np.arange(0,21,2)


swanNtot, swanLeach, swanLeak = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiLeak, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape)






########################################################
### ref FN0 -> N0= 12.8...
######################################################

Imax=30
CNmax=3

FN0 = 80


for indx in range(len(FN)):

    print('FN = ', FN[indx])
    
    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    # ref N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    ### and add first intervention before sowing
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    ### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha
    stiLeak[indx]= np.sum(stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times) ) #mm


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    # swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    # cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha

    # swanLeach[indx]= np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times) *10
    # swanLeak[indx]= np.trapz(mdl.LeakV(sSwan), x=mdl.times) 





###### plot N leach conc
ax.plot(FN0+swanNtot, stiLeach/stiLeak, 'o', color='tab:orange', label="F$_{N0}$ = "+str(FN0)+" kg ha$^{-1}$", ls='')
# ax.plot(FN0+swanNtot, swanLeach/swanLeak, 'v', color='tab:orange', label='Control model', ls='')







# ##########################################################
# ### med N0 =10.022 
# ##########################################################

FN0=40


for indx in range(len(FN)):

    print('FN = ', FN[indx])
    
    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    # med N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    ### and add first intervention before sowing
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    ### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha
    stiLeak[indx]= np.sum(stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times) ) #mm


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    # swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    # cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha

    # swanLeach[indx]= np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times) *10
    # swanLeak[indx]= np.trapz(mdl.LeakV(sSwan), x=mdl.times) 





###### plot N leach conc
ax.plot(FN0+swanNtot, stiLeach/stiLeak, 'v', color='tab:blue', label="F$_{N0}$ = "+str(FN0)+" kg ha$^{-1}$", ls='')
# ax.plot(FN0+swanNtot, swanLeach/swanLeak, 'v', color='tab:orange', label='Control model', ls='')



















# ##########################################################
# ### low N0 =7.22 
# ##########################################################

FN0 = 0


for indx in range(len(FN)):

    print('FN = ', FN[indx])
    
    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    # ref N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    ### and add first intervention before sowing
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0], axis=0 )
    irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
    fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

    ### STICS simulation
    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
    # set fertilizer calendar
    stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
    # rum simulation
    stiIO.runUSM(usm_corn2013)
    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)
    # N leached (STICS) 
    stiLeach[indx]= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha
    stiLeak[indx]= np.sum(stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times) ) #mm


    ### SWAN model simulation
    mdl.t0=tSti[0]
    mdl.tf=tSti[-1]
    mdl.times = tSti
    mdl.s0 = Ssti[0]
    mdl.n0 = Nsti[0]
    # set climate (ET0 and rain)
    # swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
    ## set irragation
    swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
    ## set fertigation
    swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
    ## run simulation 
    # cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha

    # swanLeach[indx]= np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times) *10
    # swanLeak[indx]= np.trapz(mdl.LeakV(sSwan), x=mdl.times) 





###### plot N leach conc
ax.plot(FN0+swanNtot, stiLeach/stiLeak, 's', color='tab:gray', label="F$_{N0}$ = "+str(FN0)+" kg ha$^{-1}$", ls='')
# ax.plot(FN0+swanNtot, swanLeach/swanLeak, 'v', color='tab:orange', label='Control model', ls='')








########################################################
### ref scenario used for fit
######################################################

# FN0=80

# # #####ref scenario : used for fit
# irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
# fertiCal_corn2013 = np.array([ [120,FN0] ])

# ### STICS simulation
# # set irragation calendar
# stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
# # set fertilizer calendar
# stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
# # rum simulation
# stiIO.runUSM(usm_corn2013)
# ## load data
# stiData_corn2013 = stiIO.loadData(sti_corn2013)
# tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
# Csti = swanSti.laiTocanopy(Lsti)
# # N leached (STICS) 
# stiLeach= np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)) #kg/ha
# stiLeak= np.sum(stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times) ) #mm

# ### SWAN model simulation
# mdl.t0=tSti[0]
# mdl.tf=tSti[-1]
# mdl.times = tSti
# mdl.s0 = Ssti[0]
# mdl.n0 = Nsti[0]
# # set climate (ET0 and rain)
# # swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
# ## set irragation
# swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
# ## set fertigation
# swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
# ## run simulation 
# # cSwan, sSwan, nSwan, bSwan =  mdl.simulate()

# swanNtot= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha

# # swanLeach[indx]= np.trapz(mdl.LeachV(sSwan,nSwan), x=mdl.times) *10
# # swanLeak[indx]= np.trapz(mdl.LeakV(sSwan), x=mdl.times) 





# ###### plot N leach conc
# ax.plot(FN0+swanNtot, stiLeach/stiLeak, 'D', color='k', label="Reference", ls='')
# # ax.plot(FN0+swanNtot, swanLeach/swanLeak, 'v', color='tab:orange', label='Control model', ls='')







################## add limit
CNcrit = 0.112 # kg/(ha mm)
start, end = ax.get_xlim()
ax.plot([start, end], [CNcrit, CNcrit], 'r', label ='$C_{N crit}$')



########## finish plot


fig.legend(loc='right', ncol=1)
fig.tight_layout(rect=[0,0,0.77,1])









plt.show()
