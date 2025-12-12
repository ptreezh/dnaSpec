"""
Cache Manager Skill - 缓存区管理技能
用于项目初始化时搭建缓存区，避免AI产生冗余文件
"""
from typing import Dict, Any
import os
import json
from pathlib import Path
import time
from datetime import datetime, timedelta


# 全局缓存区配置
_cache_config = {
    "cache_root": ".dnaspec/cache",
    "temp_area": ".dnaspec/temp",
    "staging_area": ".dnaspec/staging",
    "max_cache_size_mb": 500,
    "auto_cleanup_hours": 24,
    "gitignore_patterns": [
        ".dnaspec/temp/*",
        ".dnaspec/staging/*",
        "*_temp*",
        "*_debug*",
        "*_test_*.py",
        "ai_generated_*",
        "experiment_*"
    ]
}

_current_session = None


def execute(args: Dict[str, Any]) -> str:
    """
    执行缓存区管理技能
    """
    operation = args.get("operation", "")
    project_path = args.get("project_path", ".")
    content = args.get("content", "")
    file_path = args.get("file_path", "")

    if operation == "init-cache":
        return initialize_cache_system(project_path)
    elif operation == "stage-file":
        return stage_file(file_path, content, project_path)
    elif operation == "validate-staged":
        return validate_staged_files(project_path)
    elif operation == "commit-staged":
        return commit_staged_files(project_path, args.get("message", ""))
    elif operation == "cleanup-cache":
        return cleanup_cache(project_path)
    elif operation == "cache-status":
        return get_cache_status(project_path)
    elif operation == "add-gitignore":
        return setup_gitignore(project_path)
    elif operation == "configure-rules":
        return configure_ai_rules(project_path, args.get("rules", {}))
    else:
        return f"未知操作: {operation}"


def initialize_cache_system(project_path: str) -> str:
    """
    在项目中初始化缓存系统
    """
    global _current_session
    project_root = Path(project_path).resolve()

    # 创建缓存区目录结构
    cache_root = project_root / _cache_config["cache_root"]
    temp_area = cache_root / "temp"
    staging_area = cache_root / "staging"
    meta_dir = cache_root / "meta"

    for directory in [cache_root, temp_area, staging_area, meta_dir]:
        directory.mkdir(parents=True, exist_ok=True)

    # 创建缓存配置文件
    config_file = meta_dir / "cache_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(_cache_config, f, indent=2, ensure_ascii=False)

    # 创建会话文件
    _current_session = {
        "session_id": f"cache_session_{int(time.time())}",
        "start_time": datetime.now().isoformat(),
        "project_path": str(project_root),
        "files_staged": 0,
        "files_committed": 0,
        "temp_files": []
    }

    session_file = meta_dir / "current_session.json"
    with open(session_file, 'w', encoding='utf-8') as f:
        json.dump(_current_session, f, indent=2, ensure_ascii=False)

    # 创建.gitignore（如果不存在）
    setup_gitignore(project_path)

    result = f"""🚀 DNASPEC缓存系统初始化完成！

📁 缓存区结构:
  - 临时工作区: {temp_area}
  - 验证暂存区: {staging_area}
  - 元数据目录: {meta_dir}

📋 会话ID: {_current_session['session_id']}
📅 开始时间: {_current_session['start_time']}
🎯 项目路径: {project_root}

✅ 缓存系统已准备就绪，开始管理AI生成的文件...
"""

    return result


def stage_file(file_path: str, content: str, project_path: str) -> str:
    """
    将文件暂存到验证区
    """
    global _current_session
    project_root = Path(project_path).resolve()
    staging_area = project_root / _cache_config["staging_area"]

    # 更新会话
    _current_session = load_session(project_root)
    if not _current_session:
        return "错误: 缓存系统未初始化，请先运行init-cache操作"

    # 生成暂存文件路径
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    staging_filename = f"{timestamp}_{os.path.basename(file_path)}"
    staging_path = staging_area / staging_filename

    # 写入暂存文件
    try:
        with open(staging_path, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        return f"❌ 暂存文件失败: {str(e)}"

    # 创建元数据
    metadata = {
        "original_path": file_path,
        "staging_path": str(staging_path),
        "timestamp": timestamp,
        "size_bytes": len(content.encode('utf-8')),
        "session_id": _current_session["session_id"],
        "status": "staged",
        "validation_checks": []
    }

    metadata_file = staging_area / f"{staging_filename}.meta.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    # 更新会话统计
    _current_session["files_staged"] += 1
    save_session(project_root, _current_session)

    result = f"""📝 文件已暂存到验证区

📄 原始路径: {file_path}
📁 暂存路径: {staging_path}
⏰ 暂存时间: {timestamp}
📊 文件大小: {metadata['size_bytes']} 字节

🔍 文件正在等待验证...
使用 'validate-staged' 命令进行验证
"""

    return result


def validate_staged_files(project_path: str) -> str:
    """
    验证暂存区中的文件
    """
    project_root = Path(project_path).resolve()
    staging_area = project_root / _cache_config["staging_area"]

    if not staging_area.exists():
        return "❌ 错误: 暂存区不存在"

    staged_files = list(staging_area.glob("*.meta.json"))
    if not staged_files:
        return "📭 暂存区中没有文件需要验证"

    validation_results = []

    for meta_file in staged_files:
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            staging_path = Path(metadata["staging_path"])
            if not staging_path.exists():
                validation_results.append(f"❌ {metadata['original_path']}: 暂存文件不存在")
                continue

            # 基本验证检查
            checks = []

            # 检查文件大小
            if metadata["size_bytes"] == 0:
                checks.append("⚠️ 文件为空")
            else:
                checks.append("✅ 文件大小正常")

            # 检查文件内容是否包含敏感信息
            with open(staging_path, 'r', encoding='utf-8') as f:
                content = f.read()

            sensitive_patterns = ["password", "api_key", "secret", "token", "private_key"]
            found_sensitive = []
            for pattern in sensitive_patterns:
                if pattern.lower() in content.lower():
                    found_sensitive.append(pattern)

            if found_sensitive:
                checks.append(f"⚠️ 发现敏感信息: {', '.join(found_sensitive)}")
            else:
                checks.append("✅ 未发现敏感信息")

            # 检查代码语法（如果是代码文件）
            if metadata["original_path"].endswith(('.py', '.js', '.java', '.cpp', '.c')):
                if content.strip().startswith(('def ', 'function', 'class ', 'public class', 'import ', 'from ')):
                    checks.append("✅ 代码结构正常")
                else:
                    checks.append("⚠️ 可能不是有效的代码文件")

            metadata["validation_checks"] = checks
            metadata["status"] = "validated" if all("✅" in check for check in checks) else "needs_review"

            # 保存更新的元数据
            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            validation_results.append(f"{'✅' if metadata['status'] == 'validated' else '⚠️'} {metadata['original_path']}: {'; '.join(checks)}")

        except Exception as e:
            validation_results.append(f"❌ 验证 {meta_file.name} 时出错: {str(e)}")

    result = "🔍 验证结果:\n" + "\n".join(validation_results)
    return result


def commit_staged_files(project_path: str, commit_message: str = "") -> str:
    """
    将验证通过的文件提交到主工作区
    """
    project_root = Path(project_path).resolve()
    staging_area = project_root / _cache_config["staging_area"]
    _current_session = load_session(project_root)

    if not _current_session:
        return "❌ 错误: 缓存系统未初始化"

    staged_files = list(staging_area.glob("*.meta.json"))
    if not staged_files:
        return "📭 暂存区中没有文件"

    committed_count = 0
    commit_results = []

    for meta_file in staged_files:
        try:
            with open(meta_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)

            if metadata["status"] != "validated":
                continue

            staging_path = Path(metadata["staging_path"])
            target_path = project_root / metadata["original_path"]

            # 确保目标目录存在
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # 移动文件到主工作区
            import shutil
            shutil.move(str(staging_path), str(target_path))

            # 更新Git（如果是Git仓库）
            if (project_root / ".git").exists():
                try:
                    import subprocess
                    subprocess.run(["git", "add", str(target_path.relative(project_root))],
                              cwd=project_root, capture_output=True)
                except:
                    pass  # Git操作失败不影响文件移动

            # 更新元数据
            metadata["status"] = "committed"
            metadata["commit_time"] = datetime.now().isoformat()
            metadata["commit_message"] = commit_message

            with open(meta_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)

            committed_count += 1
            commit_results.append(f"✅ {metadata['original_path']} 已提交到主工作区")

        except Exception as e:
            commit_results.append(f"❌ 提交 {meta_file.name} 失败: {str(e)}")

    # 更新会话统计
    _current_session["files_committed"] += committed_count
    save_session(project_root, _current_session)

    result = f"🎯 文件提交完成!

📈 提交统计:
{chr(10).join(commit_results)}

✅ 成功提交: {committed_count} 个文件
📊 总计提交: {_current_session['files_committed']} 个文件
📝 提交信息: {commit_message or '自动提交'}"

    return result


def setup_gitignore(project_path: str) -> str:
    """
    设置.gitignore文件，避免缓存区文件被Git跟踪
    """
    project_root = Path(project_path).resolve()
    gitignore_path = project_root / ".gitignore"

    gitignore_content = """
# DNASPEC缓存区文件 - 避免AI生成文件被Git跟踪
.dnaspec/temp/
.dnaspec/staging/
.dnaspec/cache/meta/

# AI生成的临时文件
*ai_generated*
*experiment_*
*debug_*
*test_temp*
*_temp.*
.temp.*
cache_*.py
ai_works/

# IDE和编辑器临时文件
.vscode/
.idea/
*.swp
*.swo
*~

# Python缓存
__pycache__/
*.py[cod]
*$py.class
*.egg-info/
"""

    try:
        if gitignore_path.exists():
            # 读取现有内容并合并
            existing_content = gitignore_path.read_text(encoding='utf-8')
            if ".dnaspec/" not in existing_content:
                gitignore_path.write_text(existing_content + gitignore_content, encoding='utf-8')
                return "✅ .gitignore 已更新，添加DNASPEC缓存规则"
            else:
                return "ℹ️ .gitignore 已包含DNASPEC规则"
        else:
            gitignore_path.write_text(gitignore_content, encoding='utf-8')
            return "✅ .gitignore 已创建，包含DNASPEC缓存规则"
    except Exception as e:
        return f"❌ 设置.gitignore失败: {str(e)}"


def configure_ai_rules(project_path: str, rules: Dict[str, Any]) -> str:
    """
    配置AI文件管理规则
    """
    project_root = Path(project_path).resolve()
    meta_dir = project_root / _cache_config["cache_root"] / "meta"

    rules_file = meta_dir / "ai_rules.json"

    default_rules = {
        "auto_validation": True,
        "auto_commit": False,
        "max_file_size_kb": 1000,
        "allowed_extensions": [".py", ".js", ".ts", ".java", ".cpp", ".c", ".md", ".txt"],
        "blocked_patterns": ["password", "secret", "token", "api_key", "private_key"],
        "cleanup_after_hours": 24,
        "git_auto_add": True
    }

    # 合并用户自定义规则
    default_rules.update(rules)

    try:
        with open(rules_file, 'w', encoding='utf-8') as f:
            json.dump(default_rules, f, indent=2, ensure_ascii=False)
        return f"✅ AI规则配置已更新到 {rules_file}"
    except Exception as e:
        return f"❌ 配置AI规则失败: {str(e)}"


def load_session(project_path: str) -> Dict[str, Any]:
    """加载当前会话"""
    try:
        project_root = Path(project_path).resolve()
        session_file = project_root / _cache_config["cache_root"] / "meta" / "current_session.json"
        if session_file.exists():
            with open(session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        return None


def save_session(project_path: str, session: Dict[str, Any]) -> None:
    """保存会话"""
    try:
        project_root = Path(project_path).resolve()
        session_file = project_root / _cache_config["cache_root"] / "meta" / "current_session.json"
        with open(session_file, 'w', encoding='utf-8') as f:
            json.dump(session, f, indent=2, ensure_ascii=False)
    except:
        pass


def cleanup_cache(project_path: str) -> str:
    """清理过期缓存文件"""
    project_root = Path(project_path).resolve()
    staging_area = project_root / _cache_config["staging_area"]
    temp_area = project_root / _cache_config["temp"]

    cleanup_count = 0
    results = []

    # 清理超过24小时的暂存文件
    if staging_area.exists():
        cutoff_time = datetime.now() - timedelta(hours=_cache_config["auto_cleanup_hours"])
        for meta_file in staging_area.glob("*.meta.json"):
            try:
                with open(meta_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)

                staging_path = Path(metadata["staging_path"])
                if staging_path.exists():
                    file_time = datetime.fromisoformat(metadata["timestamp"])
                    if file_time < cutoff_time:
                        staging_path.unlink()
                        meta_file.unlink()
                        cleanup_count += 1
                        results.append(f"清理过期文件: {metadata['original_path']}")
            except:
                continue

    if cleanup_count == 0:
        return "✅ 缓存区清理完成，没有过期文件"
    else:
        return f"🧹 缓存区清理完成，清理了 {cleanup_count} 个过期文件"


def get_cache_status(project_path: str) -> str:
    """获取缓存状态"""
    project_root = Path(project_path).resolve()
    cache_root = project_root / _cache_config["cache_root"]

    if not cache_root.exists():
        return "❌ 缓存系统未初始化"

    staging_area = cache_root / "staging_area"
    temp_area = cache_root / "temp"

    staging_count = len(list(staging_area.glob("*.meta.json"))) if staging_area.exists() else 0
    temp_count = len(list(temp_area.rglob("*"))) if temp_area.exists() else 0

    session = load_session(project_path)
    session_info = ""
    if session:
        session_info = f"""
会话信息:
  - 会话ID: {session.get('session_id', 'N/A')}
  - 开始时间: {session.get('start_time', 'N/A')}
  - 暂存文件: {session.get('files_staged', 0)}
  - 提交文件: {session.get('files_committed', 0)}
"""

    return f"""📊 DNASPEC缓存状态

📁 缓存目录: {cache_root}
📋 暂存文件: {staging_count} 个
🗂️ 临时文件: {temp_count} 个
💾 缓存大小限制: {_cache_config['max_cache_size_mb']}MB
🧹 自动清理: {_cache_config['auto_cleanup_hours']}小时

{session_info}
"""