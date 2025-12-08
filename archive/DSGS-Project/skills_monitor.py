#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Skills调用日志监控和分析工具
"""

import json
import os
import sys
from datetime import datetime
from collections import defaultdict, Counter
import re

class SkillsUsageMonitor:
    """Skills使用监控器"""
    
    def __init__(self, log_file="skills_usage.log"):
        self.log_file = log_file
        self.usage_data = []
    
    def log_skill_invocation(self, skill_name, user_message, confidence, matched_keywords, success=True):
        """记录Skill调用日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "skill_name": skill_name,
            "user_message": user_message,
            "confidence": confidence,
            "matched_keywords": matched_keywords,
            "success": success
        }
        
        # 写入日志文件
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
        
        # 保存到内存中用于分析
        self.usage_data.append(log_entry)
    
    def load_usage_data(self):
        """加载历史使用数据"""
        if not os.path.exists(self.log_file):
            return
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    self.usage_data.append(entry)
                except json.JSONDecodeError:
                    continue
    
    def analyze_usage_patterns(self):
        """分析使用模式"""
        if not self.usage_data:
            self.load_usage_data()
        
        if not self.usage_data:
            print("暂无使用数据")
            return
        
        # 统计各Skill调用次数
        skill_counts = Counter()
        total_invocations = len(self.usage_data)
        
        # 统计关键词使用频率
        keyword_counts = Counter()
        
        # 统计置信度分布
        confidence_levels = []
        
        for entry in self.usage_data:
            skill_counts[entry["skill_name"]] += 1
            confidence_levels.append(entry["confidence"])
            
            # 统计关键词
            for keyword in entry.get("matched_keywords", []):
                keyword_counts[keyword] += 1
        
        print("=== Skills使用分析报告 ===")
        print(f"总调用次数: {total_invocations}")
        print(f"时间范围: {self.usage_data[0]['timestamp']} 至 {self.usage_data[-1]['timestamp']}")
        
        print("\n各Skill调用次数:")
        for skill, count in skill_counts.most_common():
            percentage = (count / total_invocations) * 100
            print(f"  {skill}: {count}次 ({percentage:.1f}%)")
        
        print("\n高频关键词:")
        for keyword, count in keyword_counts.most_common(10):
            print(f"  {keyword}: {count}次")
        
        print(f"\n置信度统计:")
        if confidence_levels:
            avg_confidence = sum(confidence_levels) / len(confidence_levels)
            min_confidence = min(confidence_levels)
            max_confidence = max(confidence_levels)
            print(f"  平均置信度: {avg_confidence:.3f}")
            print(f"  最低置信度: {min_confidence:.3f}")
            print(f"  最高置信度: {max_confidence:.3f}")
        
        return {
            "skill_counts": dict(skill_counts),
            "keyword_counts": dict(keyword_counts),
            "confidence_stats": {
                "average": avg_confidence if confidence_levels else 0,
                "min": min_confidence if confidence_levels else 0,
                "max": max_confidence if confidence_levels else 0
            }
        }
    
    def identify_optimization_opportunities(self):
        """识别优化机会"""
        if not self.usage_data:
            self.load_usage_data()
        
        opportunities = []
        
        # 1. 识别低置信度调用
        low_confidence_calls = [entry for entry in self.usage_data if entry["confidence"] < 0.1]
        if low_confidence_calls:
            opportunities.append(f"发现 {len(low_confidence_calls)} 次低置信度调用，建议优化关键词匹配")
        
        # 2. 识别未成功调用
        failed_calls = [entry for entry in self.usage_data if not entry.get("success", True)]
        if failed_calls:
            opportunities.append(f"发现 {len(failed_calls)} 次调用失败，建议检查Skill实现")
        
        # 3. 识别使用频率低的Skills
        skill_counts = Counter(entry["skill_name"] for entry in self.usage_data)
        low_usage_skills = [skill for skill, count in skill_counts.items() if count < 3]
        if low_usage_skills:
            opportunities.append(f"以下Skills使用频率较低: {', '.join(low_usage_skills)}，建议优化描述或关键词")
        
        return opportunities

def demonstrate_monitoring():
    """演示监控功能"""
    print("=== Skills调用监控演示 ===\n")
    
    # 创建监控器
    monitor = SkillsUsageMonitor("demo_skills_usage.log")
    
    # 模拟一些Skill调用日志
    demo_calls = [
        ("dnaspec-agent-creator", "创建智能agent", 0.37, ["agent"]),
        ("dnaspec-task-decomposer", "分解原子化任务", 0.25, ["task"]),
        ("dnaspec-dapi-checker", "检查接口一致性", 0.42, ["interface", "check"]),
        ("dnaspec-modulizer", "模块化检查", 0.38, ["module", "check"]),
        ("dnaspec-constraint-generator", "生成系统约束", 0.31, ["constraint", "generate"]),
    ]
    
    # 记录调用日志
    for skill_name, message, confidence, keywords in demo_calls:
        monitor.log_skill_invocation(skill_name, message, confidence, keywords)
        print(f"记录调用: {skill_name} <- '{message}' (置信度: {confidence})")
    
    print("\n" + "="*50)
    
    # 分析使用模式
    monitor.analyze_usage_patterns()
    
    # 识别优化机会
    opportunities = monitor.identify_optimization_opportunities()
    if opportunities:
        print("\n优化建议:")
        for opportunity in opportunities:
            print(f"  • {opportunity}")
    else:
        print("\n✓ 暂无明显优化机会")

if __name__ == "__main__":
    demonstrate_monitoring()