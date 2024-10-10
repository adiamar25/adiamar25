#ifndef _VL_STRING_HPP_
#define _VL_STRING_HPP_

# include <iostream>
#include "vl_vector.hpp"

template<size_t StaticCapacity=16>
class vl_string : public vl_vector<char, StaticCapacity>
{
 public:
  //-------------------------------------------------------
  //  Constructors
  //-------------------------------------------------------

  // Default Constructor
  inline vl_string() : vl_vector<char, StaticCapacity>() {}

  // Copy Constructor
  inline vl_string(const vl_string<StaticCapacity>& other) :
    vl_vector<char, StaticCapacity>(other) {}

  // Implicit Constructor
  inline vl_string(const char* str)
  {
    this->_size = static_cast<size_t>(strlen(str));
    this->_capacity = this->_size <= StaticCapacity
        ? StaticCapacity
        : static_cast<int>(this->_size * 1.5);

    char* vec = this->_static_vec;
    this->_dynamic_vec = nullptr;

    // check if dynamic memory allocation is required
    if (this->_capacity > StaticCapacity)
    {
      this->_dynamic_vec = new char[this->_capacity];
      vec = this->_dynamic_vec;
    }

    for (size_t i = 0; i < this->_size; ++i)
    {
      vec[i] = str[i];
    }
  }

  // Destructor
  ~vl_string() = default;

  // Methods
  inline void append(const char* str)
  {
    vl_string<StaticCapacity> string(str);
    this->insert (this->end(), string.begin(), string.end());
  }

  //-------------------------------------------------------
  //  Operators
  //-------------------------------------------------------

  inline vl_string& operator+=(const char c)
  {
    this->push_back(c);

    return *this;
  }

  inline vl_string& operator+=(const char* str)
  {
    append(str);

    return *this;
  }

  template<size_t otherCapacity=16>
  inline vl_string& operator+=(const vl_vector<char, otherCapacity>& vl)
  {
    this->insert(this->end(), vl.begin(), vl.end());

    return *this;
  }

  inline vl_string operator+(const char c)
  {
    vl_string<StaticCapacity> string(*this);
    string.push_back (c);

    return string;
  }

  inline vl_string operator+(const char* str)
  {
    vl_string<StaticCapacity> string(*this);
    string.append (str);

    return string;
  }

  template<size_t otherCapacity=16>
  inline vl_string operator+(const vl_vector<char, otherCapacity>& vl)
  {
    vl_string<StaticCapacity> string(*this);
    string.insert(this->end(), vl.begin(), vl.end());

    return string;
  }

  // Implicit Casting Operator
  inline operator std::string() const
  {
    std::string str;

    if (this->_size > 0)
    {
      str = std::string(this->_size > StaticCapacity
          ? this->_dynamic_vec
          : this->_static_vec, this->_size);
    }

    return str;
  }

};


#endif //_VL_STRING_HPP_
