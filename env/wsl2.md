# WSL2（Windows Subsystem for Linux 2）

## ✅ 安装 WSL2 的完整流程（Windows 10 & 11）

### 🌟 方法一：一键安装命令（推荐）

打开 **PowerShell（管理员）**，输入以下命令：

```powershell
wsl --install
```

它会自动安装：

- WSL 核心组件
- WSL2 版本
- 默认的 Linux 发行版（通常是 Ubuntu）

### 安装完成后：

- 重启电脑（有提示就重启）
- 首次启动会让你设置一个 Linux 用户名和密码
- 然后你就可以使用 Linux 环境了！

------

## 🔧 检查系统是否支持 WSL2

可以提前检查：

1. **Windows 版本**：
   - Windows 10 版本 2004 及以上（Build ≥ 19041）
   - 或 Windows 11 ✅
2. 打开 PowerShell，运行：

```powershell
wsl --list --online
```

如果这个命令能运行，就说明你的系统支持。

------

## 💡 想选择不同的 Linux 发行版？

你可以查看并安装其他版本，比如 Debian、Kali、Arch 等：

```powershell
wsl --list --online
```

然后安装，例如：

```powershell
wsl --install -d Debian
```

------

## 🧠 设置默认使用 WSL2（如果你已有 WSL1）

确保 WSL2 是默认版本：

```powershell
wsl --set-default-version 2
```

------

## 🚀 启动方式

安装好之后，可以从 **开始菜单** 找到：

- Ubuntu（或你安装的发行版名）
- 点击打开即可开始使用 WSL Linux 环境

------

## 🛠️ WSL 的一些常用命令

| 命令                         | 说明                                          |
| ---------------------------- | --------------------------------------------- |
| `wsl`                        | 启动默认 Linux                                |
| `wsl --list --verbose`       | 查看当前已安装的发行版及其版本（WSL1 / WSL2） |
| `wsl --set-version <名称> 2` | 将某个发行版切换到 WSL2                       |
| `wsl --shutdown`             | 关闭所有 WSL 实例                             |
| `wsl --unregister <名称>`    | 卸载发行版                                    |