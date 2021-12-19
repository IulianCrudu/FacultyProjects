package Model.stmt;

import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.exp.IExp;
import Model.types.IntType;
import Model.types.StringType;
import Model.value.IValue;
import Model.value.IntValue;
import Model.value.StringValue;

import java.io.BufferedReader;
import java.io.IOException;

public class ReadFileStmt implements IStmt {
    IExp expression;
    String var_name;

    public ReadFileStmt(IExp exp, String var_name) {
        this.expression = exp;
        this.var_name = var_name;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<StringValue, BufferedReader> fileTable = state.getFileTable();
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();

        if(!table.isDefined(this.var_name)) {
            throw new MyException(this.var_name + " not defined.");
        }

        IValue tableValue = table.lookup(this.var_name);
        if(!tableValue.getType().equals(new IntType())) {
            throw new MyException(this.var_name + " is not referencing an integer.");
        }

        IValue exprValue = this.expression.eval(table, heap);
        if(!exprValue.getType().equals(new StringType())) {
            throw new MyException(exprValue.toString() + " does not evaluate to a string.");
        }

        StringValue fileName = (StringValue) exprValue;
        if(!fileTable.isDefined(fileName)) {
            throw new MyException(fileName.getValue() + " does not exist in the FileTable.");
        }
        BufferedReader br = fileTable.lookup(fileName);
        try {
            String line = br.readLine();
            IntValue intValue;

            if(line.isEmpty()) {
                intValue = new IntValue();
            } else {
                intValue = new IntValue(Integer.parseInt(line));
            }

            table.update(this.var_name, intValue);
        } catch (IOException exc) {
            throw new MyException(exc.getMessage());
        }

        return null;
    }

    @Override
    public String toString() {
        return "ReadFile(" + this.expression.toString() + "," + this.var_name + ")";
    }
}
