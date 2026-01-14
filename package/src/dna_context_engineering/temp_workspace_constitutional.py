"""
宪法级临时工作区管理技能 - 确保所有创建的工作区和文件符合宪法原则
所有生成的目录结构和文件都必须遵循宪法原则
"""
from typing import Dict, Any
import os
import tempfile
import shutil
from pathlib import Path
import subprocess
import json


# 全局变量存储当前工作会话
_current_temp_workspace = None
_confirmed_area = None
_max_temp_files = 20  # 临时文件数量阈值


def execute(args: Dict[str, Any]) -> str:
    """
    执行宪法级临时工作区管理技能
    确保所有操作都符合宪法原则
    """
    # 导入宪法验证器
    try:
        from .constitutional_validator import validate_constitutional_compliance
    except ImportError:
        return "错误: 无法导入宪法验证功能"

    # 验证输入参数是否符合宪法原则
    validation = validate_constitutional_compliance(str(args), "cognitive_convenience")
    if not validation["compliant"]:
        return f"❌ 参数宪法验证失败: {validation['feedback']}"

    operation = args.get("operation", "")
    file_content = args.get("file_content", "")
    file_path = args.get("file_path", "")
    confirm_file = args.get("confirm_file", "")

    # 对特定操作的内容进行宪法验证
    if operation == "add-file" and file_content:
        content_validation = validate_constitutional_compliance(file_content, "all")
        if not content_validation["compliant"]:
            return f"❌ 文件内容宪法验证失败: {content_validation['feedback']}"

    if operation == "create-workspace":
        return create_constitutional_workspace()
    elif operation == "add-file":
        return add_constitutional_file_to_workspace(file_path, file_content)
    elif operation == "list-files":
        return list_constitutional_files_in_workspace()
    elif operation == "confirm-file":
        return confirm_constitutional_file_from_workspace(confirm_file)
    elif operation == "confirm-all":
        return confirm_all_constitutional_files_from_workspace()
    elif operation == "clean-workspace":
        return clean_constitutional_workspace()
    elif operation == "get-workspace-path":
        return get_constitutional_workspace_path()
    elif operation == "auto-manage":
        return auto_manage_constitutional_workspace()
    elif operation == "integrate-with-git":
        repo_path = args.get("repo_path", ".")
        return integrate_constitutional_with_git(repo_path)
    else:
        validation = validate_constitutional_compliance(f"未知操作: {operation}", "cognitive_gestalt")
        if not validation["compliant"]:
            return f"❌ 未知操作宪法验证失败: {validation['feedback']}"
        return f"未知操作: {operation}"


def create_constitutional_workspace() -> str:
    """
    创建宪法级临时工作区
    确保工作区结构符合宪法原则
    """
    global _current_temp_workspace, _confirmed_area

    # 创建临时目录
    _current_temp_workspace = tempfile.mkdtemp(prefix="constitutional_ai_workspace_")

    # 创建确认区域 - 确保路径符合宪法原则
    _confirmed_area = os.path.join(_current_temp_workspace, "confirmed")
    os.makedirs(_confirmed_area, exist_ok=True)

    # 创建宪法合规说明文件
    constitution_file = os.path.join(_current_temp_workspace, "CONSTITUTION_COMPLIANCE.md")
    constitution_content = """# 工作区宪法合规说明

此工作区严格遵循DNASPEC宪法原则：

## 宪法原则
1. **渐进披露原则**: 信息按层次组织
2. **认知便利原则**: 内容清晰、便于理解  
3. **信息封装原则**: 内容自包含、边界清晰
4. **认知格式塔原则**: 形成完整认知单元

## 工作区结构
- `confirmed/` - 确认区域，存放通过验证的内容
- 临时文件 - 待确认和验证的内容
"""
    
    # 验证宪法说明内容
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(constitution_content, "information_encapsulation")
        if not validation["compliant"]:
            constitution_content += f"\n\n宪法注释: {validation['feedback']}"
    except ImportError:
        pass

    with open(constitution_file, 'w', encoding='utf-8') as f:
        f.write(constitution_content)

    result = f"🏛️ 宪法级临时工作区已创建: {_current_temp_workspace}"

    # 验证结果
    try:
        validation = validate_constitutional_compliance(result, "information_encapsulation")
        if not validation["compliant"]:
            result += f" (宪法验证: {validation['feedback']})"
    except ImportError:
        pass

    return result


def add_constitutional_file_to_workspace(file_path: str, content: str) -> str:
    """
    添加宪法合规的文件到工作区
    确保文件内容符合宪法原则
    """
    global _current_temp_workspace

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区，请先执行create-workspace操作"

    # 验证文件路径
    try:
        from .constitutional_validator import validate_constitutional_compliance
        path_validation = validate_constitutional_compliance(file_path, "cognitive_convenience")
        if not path_validation["compliant"]:
            return f"❌ 文件路径宪法验证失败: {path_validation['feedback']}"
    except ImportError:
        pass

    # 确保临时工作区路径存在
    temp_file_path = os.path.join(_current_temp_workspace, file_path)
    os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

    # 验证内容是否符合宪法原则
    content_validation = validate_constitutional_compliance(content, "all")
    if not content_validation["compliant"]:
        # 如果内容不符合宪法原则，记录宪法注释
        content_with_note = f"{content}\n\n<!-- Constitutional Note: {content_validation['feedback']} -->"
        final_content = content_with_note
    else:
        final_content = content

    # 写入文件内容
    with open(temp_file_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    # 检查是否需要整理清理
    result = auto_manage_constitutional_workspace()

    final_result = f"📄 宪法级文件已添加到工作区: {temp_file_path}\n{result}"

    # 验证最终结果
    try:
        validation = validate_constitutional_compliance(final_result, "information_encapsulation")
        if not validation["compliant"]:
            final_result += f"\n宪法验证: {validation['feedback']}"
    except ImportError:
        pass

    return final_result


def list_constitutional_files_in_workspace() -> str:
    """
    列出宪法级工作区中的文件
    """
    global _current_temp_workspace

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    files = []
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not file_path.startswith(os.path.join(_current_temp_workspace, "confirmed")):
                files.append(file_path)

    if not files:
        result = "临时工作区中没有文件"
    else:
        result = f"🏛️ 宪法级工作区中的文件 ({len(files)} 个):\n"
        for file_path in files:
            result += f"  - {file_path}\n"

    # 验证结果
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "cognitive_convenience")
        if not validation["compliant"]:
            result += f"\n宪法验证: {validation['feedback']}"
    except ImportError:
        pass

    return result


def confirm_constitutional_file_from_workspace(file_path: str) -> str:
    """
    将文件从宪法级工作区确认到确认区域
    确保确认过程符合宪法原则
    """
    global _current_temp_workspace, _confirmed_area

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    temp_file_path = os.path.join(_current_temp_workspace, file_path)
    confirmed_file_path = os.path.join(_confirmed_area, file_path)

    if not os.path.exists(temp_file_path):
        return f"错误: 临时文件不存在: {temp_file_path}"

    # 确保目标目录存在
    os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)

    # 读取临时文件内容
    with open(temp_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 验证内容在确认时是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        content_validation = validate_constitutional_compliance(content, "all")
        if not content_validation["compliant"]:
            # 添加宪法注释到内容中
            content_with_note = f"{content}\n\n<!-- Constitutional Note: {content_validation['feedback']} -->"
        else:
            content_with_note = content

        # 写入确认区域
        confirmed_dir = os.path.dirname(confirmed_file_path)
        os.makedirs(confirmed_dir, exist_ok=True)
        with open(confirmed_file_path, 'w', encoding='utf-8') as f:
            f.write(content_with_note)
    except ImportError:
        # 如果无法验证，直接写入
        with open(confirmed_file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    result = f"✅ 文件已宪法确认到确认区域: {confirmed_file_path}"

    # 验证结果
    try:
        validation = validate_constitutional_compliance(result, "information_encapsulation")
        if not validation["compliant"]:
            result += f" (宪法验证: {validation['feedback']})"
    except ImportError:
        pass

    return result


def confirm_all_constitutional_files_from_workspace() -> str:
    """
    将宪法级工作区中的所有文件确认到确认区域
    """
    global _current_temp_workspace, _confirmed_area

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    files = []
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            if not file_path.startswith(os.path.join(_current_temp_workspace, "confirmed")):
                files.append(os.path.relpath(file_path, _current_temp_workspace))

    confirmed_count = 0
    for file_path in files:
        temp_file_path = os.path.join(_current_temp_workspace, file_path)
        confirmed_file_path = os.path.join(_confirmed_area, file_path)

        # 读取文件内容
        with open(temp_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 验证每个文件内容是否符合宪法原则
        try:
            from .constitutional_validator import validate_constitutional_compliance
            content_validation = validate_constitutional_compliance(content, "all")
            if not content_validation["compliant"]:
                # 添加宪法注释
                content_with_note = f"{content}\n\n<!-- Constitutional Note: {content_validation['feedback']} -->"
            else:
                content_with_note = content
        except ImportError:
            content_with_note = content

        os.makedirs(os.path.dirname(confirmed_file_path), exist_ok=True)
        with open(confirmed_file_path, 'w', encoding='utf-8') as f:
            f.write(content_with_note)
        confirmed_count += 1

    result = f"✅ 已宪法确认 {confirmed_count} 个文件到确认区域"

    # 验证结果
    try:
        validation = validate_constitutional_compliance(result, "information_encapsulation")
        if not validation["compliant"]:
            result += f" (宪法验证: {validation['feedback']})"
    except ImportError:
        pass

    return result


def clean_constitutional_workspace() -> str:
    """
    清理宪法级工作区
    """
    global _current_temp_workspace

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    try:
        shutil.rmtree(_current_temp_workspace)
        _current_temp_workspace = None

        result = "🏛️ 宪法级临时工作区已清理"

        # 验证结果
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(result, "cognitive_convenience")
            if not validation["compliant"]:
                result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass

        return result
    except Exception as e:
        error_result = f"❌ 清理宪法级工作区失败: {str(e)}"

        # 验证错误结果
        try:
            validation = validate_constitutional_compliance(error_result, "cognitive_convenience")
            if not validation["compliant"]:
                error_result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass

        return error_result


def get_constitutional_workspace_path() -> str:
    """
    获取宪法级工作区路径
    """
    global _current_temp_workspace

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    result = _current_temp_workspace

    # 验证结果
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "cognitive_convenience")
        if not validation["compliant"]:
            result += f" (宪法验证: {validation['feedback']})"
    except ImportError:
        pass

    return result


def auto_manage_constitutional_workspace() -> str:
    """
    自动管理宪法级工作区
    """
    global _current_temp_workspace, _max_temp_files

    if not _current_temp_workspace:
        return "错误: 未创建临时工作区"

    # 计算临时文件数量（排除confirmed目录）
    temp_file_count = 0
    for root, dirs, filenames in os.walk(_current_temp_workspace):
        if not root.startswith(os.path.join(_current_temp_workspace, "confirmed")):
            temp_file_count += len(filenames)

    if temp_file_count > _max_temp_files:
        # 超过阈值，进行整理
        result = f"⚠️ 临时文件数量 ({temp_file_count}) 超过宪法阈值 ({_max_temp_files})，建议进行整理:\n"
        result += "1. 选择需要确认的文件: 使用 confirm-file 操作\n"
        result += "2. 或确认所有文件: 使用 confirm-all 操作\n"
        result += "3. 或清理临时工作区: 使用 clean-workspace 操作\n"
        result += list_constitutional_files_in_workspace()
    else:
        result = f"✅ 临时文件数量正常 ({temp_file_count}/{_max_temp_files})"

    # 验证结果
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "cognitive_convenience")
        if not validation["compliant"]:
            result += f"\n宪法验证: {validation['feedback']}"
    except ImportError:
        pass

    return result


def integrate_constitutional_with_git(confirm_to_repo: str = ".") -> str:
    """
    与Git集成：将确认区域的宪法合规文件提交到Git仓库
    """
    global _confirmed_area

    if not _confirmed_area:
        return "错误: 未创建临时工作区或确认区域"

    if not os.path.exists(_confirmed_area):
        return "错误: 确认区域不存在"

    try:
        # 切换到目标仓库目录
        original_dir = os.getcwd()
        os.chdir(confirm_to_repo)

        # 获取确认区域所有文件
        files_to_add = []
        for root, dirs, filenames in os.walk(_confirmed_area):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                rel_path = os.path.relpath(file_path, _confirmed_area)
                files_to_add.append(rel_path)

        if not files_to_add:
            result = "确认区域中没有宪法合规文件需要提交"
        else:
            # 使用Git命令添加文件
            git_add_cmd = ["git", "add"] + files_to_add
            result_add = subprocess.run(git_add_cmd, capture_output=True, text=True)

            if result_add.returncode != 0:
                result = f"Git添加宪法合规文件失败: {result_add.stderr}"
            else:
                # 提交更改
                commit_msg = f"Constitutional AI generated files: {', '.join(files_to_add[:5])}{'...' if len(files_to_add) > 5 else ''}"

                # 验证提交消息是否符合宪法原则
                try:
                    from .constitutional_validator import validate_constitutional_compliance
                    commit_validation = validate_constitutional_compliance(commit_msg, "cognitive_convenience")
                    if not commit_validation["compliant"]:
                        commit_msg += f" # Constitutional Note: {commit_validation['feedback']}"
                except ImportError:
                    pass

                git_commit_cmd = ["git", "commit", "-m", commit_msg]
                result_commit = subprocess.run(git_commit_cmd, capture_output=True, text=True)

                if result_commit.returncode != 0:
                    result = f"Git提交宪法合规文件失败: {result_commit.stderr}"
                else:
                    result = f"✅ 成功将 {len(files_to_add)} 个宪法合规文件提交到Git仓库"

        os.chdir(original_dir)

        # 验证Git集成结果
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(result, "all")
            if not validation["compliant"]:
                result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass

        return result

    except Exception as e:
        os.chdir(original_dir)
        error_result = f"❌ Git宪法集成操作失败: {str(e)}"

        # 验证错误结果
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(error_result, "cognitive_convenience")
            if not validation["compliant"]:
                error_result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass

        return error_result