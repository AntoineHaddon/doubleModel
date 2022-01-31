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
sticsIO.dirStics = cwd+'/../lettuceMurviel/'
tec_lettuce = sticsIO.dirStics + "salade_tec.xml"

# usm_lettuce = "lettuce_ref"
# cli_lettuce = sticsIO.dirStics + 'climsalj.2000'
# sti_lettuce = sticsIO.dirStics + 'mod_slettuce_ref.sti'

usm_lettuce = "lettuce_2013"
cli_lettuce = sticsIO.dirStics + 'sitej.2013'
sti_lettuce = sticsIO.dirStics + 'mod_slettuce_2013.sti'

# sti_lettuce = sticsIO.dirStics + 'mod_smaize_ferti_2013.sti'
# tec_lettuce = sticsIO.dirStics + "maize_ferti_tec.xml"
# usm_lettuce = "maize_ferti_2013"

# set initial conditons file
#ref
sticsIO.setIniFile(usm_lettuce,"salade_ini.xml")
# high NO3
# sticsIO.setIniFile(usm_lettuce,"maize_fullNO3_ini.xml")


# set irragation calendar
#####ref scenario
# irrigCal_lettuce = np.array([ [207,30.0], [226,30.0] ])

# sticsIO.writeIrrigCal(tec_lettuce, irrigCal_lettuce)

# set fertilizer calendar
#####ref scenario
# fertiCal_lettuce = np.array([ [120,80.0] ])

# sticsIO.writeFertiCal(tec_lettuce, fertiCal_lettuce)



# rum simulation
sticsIO.runUSM(usm_lettuce)

## load data
stiData_lettuce = sticsIO.loadData(sti_lettuce)
# soilParam = sticsIO.loadSoilParam()






# indices for stiData_lettuce
# fixed
iyear,imonth,idayofmonth,iday=0,1,2,3

# line number in var.mod + nb of fixed outputs





################
# time
###############


stages = sticsIO.readStages(sti_lettuce,plant='lettuce')

#limit to plant life
tsow = stages['sow']        # Sowing
tger = stages['ger']        # Germination
tlev = stages['lev']        # Emergence
tharv= stages['rec']        # Harvest

iSow = int(tsow-stiData_lettuce[0,iday])
iGer = int(tger-stiData_lettuce[0,iday])
iLev = int(tlev-stiData_lettuce[0,iday])
iHarv = int(tharv-stiData_lettuce[0,iday])


#full range of data
it0,itf= 0, len(stiData_lettuce[:,iday])-1

# from planting to harvest
# it0, itf =iSow, iHarv

t0,tf=stiData_lettuce[it0,iday],stiData_lettuce[itf,iday]

itime=range(it0,itf+1)


# print(stiData_lettuce[itime,iday])

import pandas as pd
dates = pd.date_range( dt.datetime(*[int(i) for i in stiData_lettuce[it0,iyear:iday] ] ), periods=itf-it0+1 )




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

# index for Weather time
it0cli,itfcli = int(t0)-1,int(tf)

ET0= sticsIO.readClimate('ET0', cli_lettuce)[it0cli:itfcli]
rain= sticsIO.readClimate('rain', cli_lettuce)[it0cli:itfcli]
tempMin = sticsIO.readClimate('tempMin', cli_lettuce)[it0cli:itfcli]
tempMax = sticsIO.readClimate('tempMax', cli_lettuce)[it0cli:itfcli]



# if __name__ == "__main__":
#     plt.figure(figsize=(12,5))
#     plt.title('Weather')
#     plt.plot(dates, ET0, 'g', label='ET0 [mm/d]')
#     plt.plot(dates, tempMin, 'b', label='T min')
#     plt.plot(dates, tempMax, 'r', label='T max')
#     plt.bar(dates, rain, label='Rain [mm/d]')
#     plt.legend()
#     plt.tight_layout()




##################
# Plant
###################

tauxcouv=sticsIO.readOutput('tauxcouv', stiData_lettuce)           # [-]
masecn=sticsIO.readOutput("masec(n)", stiData_lettuce)       # t/ha
mafrais = sticsIO.readOutput("mafrais", stiData_lettuce)     # t/ha


if __name__ == "__main__":

    fig,ax = plt.subplots(figsize=(12,5))
    ax.set(title='Plant')
    ax.plot(dates,tauxcouv, label='Canopy Cover [m$^2$/m$^2$]' )
    ax.plot(dates,masecn, label='Dry biomass [t/ha] = 100 [g/m$^2$]' )
    # ax.plot(dates,mafrais, 'k',label='Fresh biomass [t/ha] = 100 [g/m$^2$]' )


    # ax.plot(dates,sticsIO.readOutput('dltams(n)', stiData_lettuce), label='plant growth rate [t/ha d]')
    # ax.plot(dates,sticsIO.readOutput('ulai(n)', stiData_lettuce), label='relative development unit for LAI')


    ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
    ax.plot([dates[iLev-it0],dates[iLev-it0]],[0,ax.get_ylim()[1]],'--b',label='emergence')
    ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')

    ax.legend()
    plt.tight_layout()

    # plt.figure(figsize=(12,5))
    # plt.title('code bbch')
    # plt.plot(dates, sticsIO.readOutput('codebbch_output', stiData_lettuce) )






####################
# Soil water
###################

#soil water in layers
# [% dry weigth] : HR/100 * bulkDensity[g/cm3] = swc [-]
iHR= np.array( [sticsIO.varIndex("HR("+str(i)+")") for i in range(1,6)] )

# water content volume basis in layers [-] :  HR/100 * bulkDensity
swclayer = stiData_lettuce[:,iHR]/100 * bulkDensity
# water volume in layers [mm] :  soil water content in layer * height of layer [cm] * mm/cm
volWlayer = stiData_lettuce[:,iHR]/100 * bulkDensity * thickness*10
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
profmes = sticsIO.readProfmes(tec_lettuce)*10        # mesuremt depth cm*10=mm, defined in *_tec.xml file
# sMes=stiData_lettuce[:,iresmes]/profmes
sMes= sticsIO.swcMes(stiData_lettuce, tec_lettuce)


wpVolmes = np.sum(sWp[:3]*thickness[:3]*10)+ sWp[3]*(profmes-np.sum(thickness[:3]*10) )
fcVolmes = np.sum(sfc[:3]*thickness[:3]*10)+ sfc[3]*(profmes-np.sum(thickness[:3]*10) )
swpMes=wpVolmes/profmes
sfcMes=fcVolmes/profmes


# water process
irrig = sticsIO.readOutput('airg(n)', stiData_lettuce)          # irrigation mm/d
idrain =sticsIO.varIndex("drain")          # water drained at base of profile (leakage) mm/d


# water in root zone
iresrac=sticsIO.varIndex("resrac")         # water in root zone [mm]
izrac=sticsIO.varIndex("zrac")           # root depth [cm]
# water stress
itetstomate=sticsIO.varIndex("tetstomate")     # W stress factor
iWstress=sticsIO.varIndex("swfac")        # plant water stress (swfac) [0,1]
Wstress = sticsIO.readOutput('swfac', stiData_lettuce)


sRoot=np.divide(stiData_lettuce[:,iresrac], stiData_lettuce[:,izrac]*10, out = np.zeros_like(stiData_lettuce[:,iresrac]), where=stiData_lettuce[:,izrac]!=0)



if __name__ == "__main__":

    # fig,ax = plt.subplots(figsize=(12,5))
    # ax.set(title='Water volume in layers')
    # ax.plot(dates, volWlayer[itime,0], label='Soil water volume [mm] (depth 0-'+str(thickness[0])+'cm) ' )
    # ax.plot(dates, volWlayer[itime,1], label='Soil water volume [mm] (depth '+str(thickness[0])+'-'+str(thickness[0]+thickness[1])+'cm) ' )
    # ax.plot(dates, volWlayer[itime,2], label='Soil water volume [mm] (depth '+str(thickness[0]+thickness[1])+'-'+str(thickness[0]+thickness[1]+thickness[2])+'cm) ' )
    #
    # ax.bar(dates, irrig,  label='Irrigation [mm]' )
    # ax.bar(dates, rain, color='c', label='Rain [mm] ')
    #
    # ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
    # ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')
    # ax.legend()
    # plt.tight_layout()


    fig,ax = plt.subplots(figsize=(12,5))
    ax.set(title='Water content in layers')
    ax.plot(dates, swclayer[itime,0], label='Soil water content [mm/mm] (depth 0-'+str(thickness[0])+'cm) ' )
    ax.plot(dates, swclayer[itime,1], label='Soil water content [mm/mm] (depth '+str(thickness[0])+'-'+str(thickness[0]+thickness[1])+'cm) ' )
    ax.plot(dates, swclayer[itime,2], label='Soil water content [mm/mm] (depth '+str(thickness[0]+thickness[1])+'-'+str(thickness[0]+thickness[1]+thickness[2])+'cm) ' )

    ax.plot(dates[[0,-1]],[sWp[0],sWp[0]], '--k', label='wilting point layer 1')
    ax.plot(dates[[0,-1]],[sfc[0],sfc[0]], '--k', label='field capacity layer 1')

    ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
    ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')

    ax.legend()
    plt.tight_layout()


    # plt.figure()
    # plt.title('Total Soil Moisture')
    # plt.plot(stiData_lettuce[itime,iday],totalVol[itime], label='total water volume [mm]' )
    # plt.plot(stiData_lettuce[itime,iday],totalSWC[itime], label = 'total soil water content' )
    # plt.plot([t0,tf],[totalSfc,totalSfc],'--', label='Sfc')
    # plt.plot([t0,tf],[totalSwp,totalSwp],'-.', label='Swp')
    # plt.bar(stiData_lettuce[itime,iday], stiData_lettuce[itime,iirrig], color='k', label='irrig' )
    # plt.bar(stiData_lettuce[itime,iday], stiData_lettuce[itime,idrain], color='b', label='Leakage' )
    # plt.legend()

    # plt.figure()
    # plt.title('Soil Moisture in root zone')
    # plt.plot(stiData_lettuce[itime,iday], stiData_lettuce[itime,itetstomate]+swpMes, '--', label='S*' )
    # plt.plot(stiData_lettuce[itime,iday], sRoot[itime]+swpMes, label='S root')
    # plt.plot(stiData_lettuce[itime,iday], sMes[itime], ':', label='S mes' )
    # plt.plot(stiData_lettuce[itime,iday],stiData_lettuce[itime,iWstress],'k',label='W stress' )
    # # plt.plot([t0,tf],[swpMes,swpMes],'--', label='SwpMes')
    # # plt.plot([t0,tf],[sfcMes,sfcMes],'-.', label='SfcMes')
    # plt.plot([t0,tf],[totalSfc,totalSfc],'--', label='Sfc')
    # plt.plot([t0,tf],[totalSwp,totalSwp],'-.', label='Swp')
    # plt.axis([t0, tf, -0.0 , 1.0])
    # plt.legend()

    # fig,ax=plt.subplots()
    # ax.plot(stiData_lettuce[itime,iday], sMes[itime], label='S mes' )
    # ax2=ax.twinx()
    # ax2.bar(stiData_lettuce[itime,iday], stiData_lettuce[itime,iirrig], label='irrig' )
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
Nleach = np.zeros(stiData_lettuce[:,iday].size)
Nleach[0] = stiData_lettuce[0,iQles]
Ndenit = np.zeros(stiData_lettuce[:,iday].size)
Ndenit[0] = stiData_lettuce[0,iNdenit]
for iNl in range(1,Nleach.size):
    Nleach[iNl]=stiData_lettuce[iNl,iQles]-stiData_lettuce[iNl-1,iQles]
    Ndenit[iNl]=stiData_lettuce[iNl,iNdenit]-stiData_lettuce[iNl-1,iNdenit]

Nmineralized = np.zeros(stiData_lettuce[:,iday].size)
Nmineralized[iSow] = stiData_lettuce[iSow,iNmineraliz]
Nvol = np.zeros(stiData_lettuce[:,iday].size)
Nvol[iSow] = stiData_lettuce[iSow,iNvol]

for iN in range(iSow,iHarv):
    Nmineralized[iN]=stiData_lettuce[iN,iNmineraliz]-stiData_lettuce[iN-1,iNmineraliz]
    Nvol[iN]=stiData_lettuce[iN,iNvol]-stiData_lettuce[iN-1,iNvol]

#total N03 [kg/ha]
# totalNO3=np.sum(stiData_lettuce[:,iAZnit],axis=1)
totalNO3=sticsIO.totalSoilVar("AZnit", stiData_lettuce)
totalNH4=sticsIO.totalSoilVar("AZamm", stiData_lettuce)
totalNorg=sticsIO.readOutput('Nhumt', stiData_lettuce)

Nvoleng = sticsIO.readOutput('Nvoleng', stiData_lettuce)


#effective fertiliser : fertilizer - immobilized - denitrified - volatized
Nfert = sticsIO.readOutput('anit(n)', stiData_lettuce) -sticsIO.readOutput('Norgeng', stiData_lettuce) -Ndenit -Nvoleng


## N in plant
CNplante = sticsIO.readOutput('CNplante', stiData_lettuce)      # N concetration iin plant [% dry weight]
Nplant = sticsIO.readOutput('QNplante', stiData_lettuce)      # amount of N taken up by the plant [kg/ha] = N mass in plant =CNplante * masecn / 100 *1000
Ndemande = sticsIO.readOutput('demande', stiData_lettuce)       # daily N need for max crop growth [kg/ha/d]
Nstress =  sticsIO.readOutput('inn', stiData_lettuce)           # N stress = CNplante / critical N plant concentration
NcritCon = CNplante/Nstress                                      # critical N plant concentration
NcritMass = NcritCon * masecn / 100


if __name__ == "__main__":

    # fig,ax = plt.subplots(figsize=(12,5))
    #
    # plt.title('Nitrogen in layers [kg/ha]')
    # ax.plot(dates, stiData_lettuce[itime,iAZnit[0]], label='Soil NO$_3$ (depth 0-20cm)')
    # ax.plot(dates, stiData_lettuce[itime,iAZnit[1]], label='Soil NO$_3$ (depth 20-40cm)')
    # ax.plot(dates, stiData_lettuce[itime,iAZnit[2]], label='Soil NO$_3$ (depth 40-60cm)')
    # # ax.plot(dates, stiData_lettuce[itime,iFertig],  label='Fertilisation')
    #
    # ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
    # # ax.plot([dates[iLev-it0],dates[iLev-it0]],[0,ax.get_ylim()[1]],'--b',label='emergence')
    # ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')
    # ax.legend()
    # plt.tight_layout()


    fig,ax = plt.subplots(figsize=(12,5))
    ax.set(title='Total Nitrogen [kg/ha]')
    ax.plot(dates, totalNO3[itime], label='total NO$_3$ ' )
    ax.plot(dates, totalNH4[itime], label='total NH$_4$ ' )
    # ax.plot(stiData_lettuce[itime,iday], totalNorg[itime], label='total N org ' )
    # ax.plot(dates, Nleach[itime], label='N leached ' )

    ax.plot(dates, NcritMass*1000, '-.', label = 'N critical mass [kg/ha]')
    ax.plot(dates, Nplant, '-.', label = 'N plante [kg/ha]')

    ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
    # ax.plot([dates[iLev-it0],dates[iLev-it0]],[0,ax.get_ylim()[1]],'--b',label='emergence')
    ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')
    ax.legend()
    plt.tight_layout()



    # fig,ax = plt.subplots(figsize=(12,5))
    # ax.plot(dates, Nstress, label = 'N stress')
    # ax.plot(dates, CNplante, label='N plant [% MS]' )
    #
    # ax.plot(masecn, NcritCon, label='crit N')
    # ax.plot(masecn, CNplante, label='N plant' )
    #
    # ax.legend()
    # plt.tight_layout()






# if __name__ == "__main__":
#
#
#     fig,ax = plt.subplots(figsize=(12,5))
#     ax.set(title='Stress')
#
#     ax.plot(dates, Nstress, label = 'N stress')
#     ax.plot(dates, Wstress, label = 'Water  stress')
#
#     ax.plot([dates[iSow-it0],dates[iSow-it0]],[0,ax.get_ylim()[1]],'--g',label='sowing')
#     ax.plot([dates[iHarv-it0],dates[iHarv-it0]],[0,ax.get_ylim()[1]],'--k',label='harvest')
#
#     ax.legend()
#     plt.tight_layout()



if __name__ == "__main__":
    plt.tight_layout()
    plt.show()
