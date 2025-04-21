
## **语法分析**
### **1. SysY 文法**
我们对 SysY 文法进行了一定的限制以减少难度，主要改变是同学们不需要支持二维以上的数组解析、不需要支持各种形式的浮点数字面量解析(不需要支持即我们在测试中不会出现这样的用例)，并对左递归文法做了处理。新的文法请参考 [文法定义](grammar.md)。请注意，实现必须以该文法为准
### **2. 抽象语法树**
抽象语法树(abstract syntax tree, AST) 是源代码语法结构的一种抽象表示。它以树状的形式表现编程语言的语法结构，树上的每个节点都表示源代码中的一种结构

我们知道文法中的一个 **产生式** 可以化为树的形式，如 ```FuncDef -> FuncType Ident '(' [FuncFParams] ')' Block``` 可以展开为以 **FuncDef** 为父节点，```FuncType``` ```Ident``` ```'('``` ```[FuncFParams]``` ```')'``` ```Block``` 为从左至右子节点的一颗多叉树

为了之后语义分析的实现方便，我们为每一个非终结符定义一个类，以便不同的树节点可以拥有他们自己的成员变量，他们拥有共同的基类 **AstNode**，定义在 [abstract_syntax_tree.h](/src/include/front/abstract_syntax_tree.h) 中
```C++
struct AstNode{
    NodeType type;  // the node type
    AstNode* parent;    // the parent node
    vector<AstNode*> children;     // children of node

    /**
     * @brief Get the json output object
     * @param root: a Json::Value buffer, should be initialized before calling this function
     */
    void get_json_output(Json::Value& root) const;
}

struct CompUnit: AstNode {
struct Decl: AstNode{
struct FuncDef: AstNode{
struct ConstDecl: AstNode {
...
```
其中 **NodeType** 代表了树节点的类型，每个非终结符有自己的 NodeType，所有的终结符认为式 Terminal 类型，NodeType 枚举类定义在[abstract_syntax_tree.h](/src/include/front/abstract_syntax_tree.h) 中
```C++
enum class NodeType {
    TERMINAL,       // terminal lexical unit
    COMPUINT,
    DECL,
    FUNCDEF,
    ...
}
```
```void get_json_output(Json::Value& root) const;``` 可以实现语法树的输出，我们已经提供了实现，**请不要改动它**，除非你能保证改动后输出仍与我们提供的标准输出一致

### **3. Parser**
解析器(Parser) 一般是指指把某种格式的文本（字符串）转换成某种数据结构的程序，在我们的语法分析过程中，Parser 接收 Token 串，转化为 AST，它被定义在 [syntax.h](/src/include/front/syntax.h)

```C++
struct Parser {
    uint32_t index; // current token index
    const std::vector<Token>& token_stream;
    
    /**
     * @brief creat the abstract syntax tree
     * @return the root of abstract syntax tree
     */
    CompUnit* get_abstract_syntax_tree();
}
```
其中 **uint32_t index** 记录了已分析 Token 串的位置，**vector<Token>& token_stream** 是输入的 Token 串，```CompUnit* get_abstract_syntax_tree();``` 是**提供给外部的接口**，返回一颗分析完成的语法树

<table><tr><td bgcolor=MistyRose><strong>TODO:<strong> 实现 CompUnit* get_abstract_syntax_tree(); 函数</td></tr></table>


### **4. 递归下降法实现**
语法分析有很多种方式，在此我们介绍用递归下降法实现 LL(k) 分析的方法，但不要求同学们必须使用该方法，实现 **get_abstract_syntax_tree** 接口即可

在递归下降法中，我们首先要解决 **左递归** 问题：在某些文法，特别是表达式相关的文法中存在形如 ```AddExp -> MulExp | AddExp ('+' | '−') MulExp``` 的产生式，我们需要进行左递归的消除才能使用递归下降法，消除后产生式形为
```
AddExp -> MulExp [ ('+' | '-') AddExp ]
```
但是这个产生式在语义分析中并不好用，同学们可以思考一下为什么不对 (**提示: 运算顺序**)

于是经过进一步的变换，这个表达式可以变成我们实验规定的文法的样子，并且这三个产生式所产生的语言是等价的
```
AddExp -> MulExp { ('+' | '-') MulExp }
```

实现递归下降法，我们需要为每个非终结符节点创建一个 parse 函数
```C++
struct Parser {
    /**
     * @brief recursive descent functions for non-terminals
     * @param root: current parsing non-terminal
     * @return true: 为了程序通用性 对 [] 包括起来的非终结符我们一样会调用这个递归下降函数, bool 返回值用来判断是否为空
     */
    bool parseCompUint(CompUnit* root);
    bool parseDecl(Decl* root);
    bool parseConstDecl(ConstDecl* root);
    bool parseBType(BType* root);
    bool parseConstDef(ConstDef* root);
    ...
}
```

在 parse 函数中，我们根据下一个需要处理的 token 类型和该节点不同产生式的 first 集来选择处理哪一个产生式；在处理产生式时，应该按顺序从左到右依次处理，对非终结符调用其相应的 parse 函数，并将得到的语法树节点加入该节点的子节点中；对终结符，我们使用一个特殊的 parse 函数 ```Term* parseTerm(AstNode* parent, TokenType expected);``` 来处理，其功能是
1. 判断当前 index 所指的 Token 是否为产生式所要求的 Token 类型，如果不是则发生了错误，程序运行结果则不可预计
2. 如果是符合预期的 Token 类型
   1. a. 则 new 一个 Term 节点并将 Token 内容拷贝到节点中
   2. 将该节点加入 parent 的子节点
   3. Parser 的 index++

```C++
struct Term: AstNode {
    Token token;

    /**
     * @brief constructor
     */
    Term(Token t, AstNode* p = nullptr);
};

struct Parser {
    /**
     * @brief parse a specific type terminal token
     * @param expected: the specific type
     * @return Term* 
     */
    Term* parseTerm(AstNode* parent, TokenType expected);
}
```
> TIPS：这里建议大家对任何不符合预期的地方直接 assert(0)，因为我们保证提供的源程序符合文法，所以如果不符合预期一定是你自己写错了

对于 parse 函数的三种最基本的操作，我们提供了宏和使用方法供同学们参考
1. 根据下一个 Token 类型的类型选择处理的产生式(一般只看下一个 Token 就可以选择产生式，少数情况下多个产生式的 first 集有交集时，应多向后看几个 Token)
   ```C++
    #define CUR_TOKEN_IS(tk_type) (token_stream[index].type == TokenType::tk_type)

   if (CUR_TOKEN_IS(tk_type1)) {
        // code
   }
   else if (CUR_TOKEN_IS(tk_type2)) {
        // code
   }
   ...
   ```
2. 如果是非终结符，则调用其 pasrse 函数，并将其挂在 root 节点上
    ```C++
    #define PARSE(name, type) auto name = new type(root); assert(parse##type(name)); root->children.push_back(name); 

    PASER(exp_node, Exp);    // create a Exp node: exp_node, parse it, and add it to root.children
    ```
3. 如果是终结符，则调用 pasrseTerm 函数，并将其挂在 root 节点上
    ```C++
    #define PARSE_TOKEN(tk_type) root->children.push_back(parseTerm(root, TokenType::tk_type))

    PARSE_TOKEN(CONSTTK);    // parse root's first child as Exp, and add it to root.children
    ```

我们还为大家准备了用于 debug 的 log 函数，只需要在每个 parse 函数的头部加上它，就可以监视到你的解析程序的执行过程
```C++
void Parser::log(AstNode* node){
        std::cout << "in parse" << toString(node->type) << ", cur_token_type::" << toString(token_stream[index].type) << ", token_val::" << token_stream[index].value << '\n';
}
```

我们仍然以 ```FuncDef -> FuncType Ident '(' [FuncFParams] ')' Block``` 为例，展示 parseFuncDef 函数的实现
```C++
// FuncDef -> FuncType Ident '(' [FuncFParams] ')' Block
bool Parser::parseFuncDef(FuncDef* root) {
    log(root);

    PARSE(functype, FuncType);
    PARSE_TOKEN(IDENFR);
    PARSE_TOKEN(LPARENT);
    
    // no [FuncFParams], FuncType Ident '(' ')' Block
    if(CUR_TOKEN_IS(RPARENT)) {
        PARSE_TOKEN(RPARENT);
    }
    // FuncType Ident '(' FuncFParams ')' Block
    else {
        PARSE(node, FuncFParams);
        PARSE_TOKEN(RPARENT);
    }

    PARSE(block, Block);
    return true;
}
```

看到这里，你应该可以自己用递归下降法实现语法分析程序了，请不要忘记最终提供的接口是 **get_abstract_syntax_tree**

