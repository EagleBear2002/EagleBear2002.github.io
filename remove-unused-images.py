import os
import re
from urllib.parse import unquote

# 定义正则表达式模式
pattern = r'!\[.*?\]\((.*?)\)|<img[^>]+src=["\'](.*?)["\']'

root_path = os.path.join('.', '_posts')

# 存储所有图片路径的集合
image_paths = set()

# 遍历当前目录及其子目录下的所有 markdown 文件
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith('.md'):
            file_path = os.path.normpath(os.path.join(root, file))
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 使用正则表达式匹配图片路径
                matches = re.findall(pattern, content)
                for match in matches:
                    # 将匹配到的图片路径添加到集合中
                    image_path = os.path.normpath(os.path.join(root, match[0] or match[1]))
                    image_path = unquote(image_path)
                    print(image_path)
                    
                    image_paths.add(image_path)

# 遍历当前目录及其子目录下的所有图片文件
for root, dirs, files in os.walk(root_path):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            file_path = os.path.normpath(os.path.join(root, file))
            file_path = unquote(file_path)
            
            # 如果图片路径不在集合中，则删除该图片文件
            if file_path not in image_paths:
                os.remove(file_path)
                print(f"Deleted image: {file_path}")