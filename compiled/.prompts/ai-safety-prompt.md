# 任務：編譯「AI 安全與合規」知識 Wiki 頁

你是 SecondBrain 知識編譯器。以下是「AI 安全與合規」主題下的 1 篇筆記摘要。
主題描述：AI 安全、模型對齊、jailbreak、資安、開源風險

## 要求

請根據以下筆記內容，產出一篇結構化的知識 Wiki 頁，格式如下：

```
---
title: "AI 安全與合規 — 知識 Wiki"
date: 2026-04-10
type: wiki
content_layer: L3
topic: ai-safety
source_count: 1
last_compiled: 2026-04-10
_skip_sync: true
---

# {主題名稱} — 知識 Wiki

## 主題概述
(2-3 段，概括此主題的核心範圍、為何重要、目前發展階段)

## 核心概念
(列出 5-10 個核心概念，每個用 ### 小節，2-3 句說明 + Wiki Link 引用來源筆記)

## 關鍵發現
(從筆記中提煉的重要洞見，每條用 > blockquote + 來源 Wiki Link)

## 跨筆記關聯
(不同筆記之間的連結、矛盾、演進關係)

## 待探索方向
(筆記中提到但尚未深入的議題，供未來研究)
```

## 引用規則

- 每個段落都必須用 `[[note-filename]]` 或 `[[note-filename|顯示名稱]]` Wiki Link 引用來源筆記
- filename 就是下方每篇筆記的 `filename` 欄位（不含 .md）
- 不要虛構不存在的筆記名稱

---

## 筆記清單（共 1 篇）

### [1/1] CC-BOS 論文深度分析 — 文言文越獄攻擊
- **filename**: `2026-03-30_CC-BOS論文分析`
- **path**: `dispatch-outputs/2026-03-30_CC-BOS論文分析.md`
- **date**: 2026-03-30
- **category**: research
- **tags**: LLM安全, jailbreak, 文言文, ICLR2026, 對齊

**內容摘要：**

# CC-BOS 論文深度分析

**論文標題：** Obscure but Effective: Classical Chinese Jailbreak Prompt Optimization via Bio-Inspired Search
**發表：** ICLR 2026
**arXiv：** 2602.22983
**機構：** 南洋理工大學、阿里巴巴等 9 家機構

---

## 一、研究核心問題

現有 LLM 的安全對齊（safety alignment）主要以現代語言進行訓練，英文為主，中文也以白話文為主。古典中文（文言文）因語法結構、語義壓縮方式與現代語言截然不同，可能構成安全過濾器的盲區。本研究試圖系統性驗證並利用這個盲區。

## 二、方法論：CC-BOS 框架

CC-BOS 的全名是 Classical Chinese Bio-inspired Optimization Search，核心架構包含三層：

### 2.1 文言文語言層
利用古典中文的語言特性作為基礎混淆手段。文言文的特點包括：一字多義（同一字可為名詞、動詞、形容詞）、省略主語、大量隱喻與典故
(...截斷)

---
