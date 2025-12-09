#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini CLI 智能技能匹配系统
"""

import re
import time
import sys
import os
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass

# 添加项目路径到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini_skills_core import SkillManager, SkillInfo, get_skill_manager

@dataclass
class MatchResult:
    """匹配结果"""
    skill_info: SkillInfo
    confidence: float
    match_details: Dict[str, Any]
    processing_time: float

class IntelligentSkillMatcher:
    """智能技能匹配器"""
    
    def __init__(self):
        self.skill_manager = get_skill_manager()
        self.match_history = []  # 匹配历史，用于学习优化
    
    def match_skill_intelligently(self, user_request: str) -> Optional[MatchResult]:
        """智能匹配技能"""
        start_time = time.time()
        
        # 1. 多维度匹配
        exact_matches = self._find_exact_matches(user_request)
        semantic_matches = self._find_semantic_matches(user_request)
        context_matches = self._find_context_matches(user_request)
        
        # 2. 综合评分
        combined_scores = self._combine_match_scores(
            user_request, exact_matches, semantic_matches, context_matches
        )
        
        # 3. 获取最佳匹配
        best_match = self._get_best_match(combined_scores)
        
        processing_time = time.time() - start_time
        
        if best_match:
            return MatchResult(
                skill_info=best_match['skill_info'],
                confidence=best_match['combined_score'],
                match_details=best_match['details'],
                processing_time=processing_time
            )
        
        return None
    
    def _find_exact_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找精确匹配"""
        request_lower = request.lower()
        matches = []
        
        for skill_info in self.skill_manager.list_skills():
            score = 0.0
            details = {}
            
            # 关键词精确匹配 (权重0.6)
            matched_keywords = []
            for keyword in skill_info.keywords:
                if keyword.lower() in request_lower:
                    matched_keywords.append(keyword)
                    score += 0.6 / len(skill_info.keywords)
            
            # 技能名称匹配 (权重0.4)
            if skill_info.name.lower() in request_lower:
                score += 0.4
            
            # DNASPEC技能特殊处理 - 基于技能描述的关键短语匹配
            if "dnaspec" in skill_info.name.lower():
                # 为每个DNASPEC技能定义关键短语
                skill_phrases = {
                    'dnaspec-architect': ['架构设计', '系统设计', 'architecture', 'design system'],
                    'dnaspec-agent-creator': ['创建智能体', '智能体角色', 'agent creation', 'multi-agent'],
                    'dnaspec-task-decomposer': ['任务分解', '复杂任务', 'task decomposition', 'complex task'],
                    'dnaspec-dapi-checker': ['接口检查', '一致性检查', 'api validation', 'interface consistency'],
                    'dnaspec-modulizer': ['模块化', '成熟度检查', 'modularization', 'module maturity']
                }
                
                phrases = skill_phrases.get(skill_info.name.lower(), [])
                for phrase in phrases:
                    if phrase.lower() in request_lower:
                        score += 0.3
                        matched_keywords.append(phrase)
            
            if score > 0.1:  # 阈值
                matches.append({
                    'skill_info': skill_info,
                    'score': min(score, 1.0),
                    'type': 'exact',
                    'matched_keywords': matched_keywords
                })
        
        return matches
    
    def _find_semantic_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找语义匹配"""
        request_lower = request.lower()
        matches = []
        
        # 提取请求中的关键词
        request_words = set(re.findall(r'[\w\u4e00-\u9fff]+', request_lower))
        
        for skill_info in self.skill_manager.list_skills():
            score = 0.0
            details = {}
            
            # 描述语义相似度 (权重0.6)
            desc_words = set(re.findall(r'[\w\u4e00-\u9fff]+', skill_info.description.lower()))
            common_words = len(request_words.intersection(desc_words))
            
            if common_words > 0:
                semantic_score = 0.6 * (common_words / max(len(desc_words), 1))
                score += semantic_score
                details['semantic_similarity'] = semantic_score
            
            # 关键词语义扩展 (权重0.4)
            extended_keywords = self._extend_keywords(skill_info.keywords)
            matched_extended = []
            for ext_keyword in extended_keywords:
                if ext_keyword.lower() in request_lower:
                    matched_extended.append(ext_keyword)
                    score += 0.4 / len(extended_keywords)
            
            if score > 0.05:  # 阈值
                matches.append({
                    'skill_info': skill_info,
                    'score': min(score, 1.0),
                    'type': 'semantic',
                    'matched_extended': matched_extended,
                    'details': details
                })
        
        return matches
    
    def _find_context_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找上下文匹配"""
        matches = []
        
        # 基于请求类型和上下文的匹配
        context_indicators = self._extract_context_indicators(request)
        
        for skill_info in self.skill_manager.list_skills():
            score = 0.0
            context_matches = []
            
            # 上下文相关性 (权重1.0)
            for indicator in context_indicators:
                if self._is_skill_relevant_to_context(skill_info, indicator):
                    context_matches.append(indicator)
                    score += 1.0 / len(context_indicators)
            
            if score > 0.1:  # 阈值
                matches.append({
                    'skill_info': skill_info,
                    'score': min(score, 1.0),
                    'type': 'context',
                    'context_matches': context_matches
                })
        
        return matches
    
    def _combine_match_scores(self, request: str, exact_matches: List, 
                             semantic_matches: List, context_matches: List) -> List[Dict[str, Any]]:
        """综合匹配评分"""
        combined_scores = {}
        
        # 收集所有匹配结果
        all_matches = exact_matches + semantic_matches + context_matches
        
        for match in all_matches:
            skill_name = match['skill_info'].name
            
            if skill_name not in combined_scores:
                combined_scores[skill_name] = {
                    'skill_info': match['skill_info'],
                    'exact_score': 0.0,
                    'semantic_score': 0.0,
                    'context_score': 0.0,
                    'matches': []
                }
            
            # 累加不同类型得分
            score_dict = combined_scores[skill_name]
            if match['type'] == 'exact':
                score_dict['exact_score'] = max(score_dict['exact_score'], match['score'])
            elif match['type'] == 'semantic':
                score_dict['semantic_score'] = max(score_dict['semantic_score'], match['score'])
            elif match['type'] == 'context':
                score_dict['context_score'] = max(score_dict['context_score'], match['score'])
            
            score_dict['matches'].append(match)
        
        # 计算综合得分
        final_scores = []
        for skill_name, score_data in combined_scores.items():
            # 综合评分公式：精确(0.5) + 语义(0.3) + 上下文(0.2)
            combined_score = (
                score_data['exact_score'] * 0.5 +
                score_data['semantic_score'] * 0.3 +
                score_data['context_score'] * 0.2
            )
            
            final_scores.append({
                'skill_info': score_data['skill_info'],
                'combined_score': combined_score,
                'exact_score': score_data['exact_score'],
                'semantic_score': score_data['semantic_score'],
                'context_score': score_data['context_score'],
                'details': {
                    'matches': score_data['matches']
                }
            })
        
        # 按得分排序
        final_scores.sort(key=lambda x: x['combined_score'], reverse=True)
        return final_scores
    
    def _get_best_match(self, combined_scores: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """获取最佳匹配"""
        if not combined_scores:
            return None
        
        best_match = combined_scores[0]
        if best_match['combined_score'] > 0.15:  # 最低阈值
            return best_match
        
        return None
    
    def _extend_keywords(self, keywords: List[str]) -> List[str]:
        """扩展关键词"""
        extended = keywords.copy()
        
        # 关键词同义词扩展
        synonym_map = {
            '创建': ['生成', '构建', '设计', '开发'],
            '智能体': ['agent', '代理', 'ai助手', 'agentic', '模块智能化', '具身认知'],
            '分解': ['拆分', '细化', '原子化', '一步步拆解', '任务分析', '任务清单', '任务计划'],
            '任务': ['工作', 'job', 'activity', 'task'],
            '约束': ['规范', '限制', '规则', 'constraint', 'specification'],
            '接口': ['api', '界面', 'boundary', 'interface', '参数', '定义', '参数不一致', '接口不匹配', '参数错误', '接口错误'],
            '检查': ['验证', '核验', 'audit', 'consistency', 'verification'],
            '模块': ['component', '模块化', 'component', 'module', '隔离测试', '分区测试', '降低系统复杂度', '系统重构'],
            '重构': ['重写', '优化', 'refactor', 'improvement'],
            '架构': ['structure', '设计', 'framework', 'architecture', 'blueprint'],
            '成熟度': ['maturity', 'assessment', 'evaluation', '自底向上', 'bottom_up', 'sealing', '封装'],
            '系统': ['system', '体系', '体系结构', 'structure'],
            'dnaspec': ['dynamic', 'specification', 'growth', 'system', '动态规范', '动态增长']
        }
        
        for keyword in keywords:
            for syn_keyword, synonyms in synonym_map.items():
                if syn_keyword in keyword:
                    extended.extend(synonyms)
        
        return list(set(extended))  # 去重
    
    def _extract_context_indicators(self, request: str) -> List[str]:
        """提取上下文指示器"""
        indicators = []
        
        # 请求类型指示器
        type_patterns = {
            'creation': ['创建', '生成', '设计', '构建', 'create', 'generate', 'build'],
            'decomposition': ['分解', '拆分', '细化', '一步步拆解', '任务分析', '任务清单', '任务计划'],
            'validation': ['检查', '验证', '核验', '验证', '一致性', '不一致', '参数不一致', '定义不一致', '接口不匹配'],
            'generation': ['生成', '产生', '创建', '产生'],
            'optimization': ['优化', '重构', '改进', '系统重构', '降低系统复杂度', '隔离测试', '分区测试'],
            'analysis': ['分析', '评估', '审查', '成熟度', '模块化', '封装', '自底向上']
        }
        
        request_lower = request.lower()
        for type_name, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in request_lower:
                    indicators.append(type_name)
                    break
        
        # 领域指示器
        domain_patterns = {
            'ai': ['智能', 'ai', '机器学习', 'agentic', '模块智能化', '具身认知'],
            'software': ['软件', '程序', '代码', 'module', 'component'],
            'system': ['系统', '架构', '体系', 'architecture', 'design'],
            'project': ['项目', '工程', '任务', 'project', 'task'],
            'data': ['数据', 'database', '信息', 'api', '接口']
        }
        
        for domain, patterns in domain_patterns.items():
            for pattern in patterns:
                if pattern in request_lower:
                    indicators.append(domain)
                    break
        
        return list(set(indicators))  # 去重
    
    def _is_skill_relevant_to_context(self, skill_info: SkillInfo, context: str) -> bool:
        """判断技能是否与上下文相关"""
        context_relevance = {
            'creation': ['agent-creator', 'architect'],
            'decomposition': ['task-decomposer'],
            'validation': ['dapi-checker', 'modulizer'],
            'generation': ['constraint-generator', 'agent-creator'],
            'optimization': ['modulizer', 'architect'],
            'analysis': ['dapi-checker', 'modulizer'],
            'ai': ['agent-creator'],
            'software': ['task-decomposer', 'dapi-checker'],
            'system': ['architect'],
            'project': ['task-decomposer', 'agent-creator'],
            'data': ['dapi-checker']
        }
        
        relevant_skills = context_relevance.get(context, [])
        return any(skill_name in skill_info.name for skill_name in relevant_skills)
    
    def learn_from_match_result(self, user_request: str, match_result: Optional[MatchResult], 
                               user_feedback: float):
        """从匹配结果中学习"""
        # 记录匹配历史用于后续优化
        self.match_history.append({
            'request': user_request,
            'result': match_result,
            'feedback': user_feedback,
            'timestamp': time.time()
        })
        
        # 保持历史记录在合理范围内
        if len(self.match_history) > 1000:
            self.match_history = self.match_history[-500:]

# 全局匹配器实例
intelligent_matcher = IntelligentSkillMatcher()

def get_intelligent_matcher() -> IntelligentSkillMatcher:
    """获取全局智能匹配器"""
    return intelligent_matcher

if __name__ == "__main__":
    # 测试智能匹配系统
    matcher = get_intelligent_matcher()
    
    print("=== Gemini CLI 智能技能匹配系统测试 ===")
    
    test_requests = [
        "创建一个项目管理智能体",
        "分解复杂的软件开发任务",
        "生成API接口约束规范",
        "检查微服务接口一致性",
        "对系统进行模块化重构",
        "设计分布式系统架构",
        "优化现有代码结构",
        "分析系统性能瓶颈"
    ]
    
    print("智能匹配测试:")
    for request in test_requests:
        result = matcher.match_skill_intelligently(request)
        if result:
            print(f"  '{request}'")
            print(f"    -> {result.skill_info.name} (置信度: {result.confidence:.3f})")
            print(f"    -> 处理时间: {result.processing_time:.3f}ms")
        else:
            print(f"  '{request}' -> 无匹配技能")
        print()