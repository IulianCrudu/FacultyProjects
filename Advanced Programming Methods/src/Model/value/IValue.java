package Model.value;

import Model.types.IType;

import java.io.Serializable;

public interface IValue extends Serializable  {
    IType getType();
    IValue deepCopy();
}
