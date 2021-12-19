package Model.adt;

import Exceptions.DataTypeException;
import Exceptions.MyException;

import java.util.Vector;

public class List<T> implements IList<T> {
    Vector<T> list;

    public List() {
        this.list = new Vector<>();
    }

    @Override
    public void add(T v) {
        this.list.add(v);
    }

    @Override
    public T get() throws MyException {
        if(this.isEmpty()) {
            throw new DataTypeException("Nothing to pop. List is empty");
        }
        return this.list.lastElement();
    }

    @Override
    public T pop() throws MyException {
        T lastElement = this.get();
        this.list.removeElementAt(this.size() - 1);

        return lastElement;
    }

    public int size() {
        return this.list.size();
    }

    @Override
    public boolean isEmpty() {
        return this.list.isEmpty();
    }

    @Override
    public void clear(){
        this.list.clear();
    }

    @Override
    public String toString() {
        return this.list.toString();
    }

    @Override
    public String getListLog() {
        StringBuilder res = new StringBuilder();

        for(T elem : this.list) {
            res.append(elem.toString()).append("\n");
        }

        return res.toString();
    }

}
