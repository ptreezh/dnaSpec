#!/usr/bin/env python3
"""
DNASPEC Init - 独立执行接口
提供DNASPEC项目协调机制的初始化和管理功能
"""
import sys
import os
import json
import argparse
from typing import Dict, Any, List, Optional

# 添加主实现路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'src'))

try:
    from dna_spec_kit_integration.skills.dnaspec_init import DNASPECInitSkill, InitOperation, ProjectType, InitType
except ImportError:
    print("❌ 错误: 无法导入DNASPECInitSkill")
    print("请确保已正确安装DNASPEC依赖")
    sys.exit(1)


def parse_operation_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="DNASPEC 项目协调机制初始化和管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 初始化项目
  python dnaspec_init.py --operation init-project --init-type project --features caching,git-hooks
  
  # 检测项目状态
  python dnaspec_init.py --operation detect
  
  # 查看配置
  python dnaspec_init.py --operation get-config
  
  # 重置协调机制
  python dnaspec_init.py --operation reset --confirm
  
  # 获取详细状态
  python dnaspec_init.py --operation status

支持的初始化类型: project, team, enterprise, solo, auto
支持的项目类型: web_application, mobile_app, api_service, desktop_app, library, microservice, data_science, ml_project, generic
支持的特性: caching, git-hooks, ci-cd, monitoring, security
        """
    )
    
    parser.add_argument(
        '--operation', '-o',
        type=str,
        required=True,
        choices=['init-project', 'detect', 'reset', 'get-config', 'status', 'upgrade'],
        help='要执行的操作'
    )
    
    parser.add_argument(
        '--init-type', '-t',
        type=str,
        default='auto',
        choices=['project', 'team', 'enterprise', 'solo', 'auto'],
        help='初始化类型 (默认: auto)'
    )
    
    parser.add_argument(
        '--project-type', '-p',
        type=str,
        default='generic',
        choices=['web_application', 'mobile_app', 'api_service', 'desktop_app', 'library', 'microservice', 'data_science', 'ml_project', 'generic'],
        help='项目类型 (默认: generic)'
    )
    
    parser.add_argument(
        '--features', '-f',
        type=str,
        nargs='*',
        default=[],
        help='要启用的特性列表 (caching git-hooks ci-cd monitoring security)'
    )
    
    parser.add_argument(
        '--force', '-F',
        action='store_true',
        help='强制重新初始化'
    )
    
    parser.add_argument(
        '--confirm', '-c',
        action='store_true',
        help='确认危险操作 (如重置)'
    )
    
    parser.add_argument(
        '--template', '-T',
        type=str,
        help='使用指定的初始化模板'
    )
    
    parser.add_argument(
        '--project-root', '-r',
        type=str,
        help='项目根目录 (默认: 当前目录)'
    )
    
    parser.add_argument(
        '--output-format', '-O',
        type=str,
        choices=['json', 'text'],
        default='text',
        help='输出格式 (默认: text)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='详细输出'
    )
    
    return parser.parse_args()


def format_output(result: Dict[str, Any], format_type: str = 'text', verbose: bool = False) -> str:
    """格式化输出结果"""
    if format_type == 'json':
        return json.dumps(result, indent=2, ensure_ascii=False)
    
    # 文本格式输出
    if not result.get('success', False):
        output = f"❌ 操作失败: {result.get('error', result.get('message', '未知错误'))}\n"
        if verbose and 'timestamp' in result:
            output += f"⏰ 时间: {result['timestamp']}\n"
        return output
    
    operation = result.get('operation', 'unknown')
    
    if operation == 'init-project':
        output = f"✅ {result.get('message', '初始化完成')}\n"
        output += f"📋 初始化类型: {result.get('init_type', 'unknown')}\n"
        output += f"🏗️ 项目类型: {result.get('project_type', 'unknown')}\n"
        
        features = result.get('features_enabled', [])
        if features:
            output += f"⚙️ 启用的特性: {', '.join(features)}\n"
        
        created_files = result.get('created_files', [])
        if created_files:
            output += f"📁 创建的文件:\n"
            for file_path in created_files:
                output += f"   - {file_path}\n"
        
        next_steps = result.get('next_steps', [])
        if next_steps:
            output += f"\n📝 后续步骤:\n"
            for step in next_steps:
                output += f"   {step}\n"
    
    elif operation == 'detect':
        status = result.get('status', 'unknown')
        status_icons = {
            'complete': '✅',
            'partial': '⚠️',
            'not_initialized': '❌'
        }
        icon = status_icons.get(status, '❓')
        
        output = f"{icon} 项目状态: {status}\n"
        
        existing = result.get('existing_files', [])
        missing = result.get('missing_files', [])
        
        if existing:
            output += f"✅ 已存在文件 ({len(existing)}):\n"
            for file_path in existing:
                output += f"   - {file_path}\n"
        
        if missing:
            output += f"❌ 缺失文件 ({len(missing)}):\n"
            for file_path in missing:
                output += f"   - {file_path}\n"
        
        project_features = result.get('project_features', {})
        if project_features:
            output += f"\n🔍 检测到的项目特征:\n"
            languages = project_features.get('languages', [])
            if languages:
                output += f"   🏷️ 编程语言: {', '.join(languages)}\n"
            tools = project_features.get('tools', [])
            if tools:
                output += f"   🛠️ 开发工具: {', '.join(tools)}\n"
    
    elif operation == 'status':
        status = result.get('status', {})
        output = f"📊 详细状态报告\n\n"
        
        status_info = status.get('status', {})
        output += f"🎯 基础状态:\n"
        output += f"   状态: {status_info.get('status', 'unknown')}\n"
        output += f"   项目根目录: {status_info.get('project_root', 'unknown')}\n"
        output += f"   最后检查: {status_info.get('last_check', 'unknown')}\n"
        
        performance = status.get('performance', {})
        if performance:
            output += f"\n⚡ 性能指标:\n"
            output += f"   缓存大小: {performance.get('cache_size_mb', 0)} MB\n"
            output += f"   缓存文件数: {performance.get('cache_files_count', 0)}\n"
        
        features = status.get('features', {})
        if features:
            output += f"\n🔧 功能状态:\n"
            for feature, enabled in features.items():
                icon = "✅" if enabled else "❌"
                output += f"   {icon} {feature}: {'已启用' if enabled else '未启用'}\n"
        
        coordination_enabled = status.get('coordination_enabled', False)
        output += f"\n🤖 协调机制: {'✅ 已启用' if coordination_enabled else '❌ 未启用'}\n"
        
        recommendations = status.get('recommendations', [])
        if recommendations:
            output += f"\n💡 建议:\n"
            for rec in recommendations:
                output += f"   - {rec}\n"
    
    elif operation == 'get-config':
        config = result.get('configuration', {})
        output = f"📋 配置文件信息\n\n"
        output += f"📁 配置文件: {result.get('config_file', 'unknown')}\n"
        output += f"📏 文件大小: {result.get('file_size', 0)} 字节\n"
        output += f"🕒 最后修改: {result.get('last_modified', 'unknown')}\n"
        
        if config:
            output += f"\n📊 配置内容:\n"
            dnaspec_config = config.get('dnaspec', {})
            output += f"   版本: {dnaspec_config.get('version', 'unknown')}\n"
            output += f"   初始化类型: {dnaspec_config.get('init_type', 'unknown')}\n"
            output += f"   项目类型: {dnaspec_config.get('project_type', 'unknown')}\n"
            
            features = dnaspec_config.get('features', {})
            enabled_features = [k for k, v in features.items() if v]
            if enabled_features:
                output += f"   启用的特性: {', '.join(enabled_features)}\n"
    
    elif operation == 'reset':
        output = f"🔄 {result.get('message', '重置完成')}\n"
        backup_info = result.get('backup_info', {})
        if backup_info:
            output += f"💾 备份位置: {backup_info.get('backup_location', 'unknown')}\n"
        
        next_steps = result.get('next_steps', [])
        if next_steps:
            output += f"\n📝 后续步骤:\n"
            for step in next_steps:
                output += f"   {step}\n"
    
    elif operation == 'upgrade':
        output = f"⬆️ {result.get('message', '升级完成')}\n"
        current_version = result.get('current_version', 'unknown')
        output += f"📦 当前版本: {current_version}\n"
    
    else:
        output = f"✅ 操作完成: {result.get('message', '未知操作')}\n"
    
    if verbose and 'timestamp' in result:
        output += f"\n⏰ 执行时间: {result['timestamp']}\n"
    
    return output


def main():
    """主函数"""
    try:
        # 解析参数
        args = parse_operation_args()
        
        # 验证特性参数
        valid_features = ['caching', 'git-hooks', 'ci-cd', 'monitoring', 'security']
        invalid_features = [f for f in args.features if f not in valid_features]
        if invalid_features:
            print(f"❌ 错误: 不支持的特性: {', '.join(invalid_features)}")
            print(f"支持的特性: {', '.join(valid_features)}")
            sys.exit(1)
        
        # 创建技能实例
        project_root = args.project_root or os.getcwd()
        skill = DNASPECInitSkill(project_root=project_root)
        
        # 执行操作
        if args.operation == 'init-project':
            result = skill.execute(
                operation='init-project',
                init_type=args.init_type,
                project_type=args.project_type,
                features=args.features,
                force=args.force,
                template=args.template
            )
        elif args.operation == 'detect':
            result = skill.execute(operation='detect')
        elif args.operation == 'reset':
            result = skill.execute(
                operation='reset',
                confirm=args.confirm,
                backup=True
            )
        elif args.operation == 'get-config':
            result = skill.execute(operation='get-config')
        elif args.operation == 'status':
            result = skill.execute(operation='status')
        elif args.operation == 'upgrade':
            result = skill.execute(operation='upgrade')
        else:
            print(f"❌ 错误: 不支持的操作 '{args.operation}'")
            sys.exit(1)
        
        # 输出结果
        output = format_output(result, args.output_format, args.verbose)
        print(output)
        
        # 设置退出码
        if not result.get('success', False):
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n⚠️ 操作被用户中断")
        sys.exit(130)
    except Exception as e:
        print(f"❌ 意外错误: {str(e)}")
        if args.verbose if 'args' in locals() else False:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
