#pragma once
#include "repository.h"
#include "domain.h"
#include "undo_redo.h"

typedef struct {
    Repository* repository;
    UndoRedoService* undo_redo;
} Service;

Service* create_service(Repository* repository);
void destroy_service(Service* service);

int add_product(Service* service, char* name, enum product_category category, int quantity, int day, int month, int year);
int delete_product(Service* service, char* name, enum product_category category);
int update_product(Service* service, char* name, enum product_category category, int quantity, int day, int month, int year);
Product* get_product(Service* service, char* name, enum product_category category);
DynamicArray* products_sorted_by_quantity(Service* service, DynamicArray* products);
DynamicArray* products_sorted_by_name(Service* service, DynamicArray* products);
DynamicArray* list_products(Service* service);
DynamicArray* products_containing_string(Service* service, char* string, int mode);
DynamicArray* get_products_for_category(Service* service, enum product_category category);
DynamicArray* get_products_that_expire_in_x_days(Service* service, DynamicArray* da, int days);
Date* get_today(Service* service);
DynamicArray* list_expiring_products(Service* service, char* category, int expiring_days);

int redo_operation(Service* service);
int undo_operation(Service* service);
