# OpenClaw 安裝指南

## 系統需求

- Node.js v20+
- npm v8+
- Linux/macOS/WSL2

## 安裝步驟

### 1. 安裝 OpenClaw

```bash
npm install -g openclaw
```

### 2. 初始配置

```bash
openclaw configure
```

跟隨向導完成：
- 模型配置（推薦使用 Bailian/Qwen）
- 頻道配置（Discord/Telegram）
- Gateway 設置

### 3. 啟動 Gateway

```bash
openclaw gateway start
```

### 4. 驗證安裝

```bash
openclaw status
```

## 技能安裝

### 內建技能

以下技能已內建於 OpenClaw：

```bash
# 無需額外安裝，配置後即可使用
- discord
- healthcheck  
- skill-creator
- tmux
- video-frames
- weather
```

### 外部技能

```bash
# 從 ClawHub 安裝
openclaw skills install <skill-name>

# 或手動複製到 skills 目錄
cp -r /path/to/skill ~/.openclaw/workspace/skills/
```

### 已安裝技能清單

| 技能 | 位置 | 說明 |
|------|------|------|
| `docx` | `~/.openclaw/workspace/skills/docx` | Word 文件處理 |
| `xlsx` | `~/.openclaw/workspace/skills/xlsx` | Excel 電子表格 |
| `anthropic-pptx` | `~/.openclaw/workspace/skills/anthropic-pptx` | PowerPoint 簡報 |
| `playwright-mcp` | `~/.openclaw/workspace/skills/playwright-mcp` | 瀏覽器自動化 |
| `nano-banana-pro` | `~/.openclaw/workspace/skills/nano-banana-pro` | Gemini 圖像生成 |
| `markdown-converter` | `~/.openclaw/workspace/skills/markdown-converter` | 文件轉換 |

## 瀏覽器配置（WSL2）

### 使用 xvfb 運行 Chrome

```bash
# 安裝 xvfb
sudo apt-get install xvfb

# 測試 Chrome
xvfb-run -a google-chrome --no-sandbox --disable-gpu --headless \
  --screenshot=test.png https://example.com
```

### 配置 OpenClaw Browser

編輯 `~/.openclaw/openclaw.json`：

```json
{
  "browser": {
    "noSandbox": true
  }
}
```

重啟 Gateway：

```bash
openclaw gateway restart
```

## 常見問題

### Gateway 無法啟動

```bash
# 檢查配置
openclaw doctor

# 修復配置
openclaw doctor --fix
```

### 技能無法載入

```bash
# 檢查技能目錄
ls -la ~/.openclaw/workspace/skills/

# 確認 SKILL.md 存在
cat ~/.openclaw/workspace/skills/<skill>/SKILL.md
```

### 瀏覽器錯誤

WSL2 環境需要 xvfb：

```bash
# 確認 xvfb 已安裝
which xvfb-run

# 測試 Chrome
xvfb-run -a google-chrome --version
```

## 下一步

- 查看 [skills.md](skills.md) 了解技能使用
- 查看 [config.md](config.md) 了解配置選項
- 訪問 [OpenClaw 文檔](https://docs.openclaw.ai)

---

**Last Updated:** 2026-03-12
