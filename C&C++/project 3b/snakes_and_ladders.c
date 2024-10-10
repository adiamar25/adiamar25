#include <string.h> // For strlen(), strcmp(), strcpy()
#include "markov_chain.h"

#define MAX(X, Y) (((X) < (Y)) ? (Y) : (X))

#define EMPTY -1
#define BOARD_SIZE 100
#define MAX_GENERATION_LENGTH 60

#define DICE_MAX 6
#define NUM_OF_TRANSITIONS 20

#define NUM_1 1
#define NUM_2 2
#define NUM_3 3
#define NUM_10 10
#define NUM_100 100

/**
 * represents the transitions by ladders and snakes in the game
 * each tuple (x,y) represents a ladder from x to if x<y or a snake otherwise
 */
const int transitions[][2] = {{13, 4},
                              {85, 17},
                              {95, 67},
                              {97, 58},
                              {66, 89},
                              {87, 31},
                              {57, 83},
                              {91, 25},
                              {28, 50},
                              {35, 11},
                              {8,  30},
                              {41, 62},
                              {81, 43},
                              {69, 32},
                              {20, 39},
                              {33, 70},
                              {79, 99},
                              {23, 76},
                              {15, 47},
                              {61, 14}};

/**
 * struct represents a Cell in the game board
 */
typedef struct Cell {
    int number; // Cell number 1-100
    int ladder_to;  // ladder_to represents the jump of the
    // ladder in case there is one from this square
    int snake_to;  // snake_to represents the jump of
    // the snake in case there is one from this square
    //both ladder_to and snake_to should be -1 if the Cell doesn't have them
} Cell;

/** Error handler **/
static int handle_error(char *error_msg, MarkovChain **database)
{
    printf("%s", error_msg);
    if (database != NULL)
    {
        free_markov_chain(database);
    }
    return EXIT_FAILURE;
}

static void print_cell (void *cell)
{
  if (((Cell*)cell)->ladder_to == -1 && ((Cell*)cell)->snake_to == -1)
  {
    if (((Cell*)cell)->number == NUM_100)
    {
      printf ("[%d]", ((Cell*)cell)->number);
    }
    else
    {
      printf ("[%d] -> ", ((Cell*)cell)->number);
    }
  }
  else if (((Cell*)cell)->ladder_to != -1)
  {
    printf ("[%d]-ladder to %d -> ", ((Cell*)cell)->number,
                                             ((Cell*)cell)->ladder_to);
  }
  else  // snake_to != -1
  {
    printf ("[%d]-snake to %d -> ", ((Cell*)cell)->number,
                                            ((Cell*)cell)->snake_to);
  }
}

static int cell_comp (void *cell1, void *cell2)
{
  int res = 0;
  if (((Cell*)cell1)->number > ((Cell*)cell2)->number)
  {
    res = 1;
  }
  else if (((Cell*)cell1)->number < ((Cell*)cell2)->number)
  {
    res = -1;
  }
  return res;
}

static void* cell_copy (void *cell)
{
  Cell *copied_cell = malloc (sizeof (Cell));
  if (copied_cell == NULL)
  {
    printf (ALLOCATION_ERROR_MASSAGE);
    free (copied_cell);
    copied_cell = NULL;
  }
  memcpy (copied_cell, cell, sizeof (*copied_cell));
  return copied_cell;
}

static bool is_last_cell (void *cell)
{
  if (((Cell*)cell)->number == NUM_100)
  {
    return true;
  }
  return false;
}

static void init_markov_chain (MarkovChain *markov_chain)
{
  markov_chain->print_func = print_cell;
  markov_chain->comp_func = cell_comp;
  markov_chain->free_data = free;
  markov_chain->copy_func = cell_copy;
  markov_chain->is_last = is_last_cell;
}

static void init_database (LinkedList *linked_list)
{
  linked_list->size = 0;
  linked_list->first = NULL;
  linked_list->last = NULL;
}

static void generate_routes (MarkovChain *markov_chain, int route_num)
{
  printf ("Random Walk %d: ", route_num+1);
  generate_random_sequence(markov_chain,
                           markov_chain->database->first->data,
                           MAX_GENERATION_LENGTH);
  printf ("\n");
}

static int create_board(Cell *cells[BOARD_SIZE])
{
    for (int i = 0; i < BOARD_SIZE; i++)
    {
        cells[i] = malloc(sizeof(Cell));
        if (cells[i] == NULL)
        {
            for (int j = 0; j < i; j++) {
                free(cells[j]);
            }
            handle_error(ALLOCATION_ERROR_MASSAGE,NULL);
            return EXIT_FAILURE;
        }
        *(cells[i]) = (Cell) {i + 1, EMPTY, EMPTY};
    }

    for (int i = 0; i < NUM_OF_TRANSITIONS; i++)
    {
        int from = transitions[i][0];
        int to = transitions[i][1];
        if (from < to)
        {
            cells[from - 1]->ladder_to = to;
        }
        else
        {
            cells[from - 1]->snake_to = to;
        }
    }
    return EXIT_SUCCESS;
}

/**
 * fills database
 * @param markov_chain
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
static int fill_database(MarkovChain *markov_chain)
{
    Cell* cells[BOARD_SIZE];
    if(create_board(cells) == EXIT_FAILURE)
    {
        return EXIT_FAILURE;
    }
    MarkovNode *from_node = NULL, *to_node = NULL;
    size_t index_to;
    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        add_to_database(markov_chain, cells[i]);
    }

    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        from_node = get_node_from_database(markov_chain,cells[i])->data;

        if (cells[i]->snake_to != EMPTY || cells[i]->ladder_to != EMPTY)
        {
            index_to = MAX(cells[i]->snake_to,cells[i]->ladder_to) - 1;
            to_node = get_node_from_database(markov_chain, cells[index_to])
                    ->data;
            add_node_to_counter_list(from_node, to_node, markov_chain);
        }
        else
        {
            for (int j = 1; j <= DICE_MAX; j++)
            {
                index_to = ((Cell*) (from_node->data))->number + j - 1;
                if (index_to >= BOARD_SIZE)
                {
                    break;
                }
                to_node = get_node_from_database(markov_chain,
                                                 cells[index_to])->data;
                add_node_to_counter_list(from_node, to_node, markov_chain);
            }
        }
    }
    // free temp arr
    for (size_t i = 0; i < BOARD_SIZE; i++)
    {
        free(cells[i]);
    }
    return EXIT_SUCCESS;
}

/**
 * @param argc num of arguments
 * @param argv 1) Seed
 *             2) Number of sentences to generate
 * @return EXIT_SUCCESS or EXIT_FAILURE
 */
int main(int argc, char *argv[])
{
  if (argc != NUM_3)
  {
    printf ("Usage: the program can get 2 parameters only.");
    return EXIT_FAILURE;
  }
  srand ((int)strtol (argv[NUM_1], NULL, NUM_10));
  MarkovChain *markov_chain = calloc (1, sizeof (MarkovChain));
  if (markov_chain == NULL)
  {
    handle_error (ALLOCATION_ERROR_MASSAGE, &markov_chain);
    return EXIT_FAILURE;
  }
  markov_chain->database = calloc (1, sizeof (LinkedList));
  if (markov_chain->database == NULL)
  {
    handle_error (ALLOCATION_ERROR_MASSAGE, &markov_chain);
    return EXIT_FAILURE;
  }
  init_markov_chain (markov_chain);
  init_database (markov_chain->database);
  int routes_to_generate = (int) strtol (argv[NUM_2], NULL, NUM_10);
  int route_num = 0;
  if (fill_database (markov_chain) == 1)
  {
    handle_error (ALLOCATION_ERROR_MASSAGE, &markov_chain);
    return  EXIT_FAILURE;
  }
  while (route_num < routes_to_generate)
  {
    generate_routes (markov_chain, route_num);
    route_num++;
  }
  free_markov_chain (&markov_chain);
  return EXIT_SUCCESS;
}
