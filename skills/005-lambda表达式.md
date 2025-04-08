# Lambda 表达式（匿名函数）

## ✅ 基本语法

```cpp
[ 捕获列表 ] ( 参数列表 ) -> 返回类型 {
    函数体
};
```

返回类型通常可省略（编译器自动推断）。

------

## 🔹 示例：最基础用法

```cpp
auto add = [](int a, int b) {
    return a + b;
};

std::cout << add(3, 4); // 输出：7
```

------

## 🔹 捕获列表（重点）

| 捕获方式    | 含义                        |
| ----------- | --------------------------- |
| `[=]`       | **按值**捕获所有外部变量    |
| `[&]`       | **按引用**捕获所有外部变量  |
| `[x]`       | **按值**捕获变量 `x`        |
| `[&x]`      | **按引用**捕获变量 `x`      |
| `[=, &x]`   | 默认按值，但 `x` 按引用     |
| `[this]`    | 捕获所在类的 `this` 指针    |
| `[=, this]` | 组合捕获（类成员 + 外部值） |

------

## 🔹 示例：捕获变量

```cpp
int a = 10, b = 5;

auto lam1 = [=]() { return a + b; };       // 捕获 a、b 的值副本
auto lam2 = [&]() { a++; b++; };           // 修改外部变量
auto lam3 = [a, &b]() { return a + (++b); };
```

------

## 🔹 与 STL 配合使用

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

std::ranges::for_each(v, [](int x) {
    std::cout << x * 2 << " ";
});
```

------

## 🔹 返回 Lambda（闭包）

```cpp
auto make_multiplier(int factor) {
    return [=](int x) { return x * factor; };
}

auto times3 = make_multiplier(3);
std::cout << times3(10); // 输出：30
```

------

## 🔹 带状态的 Lambda（可变）

```cpp
int counter = 0;
auto count_calls = [=]() mutable {
    return ++counter;  // 捕获副本但允许修改（mutable）
};
```

------

## 🔹 泛型 Lambda（C++14 起）

```cpp
auto printer = [](const auto& x) {
    std::cout << x << std::endl;
};

printer(42);
printer("hello");
```

------

## 🔹 Lambda 作为函数参数

```cpp
void apply_to_10(const std::function<int(int)>& f) {
    std::cout << f(10);
}

apply_to_10([](int x){ return x * x; }); // 输出：100
```

（注意：如非必要，`template` + auto 参数通常更高效）

------

## 🔹 Lambda 与类成员（`[this]`）

```cpp
class MyClass {
    int val = 42;
public:
    void print() {
        auto f = [this]() { std::cout << val; };
        f();
    }
};
```