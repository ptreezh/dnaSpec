"""
约束生成技能实现 - 基于初始宪法需求的动态约束生成系统
实现需求的版本控制、时间点恢复和动态对齐机制
"""
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid
from dataclasses import dataclass, asdict
import copy

@dataclass
class ConstitutionVersion:
    """宪法版本数据类"""
    version_id: str
    requirements: str
    timestamp: str
    constraints: List[Dict[str, Any]]
    snapshot_state: Dict[str, Any]

class ConstitutionManager:
    """宪法管理器 - 管理需求宪法和版本控制"""
    
    def __init__(self):
        self.versions: List[ConstitutionVersion] = []
        self.active_version: Optional[ConstitutionVersion] = None
        self.alignment_history: List[Dict[str, Any]] = []
    
    def lock_initial_requirements(self, initial_reqs: str) -> ConstitutionVersion:
        """锁定初始需求为宪法版本"""
        version = ConstitutionVersion(
            version_id=f"CONSTITUTION-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}",
            requirements=initial_reqs,
            timestamp=datetime.now().isoformat(),
            constraints=[],
            snapshot_state={}
        )
        
        self.versions.append(version)
        self.active_version = version
        
        return version
    
    def create_constraint(self, constraint_type: str, description: str, severity: str = "medium") -> Dict[str, Any]:
        """创建约束定义"""
        constraint = {
            "id": f"CONSTRAINT-{uuid.uuid4().hex[:8]}",
            "type": constraint_type,
            "description": description,
            "severity": severity,
            "created_at": datetime.now().isoformat(),
            "active": True
        }
        return constraint
    
    def add_constraint_to_constitution(self, constraint: Dict[str, Any]):
        """将约束添加到活跃宪法中"""
        if self.active_version:
            self.active_version.constraints.append(constraint)
    
    def get_active_constitution(self) -> Optional[ConstitutionVersion]:
        """获取当前活跃的宪法版本"""
        return self.active_version
    
    def create_snapshot(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """创建系统状态快照"""
        snapshot = {
            "id": f"SNAPSHOT-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}",
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "constitution_reference": self.active_version.version_id if self.active_version else None
        }
        return snapshot
    
    def restore_to_version(self, version_id: str) -> Optional[ConstitutionVersion]:
        """恢复到指定宪法版本"""
        for version in self.versions:
            if version.version_id == version_id:
                self.active_version = version
                return version
        return None

class AlignmentChecker:
    """对齐检查器 - 检查新需求与宪法的对齐情况"""
    
    def __init__(self, constitution_manager: ConstitutionManager):
        self.constitution_manager = constitution_manager
    
    def check_alignment(self, new_requirement: str) -> Dict[str, Any]:
        """检查新需求与宪法的对齐情况"""
        if not self.constitution_manager.active_version:
            # 没有宪法则视为对齐
            return {
                "is_aligned": True,
                "alignment_score": 1.0,
                "conflicts": [],
                "suggestions": ["建议创建初始宪法需求作为对齐基准"]
            }
        
        constitution = self.constitution_manager.active_version
        constitution_text = constitution.requirements.lower()
        new_req_text = new_requirement.lower()
        
        # 基本对齐检查
        alignment_score = self._calculate_alignment_score(constitution_text, new_req_text)
        
        # 检查冲突
        conflicts = self._detect_conflicts(constitution, new_requirement)
        
        # 生成建议
        suggestions = self._generate_alignment_suggestions(constitution, new_requirement, conflicts)
        
        result = {
            "is_aligned": alignment_score > 0.5 and len(conflicts) == 0,
            "alignment_score": alignment_score,
            "conflicts": conflicts,
            "suggestions": suggestions,
            "constitution_reference": constitution.version_id
        }
        
        # 记录对齐历史
        self.constitution_manager.alignment_history.append({
            "timestamp": datetime.now().isoformat(),
            "new_requirement": new_requirement,
            "result": result
        })
        
        return result
    
    def _calculate_alignment_score(self, constitution: str, new_req: str) -> float:
        """计算对齐分数"""
        # 简单的关键词匹配算法
        constitution_words = set(constitution.split())
        new_req_words = set(new_req.split())
        
        if not constitution_words:
            return 0.0
        
        overlap = constitution_words.intersection(new_req_words)
        return len(overlap) / len(constitution_words)  # 权重于宪法覆盖度
    
    def _detect_conflicts(self, constitution: ConstitutionVersion, new_requirement: str) -> List[Dict[str, str]]:
        """检测冲突"""
        conflicts = []
        
        # 检查与宪法核心要求的冲突
        core_terms = ['security', 'privacy', 'performance', 'scalability', 'reliability']
        for term in core_terms:
            if term in constitution.requirements.lower() and f"no {term}" in new_requirement.lower():
                conflicts.append({
                    "type": "CoreRequirementConflict",
                    "description": f"New requirement conflicts with core {term} requirement in constitution",
                    "severity": "high"
                })
        
        # 检查约束冲突
        for constraint in constitution.constraints:
            if constraint['active'] and constraint['description'].lower() in new_requirement.lower():
                conflicts.append({
                    "type": "ConstraintConflict", 
                    "description": f"New requirement violates existing constraint: {constraint['description']}",
                    "severity": constraint['severity']
                })
        
        return conflicts
    
    def _generate_alignment_suggestions(self, constitution: ConstitutionVersion, new_requirement: str, conflicts: List[Dict[str, str]]) -> List[str]:
        """生成对齐建议"""
        suggestions = []
        
        if conflicts:
            suggestions.append("修改新需求以符合宪法要求")
            suggestions.append("如确实需要变更宪法，请提交正式的宪法修订请求")
        else:
            suggestions.append("新需求与宪法保持一致")
            suggestions.append("可安全地将其纳入开发计划")
        
        return suggestions

class ConstraintGenerator:
    """约束生成器主类"""
    
    def __init__(self):
        self.constitution_manager = ConstitutionManager()
        self.alignment_checker = AlignmentChecker(self.constitution_manager)
        self.timecapsule_snapshots = {}  # 存储时间胶囊快照
    
    def generate_constraints(self, requirements: str, change_request: str = None) -> Dict[str, Any]:
        """生成约束"""
        # 如果没有活跃宪法，锁定当前需求为初始宪法
        if not self.constitution_manager.active_version:
            self.constitution_manager.lock_initial_requirements(requirements)
        
        # 检查新需求与宪法的对齐情况
        alignment_result = self.alignment_checker.check_alignment(requirements)
        
        # 根据对齐结果生成约束
        generated_constraints = []
        if not alignment_result["is_aligned"]:
            # 生成对齐约束
            alignment_constraint = self.constitution_manager.create_constraint(
                "alignment", 
                f"New requirement must align with constitution: {requirements}", 
                "high"
            )
            generated_constraints.append(alignment_constraint)
        
        # 检测并生成其他类型的约束
        generated_constraints.extend(self._generate_domain_specific_constraints(requirements))
        
        # 为每个生成的约束添加到宪法
        for constraint in generated_constraints:
            self.constitution_manager.add_constraint_to_constitution(constraint)
        
        # 创建系统状态快照
        current_state = {
            "requirements": requirements,
            "change_request": change_request,
            "alignment_result": alignment_result,
            "generated_constraints": generated_constraints,
            "constitution_version": self.constitution_manager.active_version.version_id if self.constitution_manager.active_version else None
        }
        snapshot = self.constitution_manager.create_snapshot(current_state)
        
        return {
            "constitution": asdict(self.constitution_manager.active_version) if self.constitution_manager.active_version else None,
            "generated_constraints": generated_constraints,
            "alignment_result": alignment_result,
            "system_snapshot": snapshot,
            "timestamp": datetime.now().isoformat()
        }
    
    def _generate_domain_specific_constraints(self, requirements: str) -> List[Dict[str, Any]]:
        """生成领域特定约束"""
        constraints = []
        req_lower = requirements.lower()
        
        # 安全约束
        if any(security_term in req_lower for security_term in ['security', 'secure', 'auth', 'encrypt', 'privacy', 'protect']):
            constraints.append(self.constitution_manager.create_constraint(
                "security",
                "All security-related functionality must comply with OWASP standards",
                "high"
            ))
        
        # 性能约束
        if any(perf_term in req_lower for perf_term in ['performance', 'fast', 'response', 'throughput', 'latency', 'efficient']):
            constraints.append(self.constitution_manager.create_constraint(
                "performance", 
                "System must meet specified performance requirements with 99.9% availability",
                "medium"
            ))
        
        # 数据约束
        if any(data_term in req_lower for data_term in ['data', 'database', 'storage', 'retrieve', 'persist']):
            constraints.append(self.constitution_manager.create_constraint(
                "data_integrity",
                "All data operations must maintain ACID properties and backup requirements",
                "high"
            ))
        
        # 可扩展性约束
        if any(scale_term in req_lower for scale_term in ['scale', 'scalable', 'grow', 'expand', 'capacity']):
            constraints.append(self.constitution_manager.create_constraint(
                "scalability",
                "System architecture must support horizontal and vertical scaling",
                "medium"
            ))
        
        return constraints
    
    def create_timecapsule(self, label: str, state: Dict[str, Any]) -> str:
        """创建时间胶囊快照"""
        capsule_id = f"TIMECAPSULE-{label}-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:8]}"
        self.timecapsule_snapshots[capsule_id] = {
            "id": capsule_id,
            "label": label,
            "state": copy.deepcopy(state),
            "timestamp": datetime.now().isoformat(),
            "constitution_version": self.constitution_manager.active_version.version_id if self.constitution_manager.active_version else None
        }
        return capsule_id
    
    def restore_from_timecapsule(self, capsule_id: str) -> Optional[Dict[str, Any]]:
        """从时间胶囊恢复"""
        capsule = self.timecapsule_snapshots.get(capsule_id)
        if capsule:
            # 恢复宪法到该时间点的状态
            constitution_ref = capsule["constitution_version"]
            if constitution_ref:
                restored_version = self.constitution_manager.restore_to_version(constitution_ref)
                if restored_version:
                    return {
                        "restored": True,
                        "capsule_id": capsule_id,
                        "restored_constitution": asdict(restored_version),
                        "state": capsule["state"]
                    }
        
        return {
            "restored": False,
            "capsule_id": capsule_id,
            "error": "Cannot restore from this timecapsule"
        }
    
    def get_alignment_history(self) -> List[Dict[str, Any]]:
        """获取对齐历史"""
        return self.constitution_manager.alignment_history

def execute_constraint_generator(args: Dict[str, Any]) -> str:
    """
    约束生成技能执行函数
    Args:
        args: 包含'requirements'和可选'change_request'的参数字典
    Returns:
        JSON格式的约束生成结果
    """
    requirements = args.get('requirements', args.get('input', ''))
    change_request = args.get('change_request', '')
    
    if not requirements:
        return json.dumps({
            "success": False,
            "error": "No requirements provided for constraint generation"
        }, ensure_ascii=False, indent=2)
    
    generator = ConstraintGenerator()
    result_data = generator.generate_constraints(requirements, change_request)
    
    # 如果有变更请求，创建时间胶囊
    if change_request:
        state_copy = {
            "requirements": requirements,
            "change_request": change_request,
            "result": result_data
        }
        capsule_id = generator.create_timecapsule("change_request", state_copy)
        result_data["timecapsule_id"] = capsule_id
    
    result = {
        "success": True,
        "data": result_data,
        "execution_info": {
            "skill": "constraint-generator", 
            "timestamp": datetime.now().isoformat(),
            "constitution_locked": result_data["constitution"] is not None
        }
    }
    
    return json.dumps(result, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    # 测试约束生成
    test_reqs = "系统需要支持用户认证和数据加密存储"
    args = {"requirements": test_reqs, "change_request": "新增人脸识别功能"}
    result = execute_constraint_generator(args)
    print(result)