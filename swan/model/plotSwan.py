import numpy as np
import matplotlib.pyplot as plt

# import pelakModel as mdl
import swanModel as mdl

#### utils

#standard colors
bstd = 'tab:blue'
ostd = 'tab:orange'
gstd = 'tab:green'

def finalize_2d(ax,fontsize=14):
    for aa in ax:
        for a in aa:
            a.legend(prop={'size': fontsize})
    plt.tight_layout()






################ single plots

def Sproc(ax,t,c,s,sty='',lbl=''):
    ### S process
    ax.plot(t, mdl.Irig(t), sty, color=bstd, label=r"Irrigation", linewidth=2.0)
    # ax.plot(t, -mdl.TransV(t, c, s), sty, color=ostd, label='T'+lbl,linewidth=2.0)
    # ax.plot(t, -mdl.EvapV(t, c, s), sty, color='r', label='E'+lbl,linewidth=2.0)
    ax.plot(t, mdl.LeakV(s), sty, color='k',  label='Leakage'+lbl,linewidth=2.0)


def climate(ax,t):
    ax.bar(t, mdl.Rain(t), color='c', label='Rain' )
    ax.plot(t, mdl.ET0(t), color='b', label='ET$_0$' )


def Nproc(ax,t,c,s,n,sty='',lbl=''):
    ### N process
    ax.plot(t, mdl.UpNV(t,c,s,n), sty, color=ostd, label='N Uptake'+lbl, linewidth=2.0)
    ax.plot(t, mdl.Irig(t)*mdl.Cn(t), sty, color=bstd, label='Fertilisation', linewidth=2.0)
    ax.plot(t, mdl.LeachV(s,n), sty, color='k', label='Leaching'+lbl, linewidth=2.0)


def stress(ax,t,s,n,sty='',lbl=''):
    ### stress indicators, in [0,1]
    ax.plot(t, mdl.KsV(s), sty, color=bstd, label='Water stress'+lbl,linewidth=2.0)
    ax.plot(t, mdl.NstressV(s, n), sty, color=ostd, label='N stress'+lbl,linewidth=2.0)










########## 2rows, 3 colums plots



def varproc_Setup_2x3(tini=None):
    if tini is None:
        tini = mdl.t0

    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 13})

    fig,ax = plt.subplots(2,3,figsize=(15,10))

    ax[0,0].set(title="Canopy [m$^2$/m$^2$] and Biomass [kg/m$^2$]",xlabel="Time[d]")
    # ax[0,0].plot(tsen*np.ones((2,1)), np.linspace(0,1,2), label=r'$t_{sen}$' )
    ax[0,0].grid()
    ax[0,0].axis([tini, mdl.tf, 0 , 2.5])

    ax[0,1].set(title="Soil Water [mm water/ mm soil]",xlabel="Time[d]")
    # ax[0,1].plot([tini, mdl.tf], mdl.Sh*np.ones((2,1)), label=r'$S_h$' ,linewidth=2.0)
    # ax[0,1].plot([tini, mdl.tf], mdl.Sw*np.ones((2,1)), '--', label=r'$S_w$' ,linewidth=2.0)
    # ax[0,1].plot([tini, mdl.tf], mdl.Sstar*np.ones((2,1)), '-.', label=r'$S^*$' ,linewidth=2.0)
    ax[0,1].grid()
    ax[0,1].axis([tini, mdl.tf, 0 , 0.5])

    ax[0,2].set(title=r"Mineral N [g/m$^2$]",xlabel="Time[d]")
    ax[0,2].grid()
    ax[0,2].set_xlim(tini,mdl.tf)

    # ax[0,2].set(title=r"Soil Nitrogen concentration [g/m$^3$]",xlabel="Time[d]")
    # ax[0,2].plot([0, mdl.tf], [mdl.etaC*1000, mdl.etaC*1000], '-.',color='tab:orange', label=r'$\eta_{c}$', linewidth=2.0)
    # ax[0,2].axis([0, mdl.tf, 0 , mdl.etaC*2*1000])
    # ax[0,2].set_xlim(0,mdl.tf)
    # ax[0,2].grid()

    ax[1,0].set(title="Stresses [-]",xlabel="Time[d]")
    ax[1,0].grid()
    ax[1,0].axis([tini, mdl.tf, 0 , 1.05])


    ax[1,1].set(title="Water process [mm/d]",xlabel="Time[d]")
    ax[1,1].grid()
    ax[1,1].set_xlim(tini,mdl.tf)

    ax[1,2].set(title=r"N process [g/m$^2$d]",xlabel="Time[d]")
    ax[1,2].grid()
    ax[1,2].set_xlim(tini,mdl.tf)
    ax[1,2].set_ylim(0,0.5)


    plt.tight_layout()

    return fig,ax



def var_2x3(ax,t,c,s,n,b,sty='',lbl=''):
    ax[0,0].plot(t, c,  sty, color=bstd, label="Canopy"+lbl,linewidth=2.0)
    ax[0,0].plot(t, b/1000,  sty, color=ostd, label=r"Biomass"+lbl,linewidth=2.0)
    ax[0,1].plot(t, s,  sty, color=bstd, label=r'Soil Water'+lbl,linewidth=2.0)
    ax[0,2].plot(t, n,  sty, color=bstd, label=r'N'+lbl,linewidth=2.0)
    # ax[0,2].plot(t, n/(s*mdl.phi*mdl.Z/1000), sty, color=bstd, label=r'$\frac{N}{z\phi S}$'+lbl,linewidth=2.0)




def varProc_2x3(ax,t,c,s,n,b,sty='',lbl=''):

    var_2x3(ax,t,c,s,n,b,sty='',lbl=lbl)

    # ax[0,2].plot(t, mdl.Ncrit(s), sty, color=ostd, label=r'$N_{crit}(S) $'+lbl ,linewidth=2.0)

    stress(ax[1,0],t,s,n,sty='',lbl=lbl)
    climate(ax[1,1],t)
    Sproc(ax[1,1],t,c,s,sty='',lbl=lbl)
    Nproc(ax[1,2],t,c,s,n,sty='',lbl=lbl)



######################### 3 rows 1 column

def Setup_3x1():
    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 12})

    fig,ax = plt.subplots(3,1,figsize=(7,10))

    ax[0].set(title="Canopy [m$^2$/m$^2$] and Biomass [kg/m$^2$]",)
    # ax[0,0].plot(tsen*np.ones((2,1)), np.linspace(0,1,2), label=r'$t_{sen}$' )
    ax[0].grid()
    ax[0].axis([0, mdl.tf, 0 , 2])

    ax[1].set(title="Soil Water")
    # ax[1].plot([0, mdl.tf], mdl.Sh*np.ones((2,1)), label=r'$S_h$' ,linewidth=2.0)
    # ax[1].plot([0, mdl.tf], mdl.Sw*np.ones((2,1)), '--', color=ostd, label=r'$S_w$' ,linewidth=2.0)
    ax[1].plot([0, mdl.tf], mdl.Sstar*np.ones((2,1)), '-.', color=gstd, linewidth=1.0) #label=r'$S^*$' ,
    ax[1].grid()
    ax[1].axis([0, mdl.tf, 0 , 1])

    ax[2].set(title=r"Nitrogen [g/m$^2$]",xlabel="Time[d]")
    ax[2].grid()
    ax[2].set_xlim(0,mdl.tf)

    plt.tight_layout()

    return fig,ax


def var_3x1(ax,t,c,s,n,b,sty='',lbl=''):
    ax[0].plot(t, c,  sty, color=bstd, label="C"+lbl,linewidth=3.0)
    ax[0].plot(t, b/1000,  sty, color=ostd, label=r"B"+lbl,linewidth=3.0)
    ax[1].plot(t, s,  sty, color=bstd, label=r'$S$'+lbl,linewidth=3.0)
    ax[2].plot(t, n,  sty, color=bstd, label=r'$N$'+lbl,linewidth=3.0)







######################################################
### 3 rows, 2 colums



def plotPelak3x2Setup():

    plt.rc('text', usetex=True)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams.update({'font.size': 28})
    fig,ax = plt.subplots(3,2,figsize=(2*7,3*3.7))

    plt.tight_layout()

    # for 3x2 plots
    plt.subplots_adjust(left=0.09, right=0.98, top=0.98, bottom=0.08, hspace = 0.2, wspace=0.22)

    numYticks=5


    # ax[0,0].set(title=r'Biomass')
    ax[0,0].set(ylabel=r'B [kg m$^{-2}$]')
    ax[0,0].axis([mdl.t0, mdl.tf, 0 , 3])
    start, end = ax[0,0].get_ylim()
    ax[0,0].yaxis.set_ticks(np.linspace(start, end, numYticks))


    # ax[0,1].set(title=r'Canopy')
    ax[0,1].set(ylabel=r'C [m$^2$ m$^{-2}$] ')
    ax[0,1].axis([mdl.t0, mdl.tf, 0 , 1])
    start, end = ax[0,1].get_ylim()
    ax[0,1].yaxis.set_ticks(np.linspace(start, end, numYticks))


    # # ax[1,0].set(title=r'Soil Moisture')
    ax[1,0].set(ylabel=r'S [m$^3$ m$^{-3}$]')
    ax[1,0].axis([mdl.t0, mdl.tf, 0 , 1])
    start, end = ax[1,0].get_ylim()
    ax[1,0].yaxis.set_ticks(np.linspace(start, end, numYticks))


    # ax[1,1].set(title=r'Soil Nitrogen')
    ax[1,1].set(ylabel=r'$N$ [g m$^{-2}$]')
    ax[1,1].axis([mdl.t0, mdl.tf, 0 , 20])
    start, end = ax[1,1].get_ylim()
    ax[1,1].yaxis.set_ticks(np.linspace(start, end, numYticks))


    # ax[2,0].set(title=r'Irrigation' )
    ax[2,0].set(ylabel=r'I [mm d$^{-1}$]')
    ax[2,0].axis([mdl.t0, mdl.tf, 0 , 10*1.03])
    ax[2,0].spines['left'].set_bounds(0, 10)
    ax[2,0].yaxis.set_ticks(np.linspace(0, 10, numYticks))


    # ax[2,1].set(title="Nitrogen Irrigation")
    ax[2,1].set(ylabel=r'$F_N$ [g m$^{-3}$]')
    ax[2,1].axis([mdl.t0, mdl.tf, -0.1 , 50*1.03])
    ax[2,1].spines['left'].set_bounds(0, 50)
    ax[2,1].yaxis.set_ticks(np.linspace(0, 50, numYticks))


    # remove top and right axis/ box boundary
    for a in ax:
        for aa in a:
            aa.spines['top'].set_visible(False)
            aa.spines['right'].set_visible(False)

    # remove x ticks for all execpt plots in last line
    for a in ax[:-1,:]:
        for aa in a:
            aa.tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)

    # x ticks  and label on plots of last line
    for a in ax[-1,:]:
        a.set(xlabel="Time - days [d]")
        a.xaxis.set_ticks(np.linspace(mdl.t0, mdl.tf, 6))

    return fig,ax


def plotPelak3x2(ax,t,c,s,n,b,sty='',lw=1.0):

    ax[0,0].plot(t, b/1000, sty,  linewidth=lw)

    ax[0,1].plot(t, c, sty, linewidth=lw)

    ax[1,0].plot(t, s, sty, linewidth=lw)

    ax[1,1].plot(t, n, sty,  linewidth=lw)

    ax[2,0].plot(t, mdl.Irig(t), sty,  linewidth=lw)

    ax[2,1].plot(t, mdl.Cn(t)*1000, sty,  linewidth=lw)









##############################################
### 6 rows, 1 colums



def plotPelakVertSetup():

    plt.rc('text', usetex=True)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams.update({'font.size': 20})
    numfigs=5
    fig,ax = plt.subplots(numfigs,1,figsize=(7,numfigs*2.2))

    plt.tight_layout()

    # for 6 plots
    # plt.subplots_adjust(left=0.12, right=0.97, top=0.99, bottom=0.05, hspace = 0.2)
    # for 5 plots with title
    plt.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.07, hspace = 0.27)

    numYticks=3
    iplot=0

    # iplot+=1
    ax[iplot].set(title=r'Biomass', ylabel=r'[kg m$^{-2}$]')
    # ax[iplot].set(ylabel=r'B [kg m$^{-2}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 2])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Canopy', ylabel=r'[m$^2$ m$^{-2}$] ')
    # ax[iplot].set(ylabel=r'C [m$^2$ m$^{-2}$] '))
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 1])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Soil Moisture', ylabel=r'[m$^3$ m$^{-3}$]')
    # ax[iplot].set(ylabel=r'S [m$^3$ m$^{-3}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 0.6])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Soil Nitrogen', ylabel=r'[g m$^{-2}$]')
    # ax[iplot].set(ylabel=r'$N$ [g m$^{-2}$]'))
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 14])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    # iplot+=1
    # ax[iplot].set(ylabel=r'$\frac{N}{z\phi S}$ (g m$^{-3}$)')
    # ax[iplot].axis([0, mdl.tf, 0 , etaC*2*1000])

    # iplot+=1
    # # ax[iplot].set(title=r'Irrigation' )
    # ax[iplot].set(ylabel=r'I [mm d$^{-1}$]')
    # ax[iplot].axis([mdl.t0, mdl.tf, 0 , 10*1.03])
    # ax[iplot].spines['left'].set_bounds(0, 10)
    # ax[iplot].yaxis.set_ticks(np.linspace(0, 10, numYticks))

    # iplot+=1
    # # ax[iplot].set(title="Nitrogen Irrigation")
    # ax[iplot].set(ylabel=r'$F_N$ [g m$^{-3}$]')
    # ax[iplot].axis([mdl.t0, mdl.tf, -0.1 , 50*1.03])
    # ax[iplot].spines['left'].set_bounds(0, 50)
    # ax[iplot].yaxis.set_ticks(np.linspace(0, 50, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Water and N stress', ylabel=r'[-]')
    # ax[iplot].set(ylabel=r'$N$ [g m$^{-2}$]'))
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 1.03])
    ax[iplot].spines['left'].set_bounds(0, 1)
    ax[iplot].yaxis.set_ticks(np.linspace(0, 1, numYticks))



    # remove top and right axis/ box boundary
    for aa in ax:
        aa.spines['top'].set_visible(False)
        aa.spines['right'].set_visible(False)

    # remove x ticks for all execpt last plot
    for iax in range(numfigs-1):
        ax[iax].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)

    ax[-1].set(xlabel="Time - day of year")

    return fig,ax




def plotPelakVert(ax,t,c,s,n,b,sty='',lw=1.0):
    iplot=0
    ax[iplot].plot(t, b/1000, sty,  linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, c, sty, linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, s, sty, linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, n, sty,  linewidth=lw)
    # iplot+=1
    # ax[iplot].plot(t, n/(s*phi*Z/1000), sty,  linewidth=lw)
    # iplot+=1
    # ax[iplot].plot(t, mdl.Irig(t), sty,  linewidth=lw)
    # iplot+=1
    # ax[iplot].plot(t, mdl.Cn(t)*1000, sty,  linewidth=lw)
    ## stress indicators, in [0,1]
    # iplot+=1
    # ax[iplot].plot(t, mdl.KsV(s), sty, color=bstd, linewidth=lw)
    # ax[iplot].plot(t, mdl.NstressV(s, n), sty, color=ostd, linewidth=lw)








############################################
### 
###           4 rows, 1 colum
###
#############################################



def plotPelak4x1Setup():

    plt.rc('text', usetex=True)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams.update({'font.size': 16})
    numfigs=4
    fig,ax = plt.subplots(numfigs,1,figsize=(7,numfigs*2.2))

    plt.tight_layout()

    # for 6 plots
    # plt.subplots_adjust(left=0.12, right=0.97, top=0.99, bottom=0.05, hspace = 0.2)
    # for 4 plots
    # plt.subplots_adjust(left=0.12, right=0.97, top=0.98, bottom=0.1, hspace = 0.2)
    # for 4 plots with title
    plt.subplots_adjust(left=0.12, right=0.97, top=0.96, bottom=0.08, hspace = 0.25)

    numYticks=3
    iplot=0

    # iplot+=1
    ax[iplot].set(title=r'Crop Biomass', ylabel=r'[kg m$^{-2}$]')
    # ax[iplot].set(ylabel=r'B [kg m$^{-2}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 2.1])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, 2, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Canopy Cover', ylabel=r'[m$^2$ m$^{-2}$] ')
    # ax[iplot].set(ylabel=r'C [m$^2$ m$^{-2}$] '))
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 1])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r' Relative Soil Moisture', ylabel=r'[m$^3$ m$^{-3}$]')
    # ax[iplot].set(ylabel=r'S [m$^3$ m$^{-3}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 0.6])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Soil Nitrogen', ylabel=r'[g m$^{-2}$]')
    # ax[iplot].set(ylabel=r'$N$ [g m$^{-2}$]'))
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 14])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    # iplot+=1
    # ax[iplot].set(ylabel=r'$\frac{N}{z\phi S}$ (g m$^{-3}$)')
    # ax[iplot].axis([0, mdl.tf, 0 , etaC*2*1000])

 
    # remove top and right axis/ box boundary
    for aa in ax:
        aa.spines['top'].set_visible(False)
        aa.spines['right'].set_visible(False)

    # remove x ticks for all execpt last plot
    for iax in range(numfigs-1):
        ax[iax].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)

    ax[-1].set(xlabel="Time - day of year")

    return fig,ax




def plotPelak4x1(ax,t,c,s,n,b,sty='',lw=1.0):
    iplot=0
    ax[iplot].plot(t, b/1000, sty,  linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, c, sty, linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, s, sty, linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, n, sty,  linewidth=lw)
    # iplot+=1
    # ax[iplot].plot(t, n/(s*phi*Z/1000), sty,  linewidth=lw)
 


def pltCtrl4x1(ax,t):
    axIr = ax[2].twinx()
    axIr.plot(t, mdl.Irig(t), 'k', linewidth=2)
    axIr.set(ylabel=r'[mm]')
    # remove top axis/ box boundary
    axIr.spines['top'].set_visible(False)
    axIr.axis([mdl.t0, mdl.tf, 0 , 20])
    axIr.yaxis.set_ticks(np.linspace(0, 20, 3))
    axIr.legend(['Irrigation'],frameon=False,fontsize=14)

    axCn = ax[3].twinx()
    axCn.plot(t, 1000*mdl.Cn(t), 'k', linewidth=2)
    axCn.set(ylabel=r'[g m$^{-3}$]')
    # remove top axis/ box boundary
    axCn.spines['top'].set_visible(False)
    axCn.axis([mdl.t0, mdl.tf, 0 , 100])
    axCn.yaxis.set_ticks(np.linspace(0, 100, 3))
    axCn.legend(['N Irrigation'],frameon=False,fontsize=14)





#############################
##
##    plot process Vert 
##
############################



def plotPelakVertSetup_proc():

    plt.rc('text', usetex=True)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams.update({'font.size': 20})
    numfigs=3
    fig,ax = plt.subplots(numfigs,1,figsize=(7,numfigs*2.4))

    plt.tight_layout()

    # for 3 plots with titles
    plt.subplots_adjust(left=0.12, right=0.97, top=0.95, bottom=0.1, hspace = 0.25)

    numYticks=3
    iplot=0

    # iplot+=1
    ax[iplot].set(title=r'Rain')
    ax[iplot].set(ylabel=r'[mm]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 40])
    start, end = ax[iplot].get_ylim()
    ax[iplot].yaxis.set_ticks(np.linspace(start, end, numYticks))

    iplot+=1
    ax[iplot].set(title=r'Irrigation' )
    ax[iplot].set(ylabel=r'[mm d$^{-1}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, 0 , 40*1.03])
    ax[iplot].spines['left'].set_bounds(0, 40)
    ax[iplot].yaxis.set_ticks(np.linspace(0, 40, numYticks))

    iplot+=1
    ax[iplot].set(title="N water concentration ")
    ax[iplot].set(ylabel=r'[g m$^{-3}$]')
    ax[iplot].axis([mdl.t0, mdl.tf, -0.1 , 50*1.03])
    ax[iplot].spines['left'].set_bounds(0, 50)
    ax[iplot].yaxis.set_ticks(np.linspace(0, 50, numYticks))

    # iplot+=1
    # ax[iplot].set(title="Water and N stress")
    # ax[iplot].set(ylabel=r'[-]')
    # ax[iplot].axis([mdl.t0, mdl.tf, 0, 1.03])
    # ax[iplot].spines['left'].set_bounds(0, 1)
    # ax[iplot].yaxis.set_ticks(np.linspace(0, 1, numYticks))


 
    # remove top and right axis/ box boundary
    for aa in ax:
        aa.spines['top'].set_visible(False)
        aa.spines['right'].set_visible(False)

    # remove x ticks for all execpt last plot
    for iax in range(numfigs-1):
        ax[iax].tick_params(axis='x', which='both',bottom=False,top=False, labelbottom=False)

    ax[-1].set(xlabel="Time - day of year")

    return fig,ax




def plotPelakVert_proc(ax,t,c,s,n,b,sty='',lw=1.0):
    iplot=0
    ax[iplot].bar(t, mdl.Rain(t), color='c')
    iplot+=1
    ax[iplot].plot(t, mdl.Irig(t), sty, linewidth=lw)
    iplot+=1
    ax[iplot].plot(t, mdl.Cn(t)*1000, sty, linewidth=lw)
    ### stress indicators, in [0,1]
    # iplot+=1
    # ax[iplot].plot(t, mdl.KsV(s), sty, color=bstd, linewidth=lw)
    # ax[iplot].plot(t, mdl.NstressV(s, n), sty, color=ostd, linewidth=lw)





