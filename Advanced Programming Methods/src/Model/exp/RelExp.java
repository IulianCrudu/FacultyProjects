package Model.exp;

import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.types.IntType;
import Model.value.BoolValue;
import Model.value.IValue;
import Model.value.IntValue;

public class RelExp implements IExp {
    IExp e1, e2;
    String op;

    public RelExp(IExp e1, IExp e2, String op) {
        this.e1 = e1;
        this.e2 = e2;
        this.op = op;
    }

    @Override
    public IValue eval(IDict<String, IValue> table, IHeap<IValue> heap) throws MyException {
        IValue v1, v2;
        v1 = e1.eval(table, heap);
        if(!v1.getType().equals(new IntType())) {
            throw new MyException("First operand is not integer.");
        }
        v2 = e2.eval(table, heap);
        if(!v2.getType().equals(new IntType())) {
            throw new MyException("Second operand is not integer.");
        }

        IntValue i1 = (IntValue) v1;
        IntValue i2 = (IntValue) v2;

        int n1, n2;
        boolean result = false;
        n1 = i1.getValue();
        n2 = i2.getValue();

        if(this.op.equals("<")) {
            result = n1 < n2;
        }

        if(this.op.equals("<=")) {
            result = n1 <= n2;
        }

        if(this.op.equals("==")) {
            result = n1 == n2;
        }

        if(this.op.equals("!=")) {
            result = n1 != n2;
        }

        if(this.op.equals(">")) {
            result = n1 > n2;
        }

        if(this.op.equals(">=")) {
            result = n1 >= n2;
        }

        return new BoolValue(result);
    }
    @Override
    public String toString() {
        return this.e1.toString() + " " + this.op + this.e2.toString();
    }
}
