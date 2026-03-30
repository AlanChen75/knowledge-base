---
title: 归藏 Claude-to-Telegram Bot 方案测试
status: pending
priority: medium
created: 2026-03-07
---

# 归藏 Claude-to-Telegram Bot 方案

## 目标
测试归藏（藏师傅）的 Claude-to-IM Skill，用 Telegram Long Polling 直接跟本机 Claude Code 对话，作为 Happy Coder 的轻量备援入口。

## 动机
- Happy Coder 依赖 Happy 云端 (api.cluster-fluster.com)，曾遇过服务中断
- 归藏方案零云端依赖，只需 Telegram Bot API + 本机 claude CLI
- 两套并存 = 高可用

## 架构差异（已分析完成）

| | 归藏方案 | Happy Coder |
|---|---|---|
| 中间层 | Telegram（免费公共设施） | Happy 自建云 (cluster-fluster.com) |
| 协议 | HTTP Long Polling | WebSocket (Socket.IO) |
| 客户端 | Telegram App | 专属 App + Web |
| 依赖 | Telegram 服务 | Happy 云端 |
| 加密 | Telegram 自带 | tweetnacl 端对端 |

## 参考资料
- 推文: https://x.com/i/status/2029922289408692314
- Claude Agent SDK: Anthropic 官方 npm 库
- 关键原理: daemon 进程用 Long Polling 拉 Telegram 消息，spawn 本机 claude CLI 执行

## 待办
- [ ] 找到归藏的开源 repo 或 skill 原始码
- [ ] 在 ac-mac 上测试部署
- [ ] 设定 Telegram Bot（可复用现有 bot 或新建）
- [ ] 验证 Claude Agent SDK spawn claude CLI 是否正常
- [ ] 与 Happy Coder 并存测试
- [ ] 稳定后设为 systemd 服务
