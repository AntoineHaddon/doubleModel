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
fig,ax = plt.subplots(2,2,figsize=(10,10))
ax=np.ravel(ax)


ax[0].set(xlabel='Simulation model',ylabel='Control Model',title='Canopy Cover')
ax[0].axis([0,1,0,1])
ax[0].plot([0,1],[0,1],'k',lw=1)

ax[1].set(xlabel='Simulation model',ylabel='Control Model',title='Biomass')
ax[1].axis([0,22,0,22])
ax[1].plot([0,22],[0,22],'k',lw=1)

ax[2].set(xlabel='Simulation model',ylabel='Control Model',title='Soil water')
ax[2].axis([0.2,.45,0.2,0.45])
ax[2].plot([0.2,.45],[0.2,0.45],'k',lw=1)

ax[3].set(xlabel='Simulation model',ylabel='Control Model',title='Soil N')
ax[3].axis([0,17,0,17])
ax[3].plot([0,17],[0,17],'k',lw=1)


clr=['b','r','g','tab:blue','y','tab:pink','tab:brown','tab:purple','xkcd:puke','xkcd:navy blue','tab:orange','c','tab:olive']







########################################################
### ref N0 = 12.8...
######################################################

FN0 = 80

# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])
# FN = np.arange(8,15,2)
FN = np.arange(0,21,2)



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

    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times) + FN0/10


    #### plot
    # cl=clr[int(FN[indx]+FN0/10)%13]
    # cl ='k'
    cl = clr[int(totalNfert/7)]
    ax[0].scatter(Csti,cSwan, color = cl, alpha=0.5)
    ax[1].scatter(Bsti/100,bSwan/100, color = cl, alpha=0.5)
    ax[2].scatter(Ssti,sSwan, color = cl, alpha=0.5)
    ax[3].scatter(Nsti,nSwan, color = cl, alpha=0.5)














##########################################################
### med N0 =10.022 
##########################################################

FN0 = 40



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

    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times) + FN0/10

    #### plot
    # cl=clr[int(FN[indx]+FN0/10)%13]
    # cl ='k'
    cl = clr[min( int(totalNfert/7),2)]
    ax[0].scatter(Csti,cSwan, color = cl, alpha=0.5)
    ax[1].scatter(Bsti/100,bSwan/100, color = cl, alpha=0.5)
    ax[2].scatter(Ssti,sSwan, color = cl, alpha=0.5)
    ax[3].scatter(Nsti,nSwan, color = cl, alpha=0.5)









##########################################################
### low N0 =7.22 
##########################################################

FN0 = 0



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

    totalNfert = np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times) + FN0/10


    #### plot
    # cl=clr[int(FN[indx]+FN0/10)%13]
    cl ='k'
    cl = clr[int(totalNfert/7)]
    ax[0].scatter(Csti,cSwan, color = cl, alpha=0.5)
    ax[1].scatter(Bsti/100,bSwan/100, color = cl, alpha=0.5)
    ax[2].scatter(Ssti,sSwan, color = cl, alpha=0.5)
    ax[3].scatter(Nsti,nSwan, color = cl, alpha=0.5)












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











######### finish pareto front plot
from matplotlib.lines import Line2D
legend_elements = [ Line2D([0], [0], color='b', marker='o', ls='', label='$F_{N0} + \overline{F} \leq $ 60 kg ha$^{-1} $'), 
                    Line2D([0], [0], color='r', marker='o', ls='', label= '60 kg ha$^{-1} < F_{N0} + \overline{F} \leq $ 120 kg ha$^{-1}$'),
                    Line2D([0], [0], color='g', marker='o', ls='', label= '120 kg ha$^{-1}$ $< F_{N0} + \overline{F}$')   ]

fig.legend(handles=legend_elements,loc='lower center', ncol=1)
# fig.subplots_adjust(bottom=0.15)   
fig.tight_layout(rect=[0,0.1,1,1])


# fig.legend(handles=legend_elements,loc='upper left', bbox_to_anchor=(0.65, 0.35))
# fig.tight_layout()








# fig.tight_layout()





plt.show()
