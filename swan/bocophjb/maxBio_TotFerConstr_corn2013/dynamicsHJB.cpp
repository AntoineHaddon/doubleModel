// This code is published under the Eclipse Public License
// File: dynamicsHJB.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Jinyan Liu, Pierre Martinon, Olivier Tissot
// Inria Saclay and Cmap Ecole Polytechnique
// 2014-2016

#include "dependencies.hpp"


// General dynamics
// dy/dt = drift(t,y,u)dt + volatility(y,u)dWt where Wt is the standard Brownian motion


// Function for the drift (deterministic dynamics)

// Input :
// time : current time t
// initial_time : t0
// final_time : tf
// state : vector of state variables x
// control : vector of control variables u
// mode : mode of the system i
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// state_dynamics : drift f(t,x,u,i) ie deterministic dynamics




#include "header_drift"
{

  double c = state[0];
  double s = state[1];
  double n = state[2];
  // double b = state[3];

  double i = control[0];
  double Icn = control[1];
  // double cn = 1.0;

 // Model param fitted to corn2013
  double z=1000.;                 // mm               Soil depth
  double ET0ref=4.595;
  double Ssat=0.5;
  double Sfc=0.375;              // -                Field Capacity
  double Sstar=0.2446;            // -                Point of incipient stomatal closure
  double Sw=0.1747;              // -                Wilting point
  double Sh=0.0602;               // -                Hygroscopic point
  double ksat=200;              // mm/d             Saturated hydraulic conductivity
  double Kcb=1.2;                 // -                Max T/ET0
  double Kce=1.1;                 // -                Max E/ET0
  double etaC=0.033;            // g/(mm*m^2)=g/L   Maximum N concentration taken up
  double aN=0.3;                    // -                Dissolved N fraction
  double rG=0.948;                // m^2/gN           Canopy growth per unit N uptake
  double cMax=0.94;
  double tsen=90;                // d                Days to senescence
  double gamma=0.0012;            // 1/d^2            Slope of increase of senescence after tsen
  double Wstar=25.56;             // gB/m^2/d         Normalized daily water productivity


  // data for rain and ET0
  int k = floor(time);
  double rain_t = Rain[k];
  double et0_t = ET0[k];



  // water stress coeffecient
  double Ks;
  if (s<=Sw)
    Ks=0.;
  else if ( s>Sw && s<=Sstar)
    Ks=(s-Sw)/(Sstar-Sw);
  else
    Ks=1.;
  // Ks=s;

  // evaporation reduction coeffecient
  double Kr;
  if (s<Sh)
    Kr=0.;
  else
    Kr= (s-Sh)/(1.-Sh);
  // Kr=s;

  // transpiration rate
  double Tr=Ks*c*Kcb*et0_t;

  // evaporation rate
  double Ev=Kr*(1.-c)*Kce*et0_t;

  // nitrogen uptake concentration
  double UpN;
  if ( n/(s*z) < etaC )
    UpN= n/(s*z);
  else
    UpN= etaC;

  //metabolic limitation and senescence
  double Mor;
  if (time<tsen) {
    Mor = 0.0;
  } else {
    Mor =  gamma*(time-tsen)*c*c;
  }

  //leaking rate
  double Leak=0.;
  double Leach = 0.;
  if (s<Sfc) { 
    Leak=0.0;
    Leach=0.0;
  } else {
    Leak=ksat*(s-Sfc)/(Ssat-Sfc) ;
    Leach = Leak*aN*n/(s*z);
  }



  state_dynamics[0] = rG*UpN*Ks*Kcb*et0_t *c*(1-c/cMax) - Mor;
  state_dynamics[1] = 1/z * (rain_t + i - Tr - Ev - Leak ) ;
  state_dynamics[2] = Icn - Leach - UpN *Tr ;
  state_dynamics[3] = Icn;
}


// Function for the volatility (stochastic dynamics)

// Input :
// time : current time t
// initial_time : t0
// final_time : tf
// state : vector of state variables x
// control : vector of control variables u
// mode : mode of the system i
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// volatility_dynamics : vector giving the volatility expression of the volatility
// Remember that this is a matrix of dimension dim_state x dim_brownian and you have to fill every coefficient.
#include "header_volatility"
{
}
