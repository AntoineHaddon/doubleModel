import numpy as np
import matplotlib.pyplot as plt
# import scipy.interpolate as interpolate

import sys
sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/model')
import swanModel as mdl
# import plotPelak as pltPlk

sys.path.append('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb')
import pelakReuseBocopHJB as reusebocopHJB


plt.rc('text', usetex=True)
plt.rcParams.update({'font.size': 16})
plt.rcParams.update({'lines.linewidth' : 2.0})

fig,ax = plt.subplots(2,3,figsize=(15, 10))
lnsty=['-',':','--','-.',(0, (3, 5, 1, 5, 1, 5))]
clr=['k','b','r','g','y']

fig2,ax2 = plt.subplots(1,3,figsize=(15,5))
mkrsty=['.','o','v','^','<','>']




### mlus
dir='/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/maxTotFertig/'
### parameters  irrig ref, 
# paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fiti'
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/mlus96/params_mlus96_fitIbcp'
mdl.readParams(paramFile)
reusebocopHJB.rainBocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/data/rain_mlus96')
reusebocopHJB.ET0Bocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_mlus/data/ET0_mlus96')
    
# vals =  np.array([5,10])
# vals =  np.array([1,2,3,4,5,6,7,8,9,10])
vals =  np.array([3,7,12,14])








plkBiof = np.zeros(vals.shape)
plkNtot= np.zeros(vals.shape)
plkItot= np.zeros(vals.shape)
plkLeach= np.zeros(vals.shape)



for indx,val in enumerate(vals):

    timeBocop, Ctbocop, Stbocop, Ntbocop, Itbocop, CNtbocop = reusebocopHJB.readBocopResults(dir+str(val))
    val*=10

    mdl.t0= timeBocop[0]
    mdl.tf=timeBocop[-1]
    mdl.times = timeBocop

    mdl.c0=Ctbocop[0]
    mdl.s0=Stbocop[0]
    mdl.n0=Ntbocop[0]
    mdl.b0=0

    Can, SoilM, Nitro, Biom = reusebocopHJB.simPelakBocop(timeBocop,Itbocop, CNtbocop)
    mdl.printSimuInfo(mdl.times, Can, SoilM, Nitro, Biom)

    irigt=mdl.Irig(mdl.times)
    Ndoset=mdl.Cn(mdl.times)
    leacht=mdl.LeachV(SoilM,Nitro)

    # totalIrrig = np.trapz(Itbocop, x=timeBocop)
    # totalNfert = np.trapz(Itbocop*CNtbocop, x=timeBocop)
    totalIrrig = np.trapz(irigt, x=mdl.times)
    totalNfert = np.trapz(irigt*Ndoset, x=mdl.times)
    totalLeach = np.trapz(leacht, x=mdl.times)


    ax[0,0].plot(mdl.times, Can, label=str(val),linestyle=lnsty[indx % 5],color=clr[indx % 5],linewidth=3)
    ax[0,0].plot(mdl.times, Biom/1000,linestyle=lnsty[indx % 5],color=clr[indx % 5])
    ax[0,1].plot(mdl.times, SoilM,linestyle=lnsty[indx % 5],color=clr[indx % 5])
    ax[0,2].plot(mdl.times, Nitro, linestyle=lnsty[indx % 5],color=clr[indx % 5])

    ax[1,0].plot(mdl.times,mdl.Irig(mdl.times)*mdl.Cn(mdl.times), label=str(val), linestyle=lnsty[indx % 5], color=clr[indx % 5])
    ax[1,1].plot(mdl.times,mdl.Irig(mdl.times), label=r'$\int IC_N <$ '+str(val), linestyle=lnsty[indx % 5], color=clr[indx % 5])
    ax[1,2].plot(mdl.times,mdl.Cn(mdl.times),linestyle=lnsty[indx % 5] ,color=clr[indx % 5])


    # max bio constraint Total Fertig
    # ax2[0].plot(totalNfert*10, Biom[-1]*10,  marker=mkrsty[indx % 6], color='b', linestyle='',label=r'$\int IC_N <$ '+ str(val))
    # ax2[1].plot(totalIrrig, Biom[-1]*10, marker=mkrsty[indx % 6], color='b',linestyle='',label=r'$\int IC_N <$ '+str(val))
    # ax2[2].plot(totalLeach*10, Biom[-1]*10,  marker=mkrsty[indx % 6], color='b', linestyle='',label=r'$\int IC_N <$ '+str(val))
    plkBiof[indx]= Biom[-1]/100      # T/ha
    plkNtot[indx]= totalNfert*10    # kg/ha
    plkItot[indx]= totalIrrig       # mm
    plkLeach[indx]= totalLeach*10   # kg/ha





Tf=timeBocop[-1]
ax[0,0].set(title="Canopy and Biomass [kg/m$^2$]",xlabel="Time[d]")
# ax[0,0].legend()
# ax[0,0].grid()
ax[0,0].axis([0, Tf, 0 , 2])

ax[0,1].plot([0, Tf], mdl.Sstar*np.ones((2,1)), '-.',label=r'$S_*$' )
ax[0,1].set(title="Soil Moisture",xlabel="Time[d]")
ax[0,1].legend()
# ax[0,1].grid()
ax[0,1].axis([0, Tf, 0 , 1])

ax[0,2].set(title=r"Nitrogen [g/m$^2$]",xlabel="Time[d]")
Ncrit=mdl.etaC*mdl.Sstar*mdl.Z*mdl.phi/mdl.aN
ax[0,2].plot([0,mdl.times[-1]], [Ncrit,Ncrit], 'b', label=r'$N_c(S_*)$')
ax[0,2].legend()
ax[0,2].axis([0, Tf, 0 , 20])
# ax[0,2].grid()


ax[1,0].set(title=r"Fertigation [g/m$^2$d]",xlabel="Time[d]")
ax[1,0].axis([0, Tf, 0 , 0.5])
# ax[1,0].legend()
# ax[1,0].grid()

ax[1,1].set(title="Irrigation [mm/d]",xlabel="Time[d]")
# ax[1,1].legend(loc='lower center',bbox_to_anchor=(0.5, -.35), ncol=4)
ax[1,1].legend()
ax[1,1].axis([0, Tf, 0 , 10])
# ax[1,1].grid()


ax[1,2].set(title="Nitrogen Irrigation [g/L]",xlabel="Time[d]")
# ax[1,2].grid()
# ax[1,2].legend()


# ax2[0].set(title='Final Biomass [kg/m$^2$]',xlabel='Total IC$_N$ [kg/m$^2$]')
# ax2[1].set(title='Total Irrigation [m]',xlabel='Total IC$_N$ [kg/m$^2$]')
# ax2[2].set(title='Total IC$_N$ [kg/m$^2$] (constraint)',xlabel='Total IC$_N$ [kg/m$^2$]')
# ax2[2].plot([vals[0],vals[-1]],[vals[0],vals[-1]],'k')

ax2[0].set(xlabel='Total Fertilization [kg/ha]',ylabel='Final Biomass [T/ha]')
ax2[1].set(xlabel='Total Irrigation [mm]',ylabel='Final Biomass [T/ha]')
ax2[2].set(xlabel='Total Leaching [kg/ha]',ylabel='Final Biomass [T/ha]')



# plkBiof[-1]= 22.95
# plkNtot[-1]= 0.0
# plkItot[-1]= 377
# plkLeach[-1]= 12.37


ax2[0].plot(plkNtot, plkBiof,  marker='o', color='b', linestyle='')
ax2[1].plot(plkItot, plkBiof,  marker='o', color='b',label='Control Model', linestyle='')
ax2[2].plot(plkLeach, plkBiof,  marker='o', color='b', linestyle='')


### corn2013
# stiBiof = np.array([13.18, 17.47, 19.18, 19.84, 19.99, 20.7, 21.09, 21, 20.56, 21.58,  21.68, 21.56, 21.67 ])     # T/ha
# stiLeach = np.array([4   ,  4   ,  4   ,  4   ,  4   ,  4  , 4    ,  4,   5  ,  5   ,  6    ,  5   , 6  ])     # kgN/ha
### mlus
# vals =  np.array([2,4,6,8])
# stiBiof = np.array([ 24.05, 24.07, 24.24, 24.06])     # T/ha
# stiLeach = np.array([ 0.002, 0.002, 0.043, 0.002])     # kgN/ha
vals =  np.array([3,7,12,14])
stiBiof = np.array([ 16.5, 19.23, 21.95, 22.65])     # T/ha
stiLeach = np.array([ 0.002, 2.49, 5.5, 5.5])     # kgN/ha

ax2[0].plot(plkNtot, stiBiof,  marker='+', color='g', linestyle='')
ax2[1].plot(plkItot, stiBiof,  marker='+', color='g',label='STICS', linestyle='')
ax2[2].plot(stiLeach, stiBiof,  marker='+', color='g', linestyle='')



# ax2[0].legend()
ax2[1].legend(loc='lower center',bbox_to_anchor=(0.5, -.35), ncol=2)
# ax2[1].legend()

# ax2[2].legend()


fig.tight_layout()
fig2.tight_layout()

plt.show()
