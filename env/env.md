# **实验环境介绍**

## **实验工具**
实验至少需要用到以下工具，请同学们自行安装并学习，在下面也有简单的使用说明，这个程度的说明只能保证基础的使用，如果出现不符合预期的情况，**请阅读文档**
1. [Git](https://git-scm.com/doc)
2. [CMake](https://www.bookstack.cn/read/CMake-Cookbook/README.md)   
3. [GNU Makefiles](https://www.gnu.org/software/make/manual/make.html) / [GCC](https://gcc.gnu.org/) / [GDB](https://sourceware.org/gdb/)


## **代码框架介绍**
### **获取代码**
```
从希冀实验题的附件中下载 
```
可以使用 docker 来避免配置环境的问题，但是仍需从希冀中下载相应实验的框架
```
docker使用

拉取镜像：
docker pull frankd35/demo:v3

挂载目录至 /coursegrader 并使用：
docker run -it -v {你的代码框架目录}:/coursegrader frankd35/demo:v3

在使用 docker 里面的 cmake 时会遇到一个问题，因为安装了交叉编译器以及 cmake 不知道怎么把 riscv 的交叉编译器配置成了默认编译器，所以编出来的可执行文件是 riscv 版的。要解决这个问题需要在 CMakeLists.txt 中指定 x86-linux 的编译器：
    set(CMAKE_C_COMPILER    "/usr/bin/x86_64-linux-gnu-gcc-7")
    set(CMAKE_CXX_COMPILER  "/usr/bin/x86_64-linux-gnu-g++-7")
```


因为我们希望以库的形式提供 IR 测评相关的函数实现，所以请在 /lib 下根据你使用的 linux 或 windows 平台将对应的库文件重命名为 libxx.a 才能通过编译


### **测评程序**
在测评时 你应该提交一个直接包含至少 /include /src 的压缩包
 
我们的测评程序会解压你的压缩包，并将 CMakeLists.txt 和 main.cpp 复制到同一目录下（会覆盖你的文件），并链接合适的 libxx.a，使用 /test/test.py [s1/s2/S] 来进行测评, 所以请严格按照实验指导书指定的接口来完成实验（最近简单的方式是不要修改 CMakeLists.txt 和 main.cpp
```
目录结构：
--- dir
    --- {你的压缩包解压出来的文件}
    --- CMakeLists.txt
    --- main.cpp
```

### **目录结构**
```
/bin		可执行文件 + 库文件

/build		构建项目的文件

/include	头文件

/src		源代码

/src/...	子模块: IR, frontend, backend, opt
            third_party: 第三方库, 目前使用了 jsoncpp 用于生成和读取 json

/lib        我们提供的库文件, 你需要根据你使用的 linux 或 windows 平台将对应的库文件重命名为 libIR.a 才能通过编译


/test       测试框架, 可以用于自测

/CMakeList.txt

/readme.txt	
```

### **编译**
```
首先进入 /build 若CMakeList修改后应执行 cmake 命令
1. cd /build
2. cmake .. （如果是在 windows 环境下第一次支持 cmake 命令，需要使用 'cmake -G "MinGW Makefiles" ..' 以构建 makefile）
如果一切正常没有报错 执行make命令
3. make
```

### **执行**
```
1. cd /bin
2. compiler <src_filename> [-step] -o <output_filename> [-O1]
    -step: 支持以下几种输入
        s0: 词法结果 token 串
        s1: 语法分析结果语法树, 以 json 格式输出
        s2: 语义分析结果, 以 IR 程序形式输出
        -S: RISC-v 汇编
```
### **测试**
```
1. cd /test
2. python [files]:
    build.py:   进入到 build 目录, 执行 cmake .. & make
    run.py: 运行可执行文件 compiler 编译所有测试用例, 打印 compiler 返回值和报错, 输出编译结果至 /test/output
        执行方法: python run.py [s0/s1/s2/S]
    score.py: 将 run.py 生成的编译结果与标准结果进行对比并打分
        执行方法: python score.py [s0/s1/s2/S]

    test.py 编译生成 compiler 可执行文件，执行并生成结果，最后对结果进行判断并打分，结果将出现在标准输出的最后一行
        执行方法: python test.py [s0/s1/s2/S]
```

## **Windows 环境准备**
在 Windows 下至少可以完成实验一和实验二的部分，实验三部分需要在 linux 运行 qemu-riscv 来完成

为了在 windows 下运行 CMake 及 Makefiles，同学们需要安装
> - [CMake](https://cmake.org/)
>  is an open-source, cross-platform family of tools designed to build, test and package software 
> - [Mingw](https://www.mingw-w64.org/)
> A native Windows port of the GNU Compiler Collection (GCC), with freely distributable import libraries and header files for building native Windows applications

在测试中我们还用到了 ```diff``` 工具，Windows 原生是不支持的，这个工具在安装了 Git 之后，在 {ur_path_to_git}/Git/usr/bin 中可以找到 diff.exe，所以我们需要将这个目录添加到 **环境变量 PATH** 下，才能正常使用测评功能
> 完成了以上步骤以后，在 cmd 或 powershell 里敲出 cmake, make, diff 命令时，响应不应该为 **xxx 不是内部或外部命令，也不是可运行的程序
或批处理文件。**

> 如果安装了 Mingw 后仍然不支持 make, 请检查 gcc 命令在 command 里面是否支持，如果支持的话说明你的 Mingw 是安装好了的，那么请你到 {ur_path_to_Mingw}/bin 下面找一下有没有一个叫 mingw64-make.exe 的程序（应该是有的），把他的名字改成 make.exe，重启 command 就可以支持 make 命令了

## **Mac 环境准备**
可以完成实验一和实验二的部分，实验三部分需要使用 qemu-riscv 来完成，建议使用我们提供的 docker
至少需要支持 cmake, git，GNU Makefiles, gcc, diff 等工具


## **Linux 环境准备**
部分 linux 环境不是原生支持 CMake 的，安装 CMake 即可，实验三部分需要使用 qemu-riscv 来完成，建议使用我们提供的 docker
