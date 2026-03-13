#!/usr/bin/env python3
"""
AI PC Agent - 核心模組
"""

import psutil
import platform
import subprocess
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class SystemMonitor:
    """系統監控器"""
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def get_cpu_usage(self) -> float:
        """獲取 CPU 使用率"""
        return psutil.cpu_percent(interval=1)
    
    def get_memory_usage(self) -> dict:
        """獲取記憶體使用情況"""
        mem = psutil.virtual_memory()
        return {
            'total': round(mem.total / (1024**3), 2),  # GB
            'used': round(mem.used / (1024**3), 2),
            'free': round(mem.free / (1024**3), 2),
            'percent': mem.percent
        }
    
    def get_disk_usage(self) -> dict:
        """獲取磁碟使用情況"""
        disk = psutil.disk_usage('/')
        return {
            'total': round(disk.total / (1024**3), 2),
            'used': round(disk.used / (1024**3), 2),
            'free': round(disk.free / (1024**3), 2),
            'percent': disk.percent
        }
    
    def get_network_stats(self) -> dict:
        """獲取網路統計"""
        net_io = psutil.net_io_counters()
        return {
            'bytes_sent': round(net_io.bytes_sent / (1024**2), 2),  # MB
            'bytes_recv': round(net_io.bytes_recv / (1024**2), 2),
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def get_process_list(self, limit=10) -> list:
        """獲取程序列表"""
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # 按 CPU 使用率排序
        processes.sort(key=lambda x: x.get('cpu_percent', 0), reverse=True)
        return processes[:limit]
    
    def get_system_info(self) -> dict:
        """獲取系統資訊"""
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine(),
            'processor': platform.processor(),
            'python_version': platform.python_version(),
            'uptime': str(datetime.now() - self.start_time)
        }
    
    def get_report(self) -> dict:
        """生成完整系統報告"""
        return {
            'timestamp': datetime.now().isoformat(),
            'system': self.get_system_info(),
            'cpu': self.get_cpu_usage(),
            'memory': self.get_memory_usage(),
            'disk': self.get_disk_usage(),
            'network': self.get_network_stats(),
            'top_processes': self.get_process_list(5)
        }
    
    def check_thresholds(self, config: dict = None) -> list:
        """檢查是否超過閾值"""
        if not config:
            config = {
                'cpu_warning': 80,
                'cpu_critical': 95,
                'memory_warning': 80,
                'memory_critical': 95,
                'disk_warning': 80,
                'disk_critical': 90
            }
        
        alerts = []
        
        cpu = self.get_cpu_usage()
        if cpu >= config['cpu_critical']:
            alerts.append({'level': 'critical', 'type': 'cpu', 'value': cpu})
        elif cpu >= config['cpu_warning']:
            alerts.append({'level': 'warning', 'type': 'cpu', 'value': cpu})
        
        memory = self.get_memory_usage()['percent']
        if memory >= config['memory_critical']:
            alerts.append({'level': 'critical', 'type': 'memory', 'value': memory})
        elif memory >= config['memory_warning']:
            alerts.append({'level': 'warning', 'type': 'memory', 'value': memory})
        
        disk = self.get_disk_usage()['percent']
        if disk >= config['disk_critical']:
            alerts.append({'level': 'critical', 'type': 'disk', 'value': disk})
        elif disk >= config['disk_warning']:
            alerts.append({'level': 'warning', 'type': 'disk', 'value': disk})
        
        return alerts


def main():
    """主函數 - 測試用"""
    monitor = SystemMonitor()
    report = monitor.get_report()
    
    print("=" * 60)
    print("🖥️  系統監控報告")
    print("=" * 60)
    print(f"📅 時間：{report['timestamp']}")
    print(f"💻 系統：{report['system']['system']} {report['system']['release']}")
    print(f"🐍 Python: {report['system']['python_version']}")
    print(f"⏱️  運行時間：{report['system']['uptime']}")
    print("")
    print(f"📊 CPU: {report['cpu']}%")
    print(f"📊 記憶體：{report['memory']['used']}/{report['memory']['total']} GB ({report['memory']['percent']}%)")
    print(f"📊 磁碟：{report['disk']['used']}/{report['disk']['total']} GB ({report['disk']['percent']}%)")
    print(f"📊 網路：上傳 {report['network']['bytes_sent']} MB | 下載 {report['network']['bytes_recv']} MB")
    print("")
    print("🔝 Top 5 程序:")
    for i, proc in enumerate(report['top_processes'], 1):
        print(f"   {i}. {proc['name']} (CPU: {proc['cpu_percent']}%, Mem: {proc['memory_percent']}%)")
    print("=" * 60)


if __name__ == "__main__":
    main()
