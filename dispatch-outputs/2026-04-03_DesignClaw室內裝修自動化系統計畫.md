---
title: DesignClaw — AI 室內裝修全自動管線系統計畫
date: 2026-04-03
category: tech/ai-ml
tags: [DesignClaw, 室內設計, OpenCode, MetaClaw, 多代理, BIM, IFC, 自動化管線, AI-Agent]
type: plan
source: AI Interior Design Collaboration Pipeline 規格書 + MetaClaw 架構 + OpenCode Agent
project: AI工具實戰
priority: P1
status: draft
---

# DesignClaw — AI 室內裝修全自動管線系統計畫

## 一、系統定位

DesignClaw 是一套以 OpenCode Agent 為底層運行時、參考 MetaClaw 自進化架構設計的 AI 室內裝修全自動協作管線。每個設計環節由專屬 Agent 負責，Agent 之間透過事件驅動的訊息系統串接，形成從「手繪草稿」到「施工交付」的端對端自動化流程。

核心理念：**把 MetaClaw 的「Claw」（抓取 → 學習 → 進化）模式套用到室內設計產業的每一個環節。**

---

## 二、架構總覽

### 2.1 三層架構

```
┌─────────────────────────────────────────────────────────┐
│                    Layer 3: 業務層                        │
│  Notion（專案 UI）+ Google Drive（檔案倉庫）+ Web 檢視器   │
└────────────────────────┬────────────────────────────────┘
                         │ API / Webhook
┌────────────────────────┴────────────────────────────────┐
│                    Layer 2: Agent 管線層                   │
│                                                          │
│  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐  ┌──────┐      │
│  │Vision│→│Layout│→│Model │→│Render│→│Export│      │
│  │Agent │  │Agent │  │Agent │  │Agent │  │Agent │      │
│  └──────┘  └──────┘  └──────┘  └──────┘  └──────┘      │
│       ↑                                      ↓           │
│  ┌──────┐                              ┌──────┐         │
│  │Intake│                              │Deliver│         │
│  │Agent │                              │Agent  │         │
│  └──────┘                              └──────┘         │
│                                                          │
│  ┌────────────────────────────────────────────────┐      │
│  │         Orchestrator（任務排程 + 狀態機）         │      │
│  └────────────────────────────────────────────────┘      │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────┴────────────────────────────────┐
│                    Layer 1: 運行時基礎層                   │
│                                                          │
│  OpenCode Agent Runtime                                  │
│  ├── Multi-Agent 事件驅動通訊（peer-to-peer messaging）    │
│  ├── MCP Server 整合（Notion / GDrive / 自訂工具）        │
│  ├── 多模型支援（Claude / GPT / Gemini / 本地模型）        │
│  ├── Session 持久化（SQLite）                             │
│  └── 權限控制 + 工具呼叫審核                               │
│                                                          │
│  MetaClaw 進化層（可選）                                   │
│  ├── 透明代理 Proxy                                       │
│  ├── Skill 自動提取與注入                                  │
│  └── OMLS 閒置時訓練排程                                   │
└─────────────────────────────────────────────────────────┘
```

### 2.2 借鑑 MetaClaw 的設計模式

| MetaClaw 概念 | DesignClaw 對應 | 說明 |
|--------------|-----------------|------|
| 透明代理 Proxy | Orchestrator | 攔截所有 Agent 通訊，記錄決策軌跡，統一路由 |
| OMLS 閒置排程 | 渲染排程器 | 監控系統資源，在設計師不使用時自動啟動批次渲染 |
| Skill 自動提取 | 設計經驗庫 | 從每次專案中提取「什麼樣的空間配置客戶滿意度高」的 pattern |
| 雙軌學習（快/慢） | 快：Prompt 模板迭代 / 慢：Fine-tune 辨識模型 | 快車道即時更新 Agent prompt，慢車道離線微調 Vision 模型 |
| PRM 過程獎勵 | 設計評審 Agent | 每個環節輸出都經過自動品質評分再進入下一步 |

---

## 三、七個專屬 Agent 詳細設計

### Agent 0: Intake Agent（案件接收）

```
觸發：客戶提交設計需求（Notion form / Email / LINE）
輸入：需求文字、參考圖片、現場照片、平面圖掃描
輸出：標準化專案 Brief（JSON）
```

**職責：**
- 解析客戶需求（NLP 提取：空間類型、坪數、預算、風格偏好）
- 自動建立 Notion 專案頁面（透過 MCP → Notion API）
- 在 Google Drive 建立專案資料夾結構（Source / Delivery / Construction）
- 生成標準化 `project_brief.json`，觸發下一步

**工具鏈：**
- LLM：Claude Sonnet（結構化輸出）
- MCP：Notion MCP + Google Drive MCP
- 自訂工具：brief_parser（JSON schema 驗證）

**自動化腳本範例：**
```python
# intake_agent/tools/brief_parser.py
def parse_brief(raw_input: dict) -> ProjectBrief:
    """從客戶原始輸入提取結構化 Brief"""
    return ProjectBrief(
        space_type=extract_space_type(raw_input["description"]),
        area_sqm=extract_area(raw_input["description"]),
        budget_range=extract_budget(raw_input["description"]),
        style_keywords=extract_style(raw_input["images"]),
        room_requirements=extract_rooms(raw_input["description"]),
        constraints=extract_constraints(raw_input["description"])
    )
```

---

### Agent 1: Vision Agent（AI 視覺辨識）

```
觸發：project_brief.json 就緒 + 平面圖/草稿上傳
輸入：手繪草稿 / 現場照片 / 既有平面圖 PDF
輸出：結構化 floorplan.json（房間、牆體、門窗、尺寸）
```

**職責：**
- 圖片前處理（去噪、矯正透視、增強對比）
- 呼叫 TF2DeepFloorplan 辨識牆體和房間分割
- 用 Claude Vision 做二次校驗（比對辨識結果與原圖）
- 輸出標準化 JSON，包含每個房間的座標、類型、面積

**工具鏈：**
- 模型：TF2DeepFloorplan（自架 Flask API Docker）
- 校驗：Claude Haiku Vision
- 圖像處理：OpenCV（Python 工具）
- 輸出格式：react-planner 相容 JSON schema

**品質關卡：**
- 辨識信心分數 < 0.7 的房間 → 標記為「需人工確認」
- 面積偏差 > 10% → 觸發重新辨識或人工校正流程
- 結果自動推送到 Notion 專案頁供設計師審核

---

### Agent 2: Layout Agent（2D 平面配置）

```
觸發：floorplan.json 通過品質關卡
輸入：floorplan.json + project_brief.json（風格/需求）
輸出：layout.json（含家具配置、動線規劃）
```

**職責：**
- 載入 floorplan.json 到 react-planner（Web 介面或 headless）
- 根據 Brief 中的需求，用 AI 建議家具配置方案
- 呼叫 HouseDiffusion / Graph2plan 生成多個佈局候選
- 設計師在 react-planner Web UI 中選擇/調整
- 確認後輸出 layout.json

**工具鏈：**
- 編輯器：react-planner（fork：work-vv/react-planner）
- AI 佈局：HouseDiffusion API（自架）
- LLM：Claude Sonnet（佈局推薦邏輯）
- 人機介面：react-planner Web UI（設計師介入點）

**人機協作設計：**
```
AI 生成 3 個佈局方案
    → 推送到 react-planner Web UI
    → 設計師選擇 / 手動調整
    → 確認 → layout.json 鎖定
    → 自動進入下一步
```

---

### Agent 3: Model Agent（3D 建模）

```
觸發：layout.json 鎖定
輸入：layout.json + 材質偏好 + 家具庫
輸出：3D 模型檔（.FCStd / .blend）+ .ifc
```

**職責：**
- 將 layout.json 轉換為 FreeCAD Python 腳本（headless）
- 自動建立牆體、門窗、地板的 3D 幾何
- 從家具庫（parametric library）載入家具模型並放置
- 透過 IfcOpenShell 匯出 IFC 格式
- 用 Bonsai BIM（Blender addon）做 BIM 整合

**工具鏈：**
- 3D 引擎：FreeCAD（headless Python API）
- BIM：IfcOpenShell + Bonsai BIM
- 家具庫：自建 parametric 家具 JSON 定義 + FreeCAD macro
- 格式轉換：IfcOpenShell（IFC 匯出）、Blender（GLB 匯出）

**自動化腳本框架：**
```python
# model_agent/tools/layout_to_3d.py
import FreeCAD, Part, Arch

def build_3d_from_layout(layout_json: dict):
    """從 layout.json 自動生成 3D 模型"""
    doc = FreeCAD.newDocument("InteriorDesign")

    for wall in layout_json["walls"]:
        Arch.makeWall(
            length=wall["length"],
            height=wall["height"],
            width=wall["thickness"]
        )

    for room in layout_json["rooms"]:
        place_furniture(doc, room["furniture"], room["bounds"])

    # 匯出 IFC
    import ifcopenshell
    export_to_ifc(doc, "output.ifc")

    # 匯出 GLB（via Blender headless）
    export_to_glb(doc, "output.glb")
```

---

### Agent 4: Render Agent（渲染）

```
觸發：3D 模型通過品質檢查
輸入：.blend 檔 + 材質設定 + 燈光方案
輸出：渲染圖（.png / .jpg）+ 360 全景
```

**職責：**
- 載入 Blender 場景，套用材質和燈光
- Blender + Cycles 批次渲染（headless，支援 GPU 加速）
- 生成多視角渲染圖 + 360 度全景
- 閒置時排程渲染（借鑑 MetaClaw OMLS 模式）

**工具鏈：**
- 渲染器：Blender + Cycles（headless Python scripting）
- GPU 排程：自訂 OMLS-like 排程器（監控系統負載）
- 後處理：Pillow / ImageMagick（自動加浮水印、尺寸調整）
- 可選：D5 Render LiveSync（手動精修步驟，非自動化）

**OMLS 渲染排程器設計（借鑑 MetaClaw）：**
```python
# render_agent/scheduler/omls_render.py
class RenderScheduler:
    """監控系統資源，在閒置時自動啟動渲染"""

    def check_idle(self):
        gpu_usage = get_gpu_utilization()
        user_active = check_keyboard_mouse_activity()
        calendar_busy = check_google_calendar()

        if gpu_usage < 30 and not user_active:
            return True
        if calendar_busy:  # 使用者在開會 → 渲染窗口
            return True
        return False

    def queue_render(self, scene_file, output_config):
        if self.check_idle():
            start_blender_render(scene_file, output_config)
        else:
            add_to_queue(scene_file, output_config)
```

---

### Agent 5: Export Agent（格式轉換與品質檢查）

```
觸發：渲染完成
輸入：所有中間產物（.FCStd / .blend / .ifc / .glb / renders）
輸出：三層檔案包（Source / Delivery / Construction）
```

**職責：**
- 檔案格式轉換與打包
- IFC 合規性驗證（IfcOpenShell validate）
- GLB 最佳化（壓縮、LOD 生成）
- 自動分類到三層檔案結構

**三層檔案輸出：**

| 層次 | 用途 | 格式 | 接收者 |
|------|------|------|--------|
| Source（原始碼） | 設計師可編輯 | .FCStd / .blend / .skp | 設計團隊 |
| Delivery（交付） | 業主可檢視 | .glb / .pdf / .png / 360° | 業主 |
| Construction（施工） | 施工可用 | .ifc / .dwg / 材料清單 | 施工團隊 |

**工具鏈：**
- IFC 驗證：IfcOpenShell（`ifcopenshell.validate`）
- GLB 優化：gltf-pipeline / gltfpack
- PDF 生成：ReportLab（施工圖 + 材料清單）
- 打包：Python zipfile / tar

---

### Agent 6: Deliver Agent（交付與發布）

```
觸發：Export Agent 完成三層檔案包
輸入：三層檔案包 + 專案 Brief
輸出：更新 Notion 專案頁 + 上傳 Google Drive + 部署 Web 檢視器
```

**職責：**
- 上傳檔案到 Google Drive 專案資料夾（Source / Delivery / Construction）
- 更新 Notion 專案頁面（狀態、里程碑、檔案連結）
- 部署 Web 3D 檢視器（engine_web-ifc 或 xeokit）
- 生成分享連結給業主
- 通知設計師和業主（Email / LINE / Slack）

**工具鏈：**
- MCP：Google Drive MCP + Notion MCP
- Web 檢視器：engine_web-ifc（靜態部署到 Cloudflare Pages / Vercel）
- 通知：Email API / LINE Notify / Slack Webhook

---

## 四、Orchestrator 設計（核心排程引擎）

### 4.1 狀態機

```
INTAKE → VISION → LAYOUT → MODEL → RENDER → EXPORT → DELIVER
  │        │        │        │        │        │        │
  ▼        ▼        ▼        ▼        ▼        ▼        ▼
[人工介入點] 每個環節都可暫停等待設計師確認後再繼續
```

**狀態定義：**
```typescript
// orchestrator/state_machine.ts
enum ProjectState {
  INTAKE_PENDING,
  INTAKE_REVIEW,       // 等待設計師確認 Brief
  VISION_PROCESSING,
  VISION_REVIEW,       // 等待確認辨識結果
  LAYOUT_GENERATING,
  LAYOUT_REVIEW,       // 設計師在 react-planner 中調整
  MODEL_BUILDING,
  MODEL_REVIEW,        // 3D 模型確認
  RENDER_QUEUED,
  RENDER_PROCESSING,
  RENDER_REVIEW,       // 渲染結果確認
  EXPORT_PROCESSING,
  DELIVER_READY,
  DELIVERED,
  REVISION_REQUESTED   // 客戶要求修改 → 回退到指定環節
}
```

### 4.2 事件驅動通訊（OpenCode Agent 原生支援）

```typescript
// orchestrator/event_bus.ts
interface PipelineEvent {
  type: "STAGE_COMPLETE" | "REVIEW_APPROVED" | "REVIEW_REJECTED" | "ERROR";
  source_agent: string;
  target_agent: string;
  project_id: string;
  payload: any;
  timestamp: Date;
}

// Agent 間通訊範例
visionAgent.on("complete", (result) => {
  orchestrator.emit({
    type: "STAGE_COMPLETE",
    source_agent: "vision",
    target_agent: "layout",
    payload: result.floorplan_json
  });
});
```

### 4.3 回退機制

客戶要求修改時，不需要重跑整條管線：

```
修改平面配置 → 回退到 LAYOUT → 重新跑 MODEL → RENDER → EXPORT → DELIVER
修改材質顏色 → 回退到 RENDER → 重新渲染 → EXPORT → DELIVER
修改尺寸     → 回退到 MODEL → 重新建模 → RENDER → EXPORT → DELIVER
```

---

## 五、Skill 進化系統（借鑑 MetaClaw）

### 5.1 每個 Agent 自己的 Skill 庫

```
designclaw/
├── skills/
│   ├── vision/
│   │   ├── skill_001_handdrawn_correction.md    # 手繪草稿常見偏差修正
│   │   └── skill_002_photo_perspective_fix.md   # 現場照片透視矯正技巧
│   ├── layout/
│   │   ├── skill_001_small_apartment_layout.md  # 小坪數最佳配置 pattern
│   │   └── skill_002_elderly_friendly.md        # 高齡友善設計規則
│   ├── model/
│   │   ├── skill_001_wall_thickness_tw.md       # 台灣標準牆厚參數
│   │   └── skill_002_window_types_tw.md         # 台灣常見窗型規格
│   └── render/
│       ├── skill_001_natural_light_setup.md     # 自然光場景設定
│       └── skill_002_night_scene.md             # 夜景渲染參數
```

### 5.2 自動 Skill 提取（MetaClaw 快車道）

每次專案完成後，Orchestrator 自動分析：
1. 哪些環節設計師做了手動修改？→ 提取為新 Skill
2. 客戶滿意度回饋 → 關聯到當次設計決策
3. 渲染參數調整記錄 → 更新最佳實踐

```python
# skills/skill_extractor.py
def extract_skills_from_project(project_log: dict):
    """從專案歷程自動提取可複用的設計經驗"""

    # 比對 AI 原始輸出 vs 設計師最終調整
    diff = compare_ai_output_vs_final(
        project_log["ai_layout"],
        project_log["final_layout"]
    )

    if diff.significant_changes:
        new_skill = generate_skill_from_diff(diff)
        save_skill(new_skill, category=diff.stage)
```

---

## 六、技術選型總結

| 層次 | 組件 | 技術選擇 | 備選方案 |
|------|------|---------|---------|
| Runtime | Agent 框架 | OpenCode（136K stars） | Claude Code Agent SDK |
| Runtime | Agent 通訊 | OpenCode 事件驅動 peer-to-peer | Redis pub/sub |
| Runtime | MCP 整合 | OpenCode 原生 MCP | 自建 MCP bridge |
| Runtime | 模型路由 | OpenCode 多模型支援 | MetaClaw Proxy |
| Vision | 平面圖辨識 | TF2DeepFloorplan（Docker） | CubiCasa API（商業） |
| Vision | 校驗 | Claude Haiku Vision | GPT-4V |
| Layout | 2D 編輯器 | react-planner fork | Sweet Home 3D |
| Layout | AI 佈局 | HouseDiffusion | Graph2plan |
| Model | 3D CAD | FreeCAD headless（Python） | Blender headless |
| Model | BIM | IfcOpenShell + Bonsai BIM | — |
| Render | 渲染器 | Blender + Cycles headless | D5（手動精修） |
| Render | 排程 | 自訂 OMLS-like 排程器 | Celery + Redis |
| Export | IFC 驗證 | IfcOpenShell validate | — |
| Export | GLB 優化 | gltf-pipeline | gltfpack |
| Deliver | Web 檢視器 | engine_web-ifc / xeokit-sdk | Three.js + IFCLoader |
| Deliver | 專案管理 | Notion MCP | — |
| Deliver | 檔案儲存 | Google Drive MCP | S3 |
| 進化層 | Skill 管理 | 自建（Markdown 檔） | MetaClaw Skills |
| 進化層 | 模型微調 | MetaClaw RL（可選） | 手動 fine-tune |

---

## 七、專案 Repo 結構

```
designclaw/
├── README.md
├── package.json                    # Bun monorepo
├── turbo.json
├── .opencode.json                  # OpenCode 設定（MCP servers, models）
│
├── packages/
│   ├── orchestrator/               # 核心排程引擎
│   │   ├── state_machine.ts
│   │   ├── event_bus.ts
│   │   └── project_manager.ts
│   │
│   ├── agents/
│   │   ├── intake/                 # Agent 0: 案件接收
│   │   │   ├── agent.md            # Agent system prompt
│   │   │   ├── tools/
│   │   │   │   └── brief_parser.py
│   │   │   └── tests/
│   │   ├── vision/                 # Agent 1: AI 視覺辨識
│   │   │   ├── agent.md
│   │   │   ├── tools/
│   │   │   │   ├── floorplan_detector.py
│   │   │   │   └── opencv_preprocess.py
│   │   │   ├── models/             # TF2DeepFloorplan Docker
│   │   │   └── tests/
│   │   ├── layout/                 # Agent 2: 2D 平面配置
│   │   │   ├── agent.md
│   │   │   ├── tools/
│   │   │   │   └── layout_optimizer.py
│   │   │   └── web/                # react-planner Web UI
│   │   ├── model/                  # Agent 3: 3D 建模
│   │   │   ├── agent.md
│   │   │   ├── tools/
│   │   │   │   ├── layout_to_3d.py
│   │   │   │   └── ifc_exporter.py
│   │   │   └── furniture_library/
│   │   ├── render/                 # Agent 4: 渲染
│   │   │   ├── agent.md
│   │   │   ├── tools/
│   │   │   │   ├── blender_render.py
│   │   │   │   └── omls_scheduler.py
│   │   │   └── templates/          # 燈光/材質預設
│   │   ├── export/                 # Agent 5: 格式轉換
│   │   │   ├── agent.md
│   │   │   └── tools/
│   │   │       ├── ifc_validator.py
│   │   │       └── glb_optimizer.py
│   │   └── deliver/                # Agent 6: 交付發布
│   │       ├── agent.md
│   │       └── tools/
│   │           ├── notion_updater.py
│   │           └── gdrive_uploader.py
│   │
│   ├── skills/                     # 設計經驗庫（自進化）
│   │   ├── vision/
│   │   ├── layout/
│   │   ├── model/
│   │   └── render/
│   │
│   ├── mcp-servers/                # 自訂 MCP servers
│   │   ├── notion-mcp/
│   │   ├── gdrive-mcp/
│   │   └── floorplan-mcp/          # 平面圖辨識 MCP 封裝
│   │
│   └── web-viewer/                 # 客戶端 Web 3D 檢視器
│       ├── src/
│       │   └── viewer.ts           # engine_web-ifc / xeokit
│       └── package.json
│
├── docker/
│   ├── docker-compose.yml          # 全套服務
│   ├── tf2deepfloorplan/           # Vision 模型容器
│   ├── freecad-headless/           # FreeCAD 無頭容器
│   └── blender-render/             # Blender 渲染容器
│
└── docs/
    ├── architecture.md
    ├── agent-specs.md
    └── skill-authoring-guide.md
```

---

## 八、分階段實施計畫

### Phase 0: 環境搭建（1 週）

| 任務 | 詳細 | 產出 |
|------|------|------|
| 安裝 OpenCode | 設定多模型支援（Claude + Gemini） | `.opencode.json` |
| Docker 環境 | TF2DeepFloorplan + FreeCAD + Blender 容器 | `docker-compose.yml` |
| MCP 連接 | 接通 Notion MCP + Google Drive MCP | MCP 設定驗證 |
| Repo 初始化 | monorepo 骨架 + CI/CD | GitHub repo |

### Phase 1: 核心雙 Agent POC（2 週）

| 任務 | 詳細 | 產出 |
|------|------|------|
| Vision Agent | TF2DeepFloorplan Docker + Claude Vision 校驗 | floorplan.json 輸出 |
| Model Agent | FreeCAD headless 腳本：JSON → 3D → IFC | .ifc 檔案 |
| 端到端測試 | 用 3 張真實平面圖跑完 Vision → Model | POC demo |

### Phase 2: 完整管線 MVP（4 週）

| 任務 | 詳細 | 產出 |
|------|------|------|
| Orchestrator | 狀態機 + 事件 bus | 自動流轉 |
| Layout Agent | react-planner fork + HouseDiffusion | 2D 配置 |
| Render Agent | Blender Cycles headless + OMLS 排程 | 渲染圖 |
| Export Agent | IFC 驗證 + GLB 優化 + 三層打包 | 檔案包 |
| Deliver Agent | Notion 更新 + GDrive 上傳 + Web 檢視器 | 交付完成 |

### Phase 3: 進化與優化（持續）

| 任務 | 詳細 | 產出 |
|------|------|------|
| Skill 提取器 | 從專案歷程自動提取設計 pattern | 經驗庫 |
| MetaClaw 整合 | 透明代理 + RL 訓練（可選） | 模型越用越準 |
| 客戶端優化 | Web 檢視器 PWA + 手機端 | 業主體驗提升 |
| 台灣在地化 | 建材庫、法規檢查（建築技術規則）| 合規性 |

---

## 九、風險與對策

| 風險 | 影響 | 對策 |
|------|------|------|
| AI 辨識精度不足 | 下游全部偏差 | 每環節設人工審核關卡，Vision Agent 低信心分數強制人工 |
| react-planner 停更 | 2D 編輯器無法維護 | 維護自己的 fork，或評估 Sweet Home 3D |
| FreeCAD headless 不穩定 | 建模環節失敗 | Docker 化隔離 + 自動重試 + fallback 到 Blender |
| 渲染耗時過長 | 專案交付延遲 | OMLS 排程 + GPU 雲端加速（Lambda / RunPod） |
| Agent 間資料格式不一致 | 管線斷裂 | 定義嚴格的 JSON Schema + 每步驗證 |
| 客戶不習慣新流程 | 推廣困難 | 先內部試跑 3 個專案，驗證後再推廣 |

---

## 行動項目

### 立即可做（本週）
- [ ] 安裝 OpenCode Agent，設定 `.opencode.json`（多模型 + MCP）
- [ ] Docker 跑起 TF2DeepFloorplan，用 3 張平面圖測試辨識精度
- [ ] 初始化 `designclaw` GitHub repo，建立 monorepo 骨架
- [ ] 用 FreeCAD Python API 寫一個最小腳本：hardcoded JSON → 3D 牆體 → IFC

### 短期（兩週內）
- [ ] 完成 Vision Agent + Model Agent 端到端 POC（平面圖 → IFC）
- [ ] Fork react-planner，評估 work-vv 版本穩定度
- [ ] 設計 `floorplan.json` 和 `layout.json` 的 JSON Schema
- [ ] 接通 Notion MCP + Google Drive MCP，驗證自動建立專案頁

### 中期（一個月內）
- [ ] 完成 Orchestrator 狀態機 + 事件 bus
- [ ] 七個 Agent 全部上線，跑完第一個完整專案
- [ ] 部署 Web 3D 檢視器（engine_web-ifc）
- [ ] Blender Cycles headless 渲染 + OMLS 排程器

### 長期（三個月+）
- [ ] Skill 自動提取系統上線
- [ ] 台灣建材庫 + 建築技術規則合規檢查
- [ ] 評估 MetaClaw 整合（透明代理 + RL 微調 Vision 模型）
- [ ] 客戶端 PWA + 業主端體驗優化
