import numpy as np
import xml.etree.ElementTree as ET
import datetime as dt

from sys import path as syspath
syspath.append('../../utils')
import readValsFromFile as rdvl

from os import getcwd

## global variables

# directory with files to run STICS simulation (parameter files, initial condition, weather , etc... )
dirStics = getcwd() + '/../corn/'

# directory with STICS program files 
# needs to be changed to the local path 
JavaSticsDir = '/home/ahaddon/Programs/JavaSTICS-1.41-stics-9.1/'





###############
## rum STICS
##############

import subprocess as sproc



def runUSM(usm):
    return sproc.run(["java", "-jar", "JavaSticsCmd.exe", "--run", dirStics, usm], cwd=JavaSticsDir)



if __name__ == "__main__":
    # set irragation calendar
    cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"
    irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
    # irrigCal_corn2013 = np.array([ range(200,230) , 30*[5.0]]).T
    writeIrrigCal(cropmgntFile_corn2013, irrigCal_corn2013)

    # rum STICS simulation
    usm_corn2013 = "maize_reuse_2013"
    print(runUSM(usm_corn2013))






######################
## Write inputs
#####################


def addIrrigIntervention(nodeIrrigCal,irrigIntervention):
    """ add an irrigation intervention at node in xml tree """
    ##### create new irrigation event
    newIntervention = ET.SubElement(nodeIrrigCal, 'intervention', attrib={'nb_colonnes': '2'} )
    Date = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'julapI_or_sum_upvt'} )
    Date.text = str(int(irrigIntervention[0]))
    Amount = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'amount'} )
    Amount.text = str(irrigIntervention[1])
    ## for formatting of file
    newIntervention.tail = "\n" + 20*" "
    newIntervention.text = "\n" + 22*" "
    Date.tail = "\n" + 22*" "



def writeIrrigCal(cropmgntFile,irrigCal):
    """ write irrigation dates and amounts in crop management file for STICS
        cropmgntFile is the _tec.xml file
        irrigCal is an 2d array with each line is an irrigation intervention with first element is date (julian) and second element is irrigation volume (in mm)
        i.e. : irrigCal = [ [ date1, amount1], [date2, amount2], ... ] """

    ##### read  _tec.xml file
    cropmgntTree = ET.parse(cropmgntFile)

    #### irrigation part of file
    for elem in cropmgntTree.getroot():
        if elem.attrib['nom']=='irrigation':
            nodeIrrig = elem

    ### set irrigation with calendar (i.e deactivate calcuation of irrigation by stics)
    ### i.e. need line <option choix="2" nom="automatic calculation of irrigations" nomParam="codecalirrig">
    for elem in nodeIrrig.iter('option'):
        if elem.attrib['nomParam'] == 'codecalirrig':
            elem.attrib['choix'] = '2'

    ## calendar of irrigation events
    for elem in nodeIrrig.iter('ta'):
        nodeIrrigCal = elem
        # print(elem.tag, elem.attrib)
    # for elem in nodeIrrigCal:
    #     print(elem.tag, elem.attrib)
    # for irrigIntervention in nodeIrrigCal.findall('intervention'):
    #     print(irrigIntervention.tag, irrigIntervention.attrib)#, irrigIntervention.text)
    #     for elem in irrigIntervention:
    #         print(elem.tag, elem.attrib, elem.text)

    ######## setting number of irrigation events
    nodeIrrigCal.set('nb_interventions', str( irrigCal.shape[0] ) )

    ####### remove old irrigation events
    for irrigIntervention in nodeIrrigCal.findall('intervention'):
        nodeIrrigCal.remove(irrigIntervention)

    ### add events
    for indexIrrig in range(irrigCal.shape[0]):
        addIrrigIntervention(nodeIrrigCal, irrigCal[indexIrrig] )

    ##### write file
    cropmgntTree.write(cropmgntFile)



# if __name__ == "__main__":
#     cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"

#     irrigCal_corn2013 = np.array([ [207,30.0], [226,30.0] ])
#     writeIrrigCal(cropmgntFile_corn2013,irrigCal_corn2013)






def addFertiIntervention(nodeFertiCal,fertiIntervention):
    """ add an fertilisation intervention at node in xml tree """
    ##### create new fertilisation event
    newIntervention = ET.SubElement(nodeFertiCal, 'intervention', attrib={'nb_colonnes': '2'} )
    Date = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'julapN_or_sum_upvt'} )
    Date.text = str(int(fertiIntervention[0]))
    Amount = ET.SubElement(newIntervention, 'colonne', attrib={'nom': 'absolute_value/%'} )
    Amount.text = str(fertiIntervention[1])
    ## for formatting of file
    newIntervention.tail = "\n" + 20*" "
    newIntervention.text = "\n" + 22*" "
    Date.tail = "\n" + 22*" "


def writeFertiCal(cropmgntFile,fertiCal,fertiType=None):
    """ write fertilisation dates and amounts in crop management file for STICS
        cropmgntFile is the _tec.xml file
        fertiCal is an 2d array with each line is an fertilisation intervention with first element is date (julian) and second element is fertilisation ammout [kg/ha]
        i.e. : fertiCal = [ [ date1, amount1], [date2, amount2], ... ] """

    ##### read  _tec.xml file
    cropmgntTree = ET.parse(cropmgntFile)

    #### fertilisation part of file
    for elem in cropmgntTree.getroot():
        if elem.attrib['nom']=='fertilisation':
            nodeFerti = elem

    #set fertilizer type
    if not fertiType is None:
        for elem in nodeFerti:
            if elem.attrib['nom']=='engrais':
                elem.text = str(fertiType)
                print(elem.tag, elem.attrib, elem.text)


    ## calendar of fertilisation events
    nodeFertiCal = nodeFerti.find('ta')
    # print(nodeFertiCal.tag, nodeFertiCal.attrib)

    ######## setting number of ferti events
    nodeFertiCal.set('nb_interventions', str( fertiCal.shape[0] ) )

    ####### remove old ferti events
    for fertiIntervention in nodeFertiCal.findall('intervention'):
        nodeFertiCal.remove(fertiIntervention)

    ### add events
    for indexFerti in range(fertiCal.shape[0]):
        addFertiIntervention(nodeFertiCal, fertiCal[indexFerti] )

    # for elem in nodeFertiCal:
    #     print(elem.tag, elem.attrib, elem.text)
    #     for subelem in elem:
    #         print(subelem.tag, subelem.attrib, subelem.text)


    ##### write file
    cropmgntTree.write(cropmgntFile)



# if __name__ == "__main__":
#     cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"
#
#     fertiCal_corn2013 = np.array([ [120,80.0], [207,30.0], [226,30.0] ])
#     # fertiCal_corn2013 = np.array([ [120,80.0], [207,30.0] ])
#     writeFertiCal(cropmgntFile_corn2013,fertiCal_corn2013)








def setIniFile(usmName,initFile):
    """ set initialisation file for usm 'usmName' by modifying dirStics/usms.xml file """
    ##### read  usms.xml file
    usmsTree = ET.parse(dirStics+"usms.xml")
    # print(usmName,initFile)
    # find node corrsponding to usmName
    for elem in usmsTree.getroot().findall('usm'):
        if elem.attrib['nom'] == usmName:
            nodeUsm = elem

    # change initFile
    for elem in nodeUsm.findall('finit'):
        elem.text = initFile

    ##### write file
    usmsTree.write(dirStics+"usms.xml")

# if __name__ == "__main__":
#     setIniFile("maize_reuse_2013","maize_ini.xml")
    # setIniFile("maize_reuse_2013","maize_fullNO3_ini.xml")



def setN0(initFile,N0):

    ### read inifile
    initTree = ET.parse(dirStics+initFile)
    # find node sol    
    for sol in initTree.getroot().findall('sol'):
        for nodeNO3 in sol.findall('NO3init'):
            for n0 in nodeNO3.findall('horizon'):
                i = int( n0.attrib['nh'] )-1
                n0.text = str(N0[i])

    ##### write file
    initTree.write(dirStics+initFile)




# if __name__ == "__main__":
#     setN0("maize_ini.xml",[20,15,15,10,0])











##################
# Read Params
#################




def readProfmes(cropmgntFile):
    """ read Profmes parameter from crop management file (*_tec.xml)"""
    ##### read  _tec.xml file
    cropmgntTree = ET.parse(cropmgntFile)
    #### irrigation part of file
    nodeIrrig = cropmgntTree.getroot()[4]
    return float(nodeIrrig[3].text)



# if __name__ == "__main__":
    # dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
    # cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"
    # print(readProfmes(cropmgntFile_corn2013))





def loadSoilParam(paramsolFile=None):
    #load parameter file
    if paramsolFile is None:
        paramsolFile = dirStics + 'param.sol'
    soilParam = rdvl.readVals(paramsolFile,firstLine=3)

    #colums indices for soil parameters
    ithickness=1         # of layer
    ifc=2               # soil water content at field capacity (in %)
    iwp=3                # soil water content at wilting point (%)
    ibulkDensity=4       # g/cm3

    soilDict = dict()
    # layer properties
    soilDict['thickness']=soilParam[:,ithickness]         # cm
    soilDict['hccf']=soilParam[:,ifc]     # field capacity : % dry weigth
    soilDict['hminf']=soilParam[:,iwp]    # wiltingpoint : % dry weigth
    soilDict['bulkDensity']=soilParam[:,ibulkDensity]

    # conversion of relative humidity levels to soil water content relative to volume
    soilDict['sfc']=soilParam[:,ifc]/100 * soilParam[:,ibulkDensity]
    soilDict['swp']=soilParam[:,iwp]/100 * soilParam[:,ibulkDensity]

    # general properties
    soilDict['totalDepth']=np.sum(soilParam[:,ithickness])
    soilDict['totalBulkDensity'] = np.sum(soilParam[:,ibulkDensity]*soilParam[:,ithickness])/soilDict['totalDepth']

    # swc levels for total soil : average weighted by layer thickness
    soilDict['totalSfc'] = np.sum(soilDict['sfc']*soilDict['thickness'])/soilDict['totalDepth']
    soilDict['totalSwp'] = np.sum(soilDict['swp']*soilDict['thickness'])/soilDict['totalDepth']

    return soilDict


def readSoilParam(paramName,paramsolFile=None):
    return loadSoilParam(paramsolFile)[paramName]




# if __name__ == '__main__':
#     print(readSoilParam('thickness') )
#     print(readSoilParam('totalSfc') )




######################
## Read Data
#####################

def varIndex(varName,varModFile=None):
    """ return index of variable to read .sti file data
        index is line number in var.mod file + nb of fixed outputs (4) """
    # fixed inputs : year,month,day (dayofmonth of month), jul (dayofmonth of year :julian dayofmonth)
    if varName == 'year':
        return 0
    if varName == 'month':
        return 1
    if varName == 'dayofmonthofmonth':
        return 2
    if varName == 'jul':
        return 3

    if varModFile is None:
        varModFile = dirStics+'var.mod'

    with open(varModFile) as file:
        for linenumber,line in enumerate(file):
            if varName in line:
                return linenumber + 4

    # if no return then error (variable is not in var.mod or user error)
    print('varIndex error, varName : ' + str(varName))
    return -1


varIndexRange=np.vectorize(varIndex)


# if __name__ == "__main__":
#     print(varIndex("lai(n)",'../corn1996/var.mod') )
#     print( np.array( [varIndex("HR("+str(i)+")") for i in range(1,6)] ) )
#     print( varIndexRange( ["HR("+str(i)+")" for i in range(1,6) ]) )
#     print( varIndexRange( ["lai", "resmes", "airg(n)" ]) )
#     print( varIndexRange( ["lai" ]) )





def loadData(stiFile):
    """ Returns a numpy array version of file stiFile
        same structure as mod_s**.sti file : on each line outputs for a dayofmonth """
    return rdvl.readVals(stiFile,firstLine=1)


def readOutput(varNames,simData,varModFile=None,tJul=None):
    """ Returns numpy array of varNames
        simData is numpy version of a mod_s**.sti file
        variables in columns, values for a day in line """
    if tJul is None:
        return simData[:,varIndexRange(varNames,varModFile)]
    else:
        tIniSti = simData[0,3]
        itimeStics = np.array(tJul-tIniSti, dtype=int)
        return simData[itimeStics[:, np.newaxis], varIndexRange(varNames,varModFile)]


def readOutputfromFile(varNames,stiFile,varModFile=None):
    """ Returns numpy array of varNames
        from sticsDir/mod_susmName.sti file
        variables in columns, values for a dayofmonth in line """
    simData = loadData(stiFile)
    return readOutput(varNames,simData,varModFile)





# if __name__ == "__main__":
#     sti_corn2013 = dirStics + 'mod_smaize_reuse_2013.sti'
#     data_corn2013 = loadData(sti_corn2013)

#     irrig = readOutput("airg(n)", data_corn2013)
#     tstics,lai,HR1 = readOutput(["jul","lai","HR(1)"], data_corn2013,'../corn/var.mod',tJul=np.arange(112,247) ).T
#     codebbch_output = readOutputfromFile("codebbch_output", sti_corn2013,)


#     import matplotlib.pyplot as plt
#     plt.plot(tstics,lai)
#     plt.plot(tstics,HR1)
#     # plt.plot(tstics,codebbch_output)
#     # plt.plot(irrig)
#     plt.show()








###############
# Time
###############



def DatetoJul(y,m,d):
    """ convert date d/m/y to Julian day i.e day of the year """
    return dt.datetime(y,m,d).timetuple().tm_yday


def JultoDate(jul,year=2013):
    return dt.datetime(year, 1, 1) + dt.timedelta(jul - 1)


# if __name__ == "__main__":
#     print(DatetoJul(2013,4,19))
#     print(JultoDate(247))



def readStages(stiFileorData,plant='corn',varModFile=None):
    """ Return dates (julian day) of stages for corn
        stages are sow, ger, lev, mat, rec
        ini and fin are inital and final day of sim"""

    if plant == 'lettuce':
        ### from proto_lettuce_plt.xml
        BBCHcodes= dict(sow=0, ger=-99, lev=9, mat=-99, rec=99)
    else:
        ### from corn_plt.xml
        BBCHcodes= dict(sow=0, ger=5, lev=9, mat=89, rec=99)

    # Simulation results
    if isinstance(stiFileorData, str):
        simData = loadData(stiFileorData)
    elif isinstance(stiFileorData, np.ndarray):
        simData = stiFileorData
    else:
        print('readStages_corn error : stiFileor data must be string or np.ndarray')

    bbch_t = readOutput("codebbch_output",simData,varModFile)

    stageDates=dict()
    for stage in BBCHcodes:
        index= np.argmax(bbch_t>=BBCHcodes[stage])   # finds first occurence in bbch_t when greater that BBCHcodes[ibb]
        stageDates[stage] = simData[index,3]

    stageDates['ini'] = simData[0,3]
    stageDates['fin'] = simData[-1,3]

    return stageDates





def readStages_corn(stiFileorData,varModFile=None):
    """ Return dates (julian day) of stages for corn
        stages are sow, ger, lev, mat, rec
        ini and fin are inital and final day of sim"""
    ### from corn_plt.xml
    BBCHcodes= dict(sow=0, ger=5, lev=9, mat=89, rec=99)

    # Simulation results
    if isinstance(stiFileorData, str):
        simData = loadData(stiFileorData)
    elif isinstance(stiFileorData, np.ndarray):
        simData = stiFileorData
    else:
        print('readStages_corn error : stiFileor data must be string or np.ndarray')

    bbch_t = readOutput("codebbch_output",simData,varModFile)

    stageDates=dict()
    for stage in BBCHcodes:
        index= np.argmax(bbch_t>=BBCHcodes[stage])   # finds first occurence in bbch_t when greater that BBCHcodes[ibb]
        stageDates[stage] = simData[index,3]

    stageDates['ini'] = simData[0,3]
    stageDates['fin'] = simData[-1,3]

    return stageDates



def readStageDayJul_corn(stage,stiFileorData,varModFile=None):
    return readStages_corn(stiFileorData,varModFile=None)[stage]


def readStageDate_corn(stage,stiFileorData,varModFile=None,year=2013):
    return JultoDate(readStageDayJul_corn(stage,stiFileorData,varModFile=None),year)


def trangeSticsJul(stiFile):
    return loadData(stiFile)[[0,-1],3]


# if __name__ == "__main__":
#     sti_corn2013 = dirStics + 'mod_smaize_reuse_2013.sti'
#     simData_corn2013 = loadData(sti_corn2013)

    # print( readStageDate_corn('sow',sti_corn2013) )
    # print( readStageDate_corn('sow',simData_corn2013) )

    # print( readStageDayJul_corn('ger',sti_corn2013)  )

    # stages = readStages_corn(sti_corn2013)
    # stages = readStages_corn(simData_corn2013)
    # t0Stics, tfStics = [stages[s] for s in ['sow','rec']]
    # print(t0Stics, tfStics)


    # print( trangeSticsJul(sti_corn2013) )






##################
# Climate
#################



#index of colums in stics climate file
climateVarIndex = dict(
year=2-2,
month=3-2,
dayofmonth=4-2,
jul=5-2,
tempMin=6-2,
tempMax=7-2,
radiation=8-2,
ET0=9-2,
rain=10-2,
#extra optional data
wind=11-2,
vaporPress=12-2,
CO2ppm=13-2
)



def readClimate(varName,climateFile):
    climateData = rdvl.readVals(climateFile)
    return climateData[:, climateVarIndex[varName]]


# if __name__ == '__main__':
#
#     climate2013 = dirStics + 'sitej.2013'
#
#     import matplotlib.pyplot as plt
#     plt.plot( readClimate('ET0', climate2013))
#     plt.show()




#######################################
# Stics Model variables computations
#####################################


def totalSoilVar(varName, simData, varModFile=None):
    """ sum variable varName over soil layers
        variables of type varName(i) with i =1,2,3,4,5
        example : varName=AZnit returns numpy array [ AZnit(1)+...+AZnit(5) ] """
    ivar = varIndexRange( [varName+"("+str(i)+")" for i in range(1,6)],  varModFile)
    return np.sum(simData[:,ivar], axis=1 )


def swcMes(simData, cropmgntFile, varModFile=None):
    """ Soil water content (relative to volume) up to measurement depth
        resmes [mm] / (profmes*10 [cm*10] ) """
    return readOutput("resmes",simData,varModFile) / (readProfmes(cropmgntFile)*10)


def Nleach(simData, varModFile=None,tJul=None):
    """ compute daily N leached as difference of cumulative amount from a day and previous day """
    iQles=varIndex("Qles",varModFile)      # cumulative amount of NO3-N leached at the base of the soil profile [kg/ha]
    res = np.zeros(simData[:,0].size)
    res[0] = simData[0,iQles]
    for iNl in range(1,res.size):
        res[iNl]=simData[iNl,iQles]-simData[iNl-1,iQles]
    if tJul is None:
        return res
    else:
        tIniSti = simData[0,3]
        itimeStics = np.array(tJul-tIniSti, dtype=int)
        return res[itimeStics]


# if __name__ == '__main__':
#
#     sti_corn2013 = dirStics + 'mod_smaize_reuse_2013.sti'
#     simData = loadData(sti_corn2013)
#
#     import matplotlib.pyplot as plt
#     plt.plot(totalSoilVar( "AZnit", simData) )
#     plt.show()
