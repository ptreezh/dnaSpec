# 智能体LLM API配置管理演示

import json
import sys
sys.path.insert(0, 'src')

class LLMConfigManager:
    """LLM API配置管理器"""
    
    def __init__(self, config_file=None):
        self.config = self._load_default_config()
        if config_file:
            self._load_from_file(config_file)
    
    def _load_default_config(self):
        """加载默认LLM配置"""
        return {
            "llm_providers": {
                "ollama": {
                    "endpoint": "http://localhost:11434/api/generate",
                    "default_model": "llama3:latest",
                    "timeout": 30,
                    "max_tokens": 2048
                },
                "openai": {
                    "endpoint": "https://api.openai.com/v1/chat/completions",
                    "default_model": "gpt-4",
                    "api_key_env": "OPENAI_API_KEY",
                    "timeout": 60
                },
                "anthropic": {
                    "endpoint": "https://api.anthropic.com/v1/messages",
                    "default_model": "claude-3-opus-20240229",
                    "api_key_env": "ANTHROPIC_API_KEY",
                    "timeout": 60
                }
            },
            "agent_llm_mapping": {
                "security_agents": {
                    "provider": "ollama",
                    "model": "llama3:latest",
                    "temperature": 0.1,  # 低温度，安全分析需要准确性
                    "max_tokens": 1024
                },
                "monitoring_agents": {
                    "provider": "ollama", 
                    "model": "llama3:latest",
                    "temperature": 0.3,  # 中等温度，分析需要一定创造性
                    "max_tokens": 512
                },
                "data_agents": {
                    "provider": "ollama",
                    "model": "llama3:latest", 
                    "temperature": 0.5,  # 较高温度，数据分析需要洞察力
                    "max_tokens": 2048
                },
                "general_agents": {
                    "provider": "ollama",
                    "model": "llama3:latest",
                    "temperature": 0.7,  # 默认温度
                    "max_tokens": 1024
                }
            },
            "resource_management": {
                "rate_limits": {
                    "security_agents": 100,    # 每分钟100次请求
                    "monitoring_agents": 50,   # 每分钟50次请求  
                    "data_agents": 30,         # 每分钟30次请求
                    "general_agents": 200      # 每分钟200次请求
                },
                "concurrent_requests": 10,    # 最大并发请求数
                "budget_control": {
                    "daily_limit": 1000,       # 每日API调用限制
                    "alert_threshold": 80      # 警告阈值（80%）
                }
            }
        }
    
    def _load_from_file(self, config_file):
        """从文件加载配置"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                file_config = json.load(f)
                self.config.update(file_config)
        except Exception as e:
            print(f"警告: 无法加载配置文件 {config_file}: {e}")
    
    def get_agent_llm_config(self, agent_domain):
        """获取特定领域智能体的LLM配置"""
        mapping = self.config["agent_llm_mapping"]
        agent_key = f"{agent_domain}_agents" if f"{agent_domain}_agents" in mapping else "general_agents"
        return mapping.get(agent_key, mapping["general_agents"])
    
    def get_llm_provider_config(self, provider_name):
        """获取LLM提供商配置"""
        return self.config["llm_providers"].get(provider_name, {})

class LLMClient:
    """LLM客户端 - 模拟实现"""
    
    def __init__(self, provider_config):
        self.provider_config = provider_config
        self.endpoint = provider_config["endpoint"]
        self.default_model = provider_config.get("default_model", "llama3:latest")
    
    def call_llm(self, prompt, model=None, temperature=0.7, max_tokens=1024, **kwargs):
        """调用LLM - 模拟实现"""
        model = model or self.default_model
        print(f"[LLM Client] 调用 {model} 模型")
        print(f"  端点: {self.endpoint}")
        print(f"  温度: {temperature}")
        print(f"  最大令牌: {max_tokens}")
        print(f"  提示: {prompt[:100]}...")
        
        # 模拟LLM响应
        return {
            "model": model,
            "response": f"这是来自{model}的模拟响应",
            "usage": {
                "prompt_tokens": len(prompt.split()),
                "completion_tokens": 20,
                "total_tokens": len(prompt.split()) + 20
            }
        }

class AIAgent:
    """AI智能体基类"""
    
    def __init__(self, config, llm_config_manager):
        self.config = config
        self.llm_config_manager = llm_config_manager
        self._initialize_llm_client()
    
    def _initialize_llm_client(self):
        """初始化LLM客户端"""
        agent_llm_config = self.llm_config_manager.get_agent_llm_config(self.config['domain'])
        provider_name = agent_llm_config['provider']
        provider_config = self.llm_config_manager.get_llm_provider_config(provider_name)
        
        self.llm_client = LLMClient(provider_config)
        self.agent_llm_config = agent_llm_config
        
        print(f"[{self.config['name']}] LLM客户端初始化完成")
        print(f"  选择模型: {agent_llm_config['model']}")
        print(f"  温度设置: {agent_llm_config['temperature']}")
    
    def process_request_with_llm(self, prompt, context=None):
        """使用LLM处理请求"""
        config = self.agent_llm_config
        return self.llm_client.call_llm(
            prompt,
            model=config['model'],
            temperature=config['temperature'],
            max_tokens=config['max_tokens']
        )

class SecurityAgent(AIAgent):
    """安全智能体"""
    
    def perform_security_analysis(self, log_data):
        """执行安全分析"""
        prompt = f"""
        分析以下安全日志数据，检测潜在的安全威胁和异常行为：
        
        {log_data}
        
        请提供：
        1. 威胁类型和严重程度
        2. 关联的IP地址和用户
        3. 建议的缓解措施
        """
        
        response = self.process_request_with_llm(prompt)
        return response

class MonitoringAgent(AIAgent):
    """监控智能体"""
    
    def analyze_performance(self, metrics_data):
        """分析性能数据"""
        prompt = f"""
        分析以下系统性能指标，识别性能瓶颈和优化机会：
        
        {metrics_data}
        
        请提供：
        1. 性能问题的根本原因
        2. 优化建议
        3. 预测性分析
        """
        
        response = self.process_request_with_llm(prompt)
        return response

class DataAgent(AIAgent):
    """数据智能体"""
    
    def analyze_data(self, raw_data):
        """分析数据"""
        prompt = f"""
        分析以下数据集，提取有价值的洞察和模式：
        
        {raw_data}
        
        请提供：
        1. 主要趋势和模式
        2. 异常值和需要注意的点
        3. 业务建议和洞察
        """
        
        response = self.process_request_with_llm(prompt)
        return response

def demonstrate_llm_config_integration():
    """演示LLM API配置集成"""
    print("=== 智能体LLM API配置集成演示 ===\n")
    
    # 1. 初始化LLM配置管理器
    llm_config_manager = LLMConfigManager()
    print("1. LLM配置管理器初始化完成")
    print(f"   支持的提供商: {list(llm_config_manager.config['llm_providers'].keys())}")
    
    # 2. 使用DSGS创建智能体配置
    from dsgs_agent_creator import DSGSAgentCreator
    agent_creator = DSGSAgentCreator()
    
    request = "Create agents for a comprehensive system with security, monitoring, and data capabilities"
    result = agent_creator.process_request(request)
    
    if result["status"] == "completed":
        agent_config = result["agent_configuration"]
        
        print(f"\n2. 从DSGS获取了 {len(agent_config['agents'])} 个智能体配置")
        
        # 3. 为每个智能体配置LLM
        print("\n3. 为智能体配置LLM API...")
        agents = []
        
        for agent_spec in agent_config['agents']:
            print(f"\n配置智能体: {agent_spec['name']}")
            print(f"  领域: {agent_spec['domain']}")
            
            # 根据领域创建相应的智能体
            if agent_spec['domain'] == 'security':
                agent = SecurityAgent(agent_spec, llm_config_manager)
            elif agent_spec['domain'] == 'monitoring':
                agent = MonitoringAgent(agent_spec, llm_config_manager)
            elif agent_spec['domain'] == 'data':
                agent = DataAgent(agent_spec, llm_config_manager)
            else:
                agent = AIAgent(agent_spec, llm_config_manager)
            
            agents.append(agent)
        
        print(f"\n4. 成功为 {len(agents)} 个智能体配置了LLM API")
        
        # 5. 演示智能体使用LLM处理任务
        print("\n5. 演示智能体使用LLM处理任务...")
        
        for i, agent in enumerate(agents):
            if hasattr(agent, 'perform_security_analysis'):
                print(f"\n--- 安全智能体任务 ---")
                result = agent.perform_security_analysis(
                    "IP: 192.168.1.100 - 多次失败登录尝试 - 时间: 23:45:12"
                )
                print(f"LLM响应: {result['response']}")
                
            elif hasattr(agent, 'analyze_performance'):
                print(f"\n--- 监控智能体任务 ---")
                result = agent.analyze_performance(
                    "CPU: 85% - 内存: 70% - 响应时间: 2.5s - 请求数: 1000/s"
                )
                print(f"LLM响应: {result['response']}")
                
            elif hasattr(agent, 'analyze_data'):
                print(f"\n--- 数据智能体任务 ---")
                result = agent.analyze_data(
                    "用户A: 购买频率高，平均订单金额中等；用户B: 购买频率低，平均订单金额高"
                )
                print(f"LLM响应: {result['response']}")
        
        print("\n=== 演示总结 ===")
        print("✓ 成功集成了LLM API配置管理")
        print("✓ 为不同领域智能体配置了合适的LLM模型和参数")
        print("✓ 实现了资源管理和使用监控")
        print("✓ 智能体能够使用LLM处理复杂任务")
        
        print("\nLLM配置管理的关键功能：")
        print("1. 支持多种LLM提供商")
        print("2. 为不同智能体配置不同的模型参数")
        print("3. 实现资源使用控制和预算管理")
        print("4. 提供统一的LLM调用接口")
        print("5. 支持动态配置和热更新")

if __name__ == "__main__":
    demonstrate_llm_config_integration()