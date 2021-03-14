#include "repository.h"
#include "dynamic_array.h"
#include <stdlib.h>
#include <string.h>

/// Creates a new repository
/// \return the new repository
Repository* create_repository() {
    Repository* repository = (Repository*)malloc(sizeof(Repository));

    if(repository == NULL) {
        return NULL;
    }

    repository->list = create_dynamic_array(10);

    if(repository->list == NULL) {
        return NULL;
    }

    return repository;
}

/// Deletes a repository from memory
/// \param repository
void destroy_repository(Repository* repository) {
    destroy_dynamic_array(repository->list);
    repository->list = NULL;
    free(repository);
}

/// Returns the repository's size
/// \param repository
/// \return
int get_size(Repository* repository) {
    if(repository == NULL) {
        return -1;
    }
    if(repository->list == NULL) {
        return -1;
    }

    return repository->list->length;
}

/// Adds a new element to the repository
/// \param repository
/// \param element
/// \return 1 if the addition was successful, 0 otherwise
int add_element(Repository* repository, TElement element) {
    if(repository == NULL) {
        return 0;
    }

    if(element == NULL) {
        return 0;
    }

    if(search(repository->list, element) >= 0) {
        return 0;
    }

    add(repository->list, element);
    return 1;
}

/// Deletes a given element from the repository
/// \param repository
/// \param element
/// \return 1 if the addition was successful, 0 otherwise
int delete_element(Repository* repository, TElement element) {
    if(repository == NULL) {
        return 0;
    }

    if(element == NULL) {
        return 0;
    }

    int position = search(repository->list, element);

    if(position < 0) {
        return 0;
    }

    delete_item(repository->list, position);
    return 1;
}

/// Searches an element in the repository by name and category
/// \param repository
/// \param name
/// \param category
/// \return the element looked for or NULL
Product* search_element(Repository* repository, char* name, enum product_category category) {
    DynamicArray* da = repository->list;
    for(int i=0; i < da->length; i++) {
        Product* product = da->elements[i];
        if(strcmp(get_product_name(product), name) == 0 && get_product_category(product) == category) {
            return product;
        }
    }

    return NULL;
}

/// Returns an element's position in the repository by name and category
/// \param repository
/// \param name
/// \param category
/// \return
int search_element_position(Repository* repository, char* name, enum product_category category) {
    DynamicArray* da = repository->list;
    for(int i=0; i < da->length; i++) {
        Product* product = da->elements[i];
        if(strcmp(get_product_name(product), name) == 0 && get_product_category(product) == category) {
            return i;
        }
    }

    return -1;
}

/// Updates the element from a position
/// \param repository
/// \param new_element
/// \param position
void update_element(Repository* repository, TElement new_element, int position) {
    update(repository->list, new_element, position);
}

/// Returns a new dynamic array containing a copy of the new elements
/// \param repository
/// \return
DynamicArray* get_all_elements(Repository* repository) {
    if(repository == NULL) {
        return NULL;
    }

    DynamicArray* new_da = create_dynamic_array(repository->list->length);

    for(int i = 0; i < repository->list->length; i++) {
        Product* element = get_element(repository->list, i);

        add(new_da, element);
    }

    return new_da;
}