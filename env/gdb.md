#  GDB（GNU 调试器）

## ✅ GDB 是干嘛的？

`gdb` 是 GNU 的调试器，用于调试 C / C++ 等语言编写的程序，支持：

- 设置断点（`break`）
- 单步执行（`next`, `step`）
- 查看变量、内存、寄存器
- 调试 core dump

------

## 🐧 各发行版 GDB 安装方式

### 📦 Ubuntu / Debian / Kali / WSL (Ubuntu)

```bash
sudo apt update
sudo apt install gdb
```

------

### 📦 Arch Linux / Manjaro

```bash
sudo pacman -S gdb
```

------

### 📦 Fedora / CentOS / RHEL

```bash
sudo dnf install gdb
```

------

### 📦 openSUSE

```bash
sudo zypper install gdb
```

------

## 🔧 编译支持调试的程序

编译时要加上 `-g` 参数：

```bash
g++ -g main.cpp -o main
```

然后就可以用 gdb 调试了：

```bash
gdb ./main
```

常用命令举例：

| 命令                | 功能                     |
| ------------------- | ------------------------ |
| `break main`        | 在 `main` 函数处设置断点 |
| `run`               | 启动程序                 |
| `next`              | 执行下一行，不进入函数   |
| `step`              | 执行下一行，进入函数     |
| `print x`           | 查看变量 `x` 的值        |
| `backtrace` 或 `bt` | 查看当前调用栈           |
| `quit`              | 退出 GDB                 |

------

## 💡 小贴士：带 TUI 图形界面的 GDB 模式

```bash
gdb -tui ./main
```

按 `Ctrl + X` 然后 `A`，可以切换源码视图，非常方便！

------

## ✅ 检查版本 & 安装成功验证

```bash
gdb --version
```

如果看到类似：

```bash
GNU gdb (Ubuntu 12.1-3ubuntu2) ...
```

说明装好了。