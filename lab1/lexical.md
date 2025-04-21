
## **词法分析**
词法分析的目的是读入外部的字符流（源程序）对其进行扫描，把它们组成有意义的词素序列，对于每个词素，词法分析器都会产生词法单元(**Token**) 作为输出
### **1. Token**
Token 的定义在 [token.h](/src/include/front/token.h) 中，同时 Token 类型的枚举类 **TokenType** 也定义在其中  
```C++
struct Token {
    TokenType type;
    string value;
};

enum class TokenType{
    IDENFR,         // identifier	
    INTLTR,		    // int literal
    FLOATLTR,		// float literal
    CONSTTK,		// const
    VOIDTK,		    // void
    ... 
}
```
其中 **string** value 是 Token 所代表的字符串， **TokenType** type 是指 Token 的类型

### **2. DFA**
在词法分析中，我们使用确定有限状态自动机 (deterministic finite automaton, DFA) 来进行分词，对于一个给定的属于该自动机的状态和一个属于该自动机字母表 Σ 的字符，它都能根据事先给定的 **转移函数** 转移到下一个状态，某些转移函数会进行输出

我们需要为词法分析设计这样一个 DFA：它可以接收输入字符，进行状态改变，并在某些转移过程中输出累计接受到的字符所组成的字符串

该 DFA 中应存在五种状态，我们用枚举类 **State** 来表示
```C++
enum class State {
    Empty,              // space, \n, \r ...
    Ident,              // a keyword or identifier, like 'int' 'a0' 'else' ...
    IntLiteral,         // int literal, like '1' '1900', only in decimal
    FloatLiteral,       // float literal, like '0.1'
    op                  // operators and '{', '[', '(', ',' ...
};
```


我们将 DFA 及其行为的抽象为类和类方法，定义在 [lexical.h](/src/include/front/lexical.h) 中
```C++
struct DFA {
    /**
     * @brief take a char as input, change state to next state, and output a Token if necessary
     * @param[in] input: the input character
     * @param[out] buf: the output Token buffer
     * @return  return true if a Token is produced, the buf is valid then
     */
    bool next(char input, Token& buf);

    /**
     * @brief reset the DFA state to begin
     */
    void reset();

private:
    State cur_state;    // record current state of the DFA
    string cur_str;    // record input characters
};

```
其中 **State** cur_state 记录 DFA 当前的状态，**string** cur_str 记录 DFA 已经接受的字符串

每次字符输入都应调用 ```bool next(char input, Token& buf);``` 该函数是实现 DFA 的核心，即 **转移函数** ，其根据自身当前状态和输入来决定转移后的状态，如果产生 Token 则返回 true


<table><tr><td bgcolor=MistyRose><strong>TODO:<strong> 实现 DFA 中的 bool next(char input, Token& buf) 函数和 void reset(); 函数</td></tr></table>


### **3. Scanner**
Scanner 是扫描器，其职责是将字符串输入转化为 Token 串，词法分析实际上就是实现一个 Scanner

Scanner 的定义在 [lexical.h](/src/include/front/lexical.h) 中

```C++
struct Scanner {
    /**
     * @brief constructor
     * @param[in] filename: the input file  
     */
    Scanner(std::string filename); 

    /**
     * @brief run the scanner, analysis the input file and result a token stream
     * @return std::vector<Token>: the result token stream
     */
    std::vector<Token> run();

private:
    std::ifstream fin;  // the input file
};

```
其中 **std::ifstream** fin 是源文件打开得到的文件流

```std::vector<Token> run();``` 将执行分析过程，从文件流中读取字符，实例化一个 DFA 对象来获取 Token，但是我们的 DFA 只能识别代码部分，源文件中的注释输入 DFA 后并不能被正确的处理，我们需要在使用 DFA 接受字符串前对字符串进行预处理，所以 run() 的伪代码如下：
```C++
vector<Token> ret;
Token tk;
DFA dfa;
string s = preproccess(fin);    // delete comments
for(auto c: s) {
        if(dfa.next(c, tk)){
            ret.push_back(tk);
        }
}
```
<table><tr><td bgcolor=MistyRose><strong>TODO:<strong> 实现 Scanner 的 std::vector<Token> run() 函数</td></tr></table>

我们用一段最简单的 SysY 程序来展示词法分析的结果
```C++
int main() {
    return 3;
}
```

结果如下

| TokenType      | Value |
| ----------- | ----------- |
| INTTK | int |
|IDENFR	|main |
|LPARENT|	(|
|RPARENT|	)|
|LBRACE|	{|
|RETURNTK	|return|
|INTLTR|	3|
|SEMICN|	;|
|RBRACE|	}|

<table><tr><td bgcolor=yellow><strong> 词法分析部分到此结束 <td></tr></table>
