#ifdef OH_TESTS
#include "/cs/usr/oryan.hassidim/ex3b/ex3b-oryan.hassidim/oh_tests/oh_tests_helpers.h"
#endif // OH_TESTS

#include "linked_list.h"
#include "markov_chain.h"
#include <string.h>

void free_memory (MarkovChain *markov_chain, void* to_free)
{
  markov_chain->free_data (to_free);
  to_free = NULL;
}

Node* add_to_database(MarkovChain *markov_chain, void *data_ptr)
{
  // Check if word is already in database
  Node *markov_node = get_node_from_database (markov_chain, data_ptr);
  if (markov_node != NULL)
  {
    return markov_node;
  }
  MarkovNode *new_markov_node = calloc (1, sizeof (MarkovNode));
  if (new_markov_node == NULL)
  {
    free_memory (markov_chain, new_markov_node);
    return NULL;
  }
  new_markov_node->frequencies_list = NULL;
  new_markov_node->freq_list_len = 0;
  new_markov_node->data = markov_chain->copy_func (data_ptr);
  int res = add(markov_chain->database, new_markov_node);
  if (res == 1)
  {
    free_memory(markov_chain, new_markov_node->data);
    free_markov_chain (&markov_chain);
    return NULL;
  }
  return markov_chain->database->last;
}

Node* get_node_from_database(MarkovChain *markov_chain, void *data_ptr)
{
 Node *cur_node = markov_chain->database->first;
 while (cur_node != NULL)
 {
   if (markov_chain->comp_func (cur_node->data->data, data_ptr) == 0)
   {
     return cur_node;
   }
   cur_node = cur_node->next;
 }
 return NULL;
}

bool add_node_to_counter_list(MarkovNode *first_node,
                              MarkovNode *second_node,
                              MarkovChain *markov_chain)
{
  if (first_node->freq_list_len == 0)
  {
    first_node->frequencies_list = calloc (1, sizeof (NextNodeCounter));
    if (first_node->frequencies_list == NULL)
    {
      free_memory(markov_chain, first_node->frequencies_list);
      printf (ALLOCATION_ERROR_MASSAGE);
      return false;
    }
  }
  for (int i = 0; i < first_node->freq_list_len; ++i)
  {
    if (markov_chain->comp_func(
        second_node->data,
        ((first_node->frequencies_list) + i)->markov_node->data) == 0)
    {
      ((first_node->frequencies_list + i)->frequency)++;
      return true;
    }
//    if ((first_node->frequencies_list + i)->markov_node == second_node)
//    {
//      ((first_node->frequencies_list + i)->frequency)++;
//      return true;
//    }
  }
  NextNodeCounter * temp = realloc (first_node->frequencies_list,
                                        (first_node->freq_list_len+1) *
                                        sizeof (NextNodeCounter));
  if (temp == NULL)
  {
    free_memory(markov_chain, temp);
    printf (ALLOCATION_ERROR_MASSAGE);
    return false;
  }
  first_node->frequencies_list = temp;
  NextNodeCounter new_element = {second_node, 1};
  *(first_node->frequencies_list + first_node->freq_list_len) = new_element;
  (first_node->freq_list_len)++;
  return true;
}

void free_markov_chain(MarkovChain ** ptr_chain)
{
  LinkedList *database = (*ptr_chain)->database;
  while (database->first != NULL)
  {
    Node *cur_node = database->first;
    free_memory(*ptr_chain, cur_node->data->frequencies_list);
    free_memory (*ptr_chain, cur_node->data->data);
    free_memory (*ptr_chain, cur_node->data);
    database->first = database->first->next;
    free_memory (*ptr_chain, cur_node);
  }
  free_memory (*ptr_chain, database);
  free_memory (*ptr_chain, *ptr_chain);
}

int get_random_number (int max_number)
{
  return rand() % max_number;
}

MarkovNode* get_first_random_node(MarkovChain *markov_chain)
{
  LinkedList *database = markov_chain->database;
  Node *node_to_return;
  bool terminating_word = true;
  while (terminating_word)
  {
    int max_number = markov_chain->database->size;
    int i = get_random_number (max_number);
    Node *node = database->first;
    int j = 0;
    while (j < i)
    {
      node = node->next;
      j++;
    }
    if (markov_chain->is_last(node->data->data) == false)
    {
      terminating_word = false;
      node_to_return = node;
    }
  }
  return node_to_return->data;
}

unsigned int num_words_in_freq_list(int freq_list_len,
                                    NextNodeCounter *freq_list)
{
  int i = 0;
  unsigned int words_num = 0;
  while (i < freq_list_len)
  {
    words_num += (freq_list+i)->frequency;
    i++;
  }
  return words_num;
}

MarkovNode* get_next_random_node(MarkovNode *state_struct_ptr)
{
  MarkovNode *node_to_return;
  NextNodeCounter *freq_list = state_struct_ptr->frequencies_list;
  int freq_l_len = state_struct_ptr->freq_list_len;
  int i;
  int tot_freq = 0;
  int ind = 0;
  int num_words = (int)num_words_in_freq_list (freq_l_len, freq_list);
  i = get_random_number (num_words);
  bool condition = true;
  while (condition)
  {
    int cur_freq = (int) (state_struct_ptr->frequencies_list[ind].frequency);
    tot_freq += cur_freq;
    if (tot_freq > i)
    {
      condition = false;
      node_to_return = state_struct_ptr->frequencies_list[ind].markov_node;
    }
    ++ind;
  }
  return node_to_return;
}

void generate_random_sequence(MarkovChain *markov_chain,
                              MarkovNode *first_node, int max_length)
{
  if (first_node == NULL)
  {
    first_node = get_first_random_node (markov_chain);
  }
  MarkovNode *cur_node = first_node;
  markov_chain->print_func(cur_node->data);
  int words_num = 1;
  while (words_num < max_length)
  {
    cur_node = get_next_random_node (cur_node);
    markov_chain->print_func(cur_node->data);
    if (markov_chain->is_last(cur_node->data) || words_num > max_length)
    {
      return;
    }
    words_num++;
  }
}