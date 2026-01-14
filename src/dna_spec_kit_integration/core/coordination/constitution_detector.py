"""
宪法检测器模块
负责检测项目中是否存在协调机制和宪法配置
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class ConstitutionStatus(Enum):
    """宪法状态枚举"""
    FULLY_CONFIGURED = "fully_configured"      # 完全配置
    PARTIALLY_CONFIGURED = "partially_configured"  # 部分配置
    MINIMAL_CONFIGURED = "minimal_configured"  # 最小配置
    NOT_CONFIGURED = "not_configured"          # 未配置


@dataclass
class ConstitutionInfo:
    """宪法信息数据类"""
    status: ConstitutionStatus
    has_project_constitution: bool
    has_dnaspec_directory: bool
    has_skill_mapping: bool
    has_cache_system: bool
    has_git_hooks: bool
    coordination_features: List[str]
    config_files: List[str]
    missing_features: List[str]
    confidence_score: float


class ConstitutionDetector:
    """
    宪法检测器
    检测项目中是否存在协调机制和相关配置文件
    """
    
    def __init__(self, project_root: str = None):
        """
        初始化宪法检测器
        
        Args:
            project_root: 项目根目录，默认为当前工作目录
        """
        self.project_root = Path(project_root or os.getcwd())
        self._constitution_info: Optional[ConstitutionInfo] = None
    
    def detect_constitution(self) -> ConstitutionInfo:
        """
        检测项目宪法和协调机制
        
        Returns:
            ConstitutionInfo: 宪法检测结果
        """
        if self._constitution_info:
            return self._constitution_info
        
        # 检测各项配置
        has_project_constitution = self._check_project_constitution()
        has_dnaspec_directory = self._check_dnaspec_directory()
        has_skill_mapping = self._check_skill_mapping()
        has_cache_system = self._check_cache_system()
        has_git_hooks = self._check_git_hooks()
        
        # 收集协调功能列表
        coordination_features = self._collect_coordination_features(
            has_project_constitution, has_dnaspec_directory, 
            has_skill_mapping, has_cache_system, has_git_hooks
        )
        
        # 收集配置文件列表
        config_files = self._collect_config_files()
        
        # 确定宪法状态
        status = self._determine_constitution_status(
            has_project_constitution, has_dnaspec_directory, 
            has_skill_mapping, has_cache_system, has_git_hooks
        )
        
        # 计算置信度分数
        confidence_score = self._calculate_confidence_score(
            has_project_constitution, has_dnaspec_directory, 
            has_skill_mapping, has_cache_system, has_git_hooks
        )
        
        # 识别缺失的功能
        missing_features = self._identify_missing_features(coordination_features)
        
        self._constitution_info = ConstitutionInfo(
            status=status,
            has_project_constitution=has_project_constitution,
            has_dnaspec_directory=has_dnaspec_directory,
            has_skill_mapping=has_skill_mapping,
            has_cache_system=has_cache_system,
            has_git_hooks=has_git_hooks,
            coordination_features=coordination_features,
            config_files=config_files,
            missing_features=missing_features,
            confidence_score=confidence_score
        )
        
        return self._constitution_info
    
    def _check_project_constitution(self) -> bool:
        """检查是否存在项目宪法文件"""
        constitution_files = [
            "PROJECT_CONSTITUTION.md",
            "project_constitution.md",
            "PROJECT_SPEC.json",
            "project_spec.json"
        ]
        
        for filename in constitution_files:
            if (self.project_root / filename).exists():
                return True
        return False
    
    def _check_dnaspec_directory(self) -> bool:
        """检查是否存在.dnaspec目录"""
        dnaspec_dir = self.project_root / ".dnaspec"
        return dnaspec_dir.exists() and dnaspec_dir.is_dir()
    
    def _check_skill_mapping(self) -> bool:
        """检查是否存在技能映射配置"""
        # 检查可能的技能映射配置文件
        mapping_files = [
            ".dnaspec/skills_mapping.json",
            "skills_mapping.json",
            ".dnaspec/coordination_config.json",
            "coordination_config.json"
        ]
        
        for filename in mapping_files:
            if (self.project_root / filename).exists():
                return True
        
        # 检查技能执行器是否存在
        skill_executor_paths = [
            "src/dna_spec_kit_integration/core/skill_executor.py",
            "skills/skill_executor.py"
        ]
        
        for path in skill_executor_paths:
            if (self.project_root / path).exists():
                return True
        
        return False
    
    def _check_cache_system(self) -> bool:
        """检查是否存在缓存系统配置"""
        # 检查缓存系统相关文件和目录
        cache_indicators = [
            ".dnaspec/cache",
            ".dnaspec/staging",
            ".dnaspec/meta",
            "cache_manager.py",
            "git_constitution.json"
        ]
        
        for indicator in cache_indicators:
            if (self.project_root / indicator).exists():
                return True
        
        return False
    
    def _check_git_hooks(self) -> bool:
        """检查是否存在Git钩子配置"""
        git_hooks_dir = self.project_root / ".git" / "hooks"
        if not git_hooks_dir.exists():
            return False
        
        # 检查是否有DNASPEC相关的钩子
        hook_files = list(git_hooks_dir.glob("*"))
        for hook_file in hook_files:
            if hook_file.is_file() and hook_file.stat().st_size > 0:
                # 简单检查文件内容是否包含DNASPEC相关标识
                try:
                    content = hook_file.read_text(encoding='utf-8', errors='ignore')
                    if 'dnaspec' in content.lower() or 'DNASPEC' in content:
                        return True
                except:
                    pass
        
        return False
    
    def _collect_coordination_features(self, 
                                     has_constitution: bool,
                                     has_directory: bool,
                                     has_mapping: bool,
                                     has_cache: bool,
                                     has_hooks: bool) -> List[str]:
        """收集可用的协调功能列表"""
        features = []
        
        if has_constitution:
            features.append("project_constitution")
        
        if has_directory:
            features.append("dnaspec_directory")
            
        if has_mapping:
            features.extend([
                "skill_mapping",
                "unified_execution",
                "skill_coordination"
            ])
            
        if has_cache:
            features.extend([
                "cache_management",
                "file_validation",
                "staging_workflow"
            ])
            
        if has_hooks:
            features.extend([
                "git_hooks",
                "automated_validation",
                "commit_enforcement"
            ])
        
        return features
    
    def _collect_config_files(self) -> List[str]:
        """收集存在的配置文件列表"""
        config_files = []
        
        # 检查各种配置文件
        possible_configs = [
            "PROJECT_CONSTITUTION.md",
            "PROJECT_SPEC.json",
            ".dnaspec/skills_mapping.json",
            ".dnaspec/coordination_config.json",
            ".dnaspec/git_constitution.json",
            ".dnaspec/cache_config.json"
        ]
        
        for config_file in possible_configs:
            full_path = self.project_root / config_file
            if full_path.exists():
                config_files.append(config_file)
        
        return config_files
    
    def _determine_constitution_status(self,
                                     has_constitution: bool,
                                     has_directory: bool,
                                     has_mapping: bool,
                                     has_cache: bool,
                                     has_hooks: bool) -> ConstitutionStatus:
        """确定宪法配置状态"""
        configured_features = sum([
            has_constitution, has_directory, has_mapping, 
            has_cache, has_hooks
        ])
        
        if configured_features >= 4:
            return ConstitutionStatus.FULLY_CONFIGURED
        elif configured_features >= 2:
            return ConstitutionStatus.PARTIALLY_CONFIGURED
        elif configured_features >= 1:
            return ConstitutionStatus.MINIMAL_CONFIGURED
        else:
            return ConstitutionStatus.NOT_CONFIGURED
    
    def _calculate_confidence_score(self,
                                  has_constitution: bool,
                                  has_directory: bool,
                                  has_mapping: bool,
                                  has_cache: bool,
                                  has_hooks: bool) -> float:
        """计算协调机制置信度分数"""
        weights = {
            'constitution': 0.3,
            'directory': 0.2,
            'mapping': 0.25,
            'cache': 0.15,
            'hooks': 0.1
        }
        
        score = 0.0
        if has_constitution:
            score += weights['constitution']
        if has_directory:
            score += weights['directory']
        if has_mapping:
            score += weights['mapping']
        if has_cache:
            score += weights['cache']
        if has_hooks:
            score += weights['hooks']
        
        return round(score, 2)
    
    def _identify_missing_features(self, existing_features: List[str]) -> List[str]:
        """识别缺失的协调功能"""
        all_features = [
            "project_constitution",
            "dnaspec_directory", 
            "skill_mapping",
            "unified_execution",
            "skill_coordination",
            "cache_management",
            "file_validation",
            "staging_workflow",
            "git_hooks",
            "automated_validation",
            "commit_enforcement"
        ]
        
        return [feature for feature in all_features if feature not in existing_features]
    
    def should_use_coordination(self) -> bool:
        """
        判断是否应该使用协调模式
        
        Returns:
            bool: 是否使用协调模式
        """
        info = self.detect_constitution()
        
        # 阈值：置信度分数大于0.3时启用协调模式
        return info.confidence_score > 0.3
    
    def get_coordination_recommendations(self) -> List[str]:
        """
        获取协调机制配置建议
        
        Returns:
            List[str]: 配置建议列表
        """
        info = self.detect_constitution()
        recommendations = []
        
        if info.status == ConstitutionStatus.NOT_CONFIGURED:
            recommendations.extend([
                "创建 PROJECT_CONSTITUTION.md 定义项目协作规则",
                "初始化 .dnaspec 目录结构",
                "配置技能映射和统一执行器"
            ])
        elif info.status == ConstitutionStatus.MINIMAL_CONFIGURED:
            recommendations.extend([
                "完善项目宪法配置",
                "启用缓存系统和文件验证",
                "配置Git钩子自动化验证"
            ])
        elif info.status == ConstitutionStatus.PARTIALLY_CONFIGURED:
            recommendations.extend([
                "补全缺失的协调功能",
                "优化技能映射配置",
                "完善缓存和验证工作流"
            ])
        
        return recommendations
    
    def get_status_summary(self) -> Dict[str, Any]:
        """
        获取状态摘要信息
        
        Returns:
            Dict[str, Any]: 状态摘要
        """
        info = self.detect_constitution()
        
        return {
            "status": info.status.value,
            "confidence_score": info.confidence_score,
            "coordination_recommended": self.should_use_coordination(),
            "available_features": info.coordination_features,
            "missing_features": info.missing_features,
            "config_files": info.config_files,
            "recommendations": self.get_coordination_recommendations()
        }