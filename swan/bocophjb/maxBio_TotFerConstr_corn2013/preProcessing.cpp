// THIS FILE IS OPTIONAL !

// This code is published under the Eclipse Public License
// File: preProcessing.cpp
// Authors: Daphne Giorgi, Benjamin Heymann, Pierre Martinon, Olivier Tissot

// Function to make pre-processing, called before solving problem.
// Via this function, the user can access to the values of
// the definition and can change them.

// The following are the input and output available variables
// in post-processing function.
// Input :
// dim_constants : the number of constants
// constants     : the vector containing the constants

// Input/Output :
// starting_point: the vector for the starting point of the simulation
// starting_mode: the starting mode for the simulation

// Remember that the vectors numbering starts from 0
// (ex: the first component of the vector state is state[0])


#include "publicTools.hpp"
#include "dependencies.hpp"
using namespace std;

vector<double> Rain;
vector<double> ET0;


#include "header_preProcessing"
{
    //read rain data
    int verbose = 1;

    readFileToVector("/home/ahaddon/Dropbox/Work/ReUse/code/doubleModel/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/rain_corn2013",Rain,verbose);
    readFileToVector("/home/ahaddon/Dropbox/Work/ReUse/code/doubleModel/swan/bocophjb/maxBio_TotFerConstr_corn2013/data/ET0_corn2013",ET0,verbose);

    return 0;
}
