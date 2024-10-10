
#include "Matrix.h"
#include "Dense.h"


Dense::Dense (Matrix weights, Matrix bias, activation_func f)
{
  _weights = weights;
  _bias = bias;
  _f = f;
}


Matrix Dense::get_weights () const
{
  return _weights;
}

Matrix Dense::get_bias () const
{
  return _bias;
}

activation_func Dense::get_activation () const
{
  return _f;
}

Matrix Dense::operator() (Matrix &A) const
{
  return _f((_weights * A) + _bias);
}
