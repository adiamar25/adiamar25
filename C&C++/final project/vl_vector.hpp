#ifndef VL_VECTOR_HPP
#define VL_VECTOR_HPP

#include <iostream>
#include <iterator>
#include <cstddef>

// Class declarations
template<typename T, size_t static_capacity=16>
class vl_vector
{
 protected:
  // Usings
  using value_type = T;
  using size_type = std::size_t;
  using reference = value_type&;
  using const_reference = const value_type&;
  using pointer = value_type*;
  using const_pointer = const value_type*;
  using difference_type = std::ptrdiff_t;

  // Data Members
  size_type _capacity;
  size_type _size;
  T _static_vec[static_capacity];
  T* _dynamic_vec;

 public:
  // Forward Declarations
  class const_iterator;

  // Iterator
  class iterator
  {
   public:
    // Usings
    using iterator_category = std::random_access_iterator_tag;
    using value_type = typename vl_vector<T, static_capacity>::value_type;
    using pointer = typename vl_vector<T, static_capacity>::pointer;
    using reference = typename vl_vector<T, static_capacity>::reference;
    using difference_type = std::ptrdiff_t;
    using vector_ptr = vl_vector<T, static_capacity>*;

    // Constructors
    inline iterator() : _vl_vector_ptr(nullptr), _index(0) {}
    inline explicit iterator(vector_ptr vl_vector_ptr) :
      _vl_vector_ptr(vl_vector_ptr), _index(0) {}
    inline explicit iterator(vector_ptr vl_vector_ptr, int index) :
      _vl_vector_ptr(vl_vector_ptr), _index(index) {}

    // Copy Constructor
    inline iterator(const iterator& other) :
      _vl_vector_ptr(other._vl_vector_ptr),
      _index(other._index) {}

    // Operator Assignments
    inline iterator& operator=(const iterator& other)
    {
      _vl_vector_ptr = other._vl_vector_ptr;
      _index = other._index;

      return *this;
    }

    inline iterator& operator=(const const_iterator& other)
    {
      _vl_vector_ptr = other._vl_vector_ptr;
      _index = other._index;

      return *this;
    }

    // Destructor
    ~iterator() = default;

    // Casting Operators
    inline explicit operator const_iterator() const
    {
      return const_iterator(_vl_vector_ptr, _index);
    }

    // Indexing methods
    inline reference operator*() const
    {
        if (_vl_vector_ptr == nullptr)
        {
          throw std::logic_error("Bad Iterator!");
        }

        return  *(_vl_vector_ptr->data() + _index);
    }

    inline pointer operator->() { return (_vl_vector_ptr->data() + _index); };

    // Operators
    inline iterator operator+(size_t steps) const
    {
      return iterator(_vl_vector_ptr, _index + steps);
    }

    inline iterator operator-(size_t steps) const
    {
      return iterator(_vl_vector_ptr, _index - steps);
    }

    inline difference_type operator-(const iterator& other) const
    {
      return static_cast<difference_type>(other._index - _index);
    }

    inline iterator& operator++()
    {
      _index++;

      return *this;
    }

    inline iterator operator++(int)
    {
      iterator tmp = *this;
      ++(*this);

      return tmp;
    }

    inline iterator& operator--()
    {
      _index--;

      return *this;
    }

    inline iterator operator--(int)
    {
      iterator tmp = *this;
      --(*this);

      return tmp;
    }

    // Comparison Operators
    friend inline bool operator== (const iterator& lhs, const iterator& rhs)
    {
      return (*lhs._vl_vector_ptr == *rhs._vl_vector_ptr &&
              lhs._index == rhs._index);
    }

    friend inline bool operator!= (const iterator& lhs, const iterator& rhs)
    {
      return (*lhs._vl_vector_ptr != *rhs._vl_vector_ptr ||
              lhs._index != rhs._index);
    }

   private:
    // Data Members
    vector_ptr _vl_vector_ptr;
    int _index;
  };

    // Const Iterator
  class const_iterator
  {
   public:
    // Usings
    using iterator_category = std::random_access_iterator_tag;
    using value_type = typename vl_vector<T, static_capacity>::value_type;
    using pointer = typename vl_vector<T, static_capacity>::const_pointer;
    using reference = typename vl_vector<T, static_capacity>::const_reference;
    using difference_type = std::ptrdiff_t;
    using vector_ptr = const vl_vector<T, static_capacity>*;

    // Constructors
    inline const_iterator() : _vl_vector_ptr(nullptr), _index(0) {}
    inline explicit const_iterator(vector_ptr vl_vector_ptr, int index) :
      _vl_vector_ptr(vl_vector_ptr), _index(index) {}
    inline explicit const_iterator(vector_ptr vl_vector_ptr) :
      _vl_vector_ptr(vl_vector_ptr), _index(0) {}

    // Copy Constructor
    inline const_iterator(const const_iterator& other) :
        _vl_vector_ptr(other._vl_vector_ptr),
        _index(other._index) {}

    // Operator Assignments
    inline const_iterator& operator=(const const_iterator& other)
    {
      _vl_vector_ptr = other._vl_vector_ptr;
      _index = other._index;

      return *this;
    }

    inline const_iterator& operator=(const iterator& other)
    {
      _vl_vector_ptr = other._vl_vector_ptr;
      _index = other._index;

      return *this;
    }

    // Destructor
    ~const_iterator() = default;

    // Casting
    inline explicit operator iterator() const
    {
      return iterator(_vl_vector_ptr, _index);
    }

    // Indexing methods
    inline reference operator*() const
    {
      if (_vl_vector_ptr == nullptr)
      {
        throw std::logic_error("Bad Iterator!");
      }

      return *(_vl_vector_ptr->data() + _index);
    }

    inline pointer operator->() { return (_vl_vector_ptr->data() + _index); };

    // Operators
    inline const_iterator operator+(size_t steps) const
    {
      return const_iterator(_vl_vector_ptr, _index + steps);
    }

    inline const_iterator operator-(size_t steps) const
    {
      return const_iterator(_vl_vector_ptr, _index - steps);
    }

    inline difference_type operator-(const const_iterator& other) const
    {
      return static_cast<difference_type>(other._index - _index);
    }

    inline const_iterator& operator++()
    {
      _index++;

      return *this;
    }

    inline const_iterator operator++(int) const
    {
      const_iterator tmp = *this;
      ++(*this);

      return tmp;
    }

    inline const_iterator& operator--()
    {
      _index--;

      return *this;
    }

    inline const_iterator operator--(int) const
    {
      const_iterator tmp = *this;
      --(*this);

      return tmp;
    }

    // Comparison Operators
    friend inline bool operator== (const const_iterator& lhs,
                                   const const_iterator& rhs)
    {
      return (*lhs._vl_vector_ptr == *rhs._vl_vector_ptr &&
              lhs._index == rhs._index);
    }

    friend inline bool operator!= (const const_iterator& lhs,
                                   const const_iterator& rhs)
    {
      return (*lhs._vl_vector_ptr != *rhs._vl_vector_ptr ||
              lhs._index != rhs._index);
    }

   private:
    // Class Members
    vector_ptr _vl_vector_ptr;
    int _index;
  };

  //-------------------------------------------------------
  //  Constructors
  //-------------------------------------------------------

  // Default Constructor
  inline vl_vector() : _capacity(static_capacity),
                       _size(0),
                       _dynamic_vec(nullptr) {}

  // Copy Constructor
  inline vl_vector(const vl_vector<T, static_capacity>& other)
  {
    _capacity = other._capacity;
    _size = other._size;

    T* vec = _static_vec;
    _dynamic_vec = nullptr;

    // check if dynamic memory allocation is required
    if (other._capacity > static_capacity)
    {
      _dynamic_vec = new T[other._capacity];
      vec = _dynamic_vec;
    }

    for (size_t i = 0; i < other._size; ++i)
    {
      vec[i] = other[i];
    }
  }

  // Single-value initialized Constructor
  inline vl_vector(T v, size_t count)
  {
    _capacity = count <= static_capacity
                  ? static_capacity
                  : static_cast<size_t>(static_cast<double>(count) * 1.5);
    _size = count;

    T* vec = _static_vec;
    _dynamic_vec = nullptr;

    // check if dynamic memory allocation is required
    if (_capacity > static_capacity)
    {
      _dynamic_vec = new T[_capacity];
      vec = _dynamic_vec;
    }

    for (int i = 0; i < count; ++i)
    {
      vec[i] = v;
    }
  }

  // Sequence Based Constructor
  template<class ForwardIterator>
  inline vl_vector(const ForwardIterator& first, const ForwardIterator& last)
  {
    _size = std::abs(std::distance(first, last));
    _capacity = _size <= static_capacity
        ? static_capacity
        : static_cast<size_t>(static_cast<double>(_size) * 1.5);

    T* vec = _static_vec;
    _dynamic_vec = nullptr;

    if (_capacity > static_capacity)
    {
      _dynamic_vec = new T[_capacity];
      vec = _dynamic_vec;
    }

    int i = 0;
    for (auto iter = first; iter != last; ++iter)
    {
      vec[i++] = *iter;
    }
  }

  // Initializer Constructor
  inline vl_vector(std::initializer_list<value_type> initializer_list)
  {
    T* vec = _static_vec;
    _dynamic_vec = nullptr;
    _size = initializer_list.size();
    _capacity = _size <= static_capacity
        ? static_capacity
        : static_cast<size_t>(static_cast<double>(_size) * 1.5);

    // check if dynamic memory allocation is required
    if (_capacity > static_capacity)
    {
      _dynamic_vec = new T[_capacity];
      vec = _dynamic_vec;
    }
    else
    {
      _dynamic_vec = nullptr;
    }

    std::move(initializer_list.begin(), initializer_list.end(), vec);
  }

  // Destructor
  inline ~vl_vector()
  {
    delete[] _dynamic_vec;
  }


  //-------------------------------------------------------
  //  Operators
  //-------------------------------------------------------

  // Operator Assignment
  inline vl_vector<T, static_capacity>& operator=(const vl_vector& other)
  {
    if (this != &other)
    {
      T *vec = _static_vec;
      _dynamic_vec = nullptr;

      if (other._capacity > static_capacity)
      {
        delete[] _dynamic_vec;
        _dynamic_vec = new T[other._capacity];
        vec = _dynamic_vec;
      }

      for (size_t i = 0; i < other._size; ++i)
      {
        vec[i] = other[i];
      }

      _capacity = other._capacity;
      _size = other._size;
    }

    return *this;
  }

  // Operator Subscript
  inline reference operator[](int index) { return *(data() + index); }

  inline const_reference operator[](int index) const
  {
    return *(data() + index);
  }

  // Operator Comparison
  inline bool operator==(const vl_vector& other)
  {
    bool is_equal = ((_size == other._size) &&
                     (_capacity == other._capacity));

    if (is_equal)
    {
      T* vec = (_capacity > static_capacity) ? _dynamic_vec : _static_vec;
      const T* other_vec = (_capacity > static_capacity)
          ? other._dynamic_vec : other._static_vec;

      for (size_t i = 0 ; i < _size; i++)
      {
        if (vec[i] != other_vec[i])
        {
          is_equal = false;
        }
      }
    }

    return is_equal;
  }

  inline bool operator!=(const vl_vector& other)
  {
    return !(*this == other);
  }


  //-------------------------------------------------------
  //  Methods
  //-------------------------------------------------------
  inline size_type size() const { return _size; }
  inline size_type capacity() const { return _capacity; }
  inline bool empty() const { return (_size == 0); }

  inline reference at(const size_type& index)
  {
    if (index >= _size)
    {
      throw std::out_of_range("Invalid index");
    }

    return *(begin() + index);
  }

  inline const_reference at(const size_type& index) const
  {
    if (index >= _size)
    {
      throw std::out_of_range("Invalid index");
    }

    return *(begin() + index);
  }

  inline void push_back(const value_type& element)
  {
    bool is_static = (_capacity == static_capacity);

    if (_size == _capacity)  // Move to heap case
    {
      _capacity = cap_c (_size, 1);
      T* new_vec = new T[_capacity];

      for (size_t i = 0; i < _size; ++i)
      {
        new_vec[i] = at(i);
      }

      delete[] _dynamic_vec;
      _dynamic_vec = new_vec;
      is_static = false;
    }

    if (is_static)
    {
      _static_vec[_size] = element;
    }
    else
    {
      _dynamic_vec[_size] = element;
    }

    ++_size;
  }

  inline iterator insert(iterator position, const value_type& new_elem)
  {
    _capacity = cap_c (_size, 1);

    if (_capacity == static_capacity)  // The vector is always in the stack
    {
      for (iterator it = end(); it != position; --it)
      {
        *it = *(it - 1);
      }

      *position = new_elem;
    }
    else   // Heap case
    {
      const int ind = std::abs(std::distance (position, begin()));
      T* new_vec = new T[_capacity];

      for (int i = 0; i < ind; ++i)
      {
        new_vec[i] = this->at(i);
      }

      new_vec[ind] = new_elem;

      for (size_t i = ind; i < _size; ++i)
      {
        new_vec[i+1] = this->at(i);
      }

      delete[] _dynamic_vec;
      _dynamic_vec = new_vec;
    }

    ++_size;

    return position;
  }

  template<class ForwardIterator>
  inline iterator insert(iterator position,
                         const ForwardIterator& first,
                         const ForwardIterator& last)
  {
    const int elem_num = std::abs(std::distance (first, last));
    _capacity = cap_c (_size, elem_num);

    if (_capacity <= static_capacity)  // The vector is always in the stack
    {
      for (iterator it = end() + elem_num;
           it != (position + elem_num - 1);
           --it)
      {
        *it = *(it - elem_num);
      }

      for (int i = 0; i < elem_num; ++i)
      {
        *(position + i) = *(first + i);
      }
    }
    else   // Heap case
    {
      const int ind = std::abs(std::distance (position, begin()));
      T* new_vec = new T[_capacity];

      for (int i = 0; i < ind; ++i)
      {
        new_vec[i] = at(i);
      }

      for (size_t i = ind; i < _size; ++i)
      {
        new_vec[i + elem_num] = at (i);
      }

      for (int i = 0; i < elem_num; ++i)
      {
        new_vec[ind + i] = *(first + i);
      }

      delete[] _dynamic_vec;
      _dynamic_vec = new_vec;
    }

    _size += elem_num;

    return position;
  }

  inline void pop_back()
  {
    if (_size > 0)
    {
      if (_size - 1 == static_capacity)
      {
        for (size_t i = 0; i < _size - 1; ++i)
        {
          _static_vec[i] = _dynamic_vec[i];
        }

        delete[] _dynamic_vec;
        _dynamic_vec = nullptr;
        _capacity = static_capacity;
      }

      --_size;
    }
  }

  inline iterator erase(iterator position)
  {
    // Move the vector from the heap to the stack
    if (_size - 1 == static_capacity)
    {
      _capacity = static_capacity;
      const size_t ind = std::abs(std::distance (position, begin()));

      for (size_t i = 0; i < _size - 1; ++i)
      {
        if (i < ind)
        {
          _static_vec[i] = at (i);
        }
        else
        {
          _static_vec[i] = at (i + 1);
        }
      }

      delete[] _dynamic_vec;
      _dynamic_vec = nullptr;
    }
    else
    {
      for (iterator it = position; it != end() - 1; ++it)
      {
        *it = *(it + 1);
      }
    }

    --_size;

    return position;
  }

  inline iterator erase(iterator first, iterator last)
  {
    const int elem_num = std::abs(std::distance (last, first));

    if (_size - elem_num <= static_capacity)
    {
      const int ind = std::abs(std::distance (first, begin()));

      for (size_t i = 0; i < _size - elem_num; ++i)
      {
        if (i < ind)
        {
          _static_vec[i] = at(i);
        }
        else
        {
          _static_vec[i] = at(i + elem_num);
        }
      }

      _capacity = static_capacity;
      delete[] _dynamic_vec;
      _dynamic_vec = nullptr;
    }
    else
    {
      for (iterator it = first; it != end() - elem_num; ++it)
      {
        *it = *(it + elem_num);
      }
    }

    _size -= elem_num;

    return first;
  }

  void clear()
  {
    if (_size != 0)
    {
      delete[] _dynamic_vec;
      _dynamic_vec = nullptr;
      _size = 0;
      _capacity = static_capacity;
    }
  }

  inline T* data()
  {
    return ((_capacity <= static_capacity ||
             !_dynamic_vec) ? _static_vec : _dynamic_vec);
  }

  inline const T* data() const
  {
    return ((_capacity <= static_capacity ||
             !_dynamic_vec) ? _static_vec : _dynamic_vec);
  }

  inline size_t cap_c(size_t size, size_t k)
  {
    int new_cap;
    if (size + k <= _capacity)
    {
      new_cap = _capacity;
    }
    else
    {
      new_cap = int(1.5 * ((double)(size + k)));
    }

    return new_cap;
  }

  // Iterators Methods

  // Iterator Types Usings
  using reverse_iterator       = std::reverse_iterator<iterator>;
  using const_reverse_iterator = std::reverse_iterator<const_iterator>;

  // Iterator Methods
  inline iterator begin() { return iterator(this, 0); }
  inline iterator end() { return iterator(this, _size); }
  inline const_iterator begin() const { return const_iterator(this, 0); }
  inline const_iterator end() const { return const_iterator(this, _size); }

  // Const Iterator Methods
  inline const_iterator cbegin() const { return const_iterator(this, 0); }
  inline const_iterator cend() const { return const_iterator(this, _size); }

  // Reverse Iterator Methods
  inline reverse_iterator rbegin() { return reverse_iterator(end()); }
  inline reverse_iterator rend() { return reverse_iterator(begin()); }

  inline const_reverse_iterator rbegin() const
  {
    return const_reverse_iterator(end());
  }

  inline const_reverse_iterator rend() const
  {
    return const_reverse_iterator(begin());
  }

  // Const Reverse Iterator Methods
  inline const_reverse_iterator crbegin() const
  {
    return const_reverse_iterator(cend());
  }

  inline const_reverse_iterator crend() const {
    return const_reverse_iterator(cbegin());
  }

};


#endif // VL_VECTOR_HPP