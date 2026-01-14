"""
核心共同状态管理器 - 技能协同契约系统的基础
"""
import json
import threading
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum

class StateUpdateType(Enum):
    """状态更新类型"""
    TEMP_FILE_ADD = "temp_file_add"
    TEMP_FILE_CONFIRM = "temp_file_confirm"
    TEMP_FILE_REMOVE = "temp_file_remove"
    CONTEXT_ANALYSIS = "context_analysis"
    CONTEXT_OPTIMIZATION = "context_optimization"
    CONTEXT_TEMPLATE = "context_template"
    GIT_OPERATION = "git_operation"
    SECURITY_CHECK = "security_check"
    QUALITY_METRIC = "quality_metric"

class CommonStateManager:
    """核心共同状态管理器"""
    
    def __init__(self, state_file: str = None):
        self._state = self._initialize_default_state()
        self._lock = threading.RLock()  # 可重入锁，防止死锁
        self._event_history = []  # 状态变更历史
        self._state_file = state_file or self._get_default_state_file()
        
        # 从文件加载现有状态
        self._load_state_from_file()
        
    def _initialize_default_state(self) -> Dict[str, Any]:
        """初始化默认状态"""
        return {
            "version": "1.0.0",
            "last_updated": datetime.now().isoformat(),
            "temp_workspace": {
                "active_session": None,
                "temp_files": [],
                "confirmed_files": [],
                "session_start_time": None,
                "temp_file_whitelist": [],  # 白名单，允许的临时文件类型
                "violation_count": 0
            },
            "context_chain": {
                "current_analysis": None,
                "analysis_history": [],
                "optimization_flags": [],
                "quality_scores": {},
                "context_id": None,
                "chain_integrity_status": "valid",
                "last_link_time": None
            },
            "security": {
                "validation_rules": [],
                "violation_tracker": [],
                "access_control": {},
                "security_level": "strict",
                "last_violation_time": None
            },
            "directory_structure": {
                "current_structure": {},
                "proposed_changes": [],
                "consistency_status": "verified",
                "last_verification_time": None
            },
            "performance_metrics": {
                "quality_scores": {},
                "validation_stats": {},
                "execution_times": {},
                "error_rates": {},
                "last_metric_update": None
            },
            "workspace_state": {
                "current_sessions": [],
                "resource_usage": {},
                "access_tokens": [],
                "last_access_time": None
            }
        }
    
    def _get_default_state_file(self) -> str:
        """获取默认状态文件路径"""
        # 在项目根目录创建状态文件
        project_root = Path(__file__).parent.parent.parent
        return str(project_root / ".dnaspec" / "common_state.json")
    
    def _ensure_state_directory(self):
        """确保状态文件目录存在"""
        state_path = Path(self._state_file)
        state_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_state_from_file(self):
        """从文件加载状态"""
        try:
            if os.path.exists(self._state_file):
                with open(self._state_file, 'r', encoding='utf-8') as f:
                    loaded_state = json.load(f)
                    # 合并加载的状态到当前状态
                    self._state.update(loaded_state)
        except Exception as e:
            print(f"⚠️  加载状态文件失败: {e}")
            # 如果加载失败，使用默认状态
    
    def _save_state_to_file(self):
        """保存状态到文件"""
        try:
            self._ensure_state_directory()
            with open(self._state_file, 'w', encoding='utf-8') as f:
                json.dump(self._state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 保存状态文件失败: {e}")
    
    def update_state(self, category: str, key: str, value: Any) -> bool:
        """更新状态"""
        with self._lock:
            try:
                # 确保类别存在
                if category not in self._state:
                    self._state[category] = {}
                
                # 记录旧值
                old_value = self._state[category].get(key)
                
                # 更新值
                self._state[category][key] = value
                self._state["last_updated"] = datetime.now().isoformat()
                
                # 记录变更事件
                state_update_type = (StateUpdateType.CONTEXT_ANALYSIS if "context" in category
                                   else StateUpdateType.GIT_OPERATION if "git" in category
                                   else StateUpdateType.TEMP_FILE_ADD)
                self._log_state_update(state_update_type, category, key, old_value, value)
                
                # 保存到文件
                self._save_state_to_file()
                
                return True
            except Exception as e:
                print(f"❌ 更新状态失败: {e}")
                return False
    
    def get_state(self, category: str, key: str = None) -> Any:
        """获取状态"""
        with self._lock:
            if key is None:
                return self._state.get(category, {})
            return self._state.get(category, {}).get(key)
    
    def append_to_list(self, category: str, key: str, item: Any) -> bool:
        """向列表添加项"""
        with self._lock:
            try:
                if category not in self._state:
                    self._state[category] = {}
                if key not in self._state[category]:
                    self._state[category][key] = []
                
                if item not in self._state[category][key]:  # 避免重复
                    self._state[category][key].append(item)
                    self._state["last_updated"] = datetime.now().isoformat()
                    
                    # 记录变更事件
                    if "temp" in category:
                        state_update_type = StateUpdateType.TEMP_FILE_ADD
                    elif "context" in category:
                        state_update_type = StateUpdateType.CONTEXT_ANALYSIS
                    else:
                        state_update_type = StateUpdateType.GIT_OPERATION

                    self._log_state_update(state_update_type, category, key, "list_append", item)
                    
                    self._save_state_to_file()
                
                return True
            except Exception as e:
                print(f"❌ 添加到列表失败: {e}")
                return False
    
    def remove_from_list(self, category: str, key: str, item: Any) -> bool:
        """从列表移除项"""
        with self._lock:
            try:
                if (category in self._state and 
                    key in self._state[category] and 
                    isinstance(self._state[category][key], list) and
                    item in self._state[category][key]):
                    
                    self._state[category][key].remove(item)
                    self._state["last_updated"] = datetime.now().isoformat()
                    
                    self._save_state_to_file()
                
                return True
            except Exception as e:
                print(f"❌ 从列表移除失败: {e}")
                return False
    
    def increment_counter(self, category: str, key: str) -> int:
        """递增计数器"""
        with self._lock:
            try:
                if category not in self._state:
                    self._state[category] = {}
                current_val = self._state[category].get(key, 0)
                new_val = current_val + 1
                self._state[category][key] = new_val
                self._state["last_updated"] = datetime.now().isoformat()
                
                self._save_state_to_file()
                
                return new_val
            except Exception as e:
                print(f"❌ 递增计数器失败: {e}")
                return 0
    
    def _log_state_update(self, update_type: StateUpdateType, category: str, key: str, 
                         old_value: Any, new_value: Any):
        """记录状态变更"""
        update_record = {
            "timestamp": datetime.now().isoformat(),
            "update_type": update_type.value,
            "category": category,
            "key": key,
            "old_value": old_value,
            "new_value": new_value
        }
        self._event_history.append(update_record)
        
        # 保持历史记录在合理大小
        if len(self._event_history) > 1000:
            self._event_history = self._event_history[-500:]  # 保留最近500条
    
    def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """获取状态变更历史"""
        with self._lock:
            return self._event_history[-limit:]
    
    def get_full_state_snapshot(self) -> Dict[str, Any]:
        """获取完整状态快照"""
        with self._lock:
            return json.loads(json.dumps(self._state))  # 深拷贝避免外部修改
    
    def reset_category(self, category: str):
        """重置特定类别的状态"""
        with self._lock:
            default_categories = {
                "temp_workspace": {"temp_files": [], "confirmed_files": [], "violation_count": 0},
                "context_chain": {"analysis_history": [], "quality_scores": {}, "chain_integrity_status": "valid"},
                "security": {"violation_tracker": [], "last_violation_time": None},
                "directory_structure": {"proposed_changes": [], "consistency_status": "verified"},
                "performance_metrics": {"quality_scores": {}, "error_rates": {}},
                "workspace_state": {"current_sessions": [], "resource_usage": {}}
            }
            
            if category in default_categories:
                self._state[category] = default_categories[category]
                self._state["last_updated"] = datetime.now().isoformat()
                self._save_state_to_file()
    
    def check_integrity(self) -> Dict[str, Any]:
        """检查状态完整性"""
        with self._lock:
            issues = []
            
            # 检查临时文件完整性
            temp_files = set(self._state["temp_workspace"].get("temp_files", []))
            confirmed_files = set(self._state["temp_workspace"].get("confirmed_files", []))
            if temp_files & confirmed_files:  # 求交集，不应该有交集
                issues.append("临时文件和确认文件有重复")
            
            # 检查上下文链完整性
            if (self._state["context_chain"].get("chain_integrity_status") == "invalid" and
                self._state["context_chain"].get("current_analysis") is not None):
                issues.append("上下文链状态无效但仍有分析数据")
            
            # 检查安全状态
            violation_count = self._state["security"].get("violation_tracker", [])
            if len(violation_count) > 100:  # 假设超过100个违规需要关注
                issues.append(f"安全违规数量过多: {len(violation_count)}")
            
            return {
                "status": "ok" if not issues else "warning",
                "issues": issues,
                "categories": list(self._state.keys())
            }

# 全局共同状态实例
COMMON_STATE_MANAGER = CommonStateManager()

def initialize_common_state():
    """初始化共同状态 - 项目启动时调用"""
    global COMMON_STATE_MANAGER
    COMMON_STATE_MANAGER = CommonStateManager()
    print("✅ 共同状态管理器已初始化")
    
    # 验证状态完整性
    integrity_check = COMMON_STATE_MANAGER.check_integrity()
    if integrity_check["status"] == "warning":
        print(f"⚠️  状态完整性检查发现问题: {integrity_check['issues']}")
    else:
        print("✅ 状态完整性检查通过")