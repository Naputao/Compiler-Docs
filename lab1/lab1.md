# **实验一**

## **实验目标**
实验一将实现编译器前端的词法分析和语法分析部分，目标是分析输入的 **源文件** 得到一颗 **抽象语法树**

## **实验步骤**
从希冀上下载实验框架

    4.29 日对测试用例进行了更新

## **实验一标准输出**
这是一段最简单的 SysY 程序
```C++
int main() {
    return 3;
}
```
实验一将把他解析为一颗语法分析树，我们用 json 来输出语法树，标准如下：
```json
{
   "name" : "CompUnit",
   "subtree" : [
      {
         "name" : "FuncDef",
         "subtree" : [
            {
               "name" : "FuncType",
               "subtree" : [
                  {
                     "name" : "Terminal",
                     "type" : "INTTK",
                     "value" : "int"
                  }
               ]
            },
            {
               "name" : "Terminal",
               "type" : "IDENFR",
               "value" : "main"
            },
            {
               "name" : "Terminal",
               "type" : "LPARENT",
               "value" : "("
            },
            {
               "name" : "Terminal",
               "type" : "RPARENT",
               "value" : ")"
            },
            {
               "name" : "Block",
               "subtree" : [
                  {
                     "name" : "Terminal",
                     "type" : "LBRACE",
                     "value" : "{"
                  },
                  {
                     "name" : "BlockItem",
                     "subtree" : [
                        {
                           "name" : "Stmt",
                           "subtree" : [
                              {
                                 "name" : "Terminal",
                                 "type" : "RETURNTK",
                                 "value" : "return"
                              },
                              {
                                 "name" : "Exp",
                                 "subtree" : [
                                    {
                                       "name" : "AddExp",
                                       "subtree" : [
                                          {
                                             "name" : "MulExp",
                                             "subtree" : [
                                                {
                                                   "name" : "UnaryExp",
                                                   "subtree" : [
                                                      {
                                                         "name" : "PrimaryExp",
                                                         "subtree" : [
                                                            {
                                                               "name" : "Number",
                                                               "subtree" : [
                                                                  {
                                                                     "name" : "Terminal",
                                                                     "type" : "INTLTR",
                                                                     "value" : "3"
                                                                  }
                                                               ]
                                                            }
                                                         ]
                                                      }
                                                   ]
                                                }
                                             ]
                                          }
                                       ]
                                    }
                                 ]
                              },
                              {
                                 "name" : "Terminal",
                                 "type" : "SEMICN",
                                 "value" : ";"
                              }
                           ]
                        }
                     ]
                  },
                  {
                     "name" : "Terminal",
                     "type" : "RBRACE",
                     "value" : "}"
                  }
               ]
            }
         ]
      }
   ]
}

```