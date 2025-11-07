"""
AI Model Client Abstraction Layer
为不同的AI服务提供统一的API访问接口
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import requests
import time
import json


class AIModelClient(ABC):
    """AI模型客户端抽象基类"""
    
    def __init__(self, api_key: str, base_url: str = None, rate_limit_delay: float = 1.0):
        self.api_key = api_key
        self.base_url = base_url
        self.rate_limit_delay = rate_limit_delay
        self.last_request_time = 0
        
    def _ensure_rate_limit(self):
        """确保API调用速率限制"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit_delay:
            time.sleep(self.rate_limit_delay - elapsed)
        self.last_request_time = time.time()
    
    @abstractmethod
    def send_instruction(self, instruction: str) -> str:
        """发送指令到AI模型并获取响应"""
        pass
    
    @abstractmethod
    def get_remaining_quota(self) -> int:
        """获取剩余API配额"""
        pass


class AnthropicClient(AIModelClient):
    """Anthropic Claude API 客户端"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key, 
            base_url="https://api.anthropic.com/v1/messages",
            rate_limit_delay=1.0  # Anthropic免费账户限制
        )
    
    def send_instruction(self, instruction: str) -> str:
        """发送指令到Anthropic Claude"""
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": "claude-3-haiku-20240307",  # 使用免费模型
            "messages": [{"role": "user", "content": instruction}],
            "max_tokens": 1000
        }
        
        try:
            self._ensure_rate_limit()
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['content'][0]['text']
            else:
                raise Exception(f"Anthropic API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Anthropic API Request Failed: {str(e)}")
    
    def get_remaining_quota(self) -> int:
        """Anthropic没有公开的配额查询API，返回估算值"""
        # 实际实现中，这需要通过Anthropic的账单API或控制台获取
        return 1000000  # placeholder


class GoogleAIClient(AIModelClient):
    """Google Generative AI (Gemini) API 客户端"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url=f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}",
            rate_limit_delay=1.0
        )
    
    def send_instruction(self, instruction: str) -> str:
        """发送指令到Google Gemini"""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": instruction
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 1000
            }
        }
        
        try:
            self._ensure_rate_limit()
            response = requests.post(
                url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['candidates'][0]['content']['parts'][0]['text']
            else:
                raise Exception(f"Google API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Google API Request Failed: {str(e)}")
    
    def get_remaining_quota(self) -> int:
        """Google API配额查询（需要额外实现）"""
        # Google的配额信息通常通过其Billing API获取
        return 1000000  # placeholder


class OpenAIClient(AIModelClient):
    """OpenAI API 客户端"""
    
    def __init__(self, api_key: str):
        super().__init__(
            api_key=api_key,
            base_url="https://api.openai.com/v1/chat/completions",
            rate_limit_delay=1.0
        )
    
    def send_instruction(self, instruction: str) -> str:
        """发送指令到OpenAI GPT"""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": instruction}],
            "max_tokens": 1000,
            "temperature": 0.1
        }
        
        try:
            self._ensure_rate_limit()
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                raise Exception(f"OpenAI API Error: {response.status_code} - {response.text}")
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"OpenAI API Request Failed: {str(e)}")
    
    def get_remaining_quota(self) -> int:
        """OpenAI没有直接的配额查询API，返回估算值"""
        return 1000000  # placeholder


class GenericAPIClient(AIModelClient):
    """通用API客户端（用于测试和模拟）"""
    
    def __init__(self, api_key: str = "", base_url: str = "http://localhost:8080/api/generate"):
        super().__init__(api_key=api_key, base_url=base_url, rate_limit_delay=0.1)
        self.call_count = 0
    
    def send_instruction(self, instruction: str) -> str:
        """本地模拟AI响应（在真实环境中替换为实际API）"""
        # 这里是模拟实现，用于开发测试
        # 在实际部署时需要替换为真实的API调用
        self.call_count += 1
        
        # 模拟真实AI的响应延迟
        time.sleep(0.1)
        
        # 返回基于指令的响应
        if "analyze" in instruction.lower() or "context" in instruction.lower():
            return f"Analysis result for: {instruction[:50]}... [SIMULATED RESPONSE - REPLACE WITH REAL AI]"
        elif "optimize" in instruction.lower():
            return f"Optimized context: {instruction[:50]}... [SIMULATED RESPONSE - REPLACE WITH REAL AI]"  
        elif "template" in instruction.lower():
            return f"Cognitive template applied: {instruction[:50]}... [SIMULATED RESPONSE - REPLACE WITH REAL AI]"
        else:
            return f"Processed: {instruction} [SIMULATED RESPONSE - REPLACE WITH REAL AI]"
    
    def get_remaining_quota(self) -> int:
        return 1000000


# 便捷的工厂函数用于创建客户端
def create_ai_client(provider: str, api_key: str) -> AIModelClient:
    """
    创建AI模型客户端的工厂函数
    
    Args:
        provider: AI服务提供商 ("anthropic", "google", "openai", "generic")
        api_key: API密钥
        
    Returns:
        配置好的AI模型客户端实例
    """
    providers = {
        "anthropic": AnthropicClient,
        "google": GoogleAIClient, 
        "openai": OpenAIClient,
        "generic": GenericAPIClient
    }
    
    if provider not in providers:
        raise ValueError(f"Unsupported provider: {provider}. Supported: {list(providers.keys())}")
    
    return providers[provider](api_key)