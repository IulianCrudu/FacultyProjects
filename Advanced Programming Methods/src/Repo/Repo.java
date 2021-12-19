package Repo;
import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IStack;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.adt.IList;
import Model.stmt.IStmt;
import Model.value.IValue;
import Model.value.StringValue;

import java.io.*;
import java.util.ArrayList;
import java.util.Scanner;
import java.util.List;

public class Repo implements IRepo {

    List<PrgState> myPrgStates;
    final String logFilePath;

    public Repo() {
        this.myPrgStates = new ArrayList<>();

        Scanner input=new Scanner(System.in);
        System.out.println("Enter the log file name: ");
        this.logFilePath = input.nextLine();
    }

    public Repo(String filePath) {
        this.myPrgStates = new ArrayList<>();
        this.logFilePath = filePath;
    }

    @Override
    public List<PrgState> getPrgList() {
        return this.myPrgStates;
    }

    @Override
    public void setPrgList(List<PrgState> l) {
        this.myPrgStates = l;
    }

    @Override
    public void addPrg(PrgState newPrg) {
        this.myPrgStates.add(newPrg);
    }

    @Override
    public void logPrgStateExec(PrgState prgState) throws MyException {
        PrintWriter logFile = null;

        try {
            logFile= new PrintWriter(new BufferedWriter(new FileWriter(this.logFilePath, true)));
            IStack<IStmt> exeStack = prgState.getExeStack();
            IDict<String, IValue> symTable = prgState.getSymTable();
            IDict<StringValue, BufferedReader> fileTable = prgState.getFileTable();
            IHeap<IValue> heap = prgState.getHeap();
            IList<IValue> out = prgState.getOutput();

            logFile.println(prgState.getStateId());
            logFile.println("ExeStack_" + prgState.getStateId() + ":");
            logFile.print(exeStack.getStackLog());
            logFile.println("SymTable:");
            logFile.print(symTable.getDictLog());

            logFile.println("Heap:");
            logFile.print(heap.getHeapLog());

            logFile.println("Out:");
            logFile.print(out.getListLog());

            logFile.println("FileTable:");
            logFile.print(fileTable.getDictLog());
            logFile.println("");
        } catch(IOException e) {
            throw new MyException(e.getMessage());
        } finally {
            if(logFile != null)
                logFile.close();
        }
    }
}
