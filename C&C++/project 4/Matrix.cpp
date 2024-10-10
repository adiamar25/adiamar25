
#include "Matrix.h"
#include <iostream>

#define NUM01 0.1


Matrix::Matrix (int rows, int cols) : _rows(rows),
                                      _cols(cols)
{
  if (_rows <= 0 || _cols <= 0)
  {
    throw std::exception();
  }

  mat = new float[_rows * _cols];
  for (int i = 0; i < _cols * _rows; ++i)
  {
    mat[i] = 0;
  }
}

Matrix::Matrix () : _rows(1), _cols(1)
{
  mat = new float[1];
  mat[0] = 0;
}

Matrix::Matrix(const Matrix& M) : _rows(M._rows), _cols(M._cols)
{
  mat = new float[_rows * _cols];
  for (int i = 0; i < _rows * _cols; ++i)
  {
    mat[i] = M[i];
  }
}

Matrix::~Matrix()
{
  delete[] mat;
}

int Matrix::get_rows() const
{
  return _rows;
}

int Matrix::get_cols() const
{
  return _cols;
}

Matrix& Matrix::transpose()
{
  Matrix temp(_rows, _cols);
  for (int i = 0; i < _cols * _rows; ++i)
  {
    temp.mat[i] = mat[i];
  }

  int rows_num = _rows;
  _rows = _cols;
  _cols = rows_num;

  for (int i = 0; i < temp._rows; ++i)
  {
    for (int j = 0; j < temp._cols; ++j)
    {
      mat[j*_cols + i] = temp(i, j);
    }
  }

  return *this;
}

Matrix& Matrix::vectorize()
{
  _rows = _rows * _cols;
  _cols = 1;
  return *this;
}

void Matrix::plain_print ()
{
  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      std::cout << (*this)(i, j) << " ";
    }
    std::cout << std::endl;
  }
}

Matrix Matrix::dot (const Matrix& M) const
{
  if (_rows != M._rows || _cols != M._cols)
  {
    throw std::exception();
  }

  Matrix dot_mat(_rows, _cols);
  for (int i = 0; i < _rows * _cols; ++i)
  {
    dot_mat[i] = mat[i] * M[i];
  }

  return dot_mat;
}

float Matrix::norm () const
{
  float sum = 0;
  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      sum += (*this)(i, j) * (*this)(i, j);
    }
  }

  return sqrtf(sum);
}

int Matrix::argmax() const
{
  int ind = 0;
  float max_num = mat[0];

  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      if ((*this)(i, j) > max_num)
      {
        max_num = (*this)(i, j);
        ind = i*_cols + j;
      }
    }
  }

  return ind;
}

Matrix Matrix::rref() const
{
  Matrix ref_mat(*this);
  int lead_elem = 0, row_count = ref_mat._rows, col_count = ref_mat._cols;
  for (int r = 0; r < row_count; r++)
  {
    if (col_count <= lead_elem)
    {
      break;
    }
    int i = r;
    while (ref_mat(i, lead_elem) == 0){
      i++;
      if (row_count == i)
      {
        i = r;
        lead_elem++;
        if (col_count == lead_elem)
        {
          break;
        }
      }
    }
    if (lead_elem < col_count){
      for (int j = 0; j < col_count; j++)
      {
        std::swap(ref_mat(r, j), ref_mat(i, j));
      }
      float div = ref_mat(r, lead_elem);
      if (div != 0){
        for (int j = 0; j < col_count; j++)
        {
          ref_mat(r, j) = ref_mat(r, j) / div;
        }
      }
      for (int j = 0; j < row_count; j++)
      {
        if (j != r)
        {
          float mult = ref_mat(j, lead_elem);
          for (int k = 0; k < col_count; k++)
          {
            ref_mat(j, k) -= mult * ref_mat(r, k);
          }
        }
      }
    }
    lead_elem++;
  }
  return ref_mat;
}

float Matrix::sum () const
{
  float sum = 0;

  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      sum += (*this)(i, j);
    }
  }

  return sum;
}

Matrix& Matrix::operator+= (const Matrix &B)
{
  if (_rows != B._rows || _cols != B._cols)
  {
    throw std::exception();
  }

  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      mat[i*_cols + j] += B(i, j);
    }
  }

  return *this;
}

Matrix Matrix::operator+ (const Matrix& B) const
{
  if (_rows != B._rows || _cols != B._cols)
  {
    throw std::exception();
  }

  Matrix sum(_rows, _cols);
  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < _cols; ++j)
    {
      sum(i, j) = (*this)(i, j) + B(i, j);
    }
  }

  return sum;
}

Matrix Matrix::operator* (const Matrix& B) const
{
  if (_cols != B._rows)
  {
    throw std::exception();
  }

  Matrix product_mat(_rows, B._cols);
  for (int i = 0; i < _rows; ++i)
  {
    for (int j = 0; j < B._cols; ++j)
    {
      for (int k = 0; k < _cols; ++k)
      {
        product_mat(i, j) += ((*this)(i, k) * B(k, j));
      }
    }
  }

  return product_mat;
}

Matrix Matrix::operator* (float c) const
{
  Matrix product_mat(_rows, _cols);

  for (int i = 0; i < _rows * _cols; ++i)
  {
    product_mat.mat[i] = mat[i] * c;
  }

  return product_mat;
}

Matrix operator* (float c, const Matrix& A)
{
  Matrix product_mat(A._rows, A._cols);

  for (int i = 0; i < product_mat._rows * product_mat._cols; ++i)
  {
    product_mat.mat[i] = A.mat[i] * c;
  }

  return product_mat;
}

float& Matrix::operator() (int i, int j)
{
  if (i < 0 || j < 0 || i >= _rows || j >= _cols)
  {
    throw std::exception();
  }

  return mat[i*_cols + j];
}

float Matrix::operator() (int i, int j) const
{
  if (i < 0 || j < 0 || i >= _rows || j >= _cols)
  {
    throw std::exception();
  }

  return mat[i*_cols + j];
}

float& Matrix::operator[] (int k)
{
  if (k < 0 || k >= _rows * _cols)
  {
    throw std::exception();
  }

  return mat[k];
}

float Matrix::operator[] (int k) const
{
  if (k < 0 || k >= _rows * _cols)
  {
    throw std::exception();
  }

  return mat[k];
}

Matrix& Matrix::operator= (const Matrix& B)
{
  if (this == &B)
  {
    return *this;
  }

  if (_rows != B._rows || _cols != B._cols)
  {
    delete[] mat;
    _rows = B._rows;
    _cols = B._cols;
    mat = new float[_rows * _cols];
  }

  for (int i = 0; i < _rows * _cols; ++i)
  {
    mat[i] = B[i];
  }

  return *this;
}

std::ostream& operator<< (std::ostream &os, const Matrix& A)
{
  for (int i = 0; i < A._rows; ++i)
  {
    for (int j = 0; j < A._cols; ++j)
    {
      if (A(i, j) > NUM01)
      {
        os << "**";
      }
      else
      {
        os << "  ";
      }
    }
    os << std::endl;
  }

  return os;
}

std::istream& operator>> (std::istream& is, const Matrix& A)
{
  int size_to_read = (int)sizeof (float) * A._rows * A._cols;
  is.read ((char*)A.mat, size_to_read);

  if (is.fail())
  {
    throw std::exception();
  }

  return is;
}
