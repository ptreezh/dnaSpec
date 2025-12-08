"""
DNASPEC Specification Engine - 核心规范引擎
结合spec.kit的理念，实现规范驱动的上下文工程技能系统
"""
from typing import Dict, Any, List, Optional
import yaml
import json
from jinja2 import Template
from pathlib import Path
import importlib
import os


class DSGSSpecEngine:
    """
    DSGS规范引擎
    基于spec.kit理念实现的规范驱动技能系统
    """
    
    def __init__(self):
        self.spec_parser = SpecParser()
        self.skill_compiler = SkillCompiler()
        self.skill_registry = SkillRegistry()
        self.hook_system = None
    
    def register_skill_from_spec(self, spec_path: str) -> bool:
        """
        从规范文件注册技能
        """
        try:
            # 解析规范
            spec = self.spec_parser.parse(spec_path)
            
            # 验证规范
            if not self.spec_parser.validate(spec):
                raise ValueError(f"Invalid specification: {spec_path}")
            
            # 编译技能
            skill_instance = self.skill_compiler.compile(spec)
            
            # 注册技能
            success = self.skill_registry.register(skill_instance)
            
            return success
        except Exception as e:
            print(f"Failed to register skill from {spec_path}: {str(e)}")
            return False
    
    def execute_skill(self, skill_name: str, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行技能
        """
        if params is None:
            params = {}
        
        # 从注册表获取技能
        skill = self.skill_registry.get_skill(skill_name)
        if not skill:
            return {
                'success': False,
                'error': f'Skill not found: {skill_name}',
                'available_skills': list(self.skill_registry.skills.keys())
            }
        
        # 使用技能处理请求
        try:
            result = skill.process_request(context, params)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': f'Skill execution failed: {str(e)}',
                'skill_name': skill_name
            }
    
    def list_available_skills(self) -> Dict[str, str]:
        """
        列出所有可用技能
        """
        return self.skill_registry.list_skills()
    
    def load_all_specs_from_directory(self, specs_dir: str) -> int:
        """
        从目录加载所有规范文件
        """
        specs_dir = Path(specs_dir)
        spec_files = list(specs_dir.glob("*.spec.*"))  # 匹配所有.spec.*文件
        
        loaded_count = 0
        for spec_file in spec_files:
            try:
                if self.register_skill_from_spec(str(spec_file)):
                    loaded_count += 1
                    print(f"Loaded spec: {spec_file.name}")
                else:
                    print(f"Failed to load spec: {spec_file.name}")
            except Exception as e:
                print(f"Error loading spec {spec_file.name}: {str(e)}")
        
        print(f"Loaded {loaded_count} skills from {len(spec_files)} spec files")
        return loaded_count


class SpecParser:
    """
    规范解析器
    解析spec.kit风格的规范文件
    """
    
    def parse(self, spec_path: str) -> Dict[str, Any]:
        """
        解析规范文件
        支持YAML、JSON、MD格式
        """
        with open(spec_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if spec_path.endswith('.yaml') or spec_path.endswith('.yml'):
            return yaml.safe_load(content)
        elif spec_path.endswith('.json'):
            return json.loads(content)
        elif spec_path.endswith('.md'):
            return self._parse_markdown_spec(content)
        else:
            raise ValueError(f"Unsupported spec format: {spec_path}")
    
    def _parse_markdown_spec(self, content: str) -> Dict[str, Any]:
        """
        解析Markdown格式的规范
        提取spec.kit风格的YAML frontmatter
        """
        lines = content.split('\n')
        if lines and lines[0].strip() == '---':
            # 查找YAML frontmatter
            yaml_end_idx = -1
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == '---':
                    yaml_end_idx = i
                    break
            
            if yaml_end_idx > 0:
                yaml_content = '\n'.join(lines[1:yaml_end_idx])
                return yaml.safe_load(yaml_content)
        
        # 如果没有frontmatter，尝试查找spec代码块
        import re
        spec_pattern = r'```(?:yaml|json)\n(.*?)\n```'
        matches = re.findall(spec_pattern, content, re.DOTALL)
        if matches:
            # 假设第一个代码块是规范
            first_match = matches[0]
            if first_match.strip().startswith('{'):
                return json.loads(first_match)
            else:
                return yaml.safe_load(first_match)
        
        raise ValueError("No valid spec found in markdown content")
    
    def validate(self, spec: Dict[str, Any]) -> bool:
        """
        验证规范格式
        """
        required_fields = ['name', 'description', 'version', 'implementation']
        for field in required_fields:
            if field not in spec:
                raise ValueError(f"Spec missing required field: {field}")
        
        if not isinstance(spec['name'], str):
            raise ValueError("Spec name must be a string")
        
        if not isinstance(spec['implementation'], dict):
            raise ValueError("Spec implementation must be a dictionary")
        
        # 检查实现部分
        implementation = spec['implementation']
        if 'instruction_template' not in implementation:
            raise ValueError("Spec implementation must contain 'instruction_template'")
        
        return True


class SkillCompiler:
    """
    技能编译器
    将规范编译为可执行的技能实例
    """
    
    def compile(self, spec: Dict[str, Any]) -> 'DNASpecSkill':
        """
        将规范编译为技能实例
        """
        # 验证规范
        if not self._validate_spec(spec):
            raise ValueError("Invalid spec format")
        
        # 动态创建技能类
        skill_class = self._generate_skill_class(spec)
        
        # 返回技能实例
        return skill_class()
    
    def _validate_spec(self, spec: Dict[str, Any]) -> bool:
        """
        验证规范格式
        """
        required_sections = ['name', 'implementation']
        for section in required_sections:
            if section not in spec:
                return False
        
        impl = spec['implementation']
        required_impl = ['instruction_template']
        for req in required_impl:
            if req not in impl:
                return False
        
        return True
    
    def _generate_skill_class(self, spec: Dict[str, Any]) -> type:
        """
        动态生成技能类
        """
        from src.dnaspec_spec_kit_integration.core.skill import DNASpecSkill
        import os
        import sys
        
        class_name = f"{spec['name'].replace('-', '_').title()}Skill"
        
        # 从规范创建执行方法
        def __init__(self):
            DNASpecSkill.__init__(self, spec['name'], spec['description'])
        
        def process_request(self, request: str, params: Dict[str, Any]) -> Dict[str, Any]:
            """
            处理请求 - 使用AI模型执行任务
            """
            # 使用Jinja2模板处理指令
            template_content = spec['implementation']['instruction_template']
            template = Template(template_content)
            
            # 准备渲染上下文
            render_context = params.copy() if params else {}
            render_context['context'] = request  # 请求内容
            
            # 渲染AI指令
            try:
                ai_instruction = template.render(render_context)
            except Exception as e:
                return {
                    'success': False,
                    'error': f'Template rendering error: {str(e)}',
                    'raw_request': request
                }
            
            # 调用AI模型 - 在实际实现中，这里会调用AI API
            ai_response = self._call_ai_model(ai_instruction, spec.get('ai_model', 'default'))
            
            # 如果有结果处理器，应用它
            processor_script = spec['implementation'].get('result_processor', '')
            if processor_script:
                try:
                    # 在安全环境中执行处理器脚本
                    result = self._execute_processor_script(
                        processor_script, 
                        ai_response, 
                        render_context
                    )
                except Exception as e:
                    result = {
                        'raw_response': ai_response,
                        'error_processing': str(e),
                        'original_response': ai_response
                    }
            else:
                # 如果没有处理器，直接返回AI响应
                result = {
                    'raw_response': ai_response,
                    'processed_context': request
                }
            
            return {
                'success': True,
                'result': result,
                'skill_name': spec['name'],
                'execution_time': 0.0,  # 实际系统中会记录执行时间
                'input_context': request[:100]  # 记录输入上下文的简短摘要
            }
        
        def _call_ai_model(self, instruction: str, model: str = 'default') -> str:
            """
            调用AI模型
            在实际实现中，这里会连接到真正的AI API
            """
            # 模拟AI调用 - 真实实现中会使用Anthropic、OpenAI或其他API
            import time
            time.sleep(0.05)  # 模拟延迟
            
            # 模拟AI响应
            return f"[AI RESPONSE] Processed: {instruction[:100]}..."
        
        def _execute_processor_script(self, script: str, response: str, context: Dict[str, Any]) -> Any:
            """
            执行结果处理脚本
            """
            # 创建安全的执行环境
            local_vars = {
                'response': response,
                'context': context,
                'result': None
            }
            
            try:
                # 执行处理脚本
                exec(script, {}, local_vars)
                return local_vars.get('result', {'raw_response': response})
            except Exception as e:
                return {
                    'error': f'Processor script failed: {str(e)}', 
                    'raw_response': response
                }
        
        # 使用type()动态创建类
        skill_class = type(class_name, (DNASpecSkill,), {
            '__init__': __init__,
            'process_request': process_request,
            '_call_ai_model': _call_ai_model,
            '_execute_processor_script': _execute_processor_script
        })
        
        return skill_class


class SkillRegistry:
    """
    技能注册表
    管理所有已注册的技能
    """
    
    def __init__(self):
        self.skills: Dict[str, 'DNASpecSkill'] = {}
    
    def register(self, skill: 'DNASpecSkill') -> bool:
        """
        注册技能
        """
        if skill.name in self.skills:
            return False  # 技能已存在
        
        self.skills[skill.name] = skill
        return True
    
    def get_skill(self, skill_name: str) -> Optional['DNASpecSkill']:
        """
        获取技能实例
        """
        return self.skills.get(skill_name)
    
    def execute_skill(self, skill_name: str, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行技能
        """
        skill = self.get_skill(skill_name)
        if not skill:
            return {
                'success': False,
                'error': f'Skill not found: {skill_name}',
                'available_skills': list(self.skills.keys())
            }
        
        try:
            return skill.process_request(context, params)
        except Exception as e:
            return {
                'success': False,
                'error': f'Skill execution error: {str(e)}',
                'skill_name': skill_name
            }
    
    def list_skills(self) -> Dict[str, str]:
        """
        列出所有注册的技能
        """
        return {name: skill.description for name, skill in self.skills.items()}


# 全局规范引擎实例
engine = DSGSSpecEngine()

# 初始化时加载默认规范
def initialize_engine():
    """
    初始化引擎 - 加载默认技能规范
    """
    global engine
    
    # 检查specs目录并加载规范文件
    specs_dir = os.path.join(os.path.dirname(__file__), '..', 'specs')
    if os.path.exists(specs_dir):
        loaded_count = engine.load_all_specs_from_directory(specs_dir)
        print(f"DNASPEC Spec Engine initialized with {loaded_count} skills")
    else:
        print("Warning: Specs directory not found, please ensure specs/ directory exists with specification files")


# 自动初始化引擎
initialize_engine()


def get_available_skills() -> Dict[str, str]:
    """
    获取可用技能列表
    """
    return engine.list_available_skills()


def execute_skill(skill_name: str, context: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    执行技能的便捷函数
    """
    return engine.execute_skill(skill_name, context, params)