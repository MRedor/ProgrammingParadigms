#include "my_queue.h"

void list_insert(struct list_node* node, struct list_node* new) {
	new->prev = node;
	new->next = node->next;
	node->next->prev = new;
	node->next = new;
}

void list_remove(struct list_node* node) {
	node->prev->next = node->next;
	node->next->prev = node->prev;
}

void my_queue_init(struct my_queue* queue) {
	queue->size = 0;
	queue->head.prev = &queue->head;
	queue->head.next = &queue->head;
	pthread_mutex_init(&queue->mutex, NULL);
	pthread_cond_init(&queue->cond, NULL);
}

void my_queue_finit(struct my_queue* queue) {
	pthread_cond_destroy(&queue->cond);
	pthread_mutex_destroy(&queue->mutex);
}

void my_queue_push(struct my_queue* queue, struct list_node* node) {
	pthread_mutex_lock(&queue->mutex);
	list_insert(&queue->head, node);
	queue->size += 1;
	pthread_cond_signal(&queue->cond);
	pthread_mutex_unlock(&queue->mutex);
}

struct list_node* my_queue_pop(struct my_queue* queue) {
	struct list_node* node;
	pthread_mutex_lock(&queue->mutex);
	if (!queue->size) {
		node = NULL;
	} else {
		node = queue->head.prev;
		list_remove(node);
		queue->size -= 1;
	}

	pthread_mutex_unlock(&queue->mutex);
	return node;
}

int my_queue_wait(struct my_queue *queue) {
	pthread_mutex_lock(&queue->mutex);
	while (!&queue->size) {
		pthread_cond_wait(&queue->cond, &queue->mutex);
	}
	pthread_mutex_unlock(&queue->mutex);
	if (!&queue->size) {
		return 1;
	}
	return 0;
}