
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from src.dsgs_spec_kit_integration.skills import architect

def test_architect_for_simple_ecommerce():
    """测试architect技能是否能为电商网站生成正确的架构图。"""
    
    # 准备输入参数
    args = {"description": "我想要一个简单的电商网站"}
    
    # 执行技能
    result = architect.execute(args)
    
    # 验证结果
    expected_architecture = "[WebApp] -> [API Server] -> [Database]"
    assert result == expected_architecture

def test_architect_for_blog():
    """测试architect技能是否能为博客系统生成正确的架构图。"""
    args = {"description": "一个个人博客"}
    result = architect.execute(args)
    expected_architecture = "[WebApp] -> [Database]"
    assert result == expected_architecture
