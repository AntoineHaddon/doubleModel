import numpy as np
import matplotlib.pyplot as plt
import sys
sy.spath.append('../../utils')
import readValsFromFile as rdvl

import sticsIOutils as sticsIO

import os
cwd = os.getcwd()

sticsIO.dirStics = cwd+'../corn/'
sti_corn2013 = sticsIO.dirStics + 'mod_smaize_reuse_2013.sti'


# Simulation results
simData = sticsIO.loadData(sti_corn2013)

# indices for simData
# fixed
iyear,imonth,idayofmonth,iday=0,1,2,3
t0,tf=simData[0,iday],simData[-1,iday]

# line number in var.mod + nb of fixed outputs








################
# Soil
################

#parameters
soilParam = rdvl.readVals(sticsIO.dirStics + 'param.sol',firstLine=3)
#colums indices for soil parameters
ithickness=1         # of layer
ifc=2               # soil water content at field capacity (in %)
iwp=3                # soil water content t wilting point (%)
ibulkDensity=4       # g/cm3

# soil properties
thickness=soilParam[:,ithickness]         # cm
totalDepth=np.sum(thickness)
bulkDensity=soilParam[:,ibulkDensity]



#################
# Climate
#################

climateData = rdvl.readVals(sticsIO.dirStics + 'sitej.2013')

# index of colums in climate data
jtimeClimate=5-2
jrain=10-2

# index for time
it0Climate,itfClimate = int(t0)-1,int(tf)-1


#################
# Soil Water
#################

iHR= np.array( [sticsIO.varIndex("HR("+str(i)+")") for i in range(1,6)] )             # [% dry weigth] : HR/100 * bulkDensity[g/cm3] = swc [-]


# water volume in layers [mm] :  soil water content in layer * height of layer [cm] * mm/cm
volWlayer = simData[:,iHR]/100 * bulkDensity * thickness*10
totalVol = np.sum(volWlayer ,axis=1)







# NH4 and NO3 in layers [kg/ha]
iAZnit=np.array( [sticsIO.varIndex("AZnit("+str(i)+")") for i in range(1,6)] )         # NO3 in layers [kg/ha]
iAZamm = np.array( [sticsIO.varIndex("AZamm("+str(i)+")") for i in range(1,6)] )        # NH4 in layers [kg/ha]


# [plt.plot(simData[:,iday],simData[:,iAZamm[i]], '--', label='NH4 '+str(i)) for i in range(5)]
# [plt.plot(simData[:,iday],simData[:,iAZnit[i]], label='NO3 [kg/ha] ' + str(i) ) for i in range(1)]

# [plt.plot(simData[:,iday],simData[:,init_z1_z2[i]], label='NO3 z1_z2 ' + str(i) )for i in range(1)]


NO3gm2 = simData[:,iAZnit]*0.1         # [kg/ha] * [g/kg * ha/m2] = [g/m2]
# [plt.plot(simData[:,iday],NO3gm2[:,i] , label='AZnit [g/m2] - # ' + str(i) ) for i in range(2)]




#total N03
totalNO3=np.sum(simData[:,iAZnit],axis=1)         # [kg/ha]
# plt.plot(simData[:,iday], totalNO3/max(totalNO3), label='NO3 Aznit [kg/ha]' )
# plt.legend()




Nsoilconcentration = totalNO3 * 0.1 / totalVol        # [kg/ha] * [g/kg * ha/m2] / [mm] = [g/m2 mm] = [g/L]
# plt.plot(simData[:,iday],Nsoilconcentration/max(Nsoilconcentration), label='total N concentration')




# # NO3 concentration from stics ...
# iAZnitcon=np.arange(34,39)+3      # NO3 concentration in layers [mg/L]
# NO3fromCon = simData[:,iAZnitcon] /1000 * volWlayer        # [mg/mm m2] * [g/mg] * [mm] = [g/m2]
# totalNO3fromConc = np.sum(NO3fromCon,axis=1)*10         # [g/m2] * [kg/g * m2/ha] = kg/ha
# [plt.plot(simData[:,iday],NO3fromCon[:,i], '--' , label='concNO3 * volWater [g/m2] - ' + str(i)) for i in range(2)]
# plt.plot(simData[:,iday], totalNO3fromConc, label='totalNO3fromConc [kg/ha]')
# plt.plot(simData[:,iday], totalNO3/totalNO3fromConc, label='No3 diff [kg/ha]')




iNhumt = sticsIO.varIndex("Nhumt")       # amount of N in humus soil organic matter (active + inert fractions) [kg/ha]
# plt.plot(simData[:,iday], simData[:,iNhumt]*0.1 , label='N humus [g/m2]')







## N stress
inn=sticsIO.varIndex("inn")
innlai=sticsIO.varIndex("lai")
inns=sticsIO.varIndex("inns")


# plt.figure()
# plt.plot(simData[:,iday], simData[:,inn], label='inn' )
# plt.plot(simData[:,iday], simData[:,innlai], label='innlai' )
# plt.plot(simData[:,iday], simData[:,inns], label='inns' )
# plt.legend()



## N in plante
iCNplante=sticsIO.varIndex("CNplante")                # N concentration in the aboveground plant - % dry weight
idemande = sticsIO.varIndex("demande")                 # daily N requirement of the plant to maximise crop growth [kg/ha/d]

# plt.plot(simData[:,iday], simData[:,iCNplante]/simData[:,inn] )
# plt.plot(simData[:,iday], simData[:,idemande], label='N demand [kg/ha/d]' )

ibiomassDry=sticsIO.varIndex("masec(n)")
biom = simData[:,ibiomassDry]
# plt.plot(simData[:,iday],simData[:,ibiomassDry], 'k', label='Dry biomass' )


Ncrit = simData[:,iCNplante]/simData[:,inn]


# plt.plot(simData[:,ibiomassDry], Ncrit, label='crit N')
# plt.plot(simData[:,ibiomassDry], simData[:,iCNplante], label='N plant' )
# plt.legend()


plt.figure()
# plt.plot(simData[:,iday], Ncrit/max(Ncrit), label='crit N')
# plt.plot(simData[:,iday], simData[:,iCNplante]/max(simData[:,iCNplante]), 'k', label='N plant' )
plt.plot(simData[:,iday], Ncrit*biom/100, label='crit N')
plt.plot(simData[:,iday], simData[:,iCNplante]*biom/100, 'k', label='N plant' )



# dSow=112
# dGer=119
# dHarvest=247
# plt.plot([dSow, dSow], [0, 1])
# plt.plot([dGer,dGer],[0,1])
# plt.plot([dHarvest, dHarvest], [0, 1])


plt.legend()
plt.show()
