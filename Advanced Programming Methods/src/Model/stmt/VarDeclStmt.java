package Model.stmt;


import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IDict;
import Model.types.IType;
import Model.value.IValue;

public class VarDeclStmt implements IStmt{
    String name;
    IType type;

    public VarDeclStmt(String name, IType type){
        this.name = name;
        this.type = type;
    }


    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<String, IValue> table = state.getSymTable();

        if(table.isDefined(this.name)) {
            throw new MyException("Variable is already declared.");
        }

        table.add(this.name, this.type.defaultValue());

        return null;
    }

    @Override
    public String toString() {
        return type.toString() + " " + this.name;
    }
}
