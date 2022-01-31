import numpy as np
import matplotlib.pyplot as plt

import sticsIOutils as stiIO




########################
# Irrigation Calendars
#######################


#####ref scenario : used for fit
irrigCals = [np.array([ [207,30.0], [226,30.0] ])]

###### auto calculated by stics
# irrigCals = np.array([ [112,20], [197,40], [205,40], [218,40], [226,40], [235,40], [245,40] ])
irrigCals.append( np.array([  [197,40], [205,40], [218,40], [226,40], [235,40] ]) )

##### I2
irrigCals.append( np.array([ range(190,230) , 40*[5.0]]).T )

# ###### I3
irrigCals.append( np.array([ range(180,230,4) , 13*[5.0]]).T )
#
# ####### from MRAP feedback through file
import readValsFromFile as rdvl
irrigCals.append( rdvl.readVals("/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/pelak/irrigData/corn2013-Imrap.csv") )








#### STICS simulations setup : files
stiIO.dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn/'
sti_corn2013 = stiIO.dirStics + 'mod_smaize_reuse_2013.sti'
tec_corn2013 = stiIO.dirStics + "maize_reuse_tec.xml"
# cli_corn2013 = stiIO.dirStics + 'sitej.2013'
usm_corn2013 = "maize_reuse_2013"
# set initial conditons file
# stiIO.setIniFile(usm_corn2013,"maize_ini.xml")
stiIO.setIniFile(usm_corn2013,"maize_lowS0_ini.xml")

#### plot setup
fig,ax = plt.subplots(1,2,figsize=(10,5))
ax[0].set(title='LAI',xlabel='days')
ax[1].set(title='Irrigation [mm]',xlabel='days')

ax[0].set_xlim(120,250)
ax[1].set_xlim(120,250)




for ical in irrigCals:

    # set irragation calendar
    stiIO.writeIrrigCal(tec_corn2013, ical)

    # rum simulation
    stiIO.runUSM(usm_corn2013)

    ## load data
    stiData_corn2013 = stiIO.loadData(sti_corn2013)
    time = stiIO.readOutput("jul",stiData_corn2013)
    lai = stiIO.readOutput("lai(n)",stiData_corn2013)
    irrig = stiIO.readOutput("airg(n)",stiData_corn2013)

    ## plot
    ax[0].plot(time, lai)
    ax[1].plot(time, irrig)





plt.tight_layout()
plt.show()
