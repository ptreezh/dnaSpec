# dnaspec-dapi-checker子技能实现

import os
import sys
import json
import re
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class InterfaceDefinition:
    """接口定义"""
    name: str
    type: str  # external, internal, abstract
    level: str  # system, module, component, function
    signature: Dict[str, Any]
    documentation: str
    implementation_path: Optional[str] = None

@dataclass
class InconsistencyIssue:
    """不一致问题"""
    interface_name: str
    issue_type: str  # missing, mismatch, incomplete
    description: str
    severity: str  # critical, high, medium, low
    location: str
    suggested_fix: str

@dataclass
class ConsistencyReport:
    """一致性检查报告"""
    system_name: str
    scan_time: str
    total_interfaces: int
    checked_interfaces: int
    issues_found: List[InconsistencyIssue]
    summary: Dict[str, int]
    recommendations: List[str]

class DNASPEC_DAPI_Checker:
    """DNASPEC分布式接口一致性检测器"""
    
    def __init__(self):
        """初始化DAPI检查器"""
        self.name = "dnaspec-dapi-checker"
        self.description = "DNASPEC分布式接口文档检查器，用于检查系统各组件间的接口一致性和完整性"
        self.capabilities = [
            "interface_scanning",
            "consistency_checking",
            "documentation_verification",
            "issue_reporting"
        ]
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置"""
        default_config = {
            "scan_levels": ["system", "module", "component", "function"],
            "interface_types": ["external", "internal", "abstract"],
            "consistency_checks": ["signature", "behavior", "contract", "documentation"]
        }
        return default_config
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理接口一致性检查请求"""
        if not request or not request.strip():
            return {"error": "请求不能为空"}
        
        # 分析请求并执行接口检查
        check_result = self._perform_interface_consistency_check(request, context or {})
        
        result = {
            "status": "completed",
            "skill": self.name,
            "request": request,
            "check_result": check_result,
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _perform_interface_consistency_check(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """执行接口一致性检查"""
        # 提取关键信息
        key_points = self._extract_key_points(request)
        
        # 执行检查
        report = self._generate_consistency_report(request, key_points, context)
        
        return asdict(report)
    
    def _extract_key_points(self, request: str) -> List[str]:
        """从请求中提取关键点"""
        keywords = []
        request_lower = request.lower()
        
        if "api" in request_lower or "接口" in request_lower:
            keywords.append("api_interface")
        if "system" in request_lower or "系统" in request_lower:
            keywords.append("system_level")
        if "module" in request_lower or "模块" in request_lower:
            keywords.append("module_level")
        if "component" in request_lower or "组件" in request_lower:
            keywords.append("component_level")
        if "check" in request_lower or "检查" in request_lower:
            keywords.append("consistency_check")
        if "document" in request_lower or "文档" in request_lower:
            keywords.append("documentation")
            
        return keywords
    
    def _generate_consistency_report(self, request: str, key_points: List[str], context: Dict[str, Any]) -> ConsistencyReport:
        """生成一致性检查报告"""
        # 模拟接口扫描和检查过程
        interfaces = self._scan_interfaces(request, context)
        issues = self._check_consistency(interfaces, context)
        
        # 生成统计摘要
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        for issue in issues:
            severity_counts[issue.severity] += 1
        
        summary = {
            "total_issues": len(issues),
            "critical_issues": severity_counts["critical"],
            "high_issues": severity_counts["high"],
            "medium_issues": severity_counts["medium"],
            "low_issues": severity_counts["low"],
            "compliance_rate": self._calculate_compliance_rate(len(interfaces), len(issues))
        }
        
        # 生成建议
        recommendations = self._generate_recommendations(issues, interfaces)
        
        return ConsistencyReport(
            system_name="Sample System",
            scan_time=self._get_timestamp(),
            total_interfaces=len(interfaces),
            checked_interfaces=len(interfaces),
            issues_found=issues,
            summary=summary,
            recommendations=recommendations
        )
    
    def _scan_interfaces(self, request: str, context: Dict[str, Any]) -> List[InterfaceDefinition]:
        """扫描接口定义"""
        # 模拟接口扫描
        interfaces = [
            InterfaceDefinition(
                name="UserServiceAPI",
                type="external",
                level="system",
                signature={"method": "GET", "path": "/users/{id}", "parameters": ["id"]},
                documentation="用户服务API接口文档",
                implementation_path="/src/user/UserService.java"
            ),
            InterfaceDefinition(
                name="DataProcessorInterface",
                type="internal",
                level="module",
                signature={"method": "process", "input": "Data", "output": "ProcessedData"},
                documentation="数据处理器内部接口",
                implementation_path="/src/processor/DataProcessor.py"
            ),
            InterfaceDefinition(
                name="NotificationAbstract",
                type="abstract",
                level="component",
                signature={"method": "send", "parameters": ["message", "recipient"]},
                documentation="通知服务抽象接口"
            )
        ]
        return interfaces
    
    def _check_consistency(self, interfaces: List[InterfaceDefinition], context: Dict[str, Any]) -> List[InconsistencyIssue]:
        """检查接口一致性"""
        issues = []
        
        # 模拟一致性检查
        for interface in interfaces:
            # 检查实现是否存在
            if not interface.implementation_path:
                issues.append(InconsistencyIssue(
                    interface_name=interface.name,
                    issue_type="missing",
                    description=f"接口 {interface.name} 缺少实现文件",
                    severity="high",
                    location="implementation",
                    suggested_fix=f"为接口 {interface.name} 创建实现文件"
                ))
            
            # 检查文档完整性
            if len(interface.documentation) < 20:
                issues.append(InconsistencyIssue(
                    interface_name=interface.name,
                    issue_type="incomplete",
                    description=f"接口 {interface.name} 的文档不完整",
                    severity="medium",
                    location="documentation",
                    suggested_fix=f"完善接口 {interface.name} 的文档说明"
                ))
        
        return issues
    
    def _calculate_compliance_rate(self, total_interfaces: int, issues_count: int) -> float:
        """计算合规率"""
        if total_interfaces == 0:
            return 100.0
        return max(0.0, (total_interfaces - issues_count) / total_interfaces * 100)
    
    def _generate_recommendations(self, issues: List[InconsistencyIssue], interfaces: List[InterfaceDefinition]) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于发现的问题生成建议
        critical_issues = [issue for issue in issues if issue.severity == "critical"]
        if critical_issues:
            recommendations.append("立即修复关键接口问题，确保系统稳定性")
        
        missing_implementations = [issue for issue in issues if issue.issue_type == "missing"]
        if missing_implementations:
            recommendations.append("为缺少实现的接口创建相应的实现代码")
        
        incomplete_docs = [issue for issue in issues if "文档" in issue.description]
        if incomplete_docs:
            recommendations.append("完善接口文档，确保文档与实现一致")
        
        # 通用建议
        recommendations.extend([
            "定期执行接口一致性检查",
            "建立接口变更的审批流程",
            "维护接口版本兼容性",
            "实施自动化接口测试"
        ])
        
        return recommendations
    
    def _get_timestamp(self) -> str:
        """获取当前时间戳"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def get_skill_info(self) -> Dict[str, Any]:
        """获取技能信息"""
        return {
            "name": self.name,
            "description": self.description,
            "capabilities": self.capabilities
        }

# 全局实例
dapi_checker = DNASPEC_DAPI_Checker()

if __name__ == "__main__":
    # 简单测试
    print("DNASPEC DAPI Checker Skill Loaded")
    print(f"Skill Name: {dapi_checker.name}")
    print(f"Description: {dapi_checker.description}")