package Model.value;

import Model.types.IType;
import Model.types.RefType;

public class RefValue implements IValue {
    int address;
    IType locationType;

    public RefValue(int address, IType locationType) {
        this.address = address;
        this.locationType = locationType;
    }

    public int getAddress() { return this.address; }

    public void updateAddress(int newAddress) { this.address = newAddress; }

    @Override
    public String toString() {
        return this.address + "->" + this.locationType.toString();
    }

    @Override
    public IType getType() {
        return new RefType(this.locationType);
    }

    @Override
    public IValue deepCopy() {
        return new RefValue(this.address, this.locationType);
    }
}
