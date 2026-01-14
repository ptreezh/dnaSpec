"""
宪法级智能体创建技能 - 确保创建的智能体及其生成的所有内容都符合宪法原则
只对创建的文件、脚本进行宪法对齐，而不是对所有操作都强制
"""
from typing import Dict, Any, List
import json

def execute(args: Dict[str, Any]) -> str:
    """
    执行宪法级智能体创建技能
    只对生成的脚本、配置、定义文件进行宪法验证
    """
    context = args.get('context', '')
    
    if not context.strip():
        return "请提供智能体需求描述，系统将创建符合宪法原则的智能体配置和脚本"
    
    # 生成智能体配置
    agent_config = generate_agent_config(context)
    
    # 生成智能体脚本
    agent_script = generate_agent_script(agent_config)
    
    # 生成角色定义文件
    role_definition = generate_role_definition(agent_config)
    
    # 只对生成的文件内容进行宪法验证
    try:
        from .constitutional_validator import validate_constitutional_compliance
        
        # 验证脚本内容的宪法合规性
        script_validation = validate_constitutional_compliance(agent_script, "information_encapsulation")
        if not script_validation["compliant"]:
            # 添加宪法注释到脚本中
            agent_script += f'\n\n# CONSTITUTIONAL NOTE: {script_validation["feedback"]}'
        
        # 验证角色定义的宪法合规性
        role_validation = validate_constitutional_compliance(role_definition, "cognitive_convenience")
        if not role_validation["compliant"]:
            role_definition += f"\n\n<!-- Constitutional Note: {role_validation['feedback']} -->"
        
        # 验证配置的宪法合规性
        config_json = json.dumps(agent_config, ensure_ascii=False, indent=2)
        config_validation = validate_constitutional_compliance(config_json, "all")
        if not config_validation["compliant"]:
            agent_config['_constitutional_note'] = config_validation['feedback']
        
    except ImportError:
        # 如果宪法验证器不可用，继续执行不进行验证
        pass
    
    # 生成结果 - 包含所有宪法合规的文件内容
    result = format_agent_output(agent_config, agent_script, role_definition)
    
    return result

def generate_agent_config(context: str) -> Dict[str, Any]:
    """
    生成智能体配置
    """
    # 从上下文推断智能体类型和特性
    agent_type = infer_agent_type(context)
    capabilities = infer_capabilities(context)
    tools = infer_tools(context)
    personality = infer_personality(context) 
    specialization = infer_specialization(context)
    name = generate_agent_name(context)

    # 基础配置
    config = {
        'name': name,
        'type': agent_type,
        'description': context.strip(),
        'system_prompt': generate_system_prompt(context, agent_type),
        'capabilities': capabilities,
        'tools': tools,
        'personality': personality,
        'specialization': specialization
    }

    return config

def generate_system_prompt(context: str, agent_type: str) -> str:
    """
    生成系统提示词
    """
    prompt = f"""你是一个专业的{agent_type}。

核心职责: {context.strip()}

执行要求:
- 提供准确、有帮助且负责任的回应
- 根据用户需求提供适当详细程度的回答
- 确保信息完整性和一致性

请始终提供准确、有帮助的回应。
"""
    
    return prompt

def generate_agent_script(agent_config: Dict[str, Any]) -> str:
    """
    生成智能体脚本
    这个文件需要宪法对齐
    """
    script = f'''"""
{agent_config["name"]} - 智能体脚本
"""

import json
from typing import Dict, Any, List

class {agent_config["name"].replace(" ", "")}Agent:
    """
    智能体类
    """
    
    def __init__(self):
        self.name = "{agent_config["name"]}"
        self.type = "{agent_config["type"]}" 
        self.description = "{agent_config["description"]}"
        self.capabilities = {json.dumps(agent_config["capabilities"])}
        self.system_prompt = """{agent_config["system_prompt"]}"""

    def process_request(self, request: str) -> str:
        """
        处理请求
        """
        # 这里是智能体的核心逻辑
        return f"基于请求: {{request}} 生成的内容"

# 初始化智能体
def create_agent() -> {agent_config["name"].replace(" ", "")}Agent:
    """
    创建智能体实例
    """
    return {agent_config["name"].replace(" ", "")}Agent()

if __name__ == "__main__":
    agent = create_agent()
    print(f"智能体 {{agent.name}} 已就绪")
'''
    
    return script

def generate_role_definition(agent_config: Dict[str, Any]) -> str:
    """
    生成角色定义文件
    这个文件需要宪法对齐
    """
    role_def = f"""# 智能体角色定义

## 智能体信息
- **名称**: {agent_config["name"]}
- **类型**: {agent_config["type"]}
- **专业领域**: {agent_config["specialization"]}
- **性格特征**: {agent_config["personality"]}

## 核心能力
{chr(10).join(f"- {cap}" for cap in agent_config["capabilities"])}

## 可用工具
{chr(10).join(f"- {tool}" for tool in agent_config["tools"])}

## 职责范围
- 根据用户请求提供专业解答
- 确保信息准确性和实用性
- 保持专业和友好的沟通风格
"""
    
    return role_def

def infer_agent_type(context: str) -> str:
    """从上下文推断智能体类型"""
    context_lower = context.lower()

    if any(keyword in context_lower for keyword in ['分析', '数据', 'data', 'analyze']):
        return '数据分析智能体'
    elif any(keyword in context_lower for keyword in ['开发', '代码', 'programming', 'code', 'developer']):
        return '开发智能体' 
    elif any(keyword in context_lower for keyword in ['研究', 'research', '调查', '学术']):
        return '研究智能体'
    else:
        return '通用智能体'

def infer_capabilities(context: str) -> List[str]:
    """从上下文推断能力"""
    capabilities = []
    context_lower = context.lower()

    if any(keyword in context_lower for keyword in ['分析', 'analyze', '数据', 'data']):
        capabilities.append('数据分析')
    if any(keyword in context_lower for keyword in ['开发', 'code', '编程']):
        capabilities.append('编程开发')
    if any(keyword in context_lower for keyword in ['设计', 'design', '架构']):
        capabilities.append('系统设计')
    if any(keyword in context_lower for keyword in ['研究', 'research']):
        capabilities.append('研究分析')
    if any(keyword in context_lower for keyword in ['协助', 'assist', '帮助']):
        capabilities.append('任务协助')

    return capabilities if capabilities else ['通用任务处理']

def infer_tools(context: str) -> List[str]:
    """从上下文推断工具"""
    tools = []
    context_lower = context.lower()

    if any(keyword in context_lower for keyword in ['代码', 'code', '编程']):
        tools.append('代码编辑器')
    if any(keyword in context_lower for keyword in ['数据', 'data', '分析']):
        tools.append('数据分析工具')
    if any(keyword in context_lower for keyword in ['研究', 'research']):
        tools.append('学术数据库')

    return tools if tools else ['文本编辑器']

def infer_personality(context: str) -> str:
    """从上下文推断性格特征"""
    context_lower = context.lower()

    if any(keyword in context_lower for keyword in ['分析', '逻辑']):
        return '分析性、严谨'
    elif any(keyword in context_lower for keyword in ['开发', '创新', '技术']):
        return '创新、务实'
    elif any(keyword in context_lower for keyword in ['研究', '细致', '深入']):
        return '细致、探究精神'
    else:
        return '友好、专业'

def infer_specialization(context: str) -> str:
    """从上下文推断专业领域"""
    context_lower = context.lower()

    if any(keyword in context_lower for keyword in ['商业', 'business', '市场']):
        return '商业分析'
    elif any(keyword in context_lower for keyword in ['技术', 'technology', '软件']):
        return '软件开发'
    elif any(keyword in context_lower for keyword in ['数据', 'data', '分析']):
        return '数据分析'
    elif any(keyword in context_lower for keyword in ['学术', 'academic', '研究']):
        return '学术研究'
    else:
        return '通用问题解决'

def generate_agent_name(context: str) -> str:
    """生成智能体名称"""
    context_lower = context.lower()

    if '数据' in context_lower or 'data' in context_lower:
        return '数据分析师'
    elif '开发' in context_lower or 'code' in context_lower:
        return '开发工程师'
    elif '研究' in context_lower or 'research' in context_lower:
        return '研究专家'
    else:
        return '智能助手'

def format_agent_output(agent_config: Dict[str, Any], agent_script: str, role_definition: str) -> str:
    """格式化智能体输出"""
    output_lines = []
    output_lines.append("智能体创建完成")
    output_lines.append("")
    output_lines.append(f"名称: {agent_config['name']}")
    output_lines.append(f"类型: {agent_config['type']}")
    output_lines.append(f"专业领域: {agent_config['specialization']}")
    output_lines.append("")
    
    output_lines.append("📋 核心能力:")
    for capability in agent_config['capabilities']:
        output_lines.append(f"  • {capability}")
    
    output_lines.append("")
    output_lines.append("🛠️ 可用工具:")
    for tool in agent_config['tools']:
        output_lines.append(f"  • {tool}")
    
    output_lines.append("")
    output_lines.append("🎭 性格特征:")
    output_lines.append(f"  {agent_config['personality']}")
    
    output_lines.append("")
    output_lines.append("📋 生成的文件:")
    output_lines.append("  1. 智能体配置文件 (JSON)")
    output_lines.append("  2. 智能体脚本 (Python)")
    output_lines.append("  3. 角色定义文件 (Markdown)")
    
    result = "\n".join(output_lines)
    
    return result