#ifndef MY_QUEUE_H
#define MY_QUEUE_H

#include <pthread.h>

struct list_node {
	struct list_node* next;
	struct list_node* prev;
};

void list_insert(struct list_node* node, struct list_node* new_node);
void list_remove(struct list_node* node);


struct my_queue {
	struct list_node head;
	int size;
	pthread_mutex_t mutex;
	pthread_cond_t cond;
};

void my_queue_init(struct my_queue* queue);
void my_queue_finit(struct my_queue* queue);

void my_queue_push(struct my_queue* queue, struct list_node* node);
struct list_node* my_queue_pop(struct my_queue* queue);

int my_queue_wait(struct my_queue* queue);

#endif
