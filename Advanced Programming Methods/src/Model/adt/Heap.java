package Model.adt;

import Exceptions.MyException;

import java.util.HashMap;
import java.util.Map;

public class Heap<T1> implements IHeap<T1> {
    int nextAddress = 1;
    Map<Integer, T1> heap;

    public Heap() {
        this.heap = new HashMap<>();
    }

    public void setContent(Map<Integer, T1> newHeap) {
        this.heap = newHeap;
    }

    public Map<Integer, T1> getContent() { return this.heap; }

    public int add(T1 value) {
        this.heap.put(this.nextAddress, value);
        this.nextAddress++;

        return this.nextAddress - 1;
    }

    public void update(int key, T1 value) throws MyException {
        if(!this.isDefined(key)) {
            throw new MyException("Heap has no element defined on key " + key);
        }

        this.heap.put(key, value);
    }

    public boolean isDefined(int key) {
        return this.heap.containsKey(key);
    }

    public T1 getValue(int key) throws MyException {
        if(!this.isDefined(key)) {
            throw new MyException("Heap has no element defined on key " + key);
        }

        return this.heap.get(key);
    }

    public int getNextAddress() {
        return this.nextAddress;
    }

    @Override
    public String toString() {
        return this.heap.toString();
    }

    @Override
    public String getHeapLog() {
        StringBuilder res = new StringBuilder();

        for(int i = 1; i < this.nextAddress; i++) {
            if(this.isDefined(i)) {
                try {
                    res.append(i).append("->").append(this.getValue(i).toString()).append("\n");
                } catch(MyException exp) {
                    System.out.println("Should never happen");
                }
            }
        }

        return res.toString();
    }

}
