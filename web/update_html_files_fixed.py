#!/usr/bin/env python3
"""
DNASPEC HTML文件批量更新工具 (修复版)
为所有HTML文件添加统一的样式和导航
"""

import os
import re
from pathlib import Path

# HTML文件导航模板
NAVIGATION_TEMPLATE = '''    <!-- 统一的导航栏 -->
    <nav>
        <div class="container">
            <div class="nav-container">
                <div class="logo">
                    <a href="../index.html" style="color: white; text-decoration: none;">
                        <i class="fas fa-dna"></i> DNASPEC
                    </a>
                </div>
                <ul class="nav-links">
                    <li><a href="../index.html">首页</a></li>
                    <li><a href="index.html">主页</a></li>
                    <li><a href="../demo/agentic_demo.html">演示</a></li>
                    <li><a href="../concepts/agentic_system_vision.html">概念</a></li>
                    <li><a href="../docs/api_documentation_page.html">文档</a></li>
                    <li><a href="../guides/avoid_pitfalls_guide.html">指南</a></li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- 面包屑导航 -->
    <div class="container">
        <div class="breadcrumb">
            <a href="../index.html">首页</a>
            <span class="separator">></span>
            <span class="current-page">{current_page}</span>
        </div>
    </div>'''

# 页脚模板
FOOTER_TEMPLATE = '''    <!-- 统一的页脚 -->
    <footer>
        <div class="container">
            <p><strong>DNASPEC</strong> - DNA驱动的AI上下文工程系统</p>
            <p>© 2025 DNASPEC Team. 保留所有权利。</p>
            <p>
                <a href="../index.html" style="color: white; margin: 0 1rem;">首页</a> |
                <a href="index.html" style="color: white; margin: 0 1rem;">主页</a> |
                <a href="../docs/api_documentation_page.html" style="color: white; margin: 0 1rem;">文档</a> |
                <a href="../demo/agentic_demo.html" style="color: white; margin: 0 1rem;">演示</a> |
                <a href="../README.html" style="color: white; margin: 0 1rem;">导航</a>
            </p>
        </div>
    </footer>

    <script>
        // 简单的动画效果
        document.addEventListener('DOMContentLoaded', function() {{
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};

            const observer = new IntersectionObserver(function(entries) {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.classList.add('fade-in-up');
                    }}
                }});
            }}, observerOptions);

            // 观察所有内容区域
            document.querySelectorAll('.content-section').forEach(section => {{
                observer.observe(section);
            }});

            // 观察所有卡片
            document.querySelectorAll('.card').forEach(card => {{
                observer.observe(card);
            }});
        }});
    </script>'''

def get_category_from_path(file_path):
    """根据文件路径确定页面类别"""
    file_path_str = str(file_path)
    if 'homepage' in file_path_str:
        return '主页'
    elif 'demo' in file_path_str:
        return '演示'
    elif 'concepts' in file_path_str:
        return '概念'
    elif 'docs' in file_path_str:
        return '文档'
    elif 'guides' in file_path_str:
        return '指南'
    else:
        return '页面'

def update_html_file(file_path):
    """更新单个HTML文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 备份原文件
        backup_path = str(file_path) + '.backup'
        with open(backup_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 获取页面标题和类别
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1) if title_match else 'DNASPEC页面'
        category = get_category_from_path(file_path)
        
        # 检查是否已经有统一的CSS
        has_unified_css = 'dnaspec-unified.css' in content
        
        # 添加CSS链接（如果还没有）
        if not has_unified_css:
            css_link = '''    <link rel="stylesheet" href="../styles/dnaspec-unified.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">'''
            
            # 在</head>前添加CSS链接
            content = re.sub(r'</head>', css_link + '\n</head>', content)
        
        # 移除现有的内联样式（如果存在）
        content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL)
        
        # 查找<body>标签
        body_match = re.search(r'<body[^>]*>', content)
        if body_match:
            body_tag = body_match.group(0)
            body_end = body_match.end()
            
            # 在<body>标签后添加导航
            navigation = NAVIGATION_TEMPLATE.format(current_page=title)
            content = content[:body_end] + '\n' + navigation + '\n' + content[body_end:]
        
        # 查找</body>标签前的位置
        body_end_match = re.search(r'</body>', content)
        if body_end_match:
            body_start = body_end_match.start()
            
            # 在</body>前添加页脚和脚本
            footer = FOOTER_TEMPLATE
            content = content[:body_start] + '\n' + footer + '\n' + content[body_start:]
        
        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ 更新完成: {file_path}")
        return True
        
    except Exception as e:
        print(f"❌ 更新失败: {file_path} - {e}")
        return False

def main():
    """主函数"""
    web_dir = Path(".")
    html_files = list(web_dir.glob("**/*.html"))
    
    print(f"🔍 发现 {len(html_files)} 个HTML文件")
    
    success_count = 0
    total_count = len(html_files)
    
    for html_file in html_files:
        # 跳过已经更新的文件
        if 'dnaspec-unified.css' in str(html_file.name):
            continue
        if 'navigation-template.html' in str(html_file.name):
            continue
        if 'README.html' in str(html_file.name):
            continue
        if 'update_html_files' in str(html_file.name):
            continue
        # 跳过node_modules中的文件
        if 'node_modules' in str(html_file):
            continue
        # 跳过不需要更新的文件
        if html_file.name in ['README.html', 'index.html']:
            continue
            
        if update_html_file(html_file):
            success_count += 1
    
    print(f"\n📊 更新统计:")
    print(f"   总文件数: {total_count}")
    print(f"   成功更新: {success_count}")
    print(f"   失败: {total_count - success_count}")
    
    if success_count > 0:
        print(f"\n✅ 成功更新了 {success_count} 个HTML文件")
        print("💡 备份文件保存为 *.backup")
    else:
        print("\n❌ 没有文件需要更新或更新失败")

if __name__ == "__main__":
    main()