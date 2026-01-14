"""
Stigmergy检测器
检测系统中是否安装了Stigmergy CLI工具
"""
import subprocess
import os
import sys
from typing import Dict, Any


class StigmergyDetector:
    """Stigmergy检测器"""
    
    @staticmethod
    def is_stigmergy_installed() -> bool:
        """
        检查Stigmergy是否已安装
        
        Returns:
            bool: 如果Stigmergy已安装返回True，否则返回False
        """
        try:
            # 尝试运行stigmergy命令检查版本
            result = subprocess.run(
                ['stigmergy', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=True  # 在Windows上可能需要shell=True
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            # 如果直接调用失败，尝试通过npx调用
            try:
                result = subprocess.run(
                    ['npx', 'stigmergy', '--version'], 
                    capture_output=True, 
                    text=True, 
                    timeout=10
                )
                return result.returncode == 0
            except (subprocess.SubprocessError, FileNotFoundError, OSError):
                return False
    
    @staticmethod
    def get_stigmergy_version() -> str:
        """
        获取Stigmergy版本信息
        
        Returns:
            str: Stigmergy版本号，如果未安装则返回空字符串
        """
        if not StigmergyDetector.is_stigmergy_installed():
            return ""
        
        try:
            # 尝试直接调用
            result = subprocess.run(
                ['stigmergy', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10,
                shell=True
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
        
        try:
            # 尝试通过npx调用
            result = subprocess.run(
                ['npx', 'stigmergy', '--version'], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            pass
            
        return ""
    
    @staticmethod
    def get_detected_clis() -> Dict[str, Any]:
        """
        获取Stigmergy检测到的CLI工具列表
        
        Returns:
            Dict[str, Any]: 检测到的CLI工具信息
        """
        if not StigmergyDetector.is_stigmergy_installed():
            return {}
        
        try:
            # 尝试直接调用
            result = subprocess.run(
                ['stigmergy', 'scan'], 
                capture_output=True, 
                text=True, 
                timeout=30,
                shell=True
            )
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            try:
                # 尝试通过npx调用
                result = subprocess.run(
                    ['npx', 'stigmergy', 'scan'], 
                    capture_output=True, 
                    text=True, 
                    timeout=30
                )
            except (subprocess.SubprocessError, FileNotFoundError, OSError):
                return {}
        
        if result.returncode == 0:
            # 解析扫描结果
            detected_clis = {}
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if '[OK]' in line:
                    # 提取CLI工具名称
                    parts = line.split()
                    if len(parts) >= 3:
                        cli_name = parts[-1].strip('()')
                        detected_clis[cli_name] = {
                            'status': 'available',
                            'detected': True
                        }
            return detected_clis
        else:
            return {}
    
    @staticmethod
    def get_stigmergy_info() -> Dict[str, Any]:
        """
        获取Stigmergy完整信息
        
        Returns:
            Dict[str, Any]: Stigmergy信息字典
        """
        return {
            'installed': StigmergyDetector.is_stigmergy_installed(),
            'version': StigmergyDetector.get_stigmergy_version(),
            'detected_clis': StigmergyDetector.get_detected_clis(),
            'can_integrate': StigmergyDetector.is_stigmergy_installed()
        }


def main():
    """主函数 - Stigmergy检测器命令行接口"""
    import argparse
    import json
    
    parser = argparse.ArgumentParser(description='Stigmergy Detector')
    parser.add_argument('--check', action='store_true', help='Check if Stigmergy is installed')
    parser.add_argument('--version', action='store_true', help='Get Stigmergy version')
    parser.add_argument('--scan', action='store_true', help='Scan for detected CLI tools')
    parser.add_argument('--info', action='store_true', help='Get complete Stigmergy information')
    
    args = parser.parse_args()
    
    if args.check:
        installed = StigmergyDetector.is_stigmergy_installed()
        print(f"Stigmergy installed: {installed}")
        
    elif args.version:
        version = StigmergyDetector.get_stigmergy_version()
        if version:
            print(f"Stigmergy version: {version}")
        else:
            print("Stigmergy not installed or version unavailable")
            
    elif args.scan:
        clis = StigmergyDetector.get_detected_clis()
        if clis:
            print("Detected CLI tools:")
            for cli, info in clis.items():
                print(f"  {cli}: {info}")
        else:
            print("No CLI tools detected or Stigmergy not installed")
            
    elif args.info:
        info = StigmergyDetector.get_stigmergy_info()
        print(json.dumps(info, ensure_ascii=False, indent=2))
    else:
        # 默认显示基本信息
        info = StigmergyDetector.get_stigmergy_info()
        print(f"Stigmergy installed: {info['installed']}")
        if info['installed']:
            print(f"Version: {info['version']}")
            print(f"Can integrate: {info['can_integrate']}")
            if info['detected_clis']:
                print("Detected CLI tools:")
                for cli in info['detected_clis']:
                    print(f"  - {cli}")


if __name__ == "__main__":
    main()