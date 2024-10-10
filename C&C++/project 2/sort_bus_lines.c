#include "sort_bus_lines.h"
#include <stdio.h>

void swap(BusLine *a, BusLine *b)
{
  BusLine temp = *a;
  *a = *b;
  *b = temp;
}

void bubble_sort (BusLine *start, BusLine *end)
{
  for (BusLine *i = start; i < end -1; i++)
  {
    for (BusLine *j = start; j < start+(end-i)-1; j++)
    {
      if (strcmp(j->name, (j+1)->name) > 0)
      {
        swap (j, j+1);
      }
    }
  }
}

void quick_sort_helper(BusLine *start, BusLine *end, SortType sort_type)
{
  if (start < end - 1)
  {
    BusLine *pivot = partition (start, end-1, sort_type);
    quick_sort_helper (start, pivot, sort_type);
    quick_sort_helper (pivot, end, sort_type);
  }
}

void quick_sort (BusLine *start, BusLine *end, SortType sort_type)
{
  quick_sort_helper (start, end, sort_type);
}

BusLine *partition (BusLine *start, BusLine *end, SortType sort_type)
{
  BusLine *i = start-1;
  int pivot;
  if (sort_type == DISTANCE)
  {
    pivot = end->distance;
    for (BusLine *j = start; j <= end-1; j++)
    {
      if ((j->distance) <= pivot)
      {
        i++;
        swap (i, j);
      }
    }
  }
  else
  {
    pivot = end->duration;
    for (BusLine  *j = start; j <= end-1; j++)
    {
      if ((j->duration) <= pivot)
      {
        i++;
        swap (i, j);
      }
    }
  }
  swap (i + 1, end);
  return i + 1;
}



