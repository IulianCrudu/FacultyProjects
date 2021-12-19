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

public class HeapAllocationStmt implements IStmt {
    String varName;
    IExp expression;

    public HeapAllocationStmt(String varName, IExp exp) {
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

        RefValue refValue = (RefValue) val;
        RefType refType = (RefType) refValue.getType();

        IValue expValue = this.expression.eval(table, heap);
        if(!refType.getInner().equals(expValue.getType())) {
            throw new MyException("The var table inner value and expression value are not the same");
        }

        int address = heap.add(expValue);
//        refValue.updateAddress(address);

        table.update(this.varName, new RefValue(address, expValue.getType()));

        return null;
    }

    @Override
    public String toString() {
        return "new(" + this.varName + "," + this.expression.toString() + ")";
    }
}
