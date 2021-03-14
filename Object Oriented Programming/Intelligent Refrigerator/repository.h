#pragma once

#include "domain.h"
#include "dynamic_array.h"

typedef struct {
    DynamicArray* list;
} Repository;

Repository* create_repository();
void destroy_repository(Repository* repository);

int add_element(Repository* repository, TElement element);
int delete_element(Repository* repository, TElement element);
void update_element(Repository* repository, TElement element, int position);
Product* search_element(Repository* repository, char* name, enum product_category category);
int search_element_position(Repository* repository, char* name, enum product_category category);
int get_size(Repository* repository);
DynamicArray* get_all_elements(Repository* repository);
