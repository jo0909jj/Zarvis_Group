# Zarvis Group 📡

AI Assistant 協作與技能開發倉庫
Created by Joe Chiang

## 📖 關於 Zarvis

Zarvis 是一個基於 OpenClaw 框架的 AI 助手，具有以下特點：

- 🧠 **多模型支援** - 接入 Qwen、MiniMax、GLM、Kimi 等模型
- 🛠️ **豐富技能** - 文件處理、瀏覽器自動化、財經分析等
- 🔄 **自動化任務** - 持倉監控、新聞摘要、定期報告
- 💬 **多平台整合** - Discord、Telegram 等通訊平台

## 📁 倉庫結構

```
Zarvis_Group/
├── docs/                    # 文件
│   ├── setup.md            # 安裝指南
│   ├── skills.md           # 技能說明
│   └── config.md           # 配置說明
├── skills/                  # 自定義技能
├── scripts/                 # 自動化腳本
├── templates/               # 模板文件
└── workspace/               # 工作區配置
```

## 🚀 快速開始

### 安裝 OpenClaw

```bash
npm install -g openclaw
openclaw configure
```

### 配置技能

```bash
# 安裝財經相關技能
openclaw skills install weather
openclaw skills install healthcheck
```

### 啟動服務

```bash
openclaw gateway start
```

## 📊 已安裝技能

| 技能 | 用途 |
|------|------|
| `docx` | Word 文件處理 |
| `xlsx` | Excel 電子表格 |
| `pptx` | PowerPoint 簡報 |
| `playwright-mcp` | 瀏覽器自動化 |
| `weather` | 天氣查詢 |
| `healthcheck` | 系統安全審計 |

## 🔧 自動化任務

- **股市持倉監控** - 每 15 分鐘更新持倉狀態
- **財經新聞摘要** - 每 4 小時新聞分析
- **財經新聞分析** - 專家級市場解讀

## 📝 使用範例

### 生成財經報告

```bash
node create-gas-report.js
```

### 截取網頁截圖

```bash
xvfb-run -a google-chrome --no-sandbox --disable-gpu --headless \
  --screenshot=output.png --window-size=1920,1080 \
  https://example.com
```

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

## 📄 授權

MIT License

---

**Last Updated:** 2026-03-12
**Maintained by:** Zarvis Team
