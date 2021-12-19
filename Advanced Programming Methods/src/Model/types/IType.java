package Model.types;

import Model.value.IValue;

import java.io.Serializable;

public interface IType extends Serializable {
    IValue defaultValue();
    IType deepCopy();
}
