package Model.exp;
import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.value.IValue;

public class VarExp implements IExp{
    String id;

    public VarExp(String id){
        this.id = id;
    }

    public IValue eval(IDict<String, IValue> symTable, IHeap<IValue> heap) throws MyException {
        return symTable.lookup(id);
    }

    public String toString() {
        return id;
    }
}
