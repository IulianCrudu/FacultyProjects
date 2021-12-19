package Model.adt;

import Exceptions.DataTypeException;
import Exceptions.MyException;

import java.util.Stack;

public class MyStack<T> implements IStack<T> {
    Stack<T> stack;

    public MyStack() {
        this.stack = new Stack<>();
    }

    @Override
    public T pop() throws MyException {
        if(this.isEmpty()) {
            throw new DataTypeException("Nothing to pop. Stack is empty");
        }
        return this.stack.pop();
    }

    @Override
    public void push(T v) {
        this.stack.push(v);
    }

    @Override
    public boolean isEmpty() {
        return this.stack.isEmpty();
    }

    @Override
    public String toString() {
        return this.stack.toString();
    }

    @Override
    public String getStackLog() {
        StringBuilder res = new StringBuilder();

        Stack<T> copyStack = (Stack<T>)this.stack.clone();

        while(!copyStack.isEmpty()) {
            T elem = copyStack.pop();
            res.append(elem.toString()).append("\n");
        }

        return res.toString();
    }
}
