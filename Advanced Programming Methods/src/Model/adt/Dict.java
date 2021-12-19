package Model.adt;
import Exceptions.DataTypeException;
import Exceptions.MyException;

import java.io.*;
import java.util.HashMap;
import java.util.Map;

public class Dict<T1,T2> implements IDict<T1,T2>, Serializable {
    Map<T1, T2> dictionary;

    public Dict() {
        this.dictionary = new HashMap<T1,T2>();
    }

    public Map<T1, T2> getContent() { return this.dictionary; }

    @Override
    public void add(T1 key, T2 value) {
        this.dictionary.put(key, value);
    }

    @Override
    public void update(T1 key, T2 value) {
        this.dictionary.put(key, value);
    }

    @Override
    public T2 lookup(T1 id) throws MyException {
        if(!this.isDefined(id)) {
            throw new DataTypeException(id + " not present in the dictionary.");
        }
        return this.dictionary.get(id);
    }

    @Override
    public boolean isDefined(T1 id) {
        return this.dictionary.containsKey(id);
    }

    @Override
    public T2 remove(T1 id) throws MyException {
        if(!this.isDefined(id)) {
            throw new DataTypeException(id + " not present in the dictionary.");
        }

        T2 val = this.dictionary.get(id);
        this.dictionary.remove(id);
        return val;
    }

    @Override
    public IDict<T1, T2> deepCopy() {
        try {
            ByteArrayOutputStream outputStream = new ByteArrayOutputStream();
            ObjectOutputStream outputStrm = new ObjectOutputStream(outputStream);
            outputStrm.writeObject(this);
            ByteArrayInputStream inputStream = new ByteArrayInputStream(outputStream.toByteArray());
            ObjectInputStream objInputStream = new ObjectInputStream(inputStream);
            return (IDict<T1, T2>) objInputStream.readObject();
        }
        catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    @Override
    public String toString() {
        return this.dictionary.toString();
    }

    @Override
    public String getDictLog() {
        StringBuilder res = new StringBuilder();

        for(Map.Entry<T1, T2> entry : this.dictionary.entrySet()) {
            res
                .append(entry.getKey().toString())
                .append(":")
                .append(entry.getValue().toString())
                .append("\n");
        }

        return res.toString();
    }
}
