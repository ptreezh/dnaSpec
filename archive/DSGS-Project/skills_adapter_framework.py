#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DNASPEC Skills 通用适配器框架
用于将DNASPEC Skills集成到不同的AI工具中
"""

import os
import json
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import yaml

@dataclass
class SkillDefinition:
    """技能定义数据类"""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "DNASPEC System"
    license: str = "MIT"
    keywords: List[str] = None
    dependencies: List[str] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.dependencies is None:
            self.dependencies = []

class BaseAdapter(ABC):
    """基础适配器抽象类"""
    
    def __init__(self, skills_base_path: str = "skills"):
        self.skills_base_path = skills_base_path
        self.skills = self._load_skills()
    
    def _load_skills(self) -> Dict[str, SkillDefinition]:
        """从skills目录加载所有技能定义"""
        skills = {}
        if not os.path.exists(self.skills_base_path):
            return skills
        
        for skill_dir in os.listdir(self.skills_base_path):
            skill_path = os.path.join(self.skills_base_path, skill_dir)
            if os.path.isdir(skill_path):
                skill_def = self._parse_skill_definition(skill_dir, skill_path)
                if skill_def:
                    skills[skill_def.name] = skill_def
        return skills
    
    def _parse_skill_definition(self, skill_dir: str, skill_path: str) -> Optional[SkillDefinition]:
        """解析技能定义文件"""
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            return None
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析YAML前言
            if content.startswith('---'):
                lines = content.split('\n')
                yaml_lines = []
                
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        # 解析YAML内容
                        yaml_content = '\n'.join(yaml_lines)
                        yaml_data = yaml.safe_load(yaml_content)
                        
                        if yaml_data and 'name' in yaml_data and 'description' in yaml_data:
                            # 提取关键词 - 从描述中提取
                            desc = yaml_data.get('description', '')
                            keywords = self._extract_keywords_from_description(desc)
                            
                            return SkillDefinition(
                                name=yaml_data['name'],
                                description=yaml_data['description'],
                                keywords=keywords
                            )
                        break
                    elif i < 20:  # 限制YAML前言长度
                        yaml_lines.append(line)
                    else:
                        break
        except Exception as e:
            print(f"解析技能定义失败 {skill_md_path}: {e}")
        
        return None
    
    def _extract_keywords_from_description(self, description: str) -> List[str]:
        """从描述中提取关键词"""
        keywords = []
        # 提取描述中的关键短语
        trigger_phrases = ['当用户提到', '当用户需要', '用于', '支持']
        for phrase in trigger_phrases:
            if phrase in description:
                # 简单提取关键词
                parts = description.split(phrase)
                if len(parts) > 1:
                    following_text = parts[1].split('时')[0] if '时' in parts[1] else parts[1]
                    # 提取中文关键词
                    import re
                    chinese_keywords = re.findall(r'[\u4e00-\u9fff]+', following_text)
                    keywords.extend([k for k in chinese_keywords if len(k) > 1])
        
        # 添加英文关键词
        import re
        english_keywords = re.findall(r'[a-zA-Z]+', description.lower())
        keywords.extend([k for k in english_keywords if len(k) > 2])
        
        return list(set(keywords))  # 去重
    
    @abstractmethod
    def export_for_target(self, target: str) -> str:
        """导出为特定目标格式"""
        pass

class ClaudeCodeAdapter(BaseAdapter):
    """Claude Code适配器"""
    
    def export_for_target(self, target: str = "claude_skills") -> str:
        """导出为Claude Code Skills格式"""
        export_path = f"exports/claude_code_skills"
        os.makedirs(export_path, exist_ok=True)
        
        for skill_name, skill_def in self.skills.items():
            # 为每个技能创建目录和SKILL.md文件
            skill_dir = os.path.join(export_path, skill_name)
            os.makedirs(skill_dir, exist_ok=True)
            
            # 复制原始SKILL.md文件
            original_skill_path = os.path.join(self.skills_base_path, skill_name, "SKILL.md")
            if os.path.exists(original_skill_path):
                import shutil
                shutil.copy2(original_skill_path, os.path.join(skill_dir, "SKILL.md"))
                
                # 添加Claude特定的元数据
                with open(os.path.join(skill_dir, "SKILL.md"), 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 确保包含必要的字段
                if not content.startswith('---'):
                    # 如果没有YAML前言，添加一个
                    updated_content = f"""---
name: {skill_def.name}
description: {skill_def.description}
---

{content}"""
                    
                    with open(os.path.join(skill_dir, "SKILL.md"), 'w', encoding='utf-8') as f:
                        f.write(updated_content)
        
        return export_path

class GeminiCLIAdapter(BaseAdapter):
    """Gemini CLI适配器"""
    
    def export_for_target(self, target: str = "gemini_extensions") -> str:
        """导出为Gemini CLI Extensions格式"""
        export_path = f"exports/gemini_extensions"
        os.makedirs(export_path, exist_ok=True)
        
        # 创建扩展配置文件
        extensions_config = {
            "version": "1.0",
            "extensions": []
        }
        
        for skill_name, skill_def in self.skills.items():
            extension_config = {
                "name": skill_name,
                "description": skill_def.description,
                "version": skill_def.version,
                "author": skill_def.author,
                "license": skill_def.license,
                "playbook": {
                    "instructions": f"当用户请求与{skill_def.description}相关的内容时，使用此扩展。",
                    "triggers": skill_def.keywords,
                    "capabilities": ["context_management", "tool_execution"]
                },
                "mcp_servers": [],
                "context_files": [f"{skill_name}/GEMINI.md"]
            }
            
            extensions_config["extensions"].append(extension_config)
            
            # 创建扩展目录
            ext_dir = os.path.join(export_path, skill_name)
            os.makedirs(ext_dir, exist_ok=True)
            
            # 创建GEMINI.md上下文文件
            gemini_md_content = f"""# {skill_def.name} 扩展

## 功能描述
{skill_def.description}

## 使用场景
- {skill_def.description}

## 关键词触发
{', '.join(skill_def.keywords)}

## 指令示例
- "请使用{skill_def.name}进行处理"
- "我需要{skill_def.name}的帮助"
"""
            
            with open(os.path.join(ext_dir, "GEMINI.md"), 'w', encoding='utf-8') as f:
                f.write(gemini_md_content)
        
        # 保存扩展配置
        with open(os.path.join(export_path, "extensions.json"), 'w', encoding='utf-8') as f:
            json.dump(extensions_config, f, ensure_ascii=False, indent=2)
        
        return export_path

class QwenCLIAdapter(BaseAdapter):
    """Qwen CLI适配器"""
    
    def export_for_target(self, target: str = "qwen_plugins") -> str:
        """导出为Qwen CLI插件格式"""
        export_path = f"exports/qwen_plugins"
        os.makedirs(export_path, exist_ok=True)
        
        # 创建插件配置
        plugins_config = {
            "version": "1.0",
            "plugins": []
        }
        
        for skill_name, skill_def in self.skills.items():
            plugin_config = {
                "name": skill_name,
                "description": skill_def.description,
                "version": skill_def.version,
                "author": skill_def.author,
                "license": skill_def.license,
                "tools": [
                    {
                        "name": f"{skill_name}_tool",
                        "description": f"用于执行{skill_def.name}功能的工具",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "request": {
                                    "type": "string",
                                    "description": "用户请求的具体内容"
                                }
                            },
                            "required": ["request"]
                        }
                    }
                ],
                "instructions": f"当用户请求与{skill_def.description}相关的内容时，使用此插件。",
                "keywords": skill_def.keywords
            }
            
            plugins_config["plugins"].append(plugin_config)
            
            # 创建插件目录和配置文件
            plugin_dir = os.path.join(export_path, skill_name)
            os.makedirs(plugin_dir, exist_ok=True)
            
            # 创建插件配置文件
            with open(os.path.join(plugin_dir, "plugin.json"), 'w', encoding='utf-8') as f:
                json.dump(plugin_config, f, ensure_ascii=False, indent=2)
            
            # 创建插件说明文件
            readme_content = f"""# {skill_def.name} 插件

## 描述
{skill_def.description}

## 功能
- {skill_def.description}

## 触发关键词
- {', '.join(skill_def.keywords)}

## 使用方法
当用户输入包含上述关键词的请求时，系统会自动调用此插件。
"""
            
            with open(os.path.join(plugin_dir, "README.md"), 'w', encoding='utf-8') as f:
                f.write(readme_content)
        
        # 保存插件配置
        with open(os.path.join(export_path, "plugins.json"), 'w', encoding='utf-8') as f:
            json.dump(plugins_config, f, ensure_ascii=False, indent=2)
        
        return export_path

class DNASPECSkillsAdapterFramework:
    """DNASPEC Skills适配器框架"""
    
    def __init__(self, skills_base_path: str = "skills"):
        self.skills_base_path = skills_base_path
        self.adapters = {
            "claude": ClaudeCodeAdapter(skills_base_path),
            "gemini": GeminiCLIAdapter(skills_base_path),
            "qwen": QwenCLIAdapter(skills_base_path)
        }
    
    def get_adapter(self, target: str) -> BaseAdapter:
        """获取指定目标的适配器"""
        target_lower = target.lower()
        if "claude" in target_lower:
            return self.adapters["claude"]
        elif "gemini" in target_lower:
            return self.adapters["gemini"]
        elif "qwen" in target_lower:
            return self.adapters["qwen"]
        else:
            raise ValueError(f"不支持的目标: {target}. 支持: claude, gemini, qwen")
    
    def export_all(self) -> Dict[str, str]:
        """导出所有目标格式"""
        results = {}
        
        for target, adapter in self.adapters.items():
            try:
                export_path = adapter.export_for_target(target)
                results[target] = export_path
                print(f"✓ {target} 格式导出完成: {export_path}")
            except Exception as e:
                print(f"✗ {target} 格式导出失败: {e}")
        
        return results
    
    def export_for_target(self, target: str) -> str:
        """为特定目标导出"""
        adapter = self.get_adapter(target)
        return adapter.export_for_target(target)

def main():
    """主函数 - 演示适配器框架的使用"""
    print("=== DNASPEC Skills 适配器框架 ===\n")
    
    # 创建适配器框架
    framework = DNASPECSkillsAdapterFramework("skills")
    
    print("可用的适配器:")
    for target in framework.adapters.keys():
        print(f"  - {target}")
    
    print("\n开始导出所有格式...")
    results = framework.export_all()
    
    print(f"\n导出完成! 结果:")
    for target, path in results.items():
        print(f"  {target}: {path}")
    
    print(f"\n集成说明:")
    print(f"  Claude Code: 将 {results.get('claude', 'exports/claude_code_skills')} 目录中的技能复制到 ~/.config/claude/skills/")
    print(f"  Gemini CLI: 将 {results.get('gemini', 'exports/gemini_extensions')} 目录中的扩展安装到 Gemini CLI")
    print(f"  Qwen CLI: 将 {results.get('qwen', 'exports/qwen_plugins')} 目录中的插件安装到 Qwen CLI")

if __name__ == "__main__":
    main()