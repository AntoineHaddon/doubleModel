import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate
# import scipy.optimize as opt
# import math as m

from sys import path as syspath
syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
# import pelakModel as mdl
import swanModel as mdl

import plotSwan as pltSwan
syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit')
import swanFitStics as swanSti


syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO


import readValsFromFile as rdvl


########################################
# Irrigation  and fertilizer Calendar
########################################
## ferti :
## for STICS values in kg/ha = 0.1 g/m^2 and divide by irrigation to get kg/ha mm = 0.1 g/L
## from concentration in g/L = g/(m^2 mm), multiply by irrig in mm to get g/m^2
## to pass to STICS, convert to kg/ha (*10) and divide by fertilizer effeciency (0.7 for fertilizer type 8)
### ferti stics = irrig [mm] * Cn [g/L] * 10 /0.7


# #####ref scenario : used for fit
irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
fertiCal_corn2013 = np.array([ [120,80.0] ])


##### ref scenario with  fertigation
# irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
# fertiCal_corn2013 = np.array([ [120,80.0], [207,13.0], [226,13.0] ])


###### auto calculated by stics, no ferti
# irrigCal_corn2013 = np.array([ [112,20], [196,40], [205,40], [212,40], [225,40], [234,40], [244,40] ])
# fertiCal_corn2013 = np.array([ [120,80.0]] )


###### auto calculated by stics, with cst ferti to have a fixed total N
# irrigCal_corn2013 = np.array([ [196,40], [205,40], [212,40], [225,40], [234,40], [244,40] ])
# nbIrrig = irrigCal_corn2013.shape[0]
# Ntot = 67.1
# Ncst = Ntot / (0.7 * nbIrrig)		# Ntot [kg/ha] / fertieff (0.7) / # irrig events
# fertiCal_corn2013 = np.array([ [120,80.0] ,[196,Ncst], [205,Ncst], [212,Ncst], [225,Ncst], [234,Ncst], [244,Ncst]])


##### I2, no ferti
# irrigCal_corn2013 = np.array([ range(190,230) , 40*[5.0]]).T
# fertiCal_corn2013 = np.array([ [120,80.0] ])

###### I3, no ferti
# irrigCal_corn2013 = np.array([ range(180,230,4) , 13*[5.0]]).T
# fertiCal_corn2013 = np.array([ [120,80.0] ])



####### from MRAP feedback through file
# # irrigCal_corn2013 = rdvl.readVals("../irrigData/corn2013-Imrap.csv")
# irrigCal_corn2013 = rdvl.readVals("../irrigData/corn2013-CritMRAP-I.csv")
# fertiCal_corn2013 = rdvl.readVals("../irrigData/corn2013-CritMRAP-Cn.csv")



#### from bocop
FN=8
# dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/pelak/bocophjb/maxBio_TotFerConstr_rain/maxTotFertig/'+str(FN)+'/'
dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/maxFNbar12/'+str(FN)+'/'
# ref N0
irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni12.csv")
fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni12.csv")
# low N0
# irrigCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-I-Ni9.csv")
# fertiCal_corn2013 = rdvl.readVals(dirBCP+"/corn2013-bcp-Cn-Ni9.csv")


### for bocop and MRAP
### conversion of fertilization calendar from concentration to mass
### and add first intervention before sowing
fertiCal_corn2013[:,1] = fertiCal_corn2013[:,1]*irrigCal_corn2013[:,1] *10/0.7
fertiCal_corn2013 = np.insert(fertiCal_corn2013, 0, [120,80.0], axis=0 )
irrigCal_corn2013 = irrigCal_corn2013[irrigCal_corn2013 [:,1]>0]
fertiCal_corn2013 = fertiCal_corn2013[fertiCal_corn2013 [:,1]>0]



# print(fertiCal_corn2013)



####################
# STICS simulation
####################

## stics files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
sti_corn2013 = stiIO.dirStics + 'mod_smaize_reuse_2013.sti'
tec_corn2013 = stiIO.dirStics + "maize_reuse_tec.xml"
cli_corn2013 = stiIO.dirStics + 'sitej.2013'		
# cli_corn2013 = stiIO.dirStics + 'meteo-site2-1994.2013'
usm_corn2013 = "maize_reuse_2013"

# set initial conditons file
#ref
stiIO.setIniFile(usm_corn2013,"maize_ini.xml")
# high NO3
# stiIO.setIniFile(usm_corn2013,"maize_fullNO3_ini.xml")
# low NO3
# stiIO.setIniFile(usm_corn2013,"maize_lowN0_ini.xml")


# set irragation calendar
stiIO.writeIrrigCal(tec_corn2013, irrigCal_corn2013)
# set fertilizer calendar
stiIO.writeFertiCal(tec_corn2013, fertiCal_corn2013)

# rum simulation
stiIO.runUSM(usm_corn2013)

## load data
stiData_corn2013 = stiIO.loadData(sti_corn2013)
# soilParam = stiIO.loadSoilParam()

tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData_corn2013, tec_corn2013)
Csti = swanSti.laiTocanopy(Lsti)

# print('Max Canopy (STICS) :', max(Csti) )
# print('Max LAI (STICS) :', max(Lsti))
print('Final Biomass (STICS) : ', Bsti[-1], 'g/m^2 =', Bsti[-1]/100, 'T/ha')
print('N leached (STICS) : ', np.sum(stiIO.Nleach(stiData_corn2013,tJul=tSti)), 'kg/ha' )


###########################
## Pelak model simulation
#############################

### swan model, irrig ref, 
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/params_swan_Iref_Corn2013'
mdl.readParams(paramFile)



mdl.t0=tSti[0]
mdl.tf=tSti[-1]
mdl.times = tSti
# print(mdl.tf,mdl.t0)

mdl.s0 = Ssti[0]
mdl.n0 = Nsti[0]
print(mdl.IC())

# set climate (ET0 and rain)
swanSti.pelakClimatFromSTICS(tSti, cli_corn2013)
#constant ET0
# mdl.ET0ref = 3.81	# grignon 1994
# mdl.ET0 = interpolate.interp1d([mdl.t0, mdl.tf] , [mdl.ET0ref, mdl.ET0ref] ,kind='previous' )


## set irragation
swanSti.pelakIrigFromStics(tSti, stiData_corn2013)
## set fertigation
swanSti.pelakFertiFromStics(tSti, stiData_corn2013)

swanSti.printRMSE(np.array((Csti, Ssti, Nsti, Bsti)))

# rmseFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/rmseCorn2013'
# swanSti.saveRMSE(np.array((Csti, Ssti, Nsti, Bsti)), rmseFile, 0 )



## run simulation 
cPelak, sPelak, nPelak, bPelak =  mdl.simulate()



mdl.printSimuInfo(tSti, cPelak, sPelak, nPelak, bPelak)





#####################
## plot 2x3
######################

fig,ax = pltSwan.varproc_Setup_2x3()
pltSwan.varProc_2x3( ax, tSti, cPelak, sPelak, nPelak, bPelak )
pltSwan.var_2x3( ax, tSti, Csti, Ssti/mdl.phi, Nsti, Bsti, sty='+', lbl=' STICS')


# pltSwan.climate(ax[1,1], tSti)
# ax[1,1].plot(tSti, mdl.Irig(tSti), color='tab:blue', label=r"Irrigation", linewidth=2.0)


# add stics Process / stresses
ax[1,0].plot(tSti, stiIO.readOutput("swfac", stiData_corn2013,tJul=tSti),'--+', color='tab:blue', label='W stress STICS' )
ax[1,0].plot(tSti, stiIO.readOutput("inns", stiData_corn2013,tJul=tSti),'--+', color='tab:orange', label='N stress STICS' )
ax[1,1].plot(tSti, stiIO.readOutput("drain", stiData_corn2013,tJul=tSti), '--+', color='k', label=r'Leaching STICS')
NleachStics=stiIO.Nleach(stiData_corn2013,tJul=tSti) / 10        # kg/ha / 10 = g/m2
ax[1,2].plot(tSti, NleachStics, '--+', color='k', label=r'Leaching STICS')
Nuptake = stiIO.readOutput("abso(n)", stiData_corn2013,tJul=tSti)/10  	 # kg/ha / 10 = g/m2
ax[1,2].plot(tSti, Nuptake, '--+', color='tab:orange', label=r'N Uptake STICS')


pltSwan.finalize_2d(ax)


# plt.figure()
# plt.plot(tSti, mdl.Cn(tSti)*1000)
# plt.title("N concentration [mg/L]")


# with open("rain.data", 'w') as f :
#     for r in mdl.Rain(tSti):
#         f.write(str(r) +'\n' )

plt.tight_layout()

# plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/fig/fit-paraIref-Iref.pdf')
# plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/fig/fit-paraIref-IbcpFn'+str(FN)+'.pdf')


plt.show()





#####################
## plot 3x2
######################

# fig,ax = pltSwan.plotSti3x2Setup()
# pltSwan.plotSti3x2( ax, tSti, cPelak, sPelak, nPelak, bPelak ,lw=2)
# pltSwan.plotSti3x2( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='+')

# # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/firstFit_PelakSTICS_ref-3x2.pdf')

# plt.show()



# #####################
# ## plot Vert 5x1 avec stress
# ######################

# fig,ax = pltSwan.plotStiVertSetup()
# pltSwan.plotStiVert( ax, tSti, cPelak, sPelak, nPelak, bPelak ,lw=2)
# pltSwan.plotStiVert( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)

# ax[0].legend(['Control Model', 'STICS'],frameon=False,fontsize=16)


# ## stress
# ax[4].plot(tSti, mdl.KsV(sPelak), color='tab:blue', linewidth=2)
# ax[4].plot(tSti, mdl.NstressV(sPelak, nPelak), color='tab:orange', linewidth=2)
# ax[4].plot(tSti, stiIO.readOutput("swfac", stiData_corn2013,tJul=tSti), '--', color='tab:blue', linewidth=2)
# ax[4].plot(tSti, stiIO.readOutput("inns", stiData_corn2013,tJul=tSti), '--', color='tab:orange', linewidth=2)
# ax[4].legend(['Water stress', 'N stress'],frameon=False,fontsize=16)



# plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_refwithferti_-5x1.pdf')


#####################
## plot 4x1
# ######################

# fig,ax = pltSwan.plotSti4x1Setup()
# pltSwan.plotSti4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak,lw=2)
# pltSwan.plotSti4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)

# pltSwan.pltCtrl4x1(ax,tSti)

# ax[0].legend(['Control Model', 'Simulation Model'],frameon=False,fontsize=14)

# # # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_optCtrl-4x1.pdf')
# # # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_fitRef.pdf')




# plt.tight_layout()
# plt.show()


#################
## process
#################


# figProc,axProc = pltSwan.plotStiVertSetup_proc()
# pltSwan.plotStiVert_proc( axProc, tSti, cPelak, sPelak, nPelak, bPelak, sty='b',lw=2)

# # irrigCal_corn2013 = np.array([ [206,0.0],[207,30.0], [208,0.0], [225,0.0], [226,30.0], [227,0.0] ])
# # axProc[1].plot(irrigCal_corn2013[:,0],irrigCal_corn2013[:,1], color='tab:green', linewidth=2)
# # axProc[2].plot(irrigCal_corn2013[:,0],irrigCal_corn2013[:,1], color='tab:green',  linewidth=2)

# # axProc[1].legend(['Proposed control', 'Reference control'], fontsize=16, frameon=False)

# # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_inputs_totN12.pdf')


# plt.show()





###################################
## plot with 2 consecutive runs
####################################


###### run 1 : define figs but dont show
# fig,ax = pltSwan.plotSti4x1Setup()
# pltSwan.plotSti4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak, sty='b' ,lw=2)
# pltSwan.plotSti4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='b--', lw=2)

# figProc,axProc = pltSwan.plotStiVertSetup_proc()
# pltSwan.plotStiVert_proc( axProc, tSti, cPelak, sPelak, nPelak, bPelak, sty='b',lw=2)



###### run 2 : dont def figs but put legends and show
# pltSwan.plotSti4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak, sty='g' ,lw=2)
# pltSwan.plotSti4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)
# ax[0].legend(['Control model, Proposed control', 'STICS, Proposed control', 'Control Model, Reference control', 'STICS, Reference control'], fontsize=14, frameon=False)


# pltSwan.plotStiVert_proc( axProc, tSti, cPelak, sPelak, nPelak, bPelak, sty='g',lw=2)
# axProc[1].legend(['Proposed control', 'Reference control'], fontsize=16, frameon=False)

# plt.show()




###################
# controls
###################


# run 1
# fig,ax = plt.subplots(2,1)

# ax[0].set(title="Irrigation [mm/d]")
# ax[1].set(title="N concentration [mg/L]")

# ax[0].plot(tSti,mdl.ET0(tSti), color='b', label='ET$_0$')

# ax[0].plot(tSti, mdl.Irig(tSti), color='tab:blue', linewidth=2.0)
# ax[1].plot(tSti, mdl.Cn(tSti)*1000, color='tab:blue', label=r"Total N = 70 kg/ha", linewidth=2.0)



# run 2
# ax[0].plot(tSti, mdl.Irig(tSti), color='tab:orange', linewidth=2.0)
# ax[1].plot(tSti, mdl.Cn(tSti)*1000, color='tab:orange', label=r"Total N = 120 kg/ha", linewidth=2.0)

# ax[0].legend()
# ax[1].legend(loc='lower center',bbox_to_anchor=(0.5, -.6), ncol=1)

# plt.tight_layout()
# plt.show()
