package Model.stmt;

import Model.PrgState;

public class NopStmt implements IStmt {
    public PrgState execute(PrgState state){
        return null;
    }

    @Override
    public String toString(){
        return "No operation";
    }
}
