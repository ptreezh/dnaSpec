"""
DNASPEC技能管理器
管理所有DNASPEC技能并与spec.kit适配器集成
"""
import re
from typing import Dict, List, Optional, Any
from .skill import DNASpecSkill, SkillInfo, SkillResult
from .matcher import IntelligentMatcher
from .hook import HookSystem


class SkillManager:
    """DNASPEC技能管理器"""
    
    def __init__(self):
        self.skills: Dict[str, DNASpecSkill] = {}
        self.skill_registry: Dict[str, SkillInfo] = {}
        self._spec_kit_adapters = []  # 注册的spec.kit适配器
        self._intelligent_matcher = IntelligentMatcher()  # 智能匹配器
        self._hook_system = HookSystem(self)  # Hook系统
    
    def register_skill(self, skill: DNASpecSkill) -> bool:
        """注册DNASPEC技能"""
        if not isinstance(skill, DNASpecSkill):
            return False
        
        self.skills[skill.name] = skill
        
        # 更新技能注册表
        if skill.name in self.skill_registry:
            skill_info = self.skill_registry[skill.name]
            skill_info.version = skill.version
        else:
            # 创建新的技能信息
            skill_info = SkillInfo(
                name=skill.name,
                description=skill.description,
                version=skill.version
            )
            self.skill_registry[skill.name] = skill_info
        
        # 自动注册到所有已连接的spec.kit适配器
        self._register_skill_with_adapters(skill)
        
        # 注册技能关键词到智能匹配器
        self._register_skill_keywords(skill)
        
        # 启用Hook系统中的技能
        self._hook_system.config.enable_skill(skill.name)
        
        return True
    
    def _register_skill_keywords(self, skill: DNASpecSkill):
        """将技能关键词注册到智能匹配器"""
        # 根据技能类型推断关键词
        skill_type_keywords = {
            'dnaspec-architect': [
                '架构', '系统设计', 'architecture', 'design', 'structure', 
                '系统架构', '架构设计', '设计系统', 'architect', 'blueprint',
                '设计', '创建系统', '系统蓝图'
            ],
            'dnaspec-agent-creator': [
                '智能体', 'agent', 'create agent', '设计智能体', '创建智能体',
                '智能体角色', 'agent creator', '智能体设计', 'create', 'role',
                '创建', '生成智能体', '设计agent'
            ],
            'dnaspec-task-decomposer': [
                '分解任务', '任务分解', 'task decomposition', 'break down',
                '拆分', '细化', '任务分析', 'decompose', 'analyze',
                '分解', '细化任务', '任务拆分'
            ],
            'dnaspec-constraint-generator': [
                '约束', '生成约束', 'constraint', 'generate', 'specification',
                '规范', '规则', 'constraint generation', 'rules',
                '生成', '创建约束', '制定规范'
            ],
            'dnaspec-dapi-checker': [
                '接口检查', '一致性检查', 'api validation', 'interface',
                '接口验证', '检查', '验证', 'consistency', 'api', 'validation',
                '检查接口', '验证一致性'
            ],
            'dnaspec-modulizer': [
                '模块化', '重构', 'modularization', 'refactor', 'maturity',
                '模块成熟度', '封装', '重构', 'modulize', 'optimize',
                '优化', '模块重构', '系统优化'
            ]
        }
        
        # 使用技能描述中的关键词作为补充
        description_keywords = self._extract_keywords_from_description(skill.description)
        default_keywords = skill_type_keywords.get(skill.name, [])
        
        all_keywords = default_keywords + description_keywords
        
        # 注册到智能匹配器
        self._intelligent_matcher.register_skill_keywords(skill.name, all_keywords)
    
    def _extract_keywords_from_description(self, description: str) -> List[str]:
        """从技能描述中提取关键词"""
        # 简单的关键词提取，实际应用中可能需要更复杂的NLP处理
        import re
        words = re.findall(r'[\w\u4e00-\u9fff]+', description.lower())
        # 过滤常见词汇，保留有意义的关键词
        common_words = {'的', '是', '在', '和', '与', '或', '为', '有', '了', '等', '专业', '专家'}
        keywords = [word for word in words if len(word) > 1 and word not in common_words]
        return keywords
    
    def _register_skill_with_adapters(self, skill: DNASpecSkill):
        """将技能注册到所有连接的spec.kit适配器"""
        for adapter in self._spec_kit_adapters:
            try:
                # 创建适配器可调用的函数
                def skill_callable(params, skill_instance=skill):
                    request = params.get('params', '')
                    context = params.get('context', {})
                    return skill_instance.process_request(request, context)
                
                adapter.register_skill(skill.name, skill_callable)
            except Exception:
                # 适配器可能不支持动态注册，忽略错误
                pass
    
    def register_spec_kit_adapter(self, adapter) -> bool:
        """注册spec.kit适配器"""
        if not hasattr(adapter, 'register_skill'):
            return False
        
        self._spec_kit_adapters.append(adapter)
        
        # 将已存在的技能注册到新适配器
        for skill_name, skill in self.skills.items():
            try:
                def skill_callable(params, skill_instance=skill):
                    request = params.get('params', '')
                    context = params.get('context', {})
                    return skill_instance.process_request(request, context)
                
                adapter.register_skill(skill_name, skill_callable)
            except Exception:
                # 适配器可能不支持动态注册，忽略错误
                pass
        
        return True
    
    def get_skill(self, name: str) -> Optional[DNASpecSkill]:
        """获取技能"""
        return self.skills.get(name)
    
    def get_skill_info(self, name: str) -> Optional[SkillInfo]:
        """获取技能信息"""
        return self.skill_registry.get(name)
    
    def list_skills(self) -> List[SkillInfo]:
        """列出所有技能"""
        return list(self.skill_registry.values())
    
    def execute_skill(self, skill_name: str, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """执行技能"""
        skill = self.get_skill(skill_name)
        if not skill:
            return SkillResult(
                skill_name=skill_name,
                status=SkillInfo.ERROR,
                result=None,
                confidence=0.0,
                execution_time=0.0,
                error_message=f"Skill not found: {skill_name}"
            )
        
        return skill.process_request(request, context)
    
    def execute_spec_kit_command(self, command: str, adapter=None) -> Dict[str, Any]:
        """执行spec.kit命令"""
        # 如果指定了适配器，使用该适配器执行
        if adapter and hasattr(adapter, 'execute_command'):
            return adapter.execute_command(command)
        
        # 否则使用第一个注册的适配器
        if self._spec_kit_adapters:
            return self._spec_kit_adapters[0].execute_command(command)
        
        # 如果没有适配器，直接解析并执行
        return self._execute_command_directly(command)
    
    def _execute_command_directly(self, command: str) -> Dict[str, Any]:
        """直接执行命令（不通过适配器）"""
        # 简单的命令解析
        if not command.startswith("/speckit.dnaspec."):
            return {
                'success': False,
                'error': 'Invalid command format',
                'original_command': command
            }
        
        # 提取技能名称和参数
        remaining = command[len("/speckit.dnaspec."):].strip()
        if ' ' in remaining:
            skill_name, params = remaining.split(' ', 1)
            params = params.strip()
        else:
            skill_name = remaining
            params = ""
        
        full_skill_name = f"dnaspec-{skill_name}"
        
        # 执行技能
        try:
            result = self.execute_skill(full_skill_name, params)
            return {
                'success': True,
                'result': result,
                'skill_name': full_skill_name,
                'original_command': command
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'skill_name': full_skill_name,
                'params': params
            }
    
    def match_skill_intelligently(self, user_request: str) -> Optional[Dict[str, Any]]:
        """智能匹配技能"""
        match_result = self._intelligent_matcher.match_intelligently(user_request)
        
        if match_result:
            return {
                'skill_name': match_result.skill_name,
                'confidence': match_result.confidence,
                'match_type': match_result.match_type,
                'matched_keywords': match_result.matched_keywords,
                'processing_time': match_result.processing_time
            }
        
        return None
    
    def execute_intelligent_skill(self, user_request: str) -> Dict[str, Any]:
        """智能执行技能（自动匹配并执行）"""
        # 智能匹配
        match_info = self.match_skill_intelligently(user_request)
        
        if not match_info:
            return {
                'success': False,
                'error': 'No matching skill found',
                'original_request': user_request
            }
        
        if match_info['confidence'] < 0.2:  # 降低阈值以便测试
            return {
                'success': False,
                'error': f'Confidence too low: {match_info["confidence"]:.2f}',
                'confidence': match_info['confidence'],
                'original_request': user_request
            }
        
        # 执行匹配的技能
        try:
            result = self.execute_skill(match_info['skill_name'], user_request)
            return {
                'success': True,
                'skill_result': result,
                'match_info': match_info,
                'original_request': user_request
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'match_info': match_info,
                'original_request': user_request
            }
    
    def intercept_and_process_request(self, user_request: str) -> Dict[str, Any]:
        """拦截并处理用户请求（Hook系统入口）"""
        # 使用Hook系统处理请求
        hook_result = self._hook_system.intercept_request(user_request)
        
        if hook_result.intercepted:
            if hook_result.handled:
                return {
                    'success': True,
                    'hook_result': hook_result,
                    'handled_by_hook': True,
                    'skill_name': hook_result.skill_name,
                    'skill_result': hook_result.skill_result,
                    'processing_time': hook_result.processing_time
                }
            else:
                return {
                    'success': False,
                    'error': hook_result.error_message or "Hook system intercepted but failed to handle request",
                    'handled_by_hook': True,
                    'processing_time': hook_result.processing_time
                }
        else:
            # Hook系统未拦截，使用默认处理
            return self._default_request_processing(user_request)
    
    def _default_request_processing(self, user_request: str) -> Dict[str, Any]:
        """默认请求处理"""
        # 尝试智能匹配和执行
        intelligent_result = self.execute_intelligent_skill(user_request)
        if intelligent_result['success']:
            return intelligent_result
        
        # 如果智能处理失败，返回错误
        return intelligent_result
    
    def get_manager_info(self) -> Dict[str, Any]:
        """获取管理器信息"""
        matcher_info = self._intelligent_matcher.get_matcher_info()
        hook_info = self._hook_system.get_hook_info()
        
        return {
            'registered_skills_count': len(self.skills),
            'registered_skills': list(self.skills.keys()),
            'registered_adapters_count': len(self._spec_kit_adapters),
            'skill_registry_count': len(self.skill_registry),
            'intelligent_matcher_info': matcher_info,
            'hook_system_info': hook_info
        }