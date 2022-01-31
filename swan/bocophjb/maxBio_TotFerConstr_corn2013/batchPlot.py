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




### corn2013
dir='/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/maxTotFertig/'
### parameters  irrig ref, 
paramFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/params_swan_Iref_Corn2013'
mdl.readParams(paramFile)
reusebocopHJB.rainBocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/rain_corn2013')
reusebocopHJB.ET0Bocop('/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/ET0_corn2013')
    
# vals =  np.array([5,10,15])
# vals =  np.array([1,2,3,4,5,6,7,8,9,10])
vals =  np.array([2,3,4,5,6,7,8,9,10,11,12,0])








plkBiof = np.zeros(vals.shape)
plkNtot= np.zeros(vals.shape)
plkItot= np.zeros(vals.shape)
plkLeach= np.zeros(vals.shape)



for indx,val in enumerate(vals[:-1]):

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



plkBiof[-1]= 12.72
plkNtot[-1]= 0.0
plkItot[-1]= 60
plkLeach[-1]= 6.40



### corn2013
vals =  np.array([2,3,4,5,6,7,8,9,10,11,12,0])

# N0 high
vals  =   np.array([2,    3,     4,     5,     6,     7,     8,     9,     10,    11,    12,    0 ])
stiBiof = np.array([19.5, 19.79, 20.49, 20.71, 21.05, 21.25, 21.44, 21.46, 21.46, 21.46, 21.46, 13.1])     # T/ha
stiLeach = np.array([2.1, 2.1,   2.28,  2.59,  3.49,  3.49,  3.49,  3.49,  3.49,  3.49,  3.5,   2.1])     # kgN/ha
# N0 9
vals  =   np.array([2,     3,     4,     5,     6,     7,     8,     9,     10,    11,    12,    0 ])
stiBiof = np.array([17.91, 18.67, 19.37, 19.57, 21.05, 21.25, 21.44, 21.46, 21.46, 21.46, 21.46, 13.1])     # T/ha
stiLeach = np.array([0.77, 0.91,  1.04,  1.43,  3.49,  3.49,  3.49,  3.49,  3.49,  3.49,  3.5,   2.1])     # kgN/ha

### mlus
# vals =  np.array([2,4,6,8])
# stiBiof = np.array([ 24.05, 24.07, 24.24, 24.06])     # T/ha
# stiLeach = np.array([ 0.002, 0.002, 0.043, 0.002])     # kgN/ha

clr=['k','b','r','g','tab:blue','y','tab:pink','tab:brown','tab:purple','xkcd:puke','xkcd:navy blue','k']


# for i in range(12):
#     ax2[0].plot(plkNtot[i], stiBiof[i],  marker='+', color=clr[i], linestyle='')
#     ax2[0].plot(plkNtot[i], plkBiof[i],  marker='o', color=clr[i], linestyle='')
    
#     ax2[1].plot(plkItot[i], stiBiof[i],  marker='+', color=clr[i], linestyle='')
#     ax2[1].plot(plkItot[i], plkBiof[i],  marker='o', color=clr[i], linestyle='')
    
#     ax2[2].plot(stiLeach[i], stiBiof[i],  marker='+', color=clr[i], linestyle='')
#     ax2[2].plot(plkLeach[i], plkBiof[i],  marker='o', color=clr[i], linestyle='')



ax2[0].plot(plkNtot, stiBiof,  marker='+', color='tab:orange', linestyle='')
ax2[0].plot(plkNtot, plkBiof,  marker='o', color='tab:blue', linestyle='')
    
# ax2[1].plot(plkItot, stiBiof,  marker='+', color=, linestyle='')
# ax2[1].plot(plkItot, plkBiof,  marker='o', color=, linestyle='')

# ax2[2].plot(stiLeach, stiBiof,  marker='+', color=, linestyle='')
# ax2[2].plot(plkLeach, plkBiof,  marker='o', color=, linestyle='')



# ax2[0].legend()
ax2[1].legend(['Simulation model', 'Control Model'],loc='lower center',bbox_to_anchor=(0.5, -.35), ncol=2)
# ax2[1].legend()

# ax2[2].legend()


fig.tight_layout()
fig2.tight_layout()


fig3,ax3 = plt.subplots()

ax3.plot(plkNtot, stiBiof,  marker='+', color='tab:orange', linestyle='')
ax3.plot(plkNtot, plkBiof,  marker='o', color='tab:blue', linestyle='')
ax3.set(xlabel='Total Fertilization [kg/ha]',ylabel='Final Biomass [T/ha]')
ax3.legend(['Simulation model', 'Control Model'],loc='lower center',bbox_to_anchor=(0.5, -.35), ncol=2)

fig3.tight_layout()


plt.show()
