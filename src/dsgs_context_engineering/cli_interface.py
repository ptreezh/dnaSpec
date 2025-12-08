"""
CLI Interface for DNASPEC Context Engineering Skills
提供命令行接口访问DSGS技能
"""
import click
from typing import Dict, Any
import json
import sys
import os

# 将项目路径添加到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dnaspec_context_engineering.spec_engine import DSGSSpecEngine, engine


@click.group()
def dnaspec():
    """
    DNASPEC Context Engineering Skills CLI
    专业上下文工程工具集 - 增强AI辅助开发能力
    """
    pass


@dnaspec.command()
@click.argument('context', nargs=-1)
@click.option('--metrics', '-m', default='clarity,relevance,completeness', help='分析指标 (clarity,relevance,completeness,consistency,efficiency)')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json', 'table']), help='输出格式')
def analyze(context: tuple, metrics: str, format: str):
    """
    分析上下文质量
    
    示例: dnaspec analyze "这是要分析的上下文"
    """
    context_str = ' '.join(context) if context else click.get_text_stream('stdin').read()
    
    if not context_str.strip():
        click.echo("错误: 请提供要分析的上下文")
        return
    
    # 准备参数
    params = {
        'metrics': metrics.split(','),
        'output_format': format
    }
    
    # 执行技能
    result = engine.execute_skill('context-analysis', context_str, params)
    
    # 输出结果
    if result['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        elif format == 'table':
            click.echo("上下文质量分析结果:")
            click.echo("-" * 40)
            for metric, score in result['result']['metrics'].items():
                click.echo(f"{metric:12s} | {score:6.2f}")
        else:  # text format
            click.echo("上下文分析结果:")
            click.echo(f"长度: {result['result']['context_length']} 字符")
            click.echo(f"Token估算: {result['result']['token_count']}")
            click.echo("")
            click.echo("质量指标 (0.0-1.0):")
            for metric, score in result['result']['metrics'].items():
                metric_names = {
                    'clarity': '清晰度',
                    'relevance': '相关性',
                    'completeness': '完整性', 
                    'consistency': '一致性',
                    'efficiency': '效率'
                }
                indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                click.echo(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
            
            if result['result']['suggestions']:
                click.echo("\n优化建议:")
                for suggestion in result['result']['suggestions']:
                    click.echo(f"  • {suggestion}")
    else:
        click.echo(f"错误: {result['error']}", err=True)


@dnaspec.command()
@click.argument('context', nargs=-1)
@click.option('--goals', '-g', default='clarity,completeness', help='优化目标 (clarity,relevance,completeness,conciseness)')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json']), help='输出格式')
def optimize(context: tuple, goals: str, format: str):
    """
    优化上下文质量
    
    示例: dnaspec optimize --goals "clarity,completeness" "这是待优化的上下文"
    """
    context_str = ' '.join(context) if context else click.get_text_stream('stdin').read()
    
    if not context_str.strip():
        click.echo("错误: 请提供要优化的上下文")
        return
    
    # 准备参数
    params = {
        'optimization_goals': goals.split(','),
        'output_format': format
    }
    
    # 执行技能
    result = engine.execute_skill('context-optimization', context_str, params)
    
    # 输出结果
    if result['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            click.echo("上下文优化结果:")
            click.echo(f"原始长度: {result['result']['original_analysis']['context_length']} 字符")
            click.echo(f"优化后长度: {result['result']['optimized_analysis']['context_length']} 字符")
            click.echo("")
            
            click.echo("优化改进:")
            for metric, improvement in result['result']['improvement_metrics'].items():
                direction = "↗️" if improvement > 0 else "↘️" if improvement < 0 else "➡️"
                click.echo(f"  {direction} {metric}: {improvement:+.2f}")
            
            click.echo("\n优化后上下文:")
            click.echo(result['result']['optimized_context'])
    else:
        click.echo(f"错误: {result['error']}", err=True)


@dnaspec.command()
@click.argument('task', nargs=-1)
@click.option('--template', '-t', default='chain_of_thought', 
              type=click.Choice(['chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding']),
              help='认知模板类型')
@click.option('--role', '-r', default='专家', help='角色扮演中的角色')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json']), help='输出格式')
def template(task: tuple, template: str, role: str, format: str):
    """
    应用认知模板到任务
    
    示例: dnaspec template --template chain_of_thought "如何设计系统架构？"
    """
    task_str = ' '.join(task) if task else click.get_text_stream('stdin').read()
    
    if not task_str.strip():
        click.echo("错误: 请提供要应用模板的任务")
        return
    
    # 准备参数
    params = {
        'template': template,
        'role': role,
        'output_format': format
    }
    
    # 执行技能
    result = engine.execute_skill('cognitive-template', task_str, params)
    
    # 输出结果
    if result['success'] and result['result']['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            click.echo(f"应用认知模板: {result['result']['template_name']} ({result['result']['template_description']})")
            click.echo("=" * 60)
            click.echo("")
            click.echo("结构化后的任务:")
            click.echo(result['result']['enhanced_context'])
    else:
        error_msg = result['result']['error'] if result['success'] else result['error']
        click.echo(f"错误: {error_msg}", err=True)


@dnaspec.command()
def list():
    """
    列出所有可用的DSGS技能
    """
    skills = engine.list_available_skills()
    click.echo("DNASPEC Context Engineering Skills:")
    click.echo("-" * 50)
    for name, description in skills.items():
        click.echo(f"{name:25s} - {description}")


@dnaspec.command()
@click.option('--skill', '-s', required=True, help='技能名称')
@click.option('--context', '-c', required=True, help='要处理的上下文')
def execute(skill: str, context: str):
    """
    执行指定的DSGS技能
    
    示例: dnaspec execute --skill context-analysis --context "要分析的内容"
    """
    result = engine.execute_skill(skill, context, {})
    
    if result['success']:
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo(f"错误: {result['error']}", err=True)


@dnaspec.command()
def demo():
    """
    运行DSGS功能演示
    """
    click.echo("🎯 DNASPEC Context Engineering Skills 演示")
    click.echo("=" * 60)
    
    sample_context = "设计一个电商平台，需要支持用户注册登录、商品浏览、购物车、订单处理等功能。"
    
    click.echo("\n📝 示例上下文:")
    click.echo(sample_context)
    click.echo("")
    
    # 执行分析
    click.echo("🔍 执行上下文分析...")
    analysis_result = engine.execute_skill('context-analysis', sample_context, {})
    if analysis_result['success']:
        metrics = analysis_result['result']['metrics']
        click.echo("   质量指标:")
        for metric, score in metrics.items():
            metric_names = {'clarity': '清晰度', 'relevance': '相关性', 'completeness': '完整性', 
                           'consistency': '一致性', 'efficiency': '效率'}
            indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
            click.echo(f"     {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
    
    # 执行优化
    click.echo("\n🚀 执行上下文优化...")
    optimization_result = engine.execute_skill('context-optimization', sample_context, 
                                              {'optimization_goals': ['clarity', 'completeness']})
    if optimization_result['success']:
        improved_context = optimization_result['result']['optimized_context']
        click.echo(f"   优化后内容长度: {len(improved_context)} 字符")
    
    # 应用模板
    click.echo("\n🧠 应用认知模板...")
    template_result = engine.execute_skill('cognitive-template', "如何优化电商平台性能？", 
                                          {'template': 'chain_of_thought'})
    if template_result['success'] and template_result['result']['success']:
        click.echo("   思维链结构化成功")
    
    click.echo("\n✅ 演示完成！DSGS系统已准备就绪。")


if __name__ == '__main__':
    dnaspec()