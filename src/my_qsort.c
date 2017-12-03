#include <stdio.h>
#include "my_qsort.h"
#include "thread_pool.h"

int cmp(const void* a, const void* b){
    int x = *(int*)a;
    int y = *(int*)b;
    return x - y;
}

struct sorted* create_nw(int* a, int size, int dep, struct ThreadPool* pool){
    struct sorted *nw;
    nw = malloc(sizeof(struct sorted));

    nw->a = a;
    nw->size = size;
    nw->dep = dep;
    nw->pool = pool;
    nw->first = NULL;
    nw->second = NULL;
    return nw;
}

struct Task* create_task(int* a, int size, int dep, struct ThreadPool* pool){
    struct Task* task = malloc(sizeof(struct Task));
    task->arg = (void*)create_nw(a, size, dep, pool);
    task->f = my_qsort;
    return task;
}

void my_qsort(void* data){
    struct sorted* nw = data;
    int j = 0; 
    int mid = nw->a[nw->size / 2];

    if (nw->dep == 0) {
        qsort(nw->a, nw->size, sizeof(int), cmp);
        return;
    }

    for (int i = 0; i < nw->size; i++) {
        if (nw->a[i] <= mid) {
            int q;
            q = *(nw->a + i);
            *(nw->a + i) = *(nw->a + j);
            *(nw->a + j) = q;
            j++;
        } 
    }

    struct Task* task1 = create_task(nw->a, j, nw->dep - 1, nw->pool);
    struct Task* task2 = create_task(nw->a + j, nw->size - j, nw->dep - 1, nw->pool);
    nw->first = task1;
    nw->second = task2;
    thpool_submit(nw->pool, task1);
    thpool_submit(nw->pool, task2);
}


void wait_end(struct Task* task){
    if (!task) {
        return;
    }
    if (!task->finished) {
        thpool_wait(task);
    }
    wait_end(((struct sorted*)task->arg)->first);
    wait_end(((struct sorted*)task->arg)->second);
    
    free(task->arg);
    free(task);
}