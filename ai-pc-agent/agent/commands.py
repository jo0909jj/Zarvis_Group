#!/usr/bin/env python3
"""
命令執行器
安全地執行系統命令
"""

import subprocess
import platform
import shlex
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class CommandExecutor:
    """命令執行器"""
    
    def __init__(self, allowed_commands=None, blocked_commands=None):
        self.allowed_commands = allowed_commands or [
            'echo', 'dir', 'ls', 'pwd', 'cd', 'mkdir', 'rm', 'cp', 'mv',
            'cat', 'type', 'whoami', 'hostname', 'date', 'time'
        ]
        self.blocked_commands = blocked_commands or [
            'sudo', 'su', 'rm -rf /', 'format', 'del /F /Q /S',
            'shutdown', 'reboot', 'kill', 'taskkill'
        ]
    
    def is_safe(self, command: str) -> bool:
        """檢查命令是否安全"""
        cmd_lower = command.lower()
        
        # 檢查是否在被允許的列表中
        allowed = any(cmd in cmd_lower for cmd in self.allowed_commands)
        
        # 檢查是否在被禁止的列表中
        blocked = any(cmd in cmd_lower for cmd in self.blocked_commands)
        
        return allowed and not blocked
    
    def execute(self, command: str, timeout=30) -> dict:
        """
        執行命令
        
        Returns:
            dict: {
                'success': bool,
                'stdout': str,
                'stderr': str,
                'returncode': int,
                'duration': float
            }
        """
        start_time = datetime.now()
        
        try:
            # 檢查安全性
            if not self.is_safe(command):
                return {
                    'success': False,
                    'stdout': '',
                    'stderr': f'命令不被允許：{command}',
                    'returncode': -1,
                    'duration': 0
                }
            
            # 執行命令
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            duration = (datetime.now() - start_time).total_seconds()
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'duration': duration
            }
        
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': f'命令超時（{timeout}秒）',
                'returncode': -1,
                'duration': timeout
            }
        
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'duration': 0
            }
    
    def open_app(self, app_name: str) -> dict:
        """打開應用程式"""
        system = platform.system()
        
        if system == 'Windows':
            command = f'start "" "{app_name}"'
        elif system == 'Darwin':
            command = f'open -a "{app_name}"'
        else:  # Linux
            command = f'xdg-open "{app_name}"'
        
        return self.execute(command)
    
    def create_file(self, filename: str, content: str = '') -> dict:
        """創建文件"""
        try:
            path = Path(filename)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding='utf-8')
            return {
                'success': True,
                'stdout': f'文件已創建：{filename}',
                'stderr': '',
                'returncode': 0,
                'duration': 0
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1,
                'duration': 0
            }
    
    def list_files(self, path: str = '.') -> dict:
        """列出文件"""
        command = f'dir "{path}"' if platform.system() == 'Windows' else f'ls -la "{path}"'
        return self.execute(command)


def demo():
    """演示"""
    print("⚡ 命令執行器演示")
    print("=" * 60)
    
    executor = CommandExecutor()
    
    # 演示 1：系統資訊
    print("\n📍 任務 1: 獲取系統資訊")
    result = executor.execute('echo Hello from AI PC Agent!')
    print(f"✅ {result['stdout'].strip()}")
    
    # 演示 2：列出文件
    print("\n📍 任務 2: 列出當前目錄")
    result = executor.list_files()
    if result['success']:
        lines = result['stdout'].strip().split('\n')[:10]
        for line in lines:
            print(f"   {line}")
    
    # 演示 3：創建文件
    print("\n📍 任務 3: 創建測試文件")
    result = executor.create_file('test_demo.txt', 'This is a test file created by AI PC Agent')
    if result['success']:
        print(f"✅ {result['stdout']}")
    
    # 演示 4：安全性檢查
    print("\n📍 任務 4: 測試安全性檢查")
    result = executor.execute('sudo rm -rf /')
    print(f"❌ {result['stderr']}")
    
    print("\n" + "=" * 60)
    print("✅ 演示完成！")


if __name__ == "__main__":
    demo()
