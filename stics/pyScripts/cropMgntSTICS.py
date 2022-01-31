import numpy as np
import xml.etree.ElementTree as ET



def addIrrigIntervention(nodeIrrigCal,irrigIntervention):
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
    #### write irrigation dates and amounts in crop management file for STICS
    #### cropmgntFile is the _tec.xml file
    #### irrigCal is an 2d array with each line is an irrigation intervention with first element is date (julian) and second element is irrigation volume (in mm)
    #### i.e. : irrigCal = [ [ date1, amount1], [date2, amount2], ... ]

    ##### read  _tec.xml file
    cropmgntTree = ET.parse(cropmgntFile)

    #### irrigation part of file
    nodeIrrig = cropmgntTree.getroot()[4]
    # for elem in nodeIrrig:
    #     print(elem.tag, elem.attrib)

    ### should check that irriagtion is with calendar and not calcuated by stics
    ### i.e. need line <option choix="2" nom="automatic calculation of irrigations" nomParam="codecalirrig">


    ## calendar of irrigation events
    nodeIrrigCal = nodeIrrig[1][1][1]
    # for irrigIntervention in nodeIrrigCal.findall('intervention'):
    #     print(irrigIntervention.tag, irrigIntervention.attrib)#, irrigIntervention.text)
    #     for elem in irrigIntervention:
    #         print(elem.tag, elem.attrib, elem.text)


    ####### get number of irrigation events
    # nbIrrigInterventions = int(nodeIrrigCal.attrib['nb_interventions'])
    # print(nbIrrigInterventions)

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




def readProfmes(cropmgntFile):
    ##### read  _tec.xml file
    cropmgntTree = ET.parse(cropmgntFile)

    #### irrigation part of file
    nodeIrrig = cropmgntTree.getroot()[4]

    return nodeIrrig[3].text



if __name__ == "__main__":


    dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
    cropmgntFile_corn2013 = dirStics + "maize_reuse_tec.xml"

    irrigCal_corn2013 = np.array([ [200,30.0], [207,30.0], [226,30.0] ])


    # writeIrrigCal(cropmgntFile_corn2013,irrigCal_corn2013)

    print(readProfmes(cropmgntFile_corn2013))
