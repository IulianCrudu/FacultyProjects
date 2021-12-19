package Model.stmt;

import Exceptions.MyException;
import Model.PrgState;
import Model.adt.*;
import Model.value.IValue;
import Model.value.StringValue;

import java.io.BufferedReader;

public class ForkStmt implements IStmt{
    IStmt statement;

    public ForkStmt(IStmt s) {
        this.statement = s;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IHeap<IValue> heap = state.getHeap();
        IDict<StringValue, BufferedReader> fileTable = state.getFileTable();
        IList<IValue> out = state.getOutput();

        IDict<String, IValue> symTable = state.getSymTable().deepCopy();

        IStack<IStmt> stack = new MyStack<>();

        return new PrgState(stack, symTable, fileTable, heap, out, this.statement);
    }

    @Override
    public String toString() {
        return "Fork(" + this.statement.toString() + ")";
    }
}
