package Model.stmt;

import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.adt.IStack;
import Model.exp.IExp;
import Model.types.BoolType;
import Model.value.BoolValue;
import Model.value.IValue;

public class IfStmt implements IStmt {
    IExp exp;
    IStmt thenS;
    IStmt elseS;

    public IfStmt(IExp exp, IStmt thenS, IStmt elseS) {
        this.exp = exp;
        this.thenS = thenS;
        this.elseS = elseS;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IStack<IStmt> stk = state.getExeStack();
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();

        IValue v = this.exp.eval(table, heap);

        if(!v.getType().equals(new BoolType())) {
            throw new MyException("Expression does not return a boolean.");
        }

        BoolValue b = (BoolValue) v;
        boolean res = b.getValue();

        if(res) {
            stk.push(this.thenS);
        } else {
            stk.push(this.elseS);
        }

        return null;
    }

    @Override
    public String toString() {
        return "(IF(" + exp.toString()+ ") THEN(" + thenS.toString() + ")ELSE(" + elseS.toString() + "))";
    }
}
