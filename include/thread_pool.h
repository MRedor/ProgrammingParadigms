#ifndef MY_THREAD_POOL_H
#define MY_THREAD_POOL_H

#include <stdbool.h>
#include <pthread.h>
#include "my_queue.h"

struct Task {
    struct list_node node;
    void (*f)(void*);
    void* arg;

    bool finished;

    pthread_mutex_t mutex;
    pthread_cond_t cond;
};

struct ThreadPool {
   unsigned int threads_nm;
   pthread_t* threads;
   struct my_queue tasks;
};

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm);
void thpool_submit(struct ThreadPool* pool, struct Task* task);
void thpool_wait(struct Task* task);
void thpool_wait_for_all(struct Task* task);
void thpool_finit(struct ThreadPool* pool);

#endif
