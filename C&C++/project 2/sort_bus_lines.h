#ifndef EX2_REPO_SORTBUSLINES_H
#define EX2_REPO_SORTBUSLINES_H
// write only between #define EX2_REPO_SORTBUSLINES_H and #endif //EX2_REPO_SORTBUSLINES_H
#include <string.h>
#define NAME_LEN 21
/**
 * struct of BusLine. there are three fields in this struct:
 * name - a string which is no longer than 21 chars,
 * distance - the distance of the line from the university in kilometers,
 * duration - how long it takes to arrive the university in this line.
 */
typedef struct BusLine
{
    char name[NAME_LEN];
    int distance, duration;
} BusLine;
typedef enum SortType
{
    DISTANCE,
    DURATION
} SortType;

/**
 * this function gets a pointer to the start and the end of an array,
 * which all its elements are struct BusLine type,
 * and perform a bubble sort on the elements of the array,
 * as the sort process is done by the "name" field of the structs.
 * we compare elements in the algorithm using strcmp function.
 */
void bubble_sort (BusLine *start, BusLine *end);

/**
 *this function gets a pointer to the start and the end of an array,
 * which all its elements are struct BusLine type,
 * and an enum of type SortType,
 * and perform a quick sort on the elements of the array,
 * as the sort process is done by the "distance" field
 * or the "duration" field of the structs, depends on the sort_type argument.
 */
void quick_sort (BusLine *start, BusLine *end, SortType sort_type);

/**
 * this function is called only from the quick_sort function,
 * it gets the same arguments as the quick_sort function,
 * and perform the inside job of the quick_sort algorithm.
 */
BusLine *partition (BusLine *start, BusLine *end, SortType sort_type);
// write only between #define EX2_REPO_SORTBUSLINES_H and #endif //EX2_REPO_SORTBUSLINES_H
#endif //EX2_REPO_SORTBUSLINES_H
