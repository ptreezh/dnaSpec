"""
API检查技能实现 - 实现分级审核和多层级调用对齐检查
确保模块级、子系统级、系统级的接口一致性和调用对齐
"""
import json
import re
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
from datetime import datetime

class ApiLevel(Enum):
    """API等级枚举"""
    MODULE = "module"
    SUBSYSTEM = "subsystem"
    SYSTEM = "system"

@dataclass
class ApiSpecification:
    """API规范定义"""
    name: str
    version: str
    endpoints: List[Dict[str, Any]]  # [{"path": str, "method": str, "description": str, "params": [], "responses": []}]
    level: ApiLevel
    dependencies: List[str] = None  # 依赖的其他API

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class LevelBasedValidator:
    """基于级别的验证器"""

    def __init__(self):
        self.validation_rules = {
            ApiLevel.MODULE.value: {
                "max_endpoints": 10,
                "max_params_per_endpoint": 5,
                "naming_pattern": r'^/[a-z0-9/-]+$',
                "required_fields": ["path", "method", "description"]
            },
            ApiLevel.SUBSYSTEM.value: {
                "max_endpoints": 50,
                "max_params_per_endpoint": 10,
                "naming_pattern": r'^/[a-z0-9/-_/]+$',  # 允许更复杂的路径
                "required_fields": ["path", "method", "description", "params", "responses"]
            },
            ApiLevel.SYSTEM.value: {
                "max_endpoints": 200,
                "max_params_per_endpoint": 20,
                "naming_pattern": r'^/[a-z0-9/-_/<>]+$',  # 允许最复杂的路径
                "required_fields": ["path", "method", "description", "params", "responses", "dependencies"]
            }
        }

    def validate_api_spec(self, api_spec: ApiSpecification) -> Dict[str, Any]:
        """验证API规范是否符合对应级别的要求"""
        level_rules = self.validation_rules.get(api_spec.level.value, self.validation_rules[ApiLevel.MODULE.value])
        issues = []

        # 检查端点数量
        if len(api_spec.endpoints) > level_rules["max_endpoints"]:
            issues.append({
                "type": "limit_exceeded",
                "severity": "high",
                "message": f"端点数量({len(api_spec.endpoints)})超出{api_spec.level.value}级限制({level_rules['max_endpoints']})"
            })

        # 检查每个端点
        for i, endpoint in enumerate(api_spec.endpoints):
            # 检查路径格式
            path = endpoint.get("path", "")
            if not re.match(level_rules["naming_pattern"], path):
                issues.append({
                    "type": "invalid_path",
                    "severity": "medium",
                    "message": f"端点{i}的路径 '{path}' 不符合{api_spec.level.value}级命名规范"
                })

            # 检查参数数量
            params = endpoint.get("params", [])
            if len(params) > level_rules["max_params_per_endpoint"]:
                issues.append({
                    "type": "param_limit_exceeded",
                    "severity": "high",
                    "message": f"端点{i}的参数数量({len(params)})超出{api_spec.level.value}级限制({level_rules['max_params_per_endpoint']})"
                })

            # 检查必需字段
            for field in level_rules["required_fields"]:
                if field not in endpoint:
                    issues.append({
                        "type": "missing_field",
                        "severity": "high",
                        "message": f"端点{i}缺少必需字段: {field}"
                    })

        # 计算合规性分数
        total_checks = 10  # 虚拟总数
        failed_checks = len(issues)
        compliance_score = max(0, (total_checks - failed_checks) / total_checks) if total_checks > 0 else 1.0

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "compliance_score": compliance_score,
            "level": api_spec.level.value,
            "total_endpoints": len(api_spec.endpoints)
        }

class MultiLevelAligner:
    """多层级对齐器"""

    def __init__(self):
        self.call_alignment_matrix = {
            "module_to_module": True,
            "module_to_subsystem": True,
            "module_to_system": False,  # 模块不应直接调用系统级接口
            "subsystem_to_module": True,
            "subsystem_to_subsystem": True,
            "subsystem_to_system": True,
            "system_to_any": True
        }

    def validate_interlevel_alignment(self, caller_spec: ApiSpecification, callee_spec: ApiSpecification) -> Dict[str, Any]:
        """验证不同层级间调用的对齐性"""
        alignment_key = f"{caller_spec.level.value}_to_{callee_spec.level.value}"
        is_allowed = self.call_alignment_matrix.get(alignment_key, False)

        alignment_report = {
            "caller_level": caller_spec.level.value,
            "callee_level": callee_spec.level.value,
            "is_allowed": is_allowed,
            "alignment_status": "PASS" if is_allowed else "FAIL"
        }

        issues = []
        if not is_allowed:
            issues.append({
                "type": "invalid_call",
                "severity": "high",
                "message": f"无效调用: {caller_spec.level.value}级API不应直接调用{callee_spec.level.value}级API"
            })

        # 验证接口兼容性
        compat_issues = self._check_interface_compatibility(caller_spec, callee_spec)
        issues.extend(compat_issues)

        return {
            "is_aligned": is_allowed and len(compat_issues) == 0,
            "issues": issues,
            "alignment_report": alignment_report,
            "interface_compatibility": len(compat_issues) == 0
        }

    def _check_interface_compatibility(self, caller: ApiSpecification, callee: ApiSpecification) -> List[Dict[str, Any]]:
        """检查接口兼容性"""
        issues = []

        # 简化的兼容性检查
        # 检查caller是否引用了callee中存在的端点
        for caller_endpoint in caller.endpoints:
            caller_path = caller_endpoint.get("path")
            for callee_endpoint in callee.endpoints:
                callee_path = callee_endpoint.get("path")
                if caller_path == callee_path:
                    # 检查方法兼容性
                    caller_method = caller_endpoint.get("method")
                    callee_method = callee_endpoint.get("method")
                    if caller_method != callee_method:
                        issues.append({
                            "type": "method_mismatch",
                            "severity": "high",
                            "message": f"调用方法不匹配: 调用者使用'{caller_method}', 被调用者为'{callee_method}'"
                        })

        return issues

class ScopeBoundaryManager:
    """作用域边界管理者"""

    def __init__(self):
        self.boundaries = {}

    def define_scope_boundary(self, boundary_config: Dict[str, Any]) -> Dict[str, Any]:
        """定义作用域边界"""
        boundary_id = f"SCOPE-{uuid.uuid4().hex[:8]}"

        # 验证边界配置
        required_fields = ["module", "allowed_calls", "forbidden_calls"]
        missing_fields = [field for field in required_fields if field not in boundary_config]

        if missing_fields:
            return {
                "success": False,
                "error": f"边界配置缺少必需字段: {missing_fields}",
                "boundary_id": boundary_id
            }

        self.boundaries[boundary_id] = boundary_config
        self.boundaries[boundary_id]["created_at"] = datetime.now().isoformat()

        # 检查边界配置的一致性
        consistency_issues = self._check_boundary_consistency(boundary_config)

        return {
            "success": True,
            "boundary_id": boundary_id,
            "consistency_issues": consistency_issues,
            "validation_status": "PASS" if not consistency_issues else "WARN"
        }

    def _check_boundary_consistency(self, boundary_config: Dict[str, Any]) -> List[Dict[str, Any]]:
        """检查边界配置一致性"""
        issues = []

        # 检查允许和禁止调用是否有冲突
        allowed_calls = set(boundary_config.get("allowed_calls", []))
        forbidden_calls = set(boundary_config.get("forbidden_calls", []))

        conflicting_calls = allowed_calls.intersection(forbidden_calls)
        if conflicting_calls:
            issues.append({
                "type": "boundary_conflict",
                "severity": "high",
                "message": f"边界配置中允许和禁止调用存在冲突: {conflicting_calls}"
            })

        return issues

    def validate_call_within_boundary(self, caller: str, callee: str, boundary_id: str) -> bool:
        """验证调用是否在边界内"""
        boundary = self.boundaries.get(boundary_id)
        if not boundary:
            return False

        allowed_calls = boundary.get("allowed_calls", [])
        forbidden_calls = boundary.get("forbidden_calls", [])

        call_identifier = f"{caller} -> {callee}"

        # 如果在禁止列表中，则不允许
        if call_identifier in forbidden_calls:
            return False

        # 如果允许列表为空或调用在允许列表中，则允许
        if not allowed_calls or call_identifier in allowed_calls:
            return True

        return False

class ApiChecker:
    """API检查器主类"""

    def __init__(self):
        self.validator = LevelBasedValidator()
        self.aligner = MultiLevelAligner()
        self.scope_manager = ScopeBoundaryManager()
        self.timecapsules = {}  # 存储API审核时间胶囊

    def check_api_consistency(self, api_specs: Union[Dict[str, Any], List[Dict[str, Any]]],
                             detail_level: str = "standard") -> Dict[str, Any]:
        """检查API一致性"""
        # 如果是字典格式，转换为API规范对象列表
        if isinstance(api_specs, dict) and "apis" in api_specs:
            api_specs_list = api_specs["apis"]
        elif isinstance(api_specs, dict):
            # 假设单个API规范
            api_specs_list = [api_specs]
        else:
            api_specs_list = api_specs

        # 将字典格式转换为对象格式
        parsed_api_specs = []
        for api_dict in api_specs_list:
            level_str = api_dict.get("level", "module")
            try:
                level = ApiLevel(level_str)
            except ValueError:
                level = ApiLevel.MODULE  # 默认为模块级

            spec = ApiSpecification(
                name=api_dict.get("name", f"api-{uuid.uuid4().hex[:8]}"),
                version=api_dict.get("version", "1.0"),
                endpoints=api_dict.get("endpoints", []),
                level=level,
                dependencies=api_dict.get("dependencies", [])
            )
            parsed_api_specs.append(spec)

        results = {
            "api_specs_evaluated": len(parsed_api_specs),
            "level_validation_results": [],
            "interlevel_alignment_results": [],
            "scope_boundary_issues": [],
            "overall_compliance": 0.0,
            "recommendations": [],
            "total_issues": 0
        }

        # 验证每个API规范的级别要求
        total_validations = 0
        compliant_validations = 0

        for api_spec in parsed_api_specs:
            level_result = self.validator.validate_api_spec(api_spec)
            results["level_validation_results"].append({
                "api_name": api_spec.name,
                "level": api_spec.level.value,
                "validation_result": level_result,
                "endpoint_count": level_result.get("total_endpoints", 0)
            })

            total_validations += 1
            if level_result["valid"]:
                compliant_validations += 1
            results["total_issues"] += len(level_result["issues"])

        # 检查层级间对齐
        for i in range(len(parsed_api_specs)):
            for j in range(i + 1, len(parsed_api_specs)):
                align_result = self.aligner.validate_interlevel_alignment(parsed_api_specs[i], parsed_api_specs[j])
                results["interlevel_alignment_results"].append({
                    "caller": parsed_api_specs[i].name,
                    "callee": parsed_api_specs[j].name,
                    "caller_level": parsed_api_specs[i].level.value,
                    "callee_level": parsed_api_specs[j].level.value,
                    "alignment_result": align_result
                })

                if not align_result["is_aligned"]:
                    results["total_issues"] += len(align_result["issues"])

        # 计算整体合规性
        level_compliance = compliant_validations / total_validations if total_validations > 0 else 1.0
        total_alignments = len(results["interlevel_alignment_results"])
        if total_alignments > 0:
            aligned_count = sum(1 for item in results["interlevel_alignment_results"]
                              if item["alignment_result"]["is_aligned"])
            alignment_compliance = aligned_count / total_alignments
        else:
            alignment_compliance = 1.0  # 没有对齐检查时默认合规

        results["overall_compliance"] = (level_compliance + alignment_compliance) / 2.0

        # 生成推荐
        recommendations = []
        if level_compliance < 0.8:
            recommendations.append("API规范不符合对应级别要求，建议优化API设计以符合模块/子系统/系统级规范")
        if alignment_compliance < 0.8:
            recommendations.append("API间调用关系不符合层级对齐原则，建议调整调用层级关系")
        if results["overall_compliance"] < 0.8:
            recommendations.append("整体API设计需改进以提高一致性、对齐性和合规性")
        if results["total_issues"] > 0:
            recommendations.append(f"发现{results['total_issues']}个问题，建议优先解决高严重性问题")

        results["recommendations"] = recommendations

        return results

    def create_scope_boundary(self, boundary_config: Dict[str, Any]) -> Dict[str, Any]:
        """创建作用域边界"""
        return self.scope_manager.define_scope_boundary(boundary_config)

    def validate_call_within_scope(self, caller: str, callee: str, boundary_id: str) -> Dict[str, Any]:
        """验证作用域内的调用"""
        is_valid = self.scope_manager.validate_call_within_boundary(caller, callee, boundary_id)

        return {
            "valid": is_valid,
            "boundary_id": boundary_id,
            "call_path": f"{caller} -> {callee}",
            "validation_result": "ALLOWED" if is_valid else "FORBIDDEN"
        }

    def create_review_capsule(self, api_spec: Dict[str, Any], review_result: Dict[str, Any]) -> str:
        """创建API审核时间胶囊"""
        capsule_id = f"APICAPSULE-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6]}"

        self.timecapsules[capsule_id] = {
            "id": capsule_id,
            "api_spec": api_spec,
            "review_result": review_result,
            "timestamp": datetime.now().isoformat(),
            "reviewer": "api-checker"
        }

        return capsule_id

    def get_review_history(self) -> List[Dict[str, Any]]:
        """获取审核历史"""
        return list(self.timecapsules.values())

def execute_api_checker(args: Dict[str, Any]) -> str:
    """
    API检查技能执行函数
    Args:
        args: 包含'api_specs'和可选'detail_level', 'boundary_config'的参数字典
    Returns:
        JSON格式的API检查结果
    """
    api_specs = args.get("api_specs", args.get("input", {}))
    detail_level = args.get("detail_level", "standard")
    boundary_config = args.get("boundary_config", None)

    if not api_specs:
        return json.dumps({
            "success": False,
            "error": "No API specifications provided for checking"
        }, ensure_ascii=False, indent=2)

    checker = ApiChecker()

    # 如果提供了边界配置，先创建边界
    boundary_result = None
    if boundary_config:
        boundary_result = checker.create_scope_boundary(boundary_config)

    # 执行API一致性检查
    check_results = checker.check_api_consistency(api_specs, detail_level)

    # 创建审核时间胶囊
    capsule_id = checker.create_review_capsule(api_specs, check_results)

    result = {
        "success": True,
        "data": {
            "api_check_results": check_results,
            "boundary_setup": boundary_result,
            "detail_level": detail_level,
            "review_capsule_id": capsule_id
        },
        "metadata": {
            "skill_name": "api-checker",
            "execution_time": datetime.now().isoformat(),
            "version": "1.0.0"
        }
    }

    # 根据详细级别调整输出
    if detail_level == "basic":
        result["data"] = {
            "overall_compliance": check_results["overall_compliance"],
            "total_apis": check_results["api_specs_evaluated"],
            "total_issues": check_results["total_issues"],
            "review_capsule_id": capsule_id
        }
    elif detail_level == "detailed":
        result["data"]["recommendations"] = check_results["recommendations"]
        result["data"]["validation_details"] = check_results["level_validation_results"]
        result["data"]["alignment_details"] = check_results["interlevel_alignment_results"]
        result["data"]["review_capsule_id"] = capsule_id
    elif detail_level == "comprehensive":
        result["data"]["full_analysis"] = {
            "level_validation": check_results["level_validation_results"],
            "alignment_validation": check_results["interlevel_alignment_results"],
            "system_recommendations": check_results["recommendations"],
            "compliance_metrics": {
                "level_compliance": sum(1 for vr in check_results["level_validation_results"]
                                      if vr["validation_result"]["valid"]) / len(check_results["level_validation_results"]) if check_results["level_validation_results"] else 1.0,
                "alignment_compliance": sum(1 for ar in check_results["interlevel_alignment_results"]
                                          if ar["alignment_result"]["is_aligned"]) / len(check_results["interlevel_alignment_results"]) if check_results["interlevel_alignment_results"] else 1.0
            }
        }
        result["data"]["review_capsule_id"] = capsule_id

    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试API检查
    test_apis = {
        "apis": [
            {
                "name": "user-service",
                "version": "1.0",
                "endpoints": [
                    {"path": "/api/users", "method": "GET", "description": "Get user list", "params": [], "responses": [{"code": 200}]},
                    {"path": "/api/users", "method": "POST", "description": "Create new user", "params": [{"name": "username", "type": "string"}], "responses": [{"code": 201}]}
                ],
                "level": "module",
                "dependencies": []
            },
            {
                "name": "auth-service",
                "version": "1.0",
                "endpoints": [
                    {"path": "/api/login", "method": "POST", "description": "User login", "params": [{"name": "username", "type": "string"}, {"name": "password", "type": "string"}], "responses": [{"code": 200}, {"code": 401}]},
                    {"path": "/api/logout", "method": "POST", "description": "User logout", "params": [], "responses": [{"code": 200}]}
                ],
                "level": "subsystem",
                "dependencies": ["user-service"]
            }
        ]
    }

    args = {
        "api_specs": test_apis,
        "detail_level": "comprehensive"
    }

    result = execute_api_checker(args)
    print(result)