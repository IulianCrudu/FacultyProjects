package Model.types;

import Model.value.IValue;
import Model.value.StringValue;

public class StringType implements IType {
    @Override
    public IValue defaultValue() {
        return new StringValue("");
    }

    @Override
    public boolean equals(Object o) {
        return o != null && o.getClass() == this.getClass();
    }

    @Override
    public IType deepCopy() {
        return new StringType();
    }

    @Override
    public String toString(){
        return "string";
    }
}
