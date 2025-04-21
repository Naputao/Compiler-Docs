# **什么是IR**
​IR（Intermediate Representation）为中间表示。在编译系统中，编译器前端对高级编程语言（源程序）进行词法分析、语法分析、语义分析后会生成高层次 IR，在中端对高层次 IR 逐步降低到低层次 IR，并对其进行优化。后端根据降低优化后的 IR 生成目标架构汇编指令。

## **低层次抽象的 IR**
我们设计了一层形如 **（opcode，des，operand1，operand2）** 的 IR，其中 **opcode** 代表 IR 的种类决定了 IR 功能，**des** 是目的操作数，**operand1** & **operand2** 是源操作数

为了后端的实现简化，我们设计的 IR 更接近于汇编的层次，如
- 变量赋值IR
- 算术运算IR
- 逻辑运算IR
- 访存运算IR
- 类型转化IR
- 跳转IR

与 risc-v 汇编中对应算术运算、逻辑运算、访存、类型转换、跳转指令的含义基本相同。

同时为了屏蔽后端实现上的细节，我们为实现变量定义、函数调用与返回、指针运算等功能设计了以下几种 IR：
- 变量定义IR
- 调用返回IR
- 指针运算IR

具体功能可以参考 [IR 定义](ir_def.md)

## **抽象计算机模型**
组成原理告诉我们计算机由五个部分组成：运算器、控制器、存储器、输入设备、输出设备。

我们的 IR 可以视作在一个特定计算机模型上的一个指令系统，IR 可以在我们定义的计算机模型上完成计算机的所有功能，暂且称之为 **抽象计算机模型** 吧！我们还提供了一个软件来实现该计算机模型，同学们生成的 IR 将运行在这个软件上。


### **执行**
在**抽象计算机模型**中，控制器、运算器以 IR 为最小单位执行运算，操作数直接从存储中获取，每次执行一条 IR。根据 IR 的具体功能，可能会将运算器的结果写回存储器中，即写回目的操作数；也可能直接导致程序执行流的改变，即跳转 IR 或函数调用与返回 IR。

### **操作数**
在**抽象计算机模型**中有两种不同的运算器，浮点运算器和整型运算器，他们只能接受对应类型的操作数进行运算，所以操作数也被分为了整型和浮点型操作数，值得一提的是我们认为指针是整型的一种。

整型操作数可以分为：**整型变量**、**整型立即数**、**指向整型操作数的指针**、**指向浮点操作数的指针**

浮点操作数可以分为：**浮点变量**、**浮点立即数**

变量和指针操作数的值实际存放在**抽象计算机模型**的存储中，以 `Operand.name` 为唯一标识符在存储中查找得到。指针可以指向一片连续的空间用于存放数组，这一片空间只能通过 load & store IR 与基址指针来操作

> 注：
> 
> 源操作数必须是已经存在存储中的操作数，即可以通过操作数名称找到的，否则接下来的行为是未定义的
>
> 目的操作数如果不存在存储中，我们认为这是一个新的变量，并为其申请空间，如果存在则直接更新其在存储中的值
>
> 如果在存储中找到两个同名的操作数，接下来的行为是未定义的
>
> IR 是类型严格的，如果操作数类型与 **opcode** 指定的类型不符合，接下来的行为是未定义的

### **上下文**
在**抽象计算机模型**中运行的**程序**仍具有**函数**、**全局变量**、**局部变量**的概念。**IR 程序**的数据结构定义如下：
```C++
struct Program {
    std::vector<Function> functions;
    std::vector<GlobalVal> globalVal;
    Program();
    void addFunction(const Function& proc);
    std::string draw();
};
```
可以看到一个 IR 程序可以拥有多个**函数**、**全局变量**，其**入口应该为 main 函数**。每个函数在运行时，拥有自己的局部变量，也就是存放在在内存中的操作数，同时可以访问全局变量。函数在运行时的局部变量、运行位置即为**上下文**，在 IR 程序的运行过程中，**抽象计算机模型**维护了一个函数调用栈，发生函数调用时，会发生**上下文的切换**，原来的上下文将压入函数调用栈中，函数返回时，函数调用栈会将当前上下文弹出

**上下文切换**的具体含义是指：发生函数调用时，当前 IR 执行位置和存储中的操作数将被保存下来，执行流切换到下一个函数。新的函数在执行时 IR 将从第一条开始执行、存储中没有任何操作数。当从该函数返回时，将回到当初发生函数的调用的位置继续执行，存储中的操作数恢复为发生调用前保存的操作数

### **输入输出**
我们没有提供输入输出相关的 IR，可以通过调用**库函数**来与标准输入输出进行交互，例如：
```C++
int a = getint();
putch(a);
```
在 IR 中被直接翻译为函数调用：
```
1: call a, getint
2: call null, putch(a)
```

ir::Program 的 functions vector 中不应包含与库函数同名的函数，我们的 IR 测评机会对库函数进行特殊处理

## **IR 测评机**

IR 测评机的源码已经发放给大家了，结合文档和源码可以对 IR 测评机有一个更深入的认识，有任何问题都可以通过阅读源码来解决；接下来对其设计进行简要介绍

### **操作数与值**
以下代码为操作数定义了一种数据结构 ir::Value，包括了操作数的值和类型
```C++
union _4bytes {
    int32_t ival;
    float   fval;
    int*    iptr;
    float*  fptr;
};

// definition of value of a operand in memory
struct Value {
    Type t;
    _4bytes _val;
};

```

### **函数与上下文**
ir::Context 为一个执行中的 ir::Function 保存了其需要的基本数据包括

    - pc            : 当前执行的指令的位置
    - retval_addr   : 可能的返回值地址，如果该指针不为空的话就在 return IR 中写该地址
    - mem           : 该函数运行过程中的操作数以及其对应的值
    - pfunc         : 指向被指向的 ir::Function 的指针，用于获取 IR 指令等等
    
```C++
// definition of function context
struct Context {
    uint32_t pc;                            // program counter of a function
    Value* retval_addr;                   // if it's not nullptr, this addr will be written when exit a context, 
    std::map<std::string, Value> mem;
    const ir::Function* pfunc;              // executing which function 

    /**
     * @brief constructor
     */
    Context(const ir::Function*);
};
```

### **全局变量**
值得单独一提的是全局变量，在设计过程中，为了实验三翻译为汇编更加方便，全局变量必须通过 ir::Program 中的 `std::vector<GlobalVal> globalVal` 来传递

IR 测评机会根据 GlobalVal 的 maxlen 字段和本身的类型为该全局变量申请一片初始化为零的空间(类似于汇编中的 .space 伪指令)，如果是数组则分配一个 maxlen 长度的全 0 数组，如果是整形或者浮点型则初始化操作数的值为 0；并将该操作数放到 ir::Executor 中的 global_vars 中

**所以如果全局变量的初始值不为 0 时，你需要自己在 main 函数的一开始（或其他你觉得合适的地方）为这些全局变量赋值，一个参考的实现可以见 [例子](./ir_examples.md)**


### **IR 测评机**
IR 测评机实际上是去执行一个 ir::Program，其成员变量包含了执行中必须储存的一些数据结构，如

    - cxt_stack : 函数执行栈
    - cur_ctx   : 当前执行的函数上下文
    - global_vars : 全局变量表
        ...

提供了 `int run();` 函数从 main 函数开始来执行整个 ir::Program，并返回 main 函数的返回值
```C++
struct Executor {
    const ir::Program* program;
    std::map<std::string, Value> global_vars;

    Context* cur_ctx;
    std::stack<Context*> cxt_stack;

    /**
     * @brief constructor
     */
    Executor(const ir::Program*, std::ostream& os = std::cout);

    /**
     * @brief execute the ir program and return its main function's return value
     * @return int: the main function's return value
     */
    int run();

    /**
     * @brief execute next n IRs
     * @return true : execute without error occurs
     * @return false: sth bad happens
     */
    bool exec_ir(size_t n = 1);
}
```
