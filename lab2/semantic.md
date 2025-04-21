# 语义分析

## **1. 语义分析基本思路**

我们经过词法和语法分析之后已经得到了 AST，这其实是 SysY 程序的另一种形式的表示。源程序代码中的各种顺序、结构信息都存储在树中，我们可以通过**深度遍历语法树**按源程序的顺序来分析源程序。

### **以下对语义分析中的一些重点问题做一些讨论，你们也可以修改下面的设计以符合自己的思路**

## **2. 作用域与符号表**
在 Sysy 中, 作用域是由 Block 决定的, 允许嵌套且不同作用域中可以定义同名变量。在翻译成 IR 的过程中我们需要解决不同作用域中同名变量的问题, 我们的解决方案是重命名, 为变量名加上与作用域相关的后缀使得重命名之后的变量名字在一个 IR Function 中是独一无二的

### **符号**
```C++
struct STE {
    ir::Operand operand;
    vector<int> dimension;
};
```
**Symbol Table Entry(STE)** 是符号表中的一条记录，`ir::Operand operand` 记录了符号的名字和类型，但是对于数组来说，我们不止需要知道名字和类型，在语义分析的过程中还需要的`vector<int> dimension`

### **作用域**
为支持重命名, 我们需要一个数据结构来存储作用域相关的信息, 每个作用域有自己的属性来唯一标识自己, 还有一张表来存储这个作用域里所有变量的名称和类型
```C++
using map_str_ste = map<string, STE>;
// definition of scope infomation
struct ScopeInfo {
    int cnt;
    string name;
    map_str_ste table;
};
```
cnt 是作用域在函数中的唯一编号, 代表是函数中出现的第几个作用域

name 可以用来分辨作用域的类别, 'b' 代表是一个单独嵌套的作用域, 'i' 'e' 'w' 分别代表由 if else while 产生的新作用域（你也可以取你喜欢的名字，只是这样会表意比较清晰）

table 是一张存放符号的表, {string: STE}, string 是操作数的原始名称, 表项 STE 实际上就是一个 IR 的操作数，即 STE -> Operand, 在 STE 中存放的应该是变量重命名后的名称

### **符号表**

作用域是支持嵌套, 我们决定使用栈式结构来存储
```C++
struct SymbolTable {
    vector<ScopeInfo> scope_stack;
    map<std::string,ir::Function*> functions;
    
    ...
}
```
并为符号表提供了一些成员函数, 用于查询变量, 并提供 ScopeInfo 相关的操作

    void add_scope(Block*);                                 进入新作用域时, 向符号表中添加 ScopeInfo, 相当于压栈

    void exit_scope();                                      退出时弹栈

    string get_scoped_name(string id) const;                输入一个变量名, 返回其在当前作用域下重命名后的名字 (相当于加后缀)

    Operand get_operand(string id) const;                   输入一个变量名, 在符号表中寻找最近的同名变量, 返回对应的 Operand(注意，此 Operand 的 name 是重命名后的)

    STE get_ste(string id) const;                           输入一个变量名, 在符号表中寻找最近的同名变量, 返回 STE


## **3. 表达式**
观察文法可以发现, 表达式的文法展开其实和计算顺序是一致的, 只需要自底向上翻译, 即可得到正确的 IR 序列

在表达式计算还需要考虑几个其他的问题: **类型转换**, **临时变量的产生与管理**, 以及可以在分析树中做的**常数合并优化**

对于表达式相关的 AstNode 我们需要增加几个属性来记录一些信息以完成以上需求 

    Exp.is_computable                                       节点以下子树是否可以化简为常数, 通过该变量, 大部分常数合并可以直接在语法树中自底向上进行传递
    
    Exp.v                                                   一个字符串, 或者是重命名后的变量名, 或者是临时变量名称, 也可以是常数字符串
    
    Exp.t                                                   Type, 表示该表达式计算得到的类型

对于一个表达式相关的节点, 其值可以由 Operand(v, t) 来表示, 在自底向上的分析过程中认为子树的值将保存在 Operand(v, t) 所代表的操作数内, 这样的规定意味着：
- 在完成该子树的分析后，应生成一条以 Operand(v, t) 为目标操作数的 IR
- 在自底向上的过程中，可以认为该子树代表的值就存放在 Operand(v, t) 在之后的分析过程中可以使用

以表达式

    a + b / 10;

为例，其应该生成的语法树为
```json
{
    "name" : "Exp",
    "subtree" : [
    {
        "name" : "AddExp1",
        "subtree" : [
                ···
                {
                    "name" : "Terminal",
                    "type" : "IDENFR",
                    "value" : "a"
                }
                ...
            ]
            },
            {
                "name" : "Terminal",
                "type" : "PLUS",
                "value" : "+"
            },
            {
                "name" : "AddExp2",
                "subtree" : [
                    {
                    "name" : "MulExp",
                    "subtree" : [
                        {
                        ···
                        {
                            "name" : "Terminal",
                            "type" : "IDENFR",
                            "value" : "b"
                        }
                        ···
                        },
                        {
                            "name" : "Terminal",
                            "type" : "DIV",
                            "value" : "/"
                        },
                        ···                   
                        {
                            "name" : "Terminal",
                            "type" : "INTLTR",
                            "value" : "10"
                        }
                    ] 
                    }
                ]
            }
        ]
    }
    ]
}
```
以 Exp 为根节点，在分析这颗语法树时，我们采用深度遍历自底向上的方式，首先遇到的是第一个左子树 AddExp
```json
    "name" : "AddExp1",
    "subtree" : [
        ···
        {
            "name" : "Terminal",
            "type" : "IDENFR",
            "value" : "a"
        }
        ...
    ]
```
从 AddExp 开始向下，每一层都只有一个节点，我们之前提到一个表达式相关节点可以由 Operand(v, t) 来表示他的值，所以问题的关键是如何生成这个值对应的 IR，以下提供一种
原来的语法树结构大概如下所示


    AddExp -> MulExp -> UnaryExp -> PrimaryExp -> LVal -> Terminal(IDENFR, a)

在加上节点自己的属性后应该为这样：

    AddExp(v_add1, t) -> MulExp(v_mul, Int) -> UnaryExp(v_uan, Int) -> PrimaryExp(v_pri, Int) -> LVal(v_lva, Int) -> Terminal(IDENFR, a)

在分析的过程中，最底层的 `LVal(v_lva, Int) -> Terminal(IDENFR, a)` 中变量 a 应是一个已定义的变量，可以使用 **SymbolTable::get_operand(string id);** 找到对应的 Operand，然后产生由 `(v_lva, Int) -> (v_pri, Int) -> (v_uan, Int) -> (v_mul, Int) -> (v_add1, t)` 赋值的 IR。另一种方法是，为避免产生这么多无用的赋值，值进行语法树属性的传递，即通过语法树属性 (v, t) 的赋值，使 AddExp(v_add1, t) 与 Terminal(IDENFR, a) 对应的 Operand 相同

分析完 Exp 的第一个子节点 AddExp1 后接下来第二个节点是 `Terminal(PLUS, +)`，待对第三个节点 AddExp2 分析完成后，得到代表第三个节点值的 Operand(v_add2, t)，即可生成一条加法 IR

    add     v_exp, v_add1, v_add2

这里的 (v_exp, t) 是代表 Exp 节点的值的 Operand，符合 **子树的值将保存在 Operand(v, t) 所代表的操作数中** 这个假设，由此可以看到，在这样的假设下生成的 IR 可以在遍历语法树的过程中传递起来并保证顺序的正确

## **4. Stmt: 语句**

### TO BE CONTINUE

## **5. 程序接口**
在本次实验中，你们需要实现 Analyzer 类，完成 `ir::Program get_ir_program(CompUnit*);` 接口，该接口接受一个源程序语法树的根节点 **Comp***，对其进行分析，返回分析结果 **ir::Program**

```C++
struct Analyzer {
    int tmp_cnt;
    vector<ir::Instruction*> g_init_inst;
    SymbolTable symbol_table;

    /**
     * @brief constructor
     */
    Analyzer();

    // analysis functions
    ir::Program get_ir_program(CompUnit*);

    // reject copy & assignment
    Analyzer(const Analyzer&) = delete;
    Analyzer& operator=(const Analyzer&) = delete;

    // analysis functions
    void analysisCompUnit(CompUnit*, ir::Program&);
    void analysisFuncDef(FuncDef*, ir::Function&);
    void analysisDecl(Decl*, vector<ir::Instruction*>&);
    void analysisConstDecl(ConstDecl*, vector<ir::Instruction*>&);
    void analysisBType(BType*, vector<ir::Instruction*>&);
    void analysisConstDef(ConstDef*, vector<ir::Instruction*>&);
    void analysisConstInitVal(ConstInitVal*, vector<ir::Instruction*>&);
    ...
};

```

