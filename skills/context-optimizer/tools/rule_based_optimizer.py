#!/usr/bin/env python3
"""
Context Optimizer - Rule-Based Optimization Engine
确定性规则优化引擎
"""

import re
import json
import sys
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class OptimizationResult:
    """优化结果数据结构"""
    optimized_context: str
    applied_rules: List[Dict[str, Any]]
    improvements: Dict[str, float]
    change_summary: Dict[str, int]

class ContextOptimizer:
    """上下文优化器 - 确定性规则引擎"""
    
    def __init__(self):
        self.optimization_rules = {
            'clarity': self.optimize_clarity_rules,
            'relevance': self.optimize_relevance_rules,
            'completeness': self.optimize_completeness_rules,
            'consistency': self.optimize_consistency_rules,
            'efficiency': self.optimize_efficiency_rules,
            'conciseness': self.optimize_conciseness_rules
        }
        
        self.clarity_replacements = {
            r'\b一些\b': '具体的',
            r'\b某些\b': '特定的',
            r'\b很多\b': '大量(如：100个以上)',
            r'\b部分\b': '特定部分',
            r'\b可能\b': '在特定条件下',
            r'\b也许\b': '在某些情况下',
            r'\b大概\b': '大约(估算)',
            r'\b左右\b': '±5%范围内',
            r'\b大约\b': '大约(精确)',
            r'\b好像\b': '看起来像'
        }
        
        self.terminology_standards = {
            '用户': {'用户', '使用者', '操作员', '客户'},
            '系统': {'系统', '平台', '应用', '软件', '程序'},
            '数据': {'数据', '信息', '资料', '内容'},
            '功能': {'功能', '特性', '能力', '作用'},
            '接口': {'接口', 'API', '方法', '函数'}
        }
    
    def optimize_context(self, context: str, optimization_goals: List[str], 
                       preserve_style: bool = True) -> OptimizationResult:
        """执行上下文优化"""
        if not context:
            return OptimizationResult("", [], {}, {})
        
        optimized_context = context
        applied_rules = []
        change_summary = {
            'replacements': 0,
            'additions': 0,
            'removals': 0,
            'restructures': 0
        }
        
        # 按优先级应用优化规则
        for goal in optimization_goals:
            if goal in self.optimization_rules:
                optimization_func = self.optimization_rules[goal]
                context_part, rules_applied, changes = optimization_func(
                    optimized_context, preserve_style
                )
                
                if context_part != optimized_context:
                    optimized_context = context_part
                    applied_rules.extend(rules_applied)
                    
                    # 累积变化统计
                    for key in change_summary:
                        change_summary[key] += changes.get(key, 0)
        
        # 计算改进指标
        improvements = self.calculate_improvements(context, optimized_context)
        
        return OptimizationResult(
            optimized_context=optimized_context,
            applied_rules=applied_rules,
            improvements=improvements,
            change_summary=change_summary
        )
    
    def optimize_clarity_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """清晰度优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 替换模糊词汇
        for pattern, replacement in self.clarity_replacements.items():
            if re.search(pattern, optimized):
                old_count = len(re.findall(pattern, optimized))
                optimized = re.sub(pattern, replacement, optimized)
                changes['replacements'] += old_count
                
                applied_rules.append({
                    'rule': 'replace_ambiguous_terms',
                    'pattern': pattern,
                    'replacement': replacement,
                    'count': old_count
                })
        
        # 规则2: 增加明确指令
        sentences = re.split(r'[.!?。！？]+', optimized)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 检查是否缺少明确指令动词
        clear_indicators = ['请', '需要', '要求', '目标', '任务', '执行', '实现']
        has_clear_instruction = any(indicator in optimized for indicator in clear_indicators)
        
        if not has_clear_instruction and sentences:
            # 在第一个句子前添加明确指令
            if sentences[0]:
                optimized = f"请执行以下操作：{optimized}"
                changes['additions'] += 1
                
                applied_rules.append({
                    'rule': 'add_clear_instruction',
                    'instruction': '请执行以下操作：',
                    'position': 'beginning'
                })
        
        # 规则3: 优化句子长度
        long_sentences = []
        for i, sentence in enumerate(sentences):
            if len(sentence) > 150:  # 超长句子
                long_sentences.append((i, sentence))
        
        for i, sentence in long_sentences:
            # 尝试按逻辑断点分割长句
            logical_breaks = ['，并且', '，同时', '，然后', '，而且']
            for break_point in logical_breaks:
                if break_point in sentence:
                    parts = sentence.split(break_point)
                    if len(parts) >= 2:
                        new_sentence = f"{parts[0]}。{break_point[1:]}{parts[1]}"
                        optimized = optimized.replace(sentence, new_sentence)
                        changes['restructures'] += 1
                        
                        applied_rules.append({
                            'rule': 'split_long_sentence',
                            'position': i,
                            'break_point': break_point
                        })
                        break
        
        return optimized, applied_rules, changes
    
    def optimize_relevance_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """相关性优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 检测并增强领域相关性
        domain_keywords = {
            'technical': ['技术', '系统', '开发', '设计', '架构', '算法', '数据', '接口'],
            'business': ['业务', '客户', '市场', '产品', '服务', '流程', '收益', '成本'],
            'user_experience': ['用户', '体验', '界面', '交互', '可用性', '满意度', '便利性'],
            'data_analysis': ['分析', '统计', '趋势', '模式', '预测', '指标', '报告']
        }
        
        # 检测最相关的领域
        domain_scores = {}
        for domain, keywords in domain_keywords.items():
            score = sum(1 for keyword in keywords if keyword in context)
            domain_scores[domain] = score
        
        primary_domain = max(domain_scores.items(), key=lambda x: x[1])[0]
        
        # 如果主要领域相关性较低，添加相关关键词
        if domain_scores[primary_domain] < 2:
            # 在适当位置添加领域相关术语
            enhancement_suggestions = {
                'technical': '技术实现方案',
                'business': '业务价值',
                'user_experience': '用户体验优化',
                'data_analysis': '数据分析洞察'
            }
            
            enhancement = enhancement_suggestions.get(primary_domain, '相关优化')
            if '。' in optimized:
                optimized = optimized.replace('。', f'，考虑{enhancement}。', 1)
            else:
                optimized += f'，考虑{enhancement}'
            
            changes['additions'] += 1
            applied_rules.append({
                'rule': 'enhance_domain_relevance',
                'domain': primary_domain,
                'enhancement': enhancement
            })
        
        # 规则2: 移除明显偏离主题的内容
        off_topic_indicators = ['顺便说一下', '另外', '值得一提的是', '顺便']
        for indicator in off_topic_indicators:
            if indicator in optimized:
                # 移除偏离主题的句子
                pattern = f'{indicator}[^。！？]*[。！？]'
                matches = re.findall(pattern, optimized)
                for match in matches:
                    optimized = optimized.replace(match, '')
                    changes['removals'] += 1
                    
                    applied_rules.append({
                        'rule': 'remove_off_topic_content',
                        'indicator': indicator,
                        'removed_content': match[:50] + '...'
                    })
        
        return optimized, applied_rules, changes
    
    def optimize_completeness_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """完整性优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 检查并补充约束条件
        constraint_patterns = ['假设', '约束', '要求', '条件', '规则', '限制']
        has_constraints = any(pattern in context for pattern in constraint_patterns)
        
        if not has_constraints:
            # 根据上下文类型添加约束条件
            constraint_suggestions = {
                'performance': '性能约束：响应时间<500ms，并发数>1000',
                'security': '安全约束：数据加密，访问控制，审计日志',
                'usability': '可用性约束：界面友好，操作简便',
                'scalability': '扩展性约束：支持水平扩展，模块化设计'
            }
            
            # 简单检测上下文类型
            context_type = 'general'
            if '性能' in context or '速度' in context or '响应' in context:
                context_type = 'performance'
            elif '安全' in context or '权限' in context or '登录' in context:
                context_type = 'security'
            elif '界面' in context or '用户' in context or '操作' in context:
                context_type = 'usability'
            elif '扩展' in context or '增长' in context or '大量' in context:
                context_type = 'scalability'
            
            constraint = constraint_suggestions.get(context_type, '基本约束条件')
            optimized += f'\n\n约束条件：{constraint}'
            changes['additions'] += 1
            
            applied_rules.append({
                'rule': 'add_constraint_conditions',
                'type': context_type,
                'constraint': constraint
            })
        
        # 规则2: 补充边界条件
        boundary_indicators = ['边界', '范围', '限制', '例外', '特殊情况']
        has_boundaries = any(indicator in context for indicator in boundary_indicators)
        
        if not has_boundaries:
            boundary_suggestion = '\n边界条件：考虑极端情况和异常处理场景'
            optimized += boundary_suggestion
            changes['additions'] += 1
            
            applied_rules.append({
                'rule': 'add_boundary_conditions',
                'suggestion': boundary_suggestion
            })
        
        return optimized, applied_rules, changes
    
    def optimize_consistency_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """一致性优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 术语标准化
        for standard_term, variants in self.terminology_standards.items():
            term_count = {}
            for variant in variants:
                count = len(re.findall(variant, optimized))
                if count > 0:
                    term_count[variant] = count
            
            if len(term_count) > 1:  # 存在多个变体
                # 选择出现频率最高的作为标准
                primary_variant = max(term_count.items(), key=lambda x: x[1])[0]
                
                # 将其他变体替换为标准术语
                for variant, count in term_count.items():
                    if variant != primary_variant:
                        optimized = optimized.replace(variant, standard_term)
                        changes['replacements'] += count
                        
                        applied_rules.append({
                            'rule': 'standardize_terminology',
                            'standard_term': standard_term,
                            'replaced_variant': variant,
                            'count': count
                        })
        
        # 规则2: 解决逻辑矛盾
        contradiction_pairs = [
            ('必须', '可以'), ('应该', '不必'), ('总是', '从不'),
            ('所有', '没有'), ('包含', '排除'), ('允许', '禁止')
        ]
        
        for pos, neg in contradiction_pairs:
            if pos in optimized and neg in optimized:
                # 检测是否为真正的矛盾
                sentences = re.split(r'[.!?。！？]+', optimized)
                pos_sentences = [s for s in sentences if pos in s]
                neg_sentences = [s for s in sentences if neg in s]
                
                # 简单的矛盾解决策略：在否定词前添加条件
                for sentence in neg_sentences:
                    if sentence.strip():
                        qualified_neg = sentence.replace(neg, f'在特定情况下不{neg[1:]}')
                        optimized = optimized.replace(sentence, qualified_neg)
                        changes['replacements'] += 1
                        
                        applied_rules.append({
                            'rule': 'resolve_contradiction',
                            'positive_term': pos,
                            'negative_term': neg,
                            'resolution': 'add_condition_qualifier'
                        })
        
        return optimized, applied_rules, changes
    
    def optimize_efficiency_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """效率优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 移除冗余表达
        redundancy_patterns = [
            r'\bas\s+well\s+as\b': '以及',  # as well as -> 以及
            r'\bin\s+order\s+to\b': '为了',  # in order to -> 为了
            r'\bdue\s+to\s+the\s+fact\s+that\b': '因为',  # due to the fact that -> 因为
            r'\b重复\b.*?\b重复\b': '重复',  # 删除重复的"重复"
            r'\b相同\b.*?\b相同\b': '相同',  # 删除重复的"相同"
        ]
        
        for pattern, replacement in redundancy_patterns.items():
            if re.search(pattern, optimized, re.IGNORECASE):
                old_count = len(re.findall(pattern, optimized, re.IGNORECASE))
                optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
                changes['replacements'] += old_count
                
                applied_rules.append({
                    'rule': 'remove_redundancy',
                    'pattern': pattern,
                    'replacement': replacement,
                    'count': old_count
                })
        
        # 规则2: 提高信息密度
        words = re.findall(r'[\w\u4e00-\u9fff]+', optimized)
        short_words = [w for w in words if len(w) == 1]
        
        if len(short_words) > len(words) * 0.3:  # 单字词比例过高
            # 合并相关的单字词
            combinations = {
                '可 以': '可以',
                '需 要': '需要',
                '应 该': '应该',
                '可 能': '可能',
                '已 经': '已经'
            }
            
            for combination, replacement in combinations.items():
                if combination in optimized:
                    optimized = optimized.replace(combination, replacement)
                    changes['replacements'] += 1
                    
                    applied_rules.append({
                        'rule': 'improve_information_density',
                        'combination': combination,
                        'replacement': replacement
                    })
        
        return optimized, applied_rules, changes
    
    def optimize_conciseness_rules(self, context: str, preserve_style: bool) -> Tuple[str, List[Dict], Dict]:
        """简洁性优化规则"""
        optimized = context
        applied_rules = []
        changes = {'replacements': 0, 'additions': 0, 'removals': 0, 'restructures': 0}
        
        # 规则1: 移除填充词
        filler_words = [
            r'\b基本上\b', r'\b事实上\b', r'\b实际上\b', r'\b一般来说\b',
            r'\b需要注意的是\b', r'\b重要的是\b', r'\b换句话说\b'
        ]
        
        for filler in filler_words:
            if re.search(filler, optimized):
                old_count = len(re.findall(filler, optimized))
                optimized = re.sub(filler, '', optimized)
                changes['removals'] += old_count
                
                applied_rules.append({
                    'rule': 'remove_filler_words',
                    'filler_word': filler,
                    'count': old_count
                })
        
        # 规则2: 简化复杂表达
        simplifications = {
            r'进行\s+([分析|设计|开发|测试|优化|改进])': r'\1',
            r'做出\s+([决定|选择|判断|贡献])': r'\1',
            r'实现\s+([自动化|智能化|数字化])': r'\1化',
            r'提供\s+([支持|帮助|保障|服务])': r'\1'
        }
        
        for pattern, replacement in simplifications.items():
            if re.search(pattern, optimized):
                old_count = len(re.findall(pattern, optimized))
                optimized = re.sub(pattern, replacement, optimized)
                changes['replacements'] += old_count
                
                applied_rules.append({
                    'rule': 'simplify_expressions',
                    'pattern': pattern,
                    'replacement': replacement,
                    'count': old_count
                })
        
        return optimized, applied_rules, changes
    
    def calculate_improvements(self, original: str, optimized: str) -> Dict[str, float]:
        """计算改进指标"""
        if not original:
            return {}
        
        # 简单的改进指标计算
        original_len = len(original)
        optimized_len = len(optimized)
        
        length_change = (original_len - optimized_len) / original_len if original_len > 0 else 0
        
        # 词汇多样性
        original_words = set(re.findall(r'[\w\u4e00-\u9fff]+', original))
        optimized_words = set(re.findall(r'[\w\u4e00-\u9fff]+', optimized))
        
        vocabulary_change = len(optimized_words) - len(original_words)
        
        return {
            'length_reduction': abs(length_change),  # 长度减少比例
            'vocabulary_improvement': vocabulary_change,  # 词汇改进数量
            'optimization_intensity': (original_len - optimized_len) / original_len if original_len > 0 else 0
        }

def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("Usage: python rule_based_optimizer.py <context_text> <optimization_goals>")
        print("Example: python rule_based_optimizer.py 'context text' 'clarity,relevance,completeness'")
        sys.exit(1)
    
    context_text = sys.argv[1]
    optimization_goals = sys.argv[2].split(',')
    optimization_goals = [goal.strip() for goal in optimization_goals]
    
    optimizer = ContextOptimizer()
    result = optimizer.optimize_context(context_text, optimization_goals)
    
    # 输出结构化结果
    output = {
        "original_context": context_text,
        "optimized_context": result.optimized_context,
        "optimization_goals": optimization_goals,
        "applied_rules": result.applied_rules,
        "change_summary": result.change_summary,
        "improvements": result.improvements
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()