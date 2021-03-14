#pragma once
#include "service.h"
#include "dynamic_array.h"
#include "domain.h"
#include "category.h"

typedef struct {
    Service* service;
} UI;

UI* create_ui(Service* service);
void destroy_ui(UI* ui);

void start_app(UI* ui);
void print_menu(UI* ui);

void add_product_ui(UI* ui);
enum product_category read_product_category_ui();

void list_products_ui(UI* ui, DynamicArray* products);
void list_all_products_ui(UI* ui);
void display_products_containing_string_ui(UI* ui, int mode);
void undo_operation_ui(UI* ui);
void redo_operation_ui(UI* ui);
void display_products_that_will_expire(UI* ui);
