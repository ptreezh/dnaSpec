"""
DSGS Context Engineering Skills - 版本管理和自动更新系统
实现Git版本控制和自动更新功能
"""
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
import json
import requests
from datetime import datetime


class DSGSVersionManager:
    """
    DSGS版本管理器
    处理Git版本控制和自动更新功能
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.version_file = self.project_root / "VERSION"
        self.git_enabled = self._is_git_enabled()
    
    def _is_git_enabled(self) -> bool:
        """检查是否启用了Git"""
        return (self.project_root / ".git").exists()
    
    def get_current_version(self) -> str:
        """获取当前版本"""
        if self.version_file.exists():
            with open(self.version_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        
        # 如果没有版本文件，从Git获取版本
        if self.git_enabled:
            try:
                result = subprocess.run(
                    ["git", "describe", "--tags", "--always"], 
                    capture_output=True, 
                    text=True, 
                    cwd=self.project_root
                )
                if result.returncode == 0:
                    return result.stdout.strip()
            except:
                pass
        
        return "1.0.0"  # 默认版本
    
    def set_version(self, version: str) -> bool:
        """设置新版本"""
        try:
            with open(self.version_file, 'w', encoding='utf-8') as f:
                f.write(version)
            
            # 如果有Git，提交版本变更
            if self.git_enabled:
                subprocess.run(["git", "add", str(self.version_file)], 
                             cwd=self.project_root, capture_output=True)
                subprocess.run(["git", "commit", "-m", f"Update to version {version}"], 
                             cwd=self.project_root, capture_output=True)
            
            return True
        except Exception:
            return False
    
    def update_version_file(self, new_version: str) -> bool:
        """更新版本文件"""
        return self.set_version(new_version)
    
    def check_for_updates(self) -> Dict[str, Any]:
        """检查更新"""
        current_version = self.get_current_version()
        
        # 在实际实现中，这里会检查远程仓库或API
        # 模拟检查更新
        latest_version = "1.0.2"  # 假设的最新版本
        has_update = latest_version != current_version
        
        return {
            "current_version": current_version,
            "latest_version": latest_version,
            "has_update": has_update,
            "update_available": latest_version if has_update else None
        }
    
    def update_system(self, target_version: str = None) -> Dict[str, Any]:
        """更新系统到指定版本"""
        if not self.git_enabled:
            return {
                "success": False,
                "error": "项目未初始化Git，无法自动更新"
            }
        
        try:
            if target_version is None:
                target_version = self.check_for_updates()["latest_version"]
            
            # 拉取最新版本
            pull_result = subprocess.run(
                ["git", "pull", "origin", "main"], 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            
            if pull_result.returncode != 0:
                return {
                    "success": False,
                    "error": f"Git pull failed: {pull_result.stderr}"
                }
            
            # 切换到指定版本标签（如果存在）
            if target_version != "latest":
                checkout_result = subprocess.run(
                    ["git", "checkout", target_version], 
                    capture_output=True, 
                    text=True,
                    cwd=self.project_root
                )
                if checkout_result.returncode != 0:
                    # 如果标签不存在，尝试拉取标签
                    fetch_tags = subprocess.run(
                        ["git", "fetch", "--all", "--tags"], 
                        capture_output=True, 
                        text=True,
                        cwd=self.project_root
                    )
                    if fetch_tags.returncode == 0:
                        checkout_result = subprocess.run(
                            ["git", "checkout", target_version], 
                            capture_output=True, 
                            text=True,
                            cwd=self.project_root
                        )
            
            # 更新版本文件
            self.update_version_file(target_version)
            
            return {
                "success": True,
                "old_version": self.get_current_version(),
                "new_version": target_version,
                "message": f"系统已更新到版本 {target_version}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class DSGSContextSkillsUpdater:
    """
    DSGS Context Skills 自动更新器
    专门用于更新Context Engineering Skills系统
    """
    
    def __init__(self):
        self.version_manager = DSGSVersionManager()
        self.project_root = Path(".")  # 设置项目根目录
        self.update_log_file = Path("UPDATE_LOG.md")
    
    def create_update_manifest(self) -> Dict[str, Any]:
        """创建更新清单"""
        return {
            "timestamp": datetime.now().isoformat(),
            "version": self.version_manager.get_current_version(),
            "updated_components": [
                "Context Analysis Skill",
                "Context Optimization Skill", 
                "Cognitive Template Skill",
                "Skills Manager",
                "System Integration"
            ],
            "update_reason": "Bug fixes, performance improvements, new feature additions",
            "git_enabled": self.version_manager.git_enabled,
            "version_control": "Git-based version management and automatic updates"
        }
    
    def log_update(self, manifest: Dict[str, Any]):
        """记录更新信息"""
        with open(self.update_log_file, 'a', encoding='utf-8') as f:
            f.write(f"\n## Update {manifest['version']} - {manifest['timestamp']}\n")
            f.write(f"- Updated components: {', '.join(manifest['updated_components'])}\n")
            f.write(f"- Reason: {manifest['update_reason']}\n")
            f.write(f"- Git Enabled: {manifest['git_enabled']}\n\n")
    
    def check_update_readiness(self) -> Dict[str, Any]:
        """检查更新准备状态"""
        current_version = self.version_manager.get_current_version()
        update_check = self.version_manager.check_for_updates()
        
        return {
            "current_version": current_version,
            "update_available": update_check["has_update"],
            "latest_version": update_check["latest_version"],
            "git_enabled": self.version_manager.git_enabled,
            "can_update": self.version_manager.git_enabled,
            "project_health": self._check_project_health(),
            "component_status": self._check_component_health()
        }
    
    def _check_project_health(self) -> str:
        """检查项目健康状况"""
        health_indicators = []
        
        # 检查关键文件存在
        critical_files = [
            "src/dsgs_context_engineering/core/skill.py",
            "src/dsgs_context_engineering/skills/context_analysis.py",
            "src/dsgs_context_engineering/skills/context_optimization.py",
            "src/dsgs_context_engineering/skills/cognitive_template.py"
        ]
        
        missing_files = []
        for file_path in critical_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)
        
        if missing_files:
            health_indicators.append(f"Missing critical files: {len(missing_files)}")
        else:
            health_indicators.append("All critical files present")
        
        # 检查Git状态
        if self.version_manager.git_enabled:
            try:
                result = subprocess.run(
                    ["git", "status", "--porcelain"], 
                    capture_output=True, 
                    text=True,
                    cwd=self.project_root
                )
                if result.stdout.strip():
                    health_indicators.append(f"Uncommitted changes: {len(result.stdout.split())}")
                else:
                    health_indicators.append("No uncommitted changes")
            except:
                health_indicators.append("Git status check failed")
        else:
            health_indicators.append("Git not initialized")
        
        return ", ".join(health_indicators)
    
    def _check_component_health(self) -> Dict[str, str]:
        """检查组件健康状况"""
        components = {
            "context_analysis": self._check_component("Context Analysis Skill"),
            "context_optimization": self._check_component("Context Optimization Skill"),
            "cognitive_template": self._check_component("Cognitive Template Skill"),
        }
        return components
    
    def _check_component(self, component_name: str) -> str:
        """检查单个组件"""
        try:
            if component_name == "Context Analysis Skill":
                from src.dsgs_context_engineering.skills_system_real import ContextAnalysisSkill
                skill = ContextAnalysisSkill()
                result = skill.execute_with_ai("test context", {})
                return "healthy" if result['success'] else "unhealthy"
            elif component_name == "Context Optimization Skill":
                from src.dsgs_context_engineering.skills_system_real import ContextOptimizationSkill
                skill = ContextOptimizationSkill()
                result = skill.execute_with_ai("test", {})
                return "healthy" if result['success'] else "unhealthy"
            elif component_name == "Cognitive Template Skill":
                from src.dsgs_context_engineering.skills_system_real import CognitiveTemplateSkill
                skill = CognitiveTemplateSkill()
                result = skill.execute_with_ai("test", {})
                return "healthy" if result['success'] else "unhealthy"
            else:
                return "unknown"
        except Exception:
            return "unhealthy"
    
    def perform_update(self, force: bool = False) -> Dict[str, Any]:
        """执行更新"""
        readiness = self.check_update_readiness()
        
        if not readiness['can_update'] and not force:
            return {
                "success": False,
                "error": "Cannot perform update: Git not enabled for this project"
            }
        
        if not readiness['update_available'] and not force:
            return {
                "success": True,
                "message": "No updates available",
                "current_version": readiness['current_version']
            }
        
        # 进行备份
        backup_result = self._create_backup()
        if not backup_result['success'] and not force:
            return backup_result
        
        # 执行系统更新
        update_result = self.version_manager.update_system()
        
        # 创建更新清单并记录
        if update_result['success']:
            manifest = self.create_update_manifest()
            self.log_update(manifest)
        
        return update_result
    
    def _create_backup(self) -> Dict[str, Any]:
        """创建备份"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = Path(f"backup_{timestamp}")
            backup_dir.mkdir(exist_ok=True)
            
            # 备份关键文件
            files_to_backup = [
                "src/dsgs_context_engineering/core/skill.py",
                "src/dsgs_context_engineering/skills/context_analysis.py",
                "src/dsgs_context_engineering/skills/context_optimization.py", 
                "src/dsgs_context_engineering/skills/cognitive_template.py",
                "VERSION",
                "pyproject.toml"
            ]
            
            for file_path in files_to_backup:
                source = Path(file_path)
                if source.exists():
                    dest = backup_dir / source.name
                    dest.write_bytes(source.read_bytes())
            
            return {
                "success": True,
                "backup_location": str(backup_dir),
                "timestamp": timestamp
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Backup creation failed: {str(e)}"
            }


def execute_version_command(args: Dict[str, Any]) -> str:
    """
    执行版本相关的命令
    """
    command = args.get('command', 'status')
    updater = DSGSContextSkillsUpdater()
    
    if command == 'status':
        readiness = updater.check_update_readiness()
        output = []
        output.append("DSGS Context Engineering Skills - 版本状态:")
        output.append(f"当前版本: {readiness['current_version']}")
        output.append(f"更新可用: {'是' if readiness['update_available'] else '否'}")
        if readiness['update_available']:
            output.append(f"最新版本: {readiness['latest_version']}")
        output.append(f"Git支持: {'启用' if readiness['git_enabled'] else '禁用'}")
        output.append(f"项目健康: {readiness['project_health']}")
        return "\n".join(output)
    
    elif command == 'check':
        readiness = updater.check_update_readiness()
        output = []
        output.append("DSGS Context Engineering Skills - 更新检查:")
        output.append(f"版本: {readiness['current_version']} → {readiness['latest_version']}")
        output.append(f"可用更新: {readiness['update_available']}")
        output.append(f"可更新: {readiness['can_update']}")
        return "\n".join(output)
    
    elif command == 'update':
        result = updater.perform_update(force=args.get('force', False))
        if result['success']:
            return f"更新成功: {result.get('message', 'System updated')}"
        else:
            return f"更新失败: {result.get('error', 'Unknown error')}"
    
    elif command == 'backup':
        backup_result = updater._create_backup()
        if backup_result['success']:
            return f"备份成功: {backup_result['backup_location']}"
        else:
            return f"备份失败: {backup_result['error']}"
    
    else:
        return f"未知命令: {command}. 可用命令: status, check, update, backup"


# 版本管理CLI工具
def cli_main():
    """版本管理CLI入口点"""
    if len(sys.argv) < 2:
        print("DSGS Context Engineering Skills - 版本管理工具")
        print("用法:")
        print("  python -m version_manager status    # 查看当前状态")
        print("  python -m version_manager check     # 检查更新") 
        print("  python -m version_manager update    # 更新系统")
        print("  python -m version_manager backup    # 创建备份")
        return 0
    
    command = sys.argv[1]
    args = {
        'command': command,
        'force': '--force' in sys.argv or '-f' in sys.argv
    }
    
    result = execute_version_command(args)
    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(cli_main())