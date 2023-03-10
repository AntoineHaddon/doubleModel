// Please include below the paths to the files containing the code
// for the external functions that use Tdouble variables. 
// Tdouble variables correspond to values that can change during optimization:
// states, controls, algebraic variables and optimization parameters.
// Values that remain constant during optimization use standard types (double, int, ...).
// External functions that don't use Tdouble are put in file dependencies.cpp.
// All external functions must also be declared in file dependencies.hpp.

// example of content :
// #include "./model/external_function_with_Tdouble.tpp"



template<class Tdouble> Tdouble ET0(const Tdouble time, const Tdouble t0)
{
 #ifndef USE_CPPAD
  int k =floor(time-t0);
  #else
  int k =CppAD::Integer(time-t0);
  #endif

  return ET0v[k];
}



template<class Tdouble> Tdouble rain(const Tdouble time, const Tdouble t0)
{
 #ifndef USE_CPPAD
  int k =floor(time-t0);
  #else
  int k =CppAD::Integer(time-t0);
  #endif

  return rainv[k];
}
