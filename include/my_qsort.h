#ifndef MY_SORT_H
#define MY_SORT_H

#include <stdlib.h>
#include "my_queue.h"
#include "thread_pool.h"

struct sorted {
    int* a;
    int size;

    int dep;
    struct Task* first;
    struct Task* second;
    struct ThreadPool* pool;
};

int cmp(const void* a, const void* b);
struct Task* create_task(int* a, int size, int dep, struct ThreadPool* pool);
void my_qsort(void* data);

void wait_end(struct Task* task);

#endif
