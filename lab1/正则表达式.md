# Regex库

C++ 的 `<regex>` 库是 C++11 引入的，功能强大，用法和 Python、Perl 等语言类似。下面我来系统地讲一讲它的用法，配合示例代码，适合你查阅和参考。

------

## 🔧 头文件 & 命名空间

```cpp
#include <regex>
#include <string>
#include <iostream>
```

## 📌 常用类和函数

| 类/函数              | 说明                             |
| -------------------- | -------------------------------- |
| `std::regex`         | 表示正则表达式                   |
| `std::smatch`        | 用于存储字符串匹配结果（string） |
| `std::cmatch`        | 用于 C 字符串匹配                |
| `std::regex_match`   | 判断整个字符串是否匹配           |
| `std::regex_search`  | 判断字符串中是否存在匹配子串     |
| `std::regex_replace` | 替换匹配部分                     |

------

## ✅ 示例 1：regex_match（完全匹配）

```cpp
string s = "abc123";
regex r("[a-z]+\\d+");

if (regex_match(s, r)) {
    cout << "完全匹配！" << endl;
} else {
    cout << "不匹配" << endl;
}
```

------

## ✅ 示例 2：regex_search（部分匹配）

```cpp
string s = "hello 123 world";
regex r("\\d+");

smatch match;
if (regex_search(s, match, r)) {
    cout << "找到数字: " << match.str() << endl;
}
```

------

## ✅ 示例 3：regex_replace（替换）

```cpp
string s = "ID123 and ID456";
regex r("ID(\\d+)");
string result = regex_replace(s, r, "编号$1");

cout << result << endl;
// 输出：编号123 and 编号456
```

------

## ✅ 示例 4：提取所有匹配项

```cpp
string s = "apple=10, orange=20, banana=30";
regex r("(\\w+)=(\\d+)");
smatch match;

while (regex_search(s, match, r)) {
    cout << "水果: " << match[1] << ", 数量: " << match[2] << endl;
    s = match.suffix().str();  // 继续搜索剩下的字符串
}
```

------

## 📋 正则语法回顾（兼容 ECMAScript）

| 表达式  | 含义             |
| ------- | ---------------- |
| `.`     | 任意字符         |
| `\\d`   | 数字             |
| `\\w`   | 字母/数字/下划线 |
| `*`     | 0 次或多次       |
| `+`     | 1 次或多次       |
| `?`     | 0 次或 1 次      |
| `{n,m}` | n 到 m 次        |
| `()`    | 分组             |
| `       | `                |
| `^` `$` | 行首/行尾        |
| `\\`    | 转义字符         |

------

## 🧠 regex 标志位（可选）

可以控制匹配行为：

```cpp
regex r("abc", regex_constants::icase); // 忽略大小写
```

常见标志：

| 标志                          | 说明           |
| ----------------------------- | -------------- |
| `regex_constants::icase`      | 忽略大小写     |
| `regex_constants::ECMAScript` | 默认模式       |
| `regex_constants::basic`      | POSIX basic    |
| `regex_constants::extended`   | POSIX extended |
| `regex_constants::awk`        | awk 语法       |
| `regex_constants::grep`       | grep 语法      |
| `regex_constants::egrep`      | egrep 语法     |

------

## 🧨 注意事项

- C++ 字符串中的 `\` 需要写成 `\\`；
- 如果性能要求极高，可以考虑 RE2 或 Boost.Regex；
- `<regex>` 在某些平台上实现效率不是很高，但功能齐全。