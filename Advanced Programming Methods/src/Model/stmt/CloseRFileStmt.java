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
import java.io.IOException;

public class CloseRFileStmt implements IStmt {
    IExp expression;

    public CloseRFileStmt(IExp exp) {
        this.expression = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<StringValue, BufferedReader> fileTable = state.getFileTable();
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();

        IValue exprValue = this.expression.eval(table, heap);
        if(!exprValue.getType().equals(new StringType())) {
            throw new MyException(exprValue.toString() + " does not evaluate to a string.");
        }

        StringValue strValue = (StringValue) exprValue;
        if(!fileTable.isDefined(strValue)) {
            throw new MyException(strValue.getValue() + " does not exist in the FileTable.");
        }
        BufferedReader br = fileTable.lookup(strValue);

        try {
            br.close();
            fileTable.remove(strValue);
        } catch (IOException exc) {
            throw new MyException(exc.getMessage());
        }

        return null;
    }

    @Override
    public String toString() {
        return "CloseFile(" + this.expression.toString() + ")";
    }
}
