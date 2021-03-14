#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "service.h"

/// Creates a new service with the given repository
/// \param repository
/// \return the new service or null
Service* create_service(Repository* repository) {
    if(repository == NULL) {
        return NULL;
    }

    Service* service = (Service*)malloc(sizeof(Service));

    if(service == NULL) {
        return NULL;
    }

    service->repository = repository;

    UndoRedoService* undo_redo = create_undo_redo(10);
    service->undo_redo = undo_redo;

    add_state(service->undo_redo, duplicate(service->repository->list));

    return service;
}

/// Destroys the service from memory
/// \param service
void destroy_service(Service* service) {
    if(service == NULL) {
        return;
    }

    destroy_repository(service->repository);
    service->repository = NULL;

    destroy_undo_redo(service->undo_redo);
    service->undo_redo = NULL;

    free(service);
}

/// Adds a product to the service
/// \param service
/// \param name
/// \param category
/// \param quantity
/// \param day
/// \param month
/// \param year
/// \return 1 if the addition was successful, 0 otherwise
int add_product(Service* service, char* name, enum product_category category, int quantity, int day, int month, int year) {
    if(service == NULL) {
        return 0;
    }

    Product* existing_product = get_product(service, name, category);
    if(existing_product != NULL) {
        update_product(service, name, category, existing_product->quantity + quantity, day, month, year);
        return 1;
    }

    Product* product = create_product(name, category, quantity, day, month, year);
    if(product == 0) {
        return 0;
    }

    int product_added = add_element(service->repository, product);
    if(!product_added) {
        return 0;
    }

    add_state(service->undo_redo, duplicate(service->repository->list));

    return product_added;
}

/// Deletes a product from the service by name and category
/// \param service
/// \param name
/// \param category
/// \return 1 if the deletion was successful, 0 otherwise
int delete_product(Service* service, char* name, enum product_category category) {
    if(service == NULL) {
        return 0;
    }

    Product* product = search_element(service->repository, name, category);
    if(product == NULL) {
        return 0;
    }

    int product_deleted = delete_element(service->repository, product);
    if(!product_deleted) {
        return 0;
    }

    add_state(service->undo_redo, duplicate(service->repository->list));

    return product_deleted;
}

/// Update's a product's quantity and/or the expiration date
/// \param service
/// \param name
/// \param category
/// \param quantity
/// \param day
/// \param month
/// \param year
/// \return 1 if the update was successful, 0 otherwise
int update_product(Service* service, char* name, enum product_category category, int quantity, int day, int month, int year) {
    if(service == NULL) {
        return 0;
    }
    int product_position = search_element_position(service->repository, name, category);

    if(product_position < 0) {
        return 0;
    }

    Product* new_product = create_product(name, category, quantity, day, month, year);
    update_element(service->repository, new_product, product_position);

    add_state(service->undo_redo, duplicate(service->repository->list));

    return 1;
}

/// Returns the product that has the given name and category
/// \param service
/// \param name
/// \param category
/// \return the product or NULL
Product* get_product(Service* service, char* name, enum product_category category) {
    return search_element(service->repository, name, category);
}

/// Returns a duplicated dynamic array containing all the products
/// \param service
/// \return
DynamicArray* list_products(Service* service) {
    if(service == NULL) {
        return NULL;
    }

    return get_all_elements(service->repository);
}

/// Sorts the products by quantity
/// \param service
/// \param products
/// \return
DynamicArray* products_sorted_by_quantity(Service* service, DynamicArray* products) {
    if(service == NULL) {
        return NULL;
    }

    if(products == NULL) {
        return NULL;
    }

    int products_length = products->length;
    for(int i = 0;i < products_length - 1; i++) {
        for(int j = i; j < products_length; j++) {
            Product* product_i = get_element(products, i);
            Product* product_j = get_element(products, j);

            if(product_i->quantity > product_j->quantity) {
                swap(products, i, j);
            }
        }
    }

    return products;
}

/// Sorts the products by name
/// \param service
/// \param products
/// \return
DynamicArray* products_sorted_by_name(Service* service, DynamicArray* products) {
    if(service == NULL) {
        return NULL;
    }

    if(products == NULL) {
        return NULL;
    }

    int products_length = products->length;
    for(int i = 0;i < products_length - 1; i++) {
        for(int j = i; j < products_length; j++) {
            Product* product_i = get_element(products, i);
            Product* product_j = get_element(products, j);

            if(strcmp(product_i->name, product_j->name) > 0) {
                swap(products, i, j);
            }
        }
    }

    return products;
}

/// Returns a duplicated dyamic array containing the products that have a given string
/// \param service
/// \param string
/// \param mode
/// \return If mode is 1 then the products sorted by quantity, if mode is 2 then the products sorted by name
DynamicArray* products_containing_string(Service* service, char* string, int mode) {
    if(service == NULL) {
        return NULL;
    }

    DynamicArray* all_products = list_products(service);
    if(strlen(string) == 0) {
        if(mode == 1)
            return products_sorted_by_quantity(service, all_products);
        else
            return products_sorted_by_name(service, all_products);
    }

    DynamicArray* new_da = create_dynamic_array(all_products->length);
    for(int i = 0; i < all_products->length;i++) {
        Product* product = get_element(all_products, i);
        char* product_name = get_product_name(product);
        if(strstr(product_name, string) != NULL) {
            add(new_da, product);
        }
    }
    free(all_products->elements);
    free(all_products);
    if (mode == 1)
        return products_sorted_by_quantity(service, new_da);
    else
        return products_sorted_by_name(service, new_da);
}

/// Undos the previous operation
/// \param service
/// \return
int undo_operation(Service* service) {
    DynamicArray* next_state = undo_state(service->undo_redo);

    if(next_state == NULL)
        return 0;

    destroy_dynamic_array(service->repository->list);
    service->repository->list = duplicate(next_state);

    return 1;
}

/// Redos the last undo
/// \param service
/// \return
int redo_operation(Service* service) {
    DynamicArray* prev_state = redo_state(service->undo_redo);

    if(prev_state == NULL) {
        return 0;
    }

    destroy_dynamic_array(service->repository->list);
    service->repository->list = duplicate(prev_state);

    return 1;
}

/// Returns a new dynamic array with all the products from a category
/// \param service
/// \param category
/// \return
DynamicArray* get_products_for_category(Service* service, enum product_category category) {
    DynamicArray* products = create_dynamic_array(service->repository->list->length);

    for(int i = 0; i < service->repository->list->length; i++) {
        Product* product = get_element(service->repository->list, i);
        if(category == product->category) {
            add(products, product);
        }
    }

    return products;
}

/// Returns a Date object for today
/// \param service
/// \return Date object for today
Date* get_today(Service* service) {
    //http://www.java2s.com/Code/C/Development/Converttmstructuretotimetvaluehowtousemktime.htm
    //TODO: this needs to be destroyed
    time_t rawtime;
    struct tm *timeinfo;

    time(&rawtime);
    timeinfo = localtime(&rawtime);

    Date* date = (Date*)malloc(sizeof(Date));
    date->day = timeinfo->tm_mday;
    date->month = timeinfo->tm_mon + 1;
    date->year = timeinfo->tm_year + 1900;

    return date;
}

/// Returns a new dynamic array with all the products from the given da that expire in x days
/// \param service
/// \param da
/// \param days
/// \return a new dynamic array with all the products from the given da that expire in x days
DynamicArray* get_products_that_expire_in_x_days(Service* service, DynamicArray* da, int days) {
    Date* today = get_today(service);
    Date* date_to_expire = (Date*)malloc(sizeof(Date));

    DynamicArray* new_da = create_dynamic_array(da->length);

    date_to_expire->day = today->day + days;
    if(date_to_expire->day % 30 != 0) {
        date_to_expire->month = (int)(date_to_expire->day / 30) + today->month;
        date_to_expire->day = date_to_expire->day % 30;
    } else {
        date_to_expire->month = today->month + (int)(date_to_expire->day / 30 ) - 1;
        date_to_expire->day = 30;
    }

    if(date_to_expire->month % 12 != 0) {
        date_to_expire->year = today->year + (int)(date_to_expire->month / 12);
        date_to_expire->month = date_to_expire->month % 12;
    } else {
        date_to_expire->year = today->year + (int)(date_to_expire->month / 12) - 1;
        date_to_expire->month = 12;
    }

    for(int i = 0; i < da->length; i++) {
        Product* product = get_element(da, i);
        Date* expiration_date = get_product_expiration_date(product);
        if(expiration_date->year < date_to_expire->year) {
            add(new_da, product);
            continue;
        }

        if(expiration_date->year > date_to_expire->year)
            continue;

        if(expiration_date->month < date_to_expire->month) {
            add(new_da, product);
            continue;
        }

        if(expiration_date->month > date_to_expire->month)
            continue;

        if(expiration_date->day < date_to_expire->day) {
            add(new_da, product);
            continue;
        }

        if(expiration_date->day > date_to_expire->day)
            continue;

        add(new_da, product);
    }

    free(da->elements);
    free(da);
    free(date_to_expire);
    free(today);

    return new_da;
}

/// Gets all the products from a given category or from all that expire in expiring_days days
/// \param service
/// \param category
/// \param expiring_days
/// \return
DynamicArray* list_expiring_products(Service* service, char* category, int expiring_days) {

    DynamicArray* category_products = list_products(service);
    if(strlen(category) != 0) {
        enum product_category product_category = get_category_int(category);
        free(category_products->elements);
        free(category_products);
        category_products = get_products_for_category(service, product_category);
    }

    return get_products_that_expire_in_x_days(service, category_products, expiring_days);
}
