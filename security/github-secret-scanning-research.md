# GitHub Secret 掃描與爬蟲分析研究

> 狀態：待研究
> 優先級：中
> 建立日期：2026-02-01

## 研究目標

分析 GitHub public events 被惡意爬蟲利用的風險，以及哪些開源專案在短期內有密集更新可作為觀察對象。

## 背景：惡意爬蟲原理

### GitHub Events API

GitHub Events API 是完全公開的：
```
GET https://api.github.com/events
```

- 每次 push 都會出現在這個 feed 裡
- 爬蟲持續監聽 → 抓 commit diff → regex 匹配已知 token 格式
- Telegram Bot Token 格式固定：`數字:AA + Base64 字串`，非常容易匹配
- 從 token push 到被抓取，可能只有 **幾秒到幾分鐘**
- 即使 force push 清除歷史，舊 token 可能已被記錄

### 已知 token 格式（regex 特徵）

| 服務 | 格式 | Regex |
|------|------|-------|
| Telegram | `數字:AA...` | `\d{8,}:AA[A-Za-z0-9_-]{30,}` |
| OpenAI | `sk-...` | `sk-[A-Za-z0-9]{20,}` |
| Anthropic | `sk-ant-...` | `sk-ant-[A-Za-z0-9_-]{20,}` |
| Google/Gemini | `AIza...` | `AIza[A-Za-z0-9_-]{35}` |
| GitHub PAT | `ghp_...` | `ghp_[A-Za-z0-9]{36}` |
| AWS | `AKIA...` | `AKIA[A-Z0-9]{16}` |
| Stripe | `sk_live_...` | `(sk|pk)_(live|test)_[A-Za-z0-9]{20,}` |
| HuggingFace | `hf_...` | `hf_[A-Za-z0-9]{30,}` |

## 待研究項目

### 1. 分析密集更新的專案
- [ ] 用 GitHub Events API 找出短期內有大量 push 的 public repo
- [ ] 分析這些 repo 的 commit 中是否頻繁出現 secret 洩漏
- [ ] 找出哪些語言/框架的專案最容易洩漏（Python .env, Node .env, etc.）

### 2. 掃描工具對比
- [ ] truffleHog — entropy + regex 分析
- [ ] gitleaks — TOML 規則引擎
- [ ] git-secrets (AWS) — pattern-based
- [ ] GitHub Secret Scanning — 原生功能
- [ ] 比較各工具的偵測率和誤報率

### 3. 防禦架構設計
- [ ] pre-commit hook（已部署）的覆蓋率分析
- [ ] GitHub Actions CI 中加入 secret scanning
- [ ] GitHub push protection 設定
- [ ] 監控 GitHub Events API 中自己 org 的洩漏

### 4. 應急響應流程
- [ ] Token 洩漏後的標準處理 SOP
- [ ] 各服務的 token revoke 方式匯總
- [ ] 自動化撤銷腳本

## 參考資源

- [GitHub Events API](https://docs.github.com/en/rest/activity/events)
- [truffleHog](https://github.com/trufflesecurity/trufflehog)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- [GitHub Secret Scanning](https://docs.github.com/en/code-security/secret-scanning)
- [GitGuardian State of Secrets Sprawl](https://www.gitguardian.com/state-of-secrets-sprawl-on-github)

## 本機防禦措施（已部署）

### pre-commit hook
- 位置：`~/.git-templates/hooks/pre-commit`
- 部署機器：MacBook Pro, ac-mac, acmacmini2, ac-3090, ac-rpi5
- 覆蓋：Telegram, OpenAI, Anthropic, Google, GitHub, AWS, Slack, Stripe, Discord, HuggingFace, Private Key
- 新建 repo 自動套用（via `git config --global init.templateDir`）

### CLAUDE.md 安全規則
- 所有機器的 Claude Code 都已加入 token 防護指令
- Claude 在操作 git 時會遵守這些規則
