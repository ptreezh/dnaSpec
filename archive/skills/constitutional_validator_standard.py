"""
DNASPEC 标准技能定义 - 符合Claude Skills规范
"""
from typing import Dict, Any, Union, List, Optional
import json
from datetime import datetime
import re

class ClaudeSkill:
    """
    Claude Skills标准基类
    遵循Claude Skills规范和最佳实践
    """
    
    def __init__(self, name: str, description: str, version: str = "1.0.0"):
        self.name = name
        self.description = description
        self.version = version
        self.created_at = datetime.now().isoformat()
        
    def execute(self, args: Dict[str, Any]) -> Union[str, Dict[str, Any]]:
        """
        Claude Skills标准执行接口
        返回str或Dict[str, Any]格式结果
        """
        # 1. 验证输入参数（最小认知负荷）
        validation_result = self._validate_inputs(args)
        if not validation_result["valid"]:
            return f"❌ 输入验证失败: {validation_result['error']}"
        
        # 2. 执行核心逻辑
        try:
            result = self._execute_core_logic(args)
            
            # 3. 格式化输出为渐进式披露格式
            formatted_result = self._format_progressive_output(result, args)
            
            return formatted_result
            
        except Exception as e:
            return f"❌ 技能执行错误: {str(e)}"
    
    def _validate_inputs(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """验证输入参数 - 最小认知负荷"""
        # 基础验证
        if not isinstance(args, dict):
            return {"valid": False, "error": "参数必须是字典格式"}
        
        return {"valid": True, "error": None}
    
    def _execute_core_logic(self, args: Dict[str, Any]) -> Any:
        """执行核心逻辑 - 子类必须实现"""
        raise NotImplementedError("_execute_core_logic方法必须被子类实现")
    
    def _format_progressive_output(self, result: Any, args: Dict[str, Any]) -> Union[str, Dict[str, Any]]:
        """
        格式化渐进式披露输出
        符合Claude Skills的输出规范
        """
        # 默认实现：返回字符串结果
        if isinstance(result, str):
            return result
        else:
            return json.dumps(result, ensure_ascii=False, indent=2)
    
    def get_manifest(self) -> Dict[str, Any]:
        """
        获取技能清单信息 - Claude Skills标准
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "created_at": self.created_at,
            "parameters": self._get_parameters_schema(),
            "required_parameters": self._get_required_parameters(),
            "examples": self._get_examples()
        }
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        """获取参数模式 - 子类可重写"""
        return {
            "type": "object",
            "properties": {
                "context": {
                    "type": "string",
                    "description": "主要上下文或查询内容"
                },
                "detailed": {
                    "type": "boolean", 
                    "description": "是否返回详细信息",
                    "default": False
                }
            }
        }
    
    def _get_required_parameters(self) -> List[str]:
        """获取必需参数 - 子类可重写"""
        return ["context"]
    
    def _get_examples(self) -> List[Dict[str, Any]]:
        """获取使用示例 - 子类可重写"""
        return [
            {
                "input": {"context": "用户认证系统需求分析"},
                "description": "分析用户认证系统的需求质量"
            }
        ]

class ConstitutionalValidatorSkill(ClaudeSkill):
    """
    宪法验证技能 - Claude Skills标准实现
    """
    
    def __init__(self):
        super().__init__(
            name="dnaspec-constitutional-validator",
            description="使用宪法原则验证内容质量的技能，确保AI生成内容符合认知优化原则",
            version="1.0.0"
        )
    
    def _get_parameters_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "content": {
                    "type": "string",
                    "description": "要验证的内容"
                },
                "context": {
                    "type": "string", 
                    "description": "上下文信息（content的别名）"
                },
                "principle": {
                    "type": "string",
                    "description": "要验证的宪法原则类型",
                    "enum": ["all", "progressive_disclosure", "cognitive_convenience", 
                            "information_encapsulation", "cognitive_gestalt"],
                    "default": "all"
                },
                "detailed": {
                    "type": "boolean",
                    "description": "是否返回详细验证信息",
                    "default": False
                }
            }
        }
    
    def _get_required_parameters(self) -> List[str]:
        return ["content"]
    
    def _execute_core_logic(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行宪法验证 - 定量分析部分（程序逻辑）
        """
        content = args.get("content") or args.get("context", "")
        principle = args.get("principle", "all")
        detailed = args.get("detailed", False)
        
        # 验证内容是否为空
        if not content.strip():
            return {
                "error": "内容不能为空",
                "compliant": False
            }
        
        # 执行宪法验证（定量分析）
        validation_results = self._perform_constitutional_validation(content, principle)
        
        return {
            "content_length": len(content),
            "validation_results": validation_results,
            "overall_compliance": all(v["compliant"] for v in validation_results.values()),
            "principle_count": len(validation_results),
            "non_compliant_principles": [k for k, v in validation_results.items() if not v["compliant"]],
            "detailed": detailed
        }
    
    def _perform_constitutional_validation(self, content: str, principle: str) -> Dict[str, Dict[str, Any]]:
        """执行宪法验证 - 程序化定量分析"""
        results = {}
        
        if principle == "all" or principle == "progressive_disclosure":
            results["progressive_disclosure"] = self._validate_progressive_disclosure(content)
        
        if principle == "all" or principle == "cognitive_convenience":
            results["cognitive_convenience"] = self._validate_cognitive_convenience(content)
        
        if principle == "all" or principle == "information_encapsulation":
            results["information_encapsulation"] = self._validate_information_encapsulation(content)
        
        if principle == "all" or principle == "cognitive_gestalt":
            results["cognitive_gestalt"] = self._validate_cognitive_gestalt(content)
        
        return results
    
    def _validate_progressive_disclosure(self, content: str) -> Dict[str, Any]:
        """验证渐进披露原则"""
        # 定量分析：检查结构层次
        headers = len(re.findall(r'^#+\s+', content, re.MULTILINE))
        sub_headers = len(re.findall(r'^##+\s+', content, re.MULTILINE))
        has_structure = headers >= 1 and sub_headers >= 1
        content_separation = len(content.split('\n\n')) >= 2
        
        compliant = has_structure and content_separation
        confidence = min(1.0, (headers * 0.3 + sub_headers * 0.2 + (1 if content_separation else 0) * 0.5))
        
        return {
            "compliant": compliant,
            "confidence": round(confidence, 2),
            "feedback": f"渐进披露: {headers}个标题, {sub_headers}个子标题, {content_separation}个段落分隔" if compliant else "缺少层次结构或段落分离"
        }
    
    def _validate_cognitive_convenience(self, content: str) -> Dict[str, Any]:
        """验证认知便利原则"""
        # 定量分析：检查结构清晰度
        structure_elements = sum([
            bool(re.search(r'^(#|\d+\.)\s+', content, re.MULTILINE)),  # 标题或编号
            bool(re.search(r'^\s*[-*]\s+', content, re.MULTILINE)),    # 列表
            bool(re.search(r'\n\s*\n', content)),                       # 段落分离
        ])
        
        min_content_length = len(content.strip()) > 20
        has_sentences = content.count('.') + content.count('。') >= 1
        
        compliant = structure_elements >= 1 and min_content_length and has_sentences
        confidence = min(1.0, (structure_elements * 0.4 + (1 if min_content_length else 0) * 0.3 + (1 if has_sentences else 0) * 0.3))
        
        return {
            "compliant": compliant,
            "confidence": round(confidence, 2),
            "feedback": f"认知便利: {structure_elements}个结构元素, 长度{len(content)}字符" if compliant else "内容结构不清晰或长度不足"
        }
    
    def _validate_information_encapsulation(self, content: str) -> Dict[str, Any]:
        """验证信息封装原则"""
        # 定量分析：检查自包含性
        context_indicators = any(keyword in content.lower() for keyword in 
                               ['context', 'overview', 'description', 'purpose', 'function', 'role', '目标', '功能', '概述'])
        
        min_length = len(content.strip()) >= 30
        has_sentences = content.count('.') + content.count('。') >= 2 or len(content.split()) >= 10
        
        compliant = context_indicators and min_length and has_sentences
        
        confidence = min(1.0, (0.3 if context_indicators else 0) + (0.4 if min_length else 0) + (0.3 if has_sentences else 0))
        
        return {
            "compliant": compliant,
            "confidence": round(confidence, 2),
            "feedback": "信息封装: 包含上下文和完整信息" if compliant else "缺乏上下文信息或内容过短"
        }
    
    def _validate_cognitive_gestalt(self, content: str) -> Dict[str, Any]:
        """验证认知格式塔原则"""
        # 定量分析：检查完整性
        has_content = len(content.strip()) > 0
        has_structure = bool(re.search(r'^(#|\d+\.|[•\-•○▪])', content, re.MULTILINE))
        has_min_completeness = len(content) >= 20
        has_multiple_lines = len([line for line in content.split('\n') if line.strip()]) >= 2
        
        compliant = has_content and has_structure and has_min_completeness and has_multiple_lines
        
        confidence = min(1.0, (1 if has_content else 0.5) * 0.25 + (1 if has_structure else 0.5) * 0.25 + 
                        (1 if has_min_completeness else 0.5) * 0.25 + (1 if has_multiple_lines else 0.5) * 0.25)
        
        return {
            "compliant": compliant,
            "confidence": round(confidence, 2),
            "feedback": "认知格式塔: 形成完整认知单元" if compliant else "内容不完整或结构不连贯"
        }
    
    def _format_progressive_output(self, result: Dict[str, Any], args: Dict[str, Any]) -> str:
        """
        格式化渐进披露输出 - 符合Claude Skills规范
        """
        detailed = args.get("detailed", False)
        
        if result.get("error"):
            return f"❌ {result['error']}"
        
        lines = []
        
        # 主要结果（最小认知负荷）
        lines.append(f"📋 宪法验证结果")
        lines.append(f"长度: {result['content_length']} 字符")
        lines.append(f"合规: {'✅' if result['overall_compliance'] else '❌'}")
        lines.append(f"原则: {result['principle_count']} 项")
        
        if result['non_compliant_principles']:
            lines.append(f"违规: {', '.join(result['non_compliant_principles'])}")
        
        lines.append("")  # 空行
        
        # 详细信息（按需显示）
        if detailed:
            lines.append("🔍 验证详情:")
            for principle, validation in result['validation_results'].items():
                emoji = "🟢" if validation['compliant'] else "🔴"
                confidence_indicator = "🟢" if validation['confidence'] >= 0.7 else "🟡" if validation['confidence'] >= 0.4 else "🔴"
                
                lines.append(f"  {emoji} {principle}: {validation['feedback']}")
                lines.append(f"      置信度: {confidence_indicator} {validation['confidence']:.2f}")
        
        return "\n".join(lines)


# 核心技能实例
CONSTITUTIONAL_VALIDATOR_SKILL = ConstitutionalValidatorSkill()

def execute(args: Dict[str, Any]) -> str:
    """
    Claude Skills标准执行入口
    """
    return CONSTITUTIONAL_VALIDATOR_SKILL.execute(args)

def get_manifest() -> Dict[str, Any]:
    """
    获取技能清单
    """
    return CONSTITUTIONAL_VALIDATOR_SKILL.get_manifest()