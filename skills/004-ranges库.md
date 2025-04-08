# ranges库

## ✅ `std::views` 常用函数表格（惰性视图）

| 函数名                | 功能说明                        |
| --------------------- | ------------------------------- |
| `views::filter`       | 保留满足条件的元素              |
| `views::transform`    | 映射函数到每个元素              |
| `views::take(n)`      | 取前 n 个元素                   |
| `views::drop(n)`      | 跳过前 n 个元素                 |
| `views::reverse`      | 反转元素顺序                    |
| `views::iota(a, b)`   | 生成范围 [a, b) 的整数流        |
| `views::repeat(x, n)` | 重复值 x，n 次（需配合 `take`） |
| `views::chunk(n)`     | 每 n 个元素一组                 |
| `views::slide(n)`     | 滑动窗口（相邻组重叠）          |
| `views::join`         | 扁平化嵌套 range                |
| `views::split(delim)` | 按分隔符拆分 range（如字符串）  |
| `views::enumerate`    | 添加索引                        |

### ✅ `std::ranges::algorithm` 常用函数表格

| 函数名                | 功能说明                         | 示例                                            |
| --------------------- | -------------------------------- | ----------------------------------------------- |
| `ranges::sort`        | 对 range 排序（默认升序）        | `std::ranges::sort(v);`                         |
| `ranges::find`        | 查找指定值，返回迭代器           | `auto it = std::ranges::find(v, 3);`            |
| `ranges::count`       | 统计值出现次数                   | `int n = std::ranges::count(v, 1);`             |
| `ranges::copy`        | 拷贝范围到目标                   | `std::ranges::copy(v, out.begin());`            |
| `ranges::equal`       | 判断两个 range 是否相等          | `std::ranges::equal(v1, v2);`                   |
| `ranges::max_element` | 查找最大值迭代器                 | `auto it = std::ranges::max_element(v);`        |
| `ranges::min_element` | 查找最小值迭代器                 | `auto it = std::ranges::min_element(v);`        |
| `ranges::for_each`    | 遍历所有元素并执行函数           | `std::ranges::for_each(v, [](int& x){ x++; });` |
| `ranges::remove_if`   | 符合条件的元素                   | `auto it = std::ranges::remove_if(v, pred);`    |
| `ranges::unique`      | 去除相邻重复元素，将重复元素后移 | `auto it = std::ranges::unique(v);  `           |
| `ranges::any_of`      | 是否存在满足条件的元素           | `std::ranges::any_of(v, pred);`                 |
| `ranges::all_of`      | 所有元素是否都满足条件           | `std::ranges::all_of(v, pred);`                 |
| `ranges::none_of`     | 是否没有任何元素满足条件         | `std::ranges::none_of(v, pred);`                |

## 🔄 常用 `views` 操作及示例（懒执行）

### 1. `views::filter` – 过滤元素

**功能**：保留满足条件的元素。

```cpp
#include <ranges>
#include <vector>
#include <iostream>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    auto evens = v | std::views::filter([](int x) { return x % 2 == 0; });

    for (int x : evens)
        std::cout << x << " "; // 输出：2 4
}
```

------

### 2. `views::transform` – 转换元素

**功能**：对每个元素应用函数。

```cpp
auto squares = v | std::views::transform([](int x) { return x * x; });
```

------

### 3. `views::take(n)` – 取前 n 个元素

```cpp
auto first3 = v | std::views::take(3);
```

------

### 4. `views::drop(n)` – 跳过前 n 个元素

```cpp
auto after2 = v | std::views::drop(2);
```

------

### 5. `views::reverse` – 反转序列

```cpp
auto reversed = v | std::views::reverse;
```

------

### 6. `views::iota(start, end)` – 生成连续整数

```cpp
auto nums = std::views::iota(1, 6); // [1, 2, 3, 4, 5]
```

------

### 7. `views::repeat(value, n)` – 重复某个值 n 次

```cpp
auto fives = std::views::repeat(5) | std::views::take(3); // [5, 5, 5]
```

------

### 8. `views::chunk(n)` – 每 n 个元素分组（滑动窗口）

```cpp
std::vector v = {1,2,3,4,5,6};

for (auto group : v | std::views::chunk(2)) {
    for (auto x : group) std::cout << x << " ";
    std::cout << "| ";
}
// 输出：1 2 | 3 4 | 5 6 |
```

------

### 9. `views::slide(n)` – 滑动窗口（每次滑动一个元素）

```cpp
for (auto window : v | std::views::slide(3)) {
    for (auto x : window) std::cout << x << " ";
    std::cout << "| ";
}
// 输出：1 2 3 | 2 3 4 | 3 4 5 | 4 5 6 |
```

（`views::slide` 需要较新标准库，比如 GCC 13+）

------

### 10. `views::join` – 扁平化嵌套范围

```cpp
std::vector<std::vector<int>> vv = {{1,2}, {3,4}, {5}};

auto flat = vv | std::views::join;

for (int x : flat)
    std::cout << x << " "; // 输出：1 2 3 4 5
```

------

### ✅ 示例组合

```cpp
auto result = std::views::iota(1)
            | std::views::filter([](int x){ return x % 2 != 0; })  // 奇数
            | std::views::transform([](int x){ return x * x; })    // 平方
            | std::views::take(5);                                 // 取前5个

for (int x : result)
    std::cout << x << " "; // 输出：1 9 25 49 81
```

下面是 **C++20 `ranges::algorithm` 中最常用的函数列表**，这些是对传统 STL 算法的升级版，**支持直接传入 range（如 vector、list、view）而非迭代器对**，更简洁安全。

------

## 🔄 常用 `ranges::algorithm` 函数及示例

### 1. `std::ranges::sort` – 排序

和 `std::sort` 不同，无需手动指定迭代器。

```cpp
#include <ranges>
#include <vector>
#include <algorithm>

std::vector<int> v = {5, 3, 1, 4};
std::ranges::sort(v); // 自动使用 v.begin() 和 v.end()
```

------

### 2. `std::ranges::find` – 查找值

```cpp
auto it = std::ranges::find(v, 3);
if (it != v.end()) std::cout << "Found!";
```

------

### 3. `std::ranges::count` – 统计值出现次数

```cpp
int cnt = std::ranges::count(v, 4);
```

------

### 4. `std::ranges::copy` – 拷贝范围到另一个容器

```cpp
std::vector<int> dst(v.size());
std::ranges::copy(v, dst.begin());
```

------

### 5. `std::ranges::equal` – 判断两个范围是否相等

```cpp
std::vector<int> a = {1,2,3}, b = {1,2,3};
bool same = std::ranges::equal(a, b);
```

------

### 6. `std::ranges::max_element / min_element`

```cpp
auto max_it = std::ranges::max_element(v);
```

------

### 7. `std::ranges::unique` – 去重（相邻重复）

```cpp
std::vector<int> v = {1, 1, 2, 2, 3};
auto [first, last] = std::ranges::unique(v); // 返回去重后的范围
v.erase(first, last); // 去除多余元素
```

------

### 8. `std::ranges::remove_if` – 条件删除

配合 `erase` 使用：

```cpp
auto is_even = [](int x) { return x % 2 == 0; };
auto [first, last] = std::ranges::remove_if(v, is_even);
v.erase(first, last);
```

------

### 9. `std::ranges::for_each` – 遍历并执行函数

```cpp
std::ranges::for_each(v, [](int& x){ x *= 2; });
```

------

### 10. `std::ranges::any_of / all_of / none_of` – 条件判断

```cpp
std::ranges::any_of(v, [](int x){ return x > 5; });
std::ranges::all_of(v, [](int x){ return x >= 0; });
```