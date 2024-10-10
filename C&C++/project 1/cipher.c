#include "cipher.h"

#define SIZE_OF_ABC 26
#define LOWER_A_ASCII 97
#define LOWER_Z_ASCII 122
#define A_ASCII 65
#define Z_ASCII 90


/// IN THIS FILE, IMPLEMENT EVERY FUNCTION THAT'S DECLARED IN cipher.h.


void encode (char s[], int k)
{
  if (k >= SIZE_OF_ABC || k <= -SIZE_OF_ABC)
  {
    k = k%SIZE_OF_ABC;
  }

  for (int i = 0; s[i] != '\0'; ++i)
  {
    int cur_ascii = s[i];
    if (cur_ascii >= LOWER_A_ASCII && cur_ascii <= LOWER_Z_ASCII)
    {
      int new_ascii_val = cur_ascii + k;
      if (new_ascii_val < LOWER_A_ASCII)
      {
        new_ascii_val = LOWER_Z_ASCII + 1 - LOWER_A_ASCII%new_ascii_val;
      }
      else if(new_ascii_val > LOWER_Z_ASCII)
      {
        new_ascii_val = LOWER_A_ASCII - 1 + new_ascii_val%LOWER_Z_ASCII;
      }
      s[i] = new_ascii_val;
    }
    else if(cur_ascii >= A_ASCII && cur_ascii <= Z_ASCII)
    {
      int new_ascii_val = cur_ascii + k;
      if (new_ascii_val < A_ASCII)
      {
        new_ascii_val = Z_ASCII + 1 - A_ASCII%new_ascii_val;
      }
      else if(new_ascii_val > Z_ASCII){
        new_ascii_val = A_ASCII - 1 + new_ascii_val%Z_ASCII;
      }
      s[i] = new_ascii_val;
    }
  }
}

// See full documentation in header file
void decode (char s[], int k)
{
  encode(s, -k);
}
