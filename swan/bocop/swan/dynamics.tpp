// Function for the dynamics of the problem
// dy/dt = dynamics(y,u,z,p)

// The following are the input and output available variables
// for the dynamics of your optimal control problem.

// Input :
// time : current time (t)
// normalized_time: t renormalized in [0,1]
// initial_time : time value on the first discretization point
// final_time : time value on the last discretization point
// dim_* is the dimension of next vector in the declaration
// state : vector of state variables
// control : vector of control variables
// algebraicvars : vector of algebraic variables
// optimvars : vector of optimization parameters
// constants : vector of constants

// Output :
// state_dynamics : vector giving the expression of the dynamic of each state variable.

// The functions of your problem have to be written in C++ code
// Remember that the vectors numbering in C++ starts from 0
// (ex: the first component of the vector state is state[0])

// Tdouble variables correspond to values that can change during optimization:
// states, controls, algebraic variables and optimization parameters.
// Values that remain constant during optimization use standard types (double, int, ...).
#include <math.h>       /* pow */
#include "header_dynamics"
{
	// HERE : description of the function for the dynamics
	// Please give a function or a value for the dynamics of each state variable
  Tdouble c = state[0];
  Tdouble s = state[1];
  Tdouble n = state[2];
  Tdouble b = state[3];


  // double c=0.7 ;
  // Tdouble c = 0.9 / (1. + exp(-0.1*(time-50.)));

  Tdouble i = control[0];
  // Tdouble Fn = control[1];
  Tdouble Cn = control[1];

 // Model param fitted to corn2013
  double z=1000.;                 // mm               Soil depth
  double ET0ref=4.595;
  double Ssat=0.5;
  double Sfc=0.375;              // -                Field Capacity
  double Sstar=0.2446;            // -                Point of incipient stomatal closure
  double Sw=0.1747;              // -                Wilting point
  double Sh=0.0602;               // -                Hygroscopic point
  double ksat=200.;              // mm/d             Saturated hydraulic conductivity
  double Kcb=1.2;                 // -                Max T/ET0
  double Kce=1.1;                 // -                Max E/ET0
  double etaC=0.033;            // g/(mm*m^2)=g/L   Maximum N concentration taken up
  double aN=0.3;                    // -                Dissolved N fraction
  double rG=0.948;                // m^2/gN           Canopy growth per unit N uptake
  double cMax=0.94;
  double tsen=90.;                // d                Days to senescence
  double gamma=0.0012;            // 1/d^2            Slope of increase of senescence after tsen
  double Wstar=25.56;             // gB/m^2/d         Normalized daily water productivity


 // data for rain and ET0
  Tdouble rain_t = rain(time,initial_time);
  Tdouble ET0_t = ET0(time,initial_time);


  // for smoothing of max
  double NN =25.;

  // water stress coeffecient
  // = max( 0 , min (1, s-Sw)/(Sstar-Sw )));
  Tdouble Ks = 1./NN * log( 1. + 1./( exp(-NN) + exp( -NN*(s-Sw)/(Sstar-Sw) ) ) )  ; 
	// Tdouble Ks;
	// if (s<=Sw)
	// 	Ks=0.;
	// else if ( s>Sw && s<=Sstar)
	// 	Ks=(s-Sw)/(Sstar-Sw);
	// else
 //        Ks=1.;


  // evaporation reduction coeffecient
  // = max( 0 , (s-Sh)/(1.-Sh) )
  Tdouble Kr= 1./NN * log( 1. + exp( NN*(s-Sh)/(1.-Sh) ) );
	// Tdouble Kr;
 //  if (s<Sh)
	// 	Kr=0.;
	// else
	//   Kr= (s-Sh)/(1.-Sh);

  // transpiration rate
  Tdouble Tr=Ks*c*Kcb*ET0_t;

  // evaporation rate
  Tdouble Ev=Kr*(1.-c)*Kce*ET0_t;

  // nitrogen uptake concentration
  // = min (n/(s*z) , etaC)
  double NNN = 100;
  Tdouble UpN = -1./NNN * log( exp(-NNN*etaC) + exp( -NNN*n/(s*z) ) );
     // Tdouble UpN=etaC;
    // if ( n/(s*z) < etaC )
    //  UpN= n/(s*z) *Tr;
    // else
    //  UpN= etaC*Tr;

  //leaking rate
  // = max( 0 , ksat*(s-Sfc)/(Ssat-Sfc))
  Tdouble Leak= 1./NN * log( 1. + exp( NN*ksat*(s-Sfc)/(Ssat-Sfc) ) );
  // Tdouble Leak=0. ;
  // if (s<Sfc) { 
  //   Leak=0;
  // } else {
  //   Leak=ksat*(s-Sfc)/(Ssat-Sfc) ;
  // }
  // Tdouble Leach = 0.;
  Tdouble Leach = Leak*aN*n/(s*z);

	// weather limitation
  // = min(1, et0_t/ET0ref)
  Tdouble Ke=-1./NNN * log( exp(-NNN*1.) + exp( -NNN*ET0_t/ET0ref ) );
  
  state_dynamics[0] = rG*UpN*Ks*Kcb*ET0_t *c*(1-c/cMax) ;
  state_dynamics[1] = 1/z * ( i + rain_t - Tr - Ev -Leak) ;
  state_dynamics[2] = i*Cn - Leach - UpN *Tr ;
  state_dynamics[3] = Wstar*UpN/etaC * Ks*c*Kcb ;
    
    state_dynamics[4] = i*Cn ;
}
