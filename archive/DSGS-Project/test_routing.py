# 测试路由功能
import sys
import os

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from dsgs_architect import DSGSArchitect

def test_routing():
    skill = DSGSArchitect()
    
    # 测试路由
    test_cases = [
        ("Design architecture for a web application", "dsgs-system-architect"),
        ("Decompose tasks for mobile app development", "dsgs-task-decomposer"),
        ("Create agents for microservices system", "dsgs-agent-creator"),
        ("Generate constraints for API design", "dsgs-constraint-generator"),
        ("Unknown request type", "dsgs-system-architect")  # 默认路由
    ]
    
    print("测试路由功能:")
    for request, expected in test_cases:
        result = skill._route_request(request)
        status = "✓" if result == expected else "✗"
        print(f"{status} '{request}' -> '{result}' (期望: '{expected}')")

if __name__ == "__main__":
    test_routing()