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

fig,ax = plt.subplots(3,2,figsize=(12,9) )

# plt.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.08, hspace = 0.25)

numYticks=3


ax[0,0].set(title=r' Relative Soil Moisture', ylabel=r'[m$^3$ m$^{-3}$]')
ax[0,0].set(xlabel="Time [d]")
ax[0,0].set_ylim( 0 , 0.6)
start, end = ax[0,0].get_ylim()
ax[0,0].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[0,1].set(title=r'Soil Nitrogen', ylabel=r'[g m$^{-2}$]')
ax[0,1].set(xlabel="Time [d]")
ax[0,1].set_ylim( 5, 15)
# ax[0,1].set(title=r'Soil Nitrogen Concentration', ylabel=r'[g L$^{-1}$]'))
# ax[0,1].set_ylim( 0.01,0.04)
start, end = ax[0,1].get_ylim()
ax[0,1].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[1,0].set(title='Irrigation', ylabel=r'[mm d$^{-1}$]')
ax[1,0].set(xlabel="Time [d]")
ax[1,0].set_ylim( 0 , 30)
start, end = ax[1,0].get_ylim()
ax[1,0].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[1,1].set(title=r'Fertilisation', ylabel=r'[g m$^{-2}$ d$^{-1}$] ')
ax[1,1].set(xlabel="Time [d]")
ax[1,1].set_ylim( 0 , 1)
start, end = ax[1,1].get_ylim()
ax[1,1].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[2,0].set(title=r'Crop Biomass', ylabel=r'[T ha$^{-1}$]')
ax[2,0].set(xlabel="Time [d]")
ax[2,0].set_ylim( 0 , 23)
start, end = ax[2,0].get_ylim()
ax[2,0].yaxis.set_ticks(np.linspace(start, 20, numYticks))

ax[2,1].set_axis_off()


# remove top and right axis/ box boundary
for a in ax:
    for aa in a:
        aa.spines['top'].set_visible(False)
        aa.spines['right'].set_visible(False)

# remove x ticks for top row plots
# ax[0,0].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)
# ax[0,1].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)






########### only controls

figC,axC = plt.subplots(1,2,figsize=(12,5) )

axC[0].set(title='Irrigation', ylabel=r'[mm d$^{-1}$]')
axC[0].set(xlabel="Time [d]")
axC[0].set_ylim( -1 , 11)
start, end = axC[0].get_ylim()
axC[0].yaxis.set_ticks(np.linspace(0, 10, numYticks))

axC[1].set(title=r'N concentration', ylabel=r'[mg L$^{-1}$] ')
axC[1].set(xlabel="Time [d]")
axC[1].set_ylim( -5 , 55)
start, end = axC[1].get_ylim()
axC[1].yaxis.set_ticks(np.linspace(0, 50, numYticks))


# remove top and right axis/ box boundary
for aa in axC:
    aa.spines['top'].set_visible(False)
    aa.spines['right'].set_visible(False)









########################################################
### 1
######################################################

FN0= 8
FN = 7



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

print(tSti[0], mdl.t0, tSti[-1])

###### plot
ax[0,0].plot(tSti, Ssti,  color='tab:orange')
ax[0,1].plot(tSti, Nsti,  color='tab:orange')
# ax[0,1].plot(tSti, Nsti/(Ssti*mdl.Z), color='tab:orange')
ax[0,1].plot(tSti, mdl.etaC*mdl.Z*Ssti, '--', color='tab:orange', label=r'$\eta_{c} Z S(t)$')

# ax[0,0].plot(mdl.times, sSwan, color='tab:orange')
# ax[0,1].plot(mdl.times, nSwan, color='tab:orange')
# ax[0,1].plot(mdl.times, nSwan/(sSwan*mdl.Z), color='tab:orange')
# ax[0,1].plot(mdl.times, mdl.etaC*mdl.Z*sSwan, '--', color='tab:orange', label=r'$\eta_{c} Z S(t)$')


# ax[1,0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:orange', label=r"Irrigation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")
# ax[1,1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:orange', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")

ax[1,0].plot(tSti, mdl.Irig(tSti), color='tab:orange', label=r"$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
ax[1,1].plot(tSti, mdl.Irig(tSti)*mdl.Cn(tSti), color='tab:orange')

if FN0>0:
    ax[1,1].bar(fertiCal_corn2013[0,0], fertiCal_corn2013[0,1], color='tab:orange' )

ax[2,0].plot(tSti, Bsti/100,  color='tab:orange')






axC[0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:orange')
axC[1].plot(mdl.times, mdl.Cn(mdl.times)*1000, color='tab:orange', label="$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")






########################################################
### 2
######################################################

FN0=4
FN =11


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
ax[0,0].plot(tSti, Ssti,  color='tab:blue')
ax[0,1].plot(tSti, Nsti,  color='tab:blue')
# ax[0,1].plot(tSti, Nsti/(Ssti*mdl.Z), color='tab:blue')
ax[0,1].plot(tSti, mdl.etaC*mdl.Z*Ssti, '--', color='tab:blue', label=r'$\eta_{c} Z S(t)$')

# ax[0,0].plot(mdl.times, sSwan, color='tab:blue')
# ax[0,1].plot(mdl.times, nSwan, color='tab:blue')
# ax[0,1].plot(mdl.times, nSwan/(sSwan*mdl.Z), color='tab:blue')
# ax[0,1].plot(mdl.times, mdl.etaC*mdl.Z*sSwan, '--', color='tab:blue', label=r'$\eta_{c} Z S(t)$')


# ax[1,0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:blue', label=r"Irrigation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")
# ax[1,1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:blue', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")

ax[1,0].plot(tSti, mdl.Irig(tSti), color='tab:blue', label=r"$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
ax[1,1].plot(tSti, mdl.Irig(tSti)*mdl.Cn(tSti), color='tab:blue')


if FN0>0:
    ax[1,1].bar(fertiCal_corn2013[0,0], fertiCal_corn2013[0,1], color='tab:orange' )

ax[2,0].plot(tSti, Bsti/100,  color='tab:blue')





axC[0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:blue')
axC[1].plot(mdl.times, mdl.Cn(mdl.times)*1000, color='tab:blue', label="$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")








########################################################
### 3
######################################################

FN0=0
FN =15


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
ax[0,0].plot(tSti, Ssti,  color='tab:gray')
ax[0,1].plot(tSti, Nsti,  color='tab:gray')
# ax[0,1].plot(tSti, Nsti/(Ssti*mdl.Z), color='tab:gray')
ax[0,1].plot(tSti, mdl.etaC*mdl.Z*Ssti, '--', color='tab:gray', label=r'$\eta_{c} Z S(t)$')

# ax[0,0].plot(mdl.times, sSwan, color='tab:gray')
# ax[0,1].plot(mdl.times, nSwan, color='tab:gray')
# ax[0,1].plot(mdl.times, nSwan/(sSwan*mdl.Z), color='tab:gray')
# ax[0,1].plot(mdl.times, mdl.etaC*mdl.Z*sSwan, '--', color='tab:gray', label=r'$\eta_{c} Z S(t)$')


# ax[1,0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:gray', label=r"Irrigation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")
# ax[1,1].plot(mdl.times, mdl.Irig(mdl.times)*mdl.Cn(mdl.times), color='tab:gray', label="Fertilisation, $\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$")

ax[1,0].plot(tSti, mdl.Irig(tSti), color='tab:gray', label=r"$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")
ax[1,1].plot(tSti, mdl.Irig(tSti)*mdl.Cn(tSti), color='tab:gray')

if FN0>0:
    ax[1,1].bar(fertiCal_corn2013[0,0], fertiCal_corn2013[0,1], color='tab:orange' )

ax[2,0].plot(tSti, Bsti/100,  color='tab:gray')





axC[0].plot(mdl.times, mdl.Irig(mdl.times), color='tab:gray')
axC[1].plot(mdl.times, mdl.Cn(mdl.times)*1000, color='tab:gray', label="$\overline{F} =$ "+str(FN*10)+" kg ha$^{-1}$, F$_{N0}$ = "+str(FN0*10)+" kg ha$^{-1}$")







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







########### plot extras
ax[0,0].plot([tSti[0], tSti[-1]], mdl.Sstar*np.ones((2,1)), 'r--', label='$S^*$' )
# ax[0,1].plot([mdl.t0, mdl.tf], [mdl.etaC, mdl.etaC], 'r-.', label=r'$\eta_{c}$')

# ax[1,0].plot(tSti, mdl.ET0(tSti), color='tab:brown', label='ET$_0$' )
# ax[1,0].bar(tSti, mdl.Rain(tSti), color='c', label='Rain' )

ax[1,0].plot(tSti, stiIO.readClimate('ET0',cli_corn2013)[ int(tSti[0])-1:int(tSti[-1]) ], color='tab:brown', label='ET$_0$' )
ax[1,0].bar(tSti, stiIO.readClimate('rain',cli_corn2013)[ int(tSti[0])-1:int(tSti[-1]) ], color='k', label='Rain' )





############## legends

ax[0,0].legend()

from matplotlib.lines import Line2D
legend_elements = [ Line2D([0], [0], color='r', ls='--', label='$N_{crit}(S)$') ]
ax[0,1].legend(handles=legend_elements)#,loc='lower center')


# legend_elements = [ Line2D([0], [0], color='tab:orange', label='$\overline{F} =$ 80 kg ha$^{-1}$, F$_{N0}$ = 80 kg ha$^{-1}$'), 
#                     Line2D([0], [0], color='tab:blue', label= '$\overline{F} =$ 120 kg ha$^{-1}$, F$_{N0}$ = 40 kg ha$^{-1}$'),
#                     Line2D([0], [0], color='tab:gray', label= '$\overline{F} =$ 160 kg ha$^{-1}$, F$_{N0}$ = 0 kg ha$^{-1}$'),
#                     Line2D([0], [0], color='tab:brown', label='$ET_0$'), 
#                     Line2D([0], [0], color='k', label='Rain') ]
# fig.legend(handles=legend_elements,loc='upper left', bbox_to_anchor=(0.6, 0.3), ncol=1)
# fig.tight_layout()




handles, labels = ax[1,0].get_legend_handles_labels()
leg=fig.legend(handles, labels,loc='upper left', bbox_to_anchor=(0.6, 0.3), ncol=1)
leg.legendHandles[-1].set(height=1.5,y=3)
fig.tight_layout()




figC.legend(loc='lower center',bbox_to_anchor=(0.5, -0.0), ncol=1)
figC.subplots_adjust(bottom=0.15)
figC.tight_layout(rect=[0,0.15,1,1])



plt.show()
