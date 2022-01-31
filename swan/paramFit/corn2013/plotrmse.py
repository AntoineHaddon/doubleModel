import numpy as np
import matplotlib.pyplot as plt



rmseFile = '/home/ahaddon/Dropbox/Work/ReUse/code/plantSoilDyn/swan/paramFit/corn2013/rmseCorn2013'

rmse = np.loadtxt(rmseFile,delimiter=',')

plt.rcParams.update({'font.size': 12})
fig,ax = plt.subplots()

ax.plot(rmse[:,0]*10, rmse[:,1]*100, '.', label='Canopy')
ax.plot(rmse[:,0]*10, rmse[:,2]*100, 'v', label='Soil Water')
ax.plot(rmse[:,0]*10, rmse[:,3]*100, 's', label='Mineral N')
ax.plot(rmse[:,0]*10, rmse[:,4]*100, '*', label='Biomass')


ax.set(title='Relative RMSE [%]', xlabel='Total N [kg/ha]')
ax.set_ylim(0,16)
ax.legend()

plt.tight_layout()
plt.show()