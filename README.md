# 重庆大学编译原理2022教改项目

## **实验方案**
本次实验将实现一个由 SysY (精简版 C 语言，来自 https://compiler.educg.net/) 翻译至 RISC-V 汇编的编译器，生成的汇编通过 GCC 的汇编器翻译至二进制，最终运行在模拟器 qemu-riscv 上

实验至少包含四个部分: 词法和语法分析、语义分析和中间代码生成、以及目标代码生成，每个部分都依赖前一个部分的结果，逐步构建一个完整编译器

**实验一**：词法分析和语法分析，将读取源文件中代码并进行分析，输出一颗语法树

**实验二**：接受一颗语法树，进行语义分析、中间代码生成，输出中间表示 IR (Intermediate Representation)

**实验三**：根据 IR 翻译成为汇编

**实验四(可选)**：IR 和汇编层面的优化
<br><br><br>

## **实验开始之前**
本次实验将从零开始，写一个完整的编译器，编译 SysY 语言至 risc-v 汇编，并在 qemu-riscv 上跑起来

在开始之前，请不要抱有畏惧心理，我们准备好的了详细的文档、代码框架和构建方案、自动化测试程序

还有几个小建议：
1. 在编写代码时，注意代码规范，避免出现低级但难以排查的错误甚至是奇奇怪怪的链接错误，请阅读 [C++ coding style](https://zh-google-styleguide.readthedocs.io/en/latest/google-cpp-styleguide/headers/) 和助教为你准备的 [如果不遵守可能会出现各种奇奇怪怪问题的编码小技巧](/src/docs/coding_guide.txt)
2. 在遇到 bug 时，请相信计算机一定不会出错，**一定是代码的问题**
3. 在需要查找资料来解决问题时，请至少使用 [Bing](https://cn.bing.com/) 而不是百度，尽量查阅 [Google](https://www.google.com), [wikipedia](http://en.wikipedia.org), [stackoverflow](http://stackoverflow.com) 等网站的资料，因为与编译原理相关的中文资料可能会非常少，英文资料相对丰富（以助教的经验来说 CSDN 不太能解决问题
4. 上网查资料并不能解决所有的问题，他们的回答甚至有可能时错的！正确的做法应当是阅读官方文档，官方手册包含了查找对象的所有信息，关于查找对象的一切问题都可以在官方手册中找到答案。如果你需要了解如何使用 GDB，你应该阅读[Debugging with GDB](https://sourceware.org/gdb/current/onlinedocs/gdb)，或者是你需要了解 riscv 的指令集定义、汇编规则，你应该到 [riscv 官网中的技术手册](https://riscv.org/technical/specifications/) 中寻找答案
5. 在向助教和同学提问之前，请学习 [提问的智慧](https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/main/README-zh_CN.md)，以更高效的解决问题