package Model.types;

import Model.value.IValue;
import Model.value.RefValue;

public class RefType implements IType {
    IType inner;

    public RefType(IType _inner) {
        this.inner = _inner;
    }

    public IType getInner() {
        return this.inner;
    }

    @Override
    public boolean equals(Object another) {
        if(!(another instanceof RefType))
            return false;

        return this.inner.equals(((RefType) another).getInner());
    }

    @Override
    public String toString() {
        return "Ref(" + this.inner.toString() + ")";
    }

    @Override
    public IValue defaultValue() {
        return new RefValue(0, inner);
    }

    @Override
    public IType deepCopy() {
        return new RefType(this.inner);
    }
}
