package Model.adt;

import Exceptions.MyException;

import java.util.List;

public interface IList<T> {
    void add(T v);
    T pop() throws MyException;
    T get() throws MyException;
    String toString();
    String getListLog();
    boolean isEmpty();
    void clear();
}
