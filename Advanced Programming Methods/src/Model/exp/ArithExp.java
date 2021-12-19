package Model.exp;
import Exceptions.DivisionByZeroException;
import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.types.IntType;
import Model.value.IValue;
import Model.value.IntValue;

public class ArithExp implements IExp {
    char op;
    IExp e1, e2;

    public ArithExp(char _op, IExp e1, IExp e2) {
        this.op = _op;
        this.e1 = e1;
        this.e2 = e2;
    }

    @Override
    public IValue eval(IDict<String, IValue> symTable, IHeap<IValue> heap) throws MyException {
        IValue v1, v2;
        v1 = e1.eval(symTable, heap);
        if(!v1.getType().equals(new IntType())) {
            throw new MyException("First operand is not integer.");
        }
        v2 = e2.eval(symTable, heap);
        if(!v2.getType().equals(new IntType())) {
            throw new MyException("Second operand is not integer.");
        }

        IntValue i1 = (IntValue) v1;
        IntValue i2 = (IntValue) v2;

        int n1, n2, returnValue = 0;
        n1 = i1.getValue();
        n2 = i2.getValue();
        if(op == '+') returnValue = n1 + n2;
        if(op == '-') returnValue = n1 - n2;
        if(op == '*') returnValue = n1 * n2;
        if(op == '/') {
            if(n2 == 0) {
                throw new DivisionByZeroException("Division by 0 not allowed.");
            }
            returnValue = n1 / n2;
        }

        return new IntValue(returnValue);
    }

    public char getOp() {return this.op;}

    public IExp getFirst() {
        return this.e1;
    }

    public IExp getSecond() {
        return this.e2;
    }

    public String toString() { return e1.toString() + " " + op + " " + e2.toString(); }
}
