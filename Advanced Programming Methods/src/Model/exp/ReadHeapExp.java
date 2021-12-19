package Model.exp;

import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.value.IValue;
import Model.value.RefValue;

public class ReadHeapExp implements IExp {
    IExp expression;

    public ReadHeapExp(IExp _exp) {
        this.expression = _exp;
    }

    @Override
    public IValue eval(IDict<String, IValue> table, IHeap<IValue> heap) throws MyException {
        IValue val = this.expression.eval(table, heap);
        if(!(val instanceof RefValue refVal)) {
            throw new MyException("Expression does not evaluate to a RefValue.");
        }

        int address = refVal.getAddress();
        return heap.getValue(address);
    }

    @Override
    public String toString() {
        return "rH(" + this.expression.toString() + ")";
    }
}
