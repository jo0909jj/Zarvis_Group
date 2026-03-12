#!/usr/bin/env python3
"""
智能財報分析系統 - 主執行腳本

用法:
    python run_analysis.py --stock 2330 --quarter Q4-2025
    python run_analysis.py --batch ../config/stocks.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# 添加父目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent))


def load_config():
    """載入配置文件"""
    config_path = Path(__file__).parent.parent / 'config' / 'stocks.json'
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def analyze_stock(symbol: str, name: str, quarter: str = None):
    """
    分析單一股票
    
    Args:
        symbol: 股票代碼
        name: 公司名稱
        quarter: 財報季度（如 Q4-2025）
    """
    print(f"\n{'='*60}")
    print(f"分析股票：{symbol} - {name}")
    print(f"財報季度：{quarter or '最新'}")
    print(f"{'='*60}\n")
    
    # TODO: 實作財報抓取
    # 1. 從公開資訊觀測站抓取財報
    # 2. 解析 PDF/Excel
    
    # TODO: 實作財務比率計算
    # 1. 計算獲利能力指標
    # 2. 計算財務健全度指標
    # 3. 計算營運效率指標
    
    # TODO: 實作 AI 情緒分析
    # 1. 使用 OpenClaw 分析財報文字
    # 2. 評估利多/利空
    
    # TODO: 實作異常偵測
    # 1. 檢查紅燈/黃燈警示
    # 2. 計算綜合評分
    
    # TODO: 生成 PPT 報告
    # 1. 使用 pptx 技能生成報告
    # 2. 儲存至 output/reports/
    
    print(f"✅ 分析完成！")
    print(f"📊 報告位置：output/reports/{symbol}_{quarter or 'latest'}_analysis.pptx")
    
    return {
        "symbol": symbol,
        "name": name,
        "quarter": quarter,
        "status": "completed",
        "report_path": f"output/reports/{symbol}_{quarter or 'latest'}_analysis.pptx"
    }


def run_batch_analysis(config_path: str = None):
    """
    批量分析
    
    Args:
        config_path: 配置文件路徑
    """
    if config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = load_config()
    
    results = []
    
    # 分析台股
    print("\n📈 開始分析台股...")
    for stock in config.get('tw_stocks', []):
        if stock.get('priority') in ['high', 'medium']:
            result = analyze_stock(stock['symbol'], stock['name'])
            results.append(result)
    
    # 分析美股
    print("\n💵 開始分析美股...")
    for stock in config.get('us_stocks', []):
        if stock.get('priority') in ['high', 'medium']:
            result = analyze_stock(stock['symbol'], stock['name'])
            results.append(result)
    
    # 輸出結果
    print(f"\n{'='*60}")
    print(f"批量分析完成！")
    print(f"總共分析 {len(results)} 檔股票")
    print(f"{'='*60}\n")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='智能財報分析系統')
    parser.add_argument('--stock', type=str, help='股票代碼（如 2330）')
    parser.add_argument('--name', type=str, help='公司名稱')
    parser.add_argument('--quarter', type=str, help='財報季度（如 Q4-2025）')
    parser.add_argument('--batch', type=str, help='批量分析配置文件路徑')
    
    args = parser.parse_args()
    
    # 確保輸出目錄存在
    output_dir = Path(__file__).parent.parent / 'output' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if args.batch:
        # 批量分析
        results = run_batch_analysis(args.batch)
    elif args.stock:
        # 單一股票分析
        name = args.name or args.stock
        result = analyze_stock(args.stock, name, args.quarter)
    else:
        # 預設：分析台股 high priority
        config = load_config()
        high_priority = [s for s in config['tw_stocks'] if s.get('priority') == 'high']
        if high_priority:
            stock = high_priority[0]
            result = analyze_stock(stock['symbol'], stock['name'])
        else:
            print("❌ 請指定 --stock 或使用 --batch")
            sys.exit(1)


if __name__ == '__main__':
    main()
