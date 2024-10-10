// Activation.h
#ifndef ACTIVATION_H
#define ACTIVATION_H

#include "Matrix.h"

// Insert Activation namespace here...
typedef Matrix (*activation_func)(Matrix);

namespace activation
{
//    typedef Matrix (*activation_func)(Matrix);
    Matrix softmax(Matrix A);
    Matrix relu(Matrix A);
}








#endif //ACTIVATION_H