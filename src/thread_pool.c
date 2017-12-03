#include <stdlib.h>
#include <stdbool.h>
#include <pthread.h>
#include "my_queue.h"
#include "thread_pool.h"

void* thpool_process(void* arg) {
    struct ThreadPool* pool = arg;
    struct Task* task;
    while (1) {
        my_queue_wait(&pool->tasks);
        task = (struct Task*)my_queue_pop(&pool->tasks);
        if (!task) {
            continue;
        }
        if (!task->f) {
            break;
        }
        task->f(task->arg);
        pthread_mutex_lock(&task->mutex);
        task->finished = 1;
        pthread_cond_signal(&task->cond);
        pthread_mutex_unlock(&task->mutex);
    }
    return NULL;
}

void thpool_init(struct ThreadPool* pool, unsigned int threads_nm) {
    pool->threads_nm = threads_nm;
    pool->threads = malloc(sizeof(pthread_t) * threads_nm);
    my_queue_init(&pool->tasks);
    for (unsigned int i = 0; i < threads_nm; i++) {
        pthread_create(&pool->threads[i], NULL, thpool_process, pool);
    }
}

void thpool_submit(struct ThreadPool* pool, struct Task* task) {
    pthread_mutex_init(&task->mutex, NULL);
    pthread_cond_init(&task->cond, NULL);
    task->finished = false;
    my_queue_push(&pool->tasks, &task->node);
}

void thpool_wait(struct Task* task) {
    pthread_mutex_lock(&task->mutex);
    while (!task->finished) {
        pthread_cond_wait(&task->cond, &task->mutex);
    }
    pthread_mutex_unlock(&task->mutex);
}

void thpool_finit(struct ThreadPool* pool) {
    struct Task* tasks = malloc(sizeof(struct Task) * pool->threads_nm);
    for (unsigned int i = 0; i < pool->threads_nm; i++) {
        tasks[i].f = NULL;
        tasks[i].arg = NULL;
        thpool_submit(pool, &tasks[i]);
    }

    for (unsigned int i = 0; i < pool->threads_nm; i++) {
        pthread_join(pool->threads[i], NULL);
    }
    free(pool->threads);
    free(tasks);
    my_queue_finit(&pool->tasks);
}
