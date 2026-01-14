"""
DNASPEC统一技能执行器
支持所有DNASPEC技能的执行
"""
from typing import Dict, Any, List, Optional
import sys
from pathlib import Path

# 导入所有独立技能执行函数
try:
    from .context_analysis_independent import execute_context_analysis
    from .simple_architect_independent import execute_simple_architect
    from .system_architect_independent import execute_system_architect
    from .agent_creator_independent import execute_agent_creator
    from .modulizer_independent import execute_modulizer
    from .constitutional_modulizer_independent import execute_constitutional_module_formation
    from .minimalist_architect import execute as execute_minimalist_architect
    from .reality_validator import execute as execute_reality_validator
    # 三大核心技能
    from .task_decomposer import execute_task_decomposer
    from .constraint_generator import execute_constraint_generator
    from .api_checker import execute_api_checker
except ImportError as e:
    print(f"Warning: Could not import some independent skills: {e}")

# 导入基础技能类
try:
    from dna_context_engineering.skills_system_final import (
        execute as execute_context_engineering
    )
except ImportError as e:
    try:
        # 尝试使用src前缀路径
        from src.dna_context_engineering.skills_system_final import (
            execute as execute_context_engineering
        )
    except ImportError:
        # 如果都失败了，设为None或提供默认值
        execute_context_engineering = None
        print(f"Warning: Could not import context engineering skills: {e}")

# 导入命令映射器
from .command_mapper import command_mapper


class DNASPECSkillExecutor:
    """DNASPEC统一技能执行器"""

    def __init__(self):
        self.skill_registry = {
            # 上下文工程技能（通过独立函数）
            'context-analysis': execute_context_analysis,

            # 系统设计技能
            'architect': execute_system_architect,
            'simple-architect': execute_simple_architect,

            # 专业技能
            'agent-creator': execute_agent_creator,
            'modulizer': execute_modulizer,
            'constitutional-module-formation': execute_constitutional_module_formation,

            # 新增技能 for addressing low-confidence challenges
            'minimalist-architect': execute_minimalist_architect,
            'reality-validator': execute_reality_validator,

            # 三大核心技能 for comprehensive integration hall system
            'task-decomposer': execute_task_decomposer,
            'constraint-generator': execute_constraint_generator,
            'api-checker': execute_api_checker,

            # 使用命令映射器（Git和Workspace）
            'git': lambda args: command_mapper.execute_command(f"git {args.get('command', 'status')}"),
            'workspace': lambda args: command_mapper.execute_command(f"workspace {args.get('command', 'status')}"),
        }

        # 从context engineering系统获取更多技能
        try:
            self.skill_registry.update({
                'context-optimization': lambda args: execute_context_engineering({
                    'skill': 'context-optimization',
                    'context': args.get('context', ''),
                    'params': args.get('params', {})
                }),
                'cognitive-template': lambda args: execute_context_engineering({
                    'skill': 'cognitive-template',
                    'context': args.get('context', ''),
                    'params': args.get('params', {})
                }),
            })
        except:
            pass

    def execute_skill(self, skill_name: str, context: str = "", **kwargs) -> Dict[str, Any]:
        """
        执行指定的DNASPEC技能

        Args:
            skill_name: 技能名称
            context: 上下文内容
            **kwargs: 其他参数

        Returns:
            执行结果
        """
        if skill_name not in self.skill_registry:
            return {
                'success': False,
                'error': f'Unknown skill: {skill_name}',
                'available_skills': list(self.skill_registry.keys())
            }

        try:
            skill_func = self.skill_registry[skill_name]

            # 准备参数
            args = {
                'context': context,
                **kwargs
            }

            # 执行技能
            if callable(skill_func):
                result = skill_func(args)

                # 确保返回格式一致
                if isinstance(result, dict):
                    return result
                else:
                    return {
                        'success': True,
                        'result': str(result)
                    }
            else:
                return {
                    'success': False,
                    'error': f'Skill {skill_name} is not callable'
                }

        except Exception as e:
            return {
                'success': False,
                'error': f'Error executing skill {skill_name}: {str(e)}'
            }

    def get_available_skills(self) -> Dict[str, str]:
        """获取可用技能列表"""
        descriptions = {
            'context-analysis': 'Analyze context quality across 5 dimensions',
            'context-optimization': 'Optimize context quality with AI-driven improvements',
            'cognitive-template': 'Apply cognitive frameworks to structure tasks',
            'architect': 'Design system architecture and components',
            'simple-architect': 'Simple architecture design for basic projects',
            'system-architect': 'Advanced system architecture with detailed design',
            'agent-creator': 'Create specialized AI agents with defined capabilities',
            'modulizer': 'Break down complex systems into modular components',
            'constitutional-module-formation': 'Constitutional skill for bottom-up module formation from mature components',
            'minimalist-architect': 'Evaluate architectural solutions for optimal complexity and minimalism',
            'reality-validator': 'Validate actual functionality of implementations against claimed functionality',
            'git': 'Execute Git workflow operations safely',
            'workspace': 'Manage AI-generated files in secure workspace',
            # 三大核心技能
            'task-decomposer': 'Based on design principles (KISS/YAGNI/SOLID) to decompose complex tasks into atomic tasks, create isolated workspaces to prevent context explosion',
            'constraint-generator': 'Generate dynamic constraints based on initial constitutional requirements, implement version management and time-point recovery to ensure alignment',
            'api-checker': 'Implement tiered review and multi-level call alignment verification, ensure interface consistency across module/subsystem/system levels'
        }

        skills = {}
        for skill_name in self.skill_registry.keys():
            skills[skill_name] = descriptions.get(skill_name, 'No description available')

        return skills

    def get_skill_help(self, skill_name: str) -> str:
        """获取特定技能的帮助信息"""
        help_texts = {
            'context-analysis': """
Context Analysis (/dnaspec.context-analysis):
Usage: /dnaspec.context-analysis "context to analyze"

Examples:
  /dnaspec.context-analysis "Design a user authentication system"
  /dnaspec.context-analysis "API design documentation" --mode enhanced
""",
            'context-optimization': """
Context Optimization (/dnaspec.context-optimization):
Usage: /dnaspec.context-optimization "context to optimize" --goals <goals>

Examples:
  /dnaspec.context-optimization "Write clean code" --goals clarity,completeness
  /dnaspec.context-optimization "System requirements" --goals relevance,consistency
""",
            'cognitive-template': """
Cognitive Template (/dnaspec.cognitive-template):
Usage: /dnaspec.cognitive-template "task description" --template <type>

Template Types:
  chain_of_thought - Step-by-step reasoning
  few_shot - Learning from examples
  verification - Double-checking results
  role_playing - Acting as a specific role

Examples:
  /dnaspec.cognitive-template "How to improve performance" --template chain_of_thought
  /dnaspec.cognitive-template "Review this design" --template verification
""",
            'architect': """
System Architect (/dnaspec.architect):
Usage: /dnaspec.architect "system requirements" [options]

Options:
  --style <type> - Architecture style (microservices, monolithic, etc.)
  --constraints <list> - Constraints (performance, security, etc.)

Examples:
  /dnaspec.architect "E-commerce platform" --style microservices
  /dnaspec.architect "Real-time system" --constraints high_performance
""",
            'git': """
Git Operations (/dnaspec.git):
Usage: /dnaspec.git <subcommand> [arguments]

Subcommands:
  status - Show repository status
  add <files> - Add files to staging
  commit <message> - Commit changes
  push - Push to remote
  pull - Pull from remote
  branch <name> - Create branch
  log --limit <n> - Show history

Examples:
  /dnaspec.git status
  /dnaspec.git commit "Fix authentication bug"
  /dnaspec.git branch feature/new-feature
""",
            'agent-creator': """
Agent Creator (/dnaspec.agent-creator):
Usage: /dnaspec.agent-creator "智能体需求描述"

Description:
  创建专业AI智能体，根据描述自动推断智能体类型、能力、工具和特性

Examples:
  /dnaspec.agent-creator "创建一个数据分析专家，负责销售数据的分析和报告"
  /dnaspec.agent-creator "React前端开发工程师，专注于组件开发和性能优化"
  /dnaspec.agent-creator "AI研究助理，协助机器学习项目的实施"
""",
            'modulizer': """
System Modulizer (/dnaspec.modulizer):
Usage: /dnaspec.modulizer "系统架构"

Description:
  将系统架构分解为可重用模块，自动识别组件、设计模块结构、定义接口和依赖关系

Examples:
  /dnaspec.modulizer "电商平台，包含用户管理、商品目录、订单处理和支付系统"
  /dnaspec.modulizer "微服务架构的银行系统"
  /dnaspec.modulizer "内容管理系统(CMS)，支持多用户和权限管理"
""",
            'workspace': """
Workspace Management (/dnaspec.workspace):
Usage: /dnaspec.workspace <subcommand> [arguments]

Subcommands:
  create - Create new workspace
  add <file> <content> - Add file to workspace
  list - List workspace files
  clean - Clean workspace
  stage <file> - Move file to staging area
  verify <file> - Verify staged file
  promote <file> - Promote verified file

Examples:
  /dnaspec.workspace create
  /dnaspec.workspace add "auth.py" "import hashlib..."
  /dnaspec.workspace stage "auth.py"
""",
            'constitutional-module-formation': """
Constitutional Module Formation (/dnaspec.constitutional-module-formation):
Usage: /dnaspec.constitutional-module-formation operation=register_component component_name="name" component_description="description" component_category="category"

Description:
  Constitutional skill for gradual bottom-up module formation from mature components.
  Implements the constitutional requirement of encapsulating mature components into modules as complexity grows.

Operations:
  - register_component: Register a new component for tracking
  - update_component_status: Update component maturity status
  - add_component_dependency: Establish dependency relationship
  - get_ready_modules: Retrieve formed modules
  - evaluate_module_formation: Trigger module formation evaluation
  - get_formulation_insights: Get process metrics

Examples:
  /dnaspec.constitutional-module-formation operation=register_component component_name="user_auth" component_category="security"
  /dnaspec.constitutional-module-formation operation=update_component_status component_id="123abc" status="MATURE" maturity_boost=0.3
  /dnaspec.constitutional-module-formation operation=evaluate_module_formation
""",
            'task-decomposer': """
Task Decomposer (/dnaspec.task-decomposer):
Usage: /dnaspec.task-decomposer "complex task requirements" --max-depth <depth>

Description:
  Decompose complex tasks into atomic tasks following design principles (KISS, YAGNI, SOLID).
  Creates isolated workspaces to prevent context explosion and ensures each task has clear boundaries and context isolation.
  Implements the principle of gradual complexity growth from simple to sophisticated implementations.

Options:
  --max-depth <int> - Maximum depth of decomposition (default: 3)
  --workspace-base <path> - Base path for task workspaces (default: ./task_workspaces)
  --principles <list> - Comma-separated list of principles to apply (default: kiss,yagni,solid)

Examples:
  /dnaspec.task-decomposer "Build e-commerce platform" --max-depth 2
  /dnaspec.task-decomposer "Implement user authentication" --principles kiss,solid
  /dnaspec.task-decomposer "Design complex API system" --workspace-base ./complex_task_spaces
""",
            'constraint-generator': """
Constraint Generator (/dnaspec.constraint-generator):
Usage: /dnaspec.constraint-generator "initial requirements" --change-request "change description"

Description:
  Generate dynamic constraints based on constitutional requirements, implement version management and time-point recovery mechanism.
  Locks initial requirements as system constitution, performs alignment check for new requirements,
  detects conflicts with constitution, and manages demand evolution through timeline snapshots.

Options:
  --change-request <description> - Describe requested changes for conflict analysis
  --lock-constitution - Lock current requirements as constitution
  --restore-version <version_id> - Restore to specific constitution version
  --create-snapshot <label> - Create system state snapshot

Examples:
  /dnaspec.constraint-generator "User authentication system requirements" --lock-constitution
  /dnaspec.constraint-generator "New feature requirements" --change-request "Add biometric authentication"
  /dnaspec.constraint-generator "System requirements" --create-snapshot "before_major_update"
""",
            'api-checker': """
API Checker (/dnaspec.api-checker):
Usage: /dnaspec.api-checker "api definitions" --level <module|subsystem|system>

Description:
  Implements tiered review and multi-level call alignment verification for module-level,
  subsystem-level, and system-level API consistency. Ensures interface alignment across
  different hierarchy levels and manages scope boundaries from global to local.

Options:
  --level <module|subsystem|system> - Specify validation level
  --mode <basic|detailed|comprehensive> - Validation detail level
  --scope-boundary <config> - Define scope boundary configuration

Examples:
  /dnaspec.api-checker "Check module API consistency" --level module --mode detailed
  /dnaspec.api-checker "Validate subsystem interfaces" --level subsystem --scope-boundary '{"module": "payment", "allowed_calls": ["user_service"], "forbidden_calls": ["admin_service"]}'
  /dnaspec.api-checker "Review system-wide API alignment" --level system --mode comprehensive
"""
        }

        return help_texts.get(skill_name, f"No help available for skill: {skill_name}")

# 创建全局技能执行器实例
skill_executor = DNASPECSkillExecutor()


def execute_skill(skill_name: str, args: Dict[str, Any]) -> str:
    """
    全局技能执行入口函数

    Args:
        skill_name: 技能名称
        args: 参数字典

    Returns:
        执行结果字符串
    """
    result = skill_executor.execute_skill(skill_name, **args)

    if result.get('success'):
        return str(result.get('result', 'Skill executed successfully'))
    else:
        return f"Error: {result.get('error', 'Unknown error')}"


# 向后兼容的执行函数
def execute_architect(args: Dict[str, Any]) -> str:
    """向后兼容的架构师执行函数"""
    return execute_skill('architect', args)

def execute_agent_creator(args: Dict[str, Any]) -> str:
    """向后兼容的智能体创建执行函数"""
    return execute_skill('agent-creator', args)

def execute_task_decomposer(args: Dict[str, Any]) -> str:
    """向后兼容的任务分解执行函数"""
    return execute_skill('task-decomposer', args)

def execute_constraint_generator(args: Dict[str, Any]) -> str:
    """向后兼容的约束生成执行函数"""
    return execute_skill('constraint-generator', args)

def execute_dapi_checker(args: Dict[str, Any]) -> str:
    """向后兼容的API检查执行函数"""
    return execute_skill('api-checker', args)

def execute_modulizer(args: Dict[str, Any]) -> str:
    """向后兼容的模块化执行函数"""
    return execute_skill('modulizer', args)

def execute_constitutional_module_formation(args: Dict[str, Any]) -> str:
    """向后兼容的宪法模块形成执行函数"""
    return execute_skill('constitutional-module-formation', args)