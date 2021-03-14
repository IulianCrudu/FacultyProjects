#include "tests.h"
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

void test_domain_create_product() {
    Product* product = create_product("Product1", dairy, 10, 23, 4, 2021);
    assert(strcmp(product->name, "Product1") == 0);
    assert(product->category == dairy);
    assert(product->quantity == 10);
    assert(product->expiration_date->day == 23);
    assert(product->expiration_date->month == 4);
    assert(product->expiration_date->year == 2021);
    destroy_product(product);
}

void test_domain_set_product_name() {
    Product* product = create_product("Product2", dairy, 10, 23, 4, 2021);
    set_product_name(product, "ProductChanged");
    assert(strcmp(product->name, "ProductChanged") == 0);
    destroy_product(product);
}

void test_domain_get_product_name() {
    Product* product = create_product("Product3", dairy, 10, 23, 4, 2021);
    assert(strcmp(get_product_name(product), "Product3") == 0);
    destroy_product(product);
}

void test_domain_set_product_expiration_date() {
    Product* product = create_product("Product4", dairy, 10, 23, 4, 2021);
    set_product_expiration_date(product, 30, 5, 2022);
    assert(product->expiration_date->day == 30);
    assert(product->expiration_date->month == 5);
    assert(product->expiration_date->year == 2022);
    destroy_product(product);
}

void test_domain_get_product_expiration_date() {
    Product* product = create_product("Product5", dairy, 10, 23, 4, 2021);
    Date* expiration_date = get_product_expiration_date(product);
    assert(expiration_date->day == 23);
    assert(expiration_date->month == 4);
    assert(expiration_date->year == 2021);
    destroy_product(product);
}

void test_domain_get_product_category() {
    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    assert(product->category == dairy);
    destroy_product(product);
}

void test_da_create() {
    DynamicArray* da = create_dynamic_array(10);
    assert(da->capacity == 10);
    assert(da->length == 0);
    assert(da->elements != NULL);
    destroy_dynamic_array(da);
}

void test_da_add() {
    DynamicArray* da = create_dynamic_array(10);
    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);
    assert(da->elements[0] == product);
    destroy_dynamic_array(da);
}

void test_da_resize() {
    DynamicArray* da = create_dynamic_array(1);
    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);
    assert(da->capacity == 1);
    Product* product2 = create_product("Product7", dairy, 10, 23, 4, 2021);
    add(da, product2);
    assert(da->capacity == 2);
    assert(da->length == 2);
    assert(da->elements[1] == product2);
    Product* product3 = create_product("Product8", dairy, 10, 23, 4, 2021);
    add(da, product3);
    assert(da->capacity == 4);
    assert(da->length == 3);
    assert(da->elements[2] == product3);
    destroy_dynamic_array(da);
}

void test_da_delete_item() {
    DynamicArray* da = create_dynamic_array(1);

    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);

    Product* product2 = create_product("Product7", dairy, 10, 23, 4, 2021);
    add(da, product2);
    assert(da->length == 2);
    assert(da->capacity == 2);

    delete_item(da, 0);
    assert(da->length == 1);
    assert(da->elements[0] == product2);
    destroy_dynamic_array(da);
}

void test_da_search() {
    DynamicArray* da = create_dynamic_array(1);

    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);

    Product* product2 = create_product("Product7", dairy, 10, 23, 4, 2021);
    add(da, product2);
    assert(da->length == 2);
    assert(da->capacity == 2);

    Product* product3 = create_product("Product8", sweets, 10, 23, 4, 2021);

    assert(search(da, product2) == 1);
    assert(search(da, product3) == -1);
    destroy_dynamic_array(da);
    destroy_product(product3);
}

void test_da_update() {
    DynamicArray* da = create_dynamic_array(1);

    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);

    Product* product3 = create_product("Product8", sweets, 10, 23, 4, 2021);
    update(da, product3, 0);
    assert(da->elements[0] == product3);
    assert(strcmp(da->elements[0]->name, "Product8") == 0);

    destroy_dynamic_array(da);
}

void test_da_get_element() {
    DynamicArray* da = create_dynamic_array(1);

    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    add(da, product);
    assert(da->length == 1);

    assert(product == get_element(da, 0));

    destroy_dynamic_array(da);
}

void test_da_swap() {
    DynamicArray* da = create_dynamic_array(1);

    Product* product = create_product("Product6", dairy, 10, 23, 4, 2021);
    Product* product2 = create_product("Swapit", sweets, 10, 23, 4, 2021);
    add(da, product);
    add(da, product2);

    assert(da->length == 2);
    assert(product == get_element(da, 0));

    swap(da, 0, 1);
    assert(product2 == get_element(da, 0));
    assert(product == get_element(da, 1));

    destroy_dynamic_array(da);
}

void test_repository() {
    Repository* repository = create_repository();

    assert(repository->list != NULL);

    Product* product1 = create_product("Product1", dairy, 1, 23, 4, 2021);
    add_element(repository, product1);

    assert(repository->list->length == 1);
    assert(repository->list->elements[0] == product1);

    Product* product2 = create_product("Product2", sweets, 2, 23, 4, 2021);
    add_element(repository, product2);

    assert(repository->list->length == 2);
    assert(repository->list->elements[1] == product2);

    delete_element(repository, product1);

    assert(repository->list->length == 1);
    assert(repository->list->elements[0] == product2);

    Product* product3 = create_product("Product3", fruit, 10, 24, 5, 2024);

    update_element(repository, product3, 0);

    assert(repository->list->length == 1);
    assert(repository->list->elements[0] == product3);

    destroy_repository(repository);
}

void test_service() {
    Repository* repo = create_repository();
    Service* service = create_service(repo);

    assert(service->repository != NULL);

    // Test add product
    add_product(service, "Product1", dairy, 10, 25, 3, 2022);
    assert(service->repository->list->length == 1);

    //Test add product with the same name&category
    add_product(service, "Product1", dairy, 49, 26, 3, 2022);
    assert(service->repository->list->length == 1);
    assert(get_product(service, "Product1", dairy)->quantity == 59);
    assert(get_product(service, "Product1", dairy)->expiration_date->day == 26);

    //Test delete product
    delete_product(service, "Product1", dairy);
    assert(service->repository->list->length == 0);

    // Load fixtures
    char names[10][25] = {"Bread", "Chocolate", "Milk", "Milk2", "Biscuits", "Cereals", "Apple", "Orange", "Banana", "Egg"};

    for(int i=0; i<10;i++) {
        add_product(service, names[i], i%4, 20 - i+2, i*3+1, i+1, 2021);
    }
    assert(service->repository->list->length == 10);
    DynamicArray* listed_products = list_products(service);
    assert(listed_products->length == 10);

    DynamicArray* products_with_string1 = products_containing_string(service, "" ,1);
    assert(products_with_string1->length == 10);
    assert(strcmp(products_with_string1->elements[0]->name, "Egg") == 0);
    assert(strcmp(products_with_string1->elements[9]->name, "Bread") == 0);

    DynamicArray* products_with_string2 = products_containing_string(service, "a", 2);
    assert(products_with_string2->length == 5);
    assert(strcmp(products_with_string2->elements[0]->name, "Banana") == 0);
    assert(strcmp(products_with_string2->elements[4]->name, "Orange") == 0);

    DynamicArray* products_expiring1 = list_expiring_products(service, "", 45);
    assert(products_expiring1->length == 4);
    assert(strcmp(products_expiring1->elements[0]->name, "Bread") == 0);
    assert(strcmp(products_expiring1->elements[3]->name, "Milk2") == 0);

    DynamicArray* products_expiring2 = list_expiring_products(service, "dairy", 100);
    assert(products_expiring2->length == 2);
    assert(strcmp(products_expiring2->elements[0]->name, "Bread") == 0);
    assert(strcmp(products_expiring2->elements[1]->name, "Biscuits") == 0);

    free(listed_products->elements);
    free(listed_products);

    free(products_with_string1->elements);
    free(products_with_string1);

    free(products_with_string2->elements);
    free(products_with_string2);

    free(products_expiring1->elements);
    free(products_expiring1);

    free(products_expiring2->elements);
    free(products_expiring2);

    destroy_service(service);
}

void test_create_undo_redo_service() {
    UndoRedoService* ur_service = create_undo_redo(10);
    destroy_undo_redo(ur_service);
}

void test_undo_redo() {
    Repository* repository = create_repository();
    Service* service = create_service(repository);

    assert(service->undo_redo != NULL);

    // Test states are added
    add_product(service, "Product1", dairy, 10, 25, 3, 2022);
    assert(service->undo_redo->current_position == 1);
    assert(service->undo_redo->states_length == 2);

    add_product(service, "Product2", dairy, 10, 25, 3, 2022);
    assert(service->undo_redo->current_position == 2);
    assert(service->undo_redo->states_length == 3);

    // Test can undo
    undo_operation(service);
    assert(service->repository->list->length == 1);
    assert(strcmp(service->repository->list->elements[0]->name,"Product1") == 0);

    assert(service->undo_redo->current_position == 1);
    assert(service->undo_redo->states_length == 3);

    // Add another product in intermediary state
    add_product(service, "Product3", dairy, 10, 25, 3, 2022);

    assert(service->undo_redo->current_position == 2);
    assert(service->undo_redo->states_length == 3);

    // Add another product and test undo twice and then a redo
    add_product(service, "Product4", dairy, 10, 25, 3, 2022);

    assert(service->undo_redo->current_position == 3);
    assert(service->undo_redo->states_length == 4);

    undo_operation(service);
    undo_operation(service);

    assert(service->repository->list->length == 1);
    assert(strcmp(service->repository->list->elements[0]->name,"Product1") == 0);

    assert(service->undo_redo->current_position == 1);
    assert(service->undo_redo->states_length == 4);

    redo_operation(service);
    assert(service->repository->list->length == 2);
    assert(strcmp(service->repository->list->elements[0]->name,"Product1") == 0);
    assert(strcmp(service->repository->list->elements[1]->name,"Product3") == 0);

    assert(service->undo_redo->current_position == 2);
    assert(service->undo_redo->states_length == 4);

    // Test undo and redo for update
    update_product(service, "Product3", dairy, 39, 26, 3, 2022);

    Product* product3 = get_product(service, "Product3", dairy);
    assert(product3->quantity == 39);

    undo_operation(service);

    Product* redo_product = get_product(service, "Product3", dairy);
    assert(redo_product->quantity == 10);

    redo_operation(service);

    Product* undo_product = get_product(service, "Product3", dairy);
    assert(undo_product->quantity == 39);

    // Test delete undo/redo

    delete_product(service, "Product3", dairy);
    assert(service->repository->list->length == 1);

    undo_operation(service);
    assert(service->repository->list->length == 2);

    redo_operation(service);
    assert(service->repository->list->length == 1);

    destroy_service(service);
}

void test_nothing_to_undo_redo() {
    Repository* repository = create_repository();
    Service* service = create_service(repository);

    assert(redo_operation(service) == 0);
    assert(undo_operation(service) == 0);

    add_product(service, "Product1", sweets, 10, 3, 3, 2021);
    assert(redo_operation(service) == 0);
    undo_operation(service);
    assert(undo_operation(service) == 0);

    destroy_service(service);
}

void run_all_tests() {
    printf("Starting tests... \n");

    test_domain_create_product();
    test_domain_set_product_name();
    test_domain_get_product_name();
    test_domain_set_product_expiration_date();
    test_domain_get_product_expiration_date();
    test_domain_get_product_category();

    test_da_create();
    test_da_add();
    test_da_resize();
    test_da_delete_item();
    test_da_search();
    test_da_update();
    test_da_get_element();
    test_da_swap();

    test_repository();

    test_service();

    test_create_undo_redo_service();
    test_undo_redo();
    test_nothing_to_undo_redo();

    printf("Tests finished!\n");
}