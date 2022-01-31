import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate
# import scipy.optimize as opt
# import math as m

from sys import path as syspath
syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
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



#### from bocop
FN=10
dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/maxTotFertig/'+str(FN)
dirBCP = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/maxTotFertig_highN0/'+str(FN)
irrigCal = rdvl.readVals(dirBCP+"/mlus96-bcp-I.csv")
fertiCal = rdvl.readVals(dirBCP+"/mlus96-bcp-Cn.csv")

# #### for bocop and MRAP
# #### conversion of fertilization calendar from concentration to mass
fertiCal[:,1] = fertiCal[:,1]*irrigCal[:,1] *10/0.7

irrigCal = irrigCal[irrigCal [:,1]>0]
fertiCal = fertiCal[fertiCal [:,1]>0]



# # #### and add first intervention before sowing
# # fertiCal = np.insert(fertiCal, 0, [113,220.0], axis=0 )
# fertiCal = np.insert(fertiCal, 0, [113,60.0], axis=0 )








####################
# STICS simulation
####################

## stics files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/lusignan9697/'

#### reference usms
# usm = "mlu96n0"
# usm = "mlu96n6"
# usm = "mlus96s"
# usm = "mlus96i"
# usm = "mlus97i"
# usm = "mlus97s"


#### usm for opt control
usm = "mlus96reuse"

sti = stiIO.dirStics + 'mod_s' + usm + '.sti'
tec = stiIO.dirStics + usm + "_tec.xml"
cli = stiIO.dirStics + 'lusignaj.1996'
# cli = stiIO.dirStics + 'lusignaj.1997'

# set initial conditons file
#ref
# stiIO.setIniFile(usm,usm + "_ini.xml")
stiIO.setIniFile(usm,"mlu96n6_ini.xml")

if usm == "mlus96reuse":
	# set irragation + fertilizer calendar
	stiIO.writeIrrigCal(tec, irrigCal)
	stiIO.writeFertiCal(tec, fertiCal)

# rum simulation
stiIO.runUSM(usm)

## load data
stiData = stiIO.loadData(sti)
# soilParam = stiIO.loadSoilParam()

tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData, tec)
Csti = swanSti.laiTocanopy( Lsti )
csnbStics = np.array((Csti, Ssti, Nsti, Bsti))



print('Final Biomass (STICS) : ', Bsti[-1], 'g/m^2 =', Bsti[-1]/100, 'T/ha')
print('N leached (STICS) : ', np.sum(stiIO.Nleach(stiData,tJul=tSti)), 'kg/ha' )


###########################
## Pelak model simulation
#############################

### parameters
# paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fiti'
# paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fitn0'
# paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fitn6'
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fitIbcp'
mdl.readParams(paramFile)



mdl.t0=tSti[0]
mdl.tf=tSti[-1]
mdl.times = tSti
print(mdl.tf,mdl.t0)

mdl.s0 = Ssti[0]
mdl.n0 = Nsti[0]
print(mdl.IC())

# set climate (ET0 and rain)
swanSti.pelakClimatFromSTICS(tSti, cli)
#constant ET0
# mdl.ET0ref = 3.15	# lus 96
# mdl.ET0ref = 2.66	# lus 97
# mdl.ET0 = interpolate.interp1d([mdl.t0, mdl.tf] , [mdl.ET0ref, mdl.ET0ref] ,kind='previous' )


## set irragation
swanSti.pelakIrigFromStics(tSti, stiData)
## set fertigation
swanSti.pelakFertiFromStics(tSti, stiData)


## run simulation with open loop
cPelak, sPelak, nPelak, bPelak = mdl.simulate()

### run simulation with feedback
# import pelakReuseFeedback as fdb
# tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakFeedback(mdl.IC,mdl.tf, lambda t,y : (fdb.Imrap(t,y,10,mdl.Sstar),0), tout=tSti-tSti[0], tol=1e-4 )


mdl.printSimuInfo(tSti, cPelak, sPelak, nPelak, bPelak)

swanSti.printRMSE(csnbStics)



#####################
## plot 2x3
######################

fig,ax = pltSwan.varproc_Setup_2x3()
pltSwan.varProc_2x3( ax, tSti, cPelak, sPelak, nPelak, bPelak )
pltSwan.var_2x3( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='+', lbl=' stics')


# pltSwan.climate(ax[1,1], tSti)
# ax[1,1].plot(tSti, mdl.Irig(tSti), color='tab:blue', label=r"Irrigation", linewidth=2.0)


# add stics Process / stresses
ax[1,0].plot(tSti, stiIO.readOutput("swfac", stiData,tJul=tSti),'--+', color='tab:blue', label='W stress Stics' )
ax[1,0].plot(tSti, stiIO.readOutput("inns", stiData,tJul=tSti),'--+', color='tab:orange', label='N stress Stics' )
ax[1,1].plot(tSti, stiIO.readOutput("drain", stiData,tJul=tSti), '--+', color='k', label=r'L Stics')
NleachStics=stiIO.Nleach(stiData,tJul=tSti) / 10        # kg/ha / 10 = g/m2
ax[1,2].plot(tSti, NleachStics, '--+', color='k', label=r'NO$_3$ leaching Stics')


pltSwan.finalize_2d(ax)


# plt.figure()
# plt.plot(tSti, mdl.Cn(tSti)*1000)
# plt.title("N concentration [mg/L]")


# with open("rain.data", 'w') as f :
#     for r in mdl.Rain(tSti):
#         f.write(str(r) +'\n' )



plt.tight_layout()
plt.show()





#####################
## plot 3x2
######################

# fig,ax = pltSwan.plotPelak3x2Setup()
# pltSwan.plotPelak3x2( ax, tSti, cPelak, sPelak, nPelak, bPelak ,lw=2)
# pltSwan.plotPelak3x2( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='+')

# plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/firstFit_PelakSTICS_ref-3x2.pdf')



# #####################
# ## plot Vert 5x1 avec stress
# ######################

# fig,ax = pltSwan.plotPelakVertSetup()
# pltSwan.plotPelakVert( ax, tSti, cPelak, sPelak, nPelak, bPelak ,lw=2)
# pltSwan.plotPelakVert( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)

# ax[0].legend(['Control Model', 'STICS'],frameon=False,fontsize=16)


# ## stress
# ax[4].plot(tSti, mdl.KsV(sPelak), color='tab:blue', linewidth=2)
# ax[4].plot(tSti, mdl.NstressV(sPelak, nPelak), color='tab:orange', linewidth=2)
# ax[4].plot(tSti, stiIO.readOutput("swfac", stiData,tJul=tSti), '--', color='tab:blue', linewidth=2)
# ax[4].plot(tSti, stiIO.readOutput("inns", stiData,tJul=tSti), '--', color='tab:orange', linewidth=2)
# ax[4].legend(['Water stress', 'N stress'],frameon=False,fontsize=16)



# plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_refwithferti_-5x1.pdf')


#####################
## plot 4x1
######################

# fig,ax = pltSwan.plotPelak4x1Setup()
# pltSwan.plotPelak4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak,lw=2)
# pltSwan.plotPelak4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)

# ax[0].legend(['Control Model', 'STICS'],frameon=False,fontsize=16)

# # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_optCtrl-4x1.pdf')
# # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_fitRef.pdf')




# plt.tight_layout()
# plt.show()


#################
## process
#################


# figProc,axProc = pltSwan.plotPelakVertSetup_proc()
# pltSwan.plotPelakVert_proc( axProc, tPelak, cPelak, sPelak, nPelak, bPelak, sty='b',lw=2)

# # irrigCal = np.array([ [206,0.0],[207,30.0], [208,0.0], [225,0.0], [226,30.0], [227,0.0] ])
# # axProc[1].plot(irrigCal[:,0],irrigCal[:,1], color='tab:green', linewidth=2)
# # axProc[2].plot(irrigCal[:,0],irrigCal[:,1], color='tab:green',  linewidth=2)

# # axProc[1].legend(['Proposed control', 'Reference control'], fontsize=16, frameon=False)

# # plt.savefig('/home/ahaddon/Dropbox/Work/ReUse/articles/CDC2021/img/PelakSTICS_inputs_totN12.pdf')


# plt.show()





###################################
## plot with 2 consecutive runs
####################################


###### run 1 : define figs but dont show
# fig,ax = pltSwan.plotPelak4x1Setup()
# pltSwan.plotPelak4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak, sty='b' ,lw=2)
# pltSwan.plotPelak4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='b--', lw=2)

# figProc,axProc = pltSwan.plotPelakVertSetup_proc()
# pltSwan.plotPelakVert_proc( axProc, tSti, cPelak, sPelak, nPelak, bPelak, sty='b',lw=2)



###### run 2 : dont def figs but put legends and show
# pltSwan.plotPelak4x1( ax, tSti, cPelak, sPelak, nPelak, bPelak, sty='g' ,lw=2)
# pltSwan.plotPelak4x1( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='g--', lw=2)
# ax[0].legend(['Control model, Proposed control', 'STICS, Proposed control', 'Control Model, Reference control', 'STICS, Reference control'], fontsize=14, frameon=False)


# pltSwan.plotPelakVert_proc( axProc, tSti, cPelak, sPelak, nPelak, bPelak, sty='g',lw=2)
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
