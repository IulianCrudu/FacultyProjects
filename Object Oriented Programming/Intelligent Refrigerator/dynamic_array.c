#include "dynamic_array.h"
#include <stdlib.h>
#include <string.h>

/// Creates a new dynamic array with a given capacity
/// \param capacity
/// \return The dynamic array
DynamicArray* create_dynamic_array(int capacity) {
    DynamicArray* dynamic_array = (DynamicArray*)malloc(sizeof(DynamicArray));

    if(dynamic_array == NULL) {
        return NULL;
    }

    dynamic_array->capacity = capacity;
    dynamic_array->length = 0;
    dynamic_array->elements = (TElement*)malloc(sizeof(TElement) * capacity);

    if(dynamic_array->elements == NULL) {
        return NULL;
    }

    return dynamic_array;
}

/// Deletes the dynamic array from the memory
/// \param dynamic_array
void destroy_dynamic_array(DynamicArray* dynamic_array) {
    if(dynamic_array == NULL) {
        return;
    }

    if(dynamic_array->length) {
        for(int i = 0; i < dynamic_array->length; i++) {
            destroy_product(dynamic_array->elements[i]);
        }
    }

    free(dynamic_array->elements);

    free(dynamic_array);
}

/// Resizes the dynamic array to contain more elements
/// \param dynamic_array
void resize_dynamic_array(DynamicArray* dynamic_array) {
    // Create a new array with double position
    // Copy the elements from the old to the new
    // Free the old array
    // use the new one
    if (dynamic_array == NULL) {
        return;
    }

    TElement* new_elements = (TElement*)malloc(sizeof(TElement) * dynamic_array->capacity * 2);

    for(int i = 0; i < dynamic_array->length; i++) {
        new_elements[i] = dynamic_array->elements[i];
    }

    free(dynamic_array->elements);
    dynamic_array->elements = new_elements;

    dynamic_array->capacity = dynamic_array->capacity * 2;
}

/// Add a new element to the Da
/// \param dynamic_array
/// \param element
void add(DynamicArray* dynamic_array, TElement element) {
    if (dynamic_array == NULL) {
        return;
    }
    if(dynamic_array->elements == NULL) {
        return;
    }

    if(dynamic_array->length == dynamic_array->capacity) {
        resize_dynamic_array(dynamic_array);
    }

    dynamic_array->elements[dynamic_array->length++] = element;
}

/// Deletes an element from a given position
/// \param dynamic_array
/// \param position
void delete_item(DynamicArray* dynamic_array, int position) {
    if(dynamic_array == NULL) {
        return;
    }
    if(dynamic_array->length <= position || position < 0) {
        return;
    }

    TElement element = dynamic_array->elements[position];

    for (int i = position + 1; i < dynamic_array->length; i++) {
        dynamic_array->elements[i - 1] = dynamic_array->elements[i];
    }
    destroy_product(element);

    dynamic_array->length = dynamic_array->length - 1;
}

/// Returns the position of an element
/// \param dynamic_array
/// \param element
/// \return The position of the element or -1 if not found
int search(DynamicArray* dynamic_array, TElement element) {
    if (dynamic_array == NULL) {
        return -1;
    }

    if(element == NULL) {
        return -1;
    }

    char* element_name = get_product_name(element);
    enum product_category element_category = get_product_category(element);

    for(int i = 0;i < dynamic_array->length; i++) {
        TElement current_element = dynamic_array->elements[i];
        if(strcmp(get_product_name(current_element), element_name) == 0 && element_category == get_product_category(current_element)) {
            return i;
        }
    }

    return -1;
}

/// Returns the element from a given position
/// \param dynamic_array
/// \param position
/// \return The element from the position or NULL
TElement get_element(DynamicArray* dynamic_array, int position) {
    if(dynamic_array == NULL) {
        return NULL;
    }

    if(dynamic_array->elements == NULL) {
        return NULL;
    }

    if (position < 0) {
        return NULL;
    }

    return dynamic_array->elements[position];
}

/// Updates the element from a position
/// \param dynamic_array
/// \param new_element
/// \param position
void update(DynamicArray* dynamic_array, TElement new_element, int position) {
    if(dynamic_array == NULL) {
        return;
    }

    if(position < 0 || position >= dynamic_array->length) {
        return;
    }

    if(new_element == NULL) {
        return;
    }

    destroy_product(get_element(dynamic_array, position));
    dynamic_array->elements[position] = new_element;
}

/// Swaps 2 elements from 2 positions
/// \param dynamic_array
/// \param first_position
/// \param second_position
void swap(DynamicArray* dynamic_array, int first_position, int second_position) {
    if(dynamic_array == NULL) {
        return;
    }

    TElement aux_element = dynamic_array->elements[first_position];
    dynamic_array->elements[first_position] = dynamic_array->elements[second_position];
    dynamic_array->elements[second_position] = aux_element;
}

/// Returns a duplicated Dynamic Array
/// \param dynamic_array
/// \return
DynamicArray* duplicate(DynamicArray* dynamic_array) {
    DynamicArray* new_da = create_dynamic_array(dynamic_array->capacity);

    for(int i=0; i<dynamic_array->length;i++) {
        TElement element = dynamic_array->elements[i];
        new_da->elements[i] = create_product(
            element->name,
            element->category,
            element->quantity,
            element->expiration_date->day,
            element->expiration_date->month,
            element->expiration_date->year
       );
    }
    new_da->length = dynamic_array->length;

    return new_da;
}