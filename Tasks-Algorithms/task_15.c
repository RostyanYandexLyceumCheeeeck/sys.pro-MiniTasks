#include <stdio.h>
#include <stdlib.h>

#define TRUE 1
#define FALSE 0

typedef struct {
    int* data;
    size_t len;
    size_t cap;
} dynamicArr;

void nullCheck(void* ptr) {
    if (ptr == NULL) {
        printf("Нехватает динамической памяти для создания массива!!!\n");
        exit(1);
    }
}

void initEmptyDynamicArr(dynamicArr* arr) {
    arr->len = 0;
    arr->cap = 1;
    arr->data = malloc(sizeof(int));
}

void addElemToDynamicArr(dynamicArr* arr, int elem) {
    arr->data[arr->len] = elem;
    if (++arr->len == arr->cap) {
        arr->cap *= 2;
        arr->data = (int*) realloc(arr->data, arr->cap * sizeof(int));
        nullCheck(arr->data);
    }
}

int popDynamicArr(dynamicArr* arr) {
    if (!arr->len) {
        printf("Невозможно удалить элемент из пустого массива!!!\n");
        exit(2);
    }

    if (--arr->len < arr->cap / 4) {
        arr->cap /= 2;
        arr->data = (int*) realloc(arr->data, arr->cap * sizeof(int));
        nullCheck(arr->data);
    }
    return arr->data[arr->len];
}

void freeDynamicArr(dynamicArr* arr) {
    free(arr->data);
    arr->len = 0;
    arr->cap = 1;
}


int main() {
    dynamicArr arr;
    initEmptyDynamicArr(&arr);
    for (size_t i = 0; i < 10000; i++)
        addElemToDynamicArr(&arr, (int) i);
    for (size_t i = 0; i < 10000 / 4; i++)
        printf("%i ", popDynamicArr(&arr));
    freeDynamicArr(&arr);

    return 0;
}