"""
DNASPEC技能基类测试
"""
import pytest
import time
from src.dna_spec_kit_integration.core.skill_base import BaseSkill, DetailLevel, ValidationError


class TestSkill(BaseSkill):
    """测试技能实现"""
    
    def __init__(self):
        super().__init__("test-skill", "测试技能")
    
    def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                          options: dict, context: dict) -> dict:
        """执行测试技能逻辑"""
        return {
            "processed_input": input_text.upper(),
            "detail_level_used": detail_level.value,
            "options_count": len(options),
            "context_keys": list(context.keys())
        }
    
    def _format_output(self, result_data: dict, detail_level: DetailLevel) -> dict:
        """格式化输出结果"""
        if detail_level == DetailLevel.BASIC:
            return {
                "result": result_data["processed_input"]
            }
        elif detail_level == DetailLevel.STANDARD:
            return {
                "result": result_data["processed_input"],
                "level": result_data["detail_level_used"]
            }
        else:  # DETAILED
            return result_data


def test_skill_base_initialization():
    """测试技能基类初始化"""
    skill = TestSkill()
    assert skill.name == "test-skill"
    assert skill.description == "测试技能"
    assert skill.version == "1.0.0"


def test_skill_base_execute_success_basic():
    """测试技能基类成功执行 - 基础级别"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "detail_level": "basic"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["result"] == "HELLO WORLD"
    assert "metadata" in result
    assert result["metadata"]["skill_name"] == "test-skill"
    assert result["metadata"]["detail_level"] == "basic"


def test_skill_base_execute_success_standard():
    """测试技能基类成功执行 - 标准级别"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "detail_level": "standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["result"] == "HELLO WORLD"
    assert result["data"]["level"] == "standard"
    assert "metadata" in result
    assert result["metadata"]["skill_name"] == "test-skill"
    assert result["metadata"]["detail_level"] == "standard"


def test_skill_base_execute_success_detailed():
    """测试技能基类成功执行 - 详细级别"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "detail_level": "detailed",
        "options": {"option1": "value1"},
        "context": {"user": "test"}
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "data" in result
    assert result["data"]["processed_input"] == "HELLO WORLD"
    assert result["data"]["detail_level_used"] == "detailed"
    assert result["data"]["options_count"] == 1
    assert result["data"]["context_keys"] == ["user"]
    assert "metadata" in result
    assert result["metadata"]["skill_name"] == "test-skill"
    assert result["metadata"]["detail_level"] == "detailed"


def test_skill_base_execute_default_detail_level():
    """测试技能基类使用默认详细级别"""
    skill = TestSkill()
    args = {
        "input": "hello world"
        # 没有指定detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_skill_base_execute_invalid_detail_level():
    """测试技能基类处理无效详细级别"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "detail_level": "invalid_level"
        # 无效的detail_level，应该使用默认值"standard"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert result["metadata"]["detail_level"] == "standard"


def test_skill_base_execute_missing_input():
    """测试技能基类处理缺失输入"""
    skill = TestSkill()
    args = {
        # 没有input参数
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_skill_base_execute_empty_input():
    """测试技能基类处理空输入"""
    skill = TestSkill()
    args = {
        "input": ""  # 空字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input cannot be empty" in result["error"]["message"]


def test_skill_base_execute_invalid_input_type():
    """测试技能基类处理无效输入类型"""
    skill = TestSkill()
    args = {
        "input": 123  # 数字而不是字符串
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "VALIDATION_ERROR"
    assert "Input must be a string" in result["error"]["message"]


def test_skill_base_execute_invalid_options_type():
    """测试技能基类处理无效选项类型"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "options": "invalid"  # 字符串而不是字典
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    # 由于_validate_input会将无效的options转换为空字典，
    # 但我们使用的是STANDARD级别，所以返回的是简化结构
    assert "data" in result
    assert "result" in result["data"]


def test_skill_base_execute_invalid_context_type():
    """测试技能基类处理无效上下文类型"""
    skill = TestSkill()
    args = {
        "input": "hello world",
        "context": "invalid"  # 字符串而不是字典
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    # 由于_validate_input会将无效的context转换为空字典，
    # 但我们使用的是STANDARD级别，所以返回的是简化结构
    assert "data" in result
    assert "result" in result["data"]


def test_skill_base_execute_with_exception():
    """测试技能基类处理执行异常"""
    
    class FailingSkill(BaseSkill):
        def __init__(self):
            super().__init__("failing-skill", "失败技能")
        
        def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                              options: dict, context: dict) -> dict:
            raise RuntimeError("模拟执行错误")
    
    skill = FailingSkill()
    args = {
        "input": "hello world"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "error"
    assert result["error"]["type"] == "RuntimeError"
    assert "模拟执行错误" in result["error"]["message"]
    assert result["error"]["code"] == "EXECUTION_ERROR"


def test_skill_base_execution_time_measurement():
    """测试技能基类执行时间测量"""
    
    class SlowSkill(BaseSkill):
        def __init__(self):
            super().__init__("slow-skill", "慢速技能")
        
        def _execute_skill_logic(self, input_text: str, detail_level: DetailLevel, 
                              options: dict, context: dict) -> dict:
            time.sleep(0.01)  # 模拟耗时操作
            return {"result": "done"}
    
    skill = SlowSkill()
    args = {
        "input": "hello world"
    }
    
    result = skill.execute(args)
    
    assert result["status"] == "success"
    assert "metadata" in result
    assert "execution_time" in result["metadata"]
    # 执行时间应该大于0.01秒
    assert result["metadata"]["execution_time"] >= 0.01


def test_skill_base_confidence_calculation():
    """测试技能基类置信度计算"""
    skill = TestSkill()
    
    # 短输入应该有较低置信度
    args_short = {"input": "hi"}
    result_short = skill.execute(args_short)
    confidence_short = result_short["metadata"]["confidence"]
    
    # 长输入应该有较高置信度
    args_long = {"input": "this is a much longer input that should have higher confidence"}
    result_long = skill.execute(args_long)
    confidence_long = result_long["metadata"]["confidence"]
    
    assert result_short["status"] == "success"
    assert result_long["status"] == "success"
    # 长输入的置信度应该高于短输入
    assert confidence_long >= confidence_short