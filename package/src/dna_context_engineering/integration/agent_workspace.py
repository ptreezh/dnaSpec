"""
智能体工作区集成 - 集成workspace和agent-creator
"""
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field

# 添加src到路径
src_dir = Path(__file__).parent.parent.parent.parent / 'src'
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


@dataclass
class AgentWorkspaceConfig:
    """智能体工作区配置"""
    agent_name: str
    agent_role: str
    agent_capabilities: List[str]
    workspace_id: str
    isolated: bool = True  # 是否隔离
    memory_enabled: bool = False  # 是否启用记忆
    context_limit: int = 5000  # 上下文限制（tokens）


@dataclass
class AgentWorkspaceResult:
    """智能体工作区创建结果"""
    success: bool
    workspace_id: str
    workspace_path: Path
    agent_config: Dict
    created_at: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None


class AgentWorkspaceIntegrator:
    """智能体工作区集成器"""

    def __init__(self, dnaspec_root: Optional[Path] = None):
        if dnaspec_root is None:
            dnaspec_root = Path(__file__).parent.parent.parent.parent

        self.dnaspec_root = Path(dnaspec_root)
        self.workspaces_root = self.dnaspec_root / 'workspaces' / 'agents'
        self.workspaces_root.mkdir(parents=True, exist_ok=True)

    def create_agent_workspace(
        self,
        agent_name: str,
        agent_role: str,
        agent_capabilities: List[str],
        **kwargs
    ) -> AgentWorkspaceResult:
        """
        创建智能体隔离工作区

        流程:
        1. 使用workspace技能创建隔离工作区
        2. 使用agent-creator技能配置智能体
        3. 集成配置，智能体在工作区内运行

        Args:
            agent_name: 智能体名称
            agent_role: 智能体角色
            agent_capabilities: 智能体能力列表
            **kwargs: 其他配置

        Returns:
            AgentWorkspaceResult: 创建结果
        """
        print(f"\n{'='*60}")
        print(f"创建智能体工作区: {agent_name}")
        print(f"{'='*60}")

        try:
            # 步骤1: 生成工作区ID
            workspace_id = self._generate_workspace_id(agent_name)
            workspace_path = self.workspaces_root / workspace_id

            # 步骤2: 创建工作区结构
            print("\n[1/3] 创建工作区结构...")
            self._create_workspace_structure(workspace_path, agent_name)

            # 步骤3: 生成智能体配置
            print("[2/3] 生成智能体配置...")
            agent_config = self._generate_agent_config(
                agent_name, agent_role, agent_capabilities, workspace_path
            )

            # 步骤4: 创建局部上下文
            print("[3/3] 创建局部上下文...")
            self._create_local_context(workspace_path, agent_config)

            # 步骤5: 保存配置
            self._save_workspace_config(workspace_path, agent_config)

            print(f"\n✅ 智能体工作区创建成功！")
            print(f"   工作区ID: {workspace_id}")
            print(f"   工作区路径: {workspace_path}")
            print(f"   智能体角色: {agent_role}")

            return AgentWorkspaceResult(
                success=True,
                workspace_id=workspace_id,
                workspace_path=workspace_path,
                agent_config=agent_config
            )

        except Exception as e:
            print(f"\n❌ 创建失败: {e}")
            return AgentWorkspaceResult(
                success=False,
                workspace_id="",
                workspace_path=Path(),
                agent_config={},
                error=str(e)
            )

    def _generate_workspace_id(self, agent_name: str) -> str:
        """生成工作区ID"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        # 简化名称
        simple_name = agent_name.lower().replace(' ', '-').replace('_', '-')
        return f"{simple_name}-{timestamp}"

    def _create_workspace_structure(self, workspace_path: Path, agent_name: str):
        """创建工作区目录结构"""
        # 创建标准目录
        (workspace_path / 'context').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'input').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'output').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'workspace').mkdir(parents=True, exist_ok=True)
        (workspace_path / 'logs').mkdir(parents=True, exist_ok=True)

        print(f"  创建目录: {workspace_path}")

    def _generate_agent_config(
        self,
        agent_name: str,
        agent_role: str,
        capabilities: List[str],
        workspace_path: Path
    ) -> Dict:
        """生成智能体配置"""
        config = {
            'agent_name': agent_name,
            'agent_role': agent_role,
            'capabilities': capabilities,
            'workspace_id': workspace_path.name,
            'created_at': datetime.now().isoformat(),
            'isolation': {
                'enabled': True,
                'type': 'workspace',
                'context_limit': 5000
            },
            'memory': {
                'enabled': False,
                'short_term_size': 10,
                'long_term_storage': str(workspace_path / 'memory')
            },
            'context_file': str(workspace_path / 'context' / 'context.md'),
            'input_dir': str(workspace_path / 'input'),
            'output_dir': str(workspace_path / 'output'),
            'workspace_dir': str(workspace_path / 'workspace'),
            'logs_dir': str(workspace_path / 'logs')
        }

        return config

    def _create_local_context(self, workspace_path: Path, agent_config: Dict):
        """创建局部上下文文件"""
        context_file = workspace_path / 'context' / 'context.md'

        content = f"""# {agent_config['agent_name']} - 局部上下文

## 智能体信息
- **名称**: {agent_config['agent_name']}
- **角色**: {agent_config['agent_role']}
- **创建时间**: {agent_config['created_at']}

## 能力
{chr(10).join(f"- {cap}" for cap in agent_config['capabilities'])}

## 隔离配置
- **工作区**: {agent_config['workspace_id']}
- **隔离类型**: {agent_config['isolation']['type']}
- **上下文限制**: {agent_config['isolation']['context_limit']} tokens

## 工作目录
- **输入**: `{agent_config['input_dir']}`
- **输出**: `{agent_config['output_dir']}`
- **工作空间**: `{agent_config['workspace_dir']}`
- **日志**: `{agent_config['logs_dir']}`

## 执行历史

---
*此上下文仅用于 {agent_config['agent_name']} 智能体，与其他智能体隔离*
"""

        with open(context_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"  创建上下文: {context_file}")

    def _save_workspace_config(self, workspace_path: Path, config: Dict):
        """保存工作区配置"""
        config_file = workspace_path / 'agent_config.json'

        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        print(f"  保存配置: {config_file}")

    def list_agent_workspaces(self) -> List[Dict]:
        """列出所有智能体工作区"""
        workspaces = []

        if not self.workspaces_root.exists():
            return workspaces

        for workspace_dir in sorted(self.workspaces_root.iterdir()):
            if not workspace_dir.is_dir():
                continue

            config_file = workspace_dir / 'agent_config.json'
            if config_file.exists():
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    workspaces.append({
                        'workspace_id': workspace_dir.name,
                        'agent_name': config.get('agent_name'),
                        'agent_role': config.get('agent_role'),
                        'created_at': config.get('created_at'),
                        'path': str(workspace_dir)
                    })

        return workspaces

    def get_workspace_info(self, workspace_id: str) -> Optional[Dict]:
        """获取工作区信息"""
        workspace_path = self.workspaces_root / workspace_id
        config_file = workspace_path / 'agent_config.json'

        if not config_file.exists():
            return None

        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        return config


def demo_agent_workspace():
    """演示智能体工作区"""
    print("="*60)
    print("智能体工作区集成演示")
    print("="*60)

    integrator = AgentWorkspaceIntegrator()

    # 创建代码审查智能体工作区
    result = integrator.create_agent_workspace(
        agent_name="Code Review Agent",
        agent_role="代码质量审查专家",
        agent_capabilities=[
            "代码质量分析",
            "最佳实践检查",
            "安全性审查",
            "性能评估"
        ]
    )

    if result.success:
        print(f"\n✅ 工作区创建成功!")
        print(f"   智能体: {result.agent_config['agent_name']}")
        print(f"   能力数: {len(result.agent_config['capabilities'])}")
    else:
        print(f"\n❌ 创建失败: {result.error}")

    # 列出所有工作区
    print(f"\n{'='*60}")
    print("所有智能体工作区")
    print(f"{'='*60}")

    workspaces = integrator.list_agent_workspaces()
    for ws in workspaces:
        print(f"\n工作区: {ws['workspace_id']}")
        print(f"  智能体: {ws['agent_name']}")
        print(f"  角色: {ws['agent_role']}")
        print(f"  路径: {ws['path']}")

    return result


if __name__ == '__main__':
    demo_agent_workspace()
