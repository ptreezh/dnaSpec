"""
智能匹配系统单元测试
"""
import sys
import os
import pytest
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dsgs_spec_kit_integration.core.matcher import IntelligentMatcher, MatchResult


class TestIntelligentMatcher:
    """IntelligentMatcher单元测试"""
    
    def test_matcher_initialization(self):
        """测试匹配器初始化"""
        matcher = IntelligentMatcher()
        assert matcher is not None
        assert matcher.match_threshold == 0.3
        assert len(matcher._skill_keywords) == 0
        assert len(matcher._command_patterns) == 0
    
    def test_skill_keywords_registration(self):
        """测试技能关键词注册"""
        matcher = IntelligentMatcher()
        
        # 注册技能关键词
        keywords = ['架构', '系统设计', 'architecture']
        result = matcher.register_skill_keywords('dsgs-architect', keywords)
        assert result is True
        assert 'dsgs-architect' in matcher._skill_keywords
        assert matcher._skill_keywords['dsgs-architect'] == keywords
        
        # 测试无效注册
        result = matcher.register_skill_keywords('', keywords)
        assert result is False
        
        result = matcher.register_skill_keywords('dsgs-test', [])
        assert result is False
    
    def test_command_pattern_registration(self):
        """测试命令模式注册"""
        matcher = IntelligentMatcher()
        
        # 注册命令模式
        patterns = ['/speckit.dsgs.architect', '/architect']
        result = matcher.register_command_pattern('dsgs-architect', patterns)
        assert result is True
        assert 'dsgs-architect' in matcher._command_patterns
        assert matcher._command_patterns['dsgs-architect'] == patterns
    
    def test_spec_kit_command_matching(self):
        """测试spec.kit命令匹配"""
        matcher = IntelligentMatcher()
        
        # 测试有效的spec.kit命令
        result = matcher._match_spec_kit_commands("/speckit.dsgs.architect 设计电商系统")
        assert result is not None
        assert isinstance(result, MatchResult)
        assert result.skill_name == "dsgs-architect"
        assert result.confidence > 0.9
        assert result.match_type == "spec_kit_command"
        
        # 测试无效的命令
        result = matcher._match_spec_kit_commands("普通文本请求")
        assert result is None
        
        # 测试空命令
        result = matcher._match_spec_kit_commands("")
        assert result is None
    
    def test_keyword_matching(self):
        """测试关键词匹配"""
        matcher = IntelligentMatcher()
        
        # 注册技能关键词
        matcher.register_skill_keywords('dsgs-architect', ['架构', '系统设计', 'architecture'])
        matcher.register_skill_keywords('dsgs-agent-creator', ['智能体', 'agent', 'create'])
        
        # 测试关键词匹配
        matches = matcher._find_keyword_matches("设计系统架构")
        assert len(matches) > 0
        assert any(match['skill_name'] == 'dsgs-architect' for match in matches)
        
        # 测试无匹配
        matches = matcher._find_keyword_matches("无关文本")
        assert len(matches) == 0
    
    def test_semantic_matching(self):
        """测试语义匹配"""
        matcher = IntelligentMatcher()
        
        # 注册技能关键词
        matcher.register_skill_keywords('dsgs-architect', ['架构', '系统设计', 'architecture'])
        
        # 测试语义匹配
        matches = matcher._find_semantic_matches("我需要设计一个系统架构")
        assert isinstance(matches, list)
        # 语义匹配可能为空，因为简单实现
    
    def test_context_matching(self):
        """测试上下文匹配"""
        matcher = IntelligentMatcher()
        
        # 注册技能关键词
        matcher.register_skill_keywords('dsgs-architect', ['架构', '系统设计'])
        
        # 测试上下文匹配
        matches = matcher._find_context_matches("创建系统架构设计")
        assert isinstance(matches, list)
    
    def test_intelligent_matching(self):
        """测试智能匹配"""
        matcher = IntelligentMatcher()
        
        # 注册技能关键词
        matcher.register_skill_keywords('dsgs-architect', ['架构', '系统设计', 'architecture'])
        matcher.register_skill_keywords('dsgs-agent-creator', ['智能体', 'agent', 'create'])
        
        # 测试智能匹配
        result = matcher.match_intelligently("设计系统架构")
        assert result is not None
        assert isinstance(result, MatchResult)
        
        # 测试spec.kit命令高优先级匹配
        result = matcher.match_intelligently("/speckit.dsgs.architect 电商系统")
        assert result is not None
        assert result.skill_name == "dsgs-architect"
        assert result.confidence > 0.9
        
        # 测试无效请求
        result = matcher.match_intelligently("")
        assert result is None
    
    def test_matcher_info(self):
        """测试获取匹配器信息"""
        matcher = IntelligentMatcher()
        
        # 注册一些数据
        matcher.register_skill_keywords('dsgs-architect', ['架构'])
        matcher.register_command_pattern('dsgs-architect', ['/speckit.dsgs.architect'])
        
        info = matcher.get_matcher_info()
        assert isinstance(info, dict)
        assert 'match_threshold' in info
        assert 'registered_skills_count' in info
        assert 'registered_skills' in info
        assert 'registered_patterns_count' in info
        assert info['registered_skills_count'] == 1