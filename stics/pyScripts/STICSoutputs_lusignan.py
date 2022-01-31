import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sys
sys.path.append('../../utils')
import readValsFromFile as rdvl

import sticsIOutils as sticsIO

import os
cwd = os.getcwd()



####################
# STICS simulation
####################

## stics files
sticsIO.dirStics = cwd+ '/../lusignan9697/'

# usm = "mlu96n0"
# usm = "mlu96n6"
# usm = "mlus96s"
# usm = "mlus96i"
# usm = "mlus97s"
# usm = "mlus97i"

usm = "mlus96reuse"

sti = sticsIO.dirStics + 'mod_s' + usm + '.sti'
tec = sticsIO.dirStics + usm + "_tec.xml"
cli = sticsIO.dirStics + 'lusignaj.1996'

# set initial conditions file
#ref
sticsIO.setIniFile(usm,usm + "_ini.xml")


# # set irragation calendar
# #####ref scenario
# irrigCal = np.array([ [207,30.0], [226,30.0] ])
# sticsIO.writeIrrigCal(tec, irrigCal)

# # set fertilizer calendar
# #####ref scenario
# fertiCal = np.array([ [120,80.0] ])
# sticsIO.writeFertiCal(tec, fertiCal)



# rum simulation
sticsIO.runUSM(usm)

## load data
stiData = sticsIO.loadData(sti)
# soilParam = sticsIO.loadSoilParam()
# Simulation results
simData = sticsIO.loadData(sti)






# indices for simData
# fixed
iyear,imonth,idayofmonth,iday=0,1,2,3

# line number in var.mod + nb of fixed outputs





################
# time
###############

#full range of data
it0,itf= 0, len(simData[:,iday])-1

stages = sticsIO.readStages_corn(sti)

#limit to plant life
tsow = stages['sow']        # Sowing
tger = stages['ger']        # Germination
tlev = stages['lev']        # Emergence
tharv= stages['rec']        # Harvest
# print(tlev,tharv)

iSow = int(tsow-simData[0,iday])
iGer = int(tger-simData[0,iday])
iLev = int(tlev-simData[0,iday])
iHarv = int(tharv-simData[0,iday])


# it0=iSow
# it0=iLev

itf=iHarv+10

t0,tf=simData[it0,iday],simData[itf,iday]

itime=range(it0,itf+1)


# print(simData[itime,iday])

import pandas as pd
dates = pd.date_range( dt.datetime(*[int(i) for i in simData[it0,iyear:iday] ] ), periods=itf-it0+1 )





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
totalBulkDensity = np.sum(bulkDensity*thickness )/totalDepth
# print(totalBulkDensity)

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

climateData = rdvl.readVals(cli)

# index of colums in climate data
jtimeClimate=5-2
jET0=9-2
jrain=10-2

# index for time
it0Climate,itfClimate = int(t0)-1,int(tf)-1

ET0 = sticsIO.readClimate('ET0', cli)
Rain= sticsIO.readClimate('rain', cli)

print('Mean ET0 from Emergence to havest :', np.mean(ET0[int(t0)-1:int(tf)]) )

# if __name__ == "__main__":
#     plt.figure()
#     plt.title('Climate')
#     plt.plot(dates,ET0[int(t0)-1:int(tf)], 'r', label='ET0 [mm/d]')
#     plt.bar(dates,Rain[int(t0)-1:int(tf)], label='Rain [mm/d]')

    
#     plt.legend()



# # Write Rain to file
# np.savetxt(sticsIO.dirStics+"/data/rain_mlus96",Rain[int(t0)-1:int(tf)],fmt='%f')
# np.savetxt(sticsIO.dirStics+"/data/ET0_mlus96",ET0[int(t0)-1:int(tf)],fmt='%f')


##################
# Plant
###################

ilai=sticsIO.varIndex("lai")            # [-]
imasecn=sticsIO.varIndex("masec(n)")       # t/ha
imafrais = sticsIO.varIndex("mafrais")     # t/ha

# if __name__ == "__main__":

    # fig,ax = plt.subplots()
    # ax.set(title='Plant')
    # plt.plot(simData[itime,iday],simData[itime,ilai], label='lai' )
    # plt.plot(simData[itime,iday],simData[itime,imafrais], label='Fresh biomass' )
    # plt.plot(simData[itime,iday],simData[itime,imasecn], 'k', label='Dry biomass' )


    # plt.plot([tger,tger],[0,max(simData[itime,imasecn])],label='germination')
    # plt.plot([tlev,tlev],[0,max(simData[itime,imasecn])],label='levee')
    # # plt.plot([tamf,tamf],[0,max(simData[itime,imasecn])],label='amf')
    # plt.plot([tharv,tharv],[0,max(simData[itime,imasecn])],label='harvest')








####################
# Soil water
###################

#soil water in layers
# [% dry weigth] : HR/100 * bulkDensity[g/cm3] = swc [-]
iHR= np.array( [sticsIO.varIndex("HR("+str(i)+")") for i in range(1,6)] )

# water volume in layers [mm] :  soil water content in layer * height of layer [cm] * mm/cm
volWlayer = simData[:,iHR]/100 * bulkDensity * thickness*10
# total water volume [mm]
totalVol = np.sum(volWlayer ,axis=1)
# total soil water content = total Water volume / (depth of soil[cm] * mm/cm)
totalSWC = totalVol/(totalDepth*10)
# swc levels for total soil : average weighted by layer thickness
totalSfc = np.sum(sfc*thickness)/totalDepth
totalSwp = np.sum(sWp*thickness)/totalDepth
# print(totalSfc,totalSwp)


#water in 'measured' depth
iresmes=sticsIO.varIndex("resmes")        # water volume up to mesurement depth mm
profmes = sticsIO.readProfmes(tec)*10        # mesuremt depth cm*10=mm, defined in *_tec.xml file
# sMes=simData[:,iresmes]/profmes
sMes= sticsIO.swcMes(simData, tec)


wpVolmes = np.sum(sWp[:3]*thickness[:3]*10)+ sWp[3]*(profmes-np.sum(thickness[:3]*10) )
fcVolmes = np.sum(sfc[:3]*thickness[:3]*10)+ sfc[3]*(profmes-np.sum(thickness[:3]*10) )
swpMes=wpVolmes/profmes
sfcMes=fcVolmes/profmes


# water process
iirrig =sticsIO.varIndex("airg(n)")          # irrigation mm/d
idrain =sticsIO.varIndex("drain")          # water drained at base of profile (leakage) mm/d


# water in root zone
iresrac=sticsIO.varIndex("resrac")         # water in root zone [mm]
izrac=sticsIO.varIndex("zrac")           # root depth [cm]
# water stress
itetstomate=sticsIO.varIndex("tetstomate")     # W stress factor
iWstress=sticsIO.varIndex("swfac")        # plant water stress (swfac) [0,1]


sRoot=np.divide(simData[:,iresrac], simData[:,izrac]*10, out = np.zeros_like(simData[:,iresrac]), where=simData[:,izrac]!=0)



# if __name__ == "__main__":

    # plt.figure()
    # plt.title('Total Soil Moisture')
    # plt.plot(simData[itime,iday],totalVol[itime], label='total water volume [mm]' )
    # plt.plot(simData[itime,iday],totalSWC[itime], label = 'total soil water content' )
    # plt.plot([t0,tf],[totalSfc,totalSfc],'--', label='Sfc')
    # plt.plot([t0,tf],[totalSwp,totalSwp],'-.', label='Swp')
    # plt.bar(simData[itime,iday], simData[itime,iirrig], color='k', label='irrig' )
    # plt.bar(simData[itime,iday], simData[itime,idrain], color='b', label='Leakage' )
    # plt.legend()

    # plt.figure()
    # plt.title('Soil Moisture in root zone')
    # plt.plot(simData[itime,iday], simData[itime,itetstomate]+swpMes, '--', label='S*' )
    # plt.plot(simData[itime,iday], sRoot[itime]+swpMes, label='S root')
    # plt.plot(simData[itime,iday], sMes[itime], ':', label='S mes' )
    # plt.plot(simData[itime,iday],simData[itime,iWstress],'k',label='W stress' )
    # # plt.plot([t0,tf],[swpMes,swpMes],'--', label='SwpMes')
    # # plt.plot([t0,tf],[sfcMes,sfcMes],'-.', label='SfcMes')
    # plt.plot([t0,tf],[totalSfc,totalSfc],'--', label='Sfc')
    # plt.plot([t0,tf],[totalSwp,totalSwp],'-.', label='Swp')
    # plt.axis([t0, tf, -0.0 , 1.0])
    # plt.legend()

    # fig,ax=plt.subplots()
    # ax.plot(simData[itime,iday], sMes[itime], label='S mes' )
    # ax2=ax.twinx()
    # ax2.bar(simData[itime,iday], simData[itime,iirrig], label='irrig' )
    # ax.axis([t0, tf, -0.0 , 1.0])
    # lines, labels = ax.get_legend_handles_labels()
    # lines2, labels2 = ax2.get_legend_handles_labels()
    # ax2.legend(lines + lines2, labels + labels2)



################
# Nitrogen
#################


## N in soil layers
iAZnit=np.array( [sticsIO.varIndex("AZnit("+str(i)+")") for i in range(1,6)] )         # NO3 in layers [kg/ha]
# iAZamm = np.array( [sticsIO.varIndex("AZamm("+str(i)+")") for i in range(1,6)] )        # NH4 in layers [kg/ha]

#N process
iQles=sticsIO.varIndex("Qles")                          # Cumulative amount of NO3-N leached at the base of the soil profile [kg/ha]
iFertig=sticsIO.varIndex("anit(n)")                     # daily amount of fertiliser-N added to crop [kg/ha d]
iinns=sticsIO.varIndex("inns")                          # stress factor on biomass growth due to nitrogen deficiency
iNmineraliz = sticsIO.varIndex('Nmineral_from_plt')     # Cumulative N mineralized during the crop cycle (planting-harvest)
iNvol = sticsIO.varIndex('Nvolat_from_plt')             # Cumulative N volatized during the crop cycle (planting-harvest)
iNdenit = sticsIO.varIndex('QNdenit')                   # Cumulative amount of N denitrified during the simulation period

# compute daily N leached/mineralized/... as difference of cumulative amount from a day and previous day
Nleach = np.zeros(simData[:,iday].size)
Nleach[0] = simData[0,iQles]
Ndenit = np.zeros(simData[:,iday].size)
Ndenit[0] = simData[0,iNdenit]
for iNl in range(1,Nleach.size):
    Nleach[iNl]=simData[iNl,iQles]-simData[iNl-1,iQles]
    Ndenit[iNl]=simData[iNl,iNdenit]-simData[iNl-1,iNdenit]

Nmineralized = np.zeros(simData[:,iday].size)
Nmineralized[iSow] = simData[iSow,iNmineraliz]
Nvol = np.zeros(simData[:,iday].size)
Nvol[iSow] = simData[iSow,iNvol]

for iN in range(iSow,iHarv):
    Nmineralized[iN]=simData[iN,iNmineraliz]-simData[iN-1,iNmineraliz]
    Nvol[iN]=simData[iN,iNvol]-simData[iN-1,iNvol]

#total N03 [kg/ha]
# totalNO3=np.sum(simData[:,iAZnit],axis=1)
totalNO3=sticsIO.totalSoilVar("AZnit", simData)
totalNH4=sticsIO.totalSoilVar("AZamm", simData)
totalNorg=sticsIO.readOutput('Nhumt', simData)

Nvoleng = sticsIO.readOutput('Nvoleng', simData)


#effective fertiliser : fertilizer - immobilized - denitrified - volatized
Nfert = sticsIO.readOutput('anit(n)', simData) -sticsIO.readOutput('Norgeng', simData) -Ndenit -Nvoleng


# if __name__ == "__main__":
#     # plt.figure()
#     # plt.title('Nitrogen in layers [kg/ha]')
#     # [plt.plot(simData[itime,iday], simData[itime,iAZnit[i]], label='NO3 [kg/ha] ' + str(i) ) for i in range(5)]
#     # plt.bar(simData[itime,iday],simData[itime,iFertig], label='fertiliser')
#     # plt.legend()
#
#     fig,ax = plt.subplots(2,1,figsize=(7,10))
#     ax[0].set(title='Total Nitrogen [kg/ha]')
#     ax[0].plot(simData[itime,iday], totalNO3[itime], label='total NO$_3$ ' )
#     ax[0].plot(simData[itime,iday], totalNH4[itime], label='total NH$_4$ ' )
#     # ax[0].plot(simData[itime,iday], totalNorg[itime], label='total N org ' )
#     ax[0].bar(simData[itime,iday],simData[itime,iFertig], label='fertiliser')
#     ax[0].bar(simData[itime,iday],Nfert[itime], label='Effective fertiliser')
#     # ax[0].plot(simData[itime,iday], sticsIO.readOutput('QNdenit', simData)[itime], label='cumulative amount of N denitrified during the simulation period' )
#
#
#     # ax[0].plot(simData[itime,iday], sticsIO.readOutput('Nmineral_from_plt', simData)[itime], label='Cumulative N mineralized' )
#     # ax[0].plot(simData[itime,iday], sticsIO.readOutput('Nvolat_from_plt', simData)[itime], label='Cumulative N volati' )
#     ax[0].legend()
#
#     ax[1].set(title='Nitrogen process [kg/ ha d]')
#     ax[1].plot(simData[itime,iday], -Nleach[itime], label='NO$_3$ leached' )
#     ax[1].plot(simData[itime,iday], Nmineralized[itime], label='N mineralized' )
#     ax[1].plot(simData[itime,iday], -sticsIO.readOutput('Norgeng', simData)[itime], label='N immobilized from fertiliser' )
#     ax[1].plot(simData[itime,iday], -Ndenit[itime], label='N denitrified' )
#
#     ax[1].plot(simData[itime,iday], -Nvoleng[itime], label='N fertiliser volati' )
#     # ax[1].plot(simData[itime,iday], Nvol[itime], label='N vol' )
#     ax[1].legend()

    # plt.plot(simData[itime,iday], simData[itime,iinns], label='inns' )

    # plt.plot([tger,tger],[0,120], '--', label='germination')
    # plt.plot([tlev,tlev],[0,120], '--', label='levee')
    # plt.plot([tharv,tharv],[0,120], '--', label='harvest')



# if __name__ == "__main__":
#
#     # idayFerti= np.where(Nfert>0)[0][1]
#     idayFerti = 207-90
#     print('fert = ', simData[idayFerti,iFertig])
#     print('effective ferti = ferti - immobilized - denitrified - volatized = ', Nfert[idayFerti])
#     print('N mineralized = ', Nmineralized[idayFerti])
#     print('NO3 diff at fertilization', totalNO3[idayFerti]-totalNO3[idayFerti-1])
#
#     #for fertilizer type 7, ammonium nitrate
#     # deneng=0.15
#     # voleng=0.15
#     # orgeng=0.46
#
#     #for fertilizer type 7, calcium nitrate
#     # deneng=0.2
#     # voleng=0.0
#     # orgeng=0.25
#
#     #for fertilizer type 8
#     deneng=0.05
#     voleng=0.05
#     orgeng=0.2
#
#     print('denit = ', Ndenit[idayFerti], ' =< ferti * deneng = ', simData[idayFerti,iFertig]*deneng )
#     print('volatized = ', Nvoleng[idayFerti], ' =< ferti * voleng = ', simData[idayFerti,iFertig]*voleng )
#     print('immobilized = ', sticsIO.readOutput('Norgeng', simData)[idayFerti] , ' =< ferti * orgeng = ', simData[idayFerti,iFertig]*orgeng )
#
#     print('effective ferti >= ferti * (1-org-den-vol) = ferti * (1-', deneng+voleng+orgeng, ') = ' , simData[idayFerti,iFertig]*(1-deneng-voleng-orgeng) )









#### Summary plots : Lai - Biomass - SWC - N 



if __name__ == "__main__":

    fig,ax = plt.subplots(1,3,figsize=(15,5))

    ax[0].set(title='Plant')
    # ax[0].plot(dates,1-np.exp(- 0.6*simData[itime,ilai]), label='Canopy Cover' )
    ax[0].plot(dates,simData[itime,ilai], label='Leaf Area Index [m$^2$ leaf / m$^2$ soil]' )
    ax[0].plot(dates,simData[itime,imasecn], label='Dry biomass [T/ha]' )
    ax[0].set_ylim(0,25)


    ax[1].set(title='Water [mm] ')
    # ax[1].plot(dates, sMes[itime]*profmes, label='Soil water volume [mm]' )
    ax[1].plot(dates, volWlayer[itime,0], label='Soil water (layer 1) ' )
    ax[1].plot(dates, volWlayer[itime,1], label='Soil water (layer 2) ' )
    ax[1].plot(dates, volWlayer[itime,2], label='Soil water (layer 3) ' )
    ax[1].bar(dates, simData[itime,iirrig],  label='Irrigation ' )
    ax[1].bar(dates,climateData[it0Climate:itfClimate+1,jrain], color='c', label='Rain ')
    ax[1].set_ylim(0,170)


    ax[2].set(title='Nitrogen [kg/ha] ')
    ax[2].plot(dates, simData[itime,iAZnit[0]], label='Soil NO$_3$ (layer 1)')
    ax[2].plot(dates, simData[itime,iAZnit[1]], label='Soil NO$_3$ (layer 2)')
    ax[2].plot(dates, simData[itime,iAZnit[2]], label='Soil NO$_3$ (layer 3)')
    ax[2].plot(dates, simData[itime,iFertig],  label='Fertilisation')
    ax[2].set_ylim(0,150)


    for a in ax:
        a.plot([dates[iLev-it0],dates[iLev-it0]],[0,a.get_ylim()[1]],'--k')
        a.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,a.get_ylim()[1]],'--k')

        # Define the date format
        import matplotlib.dates as mdates
        # from matplotlib.dates import DateFormatter
        date_form = mdates.DateFormatter("%d-%m")
        a.xaxis.set_major_formatter(date_form)
        a.xaxis.set_major_locator(mdates.MonthLocator(interval=1))


        a.legend()

    ax[0].text(dates[iLev-it0+1], 10, 'Emergence', fontsize=12)
    ax[0].text(dates[iHarv-it0-25], 8, 'Harvest', fontsize=12)



if __name__ == "__main__":
    plt.tight_layout()
    plt.show()
