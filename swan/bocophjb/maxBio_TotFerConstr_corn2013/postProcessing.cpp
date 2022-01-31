// THIS FILE IS OPTIONAL !

// This code is published under the Eclipse Public License
// File: postProcessing.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Pierre Martinon, Olivier Tissot

// Function to make post-processing, called after having solved the problem.
// Via this function, the user can access to the values of
// the solution and can make its own calculations on them.

// The following are the input and output available variables
// in post-processing function.
// Input :
// dim_step      : the number of time step
// dim_constants : the number of constants
// initial_time  : the initial time ( \f$ t_0 \f$)
// final_time    : the final time ( \f$t_F\f$ )
// constants     : the array containing the constants
// states        : the vector containing the states.
//                 First component is time step and second is space index.
// controls      : the vector containing the controls.
//                 First component is time step and second is space index.
// modes         : the vector containing the mode.
//                 It has only one component which is time.
// valueFunction : the vector containing the value function.
//                 It depends of (time, space, mode) INTEGER triplet.
//                 If we denote (t,x,m) such a triplet then
//                 V(t,x,m) = valueFunction[(dimStep - t)*modeNb + modeNb - 1 - m][x]
//                 where modeNb = modes.size()

// The equations of your problem have to be written in C++ code
// Remember that the vectors numbering starts from 0
// (ex: the first component of the vector state is state[0])

#include "header_postProcessing"
{
    return 0;
}
