# **实验二**
## **实验目标**
由实验一的 **抽象语法树** 经过语义分析和语法制导翻译，生成**中间表示 IR**

## **实验步骤**
从希冀上下载实验框架

compiler [src_filename] -s2 -o [output_filename]    将输出你的 IR 程序至 [output_filename]

> 用于观察自己的 IR 是否生成正确

compiler [src_filename] -e -o [output_filename]     将执行你的 IR 程序并输出其结果到 [output_filename]

> 包括源程序调用 putint 等函数输出到标准输出的内容 以及将程序 main 函数的返回值打印到最后一行，这个才是用于测试比对的

    5.12 日对测试用例和测评机进行了更新

[src_filename] 是 SysY 源程序，[output_filename] 是输出文件，根据参数不同而输出不同

## **测评方法：**
**在中间代码的测评中，考虑到相同的程序可以用不同的 IR 序列来表示，我们设计了 [IR 测评机](ir_executor.md) 来执行 IR 代码，通过测评机执行 IR 序列的结果判断 IR 序列是否正确**

如果要自测，我们对自测的输入文件命名有一点要求，请务必保证以下规则（main.cpp 告诉了你为啥会有这样的限制）：

使用 **compiler [filename.sy] -e -o [output_filename]** 命令读入一个后缀为 .sy 的源文件，如果该源文件需要输入的话（如调用了 getint getch 等库函数）请将输入放到 [filename.in] 中，


## **实验二标准输出**
这是一段简单的 SysY 程序
```C++
int main() {
    putint(100); putch(32); putch(97);
    return 3;
}
```

执行 -e 选项， [output_filename] 中输出如下

```
100 a
3
```

其中，第一行是程序本身想打印到标准输出的内容，最后一行是 main 函数的返回值，**值得注意的是 SysY 程序 main 函数返回值会以 uint8 的形式进行输出**，main.cpp 也保证了这一点

使用参数 -s2 可以调用 draw() 对 IR 程序进行输出，你可以通过它来查看你生成的 IR：
```
int main()
        0: call t0, putint(100)
        1: call t1, putch(32)
        2: call t2, putch(97)
        3: return 3
end

GVT:
```