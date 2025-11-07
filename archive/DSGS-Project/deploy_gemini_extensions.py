#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini CLI Extensions 集成部署脚本
"""

import os
import json
import shutil
from pathlib import Path

def verify_gemini_extensions():
    """验证Gemini Extensions导出"""
    print("=== 验证Gemini CLI Extensions ===\n")
    
    export_path = "exports/gemini_extensions"
    if not os.path.exists(export_path):
        print("✗ Gemini Extensions导出目录不存在")
        return False
    
    # 检查extensions.json配置文件
    config_path = os.path.join(export_path, "extensions.json")
    if not os.path.exists(config_path):
        print("✗ extensions.json配置文件不存在")
        return False
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"发现 {len(config['extensions'])} 个Extensions:")
    for ext in config['extensions']:
        print(f"  ✓ {ext['name']}")
    
    # 检查每个Extension的GEMINI.md文件
    print("\n验证GEMINI.md文件:")
    for ext in config['extensions']:
        gemini_md_path = os.path.join(export_path, ext['name'], "GEMINI.md")
        if os.path.exists(gemini_md_path):
            print(f"  ✓ {ext['name']}/GEMINI.md 存在")
        else:
            print(f"  ✗ {ext['name']}/GEMINI.md 不存在")
            return False
    
    print("\n✓ 所有Gemini Extensions验证通过")
    return True

def deploy_to_gemini_cli(target_path=None):
    """部署到Gemini CLI"""
    print("\n=== 部署到Gemini CLI ===\n")
    
    # 默认Gemini Extensions路径
    if target_path is None:
        # Windows路径
        if os.name == 'nt':
            target_path = os.path.expanduser("~/AppData/Local/gemini/extensions")
        else:
            # Unix/Linux/Mac路径
            target_path = os.path.expanduser("~/.config/gemini/extensions")
    
    print(f"目标路径: {target_path}")
    
    # 创建目标目录
    os.makedirs(target_path, exist_ok=True)
    print(f"✓ 确保目标目录存在: {target_path}")
    
    # 复制所有Extensions
    source_path = "exports/gemini_extensions"
    config_path = os.path.join(source_path, "extensions.json")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    print(f"\n开始部署 {len(config['extensions'])} 个Extensions:")
    deployed_count = 0
    
    for ext in config['extensions']:
        source_ext_path = os.path.join(source_path, ext['name'])
        target_ext_path = os.path.join(target_path, ext['name'])
        
        try:
            # 如果目标已存在，先删除
            if os.path.exists(target_ext_path):
                shutil.rmtree(target_ext_path)
                print(f"  更新 {ext['name']}")
            else:
                print(f"  部署 {ext['name']}")
            
            # 复制整个Extension目录
            shutil.copytree(source_ext_path, target_ext_path)
            deployed_count += 1
            
        except Exception as e:
            print(f"  ✗ 部署 {ext['name']} 失败: {e}")
            return False
    
    # 复制配置文件
    shutil.copy2(config_path, os.path.join(target_path, "extensions.json"))
    print(f"\n✓ 成功部署 {deployed_count} 个Extensions到 {target_path}")
    return True

def create_mcp_server_stub():
    """创建MCP服务器存根（如果需要）"""
    print("\n=== 创建MCP服务器存根 ===\n")
    
    mcp_stub_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DSGS MCP服务器存根
用于Gemini CLI Extensions的工具执行
"""
import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

class DSGSMCPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.startswith('/mcp'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                request = json.loads(post_data.decode('utf-8'))
                
                # 模拟DSGS技能执行
                response = {
                    "result": f"DSGS技能执行: {request.get('tool', 'unknown')}",
                    "context": "技能执行结果上下文"
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, f"Error: {str(e)}")
        else:
            self.send_error(404)

def main():
    port = 8080
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    
    server = HTTPServer(('localhost', port), DSGSMCPHandler)
    print(f"MCP服务器启动在端口 {port}")
    server.serve_forever()

if __name__ == "__main__":
    main()
'''
    
    # 创建MCP服务器目录结构
    mcp_path = "mcp_servers"
    os.makedirs(mcp_path, exist_ok=True)
    
    with open(os.path.join(mcp_path, "dsgs_mcp_server.py"), 'w', encoding='utf-8') as f:
        f.write(mcp_stub_content)
    
    print("✓ 创建MCP服务器存根: mcp_servers/dsgs_mcp_server.py")
    print("  (需要时可配置到Gemini CLI的settings.json中)")

def create_integration_test_script():
    """创建Gemini CLI集成测试脚本"""
    print("\n=== 创建Gemini CLI集成测试脚本 ===\n")
    
    test_script_content = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gemini CLI Extensions集成测试脚本
"""

import os
import json

def test_extensions_discovery():
    """测试Extensions发现功能"""
    print("=== 测试Extensions发现功能 ===")
    
    # Gemini CLI Extensions路径
    extensions_path = os.path.expanduser("~/.config/gemini/extensions")
    
    if not os.path.exists(extensions_path):
        print("✗ Gemini Extensions目录不存在")
        return False
    
    # 检查Extensions目录
    ext_dirs = [d for d in os.listdir(extensions_path) if os.path.isdir(os.path.join(extensions_path, d))]
    expected_extensions = [
        'dsgs-agent-creator',
        'dsgs-architect',
        'dsgs-constraint-generator',
        'dsgs-dapi-checker',
        'dsgs-modulizer',
        'dsgs-system-architect',
        'dsgs-task-decomposer'
    ]
    
    print(f"发现 {len(ext_dirs)} 个已部署的Extensions:")
    found_extensions = []
    for ext_dir in ext_dirs:
        if ext_dir in expected_extensions:
            print(f"  ✓ {ext_dir}")
            found_extensions.append(ext_dir)
        else:
            print(f"  ? {ext_dir} (额外Extensions)")
    
    missing_extensions = [ext for ext in expected_extensions if ext not in found_extensions]
    if missing_extensions:
        print(f"✗ 缺失 {len(missing_extensions)} 个Extensions: {missing_extensions}")
        return False
    
    print(f"✓ 所有预期Extensions都已部署")
    return True

def test_extension_invocation():
    """测试Extension调用功能"""
    print("\n=== 测试Extension调用功能 ===")
    
    # 测试用例
    test_cases = [
        ("创建一个智能体", "dsgs-agent-creator"),
        ("分解复杂任务", "dsgs-task-decomposer"),
        ("生成系统约束", "dsgs-constraint-generator"),
        ("检查接口一致性", "dsgs-dapi-checker"),
        ("模块化重构", "dsgs-modulizer")
    ]
    
    print("Extension调用测试需要手动验证:")
    print("请在Gemini CLI中尝试以下请求:")
    for i, (request, expected_extension) in enumerate(test_cases, 1):
        print(f"  {i}. '{request}' -> 应该触发 {expected_extension}")
    
    print("\n验证步骤:")
    print("1. 打开Gemini CLI")
    print("2. 输入上述测试请求")
    print("3. 观察是否自动调用相应的Extension")
    print("4. 检查Extension的响应内容")
    
    return True

def main():
    """主函数"""
    print("=== Gemini CLI Extensions集成测试 ===\n")
    
    # 测试Extensions发现
    if not test_extensions_discovery():
        print("\n✗ Extensions发现测试失败")
        return 1
    
    # 测试Extension调用
    if not test_extension_invocation():
        print("\n✗ Extension调用测试失败")
        return 1
    
    print("\n✓ 所有集成测试通过!")
    print("\n集成验证完成。请手动测试Gemini CLI中的Extension调用功能。")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
'''
    
    with open("test_gemini_integration.py", 'w', encoding='utf-8') as f:
        f.write(test_script_content)
    
    print("✓ 创建集成测试脚本: test_gemini_integration.py")
    return True

def main():
    """主函数"""
    print("=== Gemini CLI Extensions集成部署 ===\n")
    
    # 1. 验证Extensions导出
    if not verify_gemini_extensions():
        print("\n✗ Extensions验证失败，无法继续部署")
        return 1
    
    # 2. 部署到Gemini CLI
    if not deploy_to_gemini_cli():
        print("\n✗ Extensions部署失败")
        return 1
    
    # 3. 创建MCP服务器存根
    create_mcp_server_stub()
    
    # 4. 创建测试脚本
    if not create_integration_test_script():
        print("\n✗ 测试脚本创建失败")
        return 1
    
    print("\n=== 部署完成 ===")
    print("✓ 所有DSGS Extensions已成功部署到Gemini CLI")
    print("✓ MCP服务器存根已创建: mcp_servers/dsgs_mcp_server.py")
    print("✓ 集成测试脚本已创建: test_gemini_integration.py")
    print("\n下一步操作:")
    print("1. 确保Gemini CLI已安装并配置")
    print("2. 验证Extensions是否被正确加载")
    print("3. 运行 'python test_gemini_integration.py' 进行验证")
    print("4. 手动测试Extension调用功能")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())