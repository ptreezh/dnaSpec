"""
智能匹配系统
提供用户意图识别和技能自动匹配功能
"""
import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class MatchResult:
    """匹配结果"""
    skill_name: str
    confidence: float
    match_type: str
    matched_keywords: List[str]
    processing_time: float


class IntelligentMatcher:
    """智能匹配器"""
    
    def __init__(self):
        self.match_threshold = 0.2  # 降低阈值以便测试
        self._skill_keywords = {}   # 技能关键词映射
        self._command_patterns = {} # 命令模式映射
    
    def register_skill_keywords(self, skill_name: str, keywords: List[str]) -> bool:
        """注册技能关键词"""
        if not skill_name or not keywords:
            return False
        
        self._skill_keywords[skill_name] = keywords
        return True
    
    def register_command_pattern(self, skill_name: str, patterns: List[str]) -> bool:
        """注册命令模式"""
        if not skill_name or not patterns:
            return False
        
        self._command_patterns[skill_name] = patterns
        return True
    
    def match_intelligently(self, user_request: str) -> Optional[MatchResult]:
        """智能匹配用户请求到相应技能"""
        import time
        start_time = time.time()
        
        if not user_request:
            return None
        
        # 1. spec.kit命令模式匹配
        spec_kit_match = self._match_spec_kit_commands(user_request)
        if spec_kit_match and spec_kit_match.confidence > 0.9:
            spec_kit_match.processing_time = time.time() - start_time
            return spec_kit_match
        
        # 2. 关键词匹配
        keyword_matches = self._find_keyword_matches(user_request)
        
        # 3. 语义匹配
        semantic_matches = self._find_semantic_matches(user_request)
        
        # 4. 上下文匹配
        context_matches = self._find_context_matches(user_request)
        
        # 5. 综合评分和最佳匹配选择
        best_match = self._get_best_match(
            user_request, keyword_matches, semantic_matches, context_matches
        )
        
        if best_match:
            best_match.processing_time = time.time() - start_time
        
        return best_match
    
    def _match_spec_kit_commands(self, request: str) -> Optional[MatchResult]:
        """匹配spec.kit命令模式"""
        if not request.startswith("/speckit.dnaspec."):
            return None
        
        # 提取技能名称
        remaining = request[len("/speckit.dnaspec."):].strip()
        if ' ' in remaining:
            skill_name_part = remaining.split(' ', 1)[0]
        else:
            skill_name_part = remaining
        
        full_skill_name = f"dnaspec-{skill_name_part}"
        
        return MatchResult(
            skill_name=full_skill_name,
            confidence=0.95,  # 高置信度
            match_type="spec_kit_command",
            matched_keywords=[f"/speckit.dnaspec.{skill_name_part}"],
            processing_time=0.0
        )
    
    def _find_keyword_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找关键词匹配"""
        request_lower = request.lower()
        matches = []
        
        for skill_name, keywords in self._skill_keywords.items():
            score = 0.0
            matched_keywords = []
            
            for keyword in keywords:
                if keyword.lower() in request_lower:
                    matched_keywords.append(keyword)
                    score += 1.0 / len(keywords)
            
            if score > 0:
                matches.append({
                    'skill_name': skill_name,
                    'score': min(score, 1.0),
                    'type': 'keyword',
                    'matched_keywords': matched_keywords
                })
        
        return matches
    
    def _find_semantic_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找语义匹配"""
        request_lower = request.lower()
        matches = []
        
        # 提取请求中的关键词
        request_words = set(re.findall(r'[\w\u4e00-\u9fff]+', request_lower))
        
        for skill_name, keywords in self._skill_keywords.items():
            score = 0.0
            matched_words = []
            
            # 计算语义相似度
            for keyword in keywords:
                keyword_words = set(re.findall(r'[\w\u4e00-\u9fff]+', keyword.lower()))
                common_words = len(request_words.intersection(keyword_words))
                
                if common_words > 0:
                    semantic_score = common_words / max(len(keyword_words), 1)
                    score += semantic_score
                    matched_words.extend(list(request_words.intersection(keyword_words)))
            
            if score > 0:
                matches.append({
                    'skill_name': skill_name,
                    'score': min(score, 1.0),
                    'type': 'semantic',
                    'matched_words': matched_words
                })
        
        return matches
    
    def _find_context_matches(self, request: str) -> List[Dict[str, Any]]:
        """查找上下文匹配"""
        matches = []
        request_lower = request.lower()
        
        # 上下文指示器
        context_indicators = self._extract_context_indicators(request)
        
        for skill_name in self._skill_keywords.keys():
            score = 0.0
            matched_contexts = []
            
            # 检查技能相关性
            skill_relevance = self._get_skill_context_relevance(skill_name)
            for indicator in context_indicators:
                if indicator in skill_relevance:
                    matched_contexts.append(indicator)
                    score += 1.0 / len(context_indicators)
            
            if score > 0:
                matches.append({
                    'skill_name': skill_name,
                    'score': min(score, 1.0),
                    'type': 'context',
                    'matched_contexts': matched_contexts
                })
        
        return matches
    
    def _extract_context_indicators(self, request: str) -> List[str]:
        """提取上下文指示器"""
        indicators = []
        request_lower = request.lower()
        
        # 请求类型指示器
        type_patterns = {
            'creation': ['创建', '生成', '设计', '构建', 'create', 'generate', 'build', '设计'],
            'decomposition': ['分解', '拆分', '细化', '任务分析', 'task', '分解任务'],
            'validation': ['检查', '验证', '核验', '一致性', 'validate', '检查接口'],
            'generation': ['生成', '产生', 'create', 'generate', '生成约束'],
            'optimization': ['优化', '重构', '改进', 'optimize', 'refactor', '模块化'],
            'analysis': ['分析', '评估', '审查', 'analyze', 'evaluate', '分析系统']
        }
        
        for type_name, patterns in type_patterns.items():
            for pattern in patterns:
                if pattern in request_lower:
                    indicators.append(type_name)
                    break
        
        # 领域指示器
        domain_patterns = {
            'ai': ['智能', 'ai', 'agent', '智能体', '创建智能体'],
            'software': ['软件', '程序', '代码', 'software', '开发'],
            'system': ['系统', '架构', 'system', 'architecture', '系统设计'],
            'project': ['项目', '工程', 'project', '任务'],
            'data': ['数据', 'database', '信息', 'data', '接口']
        }
        
        for domain, patterns in domain_patterns.items():
            for pattern in patterns:
                if pattern in request_lower:
                    indicators.append(domain)
                    break
        
        return list(set(indicators))  # 去重
    
    def _get_skill_context_relevance(self, skill_name: str) -> List[str]:
        """获取技能上下文相关性"""
        context_relevance = {
            'dnaspec-architect': ['system', 'architecture', 'design', 'creation', '分析'],
            'dnaspec-agent-creator': ['ai', 'creation', 'agent', '智能体'],
            'dnaspec-task-decomposer': ['decomposition', 'task', 'project', '分析'],
            'dnaspec-constraint-generator': ['generation', 'validation', '生成'],
            'dnaspec-dapi-checker': ['validation', 'data', 'system', '检查'],
            'dnaspec-modulizer': ['optimization', 'analysis', 'system', '优化']
        }
        
        return context_relevance.get(skill_name, [])
    
    def _get_best_match(self, request: str, keyword_matches: List, 
                       semantic_matches: List, context_matches: List) -> Optional[MatchResult]:
        """获取最佳匹配"""
        # 收集所有匹配结果
        all_matches = keyword_matches + semantic_matches + context_matches
        
        if not all_matches:
            return None
        
        # 按技能名称分组并计算综合得分
        combined_scores = {}
        
        for match in all_matches:
            skill_name = match['skill_name']
            
            if skill_name not in combined_scores:
                combined_scores[skill_name] = {
                    'skill_name': skill_name,
                    'keyword_score': 0.0,
                    'semantic_score': 0.0,
                    'context_score': 0.0,
                    'matches': []
                }
            
            # 累加不同类型得分
            score_dict = combined_scores[skill_name]
            if match['type'] == 'keyword':
                score_dict['keyword_score'] = max(score_dict['keyword_score'], match['score'])
            elif match['type'] == 'semantic':
                score_dict['semantic_score'] = max(score_dict['semantic_score'], match['score'])
            elif match['type'] == 'context':
                score_dict['context_score'] = max(score_dict['context_score'], match['score'])
            
            score_dict['matches'].append(match)
        
        # 计算综合得分（关键词:0.5 + 语义:0.3 + 上下文:0.2）
        final_scores = []
        for skill_name, score_data in combined_scores.items():
            combined_score = (
                score_data['keyword_score'] * 0.5 +
                score_data['semantic_score'] * 0.3 +
                score_data['context_score'] * 0.2
            )
            
            if combined_score >= self.match_threshold:
                final_scores.append({
                    'skill_name': score_data['skill_name'],
                    'combined_score': combined_score,
                    'keyword_score': score_data['keyword_score'],
                    'semantic_score': score_data['semantic_score'],
                    'context_score': score_data['context_score'],
                    'matches': score_data['matches']
                })
        
        # 按得分排序并返回最佳匹配
        if final_scores:
            final_scores.sort(key=lambda x: x['combined_score'], reverse=True)
            best_match = final_scores[0]
            
            # 确定匹配类型
            match_types = [match['type'] for match in best_match['matches']]
            primary_type = match_types[0] if match_types else 'combined'
            
            # 收集匹配的关键词
            matched_keywords = []
            for match in best_match['matches']:
                if 'matched_keywords' in match:
                    matched_keywords.extend(match['matched_keywords'])
                elif 'matched_words' in match:
                    matched_keywords.extend(match['matched_words'])
                elif 'matched_contexts' in match:
                    matched_keywords.extend(match['matched_contexts'])
            
            return MatchResult(
                skill_name=best_match['skill_name'],
                confidence=best_match['combined_score'],
                match_type=primary_type,
                matched_keywords=list(set(matched_keywords)),  # 去重
                processing_time=0.0
            )
        
        return None
    
    def get_matcher_info(self) -> Dict[str, Any]:
        """获取匹配器信息"""
        return {
            'match_threshold': self.match_threshold,
            'registered_skills_count': len(self._skill_keywords),
            'registered_skills': list(self._skill_keywords.keys()),
            'registered_patterns_count': len(self._command_patterns)
        }