import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
# import scipy.optimize as opt
# import math as m

from sys import path as syspath

syspath.append('../pyScripts')
import sticsIOutils as stiIO

import os
cwd = os.getcwd()


# load ref max biomass
with open('Bmax_t.npy', 'rb') as f:
    tmax, bmax = np.load(f)




## stics files
stiIO.dirStics = cwd+'/corn2013/'
sti_file = stiIO.dirStics + 'mod_smaize_ref_2013.sti'
tec_file = stiIO.dirStics + "maize_ref_tec.xml"
cli_file = stiIO.dirStics + 'sitej.2013'		
usm = "maize_ref_2013"

# set initial conditons file
# stiIO.setIniFile(usm,"maize_ini.xml")









Sw = 0.17475
Sstar= 0.2446
etaC=  0.02706
z = 1000


lnsty=['-',':','--','-.',(0, (3, 5, 1, 5, 1, 5))]
clr=['k','b','r','g','y']



### preparee plot
fig,ax = plt.subplots(1,3,figsize=(15,5))

ax[0].plot(tmax, bmax/1000, lw=3)

Smax,Nmax = 0.5, 20
ax[1].axis([0, Smax, 0, Nmax])
ax[1].plot([Sw,Sw],[0,Nmax], ':', label='Sw')
ax[1].plot([Sstar,Sstar],[0,Nmax], '--', label='S*')
ax[1].plot([0,Smax],[0,etaC*Smax*z], '--', label='N/zS=etac')

ax[2].set_ylim(0,Smax)
ax[2].plot([120,240],[Sw,Sw], ':', label='Sw')
ax[2].plot([120,240],[Sstar,Sstar], '--', label='S*')




for in0, n0 in enumerate(range(0,200,20)): 
	for iI, I in enumerate(range(0,50,10)) :

		stiIO.setN0("maize_ini.xml",[n0/4,n0/4,n0/4,n0/4,0])
		irrigCal_corn2013 = np.array([ [112,20],[180,I], [192,I], [203,I], [210,I], [223,I], [232,I], [242,I] ])
		stiIO.writeIrrigCal(tec_file, irrigCal_corn2013)

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

		# ax[0].plot(tJul, b/1000, linestyle=lnsty[(in0+iI) % 5], color=clr[(in0+iI) % 5])
		# ax[1].plot(s,n, linestyle=lnsty[(in0+iI) % 5], color=clr[(in0+iI) % 5])
		# ax[2].plot(tJul,s, ls=lnsty[(in0+iI)%5], color=clr[(in0+iI)%5])

		if b[-1]>bmax[-1]*0.9 :
			cl = 'k'
		else :
			cl = 'r'

		ax[0].plot(tJul, b/1000, cl)
		ax[1].plot(s,n, cl)
		ax[2].plot(tJul,s, cl)


# fig,ax = plt.subplots(1,3,figsize=(15,5))
# ax[0].plot(tJul, b/1000, label=r"Biomass", lw=3)
# ax[1].plot(tJul, s, label=r'$S$', lw=3)
# ax[2].plot(tJul, n, label=r'$N$', lw=3)


plt.tight_layout()
plt.show()
