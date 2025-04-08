# GCC（GNU 编译器）

## 🐧 1. **Ubuntu / Debian**

### 🔧 安装命令：

```bash
sudo apt update
sudo apt install build-essential
```

这会安装：

- `gcc`、`g++`
- `make`
- 常见头文件和工具链

### ✅ 检查版本：

```bash
gcc --version
g++ --version
```

### 🛠️ 多版本管理（如 gcc-10、gcc-11）：

```bash
sudo apt install gcc-10 g++-10
sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 100
sudo update-alternatives --config gcc
```

------

## 🐧 2. **Arch Linux / Manjaro**

### 🔧 安装命令：

```bash
sudo pacman -Syu base-devel
```

这会装上：

- `gcc`、`g++`
- `make`、`binutils`、其他开发工具

可单独装 GCC：

```bash
sudo pacman -S gcc
```

------

## 🐧 3. **Fedora / RHEL / CentOS**

### 🔧 安装命令：

```bash
sudo dnf groupinstall "Development Tools"
```

或者单独安装：

```bash
sudo dnf install gcc gcc-c++
```

------

## 🐧 4. **openSUSE**

### 🔧 安装命令：

```bash
sudo zypper install -t pattern devel_C_C++
```

或单独安装：

```bash
sudo zypper install gcc gcc-c++
```

------

## 🐧 5. **Kali Linux（基于 Debian）**

```bash
sudo apt update
sudo apt install build-essential
```

和 Ubuntu 方法一样。

------

## ✅ 共通检查和调试

```bash
which gcc
gcc --version
echo $PATH
```

------

## 🧠 补充：你还可以装 Clang 一起用：

- Ubuntu/Debian: `sudo apt install clang`
- Arch: `sudo pacman -S clang`
- Fedora: `sudo dnf install clang`
- openSUSE: `sudo zypper install clang`