all: main

main: main.o my_queue.o my_qsort.o thread_pool.o
	gcc main.o my_queue.o my_qsort.o thread_pool.o -I include/ -lpthread -o pqsort

main.o: src/main.c
	gcc -c src/main.c -I include/ -o main.o

my_queue.o: src/my_queue.c include/my_queue.h
	gcc -c src/my_queue.c -I include/ -o my_queue.o

my_qsort.o: src/my_qsort.c include/my_qsort.h
	gcc -c src/my_qsort.c -I include/ -o my_qsort.o


thread_pool.o: src/thread_pool.c include/thread_pool.h
	gcc -c src/thread_pool.c -I include/ -o thread_pool.o


clean:
	rm *.o pqsort

.PHONY: clean
