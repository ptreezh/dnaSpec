"""
CLI Interface for DNASPEC Context Engineering Skills
Provides command-line interface to access DNASPEC skills
"""
import click
from typing import Dict, Any
import json
import sys
import os

# Add project path to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.dnaspec_context_engineering.spec_engine import DNASPECSpecEngine, engine


@click.group()
def dnaspec():
    """
    DNASPEC Context Engineering Skills CLI
    Professional Context Engineering Toolkit - Enhanced AI-assisted Development Capabilities
    """
    pass


@dnaspec.command()
@click.argument('context', nargs=-1)
@click.option('--metrics', '-m', default='clarity,relevance,completeness', help='Analysis metrics (clarity,relevance,completeness,consistency,efficiency)')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json', 'table']), help='Output format')
def analyze(context: tuple, metrics: str, format: str):
    """
    Analyze context quality
    
    Example: dnaspec analyze "This is the context to analyze"
    """
    context_str = ' '.join(context) if context else click.get_text_stream('stdin').read()
    
    if not context_str.strip():
        click.echo("Error: Please provide context to analyze")
        return
    
    # Prepare parameters
    params = {
        'metrics': metrics.split(','),
        'output_format': format
    }
    
    # Execute skill
    result = engine.execute_skill('context-analysis', context_str, params)
    
    # Output results
    if result['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        elif format == 'table':
            click.echo("Context Quality Analysis Results:")
            click.echo("-" * 40)
            for metric, score in result['result']['metrics'].items():
                click.echo(f"{metric:12s} | {score:6.2f}")
        else:  # text format
            click.echo("Context Analysis Results:")
            click.echo(f"Length: {result['result']['context_length']} characters")
            click.echo(f"Token estimate: {result['result']['token_count']}")
            click.echo("")
            click.echo("Quality Metrics (0.0-1.0):")
            for metric, score in result['result']['metrics'].items():
                metric_names = {
                    'clarity': 'Clarity',
                    'relevance': 'Relevance',
                    'completeness': 'Completeness', 
                    'consistency': 'Consistency',
                    'efficiency': 'Efficiency'
                }
                indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
                click.echo(f"  {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
            
            if result['result']['suggestions']:
                click.echo("\nOptimization Suggestions:")
                for suggestion in result['result']['suggestions']:
                    click.echo(f"  • {suggestion}")
    else:
        click.echo(f"Error: {result['error']}", err=True)


@dnaspec.command()
@click.argument('context', nargs=-1)
@click.option('--goals', '-g', default='clarity,completeness', help='Optimization goals (clarity,relevance,completeness,conciseness)')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json']), help='Output format')
def optimize(context: tuple, goals: str, format: str):
    """
    Optimize context quality
    
    Example: dnaspec optimize --goals "clarity,completeness" "This is the context to optimize"
    """
    context_str = ' '.join(context) if context else click.get_text_stream('stdin').read()
    
    if not context_str.strip():
        click.echo("Error: Please provide context to optimize")
        return
    
    # Prepare parameters
    params = {
        'optimization_goals': goals.split(','),
        'output_format': format
    }
    
    # Execute skill
    result = engine.execute_skill('context-optimization', context_str, params)
    
    # Output results
    if result['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            click.echo("Context Optimization Results:")
            click.echo(f"Original length: {result['result']['original_analysis']['context_length']} characters")
            click.echo(f"Optimized length: {result['result']['optimized_analysis']['context_length']} characters")
            click.echo("")
            
            click.echo("Optimization Improvements:")
            for metric, improvement in result['result']['improvement_metrics'].items():
                direction = "↗️" if improvement > 0 else "↘️" if improvement < 0 else "➡️"
                click.echo(f"  {direction} {metric}: {improvement:+.2f}")
            
            click.echo("\nOptimized Context:")
            click.echo(result['result']['optimized_context'])
    else:
        click.echo(f"Error: {result['error']}", err=True)


@dnaspec.command()
@click.argument('task', nargs=-1)
@click.option('--template', '-t', default='chain_of_thought', 
              type=click.Choice(['chain_of_thought', 'few_shot', 'verification', 'role_playing', 'understanding']),
              help='Cognitive template type')
@click.option('--role', '-r', default='Expert', help='Role in role playing')
@click.option('--format', '-f', default='text', type=click.Choice(['text', 'json']), help='Output format')
def template(task: tuple, template: str, role: str, format: str):
    """
    Apply cognitive template to task
    
    Example: dnaspec template --template chain_of_thought "How to design system architecture?"
    """
    task_str = ' '.join(task) if task else click.get_text_stream('stdin').read()
    
    if not task_str.strip():
        click.echo("Error: Please provide a task to apply template to")
        return
    
    # Prepare parameters
    params = {
        'template': template,
        'role': role,
        'output_format': format
    }
    
    # Execute skill
    result = engine.execute_skill('cognitive-template', task_str, params)
    
    # Output results
    if result['success'] and result['result']['success']:
        if format == 'json':
            click.echo(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            click.echo(f"Applied Cognitive Template: {result['result']['template_name']} ({result['result']['template_description']})")
            click.echo("=" * 60)
            click.echo("")
            click.echo("Structured Task:")
            click.echo(result['result']['enhanced_context'])
    else:
        error_msg = result['result']['error'] if result['success'] else result['error']
        click.echo(f"Error: {error_msg}", err=True)


@dnaspec.command()
def list():
    """
    List all available DNASPEC skills
    """
    skills = engine.list_available_skills()
    click.echo("DNASPEC Context Engineering Skills:")
    click.echo("-" * 50)
    for name, description in skills.items():
        click.echo(f"{name:25s} - {description}")


@dnaspec.command()
@click.option('--skill', '-s', required=True, help='Skill name')
@click.option('--context', '-c', required=True, help='Context to process')
def execute(skill: str, context: str):
    """
    Execute specified DNASPEC skill
    
    Example: dnaspec execute --skill context-analysis --context "Content to analyze"
    """
    result = engine.execute_skill(skill, context, {})
    
    if result['success']:
        click.echo(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        click.echo(f"Error: {result['error']}", err=True)


@dnaspec.command()
def demo():
    """
    Run DNASPEC feature demonstration
    """
    click.echo("🎯 DNASPEC Context Engineering Skills Demo")
    click.echo("=" * 60)
    
    sample_context = "Design an e-commerce platform that needs to support user registration/login, product browsing, shopping cart, and order processing functions."
    
    click.echo("\n📝 Sample Context:")
    click.echo(sample_context)
    click.echo("")
    
    # Execute analysis
    click.echo("🔍 Executing Context Analysis...")
    analysis_result = engine.execute_skill('context-analysis', sample_context, {})
    if analysis_result['success']:
        metrics = analysis_result['result']['metrics']
        click.echo("   Quality Metrics:")
        for metric, score in metrics.items():
            metric_names = {'clarity': 'Clarity', 'relevance': 'Relevance', 'completeness': 'Completeness', 
                           'consistency': 'Consistency', 'efficiency': 'Efficiency'}
            indicator = "🟢" if score >= 0.7 else "🟡" if score >= 0.4 else "🔴"
            click.echo(f"     {indicator} {metric_names.get(metric, metric)}: {score:.2f}")
    
    # Execute optimization
    click.echo("\n🚀 Executing Context Optimization...")
    optimization_result = engine.execute_skill('context-optimization', sample_context, 
                                              {'optimization_goals': ['clarity', 'completeness']})
    if optimization_result['success']:
        improved_context = optimization_result['result']['optimized_context']
        click.echo(f"   Optimized content length: {len(improved_context)} characters")
    
    # Apply template
    click.echo("\n🧠 Applying Cognitive Template...")
    template_result = engine.execute_skill('cognitive-template', "How to optimize e-commerce platform performance?", 
                                          {'template': 'chain_of_thought'})
    if template_result['success'] and template_result['result']['success']:
        click.echo("   Chain-of-thought structuring successful")
    
    click.echo("\n✅ Demo completed! DNASPEC system is ready.")