# store、load和getptr生成汇编

在编译器中实现数组访问的内存寻址时，我采用了不同的策略来处理一维和多维数组：

## 一维数组的简单寻址

对于一维数组（如`int a[3] = {1,2,3}`），我在符号表中只记录：

- 数组名称
- 数组基地址相对于栈指针(sp)的偏移量

访问格式：`table = { (a, offset) }`

元素访问计算公式：`地址 = sp + offset + index * 4`

## 多维数组的复合寻址

对于多维数组（如`int b[3][3]`），访问过程更复杂：

1. 首先需要获取子数组的基址（如`b[2]`的基址）
2. 将这个基址存入中间变量（如变量`x`）
3. 然后通过这个中间变量访问最终元素（如`b[2][2]`）

## 寻址冲突问题

这里出现了冲突：

- 对于普通变量，使用：`sp + offset + index * 4`
- 对于存储指针的变量，需要使用：`sp + x.val + index * 4`

由于变量`x`可能存储的是指针值或普通值，系统无法自动区分应该使用哪种寻址方式。

这两者就出现了冲突，因为x.val不一定是一个指向地址的指针，有可能就是数组本身的值（例如`b[2]`）。所以用了一个set来记录哪些值是存放指针的。

```cpp
// 记录哪些变量存的是一个指针
std::unordered_set<std::string> val_is_pointer;
```

根据存放的内容到底是不是一个指向地址的指针，选择对应的计算式：

$offset + index * 4 + sp$ or $x.val+index*4+sp$

代码实现：

```cpp
// 把des寄存器的内容放到内存中
if (val_is_pointer.find(op1.name) != val_is_pointer.end()) {
    // 把指针指向的地址取出来
    auto op1_reg{getRs1(op1)};
    load_operand_in_reg(op1, op1_reg, func_svm);
    auto arr_addr_reg{rv::rvREG::T4};
    fout << "\taddi\t" << toString(arr_addr_reg) << ", "
        << toString(op1_reg) << ", " << std::stoi(op2.name) * 4
        << "\n";
    fout << "\tsw\t" << rv::toString(des_reg) << ", 0("
        << toString(arr_addr_reg) << ")\n";
} else {
    fout << "\tsw\t" << rv::toString(des_reg) << ", "
        << std::stoi(op2.name) * 4 + func_svm.find_operand(op1)
        << "(sp)" << "\n";
}
```

