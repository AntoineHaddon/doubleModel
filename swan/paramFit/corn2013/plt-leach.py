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


### model parameters  irrig ref, 
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/params_swan_Iref_Corn2013'
mdl.readParams(paramFile)


##### setup plots
plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 14})


fig,ax = plt.subplots(1,2,figsize=(12,5))

# plt.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.08, hspace = 0.25)

numYticks=3

ax[0].set(title='Water Leakage', ylabel=r'[mm d$^{-1}$]')
ax[0].set(xlabel="Time - day of year")
ax[0].set_ylim( 0 , 35)
start, end = ax[0].get_ylim()
ax[0].yaxis.set_ticks(np.linspace(start, 30, numYticks))

ax[1].set(title=r'Nitrogen Leaching', ylabel=r'[g m$^{-2}$ d$^{-1}$] ')
ax[1].set(xlabel="Time - day of year")
ax[1].set_ylim( 0 , 0.5)
start, end = ax[1].get_ylim()
ax[1].yaxis.set_ticks(np.linspace(start, end, numYticks))




# remove top and right axis/ box boundary

for aa in ax:
    aa.spines['top'].set_visible(False)
    aa.spines['right'].set_visible(False)
















########################################################
### 1
######################################################

FN0= 8
FN = 8



print('FN = ', FN)
    
#### Controls from bocop
dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN)+'/'
if FN0==8: # hi FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
if FN0==4: # med FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
if FN0==0: # low FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
### for bocop and MRAP
### conversion of fertilization calendar from concentration to mass
fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
### and add first intervention before sowing
# low FN0
fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0*10], axis=0 )
irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

# set initial conditons file
stiIO.setIniFile(usm_corn2013,"maize_ini.xml")

#### STICS simulation
# set irragation calendar
stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
# set fertilizer calendar
stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
# rum simulation
stiIO.runUSM(usm_corn2013)
## load data
stiData_corn2013 = stiIO.loadData(sti_corn2013)
# tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
Csti = swanSti.laiTocanopy(Lsti)


### SWAN model simulation
mdl.t0=swanSti.sticsTimes(stiData_corn2013, 'lev')
it0= mdl.t0 - tSti[0]
mdl.tf=tSti[-1]
mdl.times = np.arange(mdl.t0,mdl.tf+1)
mdl.s0 = Ssti[int(it0)]
mdl.n0 = Nsti[int(it0)]
# set climate (ET0 and rain)
swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
## set irragation
swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
## set fertigation
swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
## run simulation 
cSwan, sSwan, nSwan, bSwan =  mdl.simulate()



###### plot
ax[0].plot(mdl.times, mdl.LeakV(sSwan), color='tab:orange',  label="Control model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
ax[0].plot(mdl.times, stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times-1), '--', color='tab:orange', label="Simulation model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")


# ax[1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:orange', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg/ha")
ax[1].plot(mdl.times, mdl.LeachV(sSwan,nSwan), color='tab:orange')
NleachStics=stiIO.Nleach(stiData_corn2013,tJul=mdl.times-1) / 10        # kg/ha / 10 = g/m2
ax[1].plot(mdl.times, NleachStics, '--', color='tab:orange')










# # ########################################################
# # ### 2
# # ######################################################

# FN0= 4
# FN = 12



# print('FN = ', FN)
    
# #### Controls from bocop
# dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN)+'/'
# if FN0==8: # hi FN0
#     irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
#     fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
# if FN0==4: # med FN0
#     irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
#     fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
# if FN0==0: # low FN0
#     irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
#     fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
# ### for bocop and MRAP
# ### conversion of fertilization calendar from concentration to mass
# fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
# ### and add first intervention before sowing
# # low FN0
# fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0*10], axis=0 )
# irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
# fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

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
# # tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
# tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
# Csti = swanSti.laiTocanopy(Lsti)


# ### SWAN model simulation
# mdl.t0=swanSti.sticsTimes(stiData_corn2013, 'lev')
# it0= mdl.t0 - tSti[0]
# mdl.tf=tSti[-1]
# mdl.times = np.arange(mdl.t0,mdl.tf+1)
# mdl.s0 = Ssti[int(it0)]
# mdl.n0 = Nsti[int(it0)]
# # set climate (ET0 and rain)
# swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
# ## set irragation
# swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
# ## set fertigation
# swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
# ## run simulation 
# cSwan, sSwan, nSwan, bSwan =  mdl.simulate()



# ###### plot
# ax[0].plot(mdl.times, mdl.LeakV(sSwan), color='tab:blue',  label="Control model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
# ax[0].plot(mdl.times, stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times-1), '--', color='tab:blue', label="Simulation model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")


# # ax[1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:blue', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg/ha")
# ax[1].plot(mdl.times, mdl.LeachV(sSwan,nSwan), color='tab:blue')
# NleachStics=stiIO.Nleach(stiData_corn2013,tJul=mdl.times-1) / 10        # kg/ha / 10 = g/m2
# ax[1].plot(mdl.times, NleachStics, '--', color='tab:blue')












# ########################################################
# ### 3
# ######################################################

FN0= 0
FN = 16



print('FN = ', FN)
    
#### Controls from bocop
dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20/'+str(FN)+'/'
if FN0==8: # hi FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
if FN0==4: # med FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
if FN0==0: # low FN0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
### for bocop and MRAP
### conversion of fertilization calendar from concentration to mass
fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
### and add first intervention before sowing
# low FN0
fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,FN0*10], axis=0 )
irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

# set initial conditons file
stiIO.setIniFile(usm_corn2013,"maize_ini.xml")

#### STICS simulation
# set irragation calendar
stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
# set fertilizer calendar
stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
# rum simulation
stiIO.runUSM(usm_corn2013)
## load data
stiData_corn2013 = stiIO.loadData(sti_corn2013)
# tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu_fromSow(stiData_corn2013, tec_corn2013)
Csti = swanSti.laiTocanopy(Lsti)


### SWAN model simulation
mdl.t0=swanSti.sticsTimes(stiData_corn2013, 'lev')
it0= mdl.t0 - tSti[0]
mdl.tf=tSti[-1]
mdl.times = np.arange(mdl.t0,mdl.tf+1)
mdl.s0 = Ssti[int(it0)]
mdl.n0 = Nsti[int(it0)]
# set climate (ET0 and rain)
swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
## set irragation
swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
## set fertigation
swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
## run simulation 
cSwan, sSwan, nSwan, bSwan =  mdl.simulate()



###### plot
ax[0].plot(mdl.times, mdl.LeakV(sSwan), color='tab:gray',  label="Control model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
ax[0].plot(mdl.times, stiIO.readOutput("drain", stiData_corn2013,tJul=mdl.times-1), '--', color='tab:gray', label="Simulation model, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")


# ax[1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:gray', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg/ha")
ax[1].plot(mdl.times, mdl.LeachV(sSwan,nSwan), color='tab:gray')
NleachStics=stiIO.Nleach(stiData_corn2013,tJul=mdl.times-1) / 10        # kg/ha / 10 = g/m2
ax[1].plot(mdl.times, NleachStics, '--', color='tab:gray')















########################################################
### ref scenario used for fit
######################################################



# #####ref scenario : used for fit
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


###### plot
# ax[0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:orange', label=r"Irrigation, Reference")
# ax[1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:orange', label='Fertilisation, Reference')












############## legends




handles, labels = ax[0].get_legend_handles_labels()
leg=fig.legend(handles, labels,loc='lower center',bbox_to_anchor=(0.5, -0.0), ncol=2)
fig.subplots_adjust(bottom=0.15)
fig.tight_layout(rect=[0,0.15,1,1])


plt.show()
