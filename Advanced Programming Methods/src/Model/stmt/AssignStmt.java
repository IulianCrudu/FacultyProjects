package Model.stmt;

import Exceptions.MyException;
import Exceptions.UndefinedTableVariableException;
import Model.PrgState;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.exp.IExp;
import Model.types.IType;
import Model.value.IValue;

public class AssignStmt implements IStmt {

    String id;
    IExp expression;

    public AssignStmt(String id, IExp exp){
        this.id = id;
        this.expression = exp;
    }

    @Override
    public String toString(){
        return this.id + "=" + this.expression.toString();
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IDict<String, IValue> table = state.getSymTable();
        IHeap<IValue> heap = state.getHeap();
        if(!table.isDefined(this.id)) {
            throw new UndefinedTableVariableException("The used variable " + this.id + " was not declared before.");
        }
        IValue val = this.expression.eval(table, heap);
        IType typeId = (table.lookup(this.id)).getType();
        if(!val.getType().equals(typeId)) {
            throw new MyException(
                "Declared type of variable " + id +" and type of  the assigned expression do not match"
            );
        }

        table.update(this.id, val);
        return null;
    }
}
