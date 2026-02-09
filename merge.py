import os
import re

SEP = "\\"
# 定义 markdown 文件路径
prefixPath = "source" + SEP + "_posts"
# folderName = "2022Spring-软件工程与计算II"
# folderName = "2022Spring-互联网计算"
# folderName = "2022Spring-数据库系统概论"
folderName = "2022Fall-计算机与操作系统"

def merge_articles():
    # 获取当前目录路径
    current_dir = prefixPath + SEP + folderName

    file_order = [file for file in os.listdir(current_dir) if file.endswith(".md")]
    file_order.sort()

    # 创建新的Markdown文件用于合并文章
    merged_file_path = os.path.join(current_dir, folderName + ".md")
    with open(merged_file_path, "w", encoding="utf-8") as merged_file:
        for file in file_order:
            # 在每篇文章开头添加一级标题，标题内容为文件名
            file_path = os.path.join(current_dir, file)
            with open(file_path, "r", encoding="utf-8") as article_file:
                article_content = article_file.read()

                # 删除开头的YAML配置项
                article_content = re.sub(r'^---\n(.*\n)*---\n', '', article_content, flags=re.MULTILINE)

                merged_file.write("# " + os.path.splitext(file)[0] + "\n\n")
                merged_file.write(article_content + "\n\n")

    print("Successfully merged!")

# 调用合并函数
merge_articles()
