# dnaspec-architect主技能基础实现

import os
import sys
from typing import Dict, Any

class DSGSArchitect:
    """DSGS智能架构师主技能类"""
    
    def __init__(self):
        """初始化主技能"""
        self.name = "dnaspec-architect"
        self.description = "DSGS智能架构师主技能，用于复杂项目的分层架构设计、任务分解、智能体化和约束生成"
        self.subskills = [
            'dnaspec-system-architect',
            'dnaspec-task-decomposer', 
            'dnaspec-agent-creator',
            'dnaspec-constraint-generator'
        ]
    
    def process_request(self, request: str) -> Dict[str, Any]:
        """处理用户请求"""
        if not request or not request.strip():
            return {"error": "请求不能为空"}
        
        # 简单的请求路由逻辑（将在后续实现中完善）
        result = {
            "status": "processed",
            "request": request,
            "skill_used": self._route_request(request),
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _route_request(self, request: str) -> str:
        """根据请求内容路由到相应的子技能"""
        request_lower = request.lower()
        
        # 检查多个关键词组合以提高路由准确性
        # 优先检查特定关键词，避免冲突
        if "constraint" in request_lower or "约束" in request_lower or ("generate" in request_lower and "constraint" in request_lower):
            return "dnaspec-constraint-generator"
        elif "architect" in request_lower or "design" in request_lower or ("architecture" in request_lower and "design" in request_lower):
            return "dnaspec-system-architect"
        elif "decompos" in request_lower or "task" in request_lower:
            return "dnaspec-task-decomposer"
        elif "agent" in request_lower or "智能体" in request_lower:
            return "dnaspec-agent-creator"
        else:
            return "dnaspec-system-architect"  # 默认路由
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "subskills": self.subskills
        }

# 全局实例
architect = DSGSArchitect()

if __name__ == "__main__":
    # 简单测试
    print("DNASPEC Architect Skill Loaded")
    print(f"Skill Name: {architect.name}")
    print(f"Description: {architect.description}")