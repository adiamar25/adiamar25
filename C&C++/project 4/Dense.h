// Dense.h
#ifndef DENSE_H
#define DENSE_H

#include "Activation.h"

// Insert Dense class here...

class Dense
{
 private:
  Matrix _weights;
  Matrix _bias;
  activation_func _f;

 public:
  Dense(Matrix weights, Matrix bias, activation_func f);
  Matrix get_weights() const;
  Matrix get_bias() const;
  activation_func get_activation() const;
  Matrix operator() (Matrix& A) const;
};



#endif //DENSE_H