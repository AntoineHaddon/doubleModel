// This code is published under the Eclipse Public License
// File: constraints.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Jinyan Liu, Pierre Martinon, Olivier Tissot
// Inria Saclay and Cmap Ecole Polytechnique
// 2014-2016

// Function for the state admissibility

// Input :
// time : current time (t)
// state : vector of state variables (x)
// mode : current mode of the system (i)
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// true if the state is admissible
// false if it is not
#include "header_checkAdmissibleState"
{

  // // leaking rate
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
  // if (Leach<constants[0])
  //   return true;
  // else
  //   return false;

  return true;

}

// Function for the (control,state) admissibility

// Input :
// time : current time (t)
// state : vector of state variables (x)
// control: vector of control variables (u)
// mode : current mode of the system (i)
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// true if the (control,state) pair is admissible
// false if it is not
#include "header_checkAdmissibleControlState"
{
  if (control[1]<=constants[1]*control[0])
    return true;
  else
    return false;
}


#include "header_checkAdmissibleFinalState"
{
  // if (constants[0]>final_state[3])
  //   return true;
  // else
  //   return false;

  return true;

}
