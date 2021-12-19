package Model.stmt;

import Exceptions.MyException;
import Exceptions.UndefinedTableVariableException;
import Model.PrgState;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.exp.IExp;
import Model.types.RefType;
import Model.value.IValue;
import Model.value.RefValue;

public class HeapWriteStmt implements IStmt {
    String varName;
    IExp expression;

    public HeapWriteStmt(String varName, IExp exp) {
        this.varName = varName;
        this.expression = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();

        if(!table.isDefined(this.varName)) {
            throw new UndefinedTableVariableException("The used variable " + this.varName + " was not declared before.");
        }

        IValue val = table.lookup(this.varName);
        if(!(val.getType() instanceof RefType)) {
            throw new MyException("The value is not of RefType type.");
        }

        RefValue refVal = (RefValue) val;
        RefType refType = (RefType) refVal.getType();

        if(!heap.isDefined(refVal.getAddress())) {
            throw new MyException("RefValue does not point to a valid Heap address.");
        }

        IValue expVal = this.expression.eval(table, heap);
        if(!refType.getInner().equals(expVal.getType())) {
            throw new MyException("The var table inner value and expression value are not the same");
        }

        heap.update(refVal.getAddress(), expVal);

        return null;
    }

    @Override
    public String toString() {
        return this.varName + ":=" + this.expression.toString();
    }
}
