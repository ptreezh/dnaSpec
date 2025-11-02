# dsgs-constraint-generator子技能实现

import os
import sys
from typing import Dict, Any, List

class DSGSConstraintGenerator:
    """DSGS约束生成器子技能类"""
    
    def __init__(self):
        """初始化约束生成器技能"""
        self.name = "dsgs-constraint-generator"
        self.description = "DSGS约束生成器子技能，用于根据项目需求和架构设计生成系统约束、API规范约束、数据约束和质量约束"
        self.capabilities = [
            "system_constraint_generation",
            "api_constraint_definition",
            "data_constraint_validation",
            "quality_constraint_specification"
        ]
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理约束生成请求"""
        if not request or not request.strip():
            return {"error": "请求不能为空"}
        
        # 分析请求并生成约束
        constraint_specification = self._generate_constraint_specification(request, context or {})
        
        result = {
            "status": "completed",
            "skill": self.name,
            "request": request,
            "constraint_specification": constraint_specification,
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _generate_constraint_specification(self, request: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """生成约束规范"""
        # 这里是约束生成的核心逻辑
        # 在实际实现中，这将是一个复杂的分析和约束生成过程
        
        # 提取关键信息
        key_points = self._extract_key_points(request)
        
        # 生成约束规范
        specification = {
            "system_constraints": self._generate_system_constraints(request, key_points),
            "api_constraints": self._generate_api_constraints(request, key_points),
            "data_constraints": self._generate_data_constraints(request, key_points),
            "quality_constraints": self._generate_quality_constraints(request, key_points),
            "validation_mechanisms": self._define_validation_mechanisms(request, key_points)
        }
        
        return specification
    
    def _extract_key_points(self, request: str) -> List[str]:
        """从请求中提取关键点"""
        # 简单的关键词提取（实际实现中会更复杂）
        keywords = []
        request_lower = request.lower()
        
        if "web" in request_lower or "website" in request_lower:
            keywords.append("web_application")
        if "mobile" in request_lower or "app" in request_lower:
            keywords.append("mobile_app")
        if "api" in request_lower:
            keywords.append("api_service")
        if "database" in request_lower or "data" in request_lower:
            keywords.append("data_processing")
        if "ui" in request_lower or "interface" in request_lower:
            keywords.append("user_interface")
        if "security" in request_lower or "secure" in request_lower:
            keywords.append("security_constraint")
        if "performance" in request_lower or "perf" in request_lower:
            keywords.append("performance_constraint")
        if "testing" in request_lower:
            keywords.append("testing_constraint")
        if "monitor" in request_lower:
            keywords.append("monitoring_constraint")
        if "constraint" in request_lower or "规范" in request_lower:
            keywords.append("general_constraint")
            
        return keywords
    
    def _generate_system_constraints(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """生成系统约束"""
        constraints = []
        
        # 基于关键点生成系统约束
        for point in key_points:
            if point == "web_application":
                constraints.extend([
                    {
                        "id": "sys_web_001",
                        "name": "前端性能约束",
                        "category": "performance",
                        "type": "system",
                        "constraint": "页面加载时间不超过3秒",
                        "severity": "high",
                        "validation_method": "前端性能监控"
                    },
                    {
                        "id": "sys_web_002",
                        "name": "跨浏览器兼容性约束",
                        "category": "compatibility",
                        "type": "system",
                        "constraint": "支持Chrome、Firefox、Safari、Edge最新版本",
                        "severity": "medium",
                        "validation_method": "自动化兼容性测试"
                    }
                ])
            elif point == "mobile_app":
                constraints.extend([
                    {
                        "id": "sys_mobile_001",
                        "name": "移动端性能约束",
                        "category": "performance",
                        "type": "system",
                        "constraint": "应用启动时间不超过2秒",
                        "severity": "high",
                        "validation_method": "性能基准测试"
                    },
                    {
                        "id": "sys_mobile_002",
                        "name": "电池消耗约束",
                        "category": "efficiency",
                        "type": "system",
                        "constraint": "后台运行时电池消耗不超过5%/小时",
                        "severity": "medium",
                        "validation_method": "电池使用监控"
                    }
                ])
            elif point == "security_constraint":
                constraints.append({
                    "id": "sys_sec_001",
                    "name": "安全加密约束",
                    "category": "security",
                    "type": "system",
                    "constraint": "所有数据传输必须使用TLS 1.3加密",
                    "severity": "critical",
                    "validation_method": "安全扫描和审计"
                })
        
        # 默认系统约束
        if not constraints:
            constraints = [
                {
                    "id": "sys_gen_001",
                    "name": "系统可用性约束",
                    "category": "availability",
                    "type": "system",
                    "constraint": "系统可用性不低于99.9%",
                    "severity": "high",
                    "validation_method": "系统监控"
                },
                {
                    "id": "sys_gen_002",
                    "name": "系统性能约束",
                    "category": "performance",
                    "type": "system",
                    "constraint": "响应时间不超过2秒",
                    "severity": "medium",
                    "validation_method": "性能监控"
                }
            ]
        
        return constraints
    
    def _generate_api_constraints(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """生成API约束"""
        constraints = []
        
        # 基于关键点生成API约束
        for point in key_points:
            if point == "api_service":
                constraints.extend([
                    {
                        "id": "api_rest_001",
                        "name": "REST API规范约束",
                        "category": "api_design",
                        "type": "api",
                        "constraint": "遵循RESTful API设计规范",
                        "severity": "high",
                        "validation_method": "API规范验证工具"
                    },
                    {
                        "id": "api_rate_001",
                        "name": "API速率限制约束",
                        "category": "rate_limiting",
                        "type": "api",
                        "constraint": "API请求速率限制为1000次/分钟/用户",
                        "severity": "medium",
                        "validation_method": "速率限制中间件"
                    }
                ])
        
        # 默认API约束
        if "api_service" in key_points or "general_constraint" in key_points:
            constraints.extend([
                {
                    "id": "api_sec_001",
                    "name": "API安全约束",
                    "category": "security",
                    "type": "api",
                    "constraint": "所有API端点必须使用认证和授权",
                    "severity": "critical",
                    "validation_method": "安全测试工具"
                },
                {
                    "id": "api_doc_001",
                    "name": "API文档约束",
                    "category": "documentation",
                    "type": "api",
                    "constraint": "API必须提供完整的OpenAPI文档",
                    "severity": "medium",
                    "validation_method": "文档验证工具"
                }
            ])
        
        return constraints
    
    def _generate_data_constraints(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """生成数据约束"""
        constraints = []
        
        # 基于关键点生成数据约束
        for point in key_points:
            if point == "data_processing":
                constraints.extend([
                    {
                        "id": "data_val_001",
                        "name": "数据验证约束",
                        "category": "validation",
                        "type": "data",
                        "constraint": "所有输入数据必须经过验证和清理",
                        "severity": "high",
                        "validation_method": "数据验证中间件"
                    },
                    {
                        "id": "data_priv_001",
                        "name": "数据隐私约束",
                        "category": "privacy",
                        "type": "data",
                        "constraint": "遵循GDPR等数据隐私法规",
                        "severity": "critical",
                        "validation_method": "隐私合规检查"
                    }
                ])
        
        # 默认数据约束
        if "data_processing" in key_points or "general_constraint" in key_points:
            constraints.extend([
                {
                    "id": "data_int_001",
                    "name": "数据完整性约束",
                    "category": "integrity",
                    "type": "data",
                    "constraint": "确保数据的ACID属性",
                    "severity": "high",
                    "validation_method": "数据库约束和事务管理"
                },
                {
                    "id": "data_backup_001",
                    "name": "数据备份约束",
                    "category": "reliability",
                    "type": "data",
                    "constraint": "数据备份频率不低于每日一次",
                    "severity": "medium",
                    "validation_method": "备份验证工具"
                }
            ])
        
        return constraints
    
    def _generate_quality_constraints(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """生成质量约束"""
        constraints = []
        
        # 基于关键点生成质量约束
        for point in key_points:
            if point == "testing_constraint":
                constraints.append({
                    "id": "qual_test_001",
                    "name": "测试覆盖率约束",
                    "category": "testing",
                    "type": "quality",
                    "constraint": "代码测试覆盖率不低于80%",
                    "severity": "high",
                    "validation_method": "代码覆盖率工具"
                })
            elif point == "performance_constraint":
                constraints.append({
                    "id": "qual_perf_001",
                    "name": "性能指标约束",
                    "category": "performance",
                    "type": "quality",
                    "constraint": "系统响应时间95%在2秒以内",
                    "severity": "high",
                    "validation_method": "性能监控工具"
                })
        
        # 默认质量约束
        if not constraints:
            constraints = [
                {
                    "id": "qual_code_001",
                    "name": "代码质量约束",
                    "category": "code_quality",
                    "type": "quality",
                    "constraint": "代码必须通过静态分析和代码审查",
                    "severity": "medium",
                    "validation_method": "代码质量工具"
                },
                {
                    "id": "qual_doc_001",
                    "name": "文档质量约束",
                    "category": "documentation",
                    "type": "quality",
                    "constraint": "每个功能模块必须有完整的文档",
                    "severity": "low",
                    "validation_method": "文档审查"
                }
            ]
        
        return constraints
    
    def _define_validation_mechanisms(self, request: str, key_points: List[str]) -> List[Dict[str, Any]]:
        """定义验证机制"""
        mechanisms = []
        
        # 基于关键点定义验证机制
        if "security_constraint" in key_points:
            mechanisms.extend([
                {
                    "type": "security_scan",
                    "tool": "OWASP ZAP, SonarQube",
                    "frequency": "continuous",
                    "scope": "security_validation"
                }
            ])
        
        if "testing_constraint" in key_points:
            mechanisms.extend([
                {
                    "type": "test_automation",
                    "tool": "Jest, PyTest, Selenium",
                    "frequency": "continuous",
                    "scope": "functional_validation"
                }
            ])
        
        # 默认验证机制
        if not mechanisms:
            mechanisms = [
                {
                    "type": "code_quality",
                    "tool": "ESLint, Pylint, SonarQube",
                    "frequency": "continuous",
                    "scope": "code_validation"
                },
                {
                    "type": "performance_monitoring",
                    "tool": "Prometheus, Grafana",
                    "frequency": "continuous",
                    "scope": "performance_validation"
                }
            ]
        
        return mechanisms
    
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
constraint_generator = DSGSConstraintGenerator()

if __name__ == "__main__":
    # 简单测试
    print("DSGS Constraint Generator Skill Loaded")
    print(f"Skill Name: {constraint_generator.name}")
    print(f"Description: {constraint_generator.description}")