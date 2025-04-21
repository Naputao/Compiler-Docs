# IR 使用样例

​本文档是语义分析中 IR 的一个使用样例，为了便于同学们理解 IR 程序及其执行，这里直接根据源程序手动构造了 IR 程序，省去了语义分析的过程。

​对于如下源程序：

```c++
int a;
int arr[2] = { 2, 4};
int func(int p){
	p = p - 1;
	return p;
}
int main(){
	int b;
	a = arr[1];
	b = func(a);
	if (b < a) b = b * 2;
	return b;
}
```

我们手动构造了 IR 示例程序​如下：

```c++
//IR测试样例
#include <iostream>
#include "ir/ir.h"
#include "tools/ir_executor.h"
int main() {
    ir::Program program;
    ir::Function globalFunc("global", ir::Type::null);
    ir::Instruction assignInst(ir::Operand("0",ir::Type::IntLiteral),
                                     ir::Operand(),
                                     ir::Operand("a",ir::Type::Int),ir::Operator::def);
    globalFunc.addInst(&assignInst);
    ir::Instruction allocInst(ir::Operand("2",ir::Type::IntLiteral),
                              ir::Operand(),
                              ir::Operand("arr",ir::Type::IntPtr),ir::Operator::alloc);
    globalFunc.addInst(&allocInst);
    ir::Instruction storeInst(ir::Operand("arr",ir::Type::IntPtr),
                              ir::Operand("0",ir::Type::IntLiteral),
                              ir::Operand("2",ir::Type::IntLiteral),ir::Operator::store);
    ir::Instruction storeInst1(ir::Operand("arr",ir::Type::IntPtr),
                              ir::Operand("1",ir::Type::IntLiteral),
                              ir::Operand("4",ir::Type::IntLiteral),ir::Operator::store);
    ir::Instruction globalreturn(ir::Operand(),
                                 ir::Operand(),
                                 ir::Operand(), ir::Operator::_return);
    globalFunc.addInst(&storeInst);
    globalFunc.addInst(&storeInst1);
    globalFunc.addInst(&globalreturn);
    program.globalVal.emplace_back(ir::Operand("a",ir::Type::Int));
    program.globalVal.emplace_back(ir::Operand("arr",ir::Type::IntPtr),2);
    program.addFunction(globalFunc);
    std::vector<ir::Operand> paraVec = {ir::Operand("p",ir::Type::Int)};
    ir::Function funcFunction("func",paraVec,ir::Type::Int);
    ir::Instruction subInst(ir::Operand("p",ir::Type::Int),
                                     ir::Operand("1",ir::Type::IntLiteral),
                                     ir::Operand("t1",ir::Type::Int),ir::Operator::subi);
    ir::Instruction movInst(ir::Operand("t1",ir::Type::Int),
                                     ir::Operand(),
                                     ir::Operand("p",ir::Type::Int),ir::Operator::mov);
    ir::Instruction returnInst(ir::Operand("p",ir::Type::Int),
                                     ir::Operand(),
                                     ir::Operand(),ir::Operator::_return);
    funcFunction.addInst(&subInst);
    funcFunction.addInst(&movInst);
    funcFunction.addInst(&returnInst);
    program.addFunction(funcFunction);
    ir::Function mainFunction("main",ir::Type::Int);
    ir::CallInst callGlobal(ir::Operand("global",ir::Type::null),
                               ir::Operand("t0",ir::Type::null));
    ir::Instruction defInst(ir::Operand("0",ir::Type::IntLiteral),
                                     ir::Operand(),
                                     ir::Operand("b",ir::Type::Int),ir::Operator::def);
    ir::Instruction loadInst(ir::Operand("arr",ir::Type::IntPtr),
                                    ir::Operand("1",ir::Type::IntLiteral),
                                     ir::Operand("t2",ir::Type::Int),ir::Operator::load);
    ir::Instruction movInst1(ir::Operand("t2",ir::Type::Int),
                             ir::Operand(),
                             ir::Operand("a",ir::Type::Int),ir::Operator::mov);
    std::vector<ir::Operand> paraVec1 = {ir::Operand("a",ir::Type::Int)};
    ir::CallInst callInst(ir::Operand("func",ir::Type::Int),
                                     paraVec1,
                                     ir::Operand("t2",ir::Type::Int));
    ir::Instruction movInst2(ir::Operand("t2",ir::Type::Int),
                                     ir::Operand(),
                                     ir::Operand("b",ir::Type::Int),ir::Operator::mov);
    ir::Instruction lssInst(ir::Operand("b",ir::Type::Int),
                                     ir::Operand("a",ir::Type::Int),
                                     ir::Operand("t3",ir::Type::Int),ir::Operator::lss);
    ir::Instruction gotoInst(ir::Operand("t3",ir::Type::Int),
                                     ir::Operand(),
                                     ir::Operand("2",ir::Type::IntLiteral),ir::Operator::_goto);
    ir::Instruction gotoInst1(ir::Operand(),
                                     ir::Operand(),
                                     ir::Operand("4",ir::Type::IntLiteral),ir::Operator::_goto);
    ir::Instruction defInst2(ir::Operand("2",ir::Type::IntLiteral),
                                     ir::Operand(),
                                     ir::Operand("t4",ir::Type::Int),ir::Operator::def);
    ir::Instruction mulInst(ir::Operand("b",ir::Type::Int),
                                     ir::Operand("t4",ir::Type::Int),
                                     ir::Operand("t5",ir::Type::Int),ir::Operator::mul);
    ir::Instruction movInst3(ir::Operand("t5",ir::Type::Int),
                                    ir::Operand(),
                                     ir::Operand("b",ir::Type::Int),ir::Operator::mov);
    ir::Instruction returnInst1(ir::Operand("b",ir::Type::Int),
                                     ir::Operand(),
                                     ir::Operand(),ir::Operator::_return);
    mainFunction.addInst(&callGlobal);
    mainFunction.addInst(&defInst);
    mainFunction.addInst(&loadInst);
    mainFunction.addInst(&movInst1);
    mainFunction.addInst(&callInst);
    mainFunction.addInst(&movInst2);
    mainFunction.addInst(&lssInst);
    mainFunction.addInst(&gotoInst);
    mainFunction.addInst(&gotoInst1);
    mainFunction.addInst(&defInst2);
    mainFunction.addInst(&mulInst);
    mainFunction.addInst(&movInst3);
    mainFunction.addInst(&returnInst1);
    program.addFunction(mainFunction);
    std::cout << program.draw();
	// 进行验证
    ir::Executor executor(&program);
    std::cout << executor.run();
}
```

## **打印 IR 程序**
program.draw() 的结果如下：

```c
void global()
	0: def a, 0
	1: alloc arr, 2
	2: store 2, arr, 0
	3: store 4, arr, 1
	4: return null
end

int func(int p)
	0: subi t1, p, 1
	1: mov p, t1
	2: return p
end

int main()
	0: call t0, global()
	1: def b, 0
	2: load t2, arr, 1
	3: mov a, t2
	4: call t2, func(a)
	5: mov b, t2
	6: lss t3, b, a
	7: if t3 goto [pc, 2]
	8: goto [pc, 4]
	9: def t4, 2
	10: mul t5, b, t4
	11: mov b, t5
	12: return b
end

GVT:
	a int 0
	arr int* 2
```

## **执行 IR 程序**
​示例代码的最后两行是调用执行器运行生成的ir。执行过程将会跟踪每一步 value 的变化并输出最后 main 函数返回结果。

如果将宏 `DEBUG_EXEC_DETAIL` `DEBUG_EXEC_BRIEF` 打开，上述示例调用执行器将会有如下输出，打印出每一条 IR 指令的执行过程和最终返回结果 `6`。

```c
0: call t0, global()
0: def a, 0
	in get_des_operand(int a), value = 0
	in find_src_operand(intLiteral 0)	eval_int: 0
	des operand(int a), value = 0
1: alloc arr, 2
	in find_src_operand(intLiteral 2)	eval_int: 2
	in get_des_operand(int* arr), value = 0x9a2760
2: store 2, arr, 0
	in find_src_operand(intLiteral 0)	eval_int: 0
	in find_src_operand(intLiteral 2)	eval_int: 2
	in find_src_operand(int* arr), value = 0xa97380
3: store 4, arr, 1
	in find_src_operand(intLiteral 1)	eval_int: 1
	in find_src_operand(intLiteral 4)	eval_int: 4
	in find_src_operand(int* arr), value = 0xa97380
4: return null
1: def b, 0
	in get_des_operand(int b), new des (int b), value = 0
	in find_src_operand(intLiteral 0)	eval_int: 0
	des operand(int b), value = 0
2: load t2, arr, 1
	in find_src_operand(intLiteral 1)	eval_int: 1
	in find_src_operand(int* arr), value = 0xa97380
	in get_des_operand(int t2), new des (int t2), value = 0
3: mov a, t2
	in get_des_operand(int a), value = 0
	in find_src_operand(int t2), value = 4
	des operand(int a), value = 4
4: call t2, func(a)
	in get_des_operand(int t2), value = 4
	in find_src_operand(int a), value = 4
0: subi t1, p, 1
	in find_src_operand(int p), value = 4
	eval_int: 1
	in get_des_operand(int t1), new des (int t1), value = 0
1: mov p, t1
	in get_des_operand(int p), value = 4
	in find_src_operand(int t1), value = 3
	des operand(int p), value = 3
2: return p
	in find_src_operand(int p), value = 3
5: mov b, t2
	in get_des_operand(int b), value = 0
	in find_src_operand(int t2), value = 3
	des operand(int b), value = 3
6: lss t3, b, a
	in find_src_operand(int b), value = 3
	in find_src_operand(int a), value = 4
	in get_des_operand(int t3), new des (int t3), value = 0
	des operand(int t3), value = 1
7: if t3 goto [pc, 2]
	in find_src_operand(intLiteral 2)	eval_int: 2
	in find_src_operand(int t3), value = 1
	in goto: pc = 9
9: def t4, 2
	in get_des_operand(int t4), new des (int t4), value = 0
	in find_src_operand(intLiteral 2)	eval_int: 2
	des operand(int t4), value = 2
10: mul t5, b, t4
	in find_src_operand(int b), value = 3
	in find_src_operand(int t4), value = 2
	in get_des_operand(int t5), new des (int t5), value = 0
	des operand(int t5), value = 6
11: mov b, t5
	in get_des_operand(int b), value = 3
	in find_src_operand(int t5), value = 6
	des operand(int b), value = 6
12: return b
	in find_src_operand(int b), value = 6
6
```

## Global的处理
请注意源程序中并没有一个叫做 global 的函数，是因为需要**对全局变量进行初始化**，所以采用了这样一个特殊的做法

### 调用处理
​IR生成需涉及对全局变量、全局常量的处理。一种可行的方法是将global作为一个 function 进行处理，除去其中变量、常量定义声明的 IR 外，仍需生成一条 return null 的 IR。并在 main 函数中首先生成对global的调用IR。上面的示例就是采用这种方式。

*注：IR的结果仅供参考并不唯一，比如上面func中第0条和第1条就可用一条 `subi p, p, 1`​表示。语义分析处理方式不同，生成IR就可能不同。

