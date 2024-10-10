#include "MapReduceFramework.h"
#include <pthread.h>
#include <map>
#include <atomic>
#include <Barrier.h>
#include <vector>
#include <iostream>
#include <algorithm>
//#include <semaphore.h>

//#define NUM_OF_MUTEXES 7 //???
#define LOCK_MUTEX_ERR "system error: error locking mutex"
#define UNLOCK_MUTEX_ERR "system error: error unlocking mutex"
#define THREAD_INIT_ERR "system error: error creating thread"
#define THREAD_JOIN_ERR "system error: error joining threads"
#define LAST_2_BITS 62
#define SECOND_31_BITS 31
#define SUCCESS 0

typedef struct ThreadContext ThreadContext;
typedef struct JobContext JobContext;

void *thread_func (void *arg);
void lock_mutex (pthread_mutex_t *mutex);
void unlock_mutex (pthread_mutex_t *mutex);
void map_phase (ThreadContext *thread_context);
void sort_phase (ThreadContext *thread_context);
void shuffle_phase (ThreadContext *thread_context);
void reduce_phase (ThreadContext *thread_context);
K2 *intermediate_vector_max (JobContext *job_context);
bool equal_keys (K2 *key1, K2 *key2);

typedef struct JobContext
{
    pthread_t *threads{};
    ThreadContext *context{};
    const MapReduceClient *client{};
    int num_threads = 0;
    const InputVec *input_vec{};
    std::vector<IntermediateVec *> *shuffle_queue{};
    size_t pairs_in_shuffle = 0;
    OutputVec *output_vec{};
    Barrier *barrier{};
    pthread_mutex_t map_mutex = PTHREAD_MUTEX_INITIALIZER;
//    pthread_mutex_t shuffle_mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_t reduce_mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_t emit2_mutex = PTHREAD_MUTEX_INITIALIZER;
    pthread_mutex_t emit3_mutex = PTHREAD_MUTEX_INITIALIZER;
//    pthread_mutex_t wait_for_job_mutex = PTHREAD_MUTEX_INITIALIZER;
//    pthread_mutex_t thread_func_mutex = PTHREAD_MUTEX_INITIALIZER;
    std::atomic<uint64_t> *atomic_progress = nullptr;
    std::atomic<int> *atomic_counter = nullptr;
//    bool thread_waited = false;

}JobContext;

typedef struct ThreadContext
{
    int tid{};
    IntermediateVec *intermediate_vec{};
    JobContext *job{};
    void *thread_finished = nullptr;

} ThreadContext;

bool equal_keys (K2 *key1, K2 *key2)
{
  return ((!(*key1 < *key2)) && (!(*key2 < *key1)));
}

K2 *intermediate_vector_max (JobContext *job_context)
{
  K2 *max = nullptr;
  for (int i = 0; i < job_context->num_threads; i++)
  {
    if (!job_context->context[i].intermediate_vec->empty ())
    {
      max = (job_context->context[i].intermediate_vec->back ()).first;
      break;
    }
  }
  if (max == nullptr)
  { return nullptr; }
  K2 *temp;
  for (int i = 0; i < job_context->num_threads; i++)
  {
    if (!job_context->context[i].intermediate_vec->empty ())
    {
      temp = (job_context->context[i].intermediate_vec->back ()).first;
      if (*max < *temp)
      {
        max = temp;
      }
    }
  }
  return max;
}

void lock_mutex (pthread_mutex_t *mutex)
{
  if (pthread_mutex_lock (mutex) != 0)
  {
    std::cout << LOCK_MUTEX_ERR << std::endl;
    exit (EXIT_FAILURE);
  }
}

void unlock_mutex (pthread_mutex_t *mutex)
{
  if (pthread_mutex_unlock (mutex) != 0)
  {
    std::cout << UNLOCK_MUTEX_ERR << std::endl;
    exit (EXIT_FAILURE);
  }
}

void map_phase (ThreadContext *thread_context)
{
  auto input_size = thread_context->job->input_vec->size ();
  unsigned long old_value = 0;
  while (old_value < input_size)
  {
    lock_mutex (&thread_context->job->map_mutex);
    if (thread_context->job->atomic_progress->load () == 0)
    {
      (*(thread_context->job->atomic_progress)) += (1l << LAST_2_BITS);
      (*(thread_context->job->atomic_progress)) += (input_size
          << SECOND_31_BITS);
    }
    unlock_mutex (&thread_context->job->map_mutex);
    old_value = (*(thread_context->job->atomic_counter))++;
    if (old_value < input_size)
    {
        auto curr_pair = (thread_context->job->input_vec)->at(old_value);
        (thread_context->job)->client->map(curr_pair.first, curr_pair.second,
                                           thread_context);
        (*(thread_context->job->atomic_progress))++;
    }
  }
}

void sort_phase (ThreadContext *thread_context)
{
  std::sort (thread_context->intermediate_vec->begin (),
             thread_context->intermediate_vec->end (), []
                 (const std::pair<K2 *, V2 *> &p1, const std::pair<K2 *, V2 *> &p2)
             {
                 return (*(p1.first) < *(p2.first));
             });
}

void shuffle_phase (ThreadContext *thread_context)
{
  if (thread_context->tid == 0)
  {
    JobContext *job_context = thread_context->job;
//    lock_mutex (&thread_context->job->shuffle_mutex);
    (*(job_context->atomic_progress)) = (2l << LAST_2_BITS) /*0*/;

//    unsigned long total_work = calculate_total(thread_context->job);
    unsigned long total_work = 0;
    for (int i = 0; i < job_context->num_threads; i++)
    {
      total_work += (unsigned long) (job_context->context[i])
          .intermediate_vec->size ();
    }
    (*(job_context->atomic_progress)) += (total_work
        << SECOND_31_BITS);
//    shuffle (thread_context->job);
////////////////
    auto multi_level = job_context->num_threads;
    K2 *curr_max = intermediate_vector_max (job_context);
    while (curr_max != nullptr)
    {
      auto *curr_vec = new IntermediateVec (); //needs free
      for (int i = 0; i < multi_level; ++i)
      {
        if (job_context->context[i].intermediate_vec->empty ()) continue;
        auto intermediate_vec_back_i = job_context->context[i]
            .intermediate_vec->back ().first;
        while (equal_keys (intermediate_vec_back_i, curr_max))
        {
          curr_vec->push_back (job_context->context[i].intermediate_vec->back
              ());//push a pair
          job_context->context[i].intermediate_vec->pop_back ();
          (*job_context->atomic_progress)++;
          if (job_context->context[i].intermediate_vec->empty ()) break;
          intermediate_vec_back_i = job_context->context[i]
              .intermediate_vec->back ().first;
        }
      }
      job_context->shuffle_queue->push_back (curr_vec);
      curr_max = intermediate_vector_max (job_context);
    }
    for (int i = 0; i < multi_level; ++i)
    {
      delete (job_context->context[i].intermediate_vec);
      job_context->context[i].intermediate_vec = nullptr;
    }
    /////////////
//    calculate_pairs_in_shuffle_vector (thread_context->job);
    for (auto vector: (*(thread_context->job->shuffle_queue)))
    {
      (job_context->pairs_in_shuffle) += vector->size ();
    }
    (*(job_context->atomic_progress)) = /*0*/ (3lu << LAST_2_BITS);
//    unlock_mutex (&thread_context->job->shuffle_mutex);
  }
}

void reduce_phase (ThreadContext *thread_context)
{
  JobContext *job_context = thread_context->job;
  unsigned long current_length = 0;
  auto input_size = job_context->shuffle_queue->size ();
  unsigned long old_value = 0;
  while (old_value < input_size)
  {
    lock_mutex (&job_context->reduce_mutex);
    if (job_context->atomic_progress->load () == /*0*/(3lu << LAST_2_BITS))
    {
      *job_context->atomic_counter = 0;
//      auto pairs_amount = job_context->pairs_in_shuffle;
      *job_context->atomic_progress += job_context->pairs_in_shuffle <<
                                                                     SECOND_31_BITS;
    }

    unlock_mutex (&job_context->reduce_mutex);
    old_value = (*(job_context->atomic_counter))++;
    if (old_value < input_size)
    {
      auto current_vector = (job_context->shuffle_queue)->at (old_value);
      (job_context->client)->reduce (current_vector, thread_context);
      current_length = current_vector->size ();
      (*(job_context->atomic_progress)) += current_length ;

    }
  }
}

void *thread_func (void *arg)
{
  auto *thread_context = (ThreadContext *) arg;
  map_phase (thread_context);
  sort_phase (thread_context);
  thread_context->job->barrier->barrier ();
  shuffle_phase (thread_context);
  thread_context->job->barrier->barrier ();
  reduce_phase (thread_context);
  return nullptr;
}

JobHandle startMapReduceJob (const MapReduceClient &client,
                             const InputVec &inputVec, OutputVec &outputVec,
                             int multiThreadLevel)
{

  JobContext *job_context = new JobContext ();
//  auto *atomic_progress = new std::atomic<uint64_t> (0);//needs free
//  auto *atomic_counter = new std::atomic<int> (0);// needs free
  //initializing all fields of job context
  job_context->threads = new pthread_t[multiThreadLevel];// needs free
  job_context->context = new ThreadContext[multiThreadLevel]; //needs free
  job_context->client = &client;
  job_context->shuffle_queue = new std::vector<IntermediateVec *>; // needs
  // free
  job_context->num_threads = multiThreadLevel;
  job_context->input_vec = &inputVec;
  job_context->output_vec = &outputVec;
  job_context->atomic_progress = new std::atomic<uint64_t> (0);
  job_context->atomic_counter = new std::atomic<int> (0);
  job_context->barrier = new Barrier (multiThreadLevel); // needs free
  //creating context
  for (int i = 0; i < multiThreadLevel; i++)
  {
//    auto *vec_of_thread = new IntermediateVec (); // needs free
    job_context->context[i].tid = i;
    job_context->context[i].intermediate_vec = new IntermediateVec ();
    job_context->context[i].job = job_context;

  }
  //creating threads
  for (int i = 0; i < multiThreadLevel; i++)
  {

    if (pthread_create (job_context->threads + i, nullptr, thread_func,
                        job_context->context + i) != SUCCESS)
    {
      std::cout << THREAD_INIT_ERR << std::endl;
      exit (EXIT_FAILURE);
    }
  }
  return job_context;

}

void emit2 (K2 *key, V2 *value, void *context)
{

  auto *thread_context = (ThreadContext *) context;
  lock_mutex (&thread_context->job->emit2_mutex);
  thread_context->intermediate_vec->push_back ({key, value});
  unlock_mutex (&thread_context->job->emit2_mutex);
//
//      (static_cast<ThreadContext *>(context))->intermediateVec->push_back ({key,
//                                                                        value});
}

void emit3 (K3 *key, V3 *value, void *context)
{
  auto *thread_context = (ThreadContext *) context;
  lock_mutex (&thread_context->job->emit3_mutex);
  thread_context->job->output_vec->push_back ({key, value});
  unlock_mutex (&thread_context->job->emit3_mutex);
}

void waitForJob (JobHandle job)
{
  auto *job_context = static_cast<JobContext *>(job);
  for (int i = 0; i < (job_context->num_threads); i++)
  {
    if (job_context->context[i].thread_finished != nullptr)
    {
      if (*(int *) (job_context->context[i].thread_finished))
      {
        continue;
      }
    }
    if (pthread_join ((job_context->threads)[i], &((job_context->context[i]).thread_finished))
        != SUCCESS)
    {
      std::cout << THREAD_JOIN_ERR << std::endl;
      exit (EXIT_FAILURE);
    }
  }
}

void getJobState (JobHandle job, JobState *state)
{
  auto atomic = static_cast<const JobContext *>(job)->atomic_progress->load ();
  auto stage = static_cast<stage_t>((stage_t) (atomic >> LAST_2_BITS));
  auto total = (float) ((atomic >> SECOND_31_BITS) & 0x7fffffff);
  state->stage = stage;
  if (atomic == 0 || total == 0)
  {
    state->percentage = 0;
    return;
  }
  state->percentage = (100 * ((float) (atomic & 0x7fffffff))) /
                      ((float) ((atomic >> SECOND_31_BITS) & 0x7fffffff));
}

void closeJobHandle (JobHandle job)
{
  waitForJob (job);
  auto *job_context = static_cast<JobContext *> (job);
  delete job_context->atomic_progress;
  // shuffle queue
//  if (job_context->shuffle_queue)
//  {
//    for (auto &vec: *job_context->shuffle_queue)
//    {
//      if (vec)
//      {
//        for (auto &pair: *vec)
//        {
//
//          delete pair.first;
//          delete pair.second;
//        }
//        delete vec;
//      }
//    }
    while (!(job_context->shuffle_queue)->empty())
    {
        auto temp = (job_context->shuffle_queue)->back();
        job_context->shuffle_queue->pop_back();
        delete temp;
        temp = nullptr;
    }
    delete job_context->shuffle_queue;
    job_context->shuffle_queue = nullptr;


//  while (!job_context->shuffle_queue->empty ())
//  {
//    auto curr = job_context->shuffle_queue->back ();
//    job_context->shuffle_queue->pop_back ();
//    delete curr;
//    curr = nullptr;
//  }
//  delete job_context->shuffle_queue;
//  job_context->shuffle_queue = nullptr;
  /////
  delete[]job_context->context;
  delete job_context->barrier;
  delete job_context->atomic_counter;
  pthread_mutex_destroy (&(job_context->map_mutex));
  pthread_mutex_destroy (&(job_context->reduce_mutex));
  pthread_mutex_destroy (&(job_context->emit2_mutex));
  pthread_mutex_destroy (&(job_context->emit3_mutex));
  delete[] job_context->threads;
//  delete job;

}

