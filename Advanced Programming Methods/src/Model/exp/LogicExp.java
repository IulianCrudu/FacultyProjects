package Model.exp;

import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.types.BoolType;
import Model.value.BoolValue;
import Model.value.IValue;

public class LogicExp implements IExp {
    IExp e1;
    IExp e2;
    int op; // 1 - and, 2 - or

    public LogicExp(int op, IExp e1, IExp e2) {
        this.op = op;
        this.e1 = e1;
        this.e2 = e2;
    }

    @Override
    public IValue eval(IDict<String, IValue> table, IHeap<IValue> heap) throws MyException {
        IValue v1, v2;
        v1 = this.e1.eval(table, heap);
        if(!v1.getType().equals(new BoolType())) {
            throw new MyException("Operand1 is not boolean.");
        }
        v2 = this.e2.eval(table, heap);
        if(!v2.getType().equals(new BoolType())) {
            throw new MyException("Operand2 is not boolean.");
        }

        BoolValue i1 = (BoolValue) v1;
        BoolValue i2 = (BoolValue) v2;

        Boolean b1, b2;
        b1 = i1.getValue();
        b2 = i2.getValue();

        if(op == 1) {
            return new BoolValue(b1 && b2);
        } else {
            return new BoolValue(b1 || b2);
        }
    }

    @Override
    public String toString() {
        String operation;
        if(this.op == 1) {
            operation = " and ";
        } else {
            operation = " or ";
        }
        return this.e1.toString() + operation + this.e2.toString();
    }
}
