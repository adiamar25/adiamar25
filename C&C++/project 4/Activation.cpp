
#include "Matrix.h"
#include "Activation.h"


Matrix activation::relu (Matrix A)
{
  Matrix relu_mat(A.get_rows(), A.get_cols());

  for (int i = 0; i < relu_mat.get_rows(); ++i)
  {
    for (int j = 0; j < relu_mat.get_cols(); ++j)
    {
      if (A(i, j) > 0)
      {
        relu_mat(i, j) = A(i, j);
      }
    }
  }

  return relu_mat;
}

Matrix activation::softmax (Matrix A)
{
  Matrix soft_mat(A.get_rows(), A.get_cols());

  float exp_sum = 0;
  for (int i = 0; i < soft_mat.get_rows(); ++i)
  {
    for (int j = 0; j < soft_mat.get_cols(); ++j)
    {
      exp_sum += std::exp (A(i, j));
      soft_mat(i, j) = std::exp (A(i, j));
    }
  }

  exp_sum = 1 / exp_sum;
  soft_mat = exp_sum * soft_mat;

  return soft_mat;
}