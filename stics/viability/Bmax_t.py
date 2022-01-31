import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
# import scipy.optimize as opt
# import math as m

from sys import path as syspath

syspath.append('/home/ahaddon/Dropbox/Work/ReUse/code/stics/pyScripts')
import sticsIOutils as stiIO



## stics files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/viability/corn2013/'
sti_file = stiIO.dirStics + 'mod_smaize_ref_2013.sti'
tec_file = stiIO.dirStics + "maize_ref_tec.xml"
cli_file = stiIO.dirStics + 'sitej.2013'		
usm = "maize_ref_2013"

# set initial conditons file
# stiIO.setIniFile(usm,"maize_ini.xml")

irrigCal_corn2013 = np.array([ [112,20],[180,40], [192,40], [203,40], [210,40], [223,40], [232,40], [242,40] ])
stiIO.writeIrrigCal(tec_file, irrigCal_corn2013)




Sw = 0.17475
Sstar= 0.2446
etaC=  0.02706
z = 1000


lnsty=['-',':','--','-.',(0, (3, 5, 1, 5, 1, 5))]
clr=['k','b','r','g','y']



### prepare plot
fig,ax = plt.subplots(1,3,figsize=(15,5))
Smax,Nmax = 0.5, 100
ax[1].axis([0, Smax, 0, Nmax])
ax[1].plot([Sw,Sw],[0,Nmax], ':', label='Sw')
ax[1].plot([Sstar,Sstar],[0,Nmax], '--', label='S*')
ax[1].plot([0,Smax],[0,etaC*Smax*z], '--', label='N/zS=etac')

ax[2].set_ylim(0,Smax)
ax[2].plot([120,240],[Sw,Sw], ':', label='Sw')
ax[2].plot([120,240],[Sstar,Sstar], '--', label='S*')



n0=1000
stiIO.setN0("maize_ini.xml",[n0/4,n0/4,n0/4,n0/4,0])

# rum simulation
stiIO.runUSM(usm)

	## load data
stiData = stiIO.loadData(sti_file)

tiniStics = int(stiData[0,3])
stages = stiIO.readStages_corn(stiData)
t0Jul = stages['lev']      # initial time as date ~ 'julian day'
tfJul = stages['rec']     # final time as date
tJul = np.arange(int(t0Jul),int(tfJul))
itimeStics = np.array(tJul-tiniStics, dtype=int)

s = stiIO.swcMes(stiData, tec_file)[itimeStics]                          # [mm/mm]
n = stiIO.totalSoilVar("AZnit", stiData)[itimeStics] /10                # kg/ha / 10 = g/m2
b = stiIO.readOutput("masec(n)",stiData)[itimeStics] *100    # T/ha *1000 /10 = kg/ha /10= g/m2
print(b[-1])
ax[0].plot(tJul, b/1000)
ax[1].plot(s,n)
ax[2].plot(tJul,s)


# fig,ax = plt.subplots(1,3,figsize=(15,5))
# ax[0].plot(tJul, b/1000, label=r"Biomass", lw=3)
# ax[1].plot(tJul, s, label=r'$S$', lw=3)
# ax[2].plot(tJul, n, label=r'$N$', lw=3)



### ssave to file
with open('Bmax_t.npy', 'wb') as f:
    np.save(f, np.array([tJul,b]))



plt.tight_layout()
plt.show()
