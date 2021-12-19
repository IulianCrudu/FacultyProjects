package Model.adt;

import Exceptions.MyException;

public interface IStack<T> {

    T pop() throws MyException;
    void push(T v);
    boolean isEmpty();
    String toString();
    String getStackLog();
}

