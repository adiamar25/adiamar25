// Matrix.h
#ifndef MATRIX_H
#define MATRIX_H

#include <iostream>
#include <cmath>


// You don't have to use the struct. Can help you with MlpNetwork.h
struct matrix_dims {
    int rows, cols;
};

float** alloc_matrix(float** mat, int rows, int cols);


// Insert Matrix class here...

class Matrix
{
 private:
  int _rows, _cols;
  float *mat;

 public:
  Matrix (int rows, int cols);
  Matrix ();
  Matrix (const Matrix &M);
  ~Matrix ();
  int get_rows () const;
  int get_cols () const;
  Matrix &transpose ();
  Matrix &vectorize ();
  void plain_print ();
  Matrix dot (const Matrix &M) const;
  float norm () const;
  int argmax () const;
  Matrix rref () const;
  float sum() const;
  float& operator[] (int k);
  float operator[] (int k) const;
  Matrix& operator= (const Matrix& B);
  Matrix& operator+= (const Matrix& B);
  Matrix operator+ (const Matrix& B) const;
  float& operator() (int i, int j);
  float operator() (int i, int j) const;
  Matrix operator* (const Matrix& B) const;
  Matrix operator* (float c) const;
  friend Matrix operator* (float c, const Matrix& A);
  friend std::ostream& operator<< (std::ostream& os, const Matrix &A);
  friend std::istream& operator>> (std::istream& is, const Matrix& A);
};

Matrix operator* (float c, const Matrix& A);
std::ostream& operator<< (std::ostream& os, const Matrix& A);
std::istream& operator>> (std::istream& is, const Matrix& A);




#endif //MATRIX_H