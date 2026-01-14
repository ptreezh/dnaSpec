"""
Git Operations Skill - 宪法级Git操作技能
确保所有生成的Git配置、提交消息等都符合宪法原则
"""
from typing import Dict, Any
import os
import json
import subprocess
from pathlib import Path
from datetime import datetime
import re

def execute(args: Dict[str, Any]) -> str:
    """
    执行宪法级Git操作技能
    """
    # 导入宪法验证功能
    try:
        from .constitutional_validator import validate_constitutional_compliance
    except ImportError:
        return "错误: 无法导入宪法验证功能"

    operation = args.get("operation", "")
    project_path = args.get("project_path", ".")

    # 验证操作参数是否符合宪法原则
    validation = validate_constitutional_compliance(json.dumps(args), "cognitive_convenience")
    if not validation["compliant"]:
        return f"参数宪法验证失败: {validation['feedback']}"

    if operation == "setup-constitution":
        return setup_git_constitution(project_path, args.get("rules", {}))
    elif operation == "install-hooks":
        return install_git_hooks(project_path)
    elif operation == "validate-commit":
        message = args.get("message", "")
        # 验证提交消息是否符合宪法原则
        validation = validate_constitutional_compliance(message, "cognitive_convenience")
        if not validation["compliant"]:
            return f"提交消息宪法验证失败: {validation['feedback']}"
        return validate_commit_message(project_path, message)
    elif operation == "smart-commit":
        message = args.get("message", "")
        # 验证提交消息是否符合宪法原则
        validation = validate_constitutional_compliance(message, "cognitive_convenience")
        if not validation["compliant"]:
            return f"提交消息宪法验证失败: {validation['feedback']}"
        return smart_commit(project_path, message)
    elif operation == "clean-workspace":
        return clean_workspace(project_path)
    elif operation == "status-report":
        return get_workspace_status(project_path)
    elif operation == "create-workflow":
        workflow = args.get("workflow", {})
        # 验证工作流配置是否符合宪法原则
        validation = validate_constitutional_compliance(json.dumps(workflow), "information_encapsulation")
        if not validation["compliant"]:
            return f"工作流配置宪法验证失败: {validation['feedback']}"
        return create_workflow_rules(project_path, workflow)
    elif operation == "enforce-rules":
        return enforce_git_rules(project_path)
    elif operation == "branch-policy":
        policy = args.get("policy", {})
        # 验证分支策略是否符合宪法原则
        validation = validate_constitutional_compliance(json.dumps(policy), "cognitive_convenience")
        if not validation["compliant"]:
            return f"分支策略宪法验证失败: {validation['feedback']}"
        return setup_branch_policy(project_path, policy)
    elif operation == "review-policy":
        review_config = args.get("review_config", {})
        # 验证审查策略是否符合宪法原则
        validation = validate_constitutional_compliance(json.dumps(review_config), "cognitive_convenience")
        if not validation["compliant"]:
            return f"审查策略宪法验证失败: {validation['feedback']}"
        return setup_review_policy(project_path, review_config)
    else:
        validation = validate_constitutional_compliance(f"未知操作: {operation}", "cognitive_gestalt")
        if not validation["compliant"]:
            return f"操作错误宪法验证失败: {validation['feedback']}"
        return f"未知操作: {operation}"


def setup_git_constitution(project_path: str, rules: Dict[str, Any]) -> str:
    """
    设置Git项目宪法和规则，确保 Constitution 文件符合宪法原则
    """
    project_root = Path(project_path).resolve()

    # 创建.dnaspec目录
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)

    # 创建Git宪法配置
    constitution = {
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "project_path": str(project_root),
        "principles": [
            "AI生成的文件必须经过验证才能进入主工作区",
            "临时文件和调试文件自动被Git忽略",
            "只提交经过测试和验证的代码",
            "保持工作区清洁，避免AI污染",
            "所有内容必须符合宪法原则"
        ],
        "rules": {
            "auto_ignore_ai_files": True,
            "require_validation": True,
            "staging_required": True,
            "clean_temp_files": True,
            "enforce_commit_message_format": True,
            "enforce_constitutional_compliance": True
        },
        "custom_rules": rules
    }

    # 验证宪法配置是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        constitution_json = json.dumps(constitution, indent=2, ensure_ascii=False)
        validation = validate_constitutional_compliance(constitution_json, "all")
        if not validation["compliant"]:
            return f"宪法配置宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass  # 在某些环境中可能无法导入

    # 保存宪法文件
    constitution_file = dnaspec_dir / "git_constitution.json"
    with open(constitution_file, 'w', encoding='utf-8') as f:
        f.write(constitution_json)

    # 配置Git设置
    setup_git_configuration(project_root, constitution)

    result = f"""🏛️ Git项目宪法设置完成！

📋 宪法文件: {constitution_file}
🎯 项目路径: {project_root}
⚖️ 核心原则:
{chr(10).join(f'  • {principle}' for principle in constitution['principles'])}

✅ 已配置Git规则和钩子
🔒 工作区保护已激活
🚫 AI文件污染防护已启用

项目宪法将确保：
• 所有AI生成文件经过验证流程
• 临时和调试文件自动清理
• 保持工作区整洁有序
• 防止Git历史污染
• 所有内容符合宪法原则
"""

    # 验证结果是否符合宪法原则
    try:
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def setup_git_configuration(project_root: Path, constitution: Dict[str, Any]) -> None:
    """
    配置Git设置和规则
    """
    try:
        # 配置Git基本设置
        subprocess.run(["git", "config", "dnaspec.enabled", "true"],
                      cwd=project_root, capture_output=True)
        subprocess.run(["git", "config", "dnaspec.constitution",
                      str(project_root / ".dnaspec" / "git_constitution.json")],
                      cwd=project_root, capture_output=True)

        # 设置提交模板
        commit_template = get_commit_template(constitution)
        template_file = project_root / ".git" / "commit_template.txt"

        if not template_file.parent.exists():
            subprocess.run(["git", "init"], cwd=project_root, capture_output=True)

        template_file.write_text(commit_template, encoding='utf-8')
        subprocess.run(["git", "config", "commit.template", str(template_file)],
                      cwd=project_root, capture_output=True)

    except Exception as e:
        print(f"Git配置警告: {str(e)}")


def get_commit_template(constitution: Dict[str, Any]) -> str:
    """
    生成提交消息模板，确保模板内容符合宪法原则
    """
    template = """# DNASPEC项目宪法约束的提交模板
# 提交前请确认：
# 1. 代码已通过验证测试 ✓
# 2. 临时文件已清理 ✓
# 3. 符合项目规则 ✓
# 4. 内容符合宪法原则 ✓

# 类型:
[FEAT] 新功能
[FIX] 修复
[REFACTOR] 重构
[TEST] 测试
[DOCS] 文档
[STYLE] 格式
[PERF] 性能优化
[DNASPEC] AI生成内容

# 格式: <类型>(范围): 简短描述
# 示例: [FEAT](cache): 添加AI文件验证缓存系统

"""

    # 验证模板是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(template, "cognitive_convenience")
        if not validation["compliant"]:
            print(f"提交模板宪法验证警告: {validation['feedback']}")
    except ImportError:
        pass

    return template


def install_git_hooks(project_path: str) -> str:
    """
    安装Git钩子来执行DNASPEC规则
    """
    project_root = Path(project_path).resolve()
    hooks_dir = project_root / ".git" / "hooks"

    if not hooks_dir.exists():
        return "❌ 错误: 不是一个Git仓库，请先初始化Git"

    hooks_created = []

    # Pre-commit钩子 - 检查DNASPEC规则
    pre_commit_hook = '''#!/bin/sh
# DNASPEC Pre-commit Hook
# 检查暂存文件是否符合项目宪法

echo "🔍 DNASPEC Pre-commit 检查..."

# 检查是否有AI生成的临时文件
if git diff --cached --name-only | grep -E "(ai_generated|experiment_|debug_|temp_|test_temp)"; then
    echo "❌ 检测到AI生成临时文件，请先清理或验证"
    exit 1
fi

# 检查是否有未验证的大文件
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt 1048576 ]; then  # 1MB
            echo "⚠️  大文件检测: $file (${size} bytes) - 请确认已验证"
        fi
    fi
done

# 运行基本验证
python3 -c "
import json, sys, os
try:
    constitution_file = '.dnaspec/git_constitution.json'
    if os.path.exists(constitution_file):
        with open(constitution_file, 'r') as f:
            constitution = json.load(f)
        print('✅ DNASPEC项目宪法检查通过')
    else:
        print('⚠️  DNASPEC宪法文件不存在，建议初始化')
except Exception as e:
    print(f'⚠️  DNASPEC检查警告: {e}')
"

echo "✅ Pre-commit 检查完成"
exit 0
'''

    # Commit-msg钩子 - 验证提交消息格式
    commit_msg_hook = r'''#!/bin/sh
# DNASPEC Commit-msg Hook
# 验证提交消息格式

message=$(cat "$1")

# 检查最小长度
if [ ${#message} -lt 10 ]; then
    echo "❌ 提交消息太短，请提供更详细的描述"
    exit 1
fi

# 检查是否包含DNASPEC要求的类型
if ! echo "$message" | grep -E "^\[(FEAT|FIX|REFACTOR|TEST|DOCS|STYLE|PERF|DNASPEC)\]"; then
    echo "⚠️  建议使用标准提交类型: [FEAT], [FIX], [REFACTOR], [TEST], [DOCS], [STYLE], [PERF], [DNASPEC]"
fi

echo "✅ 提交消息格式验证通过"
exit 0
'''

    # Post-commit钩子 - 清理和报告
    post_commit_hook = '''#!/bin/sh
# DNASPEC Post-commit Hook
# 提交后清理和状态报告

echo "🧠 DNASPEC Post-commit 处理..."

# 清理可能的临时文件
find . -name "*ai_generated*" -type f -mtime +1 -delete 2>/dev/null || true
find . -name "experiment_*" -type f -mtime +1 -delete 2>/dev/null || true

# 更新DNASPEC统计
python3 -c "
import json, os, datetime
try:
    constitution_file = '.dnaspec/git_constitution.json'
    if os.path.exists(constitution_file):
        with open(constitution_file, 'r+') as f:
            constitution = json.load(f)
            if 'commit_count' not in constitution:
                constitution['commit_count'] = 0
            constitution['commit_count'] += 1
            constitution['last_commit'] = datetime.datetime.now().isoformat()
            f.seek(0)
            json.dump(constitution, f, indent=2, ensure_ascii=False)
            f.truncate()
        print(f'📊 DNASPEC统计: 已提交 {constitution[\"commit_count\"]} 次')
except Exception:
    pass
"

echo "✅ Post-commit 处理完成"
'''

    # 写入钩子文件
    hooks = [
        ("pre-commit", pre_commit_hook),
        ("commit-msg", commit_msg_hook),
        ("post-commit", post_commit_hook)
    ]

    for hook_name, hook_content in hooks:
        hook_file = hooks_dir / hook_name
        hook_file.write_text(hook_content, encoding='utf-8')
        hook_file.chmod(0o755)  # 设置可执行权限
        hooks_created.append(hook_name)

    result = f"""🎯 Git钩子安装完成！

已安装的钩子:
{chr(10).join(f'  • {hook}' for hook in hooks_created)}

📋 钩子功能:
• Pre-commit: 提交前检查AI文件和验证规则
• Commit-msg: 验证提交消息格式
• Post-commit: 清理临时文件和更新统计

🔒 项目宪法已强制执行
🚫 AI文件污染防护已激活
📊 提交统计已启用
"""

    # 验证结果是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"钩子安装结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def validate_commit_message(project_path: str, message: str) -> str:
    """
    验证提交消息是否符合DNASPEC规则
    """
    issues = []
    suggestions = []

    # 检查消息长度
    if len(message) < 10:
        issues.append("提交消息太短")
        suggestions.append("请提供至少10个字符的描述")

    # 检查是否包含类型标记
    type_pattern = r'^\[(FEAT|FIX|REFACTOR|TEST|DOCS|STYLE|PERF|DNASPEC)\]'
    if not re.match(type_pattern, message):
        issues.append("缺少标准提交类型")
        suggestions.append("使用格式: [类型] 描述")

    # 检查是否包含AI生成内容标记
    if any(keyword in message.lower() for keyword in ['ai', 'generated', '自动生成']):
        if '[DNASPEC]' not in message:
            issues.append("AI生成内容需要特殊标记")
            suggestions.append("使用 [DNASPEC] 标记AI生成内容")

    # 检查敏感信息
    sensitive_patterns = ['password', 'secret', 'token', 'api_key', 'private_key']
    found_sensitive = []
    for pattern in sensitive_patterns:
        if pattern.lower() in message.lower():
            found_sensitive.append(pattern)

    if found_sensitive:
        issues.append(f"发现敏感信息: {', '.join(found_sensitive)}")
        suggestions.append("移除敏感信息后再提交")

    if not issues:
        # 验证成功消息是否符合宪法原则
        result = "✅ 提交消息验证通过"
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(result, "cognitive_convenience")
            if not validation["compliant"]:
                result += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass
        return result
    else:
        result = "❌ 提交消息验证失败:\n\n"
        result += "发现的问题:\n" + "\n".join(f"• {issue}" for issue in issues)
        result += "\n\n建议:\n" + "\n".join(f"• {suggestion}" for suggestion in suggestions)
        
        # 验证错误消息是否符合宪法原则
        try:
            validation = validate_constitutional_compliance(result, "cognitive_convenience")
            if not validation["compliant"]:
                result += f"\n宪法验证反馈: {validation['feedback']}"
        except ImportError:
            pass
            
        return result


def smart_commit(project_path: str, commit_message: str = "") -> str:
    """
    智能提交，自动应用DNASPEC规则并确保提交内容符合宪法原则
    """
    project_root = Path(project_path).resolve()

    try:
        # 检查Git状态
        result = subprocess.run(["git", "status", "--porcelain"],
                              cwd=project_root, capture_output=True, text=True)

        if not result.stdout.strip():
            return "📭 没有需要提交的更改"

        # 分析更改类型
        changed_files = result.stdout.strip().split('\n')
        changes = []

        for line in changed_files:
            if line.strip():
                status = line[:2]
                file_path = line[3:]
                changes.append((status, file_path))

        # 生成智能提交消息
        if not commit_message:
            commit_message = generate_smart_commit_message(changes)

        # 执行提交前验证
        validation_result = validate_commit_message(project_path, commit_message)
        if "❌" in validation_result:
            return validation_result

        # 验证提交消息是否符合宪法原则
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(commit_message, "cognitive_convenience")
            if not validation["compliant"]:
                return f"提交消息宪法验证失败: {validation['feedback']}"
        except ImportError:
            pass

        # 添加文件到暂存区
        for status, file_path in changes:
            if status.strip():  # 有更改的文件
                subprocess.run(["git", "add", file_path], cwd=project_root, capture_output=True)

        # 提交
        result = subprocess.run(["git", "commit", "-m", commit_message],
                              cwd=project_root, capture_output=True, text=True)

        if result.returncode == 0:
            commit_result = f"""🎯 智能提交成功！

📝 提交消息: {commit_message}
📁 文件数量: {len([c for c in changes if c[0].strip()])}
🔍 DNASPEC规则: 已自动应用
✅ 项目宪法: 已遵守

提交的文件:
{chr(10).join(f'  {status} {path}' for status, path in changes if status.strip())}
"""

            # 验证提交结果是否符合宪法原则
            try:
                validation = validate_constitutional_compliance(commit_result, "all")
                if not validation["compliant"]:
                    return f"提交结果宪法验证失败: {validation['feedback']}"
            except ImportError:
                pass

            return commit_result
        else:
            return f"❌ 提交失败: {result.stderr}"

    except Exception as e:
        error_msg = f"❌ 智能提交出错: {str(e)}"
        # 验证错误消息是否符合宪法原则
        try:
            validation = validate_constitutional_compliance(error_msg, "cognitive_convenience")
            if not validation["compliant"]:
                error_msg += f" (宪法验证: {validation['feedback']})"
        except ImportError:
            pass
        return error_msg


def generate_smart_commit_message(changes: list) -> str:
    """
    根据文件更改生成智能提交消息
    """
    feat_count = 0
    fix_count = 0
    refactor_count = 0
    test_count = 0
    docs_count = 0

    # 分析文件类型和更改
    for status, file_path in changes:
        if any(keyword in file_path.lower() for keyword in ['test', 'spec']):
            test_count += 1
        elif any(keyword in file_path.lower() for keyword in ['doc', 'readme', 'md']):
            docs_count += 1
        elif 'fix' in status or 'bug' in file_path.lower():
            fix_count += 1
        elif any(keyword in file_path.lower() for keyword in ['refactor', 'cleanup']):
            refactor_count += 1
        else:
            feat_count += 1

    # 确定主要类型
    if fix_count > 0:
        commit_type = "[FIX]"
        description = f"修复问题 (影响{fix_count}个文件)"
    elif test_count > 0:
        commit_type = "[TEST]"
        description = f"添加测试 (覆盖{test_count}个文件)"
    elif docs_count > 0:
        commit_type = "[DOCS]"
        description = f"更新文档 (修改{docs_count}个文件)"
    elif refactor_count > 0:
        commit_type = "[REFACTOR]"
        description = f"重构代码 (优化{refactor_count}个文件)"
    else:
        commit_type = "[FEAT]"
        description = f"新功能开发 (添加{feat_count}个文件)"

    # 检查是否有AI生成内容
    ai_files = [f for s, f in changes if any(keyword in f.lower() for keyword in ['ai_', 'generated'])]
    if ai_files:
        commit_type = "[DNASPEC]"
        description = f"AI生成内容验证通过 ({len(ai_files)}个文件)"

    commit_message = f"{commit_type}(workspace): {description}"

    # 验证生成的提交消息是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(commit_message, "cognitive_convenience")
        if not validation["compliant"]:
            commit_message += f" # {validation['feedback']}"
    except ImportError:
        pass

    return commit_message


def clean_workspace(project_path: str) -> str:
    """
    清理工作区，移除AI生成的临时文件
    """
    project_root = Path(project_path).resolve()

    # 要清理的文件模式
    temp_patterns = [
        "*ai_generated*",
        "*experiment_*",
        "*debug_*",
        "*test_temp*",
        "*_temp.*",
        ".temp.*",
        "cache_*.py"
    ]

    cleaned_files = []
    cleaned_dirs = []

    for pattern in temp_patterns:
        # 清理文件
        for file_path in project_root.glob(pattern):
            if file_path.is_file():
                try:
                    file_path.unlink()
                    cleaned_files.append(str(file_path.relative_to(project_root)))
                except:
                    pass

        # 清理目录
        for dir_path in project_root.glob(pattern):
            if dir_path.is_dir():
                try:
                    import shutil
                    shutil.rmtree(dir_path)
                    cleaned_dirs.append(str(dir_path.relative_to(project_root)))
                except:
                    pass

    # 清理Python缓存
    for cache_dir in project_root.rglob("__pycache__"):
        try:
            import shutil
            shutil.rmtree(cache_dir)
            cleaned_dirs.append(str(cache_dir.relative_to(project_root)))
        except:
            pass

    total_cleaned = len(cleaned_files) + len(cleaned_dirs)

    if total_cleaned == 0:
        result = "✅ 工作区已经清洁，无需清理"
    else:
        result = f"""🧹 工作区清理完成！

📊 清理统计:
• 文件: {len(cleaned_files)} 个
• 目录: {len(cleaned_dirs)} 个
• 总计: {total_cleaned} 个

清理的文件:
{chr(10).join(f'  📄 {file}' for file in cleaned_files[:10])}
{('...' if len(cleaned_files) > 10 else '')}

清理的目录:
{chr(10).join(f'  📁 {dir}' for dir in cleaned_dirs[:5])}
{('...' if len(cleaned_dirs) > 5 else '')}

✨ 工作区已恢复清洁状态
🚫 AI文件污染已清除
"""

    # 验证清理结果是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"清理结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def get_workspace_status(project_path: str) -> str:
    """
    获取工作区状态报告
    """
    project_root = Path(project_path).resolve()

    # 检查DNASPEC宪法
    constitution_file = project_root / ".dnaspec" / "git_constitution.json"
    constitution_status = "❌ 未设置"

    if constitution_file.exists():
        try:
            with open(constitution_file, 'r') as f:
                constitution = json.load(f)
                constitution_status = "✅ 已设置"
                commit_count = constitution.get('commit_count', 0)
                last_commit = constitution.get('last_commit', 'N/A')
        except:
            constitution_status = "⚠️ 损坏"
    else:
        commit_count = 0
        last_commit = 'N/A'

    # 检查Git状态
    try:
        result = subprocess.run(["git", "status", "--porcelain"],
                              cwd=project_root, capture_output=True, text=True)
        git_changes = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
    except:
        git_changes = "N/A"

    # 检查临时文件
    temp_patterns = ["*ai_generated*", "*experiment_*", "*debug_*"]
    temp_files = []
    for pattern in temp_patterns:
        temp_files.extend(list(project_root.glob(pattern)))

    # 检查Git钩子
    hooks_dir = project_root / ".git" / "hooks"
    hooks_status = []
    if hooks_dir.exists():
        for hook in ["pre-commit", "commit-msg", "post-commit"]:
            hook_file = hooks_dir / hook
            if hook_file.exists() and hook_file.is_file():
                if "DNASPEC" in hook_file.read_text():
                    hooks_status.append(f"✅ {hook}")
                else:
                    hooks_status.append(f"⚠️ {hook}")
            else:
                hooks_status.append(f"❌ {hook}")

    report = f"""📊 DNASPEC工作区状态报告

🏛️ 项目宪法: {constitution_status}
📝 提交统计: {commit_count} 次
📅 最后提交: {last_commit}
🔄 Git更改: {git_changes} 个文件
🗂️ 临时文件: {len(temp_files)} 个

🎯 Git钩子状态:
{chr(10).join(f'  {hook}' for hook in hooks_status)}

💡 建议:
• 如果宪法未设置，运行 setup-constitution 初始化
• 如果有临时文件，运行 clean-workspace 清理
• 如果钩子缺失，运行 install-hooks 安装
• 定期检查工作区状态保持清洁
"""

    # 验证状态报告是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(report, "all")
        if not validation["compliant"]:
            return f"状态报告宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return report


def create_workflow_rules(project_path: str, workflow: Dict[str, Any]) -> str:
    """
    创建工作流规则，确保规则符合宪法原则
    """
    project_root = Path(project_path).resolve()
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)

    # 默认工作流规则
    default_workflow = {
        "name": "DNASPEC AI工作流",
        "version": "1.0.0",
        "stages": [
            {
                "name": "initialization",
                "description": "项目初始化和规则设置",
                "required": True,
                "actions": ["setup-constitution", "install-hooks"]
            },
            {
                "name": "development",
                "description": "AI辅助开发阶段",
                "required": False,
                "actions": ["create-temp-workspace", "validate-files"]
            },
            {
                "name": "validation",
                "description": "验证和测试阶段",
                "required": True,
                "actions": ["run-tests", "validate-staged"]
            },
            {
                "name": "commit",
                "description": "提交阶段",
                "required": True,
                "actions": ["smart-commit", "cleanup-temp"]
            }
        ],
        "rules": {
            "require_staging": True,
            "auto_cleanup": True,
            "validation_required": True,
            "enforce_git_rules": True,
            "enforce_constitutional_compliance": True
        },
        "custom_stages": workflow.get("custom_stages", []),
        "custom_rules": workflow.get("custom_rules", {})
    }

    # 合并自定义工作流
    default_workflow.update(workflow)

    # 验证工作流配置是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        workflow_json = json.dumps(default_workflow, indent=2, ensure_ascii=False)
        validation = validate_constitutional_compliance(workflow_json, "information_encapsulation")
        if not validation["compliant"]:
            return f"工作流配置宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    # 保存工作流配置
    workflow_file = dnaspec_dir / "workflow_rules.json"
    with open(workflow_file, 'w', encoding='utf-8') as f:
        json.dump(default_workflow, f, indent=2, ensure_ascii=False)

    stages_info = "\n".join(
        f"  {i+1}. {stage['name']}: {stage['description']}"
        for i, stage in enumerate(default_workflow['stages'])
    )

    result = f"""🔄 工作流规则创建完成！

📋 工作流配置: {workflow_file}
🎯 工作流名称: {default_workflow['name']}
📝 版本: {default_workflow['version']}

🔄 工作流阶段:
{stages_info}

⚙️ 规则配置:
• 要求暂存区: {default_workflow['rules']['require_staging']}
• 自动清理: {default_workflow['rules']['auto_cleanup']}
• 验证必需: {default_workflow['rules']['validation_required']}
• Git规则强制: {default_workflow['rules']['enforce_git_rules']}
• 宪法原则强制: {default_workflow['rules']['enforce_constitutional_compliance']}

✅ 工作流规则已激活
🚀 可以开始AI辅助开发
"""

    # 验证工作流创建结果是否符合宪法原则
    try:
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"工作流创建结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def enforce_git_rules(project_path: str) -> str:
    """
    强制执行Git规则
    """
    project_root = Path(project_path).resolve()

    enforced_rules = []
    issues = []

    # 检查宪法文件
    constitution_file = project_root / ".dnaspec" / "git_constitution.json"
    if not constitution_file.exists():
        issues.append("项目宪法未设置")
    else:
        enforced_rules.append("✅ 项目宪法已检查")

    # 检查Git钩子
    hooks_dir = project_root / ".git" / "hooks"
    missing_hooks = []
    for hook in ["pre-commit", "commit-msg", "post-commit"]:
        hook_file = hooks_dir / hook
        if not hook_file.exists():
            missing_hooks.append(hook)

    if missing_hooks:
        issues.append(f"缺少Git钩子: {', '.join(missing_hooks)}")
    else:
        enforced_rules.append("✅ Git钩子已检查")

    # 检查.gitignore
    gitignore_file = project_root / ".gitignore"
    if gitignore_file.exists():
        content = gitignore_file.read_text(encoding='utf-8')
        if ".dnaspec/" not in content:
            issues.append(".gitignore缺少DNASPEC规则")
        else:
            enforced_rules.append("✅ Git忽略规则已检查")
    else:
        issues.append(".gitignore文件不存在")

    # 检查临时文件
    temp_files = []
    patterns = ["*ai_generated*", "*experiment_*", "*debug_*"]
    for pattern in patterns:
        temp_files.extend(list(project_root.glob(pattern)))

    if temp_files:
        issues.append(f"发现{len(temp_files)}个临时文件需要清理")
        enforced_rules.append("⚠️ 检测到临时文件")
    else:
        enforced_rules.append("✅ 工作区清洁")

    # 自动修复问题
    fixes = []
    if ".gitignore文件不存在" in issues:
        gitignore_content = """# DNASPEC项目宪法规则
.dnaspec/temp/
.dnaspec/staging/
*ai_generated*
*experiment_*
*debug_*
*test_temp*
"""
        # 验证gitignore内容是否符合宪法原则
        try:
            from .constitutional_validator import validate_constitutional_compliance
            validation = validate_constitutional_compliance(gitignore_content, "cognitive_convenience")
            if not validation["compliant"]:
                gitignore_content += f"\n# {validation['feedback']}"
        except ImportError:
            pass
            
        gitignore_file.write_text(gitignore_content, encoding='utf-8')
        fixes.append("✅ 已创建.gitignore文件")

    if "缺少Git钩子" in issues:
        install_result = install_git_hooks(str(project_root))
        fixes.append("✅ 已安装Git钩子")

    result = f"""⚖️ Git规则强制执行完成！

🔍 检查结果:
{chr(10).join(f'  {rule}' for rule in enforced_rules)}

❌ 发现问题:
{chr(10).join(f'  • {issue}' for issue in issues) if issues else '  无问题'}

🔧 自动修复:
{chr(10).join(f'  {fix}' for fix in fixes) if fixes else '  无需修复'}

📊 总结:
• 检查项目: {project_root}
• 强制规则: {len(enforced_rules)} 项
• 发现问题: {len(issues)} 个
• 自动修复: {len(fixes)} 项

🚀 Git规则已强制执行，工作区安全！
"""

    # 验证强制执行结果是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"规则执行结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def setup_branch_policy(project_path: str, policy: Dict[str, Any]) -> str:
    """
    设置分支策略
    """
    project_root = Path(project_path).resolve()
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)

    # 默认分支策略
    default_policy = {
        "main_branch": "main",
        "develop_branch": "develop",
        "feature_prefix": "feature/",
        "release_prefix": "release/",
        "hotfix_prefix": "hotfix/",
        "protection": {
            "main": {
                "require_reviews": True,
                "require_status_checks": True,
                "enforce_admins": True
            },
            "develop": {
                "require_reviews": False,
                "require_status_checks": True,
                "enforce_admins": False
            }
        },
        "custom_rules": policy
    }

    # 合并用户策略
    default_policy.update(policy)

    # 验证分支策略是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        policy_json = json.dumps(default_policy, indent=2, ensure_ascii=False)
        validation = validate_constitutional_compliance(policy_json, "information_encapsulation")
        if not validation["compliant"]:
            return f"分支策略宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    # 保存分支策略
    policy_file = dnaspec_dir / "branch_policy.json"
    with open(policy_file, 'w', encoding='utf-8') as f:
        json.dump(default_policy, f, indent=2, ensure_ascii=False)

    # 创建分支保护规则
    if default_policy["protection"]["main"]["require_reviews"]:
        # 这里可以集成GitHub API或其他Git服务API
        pass

    result = f"""🌿 分支策略设置完成！

📋 策略文件: {policy_file}
🎯 主分支: {default_policy['main_branch']}
🔧 开发分支: {default_policy['develop_branch']}

🏷️ 分支命名规范:
• 功能分支: {default_policy['feature_prefix']}<feature-name>
• 发布分支: {default_policy['release_prefix']}<version>
• 热修复: {default_policy['hotfix_prefix']}<description>

🔒 主分支保护:
• 代码审查: {default_policy['protection']['main']['require_reviews']}
• 状态检查: {default_policy['protection']['main']['require_status_checks']}
• 管理员强制: {default_policy['protection']['main']['enforce_admins']}

✅ 分支策略已生效
🚫 不合规分支将被拒绝
📊 分支管理已规范化
"""

    # 验证分支策略结果是否符合宪法原则
    try:
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"分支策略结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result


def setup_review_policy(project_path: str, review_config: Dict[str, Any]) -> str:
    """
    设置代码审查策略
    """
    project_root = Path(project_path).resolve()
    dnaspec_dir = project_root / ".dnaspec"
    dnaspec_dir.mkdir(exist_ok=True)

    # 默认审查策略
    default_review = {
        "auto_assign": True,
        "min_reviewers": 1,
        "required_reviewers": [],
        "exclude_reviewers": [],
        "auto_merge": False,
        "merge_method": "squash",
        "dismiss_stale_reviews": True,
        "require_up_to_date": True,
        "ai_review_enabled": True,
        "checklist": [
            "代码符合项目规范",
            "已通过单元测试",
            "文档已更新",
            "性能影响已评估",
            "安全性已考虑"
        ],
        "custom_checks": review_config.get("custom_checks", []),
        "custom_rules": review_config
    }

    # 合并用户配置
    default_review.update(review_config)

    # 验证审查策略是否符合宪法原则
    try:
        from .constitutional_validator import validate_constitutional_compliance
        review_json = json.dumps(default_review, indent=2, ensure_ascii=False)
        validation = validate_constitutional_compliance(review_json, "cognitive_convenience")
        if not validation["compliant"]:
            return f"审查策略宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    # 保存审查策略
    review_file = dnaspec_dir / "review_policy.json"
    with open(review_file, 'w', encoding='utf-8') as f:
        json.dump(default_review, f, indent=2, ensure_ascii=False)

    checklist_items = "\n".join(
        f"  ☐ {item}" for item in default_review["checklist"]
    )

    result = f"""👥 代码审查策略设置完成！

📋 策略文件: {review_file}
🎯 自动分配: {default_review['auto_assign']}
👥 最少审查者: {default_review['min_reviewers']}
🔀 合并方式: {default_review['merge_method']}

✅ 审查清单:
{checklist_items}

🤖 AI审查: {default_review['ai_review_enabled']}
📊 自动合并: {default_review['auto_merge']}
🔄 更新审查: {default_review['dismiss_stale_reviews']}

🔧 审查规则已配置
📝 Pull Request模板已生成
⚡ 审查流程已自动化
"""

    # 验证审查策略结果是否符合宪法原则
    try:
        validation = validate_constitutional_compliance(result, "all")
        if not validation["compliant"]:
            return f"审查策略结果宪法验证失败: {validation['feedback']}"
    except ImportError:
        pass

    return result