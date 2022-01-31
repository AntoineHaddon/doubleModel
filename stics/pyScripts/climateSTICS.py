import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../../utils')
import readValsFromFile as rdvl
import pandas as pd
import datetime as dt


import os
cwd = os.getcwd()

dirStics = cwd+'/../corn/'
filename=dirStics + 'sitej.2013'
# dirStics = '/home/ahaddon/Dropbox/Work/ReUse/code/stics/corn1996/'
# filename = dirStics + 'meteo-site1.1996'

climateData = rdvl.readVals(filename)

#index of colums
jyear=2-2
jmonth=3-2
jday=4-1
jtime=5-2
jtempMin=6-2
jtempMax=7-2
jradiation=8-2
jET0=9-2
jrain=10-2
#extra optional data
jwind=11-2
jvaporPress=12-2
jCO2ppm=13-2



### reference simulation for corn
# it0=90-1
# itf=330-1

### restriction from sowing to harvest
it0=112-1
itf=247-1

#fullyear
# it0=0
# itf=len(climateData[:,jtime])

# change time to dates
dates=  pd.date_range( dt.datetime(*[int(i) for i in climateData[it0,jyear:jday] ] ), periods=itf-it0 )


print('Means : \n')
print('ET0 : '+ str(np.mean(climateData[it0:itf,jET0])) )

plt.hist(climateData[it0:itf,jET0], 20 )


##### plots data
plt.rc('text', usetex=True)
# plt.rcParams.update({'font.size': 16})

# plt.plot(climateData[t0:tf,jtime],climateData[t0:tf,tempMin])
# plt.plot(climateData[t0:tf,jtime],climateData[t0:tf,tempMax])

# plt.plot(climateData[t0:tf,jtime],climateData[t0:tf,radiation])

# plt.plot(climateData[it0:itf,jtime],climateData[it0:itf,jET0])
# plt.bar(climateData[it0:itf+1,jtime],climateData[it0:itf+1,jrain])



fig,ax = plt.subplots(4,1,figsize=(7,2*4))
ax[0].plot(dates, climateData[it0:itf,jtempMin], 'b', label='Min')
ax[0].plot(dates, climateData[it0:itf,jtempMax], 'r', label='Max')
ax[0].set(title='Daily Temperature (°C)')
ax[0].legend()

ax[1].plot(dates, climateData[it0:itf,jradiation])
ax[1].set(title="Radiation (MJ m$^{-2}$ d$^{-1}$)")

ax[2].plot(dates, climateData[it0:itf,jET0])
ax[2].set(title="Reference Evapotranspiration (mm d$^{-1}$)")

ax[3].bar(dates,climateData[it0:itf,jrain])
ax[3].set(title="Rain (mm d$^{-1}$)")


# Define the date format
import matplotlib.dates as mdates
# from matplotlib.dates import DateFormatter
date_form = mdates.DateFormatter("%d-%m-%Y")
for a in ax:
    a.xaxis.set_major_formatter(date_form)
    # a.xaxis.set_major_locator(mdates.MonthLocator(interval=1))

plt.tight_layout()
plt.show()



################
# write data
################

# import sys
# sys.path.append('/home/ahaddon/bin')
# import writeVals as wrt

# # Rain
# rainCal = np.stack( (np.arange(itf-it0+1) , climateData[it0:itf+1,jrain] ), axis=1 )
# wrt.writeValstoFile("../corn/data/rain.dat",rainCal)

# # ET0
# ET0Cal = np.stack( ( np.arange(itf-it0+1) , climateData[it0:itf+1,jET0] ), axis=1 )
# wrt.writeValstoFile("../corn/data/ET0.dat",ET0Cal)
