import os
import shutil
from pathlib import Path

def archive_abandoned_skills():
    """
    档案化废弃技能 - 将留核心技能，其他移至 archive 目录
    """
    skills_dir = Path("D:/DAIP/dnaSpec/src/dna_spec_kit_integration/skills")
    archive_dir = Path("D:/DAIP/dnaSpec/archive/skills")
    
    # 确保 archive 目录存在
    archive_dir.mkdir(parents=True, exist_ok=True)
    
    # 核心技能文件（需要保留在原位置）
    core_skills = {
        'unified_skill.py',  # 统一技能实现
        '__init__.py',       # 模块初始化
        '__pycache__'        # 缓存目录
    }
    
    # 获取所有技能文件
    all_files = set()
    for item in skills_dir.iterdir():
        all_files.add(item.name)
    
    # 识别要归档的废弃技能
    abandoned_skills = []
    for item in all_files:
        if item not in core_skills and not item.startswith('__'):
            src_path = skills_dir / item
            dst_path = archive_dir / item
            try:
                if src_path.is_file():
                    shutil.move(str(src_path), str(dst_path))
                    abandoned_skills.append(item)
                    print(f"MOVED: {item} -> archive/")
                elif src_path.is_dir():
                    shutil.move(str(src_path), str(dst_path))
                    abandoned_skills.append(item)
                    print(f"MOVED: {item}/ -> archive/")
            except Exception as e:
                print(f"ERROR moving {item}: {e}")
    
    print(f"\n档案化完成！共移动 {len(abandoned_skills)} 个废弃技能/文件到 archive 目录")
    print(f"保留的核心技能: {list(core_skills - {'__pycache__'})}")
    
    return abandoned_skills

if __name__ == "__main__":
    archived = archive_abandoned_skills()
    print(f"\n归档的文件列表: {archived}")