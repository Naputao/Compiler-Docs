import json
import os
import re
import subprocess

# 1. 设置章节文件夹的顺序
chapters = ['env', 'lab1', 'lab2', 'lab3', 'lab4', 'q&a', 'skills']

with open("order.json", 'r',encoding='utf-8') as file:
    dir_order = json.load(file)

print(dir_order)
chapters_show = ['环境配置', '实验一', '实验二', '实验三', '实验四', 'q&a', '小技巧']
output_dir = './build'
os.makedirs(output_dir, exist_ok=True)

def increase_header_level(match):
    # 获取当前标题的 # 数量
    header_level = len(match.group(1))
    # 将 # 数量增加 1
    return '#' * (header_level + 2) + match.group(2)

combined_file = os.path.join(output_dir, 'combined.md')
with open(combined_file, 'w', encoding='utf-8') as outfile:

    # 3. 遍历每个章节目录
    for idx, chapter in enumerate(chapters):
        chapter_title = f"## {chapters_show[idx]}\n\n"
        outfile.write(chapter_title)

        chapter_path = os.path.join(os.getcwd(), chapter)
        print(chapter_path)
        if not os.path.isdir(chapter_path):
            print(f"[跳过] 未找到目录：{chapter}")
            continue

        md_files = [os.path.join(chapter_path, d) for d in dir_order[chapter]]

        print(md_files)
        for md_file in md_files:
            with open(md_file, encoding='utf-8') as f:
                outfile.write(re.sub(r'^(#+)(\s.*)', increase_header_level, f.read(), flags=re.MULTILINE))
                outfile.write('\n\n')

import re

# 读取 Markdown 内容
with open(combined_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 删除普通链接 [text](url) => text，跳过图片 ![alt](url)
modified = re.sub(r'(?<!\!)\[(.*?)\]\(.*?\)', r'\1', content)

# 保存修改结果
with open(combined_file, 'w', encoding='utf-8') as f:
    f.write(modified)

print("✅ 所有链接已删除，仅保留链接文本。")

import os
import shutil

# 项目的根目录
target_dir = os.path.join(os.getcwd(), 'build', 'assets')

# 创建目标文件夹（如果不存在）
os.makedirs(target_dir, exist_ok=True)

# 遍历所有目录
for dirpath, dirnames, filenames in os.walk(os.getcwd()):
    if os.path.basename(dirpath) == 'assets':
        for filename in os.listdir(dirpath):
            src_file = os.path.join(dirpath, filename)
            if os.path.isfile(src_file):
                dst_file = os.path.join(target_dir, filename)

                # 如果目标文件已存在，可以选择覆盖、跳过或重命名
                if os.path.exists(dst_file):
                    print(f"跳过已存在的文件: {dst_file}")
                    continue

                shutil.move(src_file, dst_file)
                print(f"移动: {src_file} -> {dst_file}")


import re

def slugify(text):
    # 将标题转换为 GitHub 风格的链接（可进一步增强兼容性）
    return re.sub(r'[^\w\- ]', '', text).strip().lower().replace(' ', '-')

def generate_toc(markdown_content):
    lines = markdown_content.splitlines()
    toc_lines = ["## 目录\n"]

    in_code_block = False

    for line in lines:
        # 检测代码块开始/结束（支持 ``` 或 ~~~）
        if re.match(r'^(```|~~~)', line.strip()):
            in_code_block = not in_code_block
            continue

        # 如果在代码块中，跳过这一行
        if in_code_block:
            continue

        # 匹配 Markdown 标题
        match = re.match(r'^(#{1,3})\s+(.*)', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            anchor = slugify(title)
            indent = '  ' * (level - 2)
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
            print(f"{indent}- [{title}](#{anchor})")

    return '\n'.join(toc_lines)

# 示例读取文件
with open(combined_file, 'r', encoding='utf-8') as f:
    content = f.read()

toc = generate_toc(content)

print("目录已生成")


guide_file = os.path.join(output_dir, 'guidebook.md')
with open(guide_file, 'w', encoding='utf-8') as outfile:
    if os.path.exists('README.md'):
        with open('README.md', encoding='utf-8') as f:
            outfile.write(f.read())
            outfile.write("\n\n")
    outfile.write(toc)
    outfile.write("\n\n")
    with open(combined_file, encoding='utf-8') as f:
        outfile.write(f.read())