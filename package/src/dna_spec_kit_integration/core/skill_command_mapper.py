#!/usr/bin/env python3
"""
DNASPEC 技能命令映射器
支持双重部署模式：标准化技能 + Slash命令
"""
import os
import json
import yaml
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from argparse import Namespace


@dataclass
class SkillCommand:
    """技能命令定义"""
    name: str
    description: str
    skill_path: Path
    category: str
    aliases: List[str]
    parameters: Dict[str, Any]
    examples: List[str]
    version: str = "1.0.0"


class SkillCommandMapper:
    """技能命令映射器 - 支持双重部署模式"""
    
    def __init__(self, skills_root: Path):
        """
        初始化映射器
        
        Args:
            skills_root: 技能根目录路径
        """
        self.skills_root = Path(skills_root)
        self.skills_commands: Dict[str, SkillCommand] = {}
        self.command_index: Dict[str, str] = {}  # alias -> skill_name 映射
        
    def scan_skills(self) -> Dict[str, SkillCommand]:
        """
        扫描技能目录并生成命令映射
        
        Returns:
            技能命令字典
        """
        if not self.skills_root.exists():
            return {}
            
        # 扫描所有技能目录
        for skill_dir in self.skills_root.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
                
            skill_file = skill_dir / "SKILL.md"
            if not skill_file.exists():
                continue
                
            try:
                # 解析 SKILL.md 文件
                skill_info = self._parse_skill_file(skill_file)
                if skill_info:
                    command = self._create_skill_command(skill_info, skill_dir)
                    self.skills_commands[command.name] = command
                    
                    # 建立别名映射
                    self.command_index[command.name] = command.name
                    for alias in command.aliases:
                        self.command_index[alias] = command.name
                        
            except Exception as e:
                print(f"Warning: Failed to parse skill {skill_dir.name}: {e}")
                
        return self.skills_commands
    
    def _parse_skill_file(self, skill_file: Path) -> Optional[Dict[str, Any]]:
        """
        解析 SKILL.md 文件
        
        Args:
            skill_file: SKILL.md 文件路径
            
        Returns:
            解析后的技能信息
        """
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 分离 YAML frontmatter 和 Markdown 内容
            if content.startswith('---'):
                # 提取 YAML frontmatter
                end_yaml = content.find('---', 3)
                if end_yaml != -1:
                    yaml_content = content[3:end_yaml].strip()
                    markdown_content = content[end_yaml + 3:].strip()
                else:
                    yaml_content = ""
                    markdown_content = content
            else:
                yaml_content = ""
                markdown_content = content
                
            # 解析 YAML frontmatter
            skill_info = {}
            if yaml_content:
                try:
                    skill_info = yaml.safe_load(yaml_content) or {}
                except yaml.YAMLError:
                    skill_info = {}
            
            # 解析 Markdown 内容中的示例
            examples = self._extract_examples(markdown_content)
            
            # 解析参数
            parameters = self._extract_parameters(markdown_content)
            
            # 合并信息
            skill_info.update({
                'examples': examples,
                'parameters': parameters,
                'content': markdown_content
            })
            
            return skill_info
            
        except Exception as e:
            print(f"Error parsing {skill_file}: {e}")
            return None
    
    def _extract_examples(self, markdown_content: str) -> List[str]:
        """
        从 Markdown 内容中提取示例
        
        Args:
            markdown_content: Markdown 内容
            
        Returns:
            示例列表
        """
        examples = []
        
        # 查找代码块中的示例
        code_blocks = re.findall(r'```[\s\S]*?```', markdown_content)
        for block in code_blocks:
            # 提取代码块内容
            lines = block.split('\n')[1:-1]  # 去掉 ``` 标记
            example = '\n'.join(lines).strip()
            if example:
                examples.append(example)
                
        # 查找 Usage 或 Examples 段落
        usage_patterns = [
            r'##?\s*(Usage|Examples?|使用|示例)[\s\S]*?(?=##|\Z)',
            r'###?\s*(Usage|Examples?|使用|示例)[\s\S]*?(?=##|\Z)'
        ]
        
        for pattern in usage_patterns:
            matches = re.findall(pattern, markdown_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                examples.append(match)
                
        return examples[:3]  # 限制示例数量
    
    def _extract_parameters(self, markdown_content: str) -> Dict[str, Any]:
        """
        从 Markdown 内容中提取参数信息
        
        Args:
            markdown_content: Markdown 内容
            
        Returns:
            参数字典
        """
        parameters = {}
        
        # 查找参数表格或列表
        param_patterns = [
            r'\|?\s*(参数|parameter|option)[\s\S]*?(?=\n\n|\n#|\Z)',
            r'(-{1,2}[\w-]+)[\s:]*([^|\n]*)',  # 命令行参数模式
        ]
        
        for pattern in param_patterns:
            matches = re.findall(pattern, markdown_content, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    param_name = match[0].strip().replace('-', '_')
                    param_desc = match[1].strip()
                    parameters[param_name] = {
                        'description': param_desc,
                        'type': 'string',
                        'required': False
                    }
                    
        return parameters
    
    def _create_skill_command(self, skill_info: Dict[str, Any], skill_dir: Path) -> SkillCommand:
        """
        创建技能命令对象
        
        Args:
            skill_info: 技能信息
            skill_dir: 技能目录
            
        Returns:
            技能命令对象
        """
        name = skill_info.get('name', skill_dir.name)
        description = skill_info.get('description', 'No description available')
        version = skill_info.get('version', '1.0.0')
        
        # 生成别名
        aliases = []
        if name:
            # 基础别名
            aliases.append(name)
            
            # 短名称
            if '-' in name:
                short_name = name.replace('-', '')
                aliases.append(short_name)
                
            # 下划线版本
            underscore_name = name.replace('-', '_')
            aliases.append(underscore_name)
            
        # 移除重复别名
        aliases = list(set(aliases))
        
        # 推断分类
        category = self._infer_category(name, description)
        
        return SkillCommand(
            name=name,
            description=description,
            skill_path=skill_dir,
            category=category,
            aliases=aliases,
            parameters=skill_info.get('parameters', {}),
            examples=skill_info.get('examples', []),
            version=version
        )
    
    def _infer_category(self, name: str, description: str) -> str:
        """
        推断技能分类
        
        Args:
            name: 技能名称
            description: 技能描述
            
        Returns:
            分类名称
        """
        text = f"{name} {description}".lower()
        
        # 分类关键词映射
        category_keywords = {
            'architecture': ['architect', 'design', 'system', '架构', '设计'],
            'analysis': ['analyzer', 'analysis', 'context', '分析', '评估'],
            'optimization': ['optimizer', 'optimize', '优化', '改进'],
            'creation': ['creator', 'generate', '创建', '生成'],
            'management': ['manager', 'git', 'deploy', '管理', '部署'],
            'template': ['template', 'cognitive', '模板', '认知'],
            'decomposition': ['decomposer', 'task', '分解', '任务']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in text for keyword in keywords):
                return category
                
        return 'general'
    
    def get_command(self, command_name: str) -> Optional[SkillCommand]:
        """
        获取指定命令
        
        Args:
            command_name: 命令名称
            
        Returns:
            技能命令对象
        """
        # 直接查找
        if command_name in self.skills_commands:
            return self.skills_commands[command_name]
            
        # 通过别名查找
        if command_name in self.command_index:
            skill_name = self.command_index[command_name]
            return self.skills_commands.get(skill_name)
            
        return None
    
    def list_commands(self, category: Optional[str] = None) -> List[SkillCommand]:
        """
        列出所有命令
        
        Args:
            category: 可选的分类过滤
            
        Returns:
            命令列表
        """
        commands = list(self.skills_commands.values())
        
        if category:
            commands = [cmd for cmd in commands if cmd.category == category]
            
        return sorted(commands, key=lambda x: x.name)
    
    def get_categories(self) -> List[str]:
        """
        获取所有分类
        
        Returns:
            分类列表
        """
        categories = set(cmd.category for cmd in self.skills_commands.values())
        return sorted(categories)
    
    def export_manifest(self, output_path: Path) -> bool:
        """
        导出技能清单文件
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            是否成功
        """
        try:
            manifest = {
                'version': '1.0.0',
                'name': 'DNASPEC Skills',
                'description': 'DNASPEC Context Engineering Skills - Dual Deployment Compatible',
                'deployment_modes': ['standard', 'slash_command'],
                'commands': {}
            }
            
            for skill_name, command in self.skills_commands.items():
                command_dict = asdict(command)
                # 转换WindowsPath为字符串
                command_dict['skill_path'] = str(command.skill_path)
                manifest['commands'][skill_name] = command_dict
                
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)
                
            return True
            
        except Exception as e:
            print(f"Error exporting manifest: {e}")
            return False
    
    def generate_cli_integration(self, output_dir: Path) -> bool:
        """
        生成 CLI 集成文件
        
        Args:
            output_dir: 输出目录
            
        Returns:
            是否成功
        """
        try:
            # 生成命令注册文件
            commands_content = self._generate_commands_py()
            (output_dir / "commands.py").write_text(commands_content, encoding='utf-8')
            
            # 生成配置文件
            config_content = self._generate_config_yaml()
            (output_dir / "skills_config.yaml").write_text(config_content, encoding='utf-8')
            
            # 生成安装脚本
            install_content = self._generate_install_sh()
            (output_dir / "install_skills.sh").write_text(install_content, encoding='utf-8')
            
            return True
            
        except Exception as e:
            print(f"Error generating CLI integration: {e}")
            return False
    
    def _generate_commands_py(self) -> str:
        """生成 Python 命令文件"""
        commands = []
        for skill_name, command in self.skills_commands.items():
            param_docs = []
            for param_name, param_info in command.parameters.items():
                required = "required" if param_info.get('required') else "optional"
                param_docs.append(f"        {param_name}: {param_info.get('description', '')} ({required})")
            
            commands.append(f'''
def {skill_name.replace('-', '_')}(**kwargs):
    """{command.description}
    
    Args:
{chr(10).join(param_docs) if param_docs else "        No parameters"}
    """
    # Skill execution logic here
    return {{
        "skill": "{skill_name}",
        "result": "Skill executed successfully",
        "parameters": kwargs
    }}
''')
        
        return f'''#!/usr/bin/env python3
"""
DNASPEC Skills Commands
Auto-generated command functions
"""

{''.join(commands)}
'''
    
    def _generate_config_yaml(self) -> str:
        """生成 YAML 配置文件"""
        commands_data = {}
        for skill_name, command in self.skills_commands.items():
            commands_data[skill_name] = {
                'description': command.description,
                'category': command.category,
                'aliases': command.aliases,
                'version': command.version
            }
        
        return f'''# DNASPEC Skills Configuration
version: "1.0.0"
name: "DNASPEC Skills"
description: "DNASPEC Context Engineering Skills - Dual Deployment Compatible"

deployment_modes:
  - standard: "Copy skill directories to .claude/skills/"
  - slash_command: "Register as CLI commands"

commands:
{json.dumps(commands_data, ensure_ascii=False, indent=2).replace('"', "'").replace('{', '').replace('}', '').replace(',', '').replace(':', ': ')}
'''
    
    def _generate_install_sh(self) -> str:
        """生成安装脚本"""
        return '''#!/bin/bash
# DNASPEC Skills Installation Script

set -e

echo "🚀 Installing DNASPEC Skills..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "⚠️  Not in a git repository. Some features may not work."
fi

# Create .claude/skills directory if it doesn't exist
mkdir -p .claude/skills

# Copy skills to Claude directory
echo "📁 Copying skills to .claude/skills/..."
cp -r skills/* .claude/skills/

# Install CLI commands (if supported)
if command -v dnaspec >/dev/null 2>&1; then
    echo "🔧 Registering CLI commands..."
    # CLI registration logic would go here
fi

echo "✅ DNASPEC Skills installation completed!"
echo ""
echo "Usage:"
echo "  Claude Code: Skills will be automatically discovered"
echo "  CLI: Use 'dnaspec <skill-name>' commands"
echo ""
'''


# CLI 集成函数
def create_dual_deployment_system(skills_root: Path, output_dir: Path) -> Dict[str, Any]:
    """
    创建双重部署系统
    
    Args:
        skills_root: 技能根目录
        output_dir: 输出目录
        
    Returns:
        部署结果信息
    """
    mapper = SkillCommandMapper(skills_root)
    
    # 扫描技能
    print("🔍 Scanning skills...")
    commands = mapper.scan_skills()
    print(f"📋 Found {len(commands)} skills")
    
    if not commands:
        return {
            "success": False,
            "error": "No valid skills found",
            "commands_count": 0
        }
    
    # 生成 CLI 集成
    print("⚙️  Generating CLI integration...")
    cli_success = mapper.generate_cli_integration(output_dir)
    
    # 导出清单
    print("📄 Exporting skill manifest...")
    manifest_path = output_dir / "skills_manifest.json"
    manifest_success = mapper.export_manifest(manifest_path)
    
    # 生成使用指南
    print("📖 Generating usage guide...")
    guide_path = output_dir / "usage_guide.md"
    generate_usage_guide(mapper, guide_path)
    
    return {
        "success": cli_success and manifest_success,
        "commands_count": len(commands),
        "categories": mapper.get_categories(),
        "output_files": [
            str(output_dir / "commands.py"),
            str(output_dir / "skills_config.yaml"),
            str(output_dir / "install_skills.sh"),
            str(manifest_path),
            str(guide_path)
        ]
    }


def generate_usage_guide(mapper: SkillCommandMapper, guide_path: Path):
    """生成使用指南"""
    categories = mapper.get_categories()
    
    guide_content = f"""# DNASPEC Skills 使用指南

## 双重部署模式

DNASPEC 技能系统支持两种部署模式，可以同时使用：

### 1. 标准化部署 (Claude Code)
```bash
# 复制技能目录到 Claude Code
cp -r skills/* .claude/skills/
```

### 2. Slash 命令部署 (CLI)
```bash
# 注册 CLI 命令
dnaspec <skill-name> [参数]
```

## 可用技能

"""
    
    for category in categories:
        guide_content += f"### {category.title()}\n\n"
        commands = mapper.list_commands(category)
        
        for cmd in commands:
            guide_content += f"**{cmd.name}**\n"
            guide_content += f"- 描述: {cmd.description}\n"
            if cmd.aliases:
                guide_content += f"- 别名: {', '.join(cmd.aliases)}\n"
            guide_content += f"- 版本: {cmd.version}\n\n"
            
            if cmd.examples:
                guide_content += "**示例:**\n"
                for example in cmd.examples[:2]:  # 限制示例数量
                    guide_content += f"```\n{example}\n```\n"
                guide_content += "\n"
    
    guide_content += """
## 使用示例

### Claude Code 模式
在 Claude Code 中直接使用技能：
```
我需要分析这段代码的质量
[Claude Code 会自动选择 context-analyzer 技能]
```

### CLI 模式
使用命令行调用技能：
```bash
# 分析上下文质量
dnaspec context-analyzer --input "要分析的文本"

# 创建 AI 代理
dnaspec agent-creator --agent_description "数据分析专家" --capabilities "python,sql,visualization"
```
"""
    
    guide_path.write_text(guide_content, encoding='utf-8')


if __name__ == "__main__":
    # 测试运行
    skills_root = Path("../skills")
    output_dir = Path("../dual_deployment")
    
    if skills_root.exists():
        result = create_dual_deployment_system(skills_root, output_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Skills root not found: {skills_root}")