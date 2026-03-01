# Gemini 圖片生成模型限額與注意事項

> 建立日期: 2026-02-22
> 更新日期: 2026-02-23
> 適用: AI Hub gemini_image provider (ac-mac)

## 內部圖片模型：Nano Banana Pro vs Nano Banana

Gemini Pro 帳號在生成圖片時，會使用 Google 內部的 Imagen 變體模型。
兩者的差異**不是由使用者選擇模型決定的**，而是由 Google 後端配額動態控制。

### Nano Banana Pro（Pro 配額內）
- **每日限額**: Google 官方標示 100 張，但實際動態調整，**安全值約 50 張**
- **觸發條件**: 「Pro」和「思考型」模式都會觸發 Nano Banana Pro — 這不是模型選擇的問題，兩者內部都啟用同一個 Pro 圖片引擎
- **尺寸**: 正確遵循 prompt（如 16:9 → 878x490）
- **CJK 文字**: 繁體中文渲染正確，長標題（8-20 字）可正常顯示
- **畫質**: 較高，細節豐富

### Nano Banana（普通版，無限額度）
- **觸發條件 1**: Pro 每日配額耗盡後，**所有模式（Pro、思考型）都會靜默降級**到普通 Nano Banana，無任何 UI 提示
- **觸發條件 2**: 選擇「快速」(fast/quick) 模式時，直接使用普通 Nano Banana，**不消耗 Pro 配額，無每日限制**
- **尺寸**: 固定正方形（878x878），忽略 prompt 中的比例要求
- **CJK 文字**: 中文亂碼（garbled），僅 2-4 字短詞偶爾正確
- **畫質**: 較低，風格偏卡通

### 配額機制重點
1. **Pro 和思考型都用 Nano Banana Pro** — 不存在「選 Pro 模型才能用 Pro 引擎」的說法
2. **配額耗盡後靜默降級** — 不管你選哪個模式，一旦 Pro 配額用完，所有圖片生成都退回普通 Nano Banana
3. **快速模式 = 普通 Nano Banana** — 免費無限，但品質低
4. **每日 Pro 配額動態浮動** — Google 標示 100，實際可能只有 50 或更少，以前一天實測為準

### 如何判斷目前用哪個模型
- 圖片尺寸：878x490 等非正方形（Pro）vs 878x878 固定正方形（降級）
- 中文字：正確 vs 亂碼
- UI 上**不會顯示**降級提示，只能從結果判斷

## 最佳實踐

### 1. 簡單卡片：PIL overlay + 快速模式背景（推薦）
- **最推薦的做法**，適合大量產製（如 sustainability100 卡片）
- 用快速模式的 Nano Banana 生成背景插圖（prompt 中不寫中文）
- **快速模式無每日限制**，不消耗 Pro 配額
- 再用 PIL + NotoSansCJK-Bold-TC 疊加繁體中文標題
- 字型路徑: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc (index=3 for TC)
- 優點：無配額問題、中文永遠正確、可大量生成
- 適用：標題卡片、封面圖、任何需要 CJK 文字的批量圖片

### 2. 高品質圖片：Pro 配額內直接渲染
- 需要高品質且含中文的圖片時使用
- 每天最多生成 **50 張**以內（安全值）
- 早上開始跑，避免與其他自動排程搶額度
- **超過 50 張的需求，排入隔天隊列**，不要硬撐等降級

### 3. 混合方案
- Pro 額度內用 Gemini 直接渲染（品質最佳）
- 額度用完後不再嘗試（降級後品質太差）
- 剩餘需求改用 PIL overlay，或排入隔天
- 可透過檢測圖片尺寸判斷是否降級（878x878 = 降級）

### 4. 配額管理
- 每天 Pro 配額 ≈ 50 張（動態，以實測為準）
- 超出部分**不要當天硬做**，排入隔天隊列
- 監控方式：檢查圖片尺寸，一旦出現 878x878 即表示配額用完
- 建議：在 AI Hub 加上降級偵測，自動停止當天的圖片任務

## AI Hub config.py 設定
- `DAILY_LIMITS["gemini_image"] = 50`（安全值，非官方 100）
- 已正確設定，無需修改

## 相關檔案
- Provider: /usr/local/bin/ai-hub/providers/gemini_image.py
- Config: /usr/local/bin/ai-hub/config.py
- PIL overlay 腳本: /tmp/regen_all_images_v4.py
- 字型: /usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc (index 3 = TC)
