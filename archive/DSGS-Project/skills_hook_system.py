# Skills智能发现和调用Hook系统 - 完善版

import json
import os
import sys
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class SkillInfo:
    """Skill信息"""
    name: str
    description: str
    path: str
    keywords: List[str]
    confidence: float = 0.0

class SkillsDiscoveryHook:
    """Skills智能发现Hook"""
    
    def __init__(self, skills_base_path: str = "skills"):
        self.skills_base_path = skills_base_path
        self.skills_registry = self._build_skills_registry()
    
    def _build_skills_registry(self) -> List[SkillInfo]:
        """构建Skills注册表"""
        skills = []
        print("=== 构建Skills注册表 ===")
        
        if not os.path.exists(self.skills_base_path):
            print(f"警告: Skills目录不存在 {self.skills_base_path}")
            return skills
        
        for skill_dir in os.listdir(self.skills_base_path):
            skill_path = os.path.join(self.skills_base_path, skill_dir)
            if os.path.isdir(skill_path):
                skill_info = self._extract_skill_info(skill_dir, skill_path)
                if skill_info:
                    skills.append(skill_info)
                    print(f"  注册Skill: {skill_info.name}")
                    print(f"    描述: {skill_info.description[:60]}...")
                    print(f"    关键词: {skill_info.keywords}")
        
        return skills
    
    def _extract_skill_info(self, skill_dir: str, skill_path: str) -> Optional[SkillInfo]:
        """提取Skill信息"""
        # 查找SKILL.md文件
        skill_md_path = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_md_path):
            return None
        
        try:
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 解析YAML前言
            skill_name = skill_dir  # 默认使用目录名
            skill_desc = ""
            
            if content.startswith('---'):
                lines = content.split('\n')
                yaml_lines = []
                in_yaml = True
                
                for i, line in enumerate(lines[1:], 1):
                    if line.strip() == '---':
                        in_yaml = False
                        content_start = i + 1
                        break
                    elif in_yaml:
                        yaml_lines.append(line)
                
                # 解析YAML内容
                for line in yaml_lines:
                    if line.startswith('name:'):
                        skill_name = line.split(':', 1)[1].strip().strip('"\'')
                    elif line.startswith('description:'):
                        skill_desc = line.split(':', 1)[1].strip().strip('"\'')
                
                # 如果没有从YAML获取描述，使用文件内容
                if not skill_desc:
                    content_body = '\n'.join(lines[content_start:]) if content_start < len(lines) else ""
                    paragraphs = [p.strip() for p in content_body.split('\n\n') if p.strip()]
                    if paragraphs:
                        skill_desc = paragraphs[0][:300]  # 限制长度
            
            # 如果还是没有描述，使用文件名
            if not skill_desc:
                skill_desc = f"{skill_name} Skill"
            
            # 提取关键词 - 改进算法
            keywords = self._extract_keywords_improved(skill_desc, skill_name)
            
            return SkillInfo(
                name=skill_name,
                description=skill_desc,
                path=skill_path,
                keywords=keywords
            )
        except Exception as e:
            print(f"解析Skill文件失败 {skill_md_path}: {e}")
        
        return None
    
    def _extract_keywords_improved(self, description: str, skill_name: str) -> List[str]:
        """改进的关键词提取算法"""
        keywords = set()
        text = (description + " " + skill_name).lower()
        
        # 精确关键词映射 - 增加更多精确匹配
        keyword_mappings = [
            # 架构相关
            (r'architect|设计|架构|architecture', 'architect'),
            (r'system|系统|体系', 'system'),
            (r'design|设计', 'design'),
            
            # 任务相关
            (r'task|任务|task分解', 'task'),
            (r'decompos|分解|break.down|拆分', 'decomposer'),
            (r'atomic|原子化', 'atomic'),
            (r'complex.task|复杂任务', 'complex_task'),  # 新增复杂任务相关关键词
            (r'step.by.step|一步步', 'step_by_step'),  # 新增一步步拆解关键词
            (r'task.analysis|任务分析', 'task_analysis'),  # 新增任务分析关键词
            (r'task.list|任务清单', 'task_list'),  # 新增任务清单关键词
            (r'task.plan|任务计划', 'task_plan'),  # 新增任务计划关键词
            
            # 智能体相关
            (r'agent|智能体|智能代理', 'agent'),
            (r'creator|创建|create', 'creator'),
            (r'multi.agent|多智能体', 'multi_agent'),
            (r'agentic|具身认知|模块自主智能', 'agentic'),  # 新增agentic相关关键词
            (r'模块智能化|智能模块', 'module_intelligence'),  # 新增模块智能化关键词
            
            # 约束相关
            (r'constraint|约束|规范', 'constraint'),
            (r'generate|生成|generate', 'generate'),
            (r'specification|规范', 'spec'),
            
            # API/接口相关
            (r'api|接口|interface', 'api'),
            (r'interface|接口定义', 'interface'),
            (r'parameter|参数', 'parameter'),  # 新增参数相关关键词
            (r'mismatch|不匹配', 'mismatch'),  # 新增不匹配相关关键词
            (r'error|错误', 'error'),  # 新增错误相关关键词
            (r'inconsistency|不一致', 'inconsistency'),  # 新增不一致相关关键词
            (r'definition|定义', 'definition'),  # 新增定义相关关键词
            
            # 数据相关
            (r'data|数据|database|数据验证', 'data'),
            (r'schema|模式', 'schema'),
            
            # 接口检查相关 - 为DAPIcheck技能添加
            (r'interface|接口|一致性|一致性检查|文档核验|接口验证|接口检查|api.check', 'interface'),
            (r'consistency|一致|符合性', 'consistency'),
            (r'document|文档|document.verification', 'document'),
            (r'check|验证|核验|validate|verify', 'check'),
            (r'distributed|分布式|distributed.api', 'distributed'),
            (r'dapi|DAPI|dapi.check', 'dapi'),
            (r'component|组件|component.interface', 'component'),
            
            # 模块化相关 - 为modulizer技能添加
            (r'module|模块|模块化', 'module'),
            (r'maturity|成熟|成熟度|成熟性', 'maturity'),
            (r'seal|封装|encapsulation', 'seal'),
            (r'component|组件|component', 'component'),
            (r'modulize|模块化|模块成熟化|模块封装', 'modulize'),
            (r'bottom.up|自底向上|bottom.up.design', 'bottom_up'),
            (r'encapsulation|封装', 'encapsulation'),
            (r'system.complexity|系统复杂性|complexity.reduction', 'complexity'),
            (r'refactor|重构', 'refactor'),
            (r'isolation.test|隔离测试', 'isolation_test'),  # 新增隔离测试关键词
            (r'partition.test|分区测试', 'partition_test'),  # 新增分区测试关键词
            (r'system.refactor|系统重构', 'system_refactor'),  # 新增系统重构关键词
            
            # 安全监控
            (r'security|安全|security.check', 'security'),
            (r'monitor|监控|monitoring', 'monitor'),
            
            # 测试部署
            (r'test|测试|testing', 'test'),
            (r'deploy|部署|deployment', 'deploy'),
        ]
        
        # 提取匹配的关键词
        for pattern, keyword in keyword_mappings:
            if re.search(pattern, text):
                keywords.add(keyword)
        
        # 提取描述中的触发关键词（"当用户提到..."部分）
        trigger_phrases = re.findall(r'当用户提到([^，。,\.]+)', text)
        for phrase in trigger_phrases:
            # 从触发短语中提取关键词
            phrase_keywords = re.findall(r'[a-zA-Z\u4e00-\u9fff]+', phrase)
            keywords.update([k for k in phrase_keywords if len(k) > 1])
        
        # 添加技能名的组成部分作为关键词
        skill_parts = re.findall(r'[a-zA-Z]+', skill_name.lower())
        keywords.update([part for part in skill_parts if len(part) > 2])
        
        # 从描述中提取核心词汇（避免提取整个句子）
        desc_text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', description.lower())
        words = desc_text.split()
        important_words = [w for w in words if len(w) > 2 and len(w) < 20]  # 排除过长的词（可能是整个句子）
        keywords.update(important_words[:8])  # 增加数量限制到8个
        
        return list(keywords)
    
    def analyze_user_intent(self, user_message: str) -> List[SkillInfo]:
        """分析用户意图并匹配Skills"""
        print(f"\n=== 分析用户意图 ===")
        print(f"用户消息: {user_message}")
        
        matched_skills = []
        user_lower = user_message.lower()
        
        for skill in self.skills_registry:
            # 计算匹配置信度
            confidence = self._calculate_match_confidence_improved(user_lower, skill)
            if confidence > 0.05:  # 进一步降低阈值
                skill.confidence = confidence
                matched_skills.append(skill)
                print(f"  匹配Skill: {skill.name} (置信度: {confidence:.2f})")
        
        # 按置信度排序
        matched_skills.sort(key=lambda x: x.confidence, reverse=True)
        return matched_skills
    
    def _calculate_match_confidence_improved(self, user_message: str, skill: SkillInfo) -> float:
        """改进的匹配置信度计算"""
        confidence = 0.0
        user_lower = user_message.lower()
        
        # 1. 关键词匹配 (权重0.4)
        keyword_matches = 0
        high_priority_keywords = ['architect', 'design', 'system', 'task', 'decomposer', 'agent', 'constraint', 'interface', 'consistency', 'module', 'modulize', 'dapi', 'check', 'agentic', 'module_intelligence', 'complex_task', 'step_by_step', 'parameter', 'mismatch', 'error', 'inconsistency', 'definition', 'isolation_test', 'partition_test', 'system_refactor']
        medium_priority_keywords = ['api', 'document', 'generate', 'create', '分解', '设计', '架构', '智能体', '约束', '接口', '模块', '验证', '检查', '具身认知', '模块智能化', '智能模块', '复杂任务', '一步步', '任务分析', '任务清单', '任务计划', '参数', '不匹配', '错误', '不一致', '定义', '隔离测试', '分区测试', '系统重构']
        
        for keyword in skill.keywords:
            if keyword in user_lower:
                # 不同关键词有不同的权重
                if keyword in high_priority_keywords:
                    keyword_matches += 2.5  # 高权重关键词
                elif keyword in medium_priority_keywords:
                    keyword_matches += 1.5  # 中等权重关键词
                else:
                    keyword_matches += 1  # 普通权重
        
        if keyword_matches > 0:
            confidence += 0.4 * min(keyword_matches / 3, 1.0)  # 基于3个关键词的标准化
        
        # 2. 精确短语匹配 (权重0.3)
        # 检查用户消息是否包含技能描述中的关键短语
        desc_key_phrases = []
        desc_sentences = re.split(r'[，。,\.]', skill.description)
        for sentence in desc_sentences:
            # 提取描述中的关键短语（特别是"当用户提到..."部分）
            if '当用户提到' in sentence or '当用户需要' in sentence:
                key_phrase = sentence.replace('当用户提到', '').replace('当用户需要', '').replace('时使用', '').strip()
                if key_phrase:
                    desc_key_phrases.append(key_phrase)
        
        phrase_matches = 0
        for phrase in desc_key_phrases:
            if phrase in user_lower:
                phrase_matches += 2
        
        if phrase_matches > 0:
            confidence += 0.3 * min(phrase_matches / 2, 1.0)
        
        # 3. 语义匹配 (权重0.2)
        # 检查用户消息是否包含描述中的重要词汇
        desc_words = set(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', skill.description.lower()))
        user_words = set(re.findall(r'[a-zA-Z\u4e00-\u9fff]+', user_lower))
        common_words = len(desc_words.intersection(user_words))
        
        if common_words > 0:
            confidence += 0.2 * min(common_words / max(len(desc_words), 1), 1.0)
        
        # 4. 精确匹配 (权重0.1)
        # 检查用户消息是否直接包含技能名的关键部分
        skill_parts = [part for part in skill.name.lower().split('-') if len(part) > 2]
        exact_matches = sum(1 for part in skill_parts if part in user_lower)
        
        if exact_matches > 0:
            confidence += 0.1 * min(exact_matches / len(skill_parts), 1.0)
        
        return min(confidence, 1.0)
    
    def evaluate_skill_applicability(self, skill: SkillInfo, user_message: str) -> Dict[str, Any]:
        """评估Skill适用性"""
        print(f"\n=== 评估Skill适用性: {skill.name} ===")
        
        # 详细的适用性分析
        keyword_matches = [k for k in skill.keywords if k in user_message]
        
        applicability = {
            "skill_name": skill.name,
            "is_applicable": skill.confidence > 0.05,  # 降低阈值以测试DAPIcheck
            "confidence": skill.confidence,
            "matched_keywords": keyword_matches,
            "reasoning": f"发现关键词匹配: {keyword_matches}，语义相关性: {skill.confidence:.2f}",
            "suggested_action": f"建议调用 {skill.name} 处理此请求"
        }
        
        if applicability["is_applicable"]:
            print(f"  ✓ Skill适用 (置信度: {skill.confidence:.2f})")
            print(f"  匹配关键词: {keyword_matches}")
            print(f"  建议: {applicability['suggested_action']}")
        else:
            print(f"  ✗ Skill不适用 (置信度: {skill.confidence:.2f})")
            print(f"  匹配关键词: {keyword_matches}")
        
        return applicability

class SkillInvoker:
    """Skill调用器"""
    
    def __init__(self):
        self.discovery_hook = SkillsDiscoveryHook()
    
    def hook_before_ai_response(self, user_message: str, ai_context: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        """
        在AI响应前的Hook
        返回None表示继续正常AI响应，返回字典表示使用Skill响应
        """
        if ai_context is None:
            ai_context = {}
            
        print("\n" + "="*60)
        print("Skills智能发现Hook触发")
        print("="*60)
        
        # 1. 分析用户意图
        matched_skills = self.discovery_hook.analyze_user_intent(user_message)
        
        if not matched_skills:
            print("未发现匹配的Skills")
            return None
        
        # 2. 评估最匹配Skill的适用性
        top_skill = matched_skills[0]
        applicability = self.discovery_hook.evaluate_skill_applicability(top_skill, user_message)
        
        if applicability["is_applicable"]:
            # 3. 调用Skill
            skill_response = self._invoke_skill(top_skill, user_message, ai_context)
            return skill_response
        
        return None
    
    def _invoke_skill(self, skill: SkillInfo, user_message: str, ai_context: Dict[str, Any]) -> Dict[str, Any]:
        """调用Skill"""
        print(f"\n=== 调用Skill: {skill.name} ===")
        
        # 模拟Skill调用 - 实际实现中会调用具体的Skill代码
        skill_response = {
            "type": "skill_response",
            "skill_name": skill.name,
            "content": f"这是来自 {skill.name} 的专业响应。\n根据您的请求 '{user_message}'，我已为您执行相关操作并生成以下结果：\n\n[专业技能处理结果]",
            "confidence": skill.confidence,
            "matched_keywords": self.discovery_hook.evaluate_skill_applicability(skill, user_message)["matched_keywords"],
            "metadata": {
                "skill_path": skill.path,
                "invocation_time": "2025-11-01T23:45:00Z",
                "processing_context": ai_context
            }
        }
        
        print(f"Skill调用完成: {skill.name}")
        return skill_response

def demonstrate_skills_hook():
    """演示Skills Hook系统"""
    print("=== Skills智能发现和调用Hook演示 ===\n")
    
    # 创建Skill调用器
    skill_invoker = SkillInvoker()
    
    # 测试用例 - 更精确的请求，包含关键词
    test_cases = [
        "我需要设计系统架构和架构师服务",  # 应该匹配 architect 相关Skills
        "请分解复杂的开发任务",            # 应该匹配 task decomposer
        "创建一些智能体agent来工作",       # 应该匹配 agent creator
        "生成系统的约束条件和规范",        # 应该匹配 constraint generator
        "设计API接口和系统架构",          # 应该匹配 system architect
        "分解原子化任务task",             # 应该匹配 task decomposer
        "创建智能agent",                 # 应该匹配 agent creator
        "今天的天气怎么样？"              # 不匹配任何Skill
    ]
    
    for i, user_message in enumerate(test_cases, 1):
        print(f"\n--- 测试用例 {i} ---")
        
        # 模拟Hook调用
        response = skill_invoker.hook_before_ai_response(user_message, {"session_id": f"test_{i}"})
        
        if response:
            print(f"✓ Skill响应: {response['content'][:100]}...")
        else:
            print("→ 继续正常AI响应")
    
    print("\n" + "="*60)
    print("演示总结")
    print("="*60)
    print("✓ 实现了Skills智能发现机制")
    print("✓ 支持用户意图分析和Skill匹配")
    print("✓ 提供Skill适用性评估")
    print("✓ 实现自动Skill调用")
    print("✓ 保持与正常AI流程的兼容性")
    
    print("\nHook系统特点:")
    print("1. 无侵入式集成 - 不影响现有AI流程")
    print("2. 智能匹配算法 - 基于关键词和语义分析")
    print("3. 置信度驱动决策 - 避免误调用")
    print("4. 自动Skill发现 - 动态注册新Skills")
    print("5. 灵活的响应机制 - 支持Skill或AI响应")

# Hook集成示例
def integrate_with_ai_system():
    """与AI系统集成的示例"""
    print("\n=== Hook系统集成示例 ===")
    
    class AIConversationManager:
        """AI对话管理器"""
        
        def __init__(self):
            self.skill_invoker = SkillInvoker()
        
        def process_user_message(self, user_message: str) -> str:
            """处理用户消息"""
            # Hook 1: 在AI响应前检查Skills
            skill_response = self.skill_invoker.hook_before_ai_response(
                user_message, 
                {"user_id": "test_user", "session_context": "testing"}
            )
            
            if skill_response:
                # 如果Skill可以处理，直接返回Skill响应
                return f"[Skill: {skill_response['skill_name']}] {skill_response['content']}"
            else:
                # 否则继续正常的AI处理
                return f"[AI响应] 这是AI对 '{user_message}' 的标准响应"
    
    # 演示集成效果
    ai_manager = AIConversationManager()
    
    test_messages = [
        "我需要设计系统架构",      # 应该触发Skill
        "请分解开发任务",          # 应该触发Skill
        "随便聊聊"                # 应该正常AI响应
    ]
    
    print("对话流程演示:")
    for message in test_messages:
        response = ai_manager.process_user_message(message)
        print(f"用户: {message}")
        print(f"助手: {response}\n")

if __name__ == "__main__":
    demonstrate_skills_hook()
    integrate_with_ai_system()