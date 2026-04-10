---
title: "DesignClaw ComfyUI 整合架構"
date: 2026-04-04
category: tech/ai-ml
tags: [DesignClaw, ComfyUI, SDXL, ControlNet, Render-Agent, 室內設計, AI渲染]
type: plan
project: DesignClaw
priority: P1
status: draft
---

# DesignClaw ComfyUI 整合架構

## 摘要

DesignClaw 的 Render Agent 層已完成實作，透過 ComfyUI REST API + WebSocket 將 SDXL RealVisXL V5.0 整合進室內設計渲染流水線。支援 dual ControlNet（Canny 結構線 + Depth 空間感）與可選的 IP-Adapter 風格轉移，針對六種日式簡約空間類型各自調校 prompt 和參數。目標部署機器為 ac-3090（RTX 3090, 24GB VRAM）。

---

## 1. 完整架構：ComfyUI 整合到 DesignClaw Render Agent

```
DesignClaw Pipeline
───────────────────────────────────────────────────────────
平面圖輸入（JPG/PNG）
    │
    ▼
[Render Agent — render_agent.py]
    │  ├── 載入 workflow template (japanese_interior.json)
    │  ├── 載入 prompt config (japanese_minimalist.yaml)
    │  ├── 動態注入：正向 prompt、ControlNet 圖片路徑、KSampler 參數
    │  └── POST /prompt → ComfyUI API
    │
    ▼
[ComfyUI Server — localhost:8188]
    │
    ├── CheckpointLoaderSimple → RealVisXL_V5.0.safetensors
    ├── CLIPTextEncode (positive / negative)
    ├── CannyEdgePreprocessor → ControlNetApplyAdvanced (strength 0.65)
    ├── ZoeDepthMapPreprocessor → ControlNetApplyAdvanced (strength 0.45)
    ├── IP-Adapter (可選，預設關閉，weight 0.5)
    ├── KSampler (dpmpp_2m, karras, steps=30, cfg=7.0)
    ├── VAEDecode
    └── SaveImage → designclaw/<room_name>/
    │
    ▼
WebSocket /ws?clientId=<id>
    │  ├── type: progress → 顯示百分比
    │  ├── type: executing (node=null) → 完成信號
    │  └── type: execution_error → 錯誤處理
    │
    ▼
GET /history/<prompt_id> → 下載輸出圖片
    │
    ▼
test_outputs/renders/<filename>.png
```

---

## 2. 已建立的檔案清單與功能說明

| 檔案 | 位置 | 功能 |
|------|------|------|
| `render_agent.py` | `agents/` | 核心 Render Agent，封裝 ComfyUI API 呼叫、WebSocket 進度追蹤、workflow 動態組裝、重試邏輯 |
| `japanese_interior.json` | `workflows/` | ComfyUI workflow 定義，20 個節點，節點 ID 穩定（不變），供 render_agent 動態替換內容 |
| `japanese_minimalist.yaml` | `prompts/` | 六種房間的 prompt 模板，含 cfg_scale、steps、resolution、ControlNet strength 各自設定 |
| `setup-comfyui.sh` | `scripts/` | 六步驟一鍵安裝腳本：前置檢查 → Clone ComfyUI → 建 venv → 安裝套件 → 安裝 custom nodes → 下載模型 |
| `start-comfyui.sh` | `scripts/` | 啟動 ComfyUI server，--listen 0.0.0.0 支援 Tailscale 遠端，PORT 可由環境變數覆蓋 |
| `test-render.py` | `scripts/` | 三項 smoke test：API 連線、living room 單張渲染（seed=12345）、輸出目錄驗證 |

---

## 3. 技術選型

### 主模型
- **RealVisXL V5.0** (`RealVisXL_V5.0.safetensors`, ~6.5GB)
  - 基於 SDXL 1.0，針對超寫實攝影風格微調
  - 來源：HuggingFace `SG161222/RealVisXL_V5.0`
  - 選型理由：室內設計攝影質感優於 base SDXL，細節豐富，光影自然

### Dual ControlNet
| 類型 | 模型 | Strength | End% | 用途 |
|------|------|----------|------|------|
| Canny | `controlnet-canny-sdxl-1.0.safetensors` (~2.5GB) | 0.60-0.70 | 85% | 保留空間線條、傢具輪廓 |
| Depth (Zoe) | `controlnet-depth-sdxl-1.0.safetensors` (~2.5GB) | 0.40-0.50 | 75% | 保留空間深度感與層次 |

- Canny 先套用，Depth 串接在 Canny 輸出後（chained conditioning）
- Depth end% 較低（75%），讓後段生成自由發揮細節

### IP-Adapter（可選）
- **模型**: `ip-adapter-plus_sdxl_vit-h.safetensors` (~1.0GB)
- **CLIP Vision**: `clip-vit-h-14-laion2b-s32b-b79k.safetensors` (~3.5GB)
- **預設狀態**: disabled（`ipadapter.enabled: false`）
- **當啟用時**: weight=0.5, linear, end_at=0.8，提供風格參考圖遷移

### 硬體需求
- **目標**: ac-3090 (RTX 3090, 24GB VRAM)
- VRAM 估算：模型載入 ~14GB，推論峰值 ~18GB，24GB 足夠
- VAE: `sdxl_vae.safetensors`（fp16-fix 版，避免 NaN 問題）
- PyTorch CUDA 12.1 版本

### 採樣器
- **KSampler**: dpmpp_2m + karras scheduler
- Steps: 28-30（玄關走廊 28，其他 30）
- CFG: 7.0
- Denoise: 1.0（從零生成）

---

## 4. Workflow 節點組合（Node IDs 1-20）

```
ID  Label                    Class Type                  說明
─────────────────────────────────────────────────────────────────────
1   Checkpoint Loader        CheckpointLoaderSimple      載入 RealVisXL V5.0
2   VAE Loader               VAELoader                   載入 SDXL VAE fp16-fix
3   Positive Prompt          CLIPTextEncode              正向 prompt（render_agent 動態替換）
4   Negative Prompt          CLIPTextEncode              共用負向 prompt
5   Load Canny Image         LoadImage                   輸入圖（render_agent 替換路徑）
6   Canny Preprocessor       CannyEdgePreprocessor       low=100, high=200, res=1024
7   ControlNet Loader Canny  ControlNetLoader            Canny SDXL 模型
8   Apply ControlNet Canny   ControlNetApplyAdvanced     strength 0.65, end 85%
9   Load Depth Image         LoadImage                   深度圖（render_agent 替換路徑）
10  Depth Preprocessor       ZoeDepthMapPreprocessor     res=1024
11  ControlNet Loader Depth  ControlNetLoader            Depth SDXL 模型
12  Apply ControlNet Depth   ControlNetApplyAdvanced     strength 0.45, end 75%（串接 Canny 輸出）
13  Style Ref Image          LoadImage                   IP-Adapter 參考圖（可選）
14  CLIP Vision Loader       CLIPVisionLoader            ViT-H LAION-2B
15  IP-Adapter Loader        IPAdapterModelLoader        ip-adapter-plus_sdxl_vit-h
16  Apply IP-Adapter         IPAdapterAdvanced           weight 0.5, linear, end 0.8
17  Empty Latent Image       EmptyLatentImage            1024×1024（走廊為 1024×768）
18  KSampler                 KSampler                    dpmpp_2m, karras, steps=30, cfg=7.0
19  VAE Decode               VAEDecode                   latent → pixel
20  Save Image               SaveImage                   輸出到 designclaw/<room>/
```

**動態替換規則**（render_agent.py）：
- Node 3：注入正向 prompt 文字
- Node 4：注入負向 prompt 文字
- Node 5：替換 Canny 輸入圖路徑
- Node 9：替換 Depth 輸入圖路徑
- Node 13：替換 IP-Adapter 參考圖（若啟用）
- Node 16：設定 IP-Adapter weight
- Node 17：按房間設定 resolution
- Node 18：替換 seed、cfg、steps；model input 按 IP-Adapter 是否啟用切換（1,0 或 16,0）
- Node 20：設定輸出 prefix 為 `designclaw/<room_name>`

---

## 5. API 整合方式

### 提交 Workflow
```python
# POST /prompt
payload = {"prompt": workflow_dict, "client_id": "designclaw_12345"}
response = POST http://localhost:8188/prompt
# 回傳: {"prompt_id": "uuid-string"}
```

### WebSocket 進度監聽
```python
# 連線
ws = websockets.connect("ws://localhost:8188/ws?clientId=designclaw_12345")

# 訊息類型
{"type": "progress", "data": {"value": 15, "max": 30}}    # 50% 進度
{"type": "executing", "data": {"prompt_id": "...", "node": "18"}}  # 節點執行
{"type": "executing", "data": {"prompt_id": "...", "node": null}}  # 完成信號
{"type": "execution_error", "data": {"exception_message": "..."}}   # 錯誤
```

### 取得輸出圖片
```python
# 查詢歷史
GET /history/<prompt_id>
# 回傳 outputs[node_id].images[].{filename, subfolder}

# 下載圖片
GET /view?filename=xxx.png&subfolder=designclaw/living_room&type=output
```

### RenderAgent 使用範例
```python
from agents.render_agent import RenderAgent

agent = RenderAgent(api_url="http://100.108.119.78:8188")
agent.connect()

# 單房間渲染
result = agent.render_room(
    room_name="living_room",
    controlnet_image_path="test_inputs/small_openplan.jpg",
    depth_image_path="test_inputs/depth.png",  # 可選
    seed=12345,
)
# result: {"status": "success", "images": ["test_outputs/renders/xxx.png"], ...}

# 批次渲染（讀 floorplan_formal_design_v2.json）
results = agent.render_all_rooms()
```

**重試機制**: max_retries=3，Timeout 重試間隔 5s，其他錯誤 3s

---

## 6. 日式簡約風格 Prompt 策略

### 兩層式 Prompt 架構
```yaml
# 底層（全房間共用）
style_base: 攝影技術關鍵詞
  → interior design photography, wide angle lens, 8K ultra-detailed,
    photorealistic, depth of field, golden hour ambience

style_japanese: 風格關鍵詞
  → wabi-sabi aesthetic, muted earth tones, natural materials,
    hinoki cypress wood, shoji paper screens, handmade ceramics,
    ikebana, shadow and light interplay

# 上層（房間專屬）
rooms.<room>: 空間具體描述
  → 具體傢具、材質、光線、視角（主臥: tatami + tokonoma alcove...）
```

### 負向 Prompt（共用）
排除：過飽和色彩、現代西式傢具、地毯、雜亂、卡通/3D artifacts、水印

### 各房間 ControlNet 調校邏輯
| 房間 | Canny | Depth | 設計考量 |
|------|-------|-------|---------|
| 主臥室 | 0.65 | 0.45 | 標準，保留床架線條 |
| 書房 | 0.60 | 0.40 | 書桌輪廓，略降結構控制增加木紋感 |
| 客廳 | 0.60 | 0.50 | 開放空間，提高 depth 保持空間感 |
| 廚房 | 0.65 | 0.40 | 乾淨線條，強 canny 保留櫃體邊緣 |
| 陽台 | 0.55 | 0.45 | 最低 canny，保留自然感不過硬 |
| 走廊玄關 | 0.70 | 0.40 | 最強 canny，窄空間需精確線條；1024×768 橫向 |

---

## 7. 安裝和使用流程

### 一鍵安裝（ac-3090）
```bash
# 1. 複製 scripts 到 ac-3090
scp -r ~/Desktop/designclaw/scripts/ ac-3090:~/designclaw/scripts/

# 2. 執行安裝（約 20-40 分鐘，取決於網速）
ssh ac-3090 "bash ~/designclaw/scripts/setup-comfyui.sh"
# 安裝內容：
# - ComfyUI → ~/comfyui/
# - Python venv + PyTorch CUDA 12.1
# - Custom nodes: Manager, ControlNet aux, IP-Adapter plus,
#                 Impact Pack, Comfyroll, efficiency-nodes, TiledDiffusion
# - Models: RealVisXL V5.0, SDXL VAE, Canny/Depth ControlNet,
#            IP-Adapter Plus, CLIP Vision ViT-H, Interior LoRA
```

### 啟動 ComfyUI
```bash
# 本地
bash scripts/start-comfyui.sh

# ac-3090 遠端（Tailscale）
ssh ac-3090 "bash ~/designclaw/scripts/start-comfyui.sh"
# → http://100.108.119.78:8188
```

### 測試驗證
```bash
# 確認 API 可連、執行 living room 渲染、確認輸出目錄
python scripts/test-render.py
```

### 遠端呼叫 RenderAgent
```python
agent = RenderAgent(api_url="http://100.108.119.78:8188")
```

---

## 8. 下一步行動項目

- [ ] **部署安裝腳本到 ac-3090**：`scp` 整個 designclaw/ 目錄，執行 `setup-comfyui.sh`，確認所有模型下載完成
- [ ] **執行 smoke test**：`python scripts/test-render.py`，驗證 living room 渲染成功（seed=12345）
- [ ] **準備測試輸入圖**：將平面圖存為 `test_inputs/small_openplan.jpg`，確認 Canny 前處理輸出正確
- [ ] **IP-Adapter 測試**：準備一張日式室內風格參考圖，設定 `ipadapter.enabled: true`，比較有無 IP-Adapter 的差異
- [ ] **批次渲染驗證**：確認 `render_all_rooms()` 能正確讀取 `floorplan_formal_design_v2.json` 並逐一渲染六種房間
- [ ] **整合上游 Pipeline**：確認從平面圖分析階段輸出的 room type 與 `japanese_minimalist.yaml` 中的 key 對應（如 `living_room`, `master_bedroom`）
- [ ] **評估 LoRA 效果**：測試 `interior_3d_xl.safetensors` 是否提升室內設計細節，必要時換成更適合的 LoRA
- [ ] **WebUI 確認**：在 ComfyUI WebUI（port 8188）手動跑一次 `japanese_interior.json`，確認節點連線正確
