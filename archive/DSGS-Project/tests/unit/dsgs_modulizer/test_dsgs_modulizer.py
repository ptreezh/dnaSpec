# dsgs-modulizer子技能单元测试

import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'src'))

def test_skill_metadata():
    """测试技能元数据定义"""
    # 测试SKILL.md文件存在
    skill_md_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'skills', 'dsgs-modulizer', 'SKILL.md')
    assert os.path.exists(skill_md_path), "SKILL.md文件应该存在"
    
    # 读取SKILL.md内容
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 验证YAML前言存在
    assert content.startswith('---'), "文件应该以YAML前言开始"
    
    # 验证必需字段
    assert 'name: dsgs-modulizer' in content, "应该包含正确的技能名称"
    assert 'description:' in content, "应该包含描述字段"

def test_skill_basic_functionality():
    """测试技能基本功能"""
    # 测试技能可以被导入
    try:
        from dsgs_modulizer import DSGS_Modulizer
        skill = DSGS_Modulizer()
        assert skill is not None, "技能实例不应该为空"
        assert skill.name == "dsgs-modulizer", "技能名称应该正确"
    except ImportError as e:
        assert False, f"技能模块导入失败: {e}"

def test_skill_capabilities():
    """测试技能能力"""
    from dsgs_modulizer import DSGS_Modulizer
    skill = DSGS_Modulizer()
    
    # 验证技能能力列表
    expected_capabilities = [
        "bottom_up_analysis",
        "maturity_assessment",
        "component_sealing",
        "risk_evaluation"
    ]
    
    for capability in expected_capabilities:
        assert capability in skill.capabilities, f"技能能力列表应该包含: {capability}"

def test_skill_processing():
    """测试技能处理功能"""
    from dsgs_modulizer import DSGS_Modulizer
    skill = DSGS_Modulizer()
    
    # 测试正常请求处理
    test_request = "Analyze system components maturity and modularization opportunities"
    result = skill.process_request(test_request)
    
    assert result["status"] == "completed", "处理状态应该正确"
    assert result["skill"] == "dsgs-modulizer", "技能名称应该正确"
    assert result["request"] == test_request, "请求内容应该正确"
    assert "modularization_result" in result, "应该包含模块化结果"
    assert "timestamp" in result, "应该包含时间戳"

def test_skill_error_handling():
    """测试技能错误处理"""
    from dsgs_modulizer import DSGS_Modulizer
    skill = DSGS_Modulizer()
    
    # 测试空输入处理
    empty_inputs = ["", "   ", "\n\t"]
    for input_val in empty_inputs:
        result = skill.process_request(input_val)
        assert "error" in result, f"空输入 '{input_val}' 应该返回错误"
    
    # 测试None输入处理
    result = skill.process_request(None)
    assert "error" in result, "None输入应该返回错误"

def test_key_points_extraction():
    """测试关键点提取功能"""
    from dsgs_modulizer import DSGS_Modulizer
    skill = DSGS_Modulizer()
    
    # 测试关键点提取
    test_cases = [
        ("Check module maturity and sealing", ["module", "maturity", "seal"]),
        ("Analyze component level systems", ["component", "system"]),
        ("Perform bottom-up modularization", ["bottom_up"])
    ]
    
    for request, expected_points in test_cases:
        key_points = skill._extract_key_points(request)
        for point in expected_points:
            assert point in key_points, f"请求 '{request}' 应该提取关键点 '{point}'"

def test_modularization_analysis():
    """测试模块化分析功能"""
    from dsgs_modulizer import DSGS_Modulizer
    skill = DSGS_Modulizer()
    
    # 测试模块化分析
    test_request = "Perform comprehensive modularization analysis for the system"
    context = {}
    result = skill.process_request(test_request, context)
    
    assert result["status"] == "completed", "处理状态应该正确"
    modularization_result = result["modularization_result"]
    assert "components_analyzed" in modularization_result, "分析结果应该包含分析的组件"
    assert "maturity_assessments" in modularization_result, "分析结果应该包含成熟度评估"

if __name__ == "__main__":
    # 简单测试执行
    print("Running dsgs-modulizer tests...")
    
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
        test_skill_capabilities()
        print("✓ test_skill_capabilities passed")
    except Exception as e:
        print(f"✗ test_skill_capabilities failed: {e}")
    
    try:
        test_skill_processing()
        print("✓ test_skill_processing passed")
    except Exception as e:
        print(f"✗ test_skill_processing failed: {e}")
    
    try:
        test_skill_error_handling()
        print("✓ test_skill_error_handling passed")
    except Exception as e:
        print(f"✗ test_skill_error_handling failed: {e}")
    
    try:
        test_key_points_extraction()
        print("✓ test_key_points_extraction passed")
    except Exception as e:
        print(f"✗ test_key_points_extraction failed: {e}")
    
    try:
        test_modularization_analysis()
        print("✓ test_modularization_analysis passed")
    except Exception as e:
        print(f"✗ test_modularization_analysis failed: {e}")
    
    print("All tests completed.")