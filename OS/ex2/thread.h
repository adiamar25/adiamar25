
#include <cstdlib>
#include "uthreads.h"
#include <setjmp.h>
#include <stdio.h>
#include <setjmp.h>
#include <signal.h>
#include <unistd.h>
#include <sys/time.h>
#include <stdbool.h>
#include <iostream>

#ifndef Thread_H
#define Thread_H

#ifdef __x86_64__
/* code for 64 bit Intel arch */

typedef unsigned long address_t;
#define JB_SP 6
#define JB_PC 7


/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
  address_t ret;
  asm volatile("xor    %%fs:0x30,%0\n"
               "rol    $0x11,%0\n"
      : "=g" (ret)
      : "0" (addr));
  return ret;
}

#else
/* code for 32 bit Intel arch */

typedef unsigned int address_t;
#define JB_SP 4
#define JB_PC 5


/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%gs:0x18,%0\n"
                 "rol    $0x9,%0\n"
    : "=g" (ret)
    : "0" (addr));
    return ret;
}


#endif
#define AWAKE (-1)

typedef unsigned long address_t;

enum State { RUNNING, READY, SLEEPING,   BLOCKED};

class Thread{

 private:
//    static unsigned int num_of_threads  ;
//    todo count outside the class
  address_t pc = 0;
  address_t sp = 0;
  State state = RUNNING;
  bool blocked;
  const int tid;
  char *stack = nullptr ;
  int quatums_counter = 0;
  //?
  thread_entry_point  entry_point = nullptr;
  int wake_up_time = AWAKE;
  int alloc_success = true;
 public:
  jmp_buf env{};



 public:
  Thread(const int id, bool initialize, thread_entry_point entryPoint) :tid(id)
  {
    blocked = false;
    if(initialize){
      // allocation
      stack = new (std::nothrow) char[STACK_SIZE];     //todo handle somehow failed in
      if(stack == nullptr) {
        alloc_success = false;
      }
      state = READY;
      address_t curr_sp = (address_t) stack + STACK_SIZE - sizeof(address_t);
      (this -> entry_point) = entryPoint;
      auto curr_pc = (address_t) entry_point;
      sigsetjmp(env, 1);
      (env->__jmpbuf)[JB_SP] = translate_address(curr_sp);
      (env->__jmpbuf)[JB_PC] = translate_address(curr_pc);
      sigemptyset(&env->__saved_mask);
    }
//        if(! initialize){
//            //            sigaddset(&env->__saved_mask, SIGVTALRM);// todo check line
//        }
  }


  ~Thread(){ //todo check if needed
//        std::cout << "destructor"<< std::endl;
    delete[] stack;
    stack = nullptr;
  }

 public:
//    address_t getPc() const {return pc;}
//
//    address_t getSp() const {return sp;}

  State getState() const {return state;}

//    int getTid() const {return tid;}

  int get_quatums_counter() const {return quatums_counter;}

  int getWakeUpTime() const {return wake_up_time;}

  void setBlocked(bool block) {(this->blocked) = block;}

  bool isBlocked() const {return blocked;}

//    void setPc(address_t new_pc) {(this->pc) = new_pc;}
//
//    void setSp(address_t new_sp) {(this->sp) = new_sp;}

  void setState(State new_state) { (this->state) = new_state;}

  void increase_quantums(){
    quatums_counter++;
  }

  void set_wake_up_time(int new_wake_up_time) { this->wake_up_time = new_wake_up_time;}


  bool get_alloc() const {
    return alloc_success;
  }
};
#endif //_THREADS_H_
