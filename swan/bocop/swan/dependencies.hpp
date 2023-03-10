// Please give the headers of the functions called by your
// definition functions (criterion, dynamics, boundarycond, pathcond)

#include <common.hpp>
#include <publicTools.hpp>

// example of functions :

// template<class Tdouble> Tdouble external_function_with_Tdouble(const Tdouble argument_1,const int argument_2, const double argument_3);

// int external_function_without_Tdouble(const int argument_1,const double argument_2)


extern vector<double> rainv;
extern vector<double> ET0v;

template<class Tdouble> Tdouble ET0(const Tdouble time, const Tdouble t0);
template<class Tdouble> Tdouble rain(const Tdouble time, const Tdouble t0);
