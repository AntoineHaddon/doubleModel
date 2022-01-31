import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate


from sys import path as syspath
syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
import swanModel as mdl

import plotSwan as pltSwan

syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO

syspath.append('..')
import swanFitStics as swanSti




## stics data files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
sti = stiIO.dirStics + 'mod_smaize_reuse_2013.sti'
tec = stiIO.dirStics + "maize_reuse_tec.xml"
cli = stiIO.dirStics + 'sitej.2013'

## load data
stiData = stiIO.loadData(sti)
soilParam = stiIO.loadSoilParam()

tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData, tec)
Csti = swanSti.laiTocanopy( Lsti )

lsnbStics = np.array((Lsti, Ssti, Nsti, Bsti))
csnbStics = np.array((Csti, Ssti, Nsti, Bsti))









#################
# setup ref case 
################

mdl.t0=tSti[0]
mdl.tf=tSti[-1]
mdl.times = tSti
mdl.s0 = Ssti[0]
mdl.n0 = Nsti[0]

## read data
swanSti.pelakIrigFromStics(tSti, stiData)
swanSti.pelakFertiFromStics(tSti, stiData)
swanSti.pelakClimatFromSTICS(tSti, cli)
#constant ET0
# mdl.ET0ref = 4.09
# mdl.ET0 = interpolate.interp1d([0, mdl.tf] , [mdl.ET0ref, mdl.ET0ref] ,kind='previous' )



maxCsti = max(Csti)
maxET0 = max(mdl.ET0(tSti-tSti[0]))





#################
# initial guess
################

### params not fitted

### from stics
# mdl.Z=1000
# ### method bic
# mdl.tsen=90         # 218 - t0Jul
# mdl.gamma = 1e-5
# mdl.exLai=0.6
# mdl.ksat=0.33*1000
# mdl.Sh=0.14
# ### unchanged from pelak
# mdl.Kce=1.1
# mdl.aN=1

# mdl.cMax = 0.94
# print('Max Canopy (STICS) :', max(swanSti.laiTocanopy(Lsti)))



##### SWC levels : guess from stics, can be fitted...

# with porosity
# mdl.phi =soilParam["totalSfc"]+0.2           # 0.37 +0.2 = 0.57
# mdl.Sw =soilParam["totalSwp"]/mdl.phi        # 0.30
# mdl.Sfc =soilParam["totalSfc"]/mdl.phi       # 0.65
# mdl.Sstar = (mdl.Sfc +mdl.Sw)/2                         # 0.47
# swanSti.printParams(['phi','Sfc','Sw'])

# without porosity -> s is swc relative to volume
# mdl.phi =1.0
# mdl.Sw =soilParam["totalSwp"]               # 0.175
# mdl.Sfc =soilParam["totalSfc"]              # 0.375
# mdl.Sstar = (mdl.Sfc +mdl.Sw)/2             # 0.278
# swanSti.printParams(['phi','Sfc','Sw','Sstar'])

# # mdl.printParams(['phi','Sfc','Sw','Sh'],'mdl.')

####fitted parameters

#### initial guess from litterature -> pelak
# mdl.d = 13
# mdl.etaC = 0.054
# mdl.Kcb = 1.03
# mdl.rG = 0.56
# mdl.rM = 0.2
# mdl.Wstar = 33.7
#
#
# mdl.etaC = 0.03





### swan model, irrig ref, 
paramFile = 'params_swan_Iref_Corn2013'
mdl.readParams(paramFile)

# mdl.etaC = 0.035
# mdl.Kcb = 1.
# mdl.rG = 0.9
# mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * mdl.ET0ref
# swanSti.printParams(['rM'])






#### ----------- parameters fitted : bounds

paramBnds = []

# paramBnds += [['d', 5, 15]]
# paramBnds += [['Sfc', 0.25, 0.3]]
# paramBnds += [['ksat', 5, 1000]]

# paramBnds += [['etaC', 1e-5, 0.035]]
# paramBnds += [['aN', 0.1, 1]]

# paramBnds += [['Kcb', 0.7, 1.2]]

# paramBnds += [['rG', 0.01, 1.5]]
# paramBnds += [['c0', 1e-5, 0.01]]
# paramBnds += [['rM', 0.01, 0.5]]

paramBnds += [['Wstar', 1e-5, 40]]

# paramBnds += [['Sstar', 0.1, 0.3]]
# paramBnds += [['Sw', 0.05, 0.2]]
# paramBnds += [['Sh', 0., 0.1]]

pname, lbnd ,ubnd = np.array(paramBnds).T
lbnd= np.array(lbnd,dtype=float) 
ubnd= np.array(ubnd,dtype=float) 


### small variation 
# for ip in range(len(pname)):
#     lbnd[ip],ubnd[ip] = getattr(mdl,pname[ip])*0.9, getattr(mdl,pname[ip])*1.1
#     print(pname[ip] + ' : ' + str(lbnd[ip]) + ' -- ' + str(ubnd[ip]))





####### fit of a single variable
### C
# varIndex=[0]
### S
# varIndex=[1]
### N
# varIndex=[2]
### B
# varIndex=[3]


###### general fit
### C,S
# varIndex = [0,1]
### C,S,N
# varIndex = [0,1,2]
### S,N,B
# varIndex = [1,2,3]
### C,S,N,B
varIndex = [0,1,2,3]


### calibration with least square
swanSti.fitPelak_ls(pname,(lbnd,ubnd),swanSti.relRMSE_pervar,csnbStics[varIndex],varIndex) 

# swanSti.fitPelak(pname,(lbnd,ubnd),swanSti.paramErrorCSN,lsnbStics)


# mdl.rM =  mdl.rG * mdl.etaC *mdl.Kcb * mdl.ET0ref / maxCsti
# swanSti.printParams(['rM'])
# print('Max C = rG/rM * etaC * KCb * ET0ref = ', mdl.rG/mdl.rM * mdl.etaC * mdl.Kcb * mdl.ET0ref  )


# save parameters
# paramFile = 'corn2013/noPorosity/params_noPoro_Imrap_Corn2013'
# mdl.writeParams(paramFile)


swanSti.printRMSE(csnbStics)





cPelak, sPelak, nPelak, bPelak = mdl.simulate()
# mdl.printSimuInfo(tPelak, cPelak, sPelak, nPelak, bPelak)

fig,ax = pltSwan.varproc_Setup_2x3()
pltSwan.varProc_2x3( ax, tSti, cPelak, sPelak, nPelak, bPelak )
pltSwan.var_2x3( ax, tSti, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='+', lbl=' stics')

# add stics Process / stresses
ax[1,0].plot(tSti, stiIO.readOutput("swfac", stiData,tJul=tSti),'--+', color='tab:blue', label='W stress Stics' )
ax[1,0].plot(tSti, stiIO.readOutput("inns", stiData,tJul=tSti),'--+', color='tab:orange', label='N stress Stics' )
ax[1,1].plot(tSti, stiIO.readOutput("drain", stiData,tJul=tSti), '--+', color='k', label=r'L Stics')
NleachStics=stiIO.Nleach(stiData,tJul=tSti) / 10        # kg/ha / 10 = g/m2
ax[1,2].plot(tSti, NleachStics, '--+', color='k', label=r'NO$_3$ leaching Stics')


# C upper equilibrium
# maxC = mdl.rG/mdl.rM * mdl.Kcb * mdl.ET0ref * mdl.NstressV(sPelak,nPelak)*mdl.etaC * mdl.KsV(sPelak)
# ax[0,0].plot(tSti, maxC, 'k')

pltSwan.finalize_2d(ax)


plt.tight_layout()
plt.show()







# mdl.IC=[mdl.c0, Ssti[0]/mdl.phi, Nsti[0], 0]
# tPelak, cPelak, sPelak, nPelak, bPelak = mdl.simPelakDense(mdl.IC,mdl.tf, tout=np.arange(mdl.tf+1), tol=1e-6 )
# # mdl.printSimuInfo(tPelak, cPelak, sPelak, nPelak, bPelak)

# fig,ax = pltSwan.varproc_Setup_2x3()
# pltSwan.varProc_2x3( ax, tPelak, cPelak, sPelak, nPelak, bPelak )
# pltSwan.var_2x3( ax, tPelak, swanSti.laiTocanopy(Lsti), Ssti/mdl.phi, Nsti, Bsti, sty='+', lbl=' stics')

# # add stics Process / stresses
# ax[1,0].plot(tPelak, stiIO.readOutput("swfac", stiData,tJul=tSti),'--+', color='tab:blue', label='W stress Stics' )
# ax[1,0].plot(tPelak, stiIO.readOutput("inns", stiData,tJul=tSti),'--+', color='tab:orange', label='N stress Stics' )
# ax[1,1].plot(tPelak, -stiIO.readOutput("drain", stiData,tJul=tSti), '--+', color='k', label=r'L Stics')
# NleachStics=stiIO.Nleach(stiData,tJul=tSti) / 10        # kg/ha / 10 = g/m2
# ax[1,2].plot(tPelak, -NleachStics, '--+', color='k', label=r'NO$_3$ leaching Stics')


# # C upper equilibrium
# # maxC = mdl.rG/mdl.rM * mdl.Kcb * mdl.ET0(tPelak) * mdl.NstressV(sPelak,nPelak)*mdl.etaC * mdl.KsV(sPelak)
# # ax[0,0].plot(tPelak, maxC, 'k')

# pltSwan.finalize_2d(ax)


# plt.tight_layout()
# plt.show()
