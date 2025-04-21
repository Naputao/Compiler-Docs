# 文法定义

对于实验一 只需要关注第一行的文法

对于实验二 在文法之外我们还提供了语法树中属性的参考定义, 但这不是强制要求的 ###FIXME 更详细的描述 

## Extended Backus-NaurForm
SysY 语言的文法采用扩展的 Backus 范式（EBNF，Extended Backus-NaurForm）表示，其中：

    符号[...]表示方括号内包含的为可选项；
    
    符号{...}表示花括号内包含的为可重复 0 次或多次的项；
    
    终结符或者是单引号括起的串，或者是 Ident、InstConst、floatConst 这样的记号

## 文法规则

CompUnit -> (Decl | FuncDef) [CompUnit]

Decl -> ConstDecl | VarDecl

ConstDecl -> 'const' BType ConstDef { ',' ConstDef } ';'

    ConstDecl.t

BType -> 'int' | 'float'

    BType.t 

ConstDef -> Ident { '[' ConstExp ']' } '=' ConstInitVal

    ConstDef.arr_name

ConstInitVal -> ConstExp | '{' [ ConstInitVal { ',' ConstInitVal } ] '}'

    ConstInitVal.v
    ConstInitVal.t

VarDecl -> BType VarDef { ',' VarDef } ';'

    VarDecl.t

VarDef -> Ident { '[' ConstExp ']' } [ '=' InitVal ]

    VarDef.arr_name

InitVal -> Exp | '{' [ InitVal { ',' InitVal } ] '}'

    InitVal.is_computable
    InitVal.v
    InitVal.t

FuncDef -> FuncType Ident '(' [FuncFParams] ')' Block

    FuncDef.t 
    FuncDef.n 
    
FuncType -> 'void' | 'int' | 'float'

FuncFParam -> BType Ident ['[' ']' { '[' Exp ']' }]

FuncFParams -> FuncFParam { ',' FuncFParam }

Block -> '{' { BlockItem } '}'

BlockItem -> Decl | Stmt

Stmt -> LVal '=' Exp ';' 
        | Block
        | 'if' '(' Cond ')' Stmt [ 'else' Stmt ]
        | 'while' '(' Cond ')' Stmt
        | 'break' ';' 
        | 'continue' ';' 
        | 'return' [Exp] ';' 
        | [Exp] ';'

Exp -> AddExp

    Exp.is_computable
    Exp.v
    Exp.t

Cond -> LOrExp

    Cond.is_computable
    Cond.v
    Cond.t

LVal -> Ident {'[' Exp ']'}

    LVal.is_computable
    LVal.v
    LVal.t
    LVal.i

Number -> IntConst | floatConst

PrimaryExp -> '(' Exp ')' | LVal | Number

    PrimaryExp.is_computable
    PrimaryExp.v
    PrimaryExp.t

UnaryExp -> PrimaryExp | Ident '(' [FuncRParams] ')' | UnaryOp UnaryExp

    UnaryExp.is_computable
    UnaryExp.v
    UnaryExp.t

UnaryOp -> '+' | '-' | '!'

FuncRParams -> Exp { ',' Exp }

MulExp -> UnaryExp { ('*' | '/' | '%') UnaryExp }

    MulExp.is_computable
    MulExp.v
    MulExp.t

AddExp -> MulExp { ('+' | '-') MulExp }

    AddExp.is_computable
    AddExp.v
    AddExp.t

RelExp -> AddExp { ('<' | '>' | '<=' | '>=') AddExp }

    RelExp.is_computable
    RelExp.v
    RelExp.t

EqExp -> RelExp { ('==' | '!=') RelExp }

    EqExp.is_computable
    EqExp.v
    EqExp.t

LAndExp -> EqExp [ '&&' LAndExp ]

    LAndExp.is_computable
    LAndExp.v 
    LAndExp.t 

LOrExp -> LAndExp [ '||' LOrExp ]

    LOrExp.is_computable 
    LOrExp.v 
    LOrExp.t
 
ConstExp -> AddExp

    ConstExp.is_computable: true 
    ConstExp.v
    ConstExp.t