# **CMake**与**make**

一些网络资源

[Makefile基础](https://liaoxuefeng.com/books/makefile/makefile-basic/index.html)

[CMake 构建实例](https://www.runoob.com/cmake/cmake-build-demo.html)

## 🌟 一句话理解

- **make**：负责“执行编译”，是一个老牌的自动化构建工具。
- **Makefile**：是给 `make` 工具读的“说明书”，写清楚怎么编译、哪些文件依赖哪些。
- **CMake**：是一个更现代、更高级的“构建配置工具”，它能生成 `Makefile` 或其他构建系统的配置文件。

------

## 🛠️ make 和 Makefile 简介

### ✅ 作用：

`make` 会根据你写的 `Makefile`，自动决定哪些源文件需要重新编译，并调用编译器进行编译。

### 📄 Makefile 示例：

```make
main: main.o utils.o
	g++ -o main main.o utils.o

main.o: main.cpp
	g++ -c main.cpp

utils.o: utils.cpp utils.h
	g++ -c utils.cpp

clean:
	rm -f *.o main
```

### 🔄 说明：

- `main` 依赖于 `main.o` 和 `utils.o`
- 如果 `main.cpp` 改了，只会重新编译 `main.o`，提高效率
- `clean` 是自定义命令，用于清理中间文件

------

## 🧠 CMake 简介

### ✅ 作用：

CMake 是一个跨平台的构建系统生成工具。你只需要写一次 `CMakeLists.txt`，CMake 就能根据你的平台生成：

- Linux：`Makefile`
- Windows（MSVC）：Visual Studio 工程
- macOS：Xcode 工程
- 甚至 Ninja、CodeBlocks 工程等

### 📄 CMakeLists.txt 示例：

```cmake
cmake_minimum_required(VERSION 3.10)
project(MyApp)

set(CMAKE_CXX_STANDARD 17)

add_executable(MyApp main.cpp utils.cpp)
```

### 🚀 构建流程（Linux / Mac / WSL 中）：

```bash
mkdir build
cd build
cmake ..
make
```

### Windows 上（使用 Visual Studio）：

```powershell
cmake -G "Visual Studio 16 2019" ..
```

------

## 📌 总结对比：

| 特性     | make + Makefile        | CMake                  |
| -------- | ---------------------- | ---------------------- |
| 易用性   | 手动写依赖，稍麻烦     | 更现代，自动处理依赖   |
| 可移植性 | 不好，只适合 UNIX 系统 | 很好，支持多平台多 IDE |
| 学习曲线 | 简单                   | 稍复杂，但功能强大     |
| 推荐程度 | 🟡 初学者了解           | ✅ 项目开发首选         |



对于本实验给出的 `CMakeLists.txt`

```cmake
cmake_minimum_required(VERSION 3.10)
project(compiler)

# compile flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS   "-g")                     # 调试信息
set(CMAKE_CXX_FLAGS   "-Wall")                  # 开启所有警告
# debug flags
# add_definitions(-DDEBUG_DFA)
# add_definitions(-DDEBUG_SCANNER)
# add_definitions(-DDEBUG_PARSER)

# output settings
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)


# include
include_directories(./include)

# third party libs
add_library(jsoncpp ./src/third_party/jsoncpp/jsoncpp.cpp)

# --------------------- from lib ---------------------
# link libxx.a
# u should rename libxx-x86-win.a or libxx-x86-linux.a to libxx.a according to ur own platform
link_directories(./lib)
# --------------------- from lib ---------------------

# build library
# every src file directory should be compile into a lib

aux_source_directory(./src/front FRONT_SRC)
add_library(Front ${FRONT_SRC})
aux_source_directory(./src/backend BACKEND_SRC)
add_library(Backend ${BACKEND_SRC})

# 为了 debug 方便，你可以选择通过源文件来构建 IR 测评机，但是请以链接静态库文件的方式去跑分（为了防止你们修改测评机，在OJ上我们会采取此方式）
# --------------------- from src ---------------------
# aux_source_directory(./src/ir IR_SRC)
# add_library(IR ${IR_SRC})
# aux_source_directory(./src/tools TOOLS_SRC)
# add_library(Tools ${TOOLS_SRC})
# --------------------- from src ---------------------


# executable
add_executable(compiler main.cpp)

# link
# every lib should be linked with [compiler]
target_link_libraries(compiler Backend Tools Front IR jsoncpp)
```

这段 `CMakeLists.txt` 是一个典型的 CMake 项目的构建脚本，用于配置一个名为 **compiler** 的项目。它定义了编译选项、库的包含与链接、输出目录、以及源文件和库的构建方式。下面我逐一解释每个部分：

------

### 1. **基本设置**

```cmake
cmake_minimum_required(VERSION 3.10)
project(compiler)
```

- `cmake_minimum_required(VERSION 3.10)`：设置该 CMake 脚本需要的最低 CMake 版本为 3.10。这个版本支持现代的 CMake 特性。
- `project(compiler)`：定义项目的名称为 `compiler`。

------

### 2. **编译选项和调试信息**

```cmake
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS   "-g")                     # 调试信息
set(CMAKE_CXX_FLAGS   "-Wall")                  # 开启所有警告
```

- `set(CMAKE_CXX_STANDARD 14)`：指定 C++ 编译标准为 C++14。
- `set(CMAKE_CXX_FLAGS "-g")`：添加调试信息到编译选项中，生成调试符号。
- `set(CMAKE_CXX_FLAGS "-Wall")`：开启所有编译警告，帮助开发者检查潜在问题。

------

### 3. **调试选项（注释部分）**

```cmake
# debug flags
# add_definitions(-DDEBUG_DFA)
# add_definitions(-DDEBUG_SCANNER)
# add_definitions(-DDEBUG_PARSER)
```

- 这部分被注释掉了，通常是用于定义调试宏。`add_definitions(-DDEBUG_XXX)` 可以向编译器传递宏定义（如 `-DDEBUG_DFA`），这些宏在源代码中用于调试输出。

------

### 4. **输出设置**

```cmake
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)
```

- `set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)`：设置运行文件（可执行文件）的输出目录为项目根目录下的 `bin` 文件夹。
- `set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR}/bin)`：设置静态库文件的输出目录为 `bin` 文件夹。

------

### 5. **头文件目录**

```cmake
include_directories(./include)
```

- `include_directories(./include)`：将 `./include` 目录添加到编译时的头文件搜索路径中。这样，在源文件中引用头文件时，CMake 会去 `include` 文件夹寻找相关文件。

------

### 6. **第三方库**

```cmake
add_library(jsoncpp ./src/third_party/jsoncpp/jsoncpp.cpp)
```

- `add_library(jsoncpp ./src/third_party/jsoncpp/jsoncpp.cpp)`：将 `jsoncpp.cpp` 文件编译成一个名为 `jsoncpp` 的库。这个库来自于 `src/third_party/jsoncpp` 目录，通常是第三方依赖库。

------

### 7. **库文件链接目录**

```cmake
link_directories(./lib)
```

- `link_directories(./lib)`：指定一个目录（`./lib`）来搜索库文件。这是链接时的搜索路径，通常是一些外部库的 `.a` 或 `.so` 文件。

------

### 8. **源文件组织和库构建**

```cmake
aux_source_directory(./src/front FRONT_SRC)
add_library(Front ${FRONT_SRC})
aux_source_directory(./src/backend BACKEND_SRC)
add_library(Backend ${BACKEND_SRC})
```

- `aux_source_directory(./src/front FRONT_SRC)`：将 `./src/front` 目录下的所有源文件（`.cpp`）收集到变量 `FRONT_SRC` 中。
- `add_library(Front ${FRONT_SRC})`：将 `FRONT_SRC` 中的源文件编译成一个名为 `Front` 的库。
- 同样，`aux_source_directory(./src/backend BACKEND_SRC)` 和 `add_library(Backend ${BACKEND_SRC})` 会把 `./src/backend` 目录下的源文件编译成 `Backend` 库。

------

### 9. **静态库构建（注释部分）**

```cmake
# --------------------- from src ---------------------
# aux_source_directory(./src/ir IR_SRC)
# add_library(IR ${IR_SRC})
# aux_source_directory(./src/tools TOOLS_SRC)
# add_library(Tools ${TOOLS_SRC})
# --------------------- from src ---------------------
```

- 这部分被注释掉了，但它展示了如何构建其他库（如 `IR` 和 `Tools`）。如果需要，你可以取消注释并添加源文件来构建更多的库。

------

### 10. **可执行文件构建**

```cmake
add_executable(compiler main.cpp)
```

- `add_executable(compiler main.cpp)`：将 `main.cpp` 文件编译成一个名为 `compiler` 的可执行文件。

------

### 11. **库链接**

```cmake
target_link_libraries(compiler Backend Tools Front IR jsoncpp)
```

- `target_link_libraries(compiler Backend Tools Front IR jsoncpp)`：将 `compiler` 可执行文件与多个库进行链接，包括：
  - `Backend`
  - `Tools`（注释掉了）
  - `Front`
  - `IR`（注释掉了）
  - `jsoncpp`

这意味着在编译 `compiler` 时，它会链接这些库文件，确保运行时可以找到它们的符号。