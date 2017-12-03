#include <stdlib.h>
#include "thread_pool.h"
#include "my_qsort.h"
#include <stdio.h>

int main(int argc, char **argv) {
    struct ThreadPool pool;
    struct Task* task;

    int threads = atoi(argv[1]);
    int size = atoi(argv[2]);
    int depth = atoi(argv[3]);

    int* array = malloc(sizeof(int) * size);
    
    srand(42);
    for (int i = 0; i < size; i++){
        array[i] = rand();
    }

    task = create_task(array, size, depth, &pool);

    thpool_init(&pool, threads);
    thpool_submit(&pool, task);
    wait_end(task);
    thpool_finit(&pool);

    for (int i = 0; i < size - 1; i++) {
        //printf("%d\n", array[i]);
        if (array[i] > array[i + 1]){
            printf("%s\n", ":(");
            return 0;
        }
    }
    printf("%s\n", "OK");

    free(array);
    return 0;
}
