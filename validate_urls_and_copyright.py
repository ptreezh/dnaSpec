"""
Final Validation Script - Check that all URLs and copyrights are correct
"""
import os
import sys
import re

def check_files(directory, file_pattern="*.md"):
    """Check all files in directory for correct URLs and copyright"""
    print(f"Checking files in {directory} for correct URLs and copyright information...")
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.py')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查URL - 应该是正确的仓库地址
                    if 'github.com/AgentPsy/dsgs-context-engineering' in content:
                        print(f"  ⚠️  Found incorrect URL in {filepath}")
                    elif 'github.com/ptreezh/dnaSpec' in content:
                        print(f"  ✓ Correct URL in {filepath}")
                    else:
                        # 检查是否有其他不正确的URL
                        urls = re.findall(r'https://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+', content)
                        for url in urls:
                            if 'github.com/' in url and 'ptreezh/dnaSpec' not in url:
                                print(f"  ⚠️  Potentially incorrect URL in {filepath}: {url}")
                
                    # 检查版权
                    if 'AI Personality Lab' in content or 'agentpsy.com' in content:
                        print(f"  ✓ Correct copyright in {filepath}")
                    elif 'AI Persona Lab' in content:
                        print(f"  ⚠️  Found old copyright in {filepath}")
                        
                except Exception as e:
                    print(f"  ❌ Error reading {filepath}: {e}")

if __name__ == "__main__":
    # 检查主目录
    print("Validating main project files...")
    check_files(r"D:\DAIP\dnaSpec", "*.md")
    
    print("\nValidating dist directory...")
    check_files(r"D:\DAIP\dnaSpec\dist", "*.md")
    
    print("\nValidating clean_skills directory...")
    check_files(r"D:\DAIP\dnaSpec\dist\clean_skills", "*.py")
    
    print("\nValidation completed!")