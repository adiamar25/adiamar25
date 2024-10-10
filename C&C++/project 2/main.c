#include "sort_bus_lines.h"
#include "test_bus_lines.h"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#define USER_LINE 60
#define FIELD_LINE 21
#define LINES_ERROR "ERROR: the number of lines must contain only digits.\n"
#define NAME_ERROR "ERROR: bus name should contains only digits and small chars"
#define DISTANCE_ERROR "ERROR: distance should be an integer between 0 and 1000"
#define DURATION_ERROR "ERROR: duration should be an integer between 10 and 100"

int is_valid_arr(BusLine *arr)
{
  if (arr == NULL)
  {
    printf ("Error: memory allocation failed.\n");
    return 0;
  }
  return 1;
}

void free_arr(BusLine *arr)
{
  free(arr);
  arr = NULL;
}

int lines_amount()
{
  int n;
  char l_amount[FIELD_LINE];
  fgets (l_amount, FIELD_LINE, stdin);
  for (int i = 0; i < 21; i++)
  {
    if (!isdigit (l_amount[i]))
    {
      printf("%s", LINES_ERROR);
    }
  }
  sscanf (l_amount, "%d", &n);
  return n;
}

int is_valid_name(const char *name)
{
  for (int i = 0; name[i] != '\0'; i++)
  {
    if (!isdigit (name[i]) && (name[i] <'a' || name[i] > 'z'))
    {
      return 0;
    }
  }
  return 1;
}

int is_valid_distance(char *distance)
{
  for (int i = 0; distance[i] != '\0'; i++)
  {
    if (!isdigit (distance[i]))
    {
      return 0;
    }
  }
  long int dist = strtol (distance, NULL, 10);
  if (dist < 0 || dist > 1000)
  {
    return 0;
  }
  return 1;
}

int is_valid_duration(char *duration)
{
  for (int i = 0; duration[i] != '\0'; i++)
  {
    if (!isdigit (duration[i]))
    {
      return 0;
    }
  }
  long int dist = strtol (duration, NULL, 10);
  if (dist < 10 || dist > 100)
  {
    return 0;
  }
  return 1;
}

void get_lines_details(int n, BusLine* bus_lines_arr)
{
  char cur_line[USER_LINE];
  char l_name[FIELD_LINE];
  char l_dist[FIELD_LINE];
  char l_duration[FIELD_LINE];

  int i = 0;
  while (i < n)
  {
    printf("Enter line info. Then enter\n");
    fgets (cur_line, USER_LINE, stdin);
    sscanf (cur_line, "%[^,],%[^,],%s", l_name, l_dist, l_duration);
    while (!is_valid_name (l_name) ||
           !is_valid_distance (l_dist) ||
           !is_valid_duration (l_duration))
    {
      if (!is_valid_name (l_name))
      {
        printf ("%s\n", NAME_ERROR);
      }
      else if (!is_valid_distance (l_dist))
      {
        printf ("%s\n", DISTANCE_ERROR);
      }
      else if (!is_valid_duration (l_duration))
      {
        printf ("%s\n", DURATION_ERROR);
      }
      fgets (cur_line, USER_LINE, stdin);
      sscanf (cur_line, "%[^,],%[^,],%s", l_name, l_dist, l_duration);
    }
    int dist = strtol (l_dist, NULL, 10);
    int dur = strtol (l_duration, NULL, 10);
    strcpy ((bus_lines_arr+i) -> name, l_name);
    (bus_lines_arr+i) -> distance = dist;
    (bus_lines_arr+i) -> duration = dur;
    i++;
  }
}

void distance_tests(BusLine *start_sorted,
                  BusLine *end_sorted,
                  BusLine *start_org,
                  BusLine *end_org)
{
  if (is_sorted_by_distance(start_sorted, end_sorted))
  {
    printf("TEST 1 PASSED: Sorted properly by distance.\n");
  }
  else
  {
    printf("TEST 1 FAILED: Not sorted properly by distance.\n");
  }
  if (is_equal (start_sorted, end_sorted, start_org, end_org))
  {
    printf("TEST 2 PASSED: the arrays are equal.\n");
  }
  else
  {
    printf("TEST 2 FAILED: the arrays are not equal.\n");
  }
}

void duration_tests(BusLine *start_sorted,
                   BusLine *end_sorted,
                   BusLine *start_org,
                   BusLine *end_org)
{
  if (is_sorted_by_duration(start_sorted, end_sorted))
  {
    printf("TEST 3 PASSED: Sorted properly by duration.\n");
  }
  else
  {
    printf("TEST 3 FAILED: Not sorted properly by duration.\n");
  }
  if (is_equal (start_sorted, end_sorted, start_org, end_org))
  {
    printf("TEST 4 PASSED: the arrays are equal.\n");
  }
  else
  {
    printf("TEST 4 FAILED: the arrays are not equal.\n");
  }
}

void name_tests(BusLine *start_sorted,
                   BusLine *end_sorted,
                   BusLine *start_org,
                   BusLine *end_org)
{
  if (is_sorted_by_name(start_sorted, end_sorted))
  {
    printf("TEST 5 PASSED: Sorted properly by name.\n");
  }
  else
  {
    printf("TEST 5 FAILED: Not sorted properly by name.\n");
  }
  if (is_equal (start_sorted, end_sorted, start_org, end_org))
  {
    printf("TEST 6 PASSED: the arrays are equal.\n");
  }
  else
  {
    printf("TEST 6 FAILED: the arrays are not equal.\n");
  }
}

int tester(BusLine *start_org, BusLine *end_org)
{
  int lines_number = lines_amount();
  BusLine *lines_arr_copy = calloc (lines_number, sizeof (BusLine));
  if (!is_valid_arr (lines_arr_copy))
  {
    free_arr (lines_arr_copy);
    return 0;
  }
  memcpy (lines_arr_copy, start_org, lines_number * sizeof (BusLine));
  quick_sort (lines_arr_copy, lines_arr_copy+lines_number, DISTANCE);
  distance_tests (lines_arr_copy, lines_arr_copy+lines_number, start_org, end_org);
  quick_sort (lines_arr_copy, lines_arr_copy+lines_number, DURATION);
  duration_tests (lines_arr_copy, lines_arr_copy+lines_number, start_org, end_org);
  bubble_sort (lines_arr_copy, lines_arr_copy+lines_number);
  name_tests(lines_arr_copy, lines_arr_copy+lines_number, start_org, end_org);
  free_arr (lines_arr_copy);
  return 1;
}

void print_lines(BusLine *start, BusLine *end)
{
  for (BusLine *k = start; k <= end-1; k++)
  {
    printf("%s %d %d\n",k->name, k->distance, k->duration);
  }
}


/**
 * TODO add documentation
 */
int main (int argc, char *argv[])
{
  if (argc != 2)
  {
    printf ("USAGE: INCORRECT COMMAND\n");
    return EXIT_FAILURE;
  }
  // getting the amount of lines that arrive
  // to the university from the station.
  printf ("Enter number of lines. Then enter\n");
  int lines_number = lines_amount();
  // getting the details of the lines (name, distance, duration).
  BusLine *lines_arr = calloc (lines_number, sizeof (BusLine));
  if (!is_valid_arr (lines_arr))
  {
    free_arr (lines_arr);
    return EXIT_FAILURE;
  }
  get_lines_details(lines_number, lines_arr);
  if (strcmp (argv[1], "by_distance") == 0)
  {
    quick_sort(lines_arr, lines_arr + lines_number, DISTANCE);
  }
  if (strcmp (argv[1], "by_duration") == 0)
  {
    quick_sort(lines_arr, lines_arr + lines_number, DURATION);
  }
  if (strcmp (argv[1], "by_name") == 0)
  {
    bubble_sort (lines_arr, lines_arr + lines_number);
  }
  if (strcmp (argv[1], "test") == 0)
  {
    int worked = tester (lines_arr, lines_arr+lines_number);
    if (!worked)
    {
      return EXIT_FAILURE;
    }
  }
  print_lines (lines_arr, lines_arr + lines_number);
  return EXIT_SUCCESS;
}


//BusLine line1 = {"28", 13, 18};
//BusLine line2 = {"22", 18, 13};
//BusLine line3 = {"31", 2, 24};
//BusLine line4 = {"42", 20, 10};
//BusLine line5 = {"15", 6, 2};
//BusLine line6 = {"45", 12, 5};
//BusLine lines_arr[5] = {line1, line2, line3, line4, line5};
//BusLine saved_arr[5];
//BusLine new_arr[5] = {line2, line3, line4, line6, line5};
//memcpy (saved_arr, lines_arr, 5 * sizeof (BusLine));
//quick_sort (lines_arr, lines_arr+5, DISTANCE);
//int res1 = is_equal (lines_arr, lines_arr+5, saved_arr, saved_arr+5);
//printf("%d\n", res1);
//bubble_sort (lines_arr, lines_arr+5);
//int res2 = is_equal (lines_arr, lines_arr+5, saved_arr, saved_arr+5);
//printf("%d\n", res2);
//quick_sort (lines_arr, lines_arr+5, DURATION);
//int res3 = is_equal (lines_arr, lines_arr+5, saved_arr, saved_arr+5);
//printf("%d\n", res3);
//int res4 = is_equal(lines_arr, lines_arr+4, new_arr, new_arr+4);
//printf("%d", res4);
