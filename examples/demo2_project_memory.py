"""
示例2: 项目记忆系统
场景: 为项目添加持久化记忆能力
"""
import sys
from pathlib import Path

# 添加src到路径
script_dir = Path(__file__).parent
src_dir = script_dir.parent / 'src'
project_root = script_dir.parent

if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from dna_context_engineering.memory import MemoryManager, MemoryConfig, MemoryImportance


class CustomerSupportBot:
    """智能客服机器人 - 具有记忆能力"""

    def __init__(self, bot_name: str):
        self.bot_name = bot_name

        # 创建记忆系统
        config = MemoryConfig(
            enabled=True,
            max_short_term=100,
            max_long_term=500,
            auto_cleanup=True
        )
        self.memory = MemoryManager(config)

    def handle_customer_call(self, customer_phone: str, issue: str):
        """处理客户来电"""
        # 使用纯数字和字母作为ID，避免文件系统问题
        customer_id = f"customer_{customer_phone.replace('*', '').replace('-', '')}"

        print(f"\n📞 来电: {customer_phone}")
        print(f"   问题: {issue}")

        # 回忆这个客户的历史
        history = self.memory.recall_memories(customer_id, "投诉")
        if history:
            print(f"\n  💭 客户历史 ({len(history)} 条):")
            for h in history[:3]:
                print(f"     - {h.content}")
        else:
            print("\n  💭 新客户")

        # 记住这次问题
        self.memory.add_memory(
            agent_id=customer_id,
            content=f"客户来电: {issue}",
            importance=MemoryImportance.HIGH
        )

        return self._generate_response(customer_id, issue)

    def resolve_issue(self, customer_phone: str, solution: str):
        """记录问题解决方案"""
        customer_id = f"customer_{customer_phone.replace('*', '').replace('-', '')}"

        # 记住解决方案
        self.memory.add_memory(
            agent_id=customer_id,
            content=f"解决方案: {solution}",
            importance=MemoryImportance.HIGH
        )

        print(f"\n✅ 已记录解决方案: {solution}")

    def record_customer_preference(self, customer_phone: str, preference: str):
        """记录客户偏好"""
        customer_id = f"customer_{customer_phone.replace('*', '').replace('-', '')}"

        self.memory.add_memory(
            agent_id=customer_id,
            content=f"客户偏好: {preference}",
            importance=MemoryImportance.MEDIUM
        )

        print(f"  📝 已记录偏好: {preference}")

    def get_customer_summary(self, customer_phone: str):
        """获取客户摘要"""
        customer_id = f"customer_{customer_phone.replace('*', '').replace('-', '')}"

        # 获取所有记忆
        all_memories = self.memory.recall_memories(customer_id, "", limit=20)

        # 获取统计
        stats = self.memory.get_stats(customer_id)

        print(f"\n📊 客户摘要: {customer_phone}")
        print(f"   总互动: {stats['total_memories'] if stats else 0} 次")
        print(f"   历史记录:")

        categories = {}
        for memory in all_memories:
            if "来电" in memory.content:
                categories.setdefault("问题", []).append(memory)
            elif "解决方案" in memory.content:
                categories.setdefault("解决方案", []).append(memory)
            elif "偏好" in memory.content:
                categories.setdefault("偏好", []).append(memory)

        for category, memories in categories.items():
            print(f"\n   {category} ({len(memories)}):")
            for m in memories[-3:]:  # 显示最近3条
                print(f"     - {m.content}")

    def _generate_response(self, customer_id: str, issue: str):
        """根据历史生成响应"""
        history = self.memory.recall_memories(customer_id, "解决方案")

        if history:
            recent_solution = history[0].content.replace("解决方案: ", "")
            return f"根据之前的经验，建议: {recent_solution}"
        else:
            return "让我帮您解决这个问题..."


def demo_project_memory():
    """演示项目记忆系统"""

    print("=" * 70)
    print("示例2: 项目记忆系统")
    print("=" * 70)
    print("\n场景: 智能客服系统 - 为每个客户建立记忆档案")
    print("效果: 跨时间保持客户关系，提供个性化服务")
    print("-" * 70)

    # 创建客服机器人
    bot = CustomerSupportBot("智能客服小帮手")

    # 第一天：客户第一次来电
    print("\n" + "=" * 70)
    print("【第1天】客户 138****1234 首次来电")
    print("=" * 70)

    response = bot.handle_customer_call(
        "138****1234",
        "我无法登录系统"
    )
    print(f"  🤖 {response}")

    bot.resolve_issue(
        "138****1234",
        "重置密码，发送到注册邮箱"
    )

    bot.record_customer_preference(
        "138****1234",
        "喜欢通过邮件沟通，不喜欢电话"
    )

    # 第七天：客户第二次来电
    print("\n" + "=" * 70)
    print("【第7天】同一客户再次来电")
    print("=" * 70)

    response = bot.handle_customer_call(
        "138****1234",
        "系统又登录不了了"
    )
    print(f"  🤖 {response}")

    print("\n  💡 客服记得:")
    print("     - 这是老客户（之前登录问题）")
    print("     - 客户偏好邮件沟通")
    print("     - 有历史解决方案可参考")

    bot.resolve_issue(
        "138****1234",
        "检查账号被锁定，发送重置链接到邮箱"
    )

    # 查看客户摘要
    print("\n" + "=" * 70)
    print("【客户档案】")
    print("=" * 70)

    bot.get_customer_summary("138****1234")

    print("\n" + "=" * 70)
    print("效果总结:")
    print("  ✅ 记住客户历史互动（跨会话）")
    print("  ✅ 记住客户偏好（个性化服务）")
    print("  ✅ 记住解决方案（提高效率）")
    print("  ✅ 提供一致的客户体验")
    print("=" * 70)


if __name__ == '__main__':
    demo_project_memory()
