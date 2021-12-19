package Model.exp;

import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.value.IValue;

public class ValueExp implements IExp{
    IValue val;

    public ValueExp(IValue _val) {
        this.val = _val;
    }

    @Override
    public IValue eval(IDict<String, IValue> table, IHeap<IValue> heap) throws MyException {
        return this.val;
    }

    @Override
    public String toString() {
        return this.val.toString();
    }
}
