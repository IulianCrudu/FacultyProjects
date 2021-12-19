package Model.stmt;


import Exceptions.MyException;
import Model.PrgState;
import Model.adt.IHeap;
import Model.adt.IList;
import Model.adt.List;
import Model.exp.IExp;
import Model.value.IValue;

public class PrintStmt implements IStmt {

    IExp expression;

    public PrintStmt(IExp exp) {
        this.expression = exp;
    }

    @Override
    public PrgState execute(PrgState state) throws MyException {
        IList<IValue> output = state.getOutput();
        IHeap<IValue> heap = state.getHeap();
        output.add(expression.eval(state.getSymTable(), heap));
        state.setOutput(output);
        return null;
    }

    @Override
    public String toString() {
        return "print(" + this.expression.toString() + ")";
    }
}
