package Model.exp;

import Exceptions.MyException;
import Model.adt.IDict;
import Model.adt.IHeap;
import Model.value.IValue;

public interface IExp {
    IValue eval(IDict<String, IValue> table, IHeap<IValue> heap) throws MyException;
}
