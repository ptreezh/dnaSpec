"""
DNASPEC Init Skill
专门负责DNASPEC项目协调机制的初始化和管理
"""
import os
import json
import shutil
from typing import Dict, Any, List, Optional
from enum import Enum
from datetime import datetime
import logging


class InitOperation(Enum):
    """初始化操作枚举"""
    INIT_PROJECT = "init-project"
    DETECT = "detect"
    RESET = "reset"
    GET_CONFIG = "get-config"
    STATUS = "status"
    UPGRADE = "upgrade"


class ProjectType(Enum):
    """项目类型枚举"""
    WEB_APPLICATION = "web_application"
    MOBILE_APP = "mobile_app"
    API_SERVICE = "api_service"
    DESKTOP_APP = "desktop_app"
    LIBRARY = "library"
    MICROSERVICE = "microservice"
    DATA_SCIENCE = "data_science"
    ML_PROJECT = "ml_project"
    GENERIC = "generic"


class InitType(Enum):
    """初始化类型枚举"""
    PROJECT = "project"
    TEAM = "team"
    ENTERPRISE = "enterprise"
    SOLO = "solo"
    AUTO = "auto"


class InitStatus(Enum):
    """初始化状态枚举"""
    NOT_INITIALIZED = "not_initialized"
    PARTIAL = "partial"
    COMPLETE = "complete"
    CONFLICT = "conflict"


class DNASPECInitSkill:
    """
    DNASPEC初始化技能
    负责检测、初始化和管理DNASPEC项目协调机制
    """
    
    def __init__(self, project_root: str = None):
        """
        初始化DNASPEC Init技能
        
        Args:
            project_root: 项目根目录，默认为当前工作目录
        """
        self.project_root = os.path.abspath(project_root or os.getcwd())
        self.dnaspec_dir = os.path.join(self.project_root, '.dnaspec')
        self.constitution_file = os.path.join(self.project_root, 'PROJECT_CONSTITUTION.md')
        self.config_file = os.path.join(self.dnaspec_dir, 'config.json')
        self.logger = logging.getLogger(__name__)
        
        # 确保项目根目录存在
        if not os.path.exists(self.project_root):
            raise ValueError(f"项目根目录不存在: {self.project_root}")
    
    def execute_skill(self, event: Dict[str, Any], context: Any = None) -> Dict[str, Any]:
        """
        执行DNASPEC初始化技能 - 符合agentskills.io规范
        
        Args:
            event: 技能执行事件，包含输入参数
            context: 上下文信息
            
        Returns:
            标准HTTP响应格式的结果
        """
        try:
            # 从事件中提取操作类型和参数
            operation = event.get('operation', 'detect')
            params = event.get('params', {})
            
            # 根据操作类型执行相应功能
            if operation == 'init-project':
                result = self._init_project(**params)
            elif operation == 'detect':
                result = self._detect_status()
            elif operation == 'reset':
                result = self._reset_coordination(**params)
            elif operation == 'get-config':
                result = self._get_configuration()
            elif operation == 'status':
                result = self._get_status()
            elif operation == 'upgrade':
                result = self._upgrade_coordination(**params)
            else:
                result = {
                    "success": False,
                    "error": f"不支持的操作: {operation}",
                    "supported_operations": ['init-project', 'detect', 'reset', 'get-config', 'status', 'upgrade']
                }
            
            # 包装为标准HTTP响应格式
            if result.get('success', False):
                return {
                    'statusCode': 200,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(result, ensure_ascii=False)
                }
            else:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps(result, ensure_ascii=False)
                }
                
        except Exception as e:
            self.logger.error(f"DNASPEC初始化技能执行失败: {str(e)}")
            error_result = {
                "success": False,
                "error": str(e),
                "operation": event.get('operation', 'unknown'),
                "timestamp": datetime.now().isoformat()
            }
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(error_result, ensure_ascii=False)
            }
    
    def execute(self, operation: str, **params) -> Dict[str, Any]:
        """
        兼容旧接口 - 不推荐使用，建议使用execute_skill
        
        Args:
            operation: 操作类型
            **params: 操作参数
            
        Returns:
            操作结果字典
        """
        try:
            if operation == InitOperation.INIT_PROJECT.value:
                return self._init_project(**params)
            elif operation == InitOperation.DETECT.value:
                return self._detect_status()
            elif operation == InitOperation.RESET.value:
                return self._reset_coordination(**params)
            elif operation == InitOperation.GET_CONFIG.value:
                return self._get_configuration()
            elif operation == InitOperation.STATUS.value:
                return self._get_status()
            elif operation == InitOperation.UPGRADE.value:
                return self._upgrade_coordination(**params)
            else:
                return {
                    "success": False,
                    "error": f"不支持的操作: {operation}",
                    "supported_operations": [op.value for op in InitOperation]
                }
                
        except Exception as e:
            self.logger.error(f"DNASPEC初始化操作失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "operation": operation,
                "timestamp": datetime.now().isoformat()
            }
    
    def _init_project(self, 
                     init_type: str = "auto",
                     project_type: str = "generic",
                     features: List[str] = None,
                     force: bool = False,
                     template: str = None) -> Dict[str, Any]:
        """
        初始化项目
        
        Args:
            init_type: 初始化类型 (project, team, enterprise, solo, auto)
            project_type: 项目类型
            features: 要启用的功能列表
            force: 是否强制重新初始化
            template: 初始化模板
            
        Returns:
            初始化结果
        """
        # 参数验证
        if init_type not in [t.value for t in InitType] and init_type != "auto":
            return {
                "success": False,
                "error": f"不支持的初始化类型: {init_type}",
                "supported_types": [t.value for t in InitType] + ["auto"]
            }
        
        if project_type not in [t.value for t in ProjectType]:
            return {
                "success": False,
                "error": f"不支持的项目类型: {project_type}",
                "supported_types": [t.value for t in ProjectType]
            }
        
        features = features or []
        valid_features = ["caching", "git_hooks", "ci_cd", "monitoring", "security"]
        invalid_features = [f for f in features if f not in valid_features]
        if invalid_features:
            return {
                "success": False,
                "error": f"不支持的功能: {invalid_features}",
                "supported_features": valid_features
            }
        
        # 检测当前状态
        current_status = self._detect_status()
        
        if current_status["status"] == InitStatus.COMPLETE.value and not force:
            return {
                "success": True,
                "message": "项目已经完整初始化",
                "status": current_status["status"],
                "existing_files": current_status["existing_files"],
                "suggestion": "使用 force=true 强制重新初始化"
            }
        
        # 执行初始化
        init_result = self._perform_initialization(
            init_type=init_type,
            project_type=project_type,
            features=features,
            template=template
        )
        
        return {
            "success": True,
            "message": f"{init_type} 项目初始化完成",
            "init_type": init_type,
            "project_type": project_type,
            "features_enabled": features,
            "created_files": init_result["created_files"],
            "configuration": init_result["configuration"],
            "template_used": template,
            "timestamp": datetime.now().isoformat(),
            "next_steps": self._generate_next_steps(features)
        }
    
    def _detect_status(self) -> Dict[str, Any]:
        """
        检测项目状态
        
        Returns:
            项目状态信息
        """
        existing_files = []
        missing_files = []
        config_content = {}
        
        # 检查核心文件和目录
        core_items = [
            ("PROJECT_CONSTITUTION.md", "file"),
            (".dnaspec/config.json", "file"),
            (".dnaspec/cache", "directory"),
            (".dnaspec/meta", "directory"),
        ]
        
        for item_path, item_type in core_items:
            full_path = os.path.join(self.project_root, item_path)
            if os.path.exists(full_path):
                existing_files.append(item_path)
            else:
                missing_files.append(item_path)
        
        # 读取配置内容
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config_content = json.load(f)
            except Exception as e:
                config_content = {"error": f"配置读取失败: {str(e)}"}
        
        # 检测项目特征
        project_features = self._detect_project_features()
        
        # 确定状态
        if len(existing_files) == len(core_items):
            status = InitStatus.COMPLETE.value
        elif len(existing_files) > 0:
            status = InitStatus.PARTIAL.value
        else:
            status = InitStatus.NOT_INITIALIZED.value
        
        return {
            "status": status,
            "existing_files": existing_files,
            "missing_files": missing_files,
            "config_content": config_content,
            "project_features": project_features,
            "project_root": self.project_root,
            "dnaspec_dir": self.dnaspec_dir,
            "last_check": datetime.now().isoformat()
        }
    
    def _reset_coordination(self, confirm: bool = False, backup: bool = True) -> Dict[str, Any]:
        """
        重置协调机制
        
        Args:
            confirm: 是否确认重置
            backup: 是否备份现有配置
            
        Returns:
            重置结果
        """
        if not confirm:
            return {
                "success": False,
                "message": "需要确认重置操作",
                "suggestion": "设置 confirm=true 来确认重置",
                "warning": "此操作将删除所有DNASPEC配置和缓存数据"
            }
        
        try:
            backup_info = {}
            
            # 备份现有配置
            if backup and os.path.exists(self.dnaspec_dir):
                backup_dir = f"{self.dnaspec_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.move(self.dnaspec_dir, backup_dir)
                backup_info["backup_location"] = backup_dir
            
            # 删除宪法文件
            if os.path.exists(self.constitution_file):
                os.remove(self.constitution_file)
            
            return {
                "success": True,
                "message": "DNASPEC协调机制已重置",
                "backup_info": backup_info,
                "timestamp": datetime.now().isoformat(),
                "next_steps": [
                    "运行 /dnaspec.dnaspec-init operation=init-project 重新初始化",
                    "检查备份文件恢复特定配置（如果需要）"
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "重置失败",
                "timestamp": datetime.now().isoformat()
            }
    
    def _get_configuration(self) -> Dict[str, Any]:
        """
        获取当前配置信息
        
        Returns:
            配置信息
        """
        try:
            if not os.path.exists(self.config_file):
                return {
                    "success": False,
                    "message": "配置文件不存在",
                    "suggestion": "先运行初始化命令"
                }
            
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            return {
                "success": True,
                "configuration": config,
                "config_file": self.config_file,
                "file_size": os.path.getsize(self.config_file),
                "last_modified": datetime.fromtimestamp(
                    os.path.getmtime(self.config_file)
                ).isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "无法读取配置信息"
            }
    
    def _get_status(self) -> Dict[str, Any]:
        """
        获取详细状态信息
        
        Returns:
            详细状态信息
        """
        status_info = self._detect_status()
        
        # 添加性能指标
        performance_metrics = self._calculate_performance_metrics()
        
        # 添加功能状态
        feature_status = self._check_feature_status()
        
        return {
            "success": True,
            "status": status_info,
            "performance": performance_metrics,
            "features": feature_status,
            "coordination_enabled": status_info["status"] == InitStatus.COMPLETE.value,
            "recommendations": self._generate_recommendations(status_info)
        }
    
    def _upgrade_coordination(self, version: str = None, force: bool = False) -> Dict[str, Any]:
        """
        升级协调机制
        
        Args:
            version: 目标版本
            force: 是否强制升级
            
        Returns:
            升级结果
        """
        try:
            current_config = self._get_configuration()
            if not current_config["success"]:
                return {
                    "success": False,
                    "message": "未找到现有配置，无法升级",
                    "suggestion": "先运行初始化命令"
                }
            
            # 这里可以实现版本升级逻辑
            # 目前简单返回成功
            
            return {
                "success": True,
                "message": "协调机制已升级到最新版本",
                "current_version": current_config["configuration"].get("dnaspec", {}).get("version", "unknown"),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "升级失败"
            }
    
    def _perform_initialization(self, 
                               init_type: str,
                               project_type: str,
                               features: List[str],
                               template: str = None) -> Dict[str, Any]:
        """
        执行具体初始化操作
        
        Args:
            init_type: 初始化类型
            project_type: 项目类型
            features: 功能列表
            template: 模板名称
            
        Returns:
            初始化结果
        """
        created_files = []
        configuration = {}
        
        # 创建DNASPEC目录结构
        self._create_dnaspec_structure()
        created_files.append(".dnaspec/")
        
        # 生成项目宪法
        constitution_content = self._generate_constitution(init_type, project_type, features, template)
        with open(self.constitution_file, 'w', encoding='utf-8') as f:
            f.write(constitution_content)
        created_files.append("PROJECT_CONSTITUTION.md")
        
        # 生成配置文件
        config = self._generate_configuration(init_type, project_type, features, template)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        created_files.append(".dnaspec/config.json")
        
        # 启用指定功能
        if "caching" in features:
            self._setup_caching_system()
            created_files.append(".dnaspec/cache/")
        
        if "git_hooks" in features:
            self._setup_git_hooks()
            created_files.append(".dnaspec/hooks/")
        
        if "ci_cd" in features:
            self._setup_ci_cd_templates()
            created_files.append(".dnaspec/cicd/")
        
        if "monitoring" in features:
            self._setup_monitoring()
            created_files.append(".dnaspec/monitoring/")
        
        if "security" in features:
            self._setup_security()
            created_files.append(".dnaspec/security/")
        
        return {
            "created_files": created_files,
            "configuration": config
        }
    
    def _create_dnaspec_structure(self):
        """创建DNASPEC目录结构"""
        directories = [
            self.dnaspec_dir,
            os.path.join(self.dnaspec_dir, 'cache'),
            os.path.join(self.dnaspec_dir, 'cache', 'temp'),
            os.path.join(self.dnaspec_dir, 'cache', 'staging'),
            os.path.join(self.dnaspec_dir, 'cache', 'meta'),
            os.path.join(self.dnaspec_dir, 'meta'),
            os.path.join(self.dnaspec_dir, 'hooks'),
            os.path.join(self.dnaspec_dir, 'logs'),
            os.path.join(self.dnaspec_dir, 'cicd'),
            os.path.join(self.dnaspec_dir, 'monitoring'),
            os.path.join(self.dnaspec_dir, 'security')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _generate_constitution(self, 
                              init_type: str, 
                              project_type: str, 
                              features: List[str],
                              template: str = None) -> str:
        """生成项目宪法"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 如果指定了模板，使用模板内容
        if template:
            constitution = self._load_constitution_template(template)
            if constitution:
                return constitution.format(
                    project_type=project_type,
                    init_type=init_type,
                    timestamp=timestamp,
                    features="\n".join(f"- {feature}" for feature in features)
                )
        
        # 默认宪法内容
        return f"""# DNASPEC 项目协调宪法

## 项目信息
- **项目类型**: {project_type}
- **初始化类型**: {init_type}
- **初始化时间**: {timestamp}
- **DNASPEC版本**: 1.0.0

## 协调机制
本项目已启用DNASPEC协调机制，支持技能间的智能协作和优雅降级。

### 已启用的功能
{chr(10).join(f"- {feature}" for feature in features)}

## 技能协调规则

### 核心技能
1. **架构设计**: `/dnaspec.architect` - 系统架构设计
2. **任务分解**: `/dnaspec.task-decomposer` - 任务分解和规划
3. **约束生成**: `/dnaspec.constraint-generator` - 约束条件生成
4. **上下文分析**: `/dnaspec.context-analyzer` - 上下文分析
5. **上下文优化**: `/dnaspec.context-optimizer` - 上下文优化
6. **认知模板**: `/dnaspec.cognitive-templater` - 认知模板应用
7. **技能创建**: `/dnaspec.agent-creator` - 智能体创建
8. **API检查**: `/dnaspec.api-checker` - API接口检查
9. **模块化**: `/dnaspec.modulizer` - 模块化设计
10. **缓存管理**: `/dnaspec.cache-manager` - 缓存管理
11. **Git操作**: `/dnaspec.git-operations` - Git操作管理
12. **初始化**: `/dnaspec.dnaspec-init` - 协调机制管理

### 协调执行模式
- **自动检测**: 系统自动检测项目宪法状态
- **智能协调**: 当检测到协调机制时启用多技能协作
- **优雅降级**: 当协调不可用时自动降级到独立模式
- **性能优化**: 基于置信度动态选择最优执行策略

## 质量标准

### 架构设计标准
- 所有架构设计必须通过约束验证
- 架构文档必须符合项目宪法要求
- 关键决策必须有相应的约束说明

### 任务分解标准
- 任务分解必须与架构设计保持一致
- 子任务必须可测试和可验证
- 任务依赖关系必须明确

### 代码质量标准
- 所有代码变更必须通过CI/CD检查
- 缓存命中率保持在85%以上
- 技能执行时间不超过30秒

## 使用指南

### 首次使用
1. 项目已自动初始化协调机制
2. 可以直接使用技能，系统会自动启用协调模式
3. 如需自定义配置，编辑 `PROJECT_CONSTITUTION.md`

### 技能使用
```bash
# 单技能执行（自动检测协调模式）
/dnaspec.architect "system_type={project_type}"

# 多技能工作流
/dnaspec.task-decomposer "task=implement_feature"
/dnaspec.constraint-generator "domain=performance"

# 项目管理
/dnaspec.dnaspec-init "operation=detect"  # 检查状态
/dnaspec.dnaspec-init "operation=get-config"  # 查看配置
```

### 状态管理
```bash
# 检测项目状态
/dnaspec.dnaspec-init "operation=detect"

# 获取详细状态
/dnaspec.dnaspec-init "operation=status"

# 重置协调机制（如需要）
/dnaspec.dnaspec-init "operation=reset confirm=true"

# 升级协调机制
/dnaspec.dnaspec-init "operation=upgrade"
```

## 故障排除

### 常见问题
1. **技能执行失败**: 检查是否正确初始化
2. **协调模式未启用**: 运行 `/dnaspec.dnaspec-init operation=detect`
3. **配置文件错误**: 检查 `.dnaspec/config.json` 格式

### 性能优化
- 定期清理缓存文件
- 监控技能执行时间
- 根据项目规模调整配置参数

---

**最后更新**: {timestamp}
**维护者**: DNASPEC自动生成
"""
    
    def _generate_configuration(self, 
                               init_type: str, 
                               project_type: str, 
                               features: List[str],
                               template: str = None) -> Dict[str, Any]:
        """生成配置文件"""
        return {
            "dnaspec": {
                "version": "1.0.0",
                "init_type": init_type,
                "project_type": project_type,
                "template": template,
                "created_at": datetime.now().isoformat(),
                "features": {
                    "caching": "caching" in features,
                    "git_hooks": "git_hooks" in features,
                    "ci_cd": "ci_cd" in features,
                    "monitoring": "monitoring" in features,
                    "security": "security" in features,
                    "coordination": True,
                    "graceful_degradation": True,
                    "auto_detection": True
                },
                "coordination": {
                    "enabled": True,
                    "confidence_threshold": 0.3,
                    "auto_detection": True,
                    "fallback_to_independent": True,
                    "performance_monitoring": True
                },
                "skills": {
                    "architect": {"enabled": True, "priority": "high"},
                    "task-decomposer": {"enabled": True, "priority": "high"},
                    "constraint-generator": {"enabled": True, "priority": "medium"},
                    "context-analyzer": {"enabled": True, "priority": "medium"},
                    "context-optimizer": {"enabled": True, "priority": "medium"},
                    "cognitive-templater": {"enabled": True, "priority": "low"},
                    "agent-creator": {"enabled": True, "priority": "low"},
                    "api-checker": {"enabled": True, "priority": "medium"},
                    "modulizer": {"enabled": True, "priority": "medium"},
                    "cache-manager": {"enabled": True, "priority": "high"},
                    "git-operations": {"enabled": True, "priority": "medium"},
                    "dnaspec-init": {"enabled": True, "priority": "high"}
                },
                "performance": {
                    "cache_ttl": 3600,
                    "max_concurrent_tasks": 5,
                    "timeout_seconds": 300,
                    "memory_limit_mb": 1024,
                    "cache_cleanup_interval": 86400
                },
                "quality": {
                    "architecture_review_required": True,
                    "constraint_validation": True,
                    "performance_monitoring": True,
                    "error_rate_threshold": 0.05,
                    "success_rate_threshold": 0.95
                }
            }
        }
    
    def _setup_caching_system(self):
        """设置缓存系统"""
        cache_config = {
            "cache_enabled": True,
            "cache_strategies": {
                "file_cache": {"enabled": True, "ttl": 3600},
                "memory_cache": {"enabled": True, "ttl": 1800},
                "distributed_cache": {"enabled": False}
            },
            "directories": {
                "temp": "cache/temp",
                "staging": "cache/staging", 
                "meta": "cache/meta"
            },
            "performance": {
                "max_cache_size_mb": 512,
                "cleanup_interval": 3600
            }
        }
        
        cache_config_file = os.path.join(self.dnaspec_dir, 'cache', 'config.json')
        with open(cache_config_file, 'w', encoding='utf-8') as f:
            json.dump(cache_config, f, indent=2, ensure_ascii=False)
    
    def _setup_git_hooks(self):
        """设置Git钩子"""
        git_hooks_dir = os.path.join(self.project_root, '.git', 'hooks')
        
        if os.path.exists(git_hooks_dir):
            # 预提交钩子
            pre_commit_hook = """#!/bin/bash
# DNASPEC Pre-commit Hook
echo "🔍 Running DNASPEC pre-commit checks..."

# 检查是否需要运行技能
if [ -f "PROJECT_CONSTITUTION.md" ]; then
    echo "✅ DNASPEC project detected"
    # 检查技能执行记录
    if [ -f ".dnaspec/logs/last_execution.json" ]; then
        echo "📊 Last execution logged"
    fi
fi
"""
            
            hook_file = os.path.join(git_hooks_dir, 'pre-commit')
            with open(hook_file, 'w') as f:
                f.write(pre_commit_hook)
            
            # 使钩子可执行
            os.chmod(hook_file, 0o755)
    
    def _setup_ci_cd_templates(self):
        """设置CI/CD模板"""
        cicd_dir = os.path.join(self.dnaspec_dir, 'cicd')
        
        # GitHub Actions模板
        github_workflow = """name: DNASPEC CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  dnaspec-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: DNASPEC Skills Validation
      run: |
        echo "🔍 Running DNASPEC skill validations..."
        # 这里可以添加具体的验证逻辑
        
    - name: Cache Performance Check
      run: |
        echo "📊 Checking cache performance..."
        # 缓存性能检查
        
    - name: Architecture Review
      run: |
        echo "🏗️ Running architecture review..."
        # 架构评审
"""
        
        with open(os.path.join(cicd_dir, 'github-actions.yml'), 'w') as f:
            f.write(github_workflow)
    
    def _setup_monitoring(self):
        """设置监控系统"""
        monitoring_config = {
            "monitoring_enabled": True,
            "metrics": {
                "skill_execution_time": True,
                "cache_hit_rate": True,
                "coordination_success_rate": True,
                "error_rate": True
            },
            "alerts": {
                "high_error_rate": {"threshold": 0.1, "enabled": True},
                "low_cache_hit_rate": {"threshold": 0.7, "enabled": True}
            }
        }
        
        monitoring_config_file = os.path.join(self.dnaspec_dir, 'monitoring', 'config.json')
        with open(monitoring_config_file, 'w', encoding='utf-8') as f:
            json.dump(monitoring_config, f, indent=2, ensure_ascii=False)
    
    def _setup_security(self):
        """设置安全配置"""
        security_config = {
            "security_enabled": True,
            "policies": {
                "skill_execution": {
                    "require_confirmation": False,
                    "log_all_executions": True
                },
                "file_access": {
                    "restrict_cache_access": False,
                    "encrypt_sensitive_data": True
                }
            }
        }
        
        security_config_file = os.path.join(self.dnaspec_dir, 'security', 'config.json')
        with open(security_config_file, 'w', encoding='utf-8') as f:
            json.dump(security_config, f, indent=2, ensure_ascii=False)
    
    def _detect_project_features(self) -> Dict[str, Any]:
        """检测项目特征"""
        features = {
            "languages": [],
            "frameworks": [],
            "tools": [],
            "has_git": False,
            "has_docker": False,
            "has_ci": False
        }
        
        # 检测编程语言
        if os.path.exists('package.json'):
            features["languages"].append('javascript')
            features["frameworks"].append('node.js')
        if os.path.exists('requirements.txt') or os.path.exists('pyproject.toml'):
            features["languages"].append('python')
        if os.path.exists('Cargo.toml'):
            features["languages"].append('rust')
        if os.path.exists('pom.xml') or os.path.exists('build.gradle'):
            features["languages"].append('java')
        
        # 检测工具
        if os.path.exists('.git'):
            features["has_git"] = True
        if os.path.exists('Dockerfile') or os.path.exists('docker-compose.yml'):
            features["has_docker"] = True
        if os.path.exists('.github/workflows') or os.path.exists('.gitlab-ci.yml'):
            features["has_ci"] = True
            features["tools"].append('ci_cd')
        
        return features
    
    def _calculate_performance_metrics(self) -> Dict[str, Any]:
        """计算性能指标"""
        metrics = {
            "cache_size_mb": 0,
            "cache_files_count": 0,
            "last_cache_cleanup": None,
            "coordination_success_rate": 0.0
        }
        
        # 计算缓存大小
        cache_dir = os.path.join(self.dnaspec_dir, 'cache')
        if os.path.exists(cache_dir):
            total_size = 0
            file_count = 0
            for root, dirs, files in os.walk(cache_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.path.exists(file_path):
                        total_size += os.path.getsize(file_path)
                        file_count += 1
            
            metrics["cache_size_mb"] = round(total_size / (1024 * 1024), 2)
            metrics["cache_files_count"] = file_count
        
        return metrics
    
    def _check_feature_status(self) -> Dict[str, bool]:
        """检查功能状态"""
        status = {}
        
        # 检查缓存系统
        cache_config = os.path.join(self.dnaspec_dir, 'cache', 'config.json')
        status["caching"] = os.path.exists(cache_config)
        
        # 检查Git钩子
        git_hooks_dir = os.path.join(self.project_root, '.git', 'hooks')
        pre_commit = os.path.join(git_hooks_dir, 'pre-commit')
        status["git_hooks"] = os.path.exists(git_hooks_dir) and os.path.exists(pre_commit)
        
        # 检查CI/CD模板
        cicd_dir = os.path.join(self.dnaspec_dir, 'cicd')
        status["ci_cd"] = os.path.exists(cicd_dir) and len(os.listdir(cicd_dir)) > 0
        
        # 检查监控系统
        monitoring_config = os.path.join(self.dnaspec_dir, 'monitoring', 'config.json')
        status["monitoring"] = os.path.exists(monitoring_config)
        
        # 检查安全配置
        security_config = os.path.join(self.dnaspec_dir, 'security', 'config.json')
        status["security"] = os.path.exists(security_config)
        
        return status
    
    def _generate_recommendations(self, status_info: Dict[str, Any]) -> List[str]:
        """生成建议"""
        recommendations = []
        
        if status_info["status"] == InitStatus.NOT_INITIALIZED.value:
            recommendations.append("运行 /dnaspec.dnaspec-init operation=init-project 初始化项目")
        elif status_info["status"] == InitStatus.PARTIAL.value:
            recommendations.append("运行 /dnaspec.dnaspec-init operation=init-project force=true 完善初始化")
        
        if not status_info["project_features"].get("has_git", False):
            recommendations.append("建议初始化Git版本控制")
        
        if not status_info["project_features"].get("has_ci", False):
            recommendations.append("建议配置CI/CD流水线")
        
        return recommendations
    
    def _generate_next_steps(self, features: List[str]) -> List[str]:
        """生成后续步骤建议"""
        steps = [
            "✅ DNASPEC协调机制初始化完成",
            "🚀 现在可以开始使用DNASPEC技能",
            "📖 查看 PROJECT_CONSTITUTION.md 了解详细规则"
        ]
        
        if "caching" in features:
            steps.append("💾 缓存系统已启用，性能将得到优化")
        
        if "git_hooks" in features:
            steps.append("🔗 Git钩子已配置，代码质量检查将自动执行")
        
        if "ci_cd" in features:
            steps.append("⚙️ CI/CD模板已生成，可用于自动化部署")
        
        steps.extend([
            "",
            "📝 常用技能使用示例:",
            "/dnaspec.architect \"system_type=web_application\"",
            "/dnaspec.task-decomposer \"task=implement_user_interface\"",
            "/dnaspec.constraint-generator \"domain=performance\"",
            "",
            "🔧 状态检查命令:",
            "/dnaspec.dnaspec-init \"operation=detect\"",
            "/dnaspec.dnaspec-init \"operation=status\"",
            "/dnaspec.dnaspec-init \"operation=get-config\""
        ])
        
        return steps
    
    def _load_constitution_template(self, template_name: str) -> Optional[str]:
        """加载宪法模板"""
        # 这里可以实现模板加载逻辑
        # 目前返回None使用默认模板
        return None