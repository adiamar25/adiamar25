#include "cipher.h"
#include "tests.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_LINE 1025
#define NUM_5 5
#define NUM_2 2
#define NUM_10 10


int is_k_int (const char k[])
{
  char first_char = k[0];
  for (int i = 0; k[i] != '\0'; ++i)
  {
    if (!isdigit (k[i]))
    {
      if (!(i == 0 && strcmp("-", &first_char) == 0))
      {
        return 0;
      }
    }
  }
  return 1;
}

int is_ok_file(char input_path[])
{
  FILE *f = fopen (input_path, "r");
  if (f == NULL)
  {
    return 0;
  }
  fclose (f);
  return 1;
}

void call_encode(char input_path[], char output_path[], int k)
{
  FILE *input_file = fopen (input_path, "r");
  FILE *output_file = fopen(output_path, "w");
  char line[MAX_LINE];
  while (fgets (line, MAX_LINE, input_file))
  {
    encode (line, k);
    if (output_file)
    {
      fputs (line, output_file);
    }
  }
  fclose (input_file);
  if (output_file)
  {
    fclose (output_file);
  }
}

void call_decode(char input_path[], char output_path[], int k)
{
  FILE *input_file = fopen (input_path, "r");
  FILE *output_file = fopen(output_path, "w");
  char line[MAX_LINE];
  while (fgets (line, MAX_LINE, input_file))
  {
    decode (line, k);
    if (output_file)
    {
      fputs (line, output_file);
    }
  }
  fclose (input_file);
  if (output_file)
  {
    fclose (output_file);
  }
}

int run_tests()
{
  if (
      test_encode_non_cyclic_lower_case_positive_k () == 0 &&
      test_encode_cyclic_lower_case_special_char_positive_k () == 0 &&
      test_encode_non_cyclic_lower_case_special_char_negative_k () == 0 &&
      test_encode_cyclic_lower_case_negative_k () == 0 &&
      test_encode_cyclic_upper_case_positive_k () == 0 &&
      test_decode_non_cyclic_lower_case_positive_k () == 0 &&
      test_decode_cyclic_lower_case_special_char_positive_k () == 0 &&
      test_decode_non_cyclic_lower_case_special_char_negative_k () == 0 &&
      test_decode_cyclic_lower_case_negative_k () == 0 &&
      test_decode_cyclic_upper_case_positive_k () == 0)
  {
    return EXIT_SUCCESS;
  }
  return EXIT_FAILURE;
}


int main (int argc, char *argv[])
{
  if (argc != NUM_2 && argc != NUM_5)
  {
    fprintf (stderr, "The program receives 1 or 4 arguments only.\n");
    return EXIT_FAILURE;
  }
  if (argc == NUM_5)
  {
    if (strcmp(argv[1], "encode") != 0 && strcmp(argv[1], "decode") != 0)
    {
      fprintf (stderr, "The given command is invalid.\n");
      return EXIT_FAILURE;
    }
    if(is_k_int (argv[NUM_2]) == 0)
    {
      fprintf (stderr, "The given shift value is invalid.\n");
      return EXIT_FAILURE;
    }
    if (is_ok_file (argv[3]) == 0)
    {
      fprintf (stderr, "The given file is invalid.\n");
      return EXIT_FAILURE;
    }
    long k = strtol(argv[NUM_2], NULL, NUM_10);
    if (strcmp ("encode", argv[1]) == 0)
    {
      call_encode (argv[3], argv[4], k);
    }
    else
    {
      call_decode (argv[3], argv[4], k);
    }
    if (is_ok_file(argv[4]))
    {
      return EXIT_SUCCESS;
    }
    fprintf (stderr, "The given file is invalid.\n");
    return EXIT_FAILURE;
  }
  else
  {
    if (strcmp("test", argv[1]) != 0)
    {
      fprintf(stderr, "Usage: cipher test\n");
      return EXIT_FAILURE;
    }
    return run_tests();
  }
}