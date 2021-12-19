package Repo;
import Exceptions.MyException;
import Model.PrgState;

import java.util.List;

public interface IRepo {
    void addPrg(PrgState newPrg);
    void logPrgStateExec(PrgState prgState) throws MyException;
    List<PrgState> getPrgList();
    void setPrgList(List<PrgState> l);
}
