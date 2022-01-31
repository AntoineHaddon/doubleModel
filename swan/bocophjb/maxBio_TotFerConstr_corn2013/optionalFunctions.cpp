// This code is published under the Eclipse Public License
// File: optionalFunctions.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Jinyan Liu, Pierre Martinon, Olivier Tissot
// Inria Saclay and Cmap Ecole Polytechnique
// 2014-2016

// Function to define the value function outside of the state grid

// Input :
// time : current time (t)
// state : vector of state variables
// constants : vector of constants
// dim_constant : dimension of the vector constants

// Output :
// result : double representing the user interpolation formula
#include "header_userOutOfGridValueFunction"
{
    result = 1e8;
}

/** User function for component-wise control discretization */
#include "header_userControlDiscretization"
{
    vector <vector<double> > control_discretization;
    return control_discretization;
}

/** User function for the set of discretized controls*/
#include "header_userControlSet"
{
    vector< vector<double> > control_set;
    return control_set;
}

/** User function for the set of discretized controls (state dependent) */
#include "header_userControlSetStateDependent"
{
    vector< vector<double> > control_set;
    return control_set;
}

/** User function for the set of admissible transitions between system modes */
#include "header_userAdmissibleTransition"
{    
    vector<vector<int> > admissibleTransitionSet;
    return admissibleTransitionSet;
}

/** User function for state jump */
#include "header_stateJumpAtSwitching"
{

}
