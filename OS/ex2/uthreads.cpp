//
// Created by yehudal318 on 4/16/23.
//

#include "uthreads.h"
#include "Thread.h"
#include <signal.h>
#include <sys/time.h>
//?
#include <istream>
#include <iostream>
#include <algorithm>
#include <list>
#include <new>
//?

//CONSTANTS
#define RETURN_VAL_SIGSETJMP 1
#define NEED_TO_DELETE_THREAD 2
#define FAILURE (-1)
#define SUCCESS 0
#define MAIN_THREAD_ID 0
#define SAVE_MASK 1
#define NO_TID_TO_DELETE (-1)
#define USEC_IN_SEC 1000000
//MESSAGES
#define MSG_ERR_LIBRARY "thread library error: "
#define MSG_ERR_SYSTEM_CALL "system error: "
#define MSG_QUANTUM  "quantum should be a positive int!!\n"
#define MSG_ENTRY_POINT "entry_point can't be null!!!\n"
#define MSG_NO_THD "NO SUCH THREAD"
#define MSG_ERR_SYSTEM_CALL_TEXT "system call failed"
#define MSG_ALLOC_FAILURE  "failed to allocate memory exiting the program"
#define MSG_EXCEEDED_MAX "MAX number of threads already exist"
#define MSG_BLOCK_MAIN "Can't block main thread!"
#define MSG_TID_OUT_OF_RANGE "The thread id has to be between 0 and MAX_THREAD_NUM"
#define MASK sigprocmask(SIG_BLOCK, &set, nullptr)
#define UNMASK sigprocmask(SIG_UNBLOCK, &set, nullptr)


using std::cerr;
using std::endl;
using std::cout;

//DATA STRUCTURES
Thread* threads_map[MAX_THREAD_NUM]={};
std::list<int> ready_queue;
std::list<int> sleeping_threads;//todo change to map tid -> waiting time


// BLOCKED

//global variables
sigset_t set;
struct sigaction sa = {nullptr};
struct itimerval timer;
int running_id = 0;
int thread_counter = 0;
int total_quantum_counter = 1; // 1  the main thread initialization will be the first thing that happens
int program_quantum = 0;
int tid_to_be_deleted = NO_TID_TO_DELETE;


//Functions Declaration

void initialize_clock(int quantum);
int  reset_timer(int quantum);
int fetch_next_thread();
int free_thread(int tid);
//int change_state(int tid, State);
void scheduler(State state);
void print_ready_queue();
void check_on_sleeping_threads();
void free_all_resources();


/**
 * every time the sigvtalrm will be sent the handler should  be called and handle the sig
 * it should
 * 1) terminate the running of the current running process and move it to the ready queue -done
 * by the scheduler
 * 2)decrease the waiting time of all sleeping threads by one -done by the
 * check_on_sleeping_threads <- fetch_next <- yield <- scheduler
 * into running we should update the quantum counter
 * 3) fetch the next process to run from the ready queue into
 * running we should update the quantum counter done in  fetch_next() <- yield() <- scheduler()
 * @param sig ??? todo
 */
void timer_handler(int sig)
{
//    cout << "in time handler" <<endl;
  scheduler(READY);
}

/**
 * initializing the timer for the first time
 * and choosing the handler function as the response to the sigvtalrm
 * the timer will expire every quantum useconds
 * @param quantum the interval in which the alarm will be sound
 */
void initialize_clock(int quantum) {
  sa.sa_handler = &timer_handler;
  if (sigaction(SIGVTALRM, &sa, nullptr) < 0) {
    cerr << MSG_ERR_SYSTEM_CALL << MSG_ERR_SYSTEM_CALL_TEXT << endl;
    exit(EXIT_FAILURE);
  }
//     cout << "timer is ready!" << endl;
  reset_timer(quantum);
}


/**
 * reset timer to quantum amount of useconds and starts running
 * @param quantum the interval in which the alarm will be sound
 */
int  reset_timer(int quantum) {
  int sec = quantum/USEC_IN_SEC; int usec = quantum%USEC_IN_SEC;
  timer.it_value.tv_sec = sec;        // first time interval, seconds part
  timer.it_value.tv_usec = usec;        // first time interval, microseconds part
  timer.it_interval.tv_sec = sec;    // following time intervals, seconds part
  timer.it_interval.tv_usec = usec;    // following time intervals
//    std::cout << "seconds :" << sec << " mic sec: " << usec << endl;
  if (setitimer(ITIMER_VIRTUAL, &timer, nullptr)) {
    cerr<<  MSG_ERR_SYSTEM_CALL << MSG_ERR_SYSTEM_CALL_TEXT << std::endl;
    free_all_resources();
    exit(EXIT_FAILURE);
  }
//    cout <<"reset_clock func" << endl;
  return SUCCESS;
}




/**
 * frees the thread given by tid, free all the memory allocated to it, and erases it from all the
 * data structures of the program
 * @param tid the id  of said thread
 * @return SUCCESS upon a successful run FAILURE otherwise
 */
int free_thread(int tid){ //todo
  if(threads_map[tid] == nullptr){
    return FAILURE;}
  Thread *temp_ptr = threads_map[tid];
  threads_map[tid] = nullptr;
  ready_queue.remove(tid);// it's OK to remove from a list an element that not on the list.
  sleeping_threads.remove(tid);
  delete temp_ptr;
  return SUCCESS;
}
/**
 * fetches the next thread from the ready queue (by tid)
 * and updates all the relevant fields and global variables
 * (the state of the fetched thread, the thread's q_counter, the total q_counter and the running_id.
 * @return the tid of the next thread to run fetched from the ready queue
 */
int fetch_next_thread() { //
  int next = ready_queue.front();
  ready_queue.pop_front();
  check_on_sleeping_threads(); //todo check if before total++ or after line was here
  threads_map[next]->setState(RUNNING);
  threads_map[next]->increase_quantums();
  total_quantum_counter++;
//    check_on_sleeping_threads(); //todo check if before total++ or after
//    cout << "total_quantum_counter is: " << total_quantum_counter <<endl;
  running_id=next;
  return next;
}

/**
 * jumps to the thread that is held by the global variable "running_id"
 * note that the function doesnt change the running id and it should be handled beforehand
 * (by fetch_next)
 * @param tid
 */
void jump_to_thread( int return_val)
{
  UNMASK;
//    cout << "jumping no to thread num: "<< running_id<< endl;
  siglongjmp(threads_map[running_id]->env, return_val);
}

/**
 * @brief Saves the current thread state, and jumps to the other thread.
 * if ret_val = 0, it means that it's the first time we reached this function and we did just
 * saved the environment of the thread thus we should jump to the next thread
 * if ret_val != 0: it means that we've reached this code by other means i.e
 * by a siglongjmp and we should jump again 
 */
void yield(void)
{
  int ret_val = sigsetjmp(threads_map[running_id]->env, SAVE_MASK);
//    printf("current_thread is: %d   ", running_id);
//    printf("yield: ret_val=%d\n", ret_val);

  bool did_just_save_bookmark = (ret_val == 0);
  bool need_to_delete_thread = (ret_val == NEED_TO_DELETE_THREAD);
//    bool did_jump_from_another_thread = ret_val != 0;
  if (did_just_save_bookmark)
  {
//        printf("indeed\n");
    /* int next_id =*/ fetch_next_thread();
    reset_timer(program_quantum);
//        cout<<"jumping to next now"<<endl;
//        cout << "next_id: " << next_id << endl;
    jump_to_thread(RETURN_VAL_SIGSETJMP);
  }
  //added
  if(need_to_delete_thread){
    free_thread(tid_to_be_deleted);
    tid_to_be_deleted = NO_TID_TO_DELETE;
  }
}
/**
 *  @brief changes the running thread into some other state. and sets another thread to run
 *
 * should
 * save the environment of the current thread - handled by yield()
 * change all the relevant fields - here
 * updates all the relevant global variables - handled by fetch_next() called by yield()
 * fetch a new thread from the ready queue -handled by fetch_next() called by yield()
 * and change all its relevant fields  - handled by   fetch_next() called by yield()
 * and finally jump to its environment -
 *
 * should also check on sleeping threads //todo finished here last time;
 * @param state the state that the running thread shall take
 *
 */
void scheduler(State state){
  MASK; //todo check
  switch (state) {
    case READY:
//            cout<<"changing running thread to ready"<<endl;
      ready_queue.push_back(running_id);
      threads_map[running_id]->setState(READY);
//            print_ready_queue();
      yield();
      break;
    case BLOCKED:
//            cout<<"changing running thread to blocked"<<endl;
      threads_map[running_id]->setState(BLOCKED);
      threads_map[running_id]->setBlocked(true);
//            print_ready_queue();
      yield();
      break;
    case SLEEPING: //relevant fields are updated in uthread_sleep function
//            cout<<"changing running thread to sleep"<<endl;
      yield();
      break;
    default:
      break;
  }
  UNMASK; //todo check

}





/**@brief bocks a thread given by tid from running and exclude it from the ready_queue
 *
 * note that this function doesnt check validity of the input
 * @param tid
 */
void block_thread(int tid){
  threads_map[tid]->setBlocked(true);
  State state = threads_map[tid]->getState();
  switch (state) {
    case READY:
      threads_map[tid]->setState(BLOCKED);
      ready_queue.remove(tid);
      break;
    case RUNNING:
      scheduler(BLOCKED);
    default:
      break;
  }

}
void check_thread_to_delete(){
  if(tid_to_be_deleted != NO_TID_TO_DELETE){
    free_thread(tid_to_be_deleted);
    tid_to_be_deleted = NO_TID_TO_DELETE;
  }
}



/**
 *checks on all the
 */
void check_on_sleeping_threads(){
//    cout << "checking on sleeping threads" <<endl;
  std::list<int> to_remove;
  for(auto it = sleeping_threads.begin(); it != sleeping_threads.end();){
    int sleeping_tid = *it;
    if(total_quantum_counter == threads_map[sleeping_tid]->getWakeUpTime()){
      threads_map[sleeping_tid]->set_wake_up_time(AWAKE);
      it= sleeping_threads.erase(it);
      if(threads_map[sleeping_tid]->isBlocked()){
        threads_map[sleeping_tid]->setState(BLOCKED);
      }
      else{
        threads_map[sleeping_tid]->setState(READY);
        ready_queue.push_back(sleeping_tid);}
      ++it;
    }
    else{ ++it;}
//        cout << "whatttttttttttttttttttttttttttttttttttttt3" << endl;
  }
}

/**
 * frees all the resources in case of abruptly  leaving the programm
 */
void free_all_resources(){
  for (int i=MAX_THREAD_NUM-1; i>0; i--){ //todo - what about 0
    if (threads_map[i]!= nullptr) {
      free_thread(i);
    }
  }
}


int uthread_init(int quantum_usecs) {
  if(quantum_usecs <= 0){
    cerr << MSG_ERR_LIBRARY << MSG_QUANTUM;
    return FAILURE;
  }
  Thread* main_thread = new (std::nothrow) Thread(0, false, nullptr); //todo NOLINT
  // (modernize-use-auto)
  if(main_thread == nullptr){
    cerr<<  MSG_ERR_SYSTEM_CALL << MSG_ALLOC_FAILURE << std::endl;
    exit(EXIT_FAILURE);
  }
  thread_counter = 1;
  main_thread->increase_quantums();
  threads_map[0] = main_thread;
  program_quantum = quantum_usecs;
  sigemptyset(&set); ///todo check 2 lines
  sigaddset(&set, SIGVTALRM);
  initialize_clock(quantum_usecs);
  return SUCCESS;
}

/**
 * @brief Creates a new thread, whose entry point is the function entry_point with the signature
 * void entry_point(void).
 *
 * The thread is added to the end of the READY threads list.
 * The uthread_spawn function should fail if it would cause the number of concurrent threads to exceed the
 * limit (MAX_THREAD_NUM).
 * Each thread should be allocated with a stack of size STACK_SIZE bytes.
 * It is an error to call this function with a null entry_point.
 *
 * @return On success, return the ID of the created thread. On failure, return -1.
*/
int uthread_spawn(thread_entry_point entry_point){
  MASK;
  if (entry_point== nullptr){
    std::cerr << MSG_ERR_LIBRARY << MSG_ENTRY_POINT;
    UNMASK;
    return FAILURE;
  }
  int tid= MAX_THREAD_NUM;
  for (int i=0; i < MAX_THREAD_NUM; i++){
    if (threads_map[i]== nullptr){
      tid=i;
      break;
    }
  }
  if (tid==MAX_THREAD_NUM){
    cerr << MSG_ERR_LIBRARY << MSG_EXCEEDED_MAX << endl;
    UNMASK;
    return FAILURE;
  }
  // added this check  in case it has got here from the entry point of a thread
  // (and not sigsetjmp)
  check_thread_to_delete();
  Thread* new_thread=new  (std::nothrow) Thread( tid, true, entry_point);
  if(new_thread == nullptr || (!new_thread->get_alloc())){
    cerr<<  MSG_ERR_SYSTEM_CALL << MSG_ALLOC_FAILURE << endl;
    free_all_resources();
    exit(EXIT_FAILURE);
  }
  thread_counter++;
  threads_map[tid]=new_thread;
  ready_queue.push_back(tid);
  UNMASK;
  return tid;
}


int uthread_terminate(int tid) {
  MASK;
  if(tid<0 || tid>=MAX_THREAD_NUM){
    cerr << MSG_ERR_LIBRARY << MSG_TID_OUT_OF_RANGE << endl;
    UNMASK;
    return FAILURE;
  }
  if (threads_map[tid] == nullptr) {
    cerr << MSG_ERR_LIBRARY << MSG_NO_THD << endl;
    UNMASK;
    return FAILURE;
  }
  thread_counter--;
  if (tid == MAIN_THREAD_ID) {
    free_all_resources();
    exit(SUCCESS);
  } else if (tid == running_id) { //todo todo good morning to you added today
    // added this check  in case it's jumping to the entry point of a thread
    check_thread_to_delete();
    tid_to_be_deleted = running_id;
    fetch_next_thread();
    jump_to_thread(NEED_TO_DELETE_THREAD);
  }
//    cout << "terminating thread " << tid << endl;
  free_thread(tid);
  UNMASK;
  return SUCCESS;
}

int uthread_block(int tid) {
  MASK;
  if(tid<0 || tid>=MAX_THREAD_NUM){
    cerr << MSG_ERR_LIBRARY << MSG_TID_OUT_OF_RANGE << endl;
    UNMASK;
    return FAILURE;
  }
  if (tid==0 || threads_map[tid]== nullptr){
    if( tid==0) {
      cerr << MSG_ERR_LIBRARY << MSG_BLOCK_MAIN << endl;
    }
    else{
      cerr << MSG_ERR_LIBRARY << MSG_NO_THD << endl;
    }
    UNMASK;
    return FAILURE;
  }
  block_thread(tid);
  UNMASK;
  return SUCCESS;
}

/**
 * @brief Resumes a blocked thread with ID tid and moves it to the READY state.
 *
 * Resuming a thread in a RUNNING or READY state has no effect and is not considered as an error. If no thread with
 * ID tid exists it is considered an error.
 *
 * @return On success, return 0. On failure, return -1.
*/
int uthread_resume(int tid){
  MASK;
  if(tid<0 || tid>=MAX_THREAD_NUM){
    cerr << MSG_ERR_LIBRARY << MSG_TID_OUT_OF_RANGE << endl;
    UNMASK;
    return FAILURE;
  }
  if (threads_map[tid] == nullptr){
    cerr << MSG_ERR_LIBRARY << MSG_NO_THD << endl;
    UNMASK;
    return FAILURE;
  }

  if(threads_map[tid]->isBlocked()) {
    threads_map[tid]->setBlocked(false);
    if (threads_map[tid]->getState() != SLEEPING) { // add to ready queue if not sleeping
      ready_queue.push_back(tid);
      threads_map[tid]->setState(READY);
    }
  }
  UNMASK;
  return SUCCESS;
}

int uthread_sleep(int num_quantums) {
  MASK;
//    cout << "here sleeping" <<endl;
  if(num_quantums < 0 ){
    cerr << MSG_ERR_LIBRARY << MSG_QUANTUM <<endl;
    UNMASK;
    return FAILURE;
  }
  if(running_id == MAIN_THREAD_ID){
    cerr << MSG_ERR_LIBRARY << MSG_BLOCK_MAIN << endl;
    UNMASK;
    return FAILURE;
  }
  if(num_quantums > 0){
//        cout << "here too running id is:" << running_id <<endl;
    threads_map[running_id]->setState(SLEEPING);
    sleeping_threads.push_back(running_id);
    int wake_up_time = total_quantum_counter + num_quantums -1;//todo check +- 1;
//        cout << "wake_up_time :" << wake_up_time <<endl;
    threads_map[running_id]->set_wake_up_time(wake_up_time);
    scheduler(SLEEPING);
//        cout << "after the sleeping" << endl;
  }
  UNMASK;
  return SUCCESS; // covers also the case in which the num_quantum == 0
}
int uthread_get_tid() {
  return running_id;
}

int uthread_get_total_quantums() {
  return total_quantum_counter;
}

int uthread_get_quantums(int tid) {
  if(tid<0 || tid>=MAX_THREAD_NUM){
    cerr << MSG_ERR_LIBRARY << MSG_TID_OUT_OF_RANGE << endl;
    return FAILURE;
  }
  if(threads_map[tid] == nullptr){
    cerr << MSG_ERR_LIBRARY << MSG_NO_THD << endl;
    return  FAILURE;
  }
  return threads_map[tid]->get_quatums_counter();
}




//debugging functions

//void  some_point(void ){
//    cout<< "entry_point"<< endl;
//}
//void print_ready_queue(){
//    cout << "printing  ready queue" << endl;
//    if(!ready_queue.empty()){
//        for(auto tid : ready_queue){
//            cout << tid <<endl;
//        }
//    }
//}
//void thread0(void) {
//    int i = 0;
//    while (true) {
//        ++i;
////        printf("in thread0 (%d)\n", i);
//        if (i % 5 == 0)
//            uthread_resume(1);
//        {
////            printf("thread0: yielding\n");
//
//        }
////        usleep(USEC_IN_SEC);
//
//
//        }
//    }
//
//
//
//void thread1(void)
//{
//    cout << "thread1" << endl;
//    print_ready_queue();
//    cout << "block"<< endl;
//    uthread_block(1);
//    cout << "here 3333" <<endl;
//    cout << "sleep"<< endl;
//    uthread_sleep(2);
//    print_ready_queue();
//    int i = 0;
//    while (1)
//    {
//        ++i;
//
//        if (i % 5 == 0)
//        {
//        }
//    }
//}
//void thread2(void)
//{
//    cout << "Thread2" << endl;
//    print_ready_queue();
//
//    int i = 0;
//    while (1)
//    {
//        ++i;
//
//        if (i % 5 == 0)
//        {
//        }
//    }
//}
//void print_map(){
//    cout << "printing map: " << endl;
//    for(auto thread : threads_map){
//        if(thread != nullptr){
//            cout << thread->getTid() << endl ;
//        }
//    }
//}
//
//int main(int argn , char** argv){
//    uthread_init(1);
//    cout << "ok?!" << uthread_get_total_quantums() << endl;
//    cout << "end of init" << endl;
//    cout <<   "counter: " <<thread_counter << endl;
//cout << "CREATING THREad 1" << endl;
//    uthread_spawn(thread1);
//    uthread_spawn(thread2);
//    thread0();
////    uthread_spawn(thread1);
//    cout <<   "counter: " <<thread_counter << endl;
//    print_ready_queue();
//
//    cout <<   "counter: " <<thread_counter << endl;
//    print_ready_queue();
//    uthread_terminate(1);
//    uthread_spawn(some_point);
//    uthread_spawn(some_point);
//    print_ready_queue();
//    print_map();
//    print_map();
//    cout <<   "counter: " <<thread_counter << endl;
//    uthread_spawn(some_point);
//    uthread_terminate(2);
//    cout <<   "counter: " <<thread_counter << endl;
//
//
//    uthread_spawn(some_point);
//    cout << "printing map: " << endl;
//    cout << "here"<< endl;
//    print_ready_queue();
//    cout <<   "counter: " <<thread_counter << endl;
////    /uthread_terminate(0);
//    cout <<   "counter: " <<thread_counter << endl;
//    print_ready_queue();
//    while(true){
//        cout << "hello" <<endl;
//
//    }
////    for(auto thread : threads_map){
////        cout << thread->getTid() << endl ;
////    }
//
//}