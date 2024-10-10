
#include "Matrix.h"
#include "Activation.h"
#include "MlpNetwork.h"

MlpNetwork::MlpNetwork (const Matrix weights[], const Matrix biases[]) :
    _lay1 (weights[0], biases[0], activation::relu),
    _lay2 (weights[1], biases[1], activation::relu),
    _lay3 (weights[2], biases[2], activation::relu),
    _lay4 (weights[3], biases[3], activation::softmax)
{}

digit MlpNetwork::operator() (const Matrix& M)
{
  float probability;
  unsigned int val;
  Matrix res = M;
  res = res.vectorize();
  res = _lay1(res);
  res = _lay2(res);
  res = _lay3(res);
  res = _lay4(res);
  val = res.argmax();
  probability = res[(int)val];
  digit digit_to_return = {val, probability};
  return digit_to_return;
}

digit MlpNetwork::operator() (const Matrix &M) const
{
  float probability;
  unsigned int val;
  Matrix res = M;
  res = res.vectorize();
  res = _lay1(res);
  res = _lay2(res);
  res = _lay3(res);
  res = _lay4(res);
  val = res.argmax();
  probability = res[(int)val];
  digit digit_to_return = {val, probability};
  return digit_to_return;
}
