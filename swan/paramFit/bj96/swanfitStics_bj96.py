import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate


from sys import path as syspath
syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
import swanModel as mdl
import plotSwan as pltSwan

syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO

syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit')
import swanFitStics as swanSti




## stics files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/bj/'

usm = "mbj96ir"
# usm = "mbj96se"

sti = stiIO.dirStics + 'mod_s' + usm + '.sti'
tec = stiIO.dirStics + usm + "_tec.xml"
cli = stiIO.dirStics + 'boisjolj.1996'

# rum simulation
stiIO.runUSM(usm)

## load data
stiData = stiIO.loadData(sti)

tSti, Lsti, Ssti, Nsti, Bsti = swanSti.loadSimu(stiData, tec)
Csti = swanSti.laiTocanopy( Lsti )

lsnbStics = np.array((Lsti, Ssti, Nsti, Bsti))
csnbStics = np.array((Csti, Ssti, Nsti, Bsti))



#################
# setup ref case 
################

paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/bj96/params_bj96_fitir'

mdl.readParams(paramFile)

mdl.t0=tSti[0]
mdl.tf=tSti[-1]
mdl.times = tSti
mdl.s0 = Ssti[0]/mdl.phi
mdl.n0 = Nsti[0]

## read data for inputs
swanSti.pelakIrigFromStics(tSti, stiData)
swanSti.pelakFertiFromStics(tSti, stiData)
swanSti.pelakClimatFromSTICS(tSti, cli)
## for base scenario fertilisation without irrigation 
if not usm == "bj96reuse":
        swanSti.FertiSimpleFromStics(tSti, stiData)

# constant ET0
# mdl.ET0 = interpolate.interp1d([mdl.t0, mdl.tf] , [mdl.ET0ref, mdl.ET0ref] ,kind='previous' )


# maxCsti = max(Csti)
# maxET0 = max(mdl.ET0(tSti-tSti[0]))




### params not fitted

### from stics
# mdl.Z = 700

# print('Max Canopy (STICS) :', max(swanSti.laiTocanopy(Lsti)))
# print('Max LAI (STICS) :', max(Lsti))
# mdl.cMax = 0.925

### method bic
# mdl.tsen=90         # 218 - t0Jul
# mdl.gamma = 1e-5
# mdl.exLai=0.7
# mdl.Sh=0.06
# mdl.aN=0.3

# ### unchanged from pelak
# mdl.Kce=1.1





##### SWC levels : guess from stics, can be fitted...
# soilParam = stiIO.loadSoilParam()
# mdl.Sfc =soilParam["totalSfc"]              # 0.2207
# mdl.Sw =soilParam["totalSwp"]               # 0.1035
# mdl.Sstar = (mdl.Sfc +mdl.Sw)/2             # 0.1621

# mdl.printParams(['Sfc','Sstar','Sw','Sh'])





#### ----------- parameters fitted : initial guess

# ## pelak 
# mdl.c0 = 0.008
# mdl.d =7
# mdl.etaC = 0.054
# mdl.Kcb = 1.4
# mdl.rG = 1.5
# mdl.Wstar=33

## corn 2013
# mdl.c0 = 0.008
# mdl.d =7
# mdl.etaC = 0.02706
# mdl.Kcb = 1.4
# mdl.rG = 0.924
# mdl.Wstar=19.12


# mdl.Kcb = 1.1
# mdl.rG = 0.681
# mdl.cMax = 0.93
mdl.ET0ref = 6
mdl.Wstar = 20

#### ----------- parameters fitted : bounds

paramBnds = []

# paramBnds += [['d', 5, 15]]
# paramBnds += [['Sfc', 0.25, 0.3]]
# paramBnds += [['ksat', 5, 1000]]

# paramBnds += [['etaC', 1e-5, 0.04]]

# paramBnds += [['Kcb', 1, 1.4]]

# paramBnds += [['rG', 0.01, 1.5]]
# paramBnds += [['c0', 1e-5, 0.02]]

# paramBnds += [['tsen', 50, 300]]
# paramBnds += [['gamma', 1e-5, 0.01]]

paramBnds += [['Wstar', 1e-5, 100]]
paramBnds += [['ET0ref', 4, 6]]

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



# to have c at 'equilibrium' <1
# mdl.rM = mdl.rG * mdl.etaC *mdl.Kcb * maxET0
# fitPelak(pnameC,(lbndC,ubndC),paramErrorCSN)






####### fit of a single variable
### C
# varIndex=[0]
### S
# varIndex=[1]
### N
# varIndex=[2]
### B
varIndex=[3]


###### general fit
### C,S
# varIndex = [0,1]
### C,S,N
# varIndex = [0,1,2]
### S,N,B
# varIndex = [1,2,3]
### C,S,N,B
# varIndex = [0,1,2,3]



### calibration with least square
swanSti.fitPelak_ls(pname,(lbnd,ubnd),swanSti.relRMSE_pervar,csnbStics[varIndex],varIndex) 




### calibration with RMSE - and constraints
cons = (
        # {'type': 'eq', 'fun': swanSti.consMaxC, 'args':(pname,) },
       )
# check constraint on initial guess
# print( swanSti.consMaxC([],[]) )

# swanSti.fitPelak_min(pname,(lbnd,ubnd),swanSti.relRMSE,csnbStics[varIndex],varIndex,cons) 





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


pltSwan.finalize_2d(ax)


plt.tight_layout()
plt.show()
