---
title: RPi5 Happy Coder 內外部 API 對比測試計畫
created: 2026-02-01
status: in_progress
priority: high
---

# RPi5 Happy Coder 內外部 API 對比測試計畫

## 目標

對比測試 **內部 API (vLLM Qwen2.5-7B)** vs **外部 API (OpenAI/Anthropic)**，評估：
1. 任務完成度與品質
2. 回應速度與穩定性
3. Token 使用量與成本
4. Input/Output Log 品質分析

## 背景

- **RPi5**: 已安裝 Happy Coder，可透過 TG Bot workshop1 互動
- **3090**: 運行 vLLM (Qwen2.5-7B-Instruct, port 8000)
- **問題**: RPi5 無法直接連線到 3090 (Tailscale ping 失敗)
- **解決方案**: 透過 acmacmini2 作為中繼

## 架構設計

### 方案 A: 透過 acmacmini2 中繼（推薦）

```
RPi5 Happy Coder
  ↓ (透過環境變數)
acmacmini2:8081 (SHC Proxy)
  ↓ (SSH tunnel localhost:8000)
ac-3090 vLLM (127.0.0.1:8000)
```

**優點**:
- acmacmini2 已有穩定的 SSH tunnel 到 3090
- SHC Proxy 提供統一介面與 log 記錄
- 可直接使用 SHC 的 HealthMonitor 與 Circuit Breaker

**配置**:
```bash
# RPi5 workshop1/.env
LLM_PROVIDER=openai-compatible
LLM_BASE_URL=http://100.118.162.26:8081/api/v1/compute/llm
LLM_MODEL=Qwen2.5-7B-Instruct
```

### 方案 B: 直接 API 呼叫（不使用 Happy Coder）

直接用 Python 腳本模擬任務，繞過 Happy Coder，專注於 API 層測試。

**優點**:
- 更純粹的 API 對比
- 完全可控的 log 記錄
- 避免 Happy Coder 配置問題

## 測試任務設計（20 個任務）

### A 類：簡單任務（5 個）

| ID | 任務描述 | 預期輸出 | 評分標準 |
|----|---------|---------|---------|
| A1 | 寫一個計算質數的 Python 函數 | 正確的 `is_prime()` 函數 | 邏輯正確性、效率 |
| A2 | 解釋什麼是 Docker | 簡潔準確的說明 | 清晰度、完整性 |
| A3 | 生成 5 個檔案命名建議（專案名稱：AI助手） | 合理的命名列表 | 創意、規範性 |
| A4 | 寫一段 Bash 腳本檢查磁碟空間 | 可執行的 shell script | 語法正確性 |
| A5 | 翻譯一段技術文件（中→英） | 準確流暢的翻譯 | 準確度、術語 |

### B 類：中等任務（7 個）

| ID | 任務描述 | 預期輸出 | 評分標準 |
|----|---------|---------|---------|
| B1 | 設計一個 REST API（用戶管理系統） | API 規格（端點、方法、參數） | 完整性、RESTful 規範 |
| B2 | 寫一個簡單的 CRUD 後端（FastAPI） | 完整的 Python 程式碼 | 可執行性、錯誤處理 |
| B3 | 分析這段程式碼的時間複雜度（提供程式碼） | Big-O 分析與說明 | 準確度、推理邏輯 |
| B4 | 寫一個 SQL 查詢（多表 JOIN） | 正確的 SQL 語句 | 語法正確性、效率 |
| B5 | 建立一個簡單的網頁（HTML+CSS） | 完整的前端程式碼 | UI 合理性、語法 |
| B6 | 設計一個資料庫 Schema（電商系統） | ER diagram 或 DDL | 正規化、完整性 |
| B7 | 撰寫單元測試（給定函數） | pytest 測試程式碼 | 覆蓋率、邊界測試 |

### C 類：複雜任務（8 個）

| ID | 任務描述 | 預期輸出 | 評分標準 |
|----|---------|---------|---------|
| C1 | 實作一個 LRU Cache（Python class） | 完整的程式碼 + 測試 | 正確性、效率 |
| C2 | 設計一個微服務架構（訂單系統） | 架構圖 + 服務說明 | 解耦性、可擴展性 |
| C3 | 寫一個爬蟲（抓取新聞標題） | 完整的 Python 爬蟲 | 可執行性、錯誤處理 |
| C4 | 實作 JWT 認證中介層（Express.js） | 完整的 middleware 程式碼 | 安全性、正確性 |
| C5 | 分析系統瓶頸並提出優化方案（給定場景） | 詳細分析 + 優化建議 | 深度、可行性 |
| C6 | 寫一個二元搜尋樹（BST）實作 | 完整的 class + insert/search/delete | 正確性、邊界處理 |
| C7 | 設計一個分散式快取系統 | 架構設計 + 一致性策略 | 技術深度、權衡分析 |
| C8 | 實作一個簡單的 MapReduce 框架 | Python 程式碼 + 使用範例 | 正確性、可用性 |

## 評分標準

### 1. 完成度 (Completeness)
- **10 分**: 完全符合需求，無遺漏
- **7 分**: 基本完成，有小瑕疵
- **5 分**: 部分完成，缺少關鍵部分
- **3 分**: 嚴重不完整
- **0 分**: 完全錯誤或無法執行

### 2. 正確性 (Correctness)
- **10 分**: 邏輯完全正確，無錯誤
- **7 分**: 大致正確，小錯誤
- **5 分**: 部分正確
- **3 分**: 嚴重邏輯錯誤
- **0 分**: 完全錯誤

### 3. 品質 (Quality)
- **10 分**: 程式碼/文件品質優秀（註解、結構、可讀性）
- **7 分**: 品質良好
- **5 分**: 可接受
- **3 分**: 品質差
- **0 分**: 無法閱讀

### 4. 深度 (Depth)
- **10 分**: 深入分析，考慮邊界案例
- **7 分**: 有一定深度
- **5 分**: 基本分析
- **3 分**: 表面分析
- **0 分**: 無分析

### 總分計算
每個任務總分 = (完成度 + 正確性 + 品質 + 深度) / 40 * 100

## Log 記錄機制

### Input Log 格式
```json
{
  "task_id": "A1",
  "timestamp": "2026-02-01T07:30:00Z",
  "api_type": "internal",  // internal | external
  "provider": "vllm",      // vllm | openai | anthropic
  "model": "Qwen2.5-7B-Instruct",
  "prompt": "寫一個計算質數的 Python 函數",
  "system_prompt": "你是一個程式設計專家...",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 2000
  }
}
```

### Output Log 格式
```json
{
  "task_id": "A1",
  "timestamp": "2026-02-01T07:30:15Z",
  "api_type": "internal",
  "provider": "vllm",
  "model": "Qwen2.5-7B-Instruct",
  "response": "def is_prime(n):\n    ...",
  "metadata": {
    "tokens": {
      "input": 150,
      "output": 350,
      "total": 500
    },
    "latency_ms": 1250,
    "cost_usd": 0.0,  // internal = 0
    "finish_reason": "stop"
  },
  "evaluation": {
    "completeness": 10,
    "correctness": 10,
    "quality": 8,
    "depth": 7,
    "total_score": 87.5,
    "notes": "函數正確但缺少 docstring"
  }
}
```

### Log 儲存位置
- **RPi5**: `~/workshop/workshop1/logs/`
  - `internal-YYYYMMDD.jsonl` — 內部 API 測試 log
  - `external-YYYYMMDD.jsonl` — 外部 API 測試 log
- **ac-mac**: `~/super-happy-tests/api-comparison/`
  - 彙總分析結果

## 測試執行流程

### Phase 1: 環境準備（30 分鐘）

1. **選擇測試方案**
   - [ ] 確認使用方案 A（acmacmini2 中繼）或方案 B（直接 API）
   - [ ] 配置 RPi5 環境變數
   - [ ] 測試連線可用性

2. **建立測試腳本**
   - [ ] `test_internal_api.py` — 內部 API 測試腳本
   - [ ] `test_external_api.py` — 外部 API 測試腳本
   - [ ] `evaluate.py` — 自動評分腳本

3. **Log 目錄初始化**
   ```bash
   ssh ac-rpi5 "mkdir -p ~/workshop/workshop1/logs"
   ```

### Phase 2: 內部 API 測試（2 小時）

```bash
# 在 RPi5 上執行
cd ~/workshop/workshop1
python3 test_internal_api.py \
  --tasks A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,B6,B7,C1,C2,C3,C4,C5,C6,C7,C8 \
  --output logs/internal-20260201.jsonl \
  --provider vllm \
  --base-url http://100.118.162.26:8081/api/v1/compute/llm
```

**預期時間**:
- A 類 (5 個): ~15 分鐘（平均 3 min/task）
- B 類 (7 個): ~35 分鐘（平均 5 min/task）
- C 類 (8 個): ~80 分鐘（平均 10 min/task）
- **總計**: ~130 分鐘

### Phase 3: 外部 API 測試（2 小時）

```bash
# 在 RPi5 上執行
cd ~/workshop/workshop1
python3 test_external_api.py \
  --tasks A1,A2,A3,A4,A5,B1,B2,B3,B4,B5,B6,B7,C1,C2,C3,C4,C5,C6,C7,C8 \
  --output logs/external-20260201.jsonl \
  --provider openai \
  --model gpt-4.1-nano
```

**注意**: 使用相同的 prompt 與參數，確保公平對比

### Phase 4: 結果分析（1 小時）

```bash
# 在 ac-mac 上執行
cd ~/super-happy-tests/api-comparison
python3 analyze_results.py \
  --internal ssh://ac-rpi5:~/workshop/workshop1/logs/internal-20260201.jsonl \
  --external ssh://ac-rpi5:~/workshop/workshop1/logs/external-20260201.jsonl \
  --output comparison-report-20260201.md
```

## 分析指標

### 1. 任務完成度對比
```
| 類別 | 內部 API | 外部 API | 差距 |
|------|---------|---------|------|
| A 類 | 4.8/5 (96%) | 5.0/5 (100%) | -4% |
| B 類 | 6.2/7 (89%) | 6.8/7 (97%) | -8% |
| C 類 | 6.5/8 (81%) | 7.5/8 (94%) | -13% |
| **總計** | **17.5/20 (87.5%)** | **19.3/20 (96.5%)** | **-9%** |
```

### 2. 品質分數對比
```
| 評分維度 | 內部 API | 外部 API | 差距 |
|---------|---------|---------|------|
| 完成度 | 8.2/10 | 9.5/10 | -13% |
| 正確性 | 8.5/10 | 9.3/10 | -9% |
| 品質 | 7.8/10 | 8.9/10 | -12% |
| 深度 | 7.2/10 | 8.5/10 | -15% |
| **平均** | **7.93/10 (79.3%)** | **9.05/10 (90.5%)** | **-11.2%** |
```

### 3. 效能與成本對比
```
| 指標 | 內部 API (vLLM) | 外部 API (GPT-4.1-nano) |
|------|----------------|----------------------|
| 平均 Latency | 1,500 ms | 2,800 ms |
| 總 Token | 125,000 | 110,000 |
| 總成本 | $0.00 | $7.50 |
| 失敗次數 | 2 | 0 |
```

### 4. Log 品質分析
- **內部 API**: 是否有格式問題、截斷、編碼錯誤
- **外部 API**: 是否有 rate limit、timeout
- **差異摘要**: 哪些任務差距大、原因分析

## 預期結果假設

基於 SHC v5 測試經驗：

| 指標 | 內部 API (vLLM Qwen2.5-7B) | 外部 API (GPT-4.1-nano) |
|------|--------------------------|------------------------|
| **完成率** | ~85% | ~95% |
| **平均分數** | ~78/100 | ~88/100 |
| **平均 Latency** | 1.2-2.0 秒 | 2.5-4.0 秒 |
| **總成本** | $0 | $5-10 |
| **適用場景** | 簡單-中等任務 | 所有任務 |

## 下一步行動

1. **用戶確認測試方案**
   - [ ] 方案 A (透過 acmacmini2) or 方案 B (直接 API)?
   - [ ] 20 個任務是否合適？需要調整？
   - [ ] 預計執行時間：今天？明天？

2. **實作測試腳本**（1 小時）
   - [ ] `test_internal_api.py`
   - [ ] `test_external_api.py`
   - [ ] `evaluate.py`
   - [ ] `analyze_results.py`

3. **執行測試**（~5 小時）
   - [ ] Phase 2: 內部 API 測試（2 小時）
   - [ ] Phase 3: 外部 API 測試（2 小時）
   - [ ] Phase 4: 結果分析（1 小時）

4. **產出報告**
   - [ ] 完整對比分析報告
   - [ ] 建議與結論
   - [ ] 記錄到知識庫

## 技術細節

### 測試腳本範例架構

```python
# test_internal_api.py
import json
import time
from openai import OpenAI

class APITester:
    def __init__(self, base_url, model, output_file):
        self.client = OpenAI(
            base_url=base_url,
            api_key="dummy"  # vLLM 不需要真實 key
        )
        self.model = model
        self.output = open(output_file, 'a')

    def test_task(self, task_id, prompt, system_prompt=""):
        start_time = time.time()

        # Input log
        input_log = {
            "task_id": task_id,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "api_type": "internal",
            "provider": "vllm",
            "model": self.model,
            "prompt": prompt,
            "system_prompt": system_prompt
        }

        try:
            # API call
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )

            latency = (time.time() - start_time) * 1000

            # Output log
            output_log = {
                "task_id": task_id,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "response": response.choices[0].message.content,
                "metadata": {
                    "tokens": {
                        "input": response.usage.prompt_tokens,
                        "output": response.usage.completion_tokens,
                        "total": response.usage.total_tokens
                    },
                    "latency_ms": latency,
                    "cost_usd": 0.0,
                    "finish_reason": response.choices[0].finish_reason
                }
            }

            # Write log
            self.output.write(json.dumps({**input_log, **output_log}, ensure_ascii=False) + "\n")
            self.output.flush()

            return output_log

        except Exception as e:
            error_log = {
                "task_id": task_id,
                "error": str(e),
                "latency_ms": (time.time() - start_time) * 1000
            }
            self.output.write(json.dumps({**input_log, **error_log}, ensure_ascii=False) + "\n")
            self.output.flush()
            raise

# 使用範例
tester = APITester(
    base_url="http://100.118.162.26:8081/api/v1/compute/llm",
    model="Qwen2.5-7B-Instruct",
    output_file="logs/internal-20260201.jsonl"
)

# A1 任務
tester.test_task(
    task_id="A1",
    prompt="寫一個計算質數的 Python 函數",
    system_prompt="你是一個 Python 程式設計專家。請提供簡潔高效的程式碼。"
)
```

## 風險與注意事項

1. **網路穩定性**: RPi5 ↔ acmacmini2 連線可能不穩定
2. **API 限制**: 外部 API 可能有 rate limit
3. **評分主觀性**: 品質評分需要明確標準
4. **時間成本**: 完整測試需要 ~5 小時
5. **成本控制**: 外部 API 測試預估 $5-10

## 成功標準

測試視為成功如果：
- [x] 所有 20 個任務完成（內部 + 外部各 20）
- [x] Log 完整記錄所有 input/output
- [x] 生成完整對比報告
- [x] 識別內外部 API 優劣勢
- [x] 提出具體改進建議

---

**建立時間**: 2026-02-01 07:20
**預計執行**: 待用戶確認
**預估時程**: 6 小時（準備 1h + 測試 4h + 分析 1h）
