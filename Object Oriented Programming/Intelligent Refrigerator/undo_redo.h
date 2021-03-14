#pragma once

#include "dynamic_array.h"

typedef struct {
    int current_position;
    int states_length;
    int states_capacity;
    DynamicArray** states;
} UndoRedoService;

UndoRedoService* create_undo_redo(int capacity);
void destroy_undo_redo(UndoRedoService* ur_service);

int add_state(UndoRedoService* ur_service, DynamicArray* state);
void resize_states(UndoRedoService* ur_service);
DynamicArray* current_state(UndoRedoService* ur_service);
DynamicArray* undo_state(UndoRedoService* ur_service);
DynamicArray* redo_state(UndoRedoService* ur_service);
