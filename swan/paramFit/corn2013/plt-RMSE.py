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



##### setup plot RMSE
fig,ax = plt.subplots(figsize=(8,5))
ax.set(xlabel='Total Fertilization [kg/ha]',ylabel='relRMSE[\%]')







########################################################
### ref N0 = 12.8...
######################################################

FN0 = 80
Imax=10
CNmax=5

# FN =  np.array([1])
FN = np.arange(0,21,2)


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)

# Crmse, Srmse, Nrmse, Brmse = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
Crmse, Srmse, Nrmse, Brmse = np.zeros((3,len(FN))), np.zeros((3,len(FN))), np.zeros((3,len(FN))), np.zeros((3,len(FN)))


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
    fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,80.0], axis=0 )
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
    # RMSE
    Crmse[0,indx], Srmse[0,indx], Nrmse[0,indx], Brmse[0,indx] = swanSti.relRMSE_pervar([], [], np.array((Csti, Ssti, Nsti, Bsti)), [0,1,2,3])

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha



###### plot RMSE
ax.plot(FN0+swanNtot, Crmse[0,:]*100, 'o', color='tab:orange', label='Canopy', ls='')
ax.plot(FN0+swanNtot, Srmse[0,:]*100, 'v', color='tab:orange', label='Soil Water', ls='')
ax.plot(FN0+swanNtot, Nrmse[0,:]*100, 's', color='tab:orange', label='Mineral N', ls='')
ax.plot(FN0+swanNtot, Brmse[0,:]*100, 'D', color='tab:orange', label='Biomass', ls='')







##########################################################
### med N0 =10.022 
##########################################################

FN0=40

# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)

# Crmse1, Srmse1, Nrmse1, Brmse1 = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)


for indx in range(len(FN)):

    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    # med N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni10.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni10.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
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
    # RMSE
    Crmse[1,indx], Srmse[1,indx], Nrmse[1,indx], Brmse[1,indx] = swanSti.relRMSE_pervar([], [], np.array((Csti, Ssti, Nsti, Bsti)), [0,1,2,3])

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha




###### plot RMSE
ax.plot(FN0+swanNtot, Crmse[1,:]*100, 'o', color='tab:blue' , ls='')
ax.plot(FN0+swanNtot, Srmse[1,:]*100, 'v', color='tab:blue' , ls='')
ax.plot(FN0+swanNtot, Nrmse[1,:]*100, 's', color='tab:blue' , ls='')
ax.plot(FN0+swanNtot, Brmse[1,:]*100, 'D', color='tab:blue' , ls='')



















##########################################################
### low N0 =7.22 
##########################################################

FN0 = 0

# FN =  np.array([0,1,2,3,4,5,6,7,8,9,10,11,12])
# FN =  np.array([1])


swanBiof, swanNtot, swanItot, swanLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)
stiBiof, stiNtot, stiItot, stiLeach = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)

# Crmse2, Srmse2, Nrmse2, Brmse2 = np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape), np.zeros(FN.shape)


for indx in range(len(FN)):

    print('FN = ', FN[indx])

    #### Controls from bocop
    dirBCP = cwd+'/../../bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar20-I'+str(Imax)+'-CN'+str(CNmax)+'/'+str(FN[indx])
    # med N0
    irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni7.csv")
    fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni7.csv")
    ### for bocop and MRAP
    ### conversion of fertilization calendar from concentration to mass
    fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
    ### and add first intervention before sowing
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
    # RMSE
    Crmse[2,indx], Srmse[2,indx], Nrmse[2,indx], Brmse[2,indx] = swanSti.relRMSE_pervar([], [], np.array((Csti, Ssti, Nsti, Bsti)), [0,1,2,3])

    swanNtot[indx]= np.trapz(mdl.Irig(mdl.times)*mdl.Cn(mdl.times), x=mdl.times)*10    # kg/ha




###### plot RMSE
ax.plot(FN0+swanNtot, Crmse[2,:]*100, 'o', color='tab:gray' , ls='')
ax.plot(FN0+swanNtot, Srmse[2,:]*100, 'v', color='tab:gray' , ls='')
ax.plot(FN0+swanNtot, Nrmse[2,:]*100, 's', color='tab:gray' , ls='')
ax.plot(FN0+swanNtot, Brmse[2,:]*100, 'D', color='tab:gray' , ls='')








# ########################################################
# ### ref scenario used for fit
# ######################################################



# # #####ref scenario : used for fit
# irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
# fertiCal_corn2013 = np.array([ [120,80.0] ])


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
# # RMSE
# Crmse, Srmse, Nrmse, Brmse = swanSti.relRMSE_pervar([], [], np.array((Csti, Ssti, Nsti, Bsti)), [0,1,2,3])




# ###### plot RMSE
# ax.plot([80], Crmse*100, 'o', color='k' , ls='')
# ax.plot([80], Srmse*100, 'v', color='k' , ls='')
# ax.plot([80], Nrmse*100, 's', color='k' , ls='')
# ax.plot([80], Brmse*100, 'D', color='k' , ls='')





print(np.mean(Crmse), np.mean(Srmse), np.mean(Nrmse), np.mean(Brmse) )


inf70, inf130, sup130 = 0,0,0
Ninf70, Ninf130, Nsup130 = 0,0,0
FN0=[8,4,0]

for i in range(3):
    for j in range(len(FN)):
        if FN0[i]+FN[j]<7:
            inf70+= Brmse[i,j]
            Ninf70+=1
        elif FN0[i]+FN[j]<13:
            inf130+= Brmse[i,j]
            Ninf130+=1
        else:
            sup130+= Brmse[i,j]
            Nsup130+=1



print(inf70/Ninf70, inf130/Ninf130, sup130/Nsup130 )





########## finish plot
from matplotlib.lines import Line2D
legend_elements = [ Line2D([0], [0], marker='o', color='w', label='Canopy',markerfacecolor='r', markersize=7),
                    Line2D([0], [0], marker='v', color='w', label='Soil water',markerfacecolor='r', markersize=7),
                    Line2D([0], [0], marker='s', color='w', label='Mineral N',markerfacecolor='r', markersize=7),
                    Line2D([0], [0], marker='D', color='w', label='Biomass',markerfacecolor='r', markersize=7),
                    Line2D([0], [0], color='tab:orange', lw=2, label='F$_{N0}$=80 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:blue', lw=2, label='F$_{N0}$=40 kg ha$^{-1}$'),
                    Line2D([0], [0], color='tab:gray', lw=2, label='F$_{N0}$=0 kg ha$^{-1}$'),
                    # Line2D([0], [0], marker='o', color='w', label='Reference',markerfacecolor='k', markersize=7),
                  ]

fig.legend(handles=legend_elements,loc='right', ncol=1)

fig.tight_layout(rect=[0,0,0.77,1])










plt.show()
