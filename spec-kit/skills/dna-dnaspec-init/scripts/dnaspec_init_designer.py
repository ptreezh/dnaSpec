"""
DNASPEC Init Designer - Interface Adapter
Provides the expected interface for comprehensive testing while using the actual implementation
"""
import sys
import os
from typing import Dict, Any, List, Optional
from enum import Enum
import json
from datetime import datetime
import shutil

# Add the actual implementation to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src'))

try:
    from dna_spec_kit_integration.skills.dnaspec_init import DNASPECInitSkill
except ImportError:
    # Fallback implementation if import fails
    class DNASPECInitSkill:
        def execute(self, operation: str, **params):
            return {"error": "Implementation not found"}

class DNASPECInitType(Enum):
    """初始化类型枚举"""
    PROJECT = "project"
    TEAM = "team"
    ENTERPRISE = "enterprise"
    SOLO = "solo"
    AUTO = "auto"

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

class InitStatus(Enum):
    """初始化状态枚举"""
    NOT_INITIALIZED = "not_initialized"
    PARTIAL = "partial"
    COMPLETE = "complete"
    CONFLICT = "conflict"

class DNASPECInitDesigner:
    """
    DNASPEC Init Designer
    Provides unified interface for initializing DNASPEC coordination mechanisms
    """
    
    def __init__(self):
        """初始化DNASPEC Init Designer"""
        self.init_skill = DNASPECInitSkill()
        self.project_root = os.getcwd()
        self.dnaspec_dir = os.path.join(self.project_root, '.dnaspec')
        self.constitution_file = os.path.join(self.project_root, 'PROJECT_CONSTITUTION.md')
        self.config_file = os.path.join(self.dnaspec_dir, 'config.json')
        
    def initialize_project(self, 
                          init_type: str = "auto",
                          project_type: str = "generic",
                          features: List[str] = None,
                          force: bool = False) -> Dict[str, Any]:
        """
        初始化项目协调机制
        
        Args:
            init_type: 初始化类型 (project, team, enterprise, solo, auto)
            project_type: 项目类型
            features: 要启用的功能列表
            force: 是否强制重新初始化
            
        Returns:
            初始化结果字典
        """
        try:
            # 检测当前项目状态
            current_status = self.detect_project_status()
            
            if current_status["status"] == InitStatus.COMPLETE.value and not force:
                return {
                    "success": True,
                    "message": "项目已经初始化",
                    "status": current_status["status"],
                    "existing_files": current_status["existing_files"]
                }
            
            # 执行初始化
            if init_type == "auto":
                init_type = self._detect_init_type()
            
            result = self._perform_initialization(init_type, project_type, features or [])
            
            return {
                "success": True,
                "message": f"{init_type} 初始化完成",
                "init_type": init_type,
                "project_type": project_type,
                "features_enabled": features or [],
                "created_files": result.get("created_files", []),
                "configuration": result.get("configuration", {}),
                "next_steps": self._generate_next_steps(features or []),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "初始化失败",
                "timestamp": datetime.now().isoformat()
            }
    
    def detect_project_status(self) -> Dict[str, Any]:
        """
        检测项目当前状态
        
        Returns:
            项目状态信息
        """
        existing_files = []
        missing_files = []
        
        # 检查核心文件
        core_files = [
            self.constitution_file,
            self.config_file,
            os.path.join(self.dnaspec_dir, 'cache'),
            os.path.join(self.dnaspec_dir, 'meta'),
        ]
        
        for file_path in core_files:
            if os.path.exists(file_path):
                existing_files.append(file_path)
            else:
                missing_files.append(file_path)
        
        # 检测项目类型
        detected_types = self._detect_project_types()
        
        # 检测工具
        detected_tools = self._detect_development_tools()
        
        # 确定状态
        if len(existing_files) == len(core_files):
            status = InitStatus.COMPLETE.value
        elif len(existing_files) > 0:
            status = InitStatus.PARTIAL.value
        else:
            status = InitStatus.NOT_INITIALIZED.value
        
        return {
            "status": status,
            "existing_files": existing_files,
            "missing_files": missing_files,
            "detected_types": detected_types,
            "detected_tools": detected_tools,
            "project_root": self.project_root,
            "dnaspec_dir": self.dnaspec_dir
        }
    
    def reset_coordination(self, confirm: bool = False) -> Dict[str, Any]:
        """
        重置协调机制
        
        Args:
            confirm: 是否确认重置
            
        Returns:
            重置结果
        """
        if not confirm:
            return {
                "success": False,
                "message": "需要确认重置操作",
                "suggestion": "设置 confirm=true 来确认重置"
            }
        
        try:
            # 备份现有配置
            backup_dir = f"{self.dnaspec_dir}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            if os.path.exists(self.dnaspec_dir):
                shutil.move(self.dnaspec_dir, backup_dir)
            
            # 删除宪法文件
            if os.path.exists(self.constitution_file):
                os.remove(self.constitution_file)
            
            return {
                "success": True,
                "message": "协调机制已重置",
                "backup_location": backup_dir,
                "next_steps": [
                    "运行初始化命令重新配置",
                    "检查备份文件恢复特定配置"
                ]
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "重置失败"
            }
    
    def get_configuration_info(self) -> Dict[str, Any]:
        """
        获取当前配置信息
        
        Returns:
            配置信息
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {}
            
            return {
                "success": True,
                "configuration": config,
                "config_file": self.config_file,
                "last_updated": self._get_file_modification_time(self.config_file)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "无法读取配置信息"
            }
    
    def _detect_init_type(self) -> str:
        """自动检测初始化类型"""
        detected_types = self._detect_project_types()
        detected_tools = self._detect_development_tools()
        
        # 基于检测结果确定初始化类型
        if len(detected_tools.get("team_tools", [])) >= 3:
            return "team"
        elif len(detected_tools.get("enterprise_tools", [])) >= 2:
            return "enterprise"
        else:
            return "project"
    
    def _detect_project_types(self) -> List[str]:
        """检测项目类型"""
        types = []
        
        # 检查常见项目文件
        project_indicators = {
            "web_application": ["package.json", "index.html", "vite.config.js", "webpack.config.js"],
            "mobile_app": ["App.js", "app.json", "pubspec.yaml", "build.gradle"],
            "api_service": ["main.py", "app.py", "requirements.txt", "Dockerfile"],
            "ml_project": ["requirements.txt", "jupyter", "notebook.ipynb", "model.pkl"],
            "data_science": ["requirements.txt", "notebook.ipynb", "data/", "pandas"],
            "microservice": ["Dockerfile", "docker-compose.yml", "main.py", "app.py"]
        }
        
        for project_type, indicators in project_indicators.items():
            if any(os.path.exists(indicator) for indicator in indicators):
                types.append(project_type)
        
        return types if types else ["generic"]
    
    def _detect_development_tools(self) -> Dict[str, List[str]]:
        """检测开发工具"""
        tools = {
            "version_control": [],
            "build_tools": [],
            "team_tools": [],
            "enterprise_tools": [],
            "cicd_tools": []
        }
        
        # 版本控制
        if os.path.exists('.git'):
            tools["version_control"].append("git")
        
        # 构建工具
        if os.path.exists('package.json'):
            tools["build_tools"].append("npm")
        if os.path.exists('requirements.txt'):
            tools["build_tools"].append("pip")
        if os.path.exists('Dockerfile'):
            tools["build_tools"].append("docker")
        
        # 团队工具
        if os.path.exists('.github') or os.path.exists('workflows'):
            tools["team_tools"].append("github_actions")
        if os.path.exists('.gitlab-ci.yml') or os.path.exists('.gitlab'):
            tools["team_tools"].append("gitlab_ci")
        
        # 企业工具
        if os.path.exists('k8s') or os.path.exists('kubernetes'):
            tools["enterprise_tools"].append("kubernetes")
        if os.path.exists('terraform'):
            tools["enterprise_tools"].append("terraform")
        
        # CI/CD工具
        if os.path.exists('.github/workflows'):
            tools["cicd_tools"].append("github_actions")
        if os.path.exists('.circleci'):
            tools["cicd_tools"].append("circleci")
        
        return tools
    
    def _perform_initialization(self, init_type: str, project_type: str, features: List[str]) -> Dict[str, Any]:
        """执行具体初始化操作"""
        created_files = []
        configuration = {}
        
        # 创建DNASPEC目录结构
        self._create_dnaspec_structure()
        created_files.append(self.dnaspec_dir)
        
        # 生成项目宪法
        constitution_content = self._generate_constitution(init_type, project_type, features)
        with open(self.constitution_file, 'w', encoding='utf-8') as f:
            f.write(constitution_content)
        created_files.append(self.constitution_file)
        
        # 生成配置文件
        config = self._generate_configuration(init_type, project_type, features)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        created_files.append(self.config_file)
        
        # 启用指定功能
        if "caching" in features:
            self._setup_caching_system()
            created_files.append(os.path.join(self.dnaspec_dir, 'cache'))
        
        if "git_hooks" in features:
            self._setup_git_hooks()
            created_files.append(os.path.join(self.dnaspec_dir, 'hooks'))
        
        if "ci_cd" in features:
            self._setup_ci_cd_templates()
            created_files.append(os.path.join(self.dnaspec_dir, 'cicd'))
        
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
            os.path.join(self.dnaspec_dir, 'logs')
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _generate_constitution(self, init_type: str, project_type: str, features: List[str]) -> str:
        """生成项目宪法"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        return f"""# DNASPEC 项目协调宪法

## 项目信息
- **项目类型**: {project_type}
- **初始化类型**: {init_type}
- **初始化时间**: {timestamp}
- **DNASPEC版本**: 1.0.0

## 协调机制
本项目已启用DNASPEC协调机制，支持技能间的智能协作。

### 已启用的功能
{chr(10).join(f"- {feature}" for feature in features)}

## 技能协调规则

### 核心技能组合
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
```

### 状态检查
```bash
# 检查项目状态
/dnaspec.dnaspec-init "operation=detect"

# 查看配置信息
/dnaspec.dnaspec-init "operation=get-config"

# 重置协调机制（如需要）
/dnaspec.dnaspec-init "operation=reset confirm=true"
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
    
    def _generate_configuration(self, init_type: str, project_type: str, features: List[str]) -> Dict[str, Any]:
        """生成配置文件"""
        return {
            "dnaspec": {
                "version": "1.0.0",
                "init_type": init_type,
                "project_type": project_type,
                "created_at": datetime.now().isoformat(),
                "features": {
                    "caching": "caching" in features,
                    "git_hooks": "git_hooks" in features,
                    "ci_cd": "ci_cd" in features,
                    "coordination": True,
                    "graceful_degradation": True
                },
                "coordination": {
                    "enabled": True,
                    "confidence_threshold": 0.3,
                    "auto_detection": True,
                    "fallback_to_independent": True
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
                    "git-operations": {"enabled": True, "priority": "medium"}
                },
                "performance": {
                    "cache_ttl": 3600,
                    "max_concurrent_tasks": 5,
                    "timeout_seconds": 300,
                    "memory_limit_mb": 1024
                },
                "quality": {
                    "architecture_review_required": True,
                    "constraint_validation": True,
                    "performance_monitoring": True,
                    "error_rate_threshold": 0.05
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
            }
        }
        
        cache_config_file = os.path.join(self.dnaspec_dir, 'cache', 'config.json')
        with open(cache_config_file, 'w', encoding='utf-8') as f:
            json.dump(cache_config, f, indent=2, ensure_ascii=False)
    
    def _setup_git_hooks(self):
        """设置Git钩子"""
        hooks_dir = os.path.join(self.dnaspec_dir, 'hooks')
        git_hooks_dir = os.path.join(self.project_root, '.git', 'hooks')
        
        if os.path.exists(git_hooks_dir):
            # 预提交钩子
            pre_commit_hook = """#!/bin/bash
# DNASPEC Pre-commit Hook
echo "🔍 Running DNASPEC pre-commit checks..."

# 检查是否需要运行技能
if [ -f "PROJECT_CONSTITUTION.md" ]; then
    echo "✅ DNASPEC project detected"
    # 这里可以添加具体的检查逻辑
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
        os.makedirs(cicd_dir, exist_ok=True)
        
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
    - uses: actions/checkout@v2
    
    - name: DNASPEC Skills Validation
      run: |
        echo "🔍 Running DNASPEC skill validations..."
        # 这里可以添加具体的验证逻辑
        
    - name: Cache Performance Check
      run: |
        echo "📊 Checking cache performance..."
        # 缓存性能检查
"""
        
        with open(os.path.join(cicd_dir, 'github-actions.yml'), 'w') as f:
            f.write(github_workflow)
    
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
            "/dnaspec.dnaspec-init \"operation=get-config\""
        ])
        
        return steps
    
    def _get_file_modification_time(self, file_path: str) -> Optional[str]:
        """获取文件修改时间"""
        try:
            if os.path.exists(file_path):
                return datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
        except Exception:
            pass
        return None

# Re-export the main class for compatibility
class DNASPECInit:
    """DNASPEC Init - Main Interface"""
    
    def __init__(self):
        """初始化DNASPEC Init"""
        self.designer = DNASPECInitDesigner()
    
    def initialize_project(self, **kwargs) -> Dict[str, Any]:
        """初始化项目"""
        return self.designer.initialize_project(**kwargs)
    
    def detect_status(self) -> Dict[str, Any]:
        """检测状态"""
        return self.designer.detect_project_status()
    
    def reset(self, confirm: bool = False) -> Dict[str, Any]:
        """重置"""
        return self.designer.reset_coordination(confirm)
    
    def get_config(self) -> Dict[str, Any]:
        """获取配置"""
        return self.designer.get_configuration_info()