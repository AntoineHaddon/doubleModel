// This code is published under the Eclipse Public License
// File: costFunctions.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Jinyan Liu, Pierre Martinon, Olivier Tissot
// Inria Saclay and Cmap Ecole Polytechnique
// 2014-2016

// Function for the running cost

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
// running_cost : running cost l(t,x,u,i)


#include "dependencies.hpp"


#include "header_runningCost"
{

  // min Irrigation or Fertigation
  // running_cost=control[1];


  // max final Biomass
  double c = state[0];
  double s = state[1];
  double n = state[2];

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

  //nitrogen limitation
  double Kn;
  if ( n/(s*z) < etaC )
    Kn = n/(s*z)/etaC ;
  else
    Kn = 1.;

  // weather limitation
  double Ke;
  if (et0_t<ET0ref)
    Ke = et0_t/ET0ref;
  else
    Ke=1.;


  running_cost = - Wstar* Kn* Ks*c*Kcb * Ke ;




  //leaking rate
  // double s = state[1];
  // double n = state[2];
  // double a=1.;                 // -             Dissolved N fraction
  // double phi=0.43;            // -             Soil porosity
  // double z=1.;                 // m             Soil depth
  // double ksat=0.33;           // m/d           Saturated hydraulic conductivity
  //
  // double Leak=0.;
  // double Leach = 0.;
  // double eeps=1e-12;
  // if (s<0.13) { //(s<(eps/ksat)**(1/d))
  //   Leak=eeps;
  //   Leach=eeps;
  // } else {
  //   Leak=ksat*s*s*s*s*s*s*s*s*s*s*s*s*s;
  //   Leach = Leak*a*n/(s*phi*z);
  // }
  //
  // running_cost = Leach;

}


// Function for the final cost

// Input :
// initial_time : t0
// final_time : tf
// final_state : vector of state variables x_f
// final_mode : final mode of the system i_f
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// final_cost : final cost g(t0,tf,x_f,i_f)
#include "header_finalCost"
{
final_cost = 0e0;
}


// Function for the switching cost

// Input :
// current_mode : current mode
// next_mode : next mode
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// switching_cost : switching cost s(i_k,i_k+1)
#include "header_switchingCost"
{
        switching_cost = 0e0;
}
