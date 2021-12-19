package Model.stmt;

import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.exp.IExp;
import Model.types.StringType;
import Model.value.IValue;
import Model.value.StringValue;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.FileNotFoundException;

public class OpenRFileStmt implements IStmt {
    IExp expression;

    public OpenRFileStmt(IExp exp) {
        this.expression = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<StringValue, BufferedReader> fileTable = state.getFileTable();
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();
        IValue val = this.expression.eval(table, heap);

        if(!val.getType().equals(new StringType())) {
            throw new MyException("Expression evaluation is not a string.");
        }

        StringValue strVal = (StringValue) val;

        if(fileTable.isDefined(strVal)) {
            throw new MyException(strVal.toString() + " file already exists.");
        }

        try {
            BufferedReader br = new BufferedReader(new FileReader(strVal.getValue()));
            fileTable.add(strVal, br);
        } catch (FileNotFoundException exc) {
            throw new MyException(exc.getMessage());
        }

        return null;
    }

    @Override
    public String toString() {
        return "OpenFile(" + this.expression.toString() + ")";
    }
}
