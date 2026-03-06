---
title: 法拍地圖宣傳影片 (Veo)
status: in-progress
priority: high
started: 2026-03-04
---

# 法拍地圖宣傳影片

## 規格
- 6 段 × 8 秒 = 48 秒
- Veo 生成（每日 3 段額度）
- Day 2: 重做段 1 + 段 2 + 段 3 (或 段3-5)
- Day 3: 剩餘段
- 後製: TTS 旁白 + 背景音樂 + 字幕 + ffmpeg 合成

## Style Anchor (每段 prompt 結尾必須包含)

```
Cinematic, shot on digital cinema camera, 35mm film emulation, 
shallow depth of field, warm neutral tones with cool blue accent lighting, 
teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps
```

## 分鏡腳本 v4 (Taiwan-specific, approved 2026-03-05)

### 段 1 — 痛點：資訊過載 (8s)
**鏡頭**: Medium close-up, 50mm lens, slow dolly backward
**旁白**: 法拍公告資訊密密麻麻，想找到物件在哪裡？難如大海撈針
**Veo prompt**:
```
Medium close-up, 50mm lens, slow dolly backward revealing more chaos. An East Asian Taiwanese man in his 30s wearing glasses sits at a cluttered desk, rubbing his temples in frustration. Stacks of dense printed government court auction documents with small text scattered everywhere. An old monitor behind him shows a traditional government website with tables and forms. Warm desk lamp providing amber side fill from the left, cool overhead fluorescent casting shadows. Typical Taiwanese apartment interior with tiled floor visible. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

### 段 2 — 解決方案：地圖自動標記 (8s)
**鏡頭**: Wide shot, 24mm lens, slow crane descent
**旁白**: 我們自動將近萬筆法拍物件標記在地圖上，物件位置一目了然
**Veo prompt**:
```
Wide establishing shot, 24mm lens, slow smooth crane descending. A glowing digital map of Taiwan island rendered in dark navy blue interface, floating in a dark environment. Hundreds of bright red pins mark buildings and green pins mark land parcels scattered across the island shape. Small data cards float beside clusters showing price ranges and district names. The map slowly rotates to reveal depth and density of pins around Taipei area. Cool blue ambient light with warm golden pin glows creating contrast. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

### 段 3 — 直覺操作：點擊即見資訊 (8s)
**鏡頭**: Over-the-shoulder, 85mm lens, rack focus
**旁白**: 點擊即見價格、面積、拍次，一鍵直達法院公告原文
**Veo prompt**:
```
Over-the-shoulder shot, 85mm lens, subtle rack focus from shoulder to screen. A Taiwanese woman in her 30s sits at a modern desk, her hand guiding a mouse. The monitor faces toward the camera showing a dark-themed map interface with red and green pins. She clicks a pin and an elegant popup card appears with structured data. The screen reflects soft blue light on her face. Warm amber desk lamp from the left, typical Taiwanese apartment with white walls. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

### 段 4 — 手機端：戶外實地查看 (8s)
**鏡頭**: Medium shot, 35mm lens, handheld tracking
**旁白**: 出門在外也能隨時查看，打開手機，附近法拍物件盡收眼底
**Veo prompt**:
```
Medium shot, 35mm lens, handheld tracking with gentle movement. A young Taiwanese man walks through a typical Taiwan street with parked scooters, arcade-style covered sidewalks, and tropical plants. He holds a smartphone displaying a map with glowing red and green property pins. The street has characteristic Taiwanese shop signage and tile-paved ground. Warm afternoon sunlight filtering through the arcade roof, natural golden light from the left. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

### 段 5 — 免費易用：人人可用 (8s)
**鏡頭**: Medium wide, 35mm lens, slow pan right
**旁白**: 完全免費、無需註冊，新手也能輕鬆上手
**Veo prompt**:
```
Medium wide shot, 35mm lens, slow pan right. A cozy Taiwanese cafe interior with large windows. A Taiwanese grandmother with silver hair and a young professional woman sit together at a table, both looking at a laptop screen showing the map interface. The younger woman points at the screen explaining while the grandmother nods with a warm smile. Bubble tea cups on the table. Warm natural light streaming through windows from the left, soft cafe ambient lighting. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

### 段 6 — CTA：空拍收尾 (8s)
**鏡頭**: Aerial drone shot, 24mm wide-angle, slow push forward
**旁白**: 法拍地圖，您的法拍資訊入口。立即前往 foreclosure-map.homes
**Veo prompt**:
```
Aerial drone shot, 24mm wide-angle lens, slow push forward at golden hour. Flying over Taipei city skyline at dusk with Taipei 101 tower visible in the background. Camera gradually descends toward dense urban neighborhoods below. Hundreds of glowing golden pins of light appear scattered across rooftops and streets like a digital overlay on the real city. Warm golden sunset painting buildings amber, deep blue twilight sky above. Epic cinematic scale. Cinematic, 35mm film emulation, shallow depth of field, teal-and-amber color grade, soft volumetric lighting, subtle film grain, 24fps.
```

## Prompt 設計原則
- **Style Anchor**: 最後一段完全相同，確保視覺連貫
- **光線方向統一**: 所有室內場景主光源在左側 (warm amber from left)
- **色調統一**: teal-and-amber color grade
- **鏡頭焦段遞進**: 24mm(wide) → 50mm(medium) → 85mm(close) → 35mm(outdoor) → 24mm(aerial)
- **一段一個鏡頭運動**: dolly / crane / static / tracking / pan / drone
- **不含中文文字**: 所有文字後製 ffmpeg 疊加

## 進度

### 2026-03-04 Session 1 (Day 1)
- [x] 段 1 v1: veo_157bc9b1.mp4 (快捷模式，需重做)
- [x] 段 2 v1: veo_f1eb4c68.mp4 (思考型，正確流程，但 prompt 不專業)
- [x] Provider 修正: v4.1 (PRO badge 誤判 + 製作影片 chip)
- [x] AI Hub Guide 更新: Veo 使用說明
- [x] Veo prompt 研究完成，v3 腳本重寫

### 2026-03-05 (Day 2)
- [x] v4 分鏡腳本（加入台灣元素：台灣人、台灣地圖、紅綠標記、騎樓街景、101）
- [x] v4 分鏡圖片 6 張生成 + 用戶核准
- [x] ac-mac WiFi 斷線診斷（10:15 WiFi 斷開 7.5h，reason=14 AP 主動踢開）
- [x] 段 1 v4: veo_a3ef0008.mp4 (101s)
- [ ] 段 2 v4: 生成中...
- [ ] 段 3 v4: 待生成

### Day 3+ — 待做
- [ ] 生成剩餘段
- [ ] TTS 旁白錄製
- [ ] ffmpeg 合成 + 字幕疊加

## 相關檔案
- Veo 輸出: `/usr/local/bin/ai-hub/output/videos/`
- 舊版影片: https://www.youtube.com/watch?v=-92RRrxLWq4
- 法拍地圖網站: https://foreclosure-map.homes
- Veo prompt 指南: `/usr/local/bin/ai-hub/AI-HUB-GUIDE.md`

### 2026-03-05 Session 完成
- [x] v4 分鏡腳本（台灣元素）+ 圖片核准
- [x] 段 1 v4: veo_a3ef0008.mp4 (101s, 3.4MB)
- [x] 段 2 v4: veo_36f7ed94.mp4 (106s, 4.2MB)
- [x] 段 3 v4: veo_75cca6f4.mp4 (95s, 1.5MB)
- [x] TTS 旁白: Qwen3-TTS Alan clone (3 段)
- [x] BGM: Kevin MacLeod "Inspired" (CC BY 4.0)
- [x] ffmpeg 合成 24s 預覽影片
- [x] 部署到 GitHub: videos/promo-preview.mp4
- [x] WiFi 自動重連 cron 部署 (ac-mac/acmacmini2, ac-rpi5/ac-2012 有線版)
- [x] ac-mac 離線原因: WiFi 10:15 斷開 7.5h (reason=14 AP 踢開)

### Day 3 待做
- [ ] 段 4-6 Veo 生成 (額度明天刷新)
- [ ] TTS 旁白 段 4-6
- [ ] 完整 48s 影片合成 + 字幕疊加
- [ ] 最終版部署
