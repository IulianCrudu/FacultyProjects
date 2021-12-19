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

public class WhileStmt implements IStmt {
    final IExp expression;
    final IStmt statement;

    public WhileStmt(IExp _expression, IStmt _statement) {
        this.expression = _expression;
        this.statement = _statement;
    }

    @Override
    public PrgState execute(PrgState prgState) throws MyException {
        IStack<IStmt> stk = prgState.getExeStack();
        IDict<String, IValue> table = prgState.getSymTable();
        IHeap<IValue> heap = prgState.getHeap();

        IValue val = this.expression.eval(table, heap);
        if(!(val instanceof BoolValue)) {
            throw new MyException("Invalid expression type.");
        }

        if(((BoolValue) val).getValue()) {
            stk.push(this);
            stk.push(this.statement);
        }

        return null;
    }

    @Override
    public String toString() {
        return "while(" + this.expression.toString() + "{ " + this.statement.toString() + " };";
    }
}
