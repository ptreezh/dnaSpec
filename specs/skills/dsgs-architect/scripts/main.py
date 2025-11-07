# dsgs-architect主技能协调脚本

import sys
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

# 添加src目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))

try:
    from dsgs_architect import DSGSArchitect
    SKILL_AVAILABLE = True
except ImportError:
    SKILL_AVAILABLE = False
    print("警告: 无法导入dsgs_architect模块", file=sys.stderr)

def main():
    """主函数 - 技能协调入口点"""
    if not SKILL_AVAILABLE:
        print("错误: 技能模块不可用", file=sys.stderr)
        sys.exit(1)
    
    # 创建技能实例
    architect = DSGSArchitect()
    
    # 获取输入参数
    if len(sys.argv) > 1:
        user_request = " ".join(sys.argv[1:])
    else:
        # 从stdin读取输入
        user_request = sys.stdin.read().strip() if not sys.stdin.isatty() else ""
    
    # 处理请求
    result = process_user_request(architect, user_request)
    
    # 输出结果
    output_result(result)

def process_user_request(architect: DSGSArchitect, request: str) -> Dict[str, Any]:
    """处理用户请求"""
    try:
        if not request or not request.strip():
            return {
                "status": "error",
                "error": "请求不能为空",
                "timestamp": datetime.now().isoformat()
            }
        
        # 处理请求
        result = architect.process_request(request)
        result["status"] = "success"
        
        # 添加技能信息
        result["skill_info"] = architect.get_skill_info()
        
        return result
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

def output_result(result: Dict[str, Any]):
    """输出结果"""
    # 以JSON格式输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))

def get_skill_metadata() -> Dict[str, Any]:
    """获取技能元数据"""
    if not SKILL_AVAILABLE:
        return {"error": "技能不可用"}
    
    try:
        # 读取SKILL.md文件
        skill_md_path = os.path.join(os.path.dirname(__file__), '..', '..', 'skills', 'dsgs-architect', 'SKILL.md')
        if os.path.exists(skill_md_path):
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 简单解析YAML前言
            lines = content.split('\n')
            metadata = {}
            in_yaml = False
            
            for line in lines:
                if line.strip() == '---':
                    if not in_yaml:
                        in_yaml = True
                        continue
                    else:
                        break
                elif in_yaml and ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip().strip('"\'')
            
            return metadata
        else:
            return {"error": "SKILL.md文件不存在"}
    except Exception as e:
        return {"error": f"读取元数据失败: {str(e)}"}

if __name__ == "__main__":
    # 检查是否需要输出元数据
    if len(sys.argv) > 1 and sys.argv[1] == "--metadata":
        metadata = get_skill_metadata()
        print(json.dumps(metadata, ensure_ascii=False, indent=2))
    else:
        main()