# **IR 库**

​实验中助教们会提供由 IR 相关实现打包成的静态库与 IR 相关的 .h 文件，为了避免部分同学可能会因修改 .cpp 文件导致测评不通过，**请不要修改 IR 库或者是 IR 测评机相关实现**，因为**线上测评使用我们提供的静态库去链接，你的修改并不会生效**

## **ir.h**

​该文件对 IR 库中所有头文件进行了引入，同学们使用中只需引入该头文件即可
```C++
#ifndef IR_ALL_H
#define IR_ALL_H

#include"ir_operand.h"
#include"ir_operator.h"
#include"ir_instruction.h"
#include"ir_function.h"
#include"ir_program.h"

#endif
```

## **ir_operand.h**

该文件中​是对 IR 操作数的封装定义。我们对IR操作数进行类封装，将其视为具有name、type属性的复杂数据类型。这样将操作数绑定类型对于后续中端优化、后端处理等非常方便（毕竟类型系统也是语义分析一个重点）。
```C++
struct Operand {
    std::string name;
    Type type;
    Operand(std::string = "null", Type = Type::null);
};
```

​该文件对所有可能操作数类型 **Type** 进行枚举定义。这里的类型与 C 或 C++ 标准类型略有不同，如下所示：
```C++
enum class Type {
    Int,
    Float,
    IntLiteral,
    FloatLiteral,
    IntPtr,
    FloatPtr,
    String,
    null
};
std::string toString(Type t);
```

其中Int、Float为整型、浮点型变量，IntLiteral、FloatLiteral 为立即数整型、立即数浮点型，IntPtr、FloatPtr 为整型指针、浮点型指针（对于指针的支持将在拓展实验中供同学们选择），当函数的返回值为 void 时，我们提供了特殊的 null 类型。我们还提供了 ```string toString(Type t)``` 函数来打印 Type。



## **ir_operator.h**
​对IR操作符进行定义，以枚举类的形式。与 Type 的 toString 函数类似，接受一个操作符的枚举类型，返回对应字符串形式。各操作符具体含义可在 [IR定义]() 指导书中查阅。
```C++
enum class Operator {
    _return,    // return   op1
    _goto,      // goto     [op1=cond_var/null],    des = offset
    call,       // call     op1 = func_name,    des = retval  /* func.name = function, func.type = return type*/
    // alloc [arr_size]*4 byte space on stack for array named [arr_name], do not use this for global arrays
    alloc,      // alloc    op1 = arr_size,     des = arr_name
    store,      // store    des,    op1,    op2    op2为下标 -> 偏移量  op1为 store 的数组名, des 为被存储的变量
    load,       // load     des,    op1,    op2    op2为下标 -> 偏移量  op1为 load 的数组名, des 为被赋值变量
    getptr,     // op1: arr_name, op2: arr_off

    def,
    fdef,
    mov,
    fmov,
    cvt_i2f,    // convert [Int]op1 to [Float]des 
    cvt_f2i,    // convert [Float]op1 to [Int]des
    add,
    addi,
    fadd,
    ...
}
```


## **ir_instruction.h**

`struct Instruction` 是 IR 指令的基类定义。成员变量包括 Operand 类型的两个源操作数与结果操作数以及 Operator 类型的操作符，四者也是四元式形式IR的组成。成员函数包括无参构造函数和全参构造函数，具体使用可参考ir_example.cpp中代码示例。
```C++
struct Instruction {
    Operand op1;
    Operand op2;
    Operand des;
    Operator op;
    Instruction();
    Instruction(const Operand& op1, const Operand& op2, const Operand& des, const Operator& op);
    virtual std::string draw() const;
};
```
`virtual std::string draw() const;` 定义了各类型指令输出格式，并以字符串形式返回

由于函数调用指令较为特殊，需额外传入函数调用实参，这里对其进行额外定义。`Struct CallInst` 在继承基类 Instruction 的基础上多了argumentList成员变量，用于存入函数调用实参。该类中也对Instruction基类中draw方法进行重写。
```C++
struct CallInst: public Instruction{
    std::vector<Operand> argumentList;
    CallInst(const Operand& op1, std::vector<Operand> paraList, const Operand& des);
    CallInst(const Operand& op1, const Operand& des);   //无参数情况
    std::string draw() const;
};

```

## **ir_function.h**

​对函数块的定义，实质上是用于添加存放输入源程序中某个函数生成的IR指令。对各成员变量的说明如下：

- name：函数块名称，可以直接将源程序中函数名作为name。对于全局生成的IR指令，存入的函数块名称在不冲突情况下可简单命名为“global”（这里只是助教举的一个例子~）
- returnType：函数返回类型，即对应源程序中函数的返回类型。对于全局以及void类型，`ir::Type`中的`null`就派上用场了。
- ParameterList：函数形参列表。该列表可以为空（无形参情况）。列表中元素为Operand，意味着传入的形参要连带类型进行封装处理。
- InstVec：函数对应的IR指令。

```C++
struct Function {
    std::string name;
    ir::Type returnType;
    std::vector<Operand> ParameterList;
    std::vector<Instruction*> InstVec;
    Function();
    Function(const std::string&, const ir::Type&);
    Function(const std::string&, const std::vector<Operand>&, const ir::Type&);
    void addInst(Instruction* inst);
    std::string draw();
};
```
`void addInst(Instruction* inst);` 用于函数块初始化后向其中添加IR指令。

`std::string draw();` 函数块的输出方式定义，除调用 InstVec 中各指令的 draw 方法外，还定义了函数名、返回类型、函数形参的输出格式。

## **ir_program.h**

​对程序体的定义，实质上是用于添加存放上述函数块，一个输入源程序即对应一个程序体，该源程序中生成的所有IR指令均在程序体中存放。
```C++
struct Program {
    std::vector<Function> functions;
    std::vector<GlobalVal> globalVal;
    Program();
    void addFunction(const Function& proc);
    std::string draw();
};
```
​
除了函数体外，还需存放源程序中全局变量（这不仅仅是用于测评的需要，在后端生成汇编过程中也需对全局变量进行单独处理！）`ir::Operand val` 是全局变量的类型和名字，如果全局变量是一个数组时，`int maxlen` 是应该为数组申请的长度，否则应该为 0
```C++
struct GlobalVal {
    ir::Operand val;
    int maxlen = 0;     //为数组长度设计
    GlobalVal(ir::Operand va);
    GlobalVal(ir::Operand va, int len);
};
```
`void addFunction(const Function& proc);` 用于程序体初始化后向其中条件函数体。

`std::string draw();` 程序体的输出方式定义。除调用各函数体的draw方法外，还定义了全局变量的输出方式。

