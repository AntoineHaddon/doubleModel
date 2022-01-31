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

fig,ax = plt.subplots(2,2,figsize=(12,6))

# plt.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.08, hspace = 0.25)

numYticks=3

ax[0,0].set(title=r'Crop Biomass', ylabel=r'[T ha$^{-1}$]', xlabel='Time [d]')
# ax[0,0].set(ylabel=r'B [kg m$^{-2}$]')
ax[0,0].set_ylim( 0 , 23)
start, end = ax[0,0].get_ylim()
ax[0,0].yaxis.set_ticks(np.linspace(start, 20, numYticks))

ax[0,1].set(title=r'Canopy Cover', ylabel=r'[m$^2$ m$^{-2}$] ', xlabel='Time [d]')
# ax[0,1].set(ylabel=r'C [m$^2$ m$^{-2}$] '))
ax[0,1].set_ylim( 0 , 1)
start, end = ax[0,1].get_ylim()
ax[0,1].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[1,0].set(title=r' Relative Soil Moisture', ylabel=r'[m$^3$ m$^{-3}$]', xlabel='Time [d]')
# ax[1,0].set(ylabel=r'S [m$^3$ m$^{-3}$]')
ax[1,0].set_ylim( 0 , 0.6)
start, end = ax[1,0].get_ylim()
ax[1,0].yaxis.set_ticks(np.linspace(start, end, numYticks))

ax[1,1].set(title=r'Soil Nitrogen', ylabel=r'[g m$^{-2}$]', xlabel='Time [d]')
# ax[1,1].set(ylabel=r'$N$ [g m$^{-2}$]'))
ax[1,1].set_ylim( 0 , 14)
start, end = ax[1,1].get_ylim()
ax[1,1].yaxis.set_ticks(np.linspace(start, end, numYticks))


# remove top and right axis/ box boundary
for a in ax:
    for aa in a:
        aa.spines['top'].set_visible(False)
        aa.spines['right'].set_visible(False)

# remove x ticks for top row plots
# ax[0,0].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)
# ax[0,1].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)
# ax[1,0].set(xlabel="Time - day of year")
# ax[1,1].set(xlabel="Time - day of year")







########################################################
### ref N0 = 12.8...
######################################################

# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
FN =  np.array([8])




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
    tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
    Csti = swanSti.laiTocanopy(Lsti)


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




###### plot
ax[0,0].plot(tSti, Bsti/100,  color='tab:blue', ls='--')
ax[0,1].plot(tSti, Csti,  color='tab:blue', ls='--')
ax[1,0].plot(tSti, Ssti, color='tab:blue', ls='--')
ax[1,1].plot(tSti, Nsti, color='tab:blue', ls='--')

ax[0,0].plot(mdl.times, bSwan/100,  color='tab:blue')
ax[0,1].plot(mdl.times, cSwan,  color='tab:blue')
ax[1,0].plot(mdl.times, sSwan, color='tab:blue')
ax[1,1].plot(mdl.times, nSwan, color='tab:blue')










##########################################################
# ### N) = 9.92 ..
# ##########################################################



# # FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([8])




# for indx in range(len(FN)):

#     print('FN = ', FN[indx])

#     #### Controls from bocop
#     dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar12/'+str(FN[indx])+'/'
#     # low N0
#     irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni9.csv")
#     fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni9.csv")
#     ### for bocop and MRAP
#     ### conversion of fertilization calendar from concentration to mass
#     ### and add first intervention before sowing
#     fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
#     fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,80.0], axis=0 )
#     irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
#     fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]

#     # set initial conditons file
#     stiIO.setIniFile(usm_corn2013,"maize_lowN0_ini.xml")

#     #### STICS simulation
#     # set irragation calendar
#     stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
#     # set fertilizer calendar
#     stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)
#     # rum simulation
#     stiIO.runUSM(usm_corn2013)
#     ## load data
#     stiData_corn2013 = stiIO.loadData(sti_corn2013)
#     tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
#     Csti = swanSti.laiTocanopy(Lsti)

#     ### SWAN model simulation
#     mdl.t0=tSti[0]
#     mdl.tf=tSti[-1]
#     mdl.times = tSti
#     mdl.s0 = Ssti[0]
#     mdl.n0 = Nsti[0]
#     # set climate (ET0 and rain)
#     swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
#     ## set irragation
#     swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
#     ## set fertigation
#     swanSti.pelakFertiFromStics(tSti, stiData_corn2013)
#     ## run simulation 
#     cSwan, sSwan, nSwan, bSwan =  mdl.simulate()



# ###### plot
# clSim = 'tab:orange'
# clCtrl = 'tab:blue'

# ax[0,0].plot(tSti, Bsti/100,  color=clSim, ls='--')
# ax[0,1].plot(tSti, Csti,  color=clSim, ls='--')
# ax[1,0].plot(tSti, Ssti, color=clSim, ls='--')
# ax[1,1].plot(tSti, Nsti, color=clSim, ls='--')

# ax[0,0].plot(mdl.times, bSwan/100,  color=clCtrl, ls='--')
# ax[0,1].plot(mdl.times, cSwan,  color=clCtrl, ls='--')
# ax[1,0].plot(mdl.times, sSwan, color=clCtrl, ls='--')
# ax[1,1].plot(mdl.times, nSwan, color=clCtrl, ls='--')











# ########################################################
# ### ref scenario used for fit
# ######################################################



# #####ref scenario : used for fit
irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
fertiCal_corn2013 = np.array([ [120,80.0] ])
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
tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
Csti = swanSti.laiTocanopy(Lsti)


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




###### plot
ax[0,0].plot(tSti, Bsti/100,  color='tab:orange', ls='--')
ax[0,1].plot(tSti, Csti,  color='tab:orange', ls='--')
ax[1,0].plot(tSti, Ssti, color='tab:orange', ls='--')
ax[1,1].plot(tSti, Nsti, color='tab:orange', ls='--')

ax[0,0].plot(mdl.times, bSwan/100,  color='tab:orange')
ax[0,1].plot(mdl.times, cSwan,  color='tab:orange')
ax[1,0].plot(mdl.times, sSwan, color='tab:orange')
ax[1,1].plot(mdl.times, nSwan, color='tab:orange')








from matplotlib.lines import Line2D
legend_elements = [ Line2D([0], [0], color='tab:blue', lw=2, ls='--', label='Simulation Model, $\overline{F} =$ 80 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:blue', lw=2, label='Control Model, $\overline{F} =$ 80 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:orange', lw=2, ls='--', label='Simulation Model, Reference'),
                    Line2D([0], [0], color='tab:orange', lw=2, ls='-', label='Control Model, Reference'),
                  ]

fig.legend(handles=legend_elements,loc='lower center', ncol=2)
fig.subplots_adjust(bottom=0.75)   

fig.tight_layout(rect=[0,0.1,1,1])





plt.show()
