#include "linked_list.h"
#include "markov_chain.h"
#include <string.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>

#define MAX_LINE 1001
#define MAX_TWEET_LENGTH 20
#define NUM_1 1
#define NUM_2 2
#define NUM_3 3
#define NUM_4 4
#define NUM_5 5
#define NUM_10 10

int is_allocated (void *markov_chain)
{
  if (markov_chain == NULL)
  {
    printf ("%s\n", ALLOCATION_ERROR_MASSAGE);
    return 0;
  }
  return 1;
}

void init_database (LinkedList *linked_list)
{
  linked_list->size = 0;
  linked_list->first = NULL;
  linked_list->last = NULL;
}

void handle_alloc_error (FILE *f, MarkovChain **markov_chain)
{
  printf (ALLOCATION_ERROR_MASSAGE);
  free_markov_chain (markov_chain);
  fclose (f);
}

void generate_tweets (MarkovChain *markov_chain, int tweet_num)
{
  printf ("Tweet %d: ", tweet_num+1);
  generate_random_sequence(markov_chain, NULL, MAX_TWEET_LENGTH);
  printf ("\n");
}

int fill_database(FILE *fp, int words_to_read, MarkovChain *markov_chain)
{
  char line[MAX_LINE] = {0};
  int i = 0;
  while (fgets(line, MAX_LINE, fp) != NULL)
  {
    if (words_to_read != -1 && i >= words_to_read)
    {
      break;
    }
    char *fixed_line = strtok (line, "\n");
    char *cur_word = strtok (fixed_line, " ");
    while (cur_word != NULL)
    {
      if (words_to_read != -1 && i >= words_to_read)
      {
        break;
      }
      Node* first_node = add_to_database (markov_chain, cur_word);
      if (first_node == NULL)
      {
        return 1;
      }
      if (i == 0)
      {
        i++;
      }
      cur_word = strtok (NULL, " ");
      if (cur_word)
      {
        Node* second_node = add_to_database (markov_chain, cur_word);
        if (second_node == NULL)
        {
          return 1;
        }
        bool res = add_node_to_counter_list(first_node->data,
                                          second_node->data);
        if (res == false)
        {
          return 1;
        }
      }
      i++;
    }
  }
  return 0;
}

int main(int argc, char *argv[])
{
  if (argc == NUM_4 || argc == NUM_5)
  {
    FILE *f = fopen (argv[3], "r");
    if (f == NULL)
    {
      printf ("Error: the given path is not valid.");
      return EXIT_FAILURE;
    }
    int seed = (int)strtol (argv[NUM_1], NULL, NUM_10);
    srand (seed);
    MarkovChain *markov_chain = calloc (1, sizeof (MarkovChain));
    if (is_allocated (markov_chain) == 0)
    {
      handle_alloc_error (f, &markov_chain);
      return EXIT_FAILURE;
    }
    markov_chain->database = calloc (1, sizeof (LinkedList));
    if (is_allocated (markov_chain->database) == 0)
    {
      handle_alloc_error (f, &markov_chain);
      return EXIT_FAILURE;
    }
    init_database(markov_chain->database);
    int tweet_num = 0, num_words_to_read = -1;
    int tweets_max = (int)strtol (argv[NUM_2], NULL, NUM_10);
    if (argc == NUM_5)
    {
      num_words_to_read = (int)strtol (argv[4], NULL, NUM_10);
    }
    if (fill_database (f, num_words_to_read, markov_chain) == 1)
    {
      handle_alloc_error (f, &markov_chain);
      return EXIT_FAILURE;
    }
    while (tweet_num < tweets_max)
    {
      generate_tweets (markov_chain, tweet_num);
      tweet_num++;
    }
    fclose(f);
    free_markov_chain (&markov_chain);
    return EXIT_SUCCESS;
  }
  else
  {
    printf ("Usage: the program can get 3 or 4 parameters only.");
    return EXIT_FAILURE;
  }
}