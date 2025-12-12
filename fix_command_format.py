#!/usr/bin/env python3
"""
DNASPEC命令格式统一修复脚本
将所有斜杠命令统一为 /dnaspec.* 格式
"""
import os
import re
from pathlib import Path

def fix_command_format_in_file(file_path: Path) -> int:
    """修复单个文件中的命令格式"""
    if not file_path.exists():
        return 0

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_count = 0

        # 1. 替换 /speckit.dnaspec.* 为 /dnaspec.*
        speckit_pattern = r'/speckit\.dnaspec\.([^\'"\s\)]+)'
        content = re.sub(speckit_pattern, r'/dnaspec.\1', content)
        changes_count += len(re.findall(speckit_pattern, original_content))

        # 2. 替换 /dnaspec-([^ \s\'"]+) 为 /dnaspec.\1
        dash_pattern = r'/dnaspec-([^ \s\'"]+)'
        content = re.sub(dash_pattern, r'/dnaspec.\1', content)
        changes_count += len(re.findall(dash_pattern, original_content))

        # 3. 替换 dnaspec-([^ \s\'"]+) 为 /dnaspec.\1 (在需要斜杠的地方)
        # 这个需要更谨慎，只在特定上下文中替换
        dnaspec_no_slash_pattern = r'(["\`])dnaspec-([^ "\`]+)\1'
        content = re.sub(dnaspec_no_slash_pattern, r'\1/dnaspec.\2\1', content)
        changes_count += len(re.findall(dnaspec_no_slash_pattern, original_content))

        # 4. 替换使用示例中的命令
        usage_patterns = [
            (r'command:[\'"]\s*/speckit\.dnaspec\.([^\'"]+)[\'"]', r'command: "/dnaspec.\1"'),
            (r'usage:[\'"]\s*/speckit\.dnaspec\.([^\'"]+)[\'"]', r'usage: "/dnaspec.\1"'),
            (r'example:[\'"]\s*/speckit\.dnaspec\.([^\'"]+)[\'"]', r'example: "/dnaspec.\1"'),
        ]

        for pattern, replacement in usage_patterns:
            matches = re.findall(pattern, original_content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_count += len(matches)

        # 5. 修复技能名称中的格式
        skill_name_patterns = [
            (r'name["\']?\s*:\s*["\']speckit\.dnaspec\.([^"\']+)["\']', r'name: "dnaspec.\1"'),
            (r'skill["\']?\s*:\s*["\']speckit\.dnaspec\.([^"\']+)["\']', r'skill: "dnaspec.\1"'),
        ]

        for pattern, replacement in skill_name_patterns:
            matches = re.findall(pattern, original_content)
            if matches:
                content = re.sub(pattern, replacement, content)
                changes_count += len(matches)

        # 如果有更改，写回文件
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  ✅ Fixed {changes_count} command formats in {file_path.name}")
            return changes_count

    except Exception as e:
        print(f"  ❌ Error processing {file_path}: {e}")
        return 0

    return 0

def create_standard_command_mapping():
    """创建标准命令映射"""
    return {
        # 上下文工程技能
        '/dnaspec.context-analysis': {
            'description': 'Analyze context quality across 5 dimensions',
            'aliases': ['/dnaspec.analyze', '/dnaspec.analysis']
        },
        '/dnaspec.context-optimization': {
            'description': 'Optimize context quality with AI-driven improvements',
            'aliases': ['/dnaspec.optimize', '/dnaspec.optimization']
        },
        '/dnaspec.cognitive-template': {
            'description': 'Apply cognitive frameworks to structure complex tasks',
            'aliases': ['/dnaspec.template', '/dnaspec.cognitive']
        },

        # 架构设计技能
        '/dnaspec.architect': {
            'description': 'Design system architecture and components',
            'aliases': ['/dnaspec.system-architect', '/dnaspec.design']
        },
        '/dnaspec.task-decomposer': {
            'description': 'Decompose complex tasks into manageable subtasks',
            'aliases': ['/dnaspec.decompose', '/dnaspec.breakdown']
        },
        '/dnaspec.agent-creator': {
            'description': 'Create intelligent agents with specific capabilities',
            'aliases': ['/dnaspec.create-agent', '/dnaspec.agent']
        },

        # 开发辅助技能
        '/dnaspec.git-operations': {
            'description': 'Execute Git workflow operations safely',
            'aliases': ['/dnaspec.git', '/dnaspec.git-skill']
        },
        '/dnaspec.temp-workspace': {
            'description': 'Manage AI-generated files in secure workspace',
            'aliases': ['/dnaspec.temp', '/dnaspec.workspace']
        },
        '/dnaspec.cache-manager': {
            'description': 'Manage caching and file optimization',
            'aliases': ['/dnaspec.cache', '/dnaspec.manage-cache']
        },

        # 系统技能
        '/dnaspec.constraint-generator': {
            'description': 'Generate system constraints from requirements',
            'aliases': ['/dnaspec.constraints', '/dnaspec.generate-constraints']
        },
        '/dnaspec.dapi-checker': {
            'description': 'Check API design consistency and quality',
            'aliases': ['/dnaspec.api-check', '/dnaspec.check-api']
        },
        '/dnaspec.modulizer': {
            'description': 'Modularize system design into components',
            'aliases': ['/dnaspec.modularize', '/dnaspec.modules']
        },

        # 工具技能
        '/dnaspec.examples': {
            'description': 'Show usage examples for DNASPEC skills',
            'aliases': ['/dnaspec.help', '/dnaspec.usage']
        },
        '/dnaspec.liveness': {
            'description': 'Check system health and status',
            'aliases': ['/dnaspec.status', '/dnaspec.health']
        },
        '/dnaspec.version': {
            'description': 'Show DNASPEC version information',
            'aliases': ['/dnaspec.info', '/dnaspec.about']
        }
    }

def generate_command_reference():
    """生成统一的命令参考文档"""
    mapping = create_standard_command_mapping()

    reference_content = """# DNASPEC 统一命令参考

## 命令格式标准

所有DNASPEC斜杠命令使用统一格式：**/dnaspec.***

### 基本语法
```
/dnaspec.<skill-name> [arguments] [options]
```

## 核心技能命令

### 🔍 上下文分析
```
/dnaspec.context-analysis "要分析的上下文内容"
```
**别名**: `/dnaspec.analyze`, `/dnaspec.analysis`

### ⚡ 上下文优化
```
/dnaspec.context-optimization "要优化的上下文" --goals clarity,completeness
```
**别名**: `/dnaspec.optimize`, `/dnaspec.optimization`

### 🧠 认知模板
```
/dnaspec.cognitive-template "任务描述" --template chain_of_thought
```
**别名**: `/dnaspec.template`, `/dnaspec.cognitive`

### 🏗️ 系统架构
```
/dnaspec.architect "系统需求描述" --constraints high_performance,scalable
```
**别名**: `/dnaspec.system-architect`, `/dnaspec.design`

### 🔧 Git操作
```
/dnaspec.git-operations operation=status
/dnaspec.git-operations operation=commit message="feat: 添加新功能"
```
**别名**: `/dnaspec.git`, `/dnaspec.git-skill`

### 📁 临时工作区
```
/dnaspec.temp-workspace operation=create
/dnaspec.temp-workspace operation=add-file file_path=example.py content="代码内容"
```
**别名**: `/dnaspec.temp`, `/dnaspec.workspace`

## 高级技能命令

### 📋 任务分解
```
/dnaspec.task-decomposer "复杂任务描述"
```

### 🤖 智能体创建
```
/dnaspec.agent-creator "智能体需求" capabilities=analysis,coding
```

### ⚖️ 约束生成
```
/dnaspec.constraint-generator "系统需求" type=performance
```

### 🔌 API检查
```
/dnaspec.dapi-checker "API设计文档"
```

### 🧩 模块化
```
/dnaspec.modulizer "系统设计方案"
```

## 工具命令

### 📖 使用示例
```
/dnaspec.examples
/dnaspec.examples context-analysis
```

### 💡 系统状态
```
/dnaspec.liveness
```

### ℹ️ 版本信息
```
/dnaspec.version
```

## 使用选项

### 通用选项
- `--verbose` - 显示详细输出
- `--quiet` - 静默模式
- `--help` - 显示帮助信息

### 上下文分析选项
- `--mode enhanced` - 增强分析模式
- `--include-suggestions` - 包含改进建议

### 上下文优化选项
- `--goals <list>` - 优化目标 (clarity,completeness,relevance,consistency,efficiency)
- `--budget <tokens>` - Token预算限制

### 认知模板选项
- `--template <type>` - 模板类型:
  - `chain_of_thought` - 思维链推理
  - `few_shot` - 少示例学习
  - `verification` - 验证检查
  - `role_playing` - 角色扮演
  - `understanding` - 深度理解

### 系统架构选项
- `--style <type>` - 架构风格 (microservices,monolithic,event_driven)
- `--constraints <list>` - 约束条件 (performance,security,scalability)

### Git操作选项
- `operation <type>` - 操作类型:
  - `status` - 查看状态
  - `add <files>` - 添加文件
  - `commit -m <message>` - 提交
  - `push` - 推送
  - `pull` - 拉取
  - `branch <name>` - 分支管理

### 临时工作区选项
- `operation <type>` - 操作类型:
  - `create` - 创建工作区
  - `add-file` - 添加文件
  - `list-files` - 列出文件
  - `clean` - 清理工作区

## 示例用例

### 1. 分析需求文档
```
/dnaspec.context-analysis "设计一个用户认证系统，支持注册、登录、密码重置功能，要求高安全性和良好的用户体验"
```

### 2. 优化提示词
```
/dnaspec.context-optimization "帮我写代码" --goals clarity,completeness
```

### 3. 应用验证模板
```
/dnaspec.cognitive-template "审查这个系统架构设计" --template verification
```

### 4. 设计电商系统
```
/dnaspec.architect "电商平台，支持用户管理、商品管理、订单处理、支付功能" --style microservices
```

### 5. 安全的Git操作
```
# 查看状态
/dnaspec.git-operations operation=status

# 提交已验证的文件
/dnaspec.git-operations operation=commit message="feat: 添加用户认证模块"
```

### 6. 管理AI生成文件
```
# 创建临时工作区
/dnaspec.temp-workspace operation=create

# 添加AI生成的代码
/dnaspec.temp-workspace operation=add-file file_path=auth.py content="import hashlib..."

# 查看临时文件
/dnaspec.temp-workspace operation=list-files
```

---

💡 **提示**: 所有命令都支持别名，可以选择最方便的格式使用。
🔒 **安全**: 请遵循安全工作流，仅在验证后将文件移至工作区。
"""

    return reference_content

def main():
    """主修复函数"""
    print("🔧 DNASPEC Command Format Unification Tool")
    print("=" * 50)

    project_root = Path.cwd()
    src_dir = project_root / 'src'

    if not src_dir.exists():
        print("❌ src directory not found. Please run from project root.")
        return 1

    # 文件类型匹配模式
    file_patterns = [
        '**/*.py',     # Python文件
        '**/*.js',     # JavaScript文件
        '**/*.md',     # Markdown文件
        '**/*.json',   # JSON配置文件
        '**/*.yaml',   # YAML配置文件
        '**/*.yml',    # YAML配置文件
        '**/*.txt',    # 文本文件
    ]

    total_changes = 0
    processed_files = 0

    print("\n🔍 Scanning for command format issues...")

    # 扫描并修复所有相关文件
    for pattern in file_patterns:
        for file_path in src_dir.glob(pattern):
            if file_path.is_file():
                changes = fix_command_format_in_file(file_path)
                if changes > 0:
                    total_changes += changes
                processed_files += 1

    print(f"\n📊 Summary:")
    print(f"  Files processed: {processed_files}")
    print(f"  Total fixes: {total_changes}")

    # 生成命令参考文档
    print("\n📚 Generating unified command reference...")
    reference_content = generate_command_reference()
    reference_file = project_root / 'DNASPEC_COMMAND_REFERENCE.md'

    with open(reference_file, 'w', encoding='utf-8') as f:
        f.write(reference_content)

    print(f"✅ Command reference saved to: {reference_file}")

    # 创建标准命令映射文件
    mapping = create_standard_command_mapping()
    mapping_file = project_root / '.dnaspec' / 'command_mapping.json'
    mapping_file.parent.mkdir(exist_ok=True)

    import json
    with open(mapping_file, 'w', encoding='utf-8') as f:
        json.dump(mapping, f, ensure_ascii=False, indent=2)

    print(f"✅ Command mapping saved to: {mapping_file}")

    if total_changes > 0:
        print(f"\n🎉 Successfully unified {total_changes} command formats to /dnaspec.*")
        print("\n📋 Next steps:")
        print("1. Review the generated command reference")
        print("2. Test the unified commands in your AI CLI tools")
        print("3. Update any custom scripts to use the new format")
    else:
        print("\n✅ No command format issues found!")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())