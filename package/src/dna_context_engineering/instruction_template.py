"""
Instruction Template Engine
为DNASPEC Context Engineering Skills提供标准化的指令模板
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import json
import re


class InstructionTemplate(ABC):
    """指令模板抽象基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def construct_prompt(self, context: str, params: Dict[str, Any] = None) -> str:
        """根据上下文和参数构建指令提示"""
        pass
    
    @abstractmethod
    def parse_response(self, response: str) -> Dict[str, Any]:
        """解析AI模型的响应"""
        pass
    
    def validate_params(self, params: Dict[str, Any]) -> List[str]:
        """验证参数，返回错误列表"""
        return []


class ContextAnalysisTemplate(InstructionTemplate):
    """上下文分析指令模板"""
    
    def __init__(self):
        super().__init__(
            name="context-analysis",
            description="用于分析上下文质量的五维指标模板"
        )
    
    def construct_prompt(self, context: str, params: Dict[str, Any] = None) -> str:
        """构建上下文分析指令"""
        params = params or {}
        
        language = params.get("language", "Chinese")
        
        if language == "Chinese":
            prompt = f"""
请对以下上下文进行专业分析，评估其质量：

上下文：
"{context}"

请按照以下五个维度进行评估：
1. 清晰度 (Clarity): 内容表述的明确程度 (0-1分)
2. 相关性 (Relevance): 与目标任务的相关程度 (0-1分)  
3. 完整性 (Completeness): 关键信息的完备程度 (0-1分)
4. 一致性 (Consistency): 内容之间的逻辑一致性 (0-1分)
5. 效率 (Efficiency): 信息密度和简洁性 (0-1分)

请以JSON格式返回分析结果：
{{
  "clarity": 数值 (0-1),
  "relevance": 数值 (0-1), 
  "completeness": 数值 (0-1),
  "consistency": 数值 (0-1),
  "efficiency": 数值 (0-1),
  "suggestions": ["建议1", "建议2", "建议3"],
  "issues": ["问题1", "问题2"]
}}
"""
        else:  # English
            prompt = f"""
Please conduct a professional analysis of the following context and evaluate its quality:

Context:
"{context}"

Evaluate according to the following five dimensions:
1. Clarity: Clearness of content expression (0-1 points)
2. Relevance: Degree of relevance to target task (0-1 points)
3. Completeness: Degree of completeness of key information (0-1 points) 
4. Consistency: Logical consistency within content (0-1 points)
5. Efficiency: Information density and conciseness (0-1 points)

Please return the analysis results in JSON format:
{{
  "clarity": number (0-1),
  "relevance": number (0-1),
  "completeness": number (0-1),
  "consistency": number (0-1), 
  "efficiency": number (0-1),
  "suggestions": ["suggestion1", "suggestion2", "suggestion3"],
  "issues": ["issue1", "issue2"]
}}
"""
        
        return prompt
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        """解析分析结果"""
        # 尝力查找JSON部分
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                # 验证必要的字段
                required_fields = ['clarity', 'relevance', 'completeness', 'consistency', 'efficiency']
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing field: {field}")
                
                # 验证数值范围
                for field in required_fields:
                    if not isinstance(result[field], (int, float)) or not 0 <= result[field] <= 1:
                        raise ValueError(f"Field {field} must be a number between 0 and 1")
                
                return result
            except json.JSONDecodeError:
                raise ValueError(f"Could not parse JSON from response: {response}")
        else:
            raise ValueError(f"No JSON found in response: {response}")


class ContextOptimizationTemplate(InstructionTemplate):
    """上下文优化指令模板"""
    
    def __init__(self):
        super().__init__(
            name="context-optimization", 
            description="用于优化上下文内容的模板"
        )
    
    def construct_prompt(self, context: str, params: Dict[str, Any] = None) -> str:
        """构建上下文优化指令"""
        params = params or {}
        
        optimization_goals = params.get("goals", ["clarity", "completeness"])
        language = params.get("language", "Chinese")
        
        if language == "Chinese":
            goals_str = ", ".join(optimization_goals)
            prompt = f"""
请对以下上下文进行优化，重点关注{goals_str}等方面：

原始上下文：
"{context}"

请返回：
1. 优化后的上下文内容
2. 应用的优化操作列表
3. 优化前后对比分析

请以JSON格式返回结果：
{{
  "optimized_context": "优化后的上下文",
  "applied_optimizations": ["应用的优化1", "应用的优化2"],
  "improvement_analysis": {{
    "clarity_change": 数值,
    "completeness_change": 数值
  }}
}}
"""
        else:  # English
            goals_str = ", ".join(optimization_goals)
            prompt = f"""
Please optimize the following context, focusing on aspects like {goals_str}:

Original Context:
"{context}"

Please return:
1. Optimized context content
2. Applied optimization operations list  
3. Before/after comparison analysis

Please return results in JSON format:
{{
  "optimized_context": "Optimized context",
  "applied_optimizations": ["Applied optimization 1", "Applied optimization 2"],
  "improvement_analysis": {{
    "clarity_change": number,
    "completeness_change": number
  }}
}}
"""
        
        return prompt
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        """解析优化结果"""
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                result = json.loads(json_str)
                
                required_fields = ['optimized_context', 'applied_optimizations']
                for field in required_fields:
                    if field not in result:
                        raise ValueError(f"Missing field: {field}")
                
                return result
            except json.JSONDecodeError:
                raise ValueError(f"Could not parse JSON from response: {response}")
        else:
            raise ValueError(f"No JSON found in response: {response}")


class CognitiveTemplate(InstructionTemplate):
    """认知模板指令"""
    
    def __init__(self):
        super().__init__(
            name="cognitive-template",
            description="认知模板应用指令模板"
        )
    
    def construct_prompt(self, context: str, params: Dict[str, Any] = None) -> str:
        """构建认知模板应用指令"""
        params = params or {}
        
        template_type = params.get("template_type", "chain-of-thought")
        language = params.get("language", "Chinese")
        
        if language == "Chinese":
            if template_type == "chain-of-thought":
                prompt = f"""
请使用思维链方法分析以下任务：

任务：{context}

请按以下步骤进行：
1. 问题理解
2. 步骤分解  
3. 中间推理
4. 验证检查
5. 最终答案

请以结构化格式返回分析过程和结果。
"""
            elif template_type == "few-shot":
                prompt = f"""
这是一个少样本学习任务。请参照以下示例：

示例1：
输入：分析电商系统架构
输出：[架构分析结果]

示例2：
输入：设计数据库模型
输出：[数据库设计结果]

现在请分析：
{context}

请按照上述示例的模式返回结果。
"""
            elif template_type == "verification":
                prompt = f"""
请对以下内容进行验证：

{context}

请执行以下验证步骤：
1. 初初答案
2. 逻辑一致性检查
3. 事实准确性检查
4. 完整性检查
5. 最终确认

请返回验证过程和结论。
"""
            else:  # 默认思维链
                prompt = f"""
请使用结构化方法分析以下任务：

任务：{context}

请按以下框架进行分析：
1. 问题理解
2. 步骤分解
3. 中间推理
4. 验证检查
5. 最终答案

请以结构化格式返回分析过程和结果。
"""
        else:  # English
            if template_type == "chain-of-thought":
                prompt = f"""
Please analyze the following task using chain of thought method:

Task: {context}

Please proceed with the following steps:
1. Problem Understanding
2. Step Decomposition
3. Intermediate Reasoning
4. Verification Check
5. Final Answer

Please return the analysis process and result in structured format.
"""
            elif template_type == "few-shot":
                prompt = f"""
This is a few-shot learning task. Please refer to the following examples:

Example 1:
Input: Analyze e-commerce system architecture
Output: [Architecture analysis result]

Example 2: 
Input: Design database model
Output: [Database design result]

Now please analyze:
{context}

Please return the result following the above example pattern.
"""
            elif template_type == "verification":
                prompt = f"""
Please verify the following content:

{context}

Please execute the following verification steps:
1. Preliminary Answer
2. Logic Consistency Check
3. Fact Accuracy Check  
4. Completeness Check
5. Final Confirmation

Please return the verification process and conclusion.
"""
            else:  # default chain of thought
                prompt = f"""
Please analyze the following task using structured method:

Task: {context}

Please proceed with the following framework:
1. Problem Understanding
2. Step Decomposition
3. Intermediate Reasoning
4. Verification Check
5. Final Answer

Please return the analysis process and result in structured format.
"""
        
        return prompt
    
    def parse_response(self, response: str) -> Dict[str, Any]:
        """解析认知模板结果"""
        # 认知模板的结果通常是结构化文本，直接返回
        return {
            "enhanced_context": response,
            "template_type": "cognitive-template",
            "processing_steps": self._extract_processing_steps(response)
        }
    
    def _extract_processing_steps(self, response: str) -> List[str]:
        """从响应中提取处理步骤"""
        # 简单提取步骤标签
        import re
        step_patterns = [
            r'(?:步骤|Step|Phase|Stage)\s*\d*[：:]\s*([^。\n]+)',
            r'(?:问题理解|Problem Understanding|问题分析|Problem Analysis)',
            r'(?:步骤分解|Step Decomposition|分析步骤|Analysis Steps)',
            r'(?:中间推理|Intermediate Reasoning|推理过程|Reasoning Process)',
            r'(?:验证检查|Verification Check|验证过程|Verification Process)',
            r'(?:最终答案|Final Answer|结论|Conclusion)'
        ]
        
        steps = []
        for pattern in step_patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            steps.extend(matches)
        
        return list(set(steps))  # 去重


class TemplateRegistry:
    """模板注册表，管理所有可用的指令模板"""
    
    def __init__(self):
        self.templates: Dict[str, InstructionTemplate] = {}
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """初始化默认模板"""
        default_templates = [
            ContextAnalysisTemplate(),
            ContextOptimizationTemplate(), 
            CognitiveTemplate()
        ]
        
        for template in default_templates:
            self.register_template(template)
    
    def register_template(self, template: InstructionTemplate):
        """注册指令模板"""
        self.templates[template.name] = template
    
    def get_template(self, name: str) -> InstructionTemplate:
        """获取指定名称的模板"""
        if name not in self.templates:
            raise KeyError(f"Template '{name}' not found. Available: {list(self.templates.keys())}")
        return self.templates[name]
    
    def list_templates(self) -> List[str]:
        """列出所有可用模板"""
        return list(self.templates.keys())
    
    def create_prompt(self, template_name: str, context: str, params: Dict[str, Any] = None) -> str:
        """使用指定模板创建提示"""
        template = self.get_template(template_name)
        return template.construct_prompt(context, params)
    
    def parse_response(self, template_name: str, response: str) -> Dict[str, Any]:
        """使用指定模板解析响应"""
        template = self.get_template(template_name)
        return template.parse_response(response)


# 全局模板注册表实例
template_registry = TemplateRegistry()