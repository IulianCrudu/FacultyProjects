package Model.adt;

import Exceptions.MyException;
import Model.value.IValue;

import java.util.Map;

public interface IHeap<T1> {
    void setContent(Map<Integer, T1> newHeap);
    Map<Integer, T1> getContent();
    int add(T1 value);
    void update(int key, T1 value) throws MyException;
    boolean isDefined(int key);
    T1 getValue(int key) throws MyException;
    int getNextAddress();
    String toString();
    String getHeapLog();
}
