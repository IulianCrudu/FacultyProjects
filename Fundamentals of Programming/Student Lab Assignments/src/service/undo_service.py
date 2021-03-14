from typing import List


class UndoService:
    def __init__(self):
        # History of program operations that support undo/redo
        self._history = []
        self._index = -1

    def record(self, operation):
        self._history = self._history[0:self._index + 1]

        self._history.append(operation)
        self._index += 1

    def undo(self):
        if self._index == -1:
            return False

        operation = self._history[self._index]
        operation.undo()
        self._index -= 1

    def redo(self):
        if self._index + 1 == len(self._history):
            return False

        self._index += 1
        operation = self._history[self._index]
        operation.redo()
        return True


class CascadedOperation:
    """
    Represents a cascaded operation (where 1 user operation corresponds to more than 1 program op)
    """

    def __init__(self, *operations):
        self._operations: List = list(operations)

    @property
    def operations(self):
        return self._operations

    def add_operations(self, *operations):
        self.operations.extend(*operations)

    def undo(self):
        print("operatiosn", self._operations)
        for oper in self._operations:
            oper.undo()

    def redo(self):
        for oper in self._operations:
            oper.redo()


class Operation:
    def __init__(self, fun_undo, fun_redo):
        self._fun_undo = fun_undo
        self._fun_redo = fun_redo

    def undo(self):
        self._fun_undo()

    def redo(self):
        self._fun_redo()


class FunctionCall:
    def __init__(self, fun_name, *fun_params, **fun_kwargs):
        self._fun_name = fun_name
        self._fun_params = fun_params
        self._fun_kwargs = fun_kwargs

    def call(self):
        self._fun_name(*self._fun_params, **self._fun_kwargs)

    def __call__(self):
        self.call()
