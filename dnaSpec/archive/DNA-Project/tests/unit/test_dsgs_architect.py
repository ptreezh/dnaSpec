# dnaspec-architect主技能单元测试

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

def test_skill_metadata():
    """测试技能元数据定义"""
    # 测试SKILL.md文件存在
    skill_md_path = os.path.join(os.path.dirname(__file__), '..', '..', 'skills', 'dnaspec-architect', 'SKILL.md')
    assert os.path.exists(skill_md_path), "SKILL.md文件应该存在"
    
    # 读取SKILL.md内容
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 验证YAML前言存在
    assert content.startswith('---'), "文件应该以YAML前言开始"
    
    # 验证必需字段
    assert 'name: dnaspec-architect' in content, "应该包含正确的技能名称"
    assert 'description:' in content, "应该包含描述字段"
    
    # 验证描述内容
    assert 'complex projects' in content, "描述应该包含复杂项目关键词"
    assert 'architecture design' in content, "描述应该包含架构设计关键词"

def test_skill_basic_functionality():
    """测试技能基本功能"""
    # 测试技能可以被导入
    try:
        from dnaspec_architect import DNASPECArchitect
        skill = DNASPECArchitect()
        assert skill is not None, "技能实例不应该为空"
        assert skill.name == "dnaspec-architect", "技能名称应该正确"
    except ImportError as e:
        assert False, f"技能模块导入失败: {e}"

def test_skill_routing():
    """测试技能路由功能"""
    from dnaspec_architect import DNASPECArchitect
    skill = DNASPECArchitect()
    
    # 测试技能可以识别不同类型的请求
    test_cases = [
        ("Design architecture for a web application", "dnaspec-system-architect"),
        ("Decompose tasks for mobile app development", "dnaspec-task-decomposer"),
        ("Create agents for microservices system", "dnaspec-agent-creator"),
        ("Generate constraints for API design", "dnaspec-constraint-generator"),
        ("Unknown request type", "dnaspec-system-architect")  # 默认路由
    ]
    
    # 验证每个请求都能被正确路由
    for request, expected_skill in test_cases:
        routed_skill = skill._route_request(request)
        assert routed_skill == expected_skill, f"请求 '{request}' 应该路由到 '{expected_skill}', 但实际路由到 '{routed_skill}'"

def test_skill_integration_points():
    """测试技能集成点"""
    from dnaspec_architect import DNASPECArchitect
    skill = DNASPECArchitect()
    
    # 验证技能可以与其他子技能交互
    expected_subskills = [
        'dnaspec-system-architect',
        'dnaspec-task-decomposer', 
        'dnaspec-agent-creator',
        'dnaspec-constraint-generator'
    ]
    
    # 验证子技能列表
    for expected_skill in expected_subskills:
        assert expected_skill in skill.subskills, f"子技能列表应该包含: {expected_skill}"

def test_skill_error_handling():
    """测试技能错误处理"""
    from dnaspec_architect import DNASPECArchitect
    skill = DNASPECArchitect()
    
    # 测试空输入处理
    empty_inputs = ["", "   ", "\n\t"]
    for input_val in empty_inputs:
        result = skill.process_request(input_val)
        assert "error" in result, f"空输入 '{input_val}' 应该返回错误"
    
    # 测试None输入处理
    result = skill.process_request(None)
    assert "error" in result, "None输入应该返回错误"

def test_skill_processing():
    """测试技能处理功能"""
    from dnaspec_architect import DNASPECArchitect
    skill = DNASPECArchitect()
    
    # 测试正常请求处理
    test_request = "Design architecture for a web application"
    result = skill.process_request(test_request)
    
    assert result["status"] == "processed", "处理状态应该正确"
    assert result["request"] == test_request, "请求内容应该正确"
    assert "skill_used" in result, "应该包含使用的技能信息"
    assert "timestamp" in result, "应该包含时间戳"

if __name__ == "__main__":
    # 简单测试执行
    print("Running basic tests...")
    
    try:
        test_skill_metadata()
        print("✓ test_skill_metadata passed")
    except Exception as e:
        print(f"✗ test_skill_metadata failed: {e}")
    
    try:
        test_skill_basic_functionality()
        print("✓ test_skill_basic_functionality passed")
    except Exception as e:
        print(f"✗ test_skill_basic_functionality failed: {e}")
    
    try:
        test_skill_routing()
        print("✓ test_skill_routing passed")
    except Exception as e:
        print(f"✗ test_skill_routing failed: {e}")
    
    try:
        test_skill_integration_points()
        print("✓ test_skill_integration_points passed")
    except Exception as e:
        print(f"✗ test_skill_integration_points failed: {e}")
    
    try:
        test_skill_error_handling()
        print("✓ test_skill_error_handling passed")
    except Exception as e:
        print(f"✗ test_skill_error_handling failed: {e}")
    
    try:
        test_skill_processing()
        print("✓ test_skill_processing passed")
    except Exception as e:
        print(f"✗ test_skill_processing failed: {e}")
    
    print("All tests completed.")