

def execute(args: dict) -> str:
    """
    根据输入的需求描述，生成一个简单的文本架构图。
    """
    description = args.get("description", "").lower()

    # 使用字典映射关键字和架构，更易于扩展
    architecture_map = {
        "电商": "[WebApp] -> [API Server] -> [Database]",
        "博客": "[WebApp] -> [Database]",
    }

    for keyword, architecture in architecture_map.items():
        if keyword in description:
            return architecture

    return ""
