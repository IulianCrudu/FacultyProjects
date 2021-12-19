package Model.adt;

import Exceptions.MyException;
import java.util.Map;

public interface IDict<T1,T2>{
    void add(T1 v1, T2 v2);
    void update(T1 v1, T2 v2);
    Map<T1, T2> getContent();
    T2 lookup(T1 id) throws MyException;
    boolean isDefined(T1 id);
    T2 remove(T1 id)  throws MyException;
    String toString();
    String getDictLog();
    IDict<T1, T2> deepCopy();
}
