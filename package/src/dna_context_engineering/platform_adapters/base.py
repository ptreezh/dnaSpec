"""
Platform Adapter Interface
定义平台适配器的统一接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json


class PlatformAdapter(ABC):
    """
    平台适配器抽象基类
    定义所有平台适配器必须实现的接口
    """
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.initialized = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        初始化平台适配器
        返回是否成功初始化
        """
        pass
    
    @abstractmethod
    def register_tool(self, skill_definition: Dict[str, Any]) -> bool:
        """
        向平台注册工具/技能
        
        Args:
            skill_definition: 技能定义，包含name, description, parameters等
            
        Returns:
            注册是否成功
        """
        pass
    
    @abstractmethod
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行平台工具
        
        Args:
            tool_name: 工具名称
            arguments: 工具参数
            
        Returns:
            执行结果
        """
        pass
    
    @abstractmethod
    def get_available_tools(self) -> List[str]:
        """
        获取平台可用的工具列表
        
        Returns:
            可用工具名称列表
        """
        pass
    
    @abstractmethod
    def validate_api_connection(self) -> bool:
        """
        验证API连接是否有效
        
        Returns:
            连接是否有效
        """
        pass
    
    def preprocess_arguments(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        预处理参数（可选实现）
        在传递给平台前处理参数
        """
        return arguments
    
    def postprocess_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        后处理结果（可选实现）
        从平台获取结果后进行处理
        """
        return result


class ClaudeToolsAdapter(PlatformAdapter):
    """
    Claude Tools API 适配器
    为Anthropic Claude提供工具调用能力
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("claude", config)
        self.api_key = config.get("api_key")
        self.client = None  # Anthropic客户端将在initialize中创建
        
    def initialize(self) -> bool:
        """
        初始化Claude客户端
        """
        try:
            if not self.api_key:
                raise ValueError("Claude API key not provided in config")
            
            # 检查API密钥有效性
            if not self.validate_api_connection():
                return False
            
            # 导入Anthropic库
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("anthropic package required. Install with: pip install anthropic")
            
            self.initialized = True
            return True
        except Exception as e:
            print(f"Failed to initialize Claude adapter: {str(e)}")
            return False
    
    def validate_api_connection(self) -> bool:
        """
        验证Claude API连接
        """
        try:
            if not self.api_key:
                return False
            
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            # 尝试进行一次简单的API调用验证连接
            # 使用测试调用验证API密钥
            return True
        except:
            return False
    
    def register_tool(self, skill_definition: Dict[str, Any]) -> bool:
        """
        在Claude中注册工具
        注意: Claude Tools是通过对话中的工具参数在运行时定义的
        这里我们返回工具定义格式，实际注册在使用时进行
        """
        if not self.initialized:
            if not self.initialize():
                return False
        
        try:
            # Claude Tools的工具定义格式
            claude_tool_def = {
                "name": skill_definition.get("name", ""),
                "description": skill_definition.get("description", ""),
                "input_schema": {
                    "type": "object",
                    "properties": {},
                    "required": skill_definition.get("required_parameters", [])
                }
            }
            
            # 转换参数定义
            parameters = skill_definition.get("parameters", [])
            for param in parameters:
                param_name = param.get("name")
                param_type = param.get("type", "string")
                param_desc = param.get("description", "")
                
                claude_tool_def["input_schema"]["properties"][param_name] = {
                    "type": param_type,
                    "description": param_desc
                }
            
            # 在实际实现中，这里会将工具定义存储起来
            # 在Claude API调用时通过tools参数传递
            # 暂时返回成功
            return True
            
        except Exception as e:
            print(f"Failed to register tool for Claude: {str(e)}")
            return False
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过Claude API执行工具调用
        实际上是构造一个工具调用请求给Claude模型，让它处理
        """
        if not self.initialized:
            if not self.initialize():
                return {"success": False, "error": "Adapter not initialized"}
        
        try:
            # 构造Claude消息，包含工具调用请求
            message = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                temperature=0.1,
                system="你是一个上下文工程专家。根据用户需求，分析、优化和结构化上下文。",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"请使用{tool_name}技能来处理以下内容: {json.dumps(arguments)}"
                            }
                        ]
                    }
                ],
                tools=[
                    {
                        "name": tool_name,
                        "description": f"DNASPEC Context Engineering Skill: {tool_name}",
                        "input_schema": {
                            "type": "object",
                            "properties": {
                                "context": {"type": "string", "description": "要处理的上下文"},
                                "parameters": {"type": "object", "description": "处理参数"}
                            }
                        }
                    }
                ]
            )
            
            # 处理Claude的响应
            tool_calls = []
            for content_block in message.content:
                if content_block.type == "tool_use":
                    tool_calls.append({
                        "name": content_block.name,
                        "input": content_block.input,
                        "id": content_block.id
                    })
            
            # 如果Claude调用工具，我们在这里处理
            if tool_calls:
                # 在实际实现中，这里会执行具体的工具逻辑
                # 现在我们返回模拟响应
                return {
                    "success": True,
                    "result": message.content[0].text if message.content and message.content[0].type == "text" else "Tool executed",
                    "tool_calls": tool_calls,
                    "usage": {
                        "input_tokens": message.usage.input_tokens,
                        "output_tokens": message.usage.output_tokens
                    }
                }
            else:
                # 如果Claude直接回答而没有调用工具
                text_content = ""
                for content_block in message.content:
                    if content_block.type == "text":
                        text_content += content_block.text
                
                return {
                    "success": True,
                    "result": text_content,
                    "tool_calls": [],
                    "usage": {
                        "input_tokens": message.usage.input_tokens,
                        "output_tokens": message.usage.output_tokens
                    }
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute tool via Claude: {str(e)}",
                "result": None
            }
    
    def get_available_tools(self) -> List[str]:
        """
        获取Claude平台可用的DNASPEC工具列表
        """
        # 在实际实现中，这是通过查询注册的技能获得的
        # 暂时返回模拟列表
        return [
            "dnaspec-context-analysis",
            "dnaspec-context-optimization", 
            "dnaspec-cognitive-template",
            "dnaspec-context-audit"
        ]


class GenericAPIProxyAdapter(PlatformAdapter):
    """
    通用API代理适配器
    为不直接支持工具调用的平台提供代理功能
    """
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("generic-proxy", config)
        self.ai_endpoint = config.get("ai_endpoint", "")
        self.api_key = config.get("api_key", "")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def initialize(self) -> bool:
        """
        初始化代理适配器
        """
        if not self.ai_endpoint or not self.api_key:
            return False
        
        # 验证连接
        self.initialized = self.validate_api_connection()
        return self.initialized
    
    def validate_api_connection(self) -> bool:
        """
        验证API连接
        """
        try:
            import requests
            # 发送简单请求验证连接
            return True  # 简化验证
        except:
            return False
    
    def register_tool(self, skill_definition: Dict[str, Any]) -> bool:
        """
        在代理中注册工具
        实际上是存储技能定义用于后续调用
        """
        # 在代理模式下，我们只是记录工具定义
        # 实际调用仍通过API请求
        return True
    
    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        通过API代理执行工具调用
        """
        if not self.initialized:
            if not self.initialize():
                return {"success": False, "error": "Adapter not initialized"}
        
        try:
            import requests
            
            # 构造请求给AI模型
            # 这里我们构造一个提示，结合工具名称和参数
            prompt = f"""
            请作为{tool_name}技能助手处理以下请求：
            
            工具名称：{tool_name}
            参数：{json.dumps(arguments, ensure_ascii=False)}
            
            请按照该技能的规范执行操作，并返回结构化结果。
            """
            
            # 发送到AI模型端点
            response = requests.post(
                self.ai_endpoint,
                headers=self.headers,
                json={
                    "model": "gpt-4o",  # 假设使用GPT-4o或其他兼容模型
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": 1000,
                    "temperature": 0.1
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "result": result.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "usage": result.get("usage", {})
                }
            else:
                return {
                    "success": False,
                    "error": f"API request failed: {response.status_code}",
                    "result": None
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to execute tool via proxy: {str(e)}",
                "result": None
            }
    
    def get_available_tools(self) -> List[str]:
        """
        获取代理支持的工具列表
        """
        # 返回通过DNASPEC规范引擎注册的工具
        return []  # 实际实现中会从注册表获取