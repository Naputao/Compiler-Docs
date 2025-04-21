# **目标代码生成**

目标代码生成的结果是汇编，汇编经过 gcc 的汇编器处理之后，变为可执行文件。要完成这一部分实验，需要对汇编和可执行程序有深刻的理解。**这篇文档主要是在告诉你们需要生成什么样的汇编代码，你们应该解决的问题是如何完成一个生成这样的汇编代码的程序，当然文档里也有适当的提示**

## **0. 前置知识**

虽然你们可能没有专门学过汇编，但是组成原理课和硬件综合设计中你们已经和它打过交道了。一切的出发点，来自于组成原理，在这门课中你已经了解了指令如何在硬件上运行，现在你应该**学习并实现如何用一条条指令来实现高级语言程序的功能**了，汇编只是指令的助记符而已。以下重新介绍一下组成原理相关知识，以免你们已经忘记它了。

### **冯诺依曼结构**

诺依曼结构（Von Neumann architecture）是一种计算机体系结构，以数学家冯·诺依曼（John von Neumann）的名字命名。它是一种将程序指令和数据存储在同一存储器中的计算机设计原则，也被称为存储程序计算机（stored-program computer）。

在冯诺依曼结构中，计算机系统包括以下主要组件：

1. 中央处理器（Central Processing Unit，CPU）：负责执行指令和处理数据的核心部分，包括算术逻辑单元（Arithmetic Logic Unit，ALU）和控制单元（Control Unit）。


2. 存储器（Memory）：用于存储指令和数据的设备，包括主存储器（Main Memory）和辅助存储器（Auxiliary Memory）。


3. 输入/输出设备（Input/Output Devices）：用于与外部设备进行交互，如键盘、鼠标、显示器、硬盘等。

**存储程序概念是冯诺依曼结构的关键特征之一**。根据这一概念，计算机可以将指令和数据存储在同一存储器中，并按照地址访问。它将程序指令看作数据的一种形式，计算机可以像操作数据一样操作指令，使得程序可以被存储、加载和执行。

### **可执行文件与其内存映像**
可执行文件是一种用于在计算机系统上执行的二进制文件格式。它包含了计算机程序的机器代码、数据、符号表和其他必要的信息，包括头部、**代码段**、**数据段**、符号表和重定位表等部分。

程序执行的内存映像是**可执行文件在计算机被执行过程中的内存布局和状态**。它包括**代码段**、**数据段**、**堆栈**和其他可执行文件所需的资源。代码段存储程序的指令，数据段存储静态数据和全局变量，堆用于动态分配内存，栈用于函数调用和局部变量的存储。内存映像还包括处理器寄存器的状态和其他与程序执行相关的信息。

![可执行文件与其内存映像](assets/elf_mem.png)

    注：上图中 <%esp> 是 x86 中的栈指针，riscv 中应为 sp

### **用汇编来描述可执行文件！**
汇编文件可以描述不同的节及其数据（根据存储程序概念，这里的数据有一部分就是指令），在汇编中可以通过特定的语法来描述节的开始，在节与节之间的填写指令和伪指令，由汇编器将其转换为二进制的数据，即可执行文件

你生成的汇编程序大概包括以下部分:
```arm
    .data
     ...
 
    .bss
     ...

    .text

# f 是源程序中的一个函数，通过 jr  ra 返回
f:
    ...
    jr  ra

# main 是源程序中的一个函数，执行过程中通过 jal f 调用函数 f，通过 jr  ra 返回
main:
    ...
    jal f
    ...
    jr  ra
```

**.data** 表示数据段开始，接下来可以使用 `.word` `.byte` `.commn` 数据相关的伪指令来记录数据，通常是指用来存放程序中已初始化的全局变量的一块内存区域，数据段属于静态内存分配

**.bss** 表示 bss(Block Started by Symbol) 段开始，可以使用 `.space` 等指令分配初始化为 0 的一块区域，属于静态内存分配

**.text** 表示代码段开始，通常是指用来存放程序执行代码的一块内存区域。这部分区域的大小在程序运行前就已经确定，并且内存区域通常属于只读, 某些架构也允许代码段为可写，即允许修改程序。在代码段中，也有可能包含一些只读的常数变量，例如字符串常量等

`f` 和 `main` 在这里被叫做符号或标签，他们本身不会被真正存放在代码段中，他们代表的是下一条指令的地址，如果在指令中使用了该符号，汇编器在汇编时会填入该地址


**`jal f`** 的反汇编结果如下，`10350` 是这一条指令的地址，`3fe1` 是这条 jal 指令对应的二进码，`jal	10328 <f>` 中 `10328` 是符号 `f` 所代表的地址，也就是 **函数f** 的第一条汇编的地址

       10350:	3fe1                	jal	10328 <f>

**汇编中的指令和伪指令只是助记符，每一条其实就代表了一段二进制码，不同的节中的指令由汇编器放到不同的地方，所以用汇编就可以描述可执行文件！**

### **从哪里获得示例和参考？**
为了清晰的看到汇编是如何转化为可执行文件，对于一个 SysY 源程序，你可以把他转化为 C 文件，通过 gcc 编译成汇编和可执行文件，可执行文件可以通过 objdump 进行反汇编，观察汇编与 dump 结果。同时 gcc 的汇编结果可以作为你生成汇编程序的参考

> 不知道工具如何使用？ 文档不会告诉你的，STFW！


### **程序二进制接口**
程序二进制接口 **ABI（application binary interface）** 定义了机器代码（即汇编）如何访问数据结构与运算程序，它包含了

**数据类型的大小、布局和对齐**

**函数调用约定**

**系统调用约定**

**二进制目标文件格式**

等内容。决定要不要采取既定的ABI通常由编译器，操作系统或库的开发者来决定。但如果撰写一个混和多个编程语言的应用程序，就必须直接处理ABI，采用外部函数调用来达成此目的。

我们在开发编译器的过程中，生成的汇编文件应 **遵循 riscv ABI 规范**，这样我们编译器的生成的汇编才可以使用库函数，正确的被加载，并在执行后正确的返回。
> 如果不这么做就会出现各种奇奇怪怪的段错误！你可能不了解 riscv ABI，但是我想你应该知道怎么做

## **1. 内存管理**
我们知道在 ir 中，每个函数在执行时都需要维护自己的上下文，包括局部变量、运行位置。在程序执行的过程中，我们同样需要在内存中的栈上保存他们。

### **变量寻址**
在 IR 测评机中我们屏蔽掉了内存上的细节，IR 测评机保证你可以通过名字找到操作数，但是汇编中只能从内存中的某一个地址读取数据。所以我们需要对内存进行管理和分配，并记录内存地址与变量的对应关系。在变量分配的过程中，需要考虑 **由 ABI 规定的数据类型的大小、布局和对齐** 等问题

因为函数的局部变量保存在栈上，可以使用 **栈指针 + 偏移量** 的方法来确定变量在内存中的位置。在框架代码中为你们提供了这样一个数据结构，将变量与栈指针偏移量做映射，在内存中一一对应

```C++
struct stackVarMap {
    std::map<ir::Operand, int> _table;

    /**
     * @brief find the addr of a ir::Operand
     * @return the offset
    */
    int find_operand(ir::Operand);

    /**
     * @brief add a ir::Operand into current map, alloc space for this variable in memory 
     * @param[in] size: the space needed(in byte)
     * @return the offset
    */
    int add_operand(ir::Operand, uint32_t size = 4);
};
```
局部变量寻址由函数 `int find_operand(ir::Operand);` 返回的偏移量 + 栈指针来实现；向 table 中添加变量并维护变量与偏移量的映射由 `int add_operand(ir::Operand, uint32_t size = 4);` 来实现，**你需要实现这两个函数**

**变量与偏移量的映射** 只是一个逻辑映射，产生汇编代码时认为变量的值存放与此，你需要产生汇编代码来完成内存的分配、使用 load/store 操作相应地址来 读取/存放 变量的值

### **示例**
以 **函数f** 为例子说明内存管理的内容，其定义如下：
```C++
void f() {
    int a,b;
    int A[5];
    ...
}
```

该函数使用了两个整形变量和一个数组，共 **2x4 **+** 5x4** = **28** bytes

其映射可以为：
    
    {a, Int}        : sp+4
    {b, Int}        : sp+8
    {A, IntLiteral} : sp+12

那么在栈中操作变量值的汇编为
```arm
# a
lw  t0, 4(sp)
sw  t0, 4(sp)

# b
lw  t0, 8(sp)
sw  t0, 8(sp)

# A[1]
lw  t0, 16(sp)
sw  t0, 16(sp)
```

> A 数组占用 20 bytes，从 sp+12 到 sp+28，但是可以有两种存放顺序
>
> 1. A[0] 存放在 sp+12，其余依次递增
>
> 2. A[0] 存放在 sp+28，其余依次递减
>
> 此处 A[1] 的地址计算为 &A[0] + 4，只是举例说明，不一定正确，你需要根据 riscv 对数组顺序的规定来生成对应的代码

## **2. 函数调用**

### **栈与栈指针**

内存中的栈用于存储函数调用过程中的局部变量、函数参数、返回地址等信息，通过栈指针来管理。

栈指针的变化反映了栈的状态，包括栈的扩展和收缩。当**函数被调用时**，栈指针会**向下移动**，为局部变量和其他相关数据**分配空间**；当函数返回时，栈指针会**向上移动**，**释放已分配的空间**，恢复到调用该函数之前的状态。

### **函数调用约定**
函数调用过程通常分为以下六步：
1. 调用者将参数存储到被调用的函数可以访问到的位置；
2. 跳转到被调用函数起始位置；
3. 被调用函数**获取所需要的局部存储资源，按需保存寄存器(callee saved registers)** ；
4. 执行函数中的指令；
5. **将返回值存储到调用者能够访问到的位置，恢复之前保存的寄存器(callee saved registers)，释放局部存储资源**；
6. 返回调用函数的位置。
> 查阅相关资料阅读 **riscv calling convention** 相关内容，推荐 [riscv 官方技术手册](https://riscv.org/technical/specifications/) 

callee saved registers 是那些 caller 不希望在函数调用中被改变的寄存器，如果 callee 用到了这些寄存器，应该把他们保存下来并在函数调用返回时恢复

函数调用约定规定了函数调用者（caller）和被调用者（callee）分别需要做的事情，以及如何去做，以下分别介绍如何使用汇编实现函数调用

### **caller 示例**
caller 需要执行步骤 1 和 2 —— **将参数存储到被调用的函数可以访问到的位置，跳转到被调用函数起始位置**

其汇编应实现为
```arm
caller:
    # 将参数存储到被调用的函数可以访问到的位置，查阅 riscv ABI 完成此项
    ...
    # 跳转到 callee 的第一条指令所在地址
    jal callee
    # 函数调用约定保证 callee 返回后执行 jal callee 的下一条指令
    ...
```

`jal label` 其实是 `jal x1, imm` 的伪指令，其功能为将 PC+4 存放到 x1 寄存器，并使 PC += imm；callee 只需要使用指令取出 x1 的值并跳转，即可回到 caller 原来执行的位置继续执行
> callee 知道 caller 会将 PC+4 存放在 x1 中，才可以在结束时跳转回这个地址，**这便是函数调用约定的意义**，你知道为什么是 x1 吗？

### **callee 示例**
**每一个函数都可能是被调用者，所以每一个函数的汇编实现都应该遵守被调用函数的约定**

callee 需要在开始时先将 callee saved registers 保存到栈上，即将需要保存的寄存器 push 到内存的栈中；然后进行内存分配 —— 通过将 sp 向下移动来实现；此时才可以执行实现函数功能所需要的指令；执行完成后，需要向上移动 sp 来回收分配给该函数的栈空间，再 pop 出 callee saved registers 到原来的寄存器里，将返回值存储到调用者能够访问到的位置，最后跳转回原来的位置

其汇编应实现为
```arm
callee:
    # 将 callee saved registers 保存到栈上
    # 查阅 riscv ABI 以明白哪些是 callee saved registers，此处以保存 x1 为例
    addi    sp, sp, -4
    sw      x1, 4(s0)
    ...

    # 内存分配，分配的栈空间用于存放局部变量，按需分配
    addi    sp, sp, -xxx
    
    # 实现函数功能所需指令
    ...
    
    # 内存回收，与分配值相同
    addi    sp, sp, xxx

    # 将保存到栈上的 callee saved registers 重新 pop 到原寄存器 
    ...
    lw      x1, 4(s0)
    addi    sp, sp, 4
    
    # 返回
    # 将返回值存储到调用者能够访问到的位置，查阅 riscv ABI 完成此项
    ...
    # 最后，根据函数调用约定，调用者的 PC+4 就存放在 x1 中，跳转回去即可
    jr      x1
```

## **3. 全局变量**
全局变量存放在内存的数据段中，在汇编可以使用 `.space` `.word` 等伪指令声明，通过标签对其进行寻址

### **示例**
定义一个全局变量 `int a = 7;`，以下展示如何声明并对他进行寻址

```arm
.data
a:  .word   7
```

使用 `lw rd, symbol` 可以加载全局变量的值，`sw rd, symbol, rt` 可以保存全局变量的值 
```arm
lw  t0, a       # 加载
sw  t0, a, t1   # 保存
```
## **4. 生成指令与函数**

### **riscv 寄存器与指令数据结构定义**

代码框架中定义了一些 riscv 相关的数据结构，[rv_def.h](./src/include/backend/rv_def.h) 定义了 riscv 寄存器、指令的枚举类，此处并没有列举出所有的指令类型，你需要时可以自行添加

```C++
// rv interger registers
enum class rvREG {
    /* Xn       its ABI name*/
    X0,         // zero
    X1,         // ra
    X2,         // sp
    X3,         // gp
    X4,         // tp
    X5,         // t0
    ...
};
std::string toString(rvREG r);  // implement this in ur own way

enum class rvFREG {
    F0,
    F1,
    F2,
    F3,
    F4,
    F5,
    ...
};
std::string toString(rvFREG r);  // implement this in ur own way

// rv32i instructions
// add instruction u need here!
enum class rvOPCODE {
    // RV32I Base Integer Instructions
    ADD, SUB, XOR, OR, AND, SLL, SRL, SRA, SLT, SLTU,       // arithmetic & logic
    ADDI, XORI, ORI, ANDI, SLLI, SRLI, SRAI, SLTI, SLTIU,   // immediate
    LW, SW,                                                 // load & store
    BEQ, BNE, BLT, BGE, BLTU, BGEU,                         // conditional branch
    JAL, JALR,                                              // jump

    // RV32M Multiply Extension

    // RV32F / D Floating-Point Extensions

    // Pseudo Instructions
    LA, LI, MOV, J,                                         // ...
};
std::string toString(rvOPCODE r);  // implement this in ur own way
```


[rv_inst_impl.h](./src/include/backend/rv_inst_impl.h) 定义了一个通用的 riscv 指令数据结构（当然你可以不使用它，选择你喜欢的实现方式
```C++
struct rv_inst {
    rvREG rd, rs1, rs2;         // operands of rv inst
    rvOPCODE op;                // opcode of rv inst
    
    uint32_t imm;               // optional, in immediate inst
    std::string label;          // optional, in beq/jarl inst

    std::string draw() const;
};
```
通过 `std::string draw() const` 对不同 rvOPCODE 进行不同的输出，可以使该数据结构支持普通指令 (opcode, rd, rs, rt) ，也可以支持立即数指令(opcode, rd, rs, imm)，还可以支持在该指令前打上标签(label: opcode, rd, rs, rt) 或是跳转指令 (jump, rd, label)

### **生成指令**
接下来我们考虑如何**将 IR 翻译为指令**，我们的 IR 其实与指令十分相似，只是 IR 中没有寄存器的概念，变量值直接从内存中读取，现在我们需要使用 load & store 指令从内存中获取变量，加载到某个寄存器，在此过程中需要**处理寄存器分配，考虑 ABI 对特定寄存器的功能的规定**

一种简单的处理的处理方式是不进行寄存器的分配，将每条 IR 的 op1 & op2 对应地址的值 load 到临时寄存器 t0 & t1，使用相应的 riscv 指令进行运算，指令的 rd 选择固定的 t2，然后将其 store 回 des 所对应的地址

根据 **1. 内存管理** 的介绍，你已经知道怎么处理**局部变量**的地址了，记得处理**全局变量**这个例外情况。假设一条 IR 为 `add sum, a, b`，他们都是局部变量，那么其汇编应实现为：
```arm
lw  t0, xx(sp)  # load Operand(a) 到 t0
lw  t1, xx(sp)  # load Operand(b) 到 t1
add t2, t0, t1
sw  t2, xx(sp)  # store t2 到 Operand(sum) 对应地址
```
> 并不是每一种 IR Operator 都有对应的指令，但是你可以通过指令的组合实现，具体请查阅 riscv 手册

代码框架种定义了接口
```C++
void gen_instr(const ir::Instruction&);
```
你可以通过实现该函数来完成 IR 到指令的生成过程，其伪代码大概如下，记得考虑全局变量的情况：
```C++
void backend::Generator::gen_instr(const ir::Instruction& inst) {
    // if local    : get_ld_inst() -> {op = lw, rd = t0, rs = sp, imm = map.find_operand(inst.op1)}; 
    // if global   : get_ld_inst() -> {op = lw, rd = t0, label = inst.op1.name}; 
    rv::rv_inst ld_op1 = get_ld_inst(inst.op1);
    rv::rv_inst ld_op2 = get_ld_inst(inst.op2);

    // translate IR into instruction
    rv::rv_inst ir_inst;
    switch (inst.op) {
    case ir::Operator::add:
        ir_inst = {op = add, rd = t2, rs = t0, rt = t1};
        break;
    ...
    default:
        assert(0 && "illegal inst.op");
        break;
    }
    
    rv::rv_inst st_des = get_st_inst(inst.des);
    
    output(ld_op1, ld_op2, ir_inst, st_des);
}
```

### **寄存器分配**
在以上的介绍中，我们使用了固定的寄存器作为源操作数和目的操作数，但是这样程序就需要经常进行访存，所以需要进行寄存器分配，为程序处理的值找到存储位置的问题。这些变量可以存放到寄存器，也可以存放在内存中。寄存器更快，但数量有限。内存很多，但访问速度慢。好的寄存器分配算法尽量将使用更频繁的变量保存的寄存器中。

代码框架中提供了一套 api，你可以在根据自己的需求修改并实现他们以进行寄存器的分配
> 即使你不想做寄存器的分配，你也应该在 gen_instr 使用这一套 api 而不是写死 t0 t1 t2，固定分配只需要将 api 实现为返回固定寄存器即可，例如 **getRd 实现为 return rv::rvReg::X7;**。当你在后续的实验中做寄存器分配时就只需要修改 api 的内部实现，这样做程序才拥有可扩展性

```C++
// reg allocate api
rv::rvREG getRd(ir::Operand);
rv::rvFREG fgetRd(ir::Operand);
rv::rvREG getRs1(ir::Operand);
rv::rvREG getRs2(ir::Operand);
rv::rvFREG fgetRs1(ir::Operand);
rv::rvFREG fgetRs2(ir::Operand);
```

### **生成函数**
在 **3. 函数调用** 的 **callee 示例** 种详细介绍了一个函数的汇编实现，代码框架种定义了接口
```C++
void gen_func(const ir::Function&);
```
你可以通过实现该函数来完成 IR Function 到函数汇编指令的生成过程，其伪代码大概如下：
```C++
void gen_func(const ir::Function& func) {
    // do sth to deal with callee saved register & subtract stack pointer
    ...
    output(...);

    // translate all IRs in InstVec into assembly
    for (auto inst: func.InstVec) {
        gen_instr(*inst);
    }

    // do sth to pop callee saved register & recovery stack pointer
    ...
    output(...);

    // gen instructio to jump back
    rv::rv_inst jump_back = {op = jr, rd = x1};
    output(jump_back);
}
```

## **5. 程序接口**
在本次实验中，你们需要实现 Generator 类，main 函数保证调用 `void gen();` ，你需要在该函数中实现 ir::Program 到 riscv 汇编程序的转化，并将生成的汇编程序写入 `fout` 中
```C++
struct Generator {
    const ir::Program& program;         // the program to gen
    std::ofstream& fout;                 // output file

    Generator(ir::Program&, std::ofstream&);

    // reg allocate api
    rv::rvREG getRd(ir::Operand);
    rv::rvFREG fgetRd(ir::Operand);
    rv::rvREG getRs1(ir::Operand);
    rv::rvREG getRs2(ir::Operand);
    rv::rvFREG fgetRs1(ir::Operand);
    rv::rvFREG fgetRs2(ir::Operand);

    // generate wrapper function
    void gen();
    void gen_func(const ir::Function&);
    void gen_instr(const ir::Instruction&);
};

```

`void gen();` 应先处理全局变量 `program.globalVal`，再遍历 `program.functions` 调用 `void gen_func(const ir::Function&)` 对函数进行翻译

