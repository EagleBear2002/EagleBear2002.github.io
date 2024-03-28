import os
import glob
import re
import urllib.parse

def find_matching_md_filenames(folder_path, article_name_prefix):
    matching_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith(article_name_prefix) and file.endswith(".md"):
                matching_files.append(os.path.join(root, os.path.splitext(file)[0]))
    return matching_files

def delete_images(article_name):
    image_folder_path = article_name
    md_file_path = image_folder_path + ".md"

    print("Markdown Path: " + md_file_path)

    # 获取 markdown 文件中引用的图片路径
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 使用正则表达式提取图片路径
    # 匹配 Markdown 语法 ![alt_text](image_path) 和 HTML 语法 <img src="image_path" alt="alt_text">
    image_paths = re.findall(r'!\[.*?\]\((.*?)\)|<img[^>]+src=["\'](.*?)["\']', content)

    # 将图片路径列表展开成一维列表
    # image_paths = [path for group in image_paths for path in group if path]
    image_paths = [urllib.parse.unquote(folder_path + SEP + path).replace("/", SEP) for group in image_paths for path in group if path]

    # print("#############################################################")
    # for path in image_paths:
    #     print(path)
    # print("#############################################################")

    # 获取资源目录下的所有图片文件
    image_files = glob.glob(image_folder_path + SEP + "*")

    # print(image_paths)

    # 删除未被引用的图片文件
    for file in image_files:
        if file not in image_paths:
            os.remove(file)
            print("delete " + file)
        # else:
            # print("saved " + file)


    print("Successfully remove unused images in " + md_file_path)
    print()

SEP = os.path.sep
folder_path = os.path.join("_posts", "分布式数据库")
article_name_prefix = ""
article_names = find_matching_md_filenames(folder_path, article_name_prefix)
print('find_matching_md_filenames: ' + str(article_names))

for article_name in article_names:
    delete_images(article_name)
