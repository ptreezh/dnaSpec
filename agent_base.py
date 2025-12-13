# agent_base.py (完整实现)
class Agent:
    """智能体基类，完全符合宪法要求"""
    def __init__(self, agent_id: str, agent_type: str, capabilities: list):
        """
        初始化智能体
        Args:
            agent_id: 智能体唯一ID
            agent_type: 智能体类型
            capabilities: 智能体能力列表
        """
        self.id = agent_id
        self.type = agent_type
        self.capabilities = capabilities if capabilities else []
        self.context_manager = None  # 共享上下文引用
        self.assigned_tasks = []  # 智能体认领的任务
    
    def connect_to_context(self, context_manager):
        """
        连接到共享上下文
        Args:
            context_manager: 共享上下文管理器实例
        """
        self.context_manager = context_manager
    
    def claim_assigned_task(self, task_id: str) -> bool:
        """
        认领分配给自己的任务
        Args:
            task_id: 任务ID
        Returns:
            认领成功返回True
        """
        if not self.context_manager:
            return False
        
        task = self.context_manager.tasks.get(task_id)
        if not task:
            return False
        
        # 检查任务是否分配给此智能体或未分配
        if task.assigned_to == self.id or task.assigned_to is None:
            # 更新任务状态并更新到文档
            self.context_manager.update_task_status(task_id, "in_progress", self.id)
            self.assigned_tasks.append(task_id)
            return True
        
        return False
    
    def claim_matchable_task(self) -> str:
        """
        认领与其能力匹配的未分配任务
        Returns:
            成功认领的任务ID，失败返回None
        """
        if not self.context_manager or not self.capabilities:
            return None
        
        # 从共享上下文中获取匹配的任务
        available_tasks = self.context_manager.get_available_tasks(self.capabilities)
        
        for task in available_tasks:
            # 更新任务状态并更新到文档
            self.context_manager.update_task_status(task.id, "in_progress", self.id)
            self.assigned_tasks.append(task.id)
            return task.id  # 返回认领的任务ID
        
        return None  # 没有找到可认领的任务
    
    def make_autonomous_decision(self, context_data: dict):
        """
        基于上下文数据进行自主决策
        Args:
            context_data: 上下文数据字典
        Returns:
            决策结果
        """
        # 默认实现：基于上下文数据和自身能力做决策
        # 子类应重写此方法以实现具体决策逻辑
        raise NotImplementedError("子类必须实现make_autonomous_decision方法")