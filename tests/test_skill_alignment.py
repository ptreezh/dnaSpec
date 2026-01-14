"""
TDD测试案例：DNASPEC技能对齐Claude标准
基于Test-Driven Development方法验证技能格式对齐
"""

import unittest
import json
import yaml
import os
from pathlib import Path
import re

class TestDNASPECAlignment(unittest.TestCase):
    """DNASPEC技能与Claude标准对齐的测试案例"""
    
    def setUp(self):
        """测试初始化"""
        self.project_root = Path(__file__).parent.parent
        self.skills_config_path = self.project_root / ".dnaspec" / "cli_extensions" / "claude" / "dnaspec_skills.json"
        self.skills_dir = self.project_root / "skills"
        
    def test_skill_directory_structure_exists(self):
        """测试：技能目录结构是否存在"""
        # 验证主技能目录存在
        self.assertTrue(self.skills_dir.exists(), "技能目录不存在")
        
        # 验证每个技能都有独立目录
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_dir = self.skills_dir / skill_name
                self.assertTrue(skill_dir.exists(), f"技能目录 {skill_name} 不存在")
    
    def test_skill_md_files_exist(self):
        """测试：每个技能是否有SKILL.md文件"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_md_path = self.skills_dir / skill_name / "SKILL.md"
                self.assertTrue(skill_md_path.exists(), f"SKILL.md文件不存在: {skill_name}")
    
    def test_skill_yaml_frontmatter(self):
        """测试：SKILL.md文件是否包含正确的YAML frontmatter"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_md_path = self.skills_dir / skill_name / "SKILL.md"
                
                if skill_md_path.exists():
                    with open(skill_md_path, 'r', encoding='utf-8') as md_file:
                        content = md_file.read()
                        
                    # 验证YAML frontmatter存在
                    self.assertTrue(content.startswith('---'), f"{skill_name}: 缺少YAML frontmatter")
                    
                    # 提取frontmatter内容
                    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                    self.assertTrue(frontmatter_match, f"{skill_name}: 无法解析YAML frontmatter")
                    
                    # 验证必需字段
                    try:
                        frontmatter_data = yaml.safe_load(frontmatter_match.group(1))
                        self.assertIn('name', frontmatter_data, f"{skill_name}: 缺少name字段")
                        self.assertIn('description', frontmatter_data, f"{skill_name}: 缺少description字段")
                    except yaml.YAMLError as e:
                        self.fail(f"{skill_name}: YAML格式错误: {e}")
    
    def test_skill_description_quality(self):
        """测试：技能描述质量是否符合标准"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_md_path = self.skills_dir / skill_name / "SKILL.md"
                
                if skill_md_path.exists():
                    with open(skill_md_path, 'r', encoding='utf-8') as md_file:
                        content = md_file.read()
                        
                    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                    if frontmatter_match:
                        try:
                            frontmatter_data = yaml.safe_load(frontmatter_match.group(1))
                            description = frontmatter_data.get('description', '')
                            
                            # 验证描述质量
                            self.assertGreater(len(description), 10, f"{skill_name}: 描述过短")
                            self.assertLess(len(description), 300, f"{skill_name}: 描述过长")
                            
                            # 验证包含使用时机说明
                            self.assertTrue(
                                any(keyword in description.lower() for keyword in ['when', 'how', 'use', '用于', '如何']),
                                f"{skill_name}: 描述应包含使用时机说明"
                            )
                        except yaml.YAMLError:
                            pass
    
    def test_progressive_disclosure_structure(self):
        """测试：渐进式披露结构"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_dir = self.skills_dir / skill_name
                
                if skill_dir.exists():
                    # 验证主要结构元素
                    skill_md_path = skill_dir / "SKILL.md"
                    if skill_md_path.exists():
                        with open(skill_md_path, 'r', encoding='utf-8') as md_file:
                            content = md_file.read()
                            
                        # 移除frontmatter后的内容
                        main_content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
                        
                        # 验证包含关键章节
                        required_sections = ['工作流程', '使用方法', '关键决策点']
                        for section in required_sections:
                            self.assertIn(section, main_content, f"{skill_name}: 缺少关键章节 '{section}'")
                        
                        # 验证内容长度合理（不超过1500 tokens约1000个中文字符）
                        self.assertLess(len(main_content), 1500, f"{skill_name}: 核心指令过长")
    
    def test_resource_organization(self):
        """测试：资源组织结构"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            for skill in config.get('skills', []):
                skill_name = skill.get('name', '').replace('dnaspec-', '')
                skill_dir = self.skills_dir / skill_name
                
                if skill_dir.exists():
                    # 验证可选的子目录结构
                    optional_dirs = ['examples', 'tools', 'resources', 'reference']
                    found_dirs = [d for d in optional_dirs if (skill_dir / d).exists()]
                    
                    # 如果有子目录，验证命名规范
                    for dir_name in found_dirs:
                        dir_path = skill_dir / dir_name
                        self.assertTrue(dir_path.is_dir(), f"{skill_name}: {dir_name} 不是有效目录")
                        
                        # 验证文件命名规范
                        for file_path in dir_path.glob('*.md'):
                            self.assertTrue(
                                re.match(r'^[a-z0-9\-_]+\.md$', file_path.name.lower()),
                                f"{skill_name}: 文件名不符合规范 {file_path.name}"
                            )
    
    def test_backward_compatibility(self):
        """测试：向后兼容性"""
        # 验证原有JSON配置仍然有效
        if self.skills_config_path.exists():
            try:
                with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 验证必需的顶级字段
                required_fields = ['version', 'name', 'description', 'skills']
                for field in required_fields:
                    self.assertIn(field, config, f"缺少必需字段: {field}")
                    
                # 验证技能对象结构
                for skill in config.get('skills', []):
                    required_skill_fields = ['name', 'description', 'category', 'command']
                    for field in required_skill_fields:
                        self.assertIn(field, skill, f"技能缺少必需字段: {field}")
                        
            except json.JSONDecodeError as e:
                self.fail(f"JSON配置文件格式错误: {e}")
    
    def test_command_consistency(self):
        """测试：命令一致性"""
        if self.skills_config_path.exists():
            with open(self.skills_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            commands = []
            for skill in config.get('skills', []):
                command = skill.get('command', '')
                self.assertTrue(command.startswith('/'), f"{skill.get('name')}: 命令必须以/开头")
                self.assertTrue(
                    'dnaspec' in command.lower(),
                    f"{skill.get('name')}: 命令应包含dnaspec标识"
                )
                commands.append(command)
                
            # 验证命令唯一性
            self.assertEqual(len(commands), len(set(commands)), "存在重复的命令")


class TestSkillExecution(unittest.TestCase):
    """技能执行测试"""
    
    def setUp(self):
        """测试初始化"""
        self.project_root = Path(__file__).parent.parent
        self.skills_dir = self.project_root / "skills"
    
    def test_skill_loading_simulation(self):
        """测试：技能加载模拟"""
        # 模拟Claude发现和加载技能的过程
        if not self.skills_dir.exists():
            self.skipTest("技能目录不存在")
            
        skill_dirs = [d for d in self.skills_dir.iterdir() if d.is_dir()]
        self.assertGreater(len(skill_dirs), 0, "没有找到技能目录")
        
        for skill_dir in skill_dirs:
            skill_md_path = skill_dir / "SKILL.md"
            if skill_md_path.exists():
                # 模拟读取frontmatter
                with open(skill_md_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
                if frontmatter_match:
                    try:
                        frontmatter = yaml.safe_load(frontmatter_match.group(1))
                        self.assertIsInstance(frontmatter, dict)
                        self.assertIn('name', frontmatter)
                        self.assertIn('description', frontmatter)
                    except yaml.YAMLError:
                        self.fail(f"无法解析技能 {skill_dir.name} 的frontmatter")


if __name__ == '__main__':
    # 运行测试
    unittest.main(verbosity=2)