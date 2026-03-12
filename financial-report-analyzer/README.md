# 智能財報分析系統 📊

AI-powered 財報自動分析與投資建議生成系統

## 📋 專案概述

本系統自動抓取上市公司財報，使用 AI 分析財務指標，生成投資建議報告。

### 核心功能

1. **財報自動抓取** - 從公開資訊觀測站抓取財報 PDF/Excel
2. **財務指標分析** - 計算並分析關鍵財務比率
3. **AI 情緒分析** - 評估財報內容（利多/利空）
4. **自動報告生成** - 生成 PPT 投資建議報告
5. **異常警示** - 偵測財務異常訊號

---

## 🏗️ 系統架構

```
financial-report-analyzer/
├── scrapers/                 # 財報抓取模組
│   ├── twse_scraper.py      # 台股財報抓取
│   ├── sec_scraper.py       # 美股財報抓取
│   └── pdf_parser.py        # PDF 解析
├── analyzers/                # 分析模組
│   ├── financial_ratios.py  # 財務比率計算
│   ├── sentiment.py         # 情緒分析
│   └── anomaly_detection.py # 異常偵測
├── reporters/                # 報告生成
│   ├── pptx_generator.py    # PPT 報告
│   └── excel_export.py      # Excel 匯出
├── config/                   # 配置文件
│   ├── stocks.json          # 監控股票清單
│   └── thresholds.json      # 警示閾值
├── output/                   # 輸出目錄
│   ├── reports/             # 生成的報告
│   └── data/                # 原始數據
└── scripts/                  # 自動化腳本
    ├── run_analysis.py      # 執行分析
    └── schedule.sh          # 排程腳本
```

---

## 🔧 技術棧

| 模組 | 技術 | 說明 |
|------|------|------|
| 財報抓取 | Python + requests | 公開資訊觀測站 API |
| PDF 解析 | `openai-whisper` / PyPDF2 | 財報文字提取 |
| 數據分析 | Pandas + NumPy | 財務比率計算 |
| AI 分析 | OpenClaw + Qwen | 情緒分析、建議生成 |
| 報告生成 | `pptx` 技能 | PowerPoint 自動生成 |
| 數據儲存 | Excel / SQLite | 歷史數據儲存 |
| 排程 | cron / GitHub Actions | 定時執行 |

---

## 📊 分析指標

### 財務健全度
- 流動比率、速動比率
- 負債比率
- 利息保障倍數

### 獲利能力
- ROE（股東權益報酬率）
- ROA（總資產報酬率）
- 毛利率、淨利率

### 營運效率
- 存貨週轉率
- 應收帳款週轉率
- 總資產週轉率

### 現金流
- 營業現金流
- 自由現金流
- 現金再投資比率

### 估值指標
- P/E（本益比）
- P/B（股價淨值比）
- 股息殖利率

---

## 🚀 快速開始

### 1. 安裝依賴

```bash
cd financial-report-analyzer
pip install -r requirements.txt
```

### 2. 配置監控股票

編輯 `config/stocks.json`：

```json
{
  "tw_stocks": [
    {"symbol": "2330", "name": "台積電"},
    {"symbol": "2317", "name": "鴻海"},
    {"symbol": "2454", "name": "聯發科"}
  ],
  "us_stocks": [
    {"symbol": "AAPL", "name": "Apple"},
    {"symbol": "MSFT", "name": "Microsoft"}
  ]
}
```

### 3. 執行分析

```bash
python scripts/run_analysis.py --stock 2330 --quarter Q4-2025
```

### 4. 查看報告

報告輸出至 `output/reports/2330_2025Q4_analysis.pptx`

---

## 📈 使用範例

### 單一股票分析

```bash
python scripts/run_analysis.py --stock 2330
```

### 批量分析

```bash
python scripts/run_analysis.py --batch config/stocks.json
```

### 定時執行（每週一早上 8 點）

```bash
crontab -e
# 添加：
0 8 * * 1 cd /path/to/financial-report-analyzer && python scripts/run_analysis.py --batch config/stocks.json
```

---

## 🎯 輸出內容

### PPT 報告包含

1. **封面頁** - 股票名稱、分析日期
2. **公司概況** - 產業、主要產品
3. **財務摘要** - 關鍵數據總覽
4. **獲利能力分析** - ROE、毛利率趨勢
5. **財務健全度** - 負債比、流動性
6. **現金流分析** - 營業現金流、自由現金流
7. **估值分析** - P/E、P/B 歷史區間
8. **AI 投資建議** - 買入/持有/賣出
9. **風險提示** - 潛在風險因素

---

## ⚠️ 警示規則

### 紅燈警示（立即通知）
- 連續兩季營收衰退 > 20%
- 負債比率 > 70%
- 營業現金流轉負

### 黃燈警示（記錄追蹤）
- 單季營收衰退 > 10%
- 毛利率下滑 > 5 個百分點
- 存貨週轉天數增加 > 30 天

---

## 📝 待辦事項

- [ ] 實作台股財報抓取器
- [ ] 實作美股財報抓取器（SEC EDGAR）
- [ ] 財務比率計算模組
- [ ] AI 情緒分析整合
- [ ] PPT 報告模板設計
- [ ] 異常偵測演算法
- [ ] Discord 通知整合
- [ ] GitHub Actions 排程

---

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

---

## 📄 授權

MIT License

---

**Last Updated:** 2026-03-12
**Maintained by:** Zarvis Team
