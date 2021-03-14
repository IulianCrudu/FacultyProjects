#include "domain.h"
#include "dynamic_array.h"
#include "repository.h"
#include "service.h"
#include "undo_redo.h"

void test_domain_create_product();
void test_domain_set_product_name();
void test_domain_get_product_name();
void test_domain_set_product_expiration_date();
void test_domain_get_product_expiration_date();
void test_domain_get_product_category();

void test_da_create();
void test_da_add();
void test_da_resize();
void test_da_delete_item();
void test_da_search();
void test_da_update();
void test_da_get_element();
void test_da_swap();

void test_repository();

void test_service();

void test_create_undo_redo_service();
void test_undo_redo();
void test_nothing_to_undo_redo();

void run_all_tests();