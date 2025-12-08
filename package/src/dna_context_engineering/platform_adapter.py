"""
Platform Adapter Interface
AI CLI平台适配器接口，支持Claude CLI、Gemini CLI、Qwen CLI等平台
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import subprocess
import json
import os


class PlatformAdapter(ABC):
    """平台适配器抽象基类"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def is_available(self) -> bool:
        """检查平台是否可用"""
        pass
    
    @abstractmethod
    def send_command(self, command: str) -> str:
        """发送命令到平台"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """获取平台能力信息"""
        pass


class ClaudeCLIAdapter(PlatformAdapter):
    """Claude CLI 适配器"""
    
    def __init__(self):
        super().__init__(
            name="claude-cli",
            description="Anthropic Claude CLI 平台适配器"
        )
        self.claude_available = False
        self._check_availability()
    
    def is_available(self) -> bool:
        """检查Claude CLI是否可用"""
        return self.claude_available
    
    def _check_availability(self):
        """检查Claude CLI是否已安装"""
        try:
            result = subprocess.run(['claude', '--help'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            self.claude_available = (result.returncode == 0)
        except (subprocess.SubprocessError, FileNotFoundError):
            self.claude_available = False
    
    def send_command(self, command: str) -> str:
        """发送命令到Claude CLI"""
        if not self.is_available():
            raise RuntimeError("Claude CLI is not available")
        
        try:
            # 使用subprocess运行claude命令
            result = subprocess.run(
                ['claude', 'messages', 'stream', '-m', 'claude-3-haiku-20240307'],
                input=command,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return result.stdout
            else:
                raise RuntimeError(f"Claude CLI Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("Claude CLI command timed out")
        except Exception as e:
            raise RuntimeError(f"Claude CLI execution failed: {str(e)}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取Claude CLI能力"""
        return {
            "name": "Claude CLI",
            "models": ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"],
            "max_context": 200000,
            "multimodal": True,
            "available": self.is_available()
        }


class GeminiCLIAdapter(PlatformAdapter):
    """Gemini CLI 适配器"""
    
    def __init__(self):
        super().__init__(
            name="gemini-cli", 
            description="Google Gemini CLI 平台适配器"
        )
        self.gemini_available = False
        self._check_availability()
    
    def is_available(self) -> bool:
        """检查Gemini CLI是否可用"""
        return self.gemini_available
    
    def _check_availability(self):
        """检查Gemini CLI是否已安装"""
        try:
            result = subprocess.run(['gcloud', 'ai', 'models', 'list'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            self.gemini_available = (result.returncode == 0)
        except (subprocess.SubprocessError, FileNotFoundError):
            # 尝试另一种检查方式
            try:
                result = subprocess.run(['curl', '--help'], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=5)
                # 如果curl可用，我们可以使用REST API
                self.gemini_available = True
            except:
                self.gemini_available = False
    
    def send_command(self, command: str) -> str:
        """发送命令到Gemini CLI或API"""
        if not self.is_available():
            raise RuntimeError("Gemini CLI/API is not available")
        
        # 注意：实际的Gemini CLI可能不存在，这里使用API方式
        # 在实际实现中，需要根据真实的Gemini CLI命令结构来实现
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable not set")
        
        import requests
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": command
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise RuntimeError(f"Gemini API Error: {response.status_code} - {response.text}")
        except Exception as e:
            raise RuntimeError(f"Gemini API execution failed: {str(e)}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取Gemini CLI/API能力"""
        return {
            "name": "Gemini API",
            "models": ["gemini-pro", "gemini-1.5-pro"],
            "max_context": 32760,
            "multimodal": True,
            "available": self.is_available()
        }


class QwenCLIAdapter(PlatformAdapter):
    """Qwen CLI 适配器"""
    
    def __init__(self):
        super().__init__(
            name="qwen-cli",
            description="Alibaba Tongyi千问 CLI 平台适配器" 
        )
        self.qwen_available = False
        self._check_availability()
    
    def is_available(self) -> bool:
        """检查Qwen CLI是否可用"""
        return self.qwen_available
    
    def _check_availability(self):
        """检查Qwen CLI/SDK是否可用"""
        try:
            # 尝试导入Qwen SDK或检查CLI
            import subprocess
            result = subprocess.run(['python', '-c', 'import dashscope'], 
                                  capture_output=True, 
                                  text=True,
                                  timeout=5)
            self.qwen_available = (result.returncode == 0)
        except:
            self.qwen_available = False
    
    def send_command(self, command: str) -> str:
        """发送命令到Qwen"""
        if not self.is_available():
            raise RuntimeError("Qwen SDK is not available")
        
        # 使用Qwen SDK
        try:
            import dashscope
            from dashscope import Generation
            
            # 设置API密钥（需要用户配置）
            dashscope.api_key = os.getenv('DASHSCOPE_API_KEY')
            if not dashscope.api_key:
                raise RuntimeError("DASHSCOPE_API_KEY environment variable not set")
            
            response = Generation.call(
                model="qwen-max",
                prompt=command,
                max_tokens=1000,
                temperature=0.1
            )
            
            if response.status_code == 200:
                return response.output.text
            else:
                raise RuntimeError(f"Qwen API Error: {response.code} - {response.message}")
                
        except Exception as e:
            raise RuntimeError(f"Qwen execution failed: {str(e)}")
    
    def get_capabilities(self) -> Dict[str, Any]:
        """获取Qwen能力"""
        return {
            "name": "Qwen SDK",
            "models": ["qwen-max", "qwen-plus", "qwen-turbo"],
            "max_context": 32768,
            "multimodal": True,
            "available": self.is_available()
        }


class GenericAPIAdapter(PlatformAdapter):
    """通用API适配器（用于测试和模拟）"""
    
    def __init__(self):
        super().__init__(
            name="generic-api",
            description="通用API适配器（用于测试和模拟）"
        )
        self.available = True  # 总是可用用于测试
    
    def is_available(self) -> bool:
        return self.available
    
    def send_command(self, command: str) -> str:
        """模拟发送命令"""
        # 这是模拟实现，在实际使用时会被真实的AI API调用替换
        import time
        time.sleep(0.1)  # 模拟API延迟
        
        # 根据命令类型返回适当的模拟响应
        if "analyze" in command.lower() or "context" in command.lower():
            return f"[MOCK RESPONSE] Analysis result for: {command[:30]}..."
        elif "optimize" in command.lower():
            return f"[MOCK RESPONSE] Optimized context: {command[:30]}..."
        elif "template" in command.lower() or "reason" in command.lower():
            return f"[MOCK RESPONSE] Applied cognitive template to: {command[:30]}..."
        else:
            return f"[MOCk RESPONSE] Processed command: {command[:50]}..."
    
    def get_capabilities(self) -> Dict[str, Any]:
        return {
            "name": "Generic Mock API",
            "models": ["mock-model"],
            "max_context": 10000,
            "multimodal": False,
            "available": self.is_available(),
            "mock": True
        }


class PlatformAdapterManager:
    """平台适配器管理器"""
    
    def __init__(self):
        self.adapters = {
            'claude': ClaudeCLIAdapter(),
            'gemini': GeminiCLIAdapter(), 
            'qwen': QwenCLIAdapter(),
            'generic': GenericAPIAdapter()
        }
    
    def get_adapter(self, platform_name: str) -> Optional[PlatformAdapter]:
        """获取指定平台的适配器"""
        return self.adapters.get(platform_name)
    
    def get_available_adapters(self) -> Dict[str, PlatformAdapter]:
        """获取所有可用的平台适配器"""
        available = {}
        for name, adapter in self.adapters.items():
            if adapter.is_available():
                available[name] = adapter
        return available
    
    def auto_detect_platform(self) -> Optional[str]:
        """自动检测可用的AI平台"""
        for name, adapter in self.adapters.items():
            if name != 'generic' and adapter.is_available():  # 不包括通用适配器
                return name
        return None
    
    def list_adapters(self) -> Dict[str, str]:
        """列出所有适配器及其状态"""
        return {
            name: f"Available: {adapter.is_available()}" 
            for name, adapter in self.adapters.items()
        }


# 全局平台适配器管理器实例
platform_adapter_manager = PlatformAdapterManager()