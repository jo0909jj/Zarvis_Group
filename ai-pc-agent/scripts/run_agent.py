#!/usr/bin/env python3
"""
AI PC Agent - 啟動腳本
"""

import sys
import yaml
from pathlib import Path

# 添加父目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from modules.system_monitor import SystemMonitor
from agent.commands import CommandExecutor


def main():
    """主函數"""
    print("🤖 AI PC Agent 啟動")
    print("=" * 60)
    
    # 載入配置
    config_path = Path(__file__).parent.parent / 'config.yaml'
    if config_path.exists():
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        print(f"✅ 配置已載入：{config_path}")
    else:
        print("⚠️ 配置文件不存在，使用預設配置")
        config = {}
    
    # 初始化模組
    print("\n📦 初始化模組...")
    monitor = SystemMonitor()
    executor = CommandExecutor()
    print("✅ 系統監控器就緒")
    print("✅ 命令執行器就緒")
    
    # 生成初始報告
    print("\n📊 生成系統報告...")
    report = monitor.get_report()
    
    print("\n" + "=" * 60)
    print("🖥️  系統狀態")
    print("=" * 60)
    print(f"💻 系統：{report['system']['system']} {report['system']['release']}")
    print(f"📊 CPU: {report['cpu']}%")
    print(f"📊 記憶體：{report['memory']['percent']}%")
    print(f"📊 磁碟：{report['disk']['percent']}%")
    print("=" * 60)
    
    # 檢查閾值
    alerts = monitor.check_thresholds()
    if alerts:
        print("\n⚠️  警告:")
        for alert in alerts:
            print(f"   {alert['level'].upper()}: {alert['type']} = {alert['value']}%")
    else:
        print("\n✅ 系統狀態正常")
    
    print("\n💡 提示:")
    print("   - 運行 'python modules/browser_automation.py' 測試瀏覽器")
    print("   - 運行 'agent/commands.py' 測試命令執行")
    print("   - 運行 'web/dashboard.py' 啟動 Web 介面")
    print("")


if __name__ == "__main__":
    main()
