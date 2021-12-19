package Model.stmt;

import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IStack;

public class CompStmt implements IStmt {
    IStmt first, second;

    public CompStmt(IStmt f, IStmt s) {
        this.first = f;
        this.second = s;
    }

    @Override
    public String toString() {
        return "(" + this.first.toString() + ";" + this.second.toString() + ")";
    }

    public PrgState execute(PrgState state) throws MyException {
        IStack<IStmt> stk = state.getExeStack();
        stk.push(this.second);
        stk.push(this.first);

        return null;
    }
}
