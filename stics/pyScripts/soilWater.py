import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('/home/ahaddon/bin')
import readValsFromFile as rdvl


dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'

# Simulation results

simData = rdvl.readVals(dirStics + 'mod_smaize_ref_2013.sti',firstLine=1)
# print(simData[0])

# indices for simData
# fixed
iyear,imonth,idayofmonth,iday=0,1,2,3
t0,tf=simData[0,iday],simData[-1,iday]

# line number in var.mod + nb of fixed outputs
ilai=1+3
iHR=np.arange(3,8)+3               # % dry weigth : HR/100 * bulkDensity = swc
iswc=np.arange(8,14)+3             # mm^3 W / mm^3 Soil
iresmes=14+3                       # mm
iWstress=15+3                      # [0,1]
itetstomate=16+3







################
# time
###############

#full range of data
it0,itf= 0, len(simData[:,iday])-1

#limit to plant life
tsow = 112      # Sowing
tger = 119      # Germination
tlev = 128      # Emergence
tamf = 153      # Maximum acceleration of leaf growth
tharv= 247      # Harvest

iSow = int(tsow-simData[0,iday])
iGer = int(tger-simData[0,iday])
iLev = int(tlev-simData[0,iday])
iamf = int(tamf-simData[0,iday])
iHarv = int(tharv-simData[0,iday])

it0,itf=iSow,iHarv

it0=int(140-simData[0,iday])

t0,tf=simData[it0,iday],simData[itf,iday]

itime=range(it0,itf+1)







################
# Soil
################

#parameters
soilParam = rdvl.readVals(dirStics + 'param.sol',firstLine=3)
#colums indices for soil parameters
ithickness=1         # of layer
ifc=2               # soil water content at field capacity (in %)
iwp=3                # soil water content t wilting point (%)
ibulkDensity=4       # g/cm3

# soil properties
thickness=soilParam[:,ithickness]         # cm
totalDepth=np.sum(thickness)
bulkDensity=soilParam[:,ibulkDensity]

# soil relative humidity levels
hccf=soilParam[:,ifc]     # field capacity : % dry weigth
hminf=soilParam[:,iwp]    # wiltingpoint : % dry weigth

# # conversion of relative humidity levels to soil water content levels
sfc=hccf/100 * bulkDensity
sWp=hminf/100 * bulkDensity
# print(sfc,sWp)




#################
# Climate
#################

climateData = rdvl.readVals(dirStics + 'sitej.2013')

# index of colums in climate data
jtimeClimate=5-2
jrain=10-2

# index for time
it0Climate,itfClimate = int(t0)-1,int(tf)-1


# humidity in % dry weight

[plt.plot(simData[it0:itf,iday],simData[it0:itf,iHR[i]], label='HR '+str(i)) for i in range(4)]

[plt.plot([t0,tf],[hccf[i],hccf[i]],'--', label='fc '+str(i)) for i in range(4)]
[plt.plot([t0,tf],[hminf[i],hminf[i]],'-.', label='wp '+str(i)) for i in range(4)]
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))





# Soil water content : HR_vol_z1_z2 [mm^3 W / mm^3 Soil]
# [plt.plot(simData[:,iday],simData[:,iswc[i]], label='S '+str(i)) for i in range(6)]
#
# [plt.plot([t0,tf],[sfc[i],sfc[i]],'--', label='Sfc '+str(i)) for i in range(4)]
# [plt.plot([t0,tf],[sWp[i],sWp[i]],'-.', label='Swp '+str(i)) for i in range(4)]
# plt.legend()



# link HR [%dry weight] <-> HR_vol_z1_z2 [mm^3 W / mm^3 Soil]
# [%dryWeight]/100 * bulkDensity [g/cm^3] * [volSoil cm^3] = [densityWater g/cm^3] * [volWater cm^3]
# [%dryWeight]/100 * bulkDensity [g/cm^3] * [ZSoil cm] = 1 * [ZWater cm]
# HR/100 * bulkDensity = HR_vol_z1_z2 = [ZWater cm]/[ZSoil cm]
# warning : not same layer thickness for HR (thickness) and HR_vol_z1_z2 ...

# [plt.scatter(simData[:,iday], simData[:,iHR[i]]/100 *bulkDensity[i],label=str(i)) for i in range(1)]
# [plt.plot(simData[:,iday], simData[:,iswc[i]], label='swc '+str(i) ) for i in range(1) ]

# [plt.plot(simData[:,iday], simData[:,iswc[i]]*100/simData[:,iHR[i]], label='swc '+str(i) ) for i in range(3) ]
# plt.legend()



# weighted sum of soil water content up to profmes = resmes / profmes
# swc123= np.sum(simData[:,iswc[:3]],axis=1)*3/9
# plt.plot(simData[:,iday],simData[:,iresmes]/900, label='resmes',marker='.' )
# plt.plot(simData[:,iday],swc123, label='swc' )
# plt.legend()


volWlayer = simData[:,iHR]/100 * bulkDensity * thickness*10
# total water volume : sum on layers of ( soil water content in layer * height of layer [mm] )
totalVol = np.sum( volWlayer,axis=1)

# plt.plot(simData[:,iday],totalVol )
# plt.plot(simData[:,iday],climateData[it0Climate:itfClimate+1,jrain])



# total soil water content = total Water volume / depth of soil
totalSWC = totalVol/(totalDepth*10)
# swc levels for total soil : average weighted by layer thickness
totalSfc = np.sum(sfc*thickness)/totalDepth
totalSwp = np.sum(sWp*thickness)/totalDepth

wpVol = np.sum(sWp[:3]*thickness[:3]*10)

# plt.plot(simData[:,iday],totalSWC, 'k', label='swc' )
# plt.plot([t0,tf],[totalSfc,totalSfc],'--k', label='Sfc')
# plt.plot([t0,tf],[totalSwp,totalSwp],'-.k', label='Swp')
# plt.legend()



# water in root zone
itetstomate=16+3
iresrac=17+3        # water in root zone [mm]
izrac=18+3          # root depth [cm]
sRoot=np.divide(simData[:,iresrac], simData[:,izrac]*10, out=np.zeros_like(simData[:,iresrac]), where=simData[:,izrac]!=0)
iWstress=15+3                      # plant water stress [0,1]


# comparing water reserve in root zone and water vol : missing volume corresponding to wilting point
# plt.plot(simData[:,iday],simData[:,iresmes]-simData[:,iresrac],  label='-' )

profmes = 102.58*10        #mesuremt depth cm*10=mm
wpVolmes = np.sum(sWp[:3]*thickness[:3]*10)+ sWp[3]*(profmes-np.sum(thickness[:3]*10) )
fcVolmes = np.sum(sfc[:3]*thickness[:3]*10)+ sfc[3]*(profmes-np.sum(thickness[:3]*10) )

# plt.figure()
# plt.plot(simData[:,iday],simData[:,iresmes], label='water up to mesure depth [mm]' )
# plt.plot(simData[:,iday],simData[:,iresrac]+wpVolmes, '--', label='water reserve in root zone [mm]' )
# plt.plot(simData[:,iday],simData[:,izrac]*10, '--', label='root depth [mm]' )
# plt.legend()



sMes=simData[:,iresmes]/profmes
swpMes=wpVolmes/profmes
sfcMes=fcVolmes/profmes

# plt.figure()
# plt.plot(simData[itime,iday], simData[itime,itetstomate]+swpMes, '--', label='S*' )
# plt.plot(simData[itime,iday], sRoot[itime]+swpMes, label='S root')
# plt.plot(simData[itime,iday], sMes[itime], ':', label='swc up to mesure depth' )
# # plt.plot(simData[:,iday],simData[:,iWstress],'k',label='W stress factor' )
# plt.plot([t0,tf],[swpMes,swpMes],'--', label='SwpMes')
# plt.plot([t0,tf],[sfcMes,sfcMes],'-.', label='SfcMes')
# plt.axis([t0, tf, 0 , 1])
# plt.legend()


plt.show()
