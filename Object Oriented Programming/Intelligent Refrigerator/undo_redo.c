#include "undo_redo.h"
#include <stdlib.h>

UndoRedoService* create_undo_redo(int capacity) {
    UndoRedoService* ur_service = (UndoRedoService*)malloc(sizeof(UndoRedoService));
    if(ur_service == NULL) {
        return NULL;
    }

    DynamicArray** da_array = (DynamicArray**)malloc(sizeof(DynamicArray*) * capacity);
    if(da_array == NULL) {
        return NULL;
    }

    ur_service->current_position = -1;
    ur_service->states_length = 0;
    ur_service->states_capacity = capacity;
    ur_service->states = da_array;

    return ur_service;
}

void destroy_undo_redo(UndoRedoService* ur_service) {
    if(ur_service->states_length) {
        for (int i = 0; i < ur_service->states_length; i++) {
            destroy_dynamic_array(ur_service->states[i]);
        }
    }

    free(ur_service->states);
    free(ur_service);
}

void resize_states(UndoRedoService* ur_service) {
    DynamicArray** da_array = (DynamicArray**)malloc(sizeof(DynamicArray*) * ur_service->states_capacity * 2);

    for(int i = 0; i < ur_service->states_length; i++) {
        da_array[i] = ur_service->states[i];
    }

    free(ur_service->states);
    ur_service->states = da_array;
    ur_service->states_capacity = ur_service->states_capacity * 2;
}

int add_state(UndoRedoService* ur_service, DynamicArray* state) {
    if(ur_service == NULL) {
        return 0;
    }

    for(int i = ur_service->current_position + 1; i < ur_service->states_length;i++)
        destroy_dynamic_array(ur_service->states[i]);

    ur_service->states_length = ur_service->current_position + 1;

    if(ur_service->states_length == ur_service->states_capacity)
        resize_states(ur_service);

    ur_service->states[ur_service->states_length] = state;
    ur_service->states_length = ur_service->states_length + 1;
    ur_service->current_position = ur_service->current_position + 1;
    return 1;
}

DynamicArray* current_state(UndoRedoService* ur_service) {
    return ur_service->states[ur_service->current_position];
}

DynamicArray* undo_state(UndoRedoService* ur_service) {
    if(ur_service->current_position <= 0)
        return NULL;

    ur_service->current_position = ur_service->current_position - 1;
    return ur_service->states[ur_service->current_position];
}

DynamicArray* redo_state(UndoRedoService* ur_service) {
    if(ur_service->current_position == ur_service->states_length - 1)
        return NULL;

    ur_service->current_position = ur_service->current_position + 1;
    return ur_service->states[ur_service->current_position];
}