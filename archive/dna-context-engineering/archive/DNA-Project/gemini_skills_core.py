#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini CLI DNASPEC Skills 核心框架
"""

import os
import sys
import json
import time
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
from enum import Enum

class SkillStatus(Enum):
    """技能状态"""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    ERROR = "error"

@dataclass
class SkillInfo:
    """技能信息"""
    name: str
    description: str
    version: str = "1.0.0"
    author: str = "DNASPEC System"
    keywords: List[str] = None
    confidence: float = 0.0
    execution_time: float = 0.0
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []

@dataclass
class SkillResult:
    """技能执行结果"""
    skill_name: str
    status: SkillStatus
    result: Any
    confidence: float
    execution_time: float
    error_message: str = ""
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class DNASpecSkill:
    """DNASPEC技能基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.version = "1.0.0"
        self.created_time = time.time()
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> SkillResult:
        """处理请求"""
        start_time = time.time()
        
        try:
            # 执行具体的技能逻辑
            result_data = self._execute_skill_logic(request, context or {})
            execution_time = time.time() - start_time
            
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.COMPLETED,
                result=result_data,
                confidence=self._calculate_confidence(request),
                execution_time=execution_time,
                metadata={
                    "processed_at": time.time(),
                    "request_length": len(request)
                }
            )
        except Exception as e:
            execution_time = time.time() - start_time
            return SkillResult(
                skill_name=self.name,
                status=SkillStatus.ERROR,
                result=None,
                confidence=0.0,
                execution_time=execution_time,
                error_message=str(e),
                metadata={
                    "processed_at": time.time(),
                    "error_type": type(e).__name__
                }
            )
    
    def _execute_skill_logic(self, request: str, context: Dict[str, Any]) -> Any:
        """执行具体的技能逻辑 - 子类需要实现"""
        raise NotImplementedError("子类必须实现 _execute_skill_logic 方法")
    
    def _calculate_confidence(self, request: str) -> float:
        """计算匹配置信度"""
        # 简单的默认实现
        return 0.8

class SkillManager:
    """技能管理器"""
    
    def __init__(self):
        self.skills: Dict[str, DNASpecSkill] = {}
        self.skill_registry: Dict[str, SkillInfo] = {}
        self._load_skills()
    
    def _load_skills(self):
        """加载所有DNASPEC技能"""
        # 这里应该动态加载实际的技能实现
        # 目前使用模拟数据
        skill_infos = [
            SkillInfo(
                name="dnaspec-agent-creator",
                description="DNASPEC智能体创建器 - 专业的智能体设计和创建专家",
                keywords=["创建智能体", "智能体设计", "agent creator", "多智能体系统", "智能体角色定义", "模块智能化", "agentic", "具身认知", "角色定义", "行为规范", "智能体架构"]
            ),
            SkillInfo(
                name="dnaspec-task-decomposer",
                description="DNASPEC任务分解器 - 复杂任务分解和原子化专家",
                keywords=["分解任务", "任务分解", "原子化任务", "任务依赖分析", "复杂任务", "一步步拆解", "任务分析", "任务清单", "任务计划", "任务依赖", "原子化", "开发任务"]
            ),
            SkillInfo(
                name="dnaspec-constraint-generator",
                description="DNASPEC约束生成器 - 系统约束和规范生成专家",
                keywords=["生成约束", "约束生成", "API规范", "数据约束", "约束规范", "规范生成", "接口约束", "数据规范", "系统约束"]
            ),
            SkillInfo(
                name="dnaspec-dapi-checker",
                description="DNASPEC分布式接口检查器 - 接口一致性和完整性检查专家",
                keywords=["接口检查", "一致性检查", "接口验证", "参数不一致", "接口不匹配", "参数错误", "接口错误", "定义不一致", "接口不一致", "API验证", "参数匹配", "支付接口", "用户服务"]
            ),
            SkillInfo(
                name="dnaspec-modulizer",
                description="DNASPEC模块化器 - 模块成熟度检查和封装专家",
                keywords=["模块化", "模块重构", "隔离测试", "分区测试", "系统重构", "模块成熟化", "封装", "自底向上", "降低系统复杂度", "成熟度评估", "模块封装", "订单处理", "用户管理"]
            ),
            SkillInfo(
                name="dnaspec-architect",
                description="DNASPEC架构师 - 系统架构设计和协调专家",
                keywords=["系统架构", "架构设计", "架构规划", "多层架构", "architecture", "design system", "微服务", "技术栈", "模块划分", "电商系统"]
            ),
            SkillInfo(
                name="dnaspec-system-architect",
                description="DNASPEC系统架构师 - 具体系统架构设计专家",
                keywords=["技术栈选择", "模块划分", "接口定义", "系统设计", "blueprint", "framework", "系统架构"]
            )
        ]
        
        for skill_info in skill_infos:
            self.skill_registry[skill_info.name] = skill_info
        
        # 注册实际的技能实例（如果可用）
        self._register_actual_skills()
    
    def _register_actual_skills(self):
        """注册实际的技能实例"""
        try:
            # 尝试导入并注册实际的技能实例
            from .src.dnaspec_agent_creator import agent_creator
            from .src.dnaspec_task_decomposer import task_decomposer
            from .src.dnaspec_dapi_checker import dapi_checker
            from .src.dnaspec_modulizer import modulizer
            
            self.skills["dnaspec-agent-creator"] = agent_creator
            self.skills["dnaspec-task-decomposer"] = task_decomposer
            self.skills["dnaspec-dapi-checker"] = dapi_checker
            self.skills["dnaspec-modulizer"] = modulizer
            
            # 更新技能信息
            if "dnaspec-agent-creator" in self.skill_registry:
                self.skill_registry["dnaspec-agent-creator"].version = agent_creator.get_skill_info()["version"] if hasattr(agent_creator, "get_skill_info") else "1.0.0"
            
            if "dnaspec-task-decomposer" in self.skill_registry:
                self.skill_registry["dnaspec-task-decomposer"].version = task_decomposer.get_skill_info()["version"] if hasattr(task_decomposer, "get_skill_info") else "1.0.0"
                
            if "dnaspec-dapi-checker" in self.skill_registry:
                self.skill_registry["dnaspec-dapi-checker"].version = dapi_checker.get_skill_info()["version"] if hasattr(dapi_checker, "get_skill_info") else "1.0.0"
                
            if "dnaspec-modulizer" in self.skill_registry:
                self.skill_registry["dnaspec-modulizer"].version = modulizer.get_skill_info()["version"] if hasattr(modulizer, "get_skill_info") else "1.0.0"
                
        except ImportError as e:
            # 如果无法导入实际技能，使用默认处理
            pass
    
    def register_skill(self, skill: DNASpecSkill):
        """注册技能"""
        self.skills[skill.name] = skill
        if skill.name in self.skill_registry:
            # 更新技能信息
            skill_info = self.skill_registry[skill.name]
            skill_info.version = skill.version
    
    def get_skill(self, name: str) -> Optional[DNASpecSkill]:
        """获取技能"""
        return self.skills.get(name)
    
    def get_skill_info(self, name: str) -> Optional[SkillInfo]:
        """获取技能信息"""
        return self.skill_registry.get(name)
    
    def list_skills(self) -> List[SkillInfo]:
        """列出所有技能"""
        return list(self.skill_registry.values())
    
    def match_skill(self, request: str) -> Optional[SkillInfo]:
        """匹配技能"""
        request_lower = request.lower()
        best_match = None
        best_confidence = 0.0
        
        for skill_info in self.skill_registry.values():
            confidence = self._calculate_match_confidence(request_lower, skill_info)
            if confidence > best_confidence and confidence > 0.1:  # 阈值
                best_confidence = confidence
                best_match = skill_info
                best_match.confidence = confidence
        
        return best_match
    
    def _calculate_match_confidence(self, request: str, skill_info: SkillInfo) -> float:
        """计算匹配置信度"""
        confidence = 0.0
        
        # 1. 关键词匹配 (权重0.6)
        keyword_matches = 0
        for keyword in skill_info.keywords:
            if keyword.lower() in request:
                keyword_matches += 1
        
        if keyword_matches > 0:
            confidence += 0.6 * min(keyword_matches / len(skill_info.keywords), 1.0)
        
        # 2. 技能名称匹配 (权重0.3)
        if skill_info.name.lower() in request:
            confidence += 0.3
        
        # 3. 描述匹配 (权重0.1)
        desc_words = set(re.findall(r'[\w\u4e00-\u9fff]+', skill_info.description.lower()))
        request_words = set(re.findall(r'[\w\u4e00-\u9fff]+', request))
        common_words = len(desc_words.intersection(request_words))
        
        if common_words > 0:
            confidence += 0.1 * min(common_words / len(desc_words), 1.0)
        
        return min(confidence, 1.0)

# 全局技能管理器实例
skill_manager = SkillManager()

def get_skill_manager() -> SkillManager:
    """获取全局技能管理器"""
    return skill_manager

if __name__ == "__main__":
    # 测试技能管理器
    manager = get_skill_manager()
    
    print("=== DNASPEC Skills 核心框架测试 ===")
    print(f"已加载 {len(manager.list_skills())} 个技能:")
    
    for skill_info in manager.list_skills():
        print(f"  - {skill_info.name}: {skill_info.description}")
    
    # 测试技能匹配
    test_requests = [
        "创建一个项目管理智能体",
        "分解复杂的软件开发任务",
        "生成API接口约束规范",
        "检查微服务接口一致性",
        "对系统进行模块化重构"
    ]
    
    print("\n技能匹配测试:")
    for request in test_requests:
        matched_skill = manager.match_skill(request)
        if matched_skill:
            print(f"  '{request}' -> {matched_skill.name} (置信度: {matched_skill.confidence:.2f})")
        else:
            print(f"  '{request}' -> 无匹配技能")