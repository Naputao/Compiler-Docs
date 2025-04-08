# CMake

## 🌟 **推荐方式 1：系统包管理器安装**

### 🐧 Ubuntu / Debian

```bash
sudo apt update
sudo apt install cmake
```

> 默认版本可能稍旧，但对一般项目足够用了。如果你需要最新版，请看后面的「推荐方式 2」。

------

### 🐧 Arch Linux / Manjaro

```bash
sudo pacman -S cmake
```

------

### 🐧 Fedora / RHEL / CentOS

```bash
sudo dnf install cmake
```

------

### 🐧 openSUSE

```bash
sudo zypper install cmake
```

------

## 🌟 **推荐方式 2：手动安装最新版 CMake（跨发行版通用）**

如果你想安装最新版本（比如 3.29.x）：

### ✅ 步骤如下：

1. 下载最新版：

```bash
wget https://github.com/Kitware/CMake/releases/latest/download/cmake-*-linux-x86_64.tar.gz
```

（可用 `curl -LO` 替代）

1. 解压：

```bash
tar -xzf cmake-*-linux-x86_64.tar.gz
```

1. 进入目录并添加到 PATH：

```bash
cd cmake-*-linux-x86_64
sudo mv cmake-* /opt/cmake
echo 'export PATH=/opt/cmake/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

1. 测试版本：

```bash
cmake --version
```