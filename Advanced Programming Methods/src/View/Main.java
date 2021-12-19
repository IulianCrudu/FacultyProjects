package View;
import Exceptions.MyException;
import Model.adt.*;
import Model.exp.*;
import Model.stmt.*;
import Model.types.BoolType;
import Model.types.IntType;
import Model.types.RefType;
import Model.types.StringType;
import Model.value.BoolValue;
import Model.value.IValue;
import Model.value.IntValue;
import Model.value.StringValue;
import Repo.Repo;
import Repo.IRepo;
import Controller.Controller;
import Model.PrgState;

import java.io.BufferedReader;


public class Main {
    public static void main(String[] args) {
        // ex 1:  int v; v = 2; Print(v)
        IStmt ex1 = new CompStmt(
                new VarDeclStmt("v", new IntType()),
                new CompStmt(
                        new AssignStmt("v", new ValueExp(new IntValue(2))),
                        new PrintStmt(new VarExp("v"))
                )
        );

        // ex 2: a=2+3*5;b=a+1;Print(b)
        IStmt ex2 = new CompStmt(new VarDeclStmt("a", new IntType()), new CompStmt(new VarDeclStmt("b", new IntType()),
                new CompStmt(new AssignStmt("a", new ArithExp('+', new ValueExp(new IntValue(2)), new ArithExp('*',
                        new ValueExp(new IntValue(3)), new ValueExp(new IntValue(5))))), new CompStmt(
                        new AssignStmt("b", new ArithExp('+', new VarExp("a"), new ValueExp(new IntValue(1)))),
                        new PrintStmt(new VarExp("b"))))));
//
//            // ex 3: bool a; int v; a=true;(If a Then v=2 Else v=3);Print(v)
        IStmt ex3 = new CompStmt(new VarDeclStmt("a", new BoolType()), new CompStmt(new VarDeclStmt("v",
                new IntType()), new CompStmt(new AssignStmt("a", new ValueExp(new BoolValue(true))),
                new CompStmt(new IfStmt(new VarExp("a"), new AssignStmt("v", new ValueExp(new IntValue(2))),
                        new AssignStmt("v", new ValueExp(new IntValue(3)))), new PrintStmt(new
                        VarExp("v"))))));

        IStmt ex4 = new CompStmt(new VarDeclStmt("varf", new StringType()),
                new CompStmt(new AssignStmt("varf", new ValueExp(new StringValue("fisier.txt"))),
                        new CompStmt(new OpenRFileStmt(new VarExp("varf")),
                                new CompStmt(new VarDeclStmt("varc", new IntType()),
                                        new CompStmt(new ReadFileStmt(new VarExp("varf"), "varc"),
                                                new CompStmt(new PrintStmt(new VarExp("varc")),
                                                        new CompStmt(new ReadFileStmt(new VarExp("varf"), "varc"),
                                                                new CompStmt(new PrintStmt(new VarExp("varc")),
                                                                        new CloseRFileStmt(new VarExp("varf"))))))))));

        // Ref int v;new(v,20);Ref Ref int a; new(a,v);print(v);print(a)
        IStmt ex5 = new CompStmt(
            new VarDeclStmt("v", new RefType(new IntType())),
            new CompStmt(
                new HeapAllocationStmt("v", new ValueExp(new IntValue(20))),
                new CompStmt(
                    new VarDeclStmt("a", new RefType(new RefType(new IntType()))),
                    new CompStmt(
                        new HeapAllocationStmt("a", new VarExp("v")),
                        new CompStmt(
                            new PrintStmt(new VarExp("v")),
                            new PrintStmt(new VarExp("a"))
                        )
                    )
                )
            )
        );

        // Ref int v;new(v,20);Ref Ref int a; new(a,v);print(rH(v));print(rH(rH(a))+5)
        IStmt ex6 = new CompStmt(
            new VarDeclStmt("v", new RefType(new IntType())),
            new CompStmt(
                new HeapAllocationStmt("v", new ValueExp(new IntValue(20))),
                new CompStmt(
                    new VarDeclStmt("a", new RefType(new RefType(new IntType()))),
                    new CompStmt(
                        new HeapAllocationStmt("a", new VarExp("v")),
                        new CompStmt(
                            new PrintStmt(new ReadHeapExp(new VarExp("v"))),
                            new PrintStmt(
                                new ArithExp(
                                    '+',
                                    new ReadHeapExp(new ReadHeapExp(new VarExp("a"))),
                                    new ValueExp(new IntValue(5))
                                )
                            )
                        )
                    )
                )
            )
        );

        // Ref int v;new(v,20);print(rH(v)); wH(v,30);print(rH(v)+5);
        IStmt ex7 = new CompStmt(
            new VarDeclStmt("v", new RefType(new IntType())),
            new CompStmt(
                new HeapAllocationStmt("v", new ValueExp(new IntValue(20))),
                new CompStmt(
                    new PrintStmt(new ReadHeapExp(new VarExp("v"))),
                    new CompStmt(
                        new HeapWriteStmt("v", new ValueExp(new IntValue(30))),
                        new PrintStmt(
                            new ArithExp(
                            '+',
                                new ReadHeapExp(new VarExp("v")),
                                new ValueExp(new IntValue(5)))
                        )
                    )
                )
            )
        );

        // Ref int v;new(v,20);Ref Ref int a; new(a,v); new(v,30);print(rH(rH(a)))
        IStmt ex8 = new CompStmt(
            new VarDeclStmt("v", new RefType(new IntType())),
            new CompStmt(
                new HeapAllocationStmt("v", new ValueExp(new IntValue(20))),
                new CompStmt(
                    new VarDeclStmt("a", new RefType(new RefType(new IntType()))),
                    new CompStmt(
                        new HeapAllocationStmt("a", new VarExp("v")),
                        new CompStmt(
                            new HeapAllocationStmt("v", new ValueExp(new IntValue(30))),
                            new PrintStmt(new ReadHeapExp(new ReadHeapExp(new VarExp("a"))))
                        )
                    )
                )
            )
        );

        // int v; v=4; (while (v>0) print(v);v=v-1);print(v)
        IStmt ex9 = new CompStmt(new VarDeclStmt("v",new IntType()),new CompStmt(new AssignStmt("v",new ValueExp(new IntValue(4))),
                new CompStmt(new WhileStmt(new RelExp(new VarExp("v"),new ValueExp(new IntValue(0)),">"),
                        new CompStmt(new PrintStmt(new VarExp("v")), new AssignStmt("v",new ArithExp('-',
                                new VarExp("v"), new ValueExp(new IntValue(1)))))),
                        new PrintStmt(new VarExp("v")))));

        // int v; Ref int a; v=10;new(a,22); fork(wH(a,30);v=32;print(v);print(rH(a)));
        // print(v);print(rH(a))
        IStmt ex10 = new CompStmt(
            new VarDeclStmt("v",new IntType()),
            new CompStmt(
                new VarDeclStmt("a", new RefType(new IntType())),
                new CompStmt(
                    new AssignStmt("v",new ValueExp(new IntValue(10))),
                    new CompStmt(
                        new HeapAllocationStmt("a", new ValueExp(new IntValue(22))),
                        new CompStmt(
                            new ForkStmt(
                                new CompStmt(
                                    new HeapWriteStmt("a", new ValueExp(new IntValue(30))),
                                    new CompStmt(
                                        new AssignStmt("v",new ValueExp(new IntValue(32))),
                                        new CompStmt(
                                            new PrintStmt(new VarExp("v")),
                                            new PrintStmt(new ReadHeapExp(new VarExp("a")))
                                        )
                                    )
                                )
                            ),
                            new CompStmt(
                                new PrintStmt(new VarExp("v")),
                                new PrintStmt(new ReadHeapExp(new VarExp("a")))
                            )
                        )
                    )
                )
            )
        );

        IStack<IStmt> exeStack1 = new MyStack<IStmt>();
        IDict<String, IValue> symTable1 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable1 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out1 = new List<IValue>();
        IHeap<IValue> heap1 = new Heap<>();
        PrgState prg1 = new PrgState(exeStack1, symTable1, fileTable1, heap1, out1, ex1);
        IRepo repo1 = new Repo("log1.txt");
        Controller controller1 = new Controller(repo1);
        controller1.addProgram(prg1);

        IStack<IStmt> exeStack2 = new MyStack<IStmt>();
        IDict<String, IValue> symTable2 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable2 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out2 = new List<IValue>();
        IHeap<IValue> heap2 = new Heap<>();
        PrgState prg2 = new PrgState(exeStack2, symTable2, fileTable2, heap2, out2, ex2);
        IRepo repo2 = new Repo("log2.txt");
        Controller controller2 = new Controller(repo2);
        controller2.addProgram(prg2);


        IStack<IStmt> exeStack3 = new MyStack<IStmt>();
        IDict<String, IValue> symTable3 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable3 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out3 = new List<IValue>();
        IHeap<IValue> heap3 = new Heap<>();
        PrgState prg3 = new PrgState(exeStack3, symTable3, fileTable3, heap3, out3, ex3);
        IRepo repo3 = new Repo("log3.txt");
        Controller controller3 = new Controller(repo3);
        controller3.addProgram(prg3);

        IStack<IStmt> exeStack4 = new MyStack<IStmt>();
        IDict<String, IValue> symTable4 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable4 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out4 = new List<IValue>();
        IHeap<IValue> heap4 = new Heap<>();
        PrgState prg4 = new PrgState(exeStack4, symTable4, fileTable4, heap4, out4, ex4);
        IRepo repo4 = new Repo("log4.txt");
        Controller controller4 = new Controller(repo4);
        controller4.addProgram(prg4);

        IStack<IStmt> exeStack5 = new MyStack<IStmt>();
        IDict<String, IValue> symTable5 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable5 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out5 = new List<IValue>();
        IHeap<IValue> heap5 = new Heap<>();
        PrgState prg5 = new PrgState(exeStack5, symTable5, fileTable5, heap5, out5, ex5);
        IRepo repo5 = new Repo("log5.txt");
        Controller controller5 = new Controller(repo5);
        controller5.addProgram(prg5);

        IStack<IStmt> exeStack6 = new MyStack<IStmt>();
        IDict<String, IValue> symTable6 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable6 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out6 = new List<IValue>();
        IHeap<IValue> heap6 = new Heap<>();
        PrgState prg6 = new PrgState(exeStack6, symTable6, fileTable6, heap6, out6, ex6);
        IRepo repo6 = new Repo("log6.txt");
        Controller controller6 = new Controller(repo6);
        controller6.addProgram(prg6);

        IStack<IStmt> exeStack7 = new MyStack<IStmt>();
        IDict<String, IValue> symTable7 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable7 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out7 = new List<IValue>();
        IHeap<IValue> heap7 = new Heap<>();
        PrgState prg7 = new PrgState(exeStack7, symTable7, fileTable7, heap7, out7, ex7);
        IRepo repo7 = new Repo("log7.txt");
        Controller controller7 = new Controller(repo7);
        controller7.addProgram(prg7);

        IStack<IStmt> exeStack8 = new MyStack<IStmt>();
        IDict<String, IValue> symTable8 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable8 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out8 = new List<IValue>();
        IHeap<IValue> heap8 = new Heap<>();
        PrgState prg8 = new PrgState(exeStack8, symTable8, fileTable8, heap8, out8, ex8);
        IRepo repo8 = new Repo("log8.txt");
        Controller controller8 = new Controller(repo8);
        controller8.addProgram(prg8);

        IStack<IStmt> exeStack9 = new MyStack<IStmt>();
        IDict<String, IValue> symTable9 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable9 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out9 = new List<IValue>();
        IHeap<IValue> heap9 = new Heap<>();
        PrgState prg9 = new PrgState(exeStack9, symTable9, fileTable9, heap9, out9, ex9);
        IRepo repo9 = new Repo("log9.txt");
        Controller controller9 = new Controller(repo9);
        controller9.addProgram(prg9);

        IStack<IStmt> exeStack10 = new MyStack<IStmt>();
        IDict<String, IValue> symTable10 = new Dict<String, IValue>();
        IDict<StringValue, BufferedReader> fileTable10 = new Dict<StringValue, BufferedReader>();
        IList<IValue> out10 = new List<IValue>();
        IHeap<IValue> heap10 = new Heap<>();
        PrgState prg10 = new PrgState(exeStack10, symTable10, fileTable10, heap10, out10, ex10);
        IRepo repo10 = new Repo("log10.txt");
        Controller controller10 = new Controller(repo10);
        controller10.addProgram(prg10);

        TextMenu menu = new TextMenu();
        menu.addCommand(new ExitCommand("0", "exit"));
        menu.addCommand(new RunExample("1", ex1.toString(), controller1));
        menu.addCommand(new RunExample("2", ex2.toString(), controller2));
        menu.addCommand(new RunExample("3", ex3.toString(), controller3));
        menu.addCommand(new RunExample("4", ex4.toString(), controller4));
        menu.addCommand(new RunExample("5", ex5.toString(), controller5));
        menu.addCommand(new RunExample("6", ex6.toString(), controller6));
        menu.addCommand(new RunExample("7", ex7.toString(), controller7));
        menu.addCommand(new RunExample("8", ex8.toString(), controller8));
        menu.addCommand(new RunExample("9", ex9.toString(), controller9));
        menu.addCommand(new RunExample("10", ex10.toString(), controller10));
        menu.show();
    }
}
