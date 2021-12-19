package Controller;
import Exceptions.MyException;
import Model.PrgState;
import Model.value.IValue;
import Model.value.RefValue;
import Repo.IRepo;

import java.util.*;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;
import java.util.stream.Stream;


public class Controller {

    IRepo repo;
    ExecutorService executor;

    public Controller(IRepo repo) {
        this.repo = repo;
    }

    public void addProgram(PrgState newPrg) {
        this.repo.addPrg(newPrg);
    }

    private List<PrgState> removeCompletedPrg(List<PrgState> inPrgList) {
        return inPrgList.stream().filter(PrgState::isNotCompleted).collect(Collectors.toList());
    }

    private void oneStepForAllPrg(List<PrgState> prgList) throws MyException {
        prgList.forEach(prg -> {
            try {
                this.repo.logPrgStateExec(prg);
            } catch (MyException e) {
                e.printStackTrace();
            }
        });

        List<Callable<PrgState>> callList = prgList
                .stream()
                .map(
                    (PrgState p) -> (Callable<PrgState>)(p::oneStep)
                )
                .collect(Collectors.toList());

        try {

        List<PrgState> newPrgList = this.executor
                .invokeAll(callList)
                .stream()
                .map(future -> {
                    try {
                        return future.get();
                    } catch (ExecutionException | InterruptedException e) {
                        e.printStackTrace();
                    }

                    return null;
                })
                .filter(Objects::nonNull)
                .collect(Collectors.toList());

        prgList.addAll(newPrgList);

        prgList.forEach(prg -> {
            try {
                this.repo.logPrgStateExec(prg);
            } catch (MyException e) {
                e.printStackTrace();
            }
        });

        repo.setPrgList(prgList);
        } catch (InterruptedException e) {
            throw new MyException(e.getMessage());
        }
    }

    public void allStep() throws MyException {
        this.executor = Executors.newFixedThreadPool(2);
        List<PrgState> prgList = this.removeCompletedPrg(repo.getPrgList());

        while(prgList.size() > 0) {
            Stream<Integer> addresses = this.getAddrFromHeap(prgList.get(0).getHeap().getContent().values());

            for(PrgState prg : prgList) {
                addresses = Stream.concat(addresses, this.getAddrFromSymTable(prg.getSymTable().getContent().values()));
            }

            prgList.get(0).getHeap().setContent(this.safeGarbageCollector(
                    addresses.collect(Collectors.toList()),
                    prgList.get(0).getHeap().getContent()
            ));
            this.oneStepForAllPrg(prgList);
            prgList = this.removeCompletedPrg(repo.getPrgList());
        }
        this.executor.shutdown();
        repo.setPrgList(prgList);
    }

    Map<Integer, IValue> safeGarbageCollector(List<Integer> addresses, Map<Integer, IValue> heap) {
        return heap.entrySet().stream()
                .filter(e -> addresses.contains(e.getKey())).collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue));
    }

    Stream<Integer> getAddrFromSymTable(Collection<IValue> symTableValues) {
        return symTableValues.stream().filter(v -> v instanceof RefValue).map(v -> {
            RefValue v1 = (RefValue) v;
            return v1.getAddress();
        });
    }

    Stream<Integer> getAddrFromHeap(Collection<IValue> heapValues) {
        return heapValues.stream().filter(v -> v instanceof RefValue).map(v -> {
            RefValue v1 = (RefValue) v;
            return v1.getAddress();
        });
    }
}
