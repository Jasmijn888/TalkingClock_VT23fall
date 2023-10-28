import os

# 获取当前文件夹中所有匹配的文件
folder_path = os.getcwd()
files = [f for f in os.listdir(folder_path) if f.startswith("output_") and f.endswith(".mp3")]

for filename in files:
    # 提取 "output_hour_x.mp3" 或 "output_min_x.mp3" 中的数字部分
    parts = filename.split("_")
    if len(parts) == 3 and (parts[1] == "hour" or parts[1] == "min"):
        num = parts[2].split(".")[0]  # 提取 "x" 部分

        # 构建新的文件名
        new_filename = f"DE_{num}{parts[1][0]}.mp3"

        # 重命名文件
        os.rename(filename, new_filename)
        print(f"重命名文件: {filename} -> {new_filename}")

print("重命名完成")
