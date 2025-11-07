# 配置管理在Skills架构中的集成方案

import json
import os
from typing import Dict, Any

class SkillBasedConfigManager:
    """基于Skills的配置管理器"""
    
    def __init__(self, skills_base_path: str = "skills"):
        self.skills_base_path = skills_base_path
        self.config_cache = {}
        self._load_skill_configs()
    
    def _load_skill_configs(self):
        """从Skills目录加载配置"""
        print("=== 从Skills目录加载配置 ===")
        
        # 遍历所有Skills目录
        for skill_dir in os.listdir(self.skills_base_path):
            skill_path = os.path.join(self.skills_base_path, skill_dir)
            if os.path.isdir(skill_path):
                # 查找配置文件
                config_files = self._find_config_files(skill_path)
                if config_files:
                    print(f"加载 {skill_dir} 的配置文件:")
                    for config_file in config_files:
                        self._load_skill_config(skill_dir, config_file)
    
    def _find_config_files(self, skill_path: str) -> list:
        """查找Skill目录中的配置文件"""
        config_files = []
        for root, dirs, files in os.walk(skill_path):
            for file in files:
                if file.endswith(('.json', '.yaml', '.yml', '.toml')) and 'config' in file.lower():
                    config_files.append(os.path.join(root, file))
        return config_files
    
    def _load_skill_config(self, skill_name: str, config_file: str):
        """加载单个Skill的配置文件"""
        try:
            if config_file.endswith('.json'):
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                # 简化处理，实际应该支持YAML/TOML
                config = self._parse_config_file(config_file)
            
            if skill_name not in self.config_cache:
                self.config_cache[skill_name] = {}
            
            # 合并配置
            self.config_cache[skill_name].update(config)
            print(f"  ✓ {os.path.basename(config_file)}")
            
        except Exception as e:
            print(f"  ✗ 加载 {config_file} 失败: {e}")
    
    def _parse_config_file(self, config_file: str) -> Dict[str, Any]:
        """解析配置文件（简化实现）"""
        # 实际实现应该支持YAML、TOML等格式
        return {"loaded_from": config_file}
    
    def get_llm_config_for_skill(self, skill_name: str) -> Dict[str, Any]:
        """获取特定Skill的LLM配置"""
        # 从Skill配置中提取LLM相关配置
        skill_config = self.config_cache.get(skill_name, {})
        
        # 查找LLM配置部分
        llm_config = {}
        for key, value in skill_config.items():
            if 'llm' in key.lower() or 'ai' in key.lower():
                llm_config[key] = value
        
        return llm_config
    
    def get_resource_config_for_skill(self, skill_name: str) -> Dict[str, Any]:
        """获取特定Skill的资源配置"""
        skill_config = self.config_cache.get(skill_name, {})
        
        # 提取资源配置
        resource_config = {
            "cpu": skill_config.get("cpu_limit", "0.5"),
            "memory": skill_config.get("memory_limit", "512MB"),
            "api_quota": skill_config.get("api_quota_per_hour", 100)
        }
        
        return resource_config

class EnhancedAgentCreator:
    """增强版智能体创建器 - 集成配置管理"""
    
    def __init__(self, skills_base_path: str = "skills"):
        self.config_manager = SkillBasedConfigManager(skills_base_path)
        # 其他初始化代码...
    
    def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """处理请求 - 集成配置管理"""
        # 原有逻辑...
        agent_configuration = self._generate_agent_configuration(request, context or {})
        
        # 集成配置信息
        enhanced_config = self._enhance_with_config(agent_configuration)
        
        result = {
            "status": "completed",
            "skill": self.name,
            "request": request,
            "agent_configuration": enhanced_config,
            "timestamp": self._get_timestamp()
        }
        
        return result
    
    def _enhance_with_config(self, agent_config: Dict[str, Any]) -> Dict[str, Any]:
        """使用配置增强智能体配置"""
        # 为每个智能体添加配置信息
        for agent in agent_config.get('agents', []):
            agent_type = agent.get('type', 'general')
            skill_name = f"dsgs-{agent_type}-agent"  # 假设的Skill名称
            
            # 获取LLM配置
            llm_config = self.config_manager.get_llm_config_for_skill(skill_name)
            if llm_config:
                agent['llm_config'] = llm_config
            
            # 获取资源配置
            resource_config = self.config_manager.get_resource_config_for_skill(skill_name)
            if resource_config:
                agent['resource_config'] = resource_config
        
        return agent_config

def demonstrate_skill_based_config():
    """演示基于Skills的配置管理"""
    print("=== 基于Skills的配置管理演示 ===\n")
    
    # 1. 创建配置管理器
    config_manager = SkillBasedConfigManager()
    
    # 2. 显示加载的配置
    print("1. 加载的Skill配置:")
    for skill_name, config in config_manager.config_cache.items():
        print(f"   {skill_name}: {list(config.keys())}")
    
    # 3. 演示配置查询
    print("\n2. 配置查询演示:")
    test_skills = ['dsgs-agent-creator', 'dsgs-system-architect']
    for skill in test_skills:
        llm_config = config_manager.get_llm_config_for_skill(skill)
        resource_config = config_manager.get_resource_config_for_skill(skill)
        print(f"   {skill}:")
        print(f"     LLM配置: {llm_config}")
        print(f"     资源配置: {resource_config}")
    
    # 4. 演示增强版智能体创建器
    print("\n3. 增强版智能体创建器演示:")
    enhanced_creator = EnhancedAgentCreator()
    
    # 使用DSGS生成智能体配置
    import sys
    sys.path.insert(0, 'src')
    from dsgs_agent_creator import DSGSAgentCreator
    
    agent_creator = DSGSAgentCreator()
    request = "Create agents for a system with security and data processing capabilities"
    result = agent_creator.process_request(request)
    
    if result["status"] == "completed":
        # 增强配置
        enhanced_result = enhanced_creator._enhance_with_config(result["agent_configuration"])
        print(f"   增强后的智能体配置:")
        for agent in enhanced_result.get('agents', [])[:2]:  # 显示前2个
            print(f"     {agent['name']}:")
            print(f"       LLM配置: {agent.get('llm_config', '未配置')}")
            print(f"       资源配置: {agent.get('resource_config', '未配置')}")
    
    print("\n=== 演示总结 ===")
    print("✓ 实现了基于Skills的配置管理")
    print("✓ 配置文件与Skill定义紧密结合")
    print("✓ 智能体配置自动继承Skill配置")
    print("✓ 支持LLM和资源的统一管理")
    
    print("\n架构优势:")
    print("1. 配置与Skill定义一体化")
    print("2. 降低配置管理复杂度")
    print("3. 提高配置的一致性")
    print("4. 支持Skill级别的配置继承")

if __name__ == "__main__":
    demonstrate_skill_based_config()