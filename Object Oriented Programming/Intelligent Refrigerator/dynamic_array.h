#pragma once
#include "domain.h"

typedef Product* TElement;

typedef struct {
    int capacity;
    int length;
    TElement* elements;
} DynamicArray;

DynamicArray* create_dynamic_array(int capacity);
void resize_dynamic_array(DynamicArray* dynamic_array);
void destroy_dynamic_array(DynamicArray* dynamic_array);

void add(DynamicArray* dynamic_array, TElement elem);
void delete_item(DynamicArray* dynamic_array, int position);
int search(DynamicArray* dynamic_array, TElement elem);
void update(DynamicArray* dynamic_array, TElement new_element, int position);
TElement get_element(DynamicArray * dynamic_array, int position);
void swap(DynamicArray* dynamic_array, int first_position, int second_position);
DynamicArray* duplicate(DynamicArray* dynamic_array);
