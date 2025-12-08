import os
import shutil

# 源目录和目标目录
source_dir = r"D:\DAIP\dnaSpec\DNASPEC-Project"
dest_dir = r"D:\DAIP\dnaspec-core\DNASPEC-Project"

# 创建目标目录
os.makedirs(os.path.dirname(dest_dir), exist_ok=True)

# 复制整个目录树
if os.path.exists(source_dir):
    shutil.copytree(source_dir, dest_dir)
    print(f"成功复制 {source_dir} 到 {dest_dir}")
else:
    print(f"源目录不存在: {source_dir}")