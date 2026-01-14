#!/usr/bin/env python3
"""
DNASPEC 双重部署系统测试
测试标准化部署和Slash命令部署的兼容性
"""
import sys
import os
import json
import shutil
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

def test_skill_command_mapper():
    """测试技能命令映射器"""
    print("🧪 测试技能命令映射器...")
    
    try:
        from src.dna_spec_kit_integration.core.skill_command_mapper import SkillCommandMapper
        
        skills_root = project_root / "skills"
        if not skills_root.exists():
            print("❌ Skills 目录不存在")
            return False
            
        mapper = SkillCommandMapper(skills_root)
        commands = mapper.scan_skills()
        
        print(f"✅ 成功扫描 {len(commands)} 个技能")
        
        # 显示发现的技能
        for skill_name, command in list(commands.items())[:3]:  # 显示前3个
            print(f"  📋 {skill_name}: {command.description}")
            print(f"     分类: {command.category}")
            print(f"     别名: {command.aliases}")
        
        # 测试导出功能
        output_dir = project_root / "test_output"
        output_dir.mkdir(exist_ok=True)
        
        manifest_path = output_dir / "skills_manifest.json"
        success = mapper.export_manifest(manifest_path)
        
        if success and manifest_path.exists():
            print("✅ 技能清单导出成功")
            manifest_data = json.loads(manifest_path.read_text(encoding='utf-8'))
            print(f"   包含 {len(manifest_data.get('commands', {}))} 个技能")
        else:
            print("❌ 技能清单导出失败")
            
        return True
        
    except Exception as e:
        print(f"❌ 技能命令映射器测试失败: {e}")
        return False

def test_slash_command_handler():
    """测试Slash命令处理器"""
    print("\n🧪 测试Slash命令处理器...")
    
    try:
        from src.dna_spec_kit_integration.core.slash_command_handler import SlashCommandHandler
        
        skills_root = project_root / "skills"
        handler = SlashCommandHandler(skills_root)
        
        print(f"✅ 成功加载 {len(handler.commands)} 个技能命令")
        
        # 测试解析器创建
        parser = handler.create_parser()
        print("✅ 命令解析器创建成功")
        
        # 测试帮助信息
        help_result = handler.handle_command(type('Args', (), {'command': None})())
        if help_result.get('success'):
            print("✅ 帮助信息生成成功")
        
        # 测试列表命令
        list_result = handler.handle_command(
            type('Args', (), {
                'command': 'list',
                'category': None,
                'format': 'json'
            })()
        )
        if list_result.get('success'):
            print("✅ 列表命令执行成功")
        
        return True
        
    except Exception as e:
        print(f"❌ Slash命令处理器测试失败: {e}")
        return False

def test_standard_deployment():
    """测试标准化部署"""
    print("\n🧪 测试标准化部署...")
    
    try:
        # 创建测试目录
        test_claude_dir = project_root / "test_claude_skills"
        if test_claude_dir.exists():
            shutil.rmtree(test_claude_dir)
        test_claude_dir.mkdir()
        
        # 复制技能目录
        skills_root = project_root / "skills"
        if not skills_root.exists():
            print("❌ Skills 目录不存在")
            return False
            
        skill_count = 0
        for skill_dir in skills_root.iterdir():
            if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                dest_dir = test_claude_dir / skill_dir.name
                shutil.copytree(skill_dir, dest_dir)
                skill_count += 1
                print(f"  📁 复制技能: {skill_dir.name}")
        
        print(f"✅ 标准化部署成功，复制了 {skill_count} 个技能")
        
        # 验证目录结构
        expected_dirs = ['scripts', 'references', 'assets']
        for skill_dir in test_claude_dir.iterdir():
            for expected_dir in expected_dirs:
                if not (skill_dir / expected_dir).exists():
                    print(f"⚠️  技能 {skill_dir.name} 缺少目录: {expected_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ 标准化部署测试失败: {e}")
        return False

def test_cli_integration():
    """测试CLI集成"""
    print("\n🧪 测试CLI集成...")
    
    try:
        # 测试CLI命令执行
        import subprocess
        
        # 测试帮助命令
        result = subprocess.run([
            sys.executable, "cli_direct.py", "help"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ CLI帮助命令执行成功")
        else:
            print(f"❌ CLI帮助命令失败: {result.stderr}")
        
        # 测试列表命令
        result = subprocess.run([
            sys.executable, "cli_direct.py", "list"
        ], capture_output=True, text=True, cwd=project_root)
        
        if result.returncode == 0:
            print("✅ CLI列表命令执行成功")
        else:
            print(f"❌ CLI列表命令失败: {result.stderr}")
        
        return True
        
    except Exception as e:
        print(f"❌ CLI集成测试失败: {e}")
        return False

def generate_test_report(results):
    """生成测试报告"""
    print("\n📊 双重部署系统测试报告")
    print("=" * 50)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results.values() if result)
    
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {passed_tests}")
    print(f"失败测试: {total_tests - passed_tests}")
    print(f"成功率: {passed_tests / total_tests * 100:.1f}%")
    
    print("\n详细结果:")
    for test_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"  {test_name}: {status}")
    
    # 生成建议
    print("\n💡 使用建议:")
    if all(results.values()):
        print("  🎉 所有测试通过！双重部署系统工作正常")
        print("  📖 可以使用以下命令:")
        print("    - 标准化部署: cp -r skills/* .claude/skills/")
        print("    - CLI命令: dnaspec slash <skill-name> --help")
        print("    - 列出技能: dnaspec slash list")
    else:
        print("  ⚠️  部分测试失败，请检查上述错误信息")
        print("  🔧 建议先解决失败的问题后再使用部署功能")
    
    return passed_tests == total_tests

def main():
    """主函数"""
    print("🚀 DNASPEC 双重部署系统测试")
    print("=" * 50)
    
    results = {}
    
    # 运行所有测试
    results["技能命令映射器"] = test_skill_command_mapper()
    results["Slash命令处理器"] = test_slash_command_handler()
    results["标准化部署"] = test_standard_deployment()
    results["CLI集成"] = test_cli_integration()
    
    # 生成报告
    all_passed = generate_test_report(results)
    
    # 清理测试文件
    test_claude_dir = project_root / "test_claude_skills"
    if test_claude_dir.exists():
        shutil.rmtree(test_claude_dir)
    
    test_output_dir = project_root / "test_output"
    if test_output_dir.exists():
        shutil.rmtree(test_output_dir)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())