package Model;
import Exceptions.MyException;
import Model.adt.*;
import Model.stmt.IStmt;
import Model.value.IValue;
import Model.value.StringValue;

import java.io.BufferedReader;
import java.util.concurrent.atomic.AtomicInteger;

public class PrgState {

    static AtomicInteger lastId = new AtomicInteger(0);
    IStack<IStmt> exeStack;
    IDict<String, IValue> symTable;
    IList<IValue> out;
    IDict<StringValue, BufferedReader> fileTable;
    IHeap<IValue> heap;
    IStmt originalProgram; //optional field, but good to have
    int stateId;

    private synchronized static int getFreeId() {
        return lastId.getAndIncrement();
    }

    public PrgState(
        IStack<IStmt> stk,
        IDict<String, IValue> symtbl,
        IDict<StringValue, BufferedReader> fileTable,
        IHeap<IValue> heap,
        IList<IValue> ot,
        IStmt prg
    ) {
        this.stateId = getFreeId();
        this.exeStack = stk;
        this.symTable = symtbl;
        this.out = ot;
        this.fileTable = fileTable;
        this.heap = heap;
//        this.originalProgram = deepCopy(prg);
        stk.push(prg);
    }

    public Boolean isNotCompleted() {
        return !this.exeStack.isEmpty();
    }

    public PrgState oneStep() throws MyException {
        if(this.exeStack.isEmpty()) {
            throw new MyException("PrgState stack is empty.");
        }
        IStmt currentStatement = this.exeStack.pop();
        return currentStatement.execute(this);
    }

    public int getStateId() {
        return this.stateId;
    }

    public IList<IValue> getOutput() {
        return this.out;
    }

    public IDict<String, IValue> getSymTable() {
        return this.symTable;
    }

    public IStack<IStmt> getExeStack() {
        return this.exeStack;
    }

    public IDict<StringValue, BufferedReader> getFileTable() { return this.fileTable; }

    public IHeap<IValue> getHeap() { return this.heap; }

    public void setOutput(IList<IValue> _out) {
        this.out = _out;
    }

    public void setSymTable(IDict<String, IValue> _symTable) {
        this.symTable = _symTable;
    }

    public void setExeStack(IStack<IStmt> _exeStack) {
        this.exeStack = _exeStack;
    }

    public void setFileTable(IDict<StringValue, BufferedReader> fileTable) { this.fileTable = fileTable; }

    @Override
    public String toString() {
        String str = "";
        str += "Id: " + this.stateId + "\n";
        str += "Execution Stack: " + this.exeStack.toString() + "\n";
        str += "Symbol Table: " + this.symTable.toString() + "\n";
        str += "File Table: " + this.fileTable.toString() + "\n";
        str += "Heap: " + this.heap.toString() + "\n";
        str += "Output: " + this.out.toString() + "\n";
        return  str;
    }
}