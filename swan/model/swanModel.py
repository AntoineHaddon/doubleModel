import scipy.integrate as integrate
import scipy.interpolate as interpolate
import numpy as np
import matplotlib.pyplot as plt

# import warnings as wrng




###############
# Model param
###############


# Initial conditions
c0 = 0.01           # -                 Initial canopy
s0 = 0.5            # -                 Initial Soil Moisture
n0 = 10             # gN/m^2            Initial Soil N
b0 = 0.0            # g /m^2            Initial biomass
def IC():
    return [c0,s0,n0,b0]

# Time
t0 = 0              # d                 Initial time
tf = 140            # d                 Final Time
times = np.linspace(t0,tf,tf-t0)

# Canopy 
tsen=110            # d                 Days to senescence
rG=0.56             # m^2/gN            Canopy growth per unit N uptake
cMax = 0.9          # -                 Max canopy
rM=0.2              # 1/d               Canopy decline due to metabolic limitation
gamma=0.005         # 1/d^2             Slope of increase of senescence after tsen
exLai = 0.7         #                   Conversion parameter from LAI to canopy cover

# Water 
Kcb=1.03            # -                 Max T/ET0
Kce=1.1             # -                 Max E/ET0

# Biomass 
Wstar=33.7          # gB/m^2/d          Normalized daily water productivity
h=0.5               # kgY/kgB           Maximum harvest index

# Nitrogen 
etaC=0.054          # g/(mm*m^2)=g/L    Maximum N concentration taken up
aN=1.               # -                 Dissolved N fraction

#Climate 
ET0ref=5            # mm/d              Reference evapotranspiration

# soil 
Sh=0.14             # -                 Hygroscopic point
Sw=0.17             # -                 Wilting point
Sstar=0.35          # -                 Point of incipient stomatal closure
Sfc=0.59            # -                 Field capacity
Ssat=1              # -                 Saturation
ksat=330            # mm/d              Saturated hydraulic conductivity
d=13                # -                 Leakage param
phi=0.43            # -                 Soil porosity
Z=1000.             # mm                Soil depth




#all parameters
allParams = ['tsen', 'Z', 'gamma', 'exLai', 'ksat', 'Kce', 'Sh', 'phi', 'Sw', 'Sstar', 'd', 'etaC', 'Kcb', 'rG', 'rM', 'Wstar']


def printParams(pnames,prefix=''):
    # print(globals())
    for p in pnames:
        print(prefix+ p + ' = ' + str(globals()[p]) )


def readParams(fileName):
    """ read parameters from file
        each line of file must be 'paramName paramvalue'
        comment with # : line not read """
    with open(fileName,'r') as f:
        for line in f:
            if not line[0] == '#':
                pName,pVal =line.split()
                globals()[pName] = float(pVal)
                # print( pName,pVal)


def writeParams(fileName,pNames=allParams):
    """ write current global value of parameters in pNames to fileName
        possible problem if a paramName is included in another paraName, i.e. if a parameter is 'a' and other param is 'gamma' """
    lines = open(fileName,'r').readlines()
    for p in pNames:
        wrt=0
        for il,l in enumerate(lines):
            if p in l and not l[0] =='#':
                lines[il] = p + "  " + str(globals()[p]) + "\n"
                wrt=1
                break
        if not wrt:
            lines.append(p + "  " + str(globals()[p]) + "\n")

    with open(fileName,'w') as f:
        f.writelines(lines)



# if __name__ == '__main__':

    # printParams(['phi','Sfc','Sw','Sh'])
    #
    # paramFile = 'paramPelak'
    # writeParams(paramFile, allParams)
    # phi=1
    # writeParams(paramFile, ['phi'])
    # readParams(paramFile)
    # printParams(['phi','Sfc','Sw','Sh'])



#####################
# process
####################



def Ks(s):
    # water stress coeffecient
    if s<Sw:
        return 0
    elif s<Sstar:
        return (s-Sw)/(Sstar-Sw)
    else:
        return 1


def Kr(s):
    # evaporation reduction coeffecient
    if s<Sh:
        return 0
    else:
        return (s-Sh)/(1-Sh)

#reference evaporation
ET0 = interpolate.interp1d([t0, tf] , [ET0ref, ET0ref] ,kind='previous' )


def Trans(t,c,s):
    # transpiration rate
    return Ks(s)*c*Kcb*ET0(t)

def Evap(t,c,s):
    # evaporation rate
    # return Kr(s)*Kce*ET0(t)*(1-min(c,1))
    return Kr(s)*Kce*ET0(t)*(1-c)

def UpN(t,c,s,n):
    # nitrogen uptake rate
    return min(etaC, n/(s*phi*Z))*Trans(t,c,s)

def Ncrit(s):
    return etaC*phi*Z*s

def Nstress(s,n):
    return min(etaC, n/(s*phi*Z)) / etaC

def CanoGrow(t,c,s,n):
    # Canopy growth rate

    # logistic with stress and daily ET0, but fixed carrying capacity    
    return rG * min(etaC,n/(s*phi*Z)) * Ks(s) * Kcb * ET0(t) * c * ( 1- c/cMax )

    # from pelak
    # return rG*UpN(t,c,s,n) 

    # mean ETO
    # return rG * min(etaC, aN*n/(s*phi*Z)) * Ks(s)*c*Kcb* ET0ref 
    
    # without stress
    # return rG * etaC*c*Kcb* ET0ref 

    # pure logistic
    # return rG * c 


def Mor(t,c):
    #  senescence
    if t<t0+tsen:
        return 0
    else:
        return  gamma*(t-t0-tsen) *c**2


def Leak(s):
    # leaking rate
    ## tipping bucket style
    if s<Sfc:
        return 0
    else:
        return ksat*((s-Sfc)/(Ssat-Sfc))


def Leach(s,n):
    # N leaching rate
    eps=1e-12
    if s<0.13:
        return eps
    else:
        return Leak(s)*aN*n/(s*phi*Z) 


def BiomassG(t,c,s,n):
    # biomass growth rate
    # return Wstar*UpN(t,c,s,n)/(etaC*max(ET0(t),0.0001))
    return Wstar * min(etaC, n/(s*phi*Z))/etaC * Ks(s)*c*Kcb *min(ET0(t)/ET0ref,1)



#vector version
TransV=np.vectorize(Trans,otypes=[np.float])
EvapV=np.vectorize(Evap,otypes=[np.float])
LeakV=np.vectorize(Leak,otypes=[np.float])
KsV=np.vectorize(Ks,otypes=[np.float])

LeachV=np.vectorize(Leach,otypes=[np.float])
UpNV=np.vectorize(UpN,otypes=[np.float])
NstressV=np.vectorize(Nstress,otypes=[np.float])



#####################
# Controls / inputs
#####################

# Open loop

#  interpolate from calendar
def fromCalendar(dates,Vals,interKind='previous'):
    Cal=np.zeros(int(tf+1-t0))
    Cal[[int(d-t0) for d in dates]]=Vals
    return interpolate.interp1d(np.arange(t0,tf+1), Cal, kind=interKind, bounds_error=False, fill_value=(1e-10,1e-10) )



Rain = fromCalendar([0], [0])
Irig=fromCalendar([0], [0])
Cn=fromCalendar([0], [0])
Ferti=fromCalendar([0], [0])






#########################
# Dynamics
########################

# with open loop controls


def CanopyMoistNitro(t,y):
    c,s,n=y
    dC = CanoGrow(t,c,s,n) - Mor(t,c)
    dS = 1/(phi*Z) * ( Rain(t) + Irig(t) - Trans(t,c,s) - Evap(t,c,s) - Leak(s) )
    dN = Irig(t)*Cn(t) + Ferti(t) - Leach(s,n) - UpN(t,c,s,n)

    return [dC,dS,dN]


def CanopyMoistNitroBio(t,y):
    c,s,n,b=y
    dC = CanoGrow(t,c,s,n) - Mor(t,c)
    dS = 1/(phi*Z) * ( Rain(t) + Irig(t) - Trans(t,c,s) - Evap(t,c,s) - Leak(s) )
    dN = Irig(t)*Cn(t) + Ferti(t) - Leach(s,n) - UpN(t,c,s,n)
    dB = BiomassG(t,c,s,n)

    return [dC,dS,dN,dB]



def simPelak(tol=1e-8, dense=False, tout=None):
    """ Simulate Pelak model 
        with open loop controls, def variables Irig and Cn 
        options : 
            'tol' : ODE solver error  
            'dense' : outputs interpolated functions of time
            'tout' : Times at which to store the computed solution    
        """
    if dense:
        sol = integrate.solve_ivp(CanopyMoistNitroBio, [t0, tf], IC(), dense_output=dense,  rtol=tol, atol=tol, method='LSODA')
        return sol.t, sol.sol
    else:
        sol = integrate.solve_ivp(CanopyMoistNitroBio, [t0, tf], IC(), t_eval=tout,  rtol=tol, atol=tol, method='LSODA')
        Can, SoilM, Nitro, Biom = sol.y
        return sol.t, Can, SoilM, Nitro, Biom



def simPelakDense(IC,tf,tout=None,tol=1e-8):
    """legacy fct for compatibilty, should use simPelak with options"""
    sol = integrate.solve_ivp(CanopyMoistNitroBio, [t0, tf], IC(), dense_output=True,  rtol=tol, atol=tol, method='LSODA')
    if tout is None:
        return sol.t, sol.sol
    else:
        Can, SoilM, Nitro, Biom = sol.sol(tout)
        return tout, Can, SoilM, Nitro, Biom




def simulate(tol=1e-4):
    """ Simulate Pelak model 
        with open loop controls, def variables Irig and Cn 
        options : 
            'tol' : ODE solver error  
        """
    sol = integrate.solve_ivp(CanopyMoistNitroBio, [t0, tf], IC(), t_eval=times,  rtol=tol, atol=tol, method='LSODA',max_step=0.8)
    return sol.y






# with feedback

def csnbDynFeedback(t,y,feedback):
    c,s,n,b=y
    I,Cn = feedback(t,y)
    dC = CanoGrow(t,c,s,n) - Mor(t,c)
    dS = 1/(phi*Z) * ( Rain(t) + I - Trans(t,c,s) - Evap(t,c,s) - Leak(s) )
    dN = I*Cn - Leach(s,n) - UpN(t,c,s,n)
    dB = BiomassG(t,c,s,n)

    return [dC,dS,dN,dB]




def simPelakFeedback(IC,tf,feedback,tout=None,tol=1e-8):
    sol = integrate.solve_ivp(csnbDynFeedback, [0, tf], IC(), args=(feedback,), dense_output=True,  rtol=tol, atol=tol,  method='LSODA', max_step=0.1)
    if tout is None:
        Can, SoilM, Nitro, Biom = sol.sol(sol.t)
        return sol.t, Can, SoilM, Nitro, Biom
    else:
        Can, SoilM, Nitro, Biom = sol.sol(tout)
        return tout, Can, SoilM, Nitro, Biom








def printSimuInfo(t,c,s,n,b):

    totalIrrig = np.trapz(Irig(t), x=t)
    totalNfert = np.trapz(Irig(t)*Cn(t), x=t)
    totalNupt = np.trapz(UpNV(t,c,s,n), x=t)
    totalLeach = np.trapz(LeachV(s,n), x=t)


    print('Final Canopy : %.4f ' %(c[-1]) )
    print('Final Biomass : %.4f g/m^2 =  %.1f kg/ha ' %(b[-1], b[-1]*10) )
    print('Total Irrigation :  %.1f mm ' % (totalIrrig )  )
    print('Total N Fertigation :  %.4f g/m^2 =  %.1f kg/ha ' %( totalNfert, totalNfert*10))
    print('Total N Uptake :  %.4f g/m^2 = %.1f kg/ha ' %( totalNupt , totalNupt*10))
    print('Total N Leached :  %.6f g/m^2 = %.3f kg/ha ' %( totalLeach , totalLeach*10))
    print('N(Tf)-N(0) = %.3f g/m^2 ' %(n[-1]-n[0]) )
    print('N balance : Fertig - Uptake - Leach = %.3f g/m^2 ' %(totalNfert -totalNupt - totalLeach) )















if __name__ == "__main__":



    ######## corn 2013
    readParams('params_swan_Iref_Corn2013')
    [c0,s0,n0,b0] = [0.008,0.376,12.85,0]
    t0 = 128
    tsen = 90
    tf= t0+118
    ET0 = interpolate.interp1d([t0, tf] , [ET0ref, ET0ref] ,kind='previous' )



    #### Open loop controls from irrgiation and fertilisation calendar
    irigdate = np.array([207,226])
    irigdose = 30 * np.ones(irigdate.shape)  # mm/d
    Irig = fromCalendar(irigdate, irigdose)
    Ndose=0.05*np.ones(irigdate.shape)      # g/(mm*m^2)=g/L
    Cn = fromCalendar(irigdate, Ndose)



    ### rain from file
    with open('meteo-gaillac-2013','r') as f:
        meteo = f.readlines()
        rainVect = [ l.split()[9] for l in meteo[t0:tf+1] ]

    Rain = interpolate.interp1d(np.arange(t0,tf+1), rainVect, kind='previous', bounds_error=False, fill_value=(1e-10,1e-10) )
    

    times, Can, SoilM, Nitro, Biom = simPelak(tout=np.arange(t0,tf,0.5))



    printSimuInfo(times, Can, SoilM, Nitro, Biom)











    plt.rc('text', usetex=True)
    plt.rcParams.update({'font.size': 18})

    fig,ax = plt.subplots(2,3,figsize=(15,10))

    ax[0,0].set(title="Canopy and Biomass",xlabel="Time[d]")
    # ax[0,0].plot(tsen*np.ones((2,1)), np.linspace(0,1,2), label=r'$t_{sen}$' )
    ax[0,0].grid()
    ax[0,0].axis([t0, tf, 0 , 2])

    ax[0,1].set(title="Soil Moisture",xlabel="Time[d]")
    # ax[0,1].plot([t0, tf], Sh*np.ones((2,1)), label=r'$S_h$' ,linewidth=3.0)
    ax[0,1].plot([t0, tf], Sw*np.ones((2,1)), '--', label=r'$S_w$' ,linewidth=3.0)
    ax[0,1].plot([t0, tf], Sstar*np.ones((2,1)), '-.', label=r'$S^*$' ,linewidth=3.0)
    ax[0,1].grid()
    ax[0,1].axis([t0, tf, 0 , 1])

    ax[0,2].set(title=r"Nitrogen [g/m$^2$]",xlabel="Time[d]")
    ax[0,2].grid()
    # ax[0,2].set(title=r"Nitrogen concentration [g/m$^3$]",xlabel="Time[d]")
    # ax[0,2].plot([t0, tf], [etaC*1000, etaC*1000], '-.',color='tab:orange', label=r'$\eta_{c}$', linewidth=3.0)
    # ax[0,2].axis([t0, tf, 0 , etaC*2*1000])
    ax[0,2].set_xlim(t0,tf)

    ax[1,0].set(title=r"N process [g/m$^2$d]",xlabel="Time[d]")
    ax[1,0].grid()
    # ax[1,0].axis([t0, tf, 0 , 0.0011])

    ax[1,1].set(title="Water process [mm/d]",xlabel="Time[d]")
    ax[1,1].bar(np.arange(t0,tf+1), Rain(np.arange(t0,tf+1)), color='c', label='Rain' )
    ax[1,1].plot(np.arange(t0,tf+1), ET0(np.arange(t0,tf+1)), color='r', label='ET0' )
    ax[1,1].grid()
    # ax[1,1].axis([t0, tf, -0.5 , 10.5])

    ax[1,2].set(title="Nitrogen Irrigation [g/L]",xlabel="Time[d]")
    ax[1,2].grid()
    # ax[1,2].axis([t0, tf, -.0025 , 0.0525])





    # #standard colors
    bstd = 'tab:blue'
    ostd = 'tab:orange'

    ax[0,0].plot(times, Can, bstd, label="Canopy",linewidth=3.0)
    ax[0,0].plot(times, Biom/1000, ostd, label=r"Biomass",linewidth=3.0)

    ax[0,1].plot(times, SoilM, bstd, label=r'$S(t)$',linewidth=3.0)

    ax[0,2].plot(times, Nitro, bstd, label=r'$N(t)$',linewidth=3.0)
    ax[0,2].plot(times, Ncrit(SoilM), ostd, label=r'$N_{crit}(S(t)) $' ,linewidth=3.0)
    # ax[0,2].plot(times, n/(s*phi*Z/1000), bstd, label=r'$\frac{N}{z\phi S}$',linewidth=3.0)

    ax[1,0].plot(times,LeachV(SoilM,Nitro),  label='Leaching',linewidth=3.0)
    ax[1,0].plot(times,UpNV(times,Can,SoilM,Nitro),  label='Plant Uptake',linewidth=3.0)
    ax[1,0].plot(times,Irig(times)*Cn(times),  label=r"$I(t) C_N(t)$",linewidth=3.0)

    ax[1,1].plot(times, Irig(times),  label=r"I(t)", linewidth=3.0)

    ax[1,2].plot(times, Cn(times),  label=r"$C_N(t)$",linewidth=3.0)





    for aa in ax:
        for a in aa:
            a.legend()

    plt.tight_layout()

    plt.show()



