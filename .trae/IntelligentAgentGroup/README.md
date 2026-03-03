# Intelligent Agent Group

智能体协作系统配置文件

## 概述

本目录包含多智能体协作系统的所有配置文件，包括：
- 各智能体的配置文件 (config.json)
- 智能体技能定义 (SKILL.md)
- 智能体间通信协议 (PROTOCOL.md)
- 任务模板 (templates/)

## 目录结构

```
IntelligentAgentGroup/
├── PROJECT_MANAGER/           # 项目经理智能体
│   ├── config.json
│   └── SKILL.md
├── FRONTEND_AGENT/            # 前端智能体
│   ├── config.json
│   └── SKILL.md
├── BACKEND_AGENT/             # 后端智能体
│   ├── config.json
│   └── SKILL.md
├── TESTING_AGENT/             # 测试智能体
│   ├── config.json
│   └── SKILL.md
├── CODE_REVIEW_AGENT/         # 代码审查智能体
│   ├── config.json
│   └── SKILL.md
├── DEVOPS_AGENT/              # 部署/DevOps智能体
│   ├── config.json
│   └── SKILL.md
├── TEMPLATES/                 # 任务模板
│   ├── task-template.json
│   └── message-template.json
├── PROTOCOL.md                # 智能体间通信协议
├── WORKFLOWS.md               # 工作流定义文档
├── index.json                 # 智能体配置汇总
└── README.md                  # 本文件
```

## 智能体列表

| 智能体 | 标识符 | 主要职责 |
|--------|--------|----------|
| 项目经理 | PROJECT_MANAGER | 任务协调、需求分析、进度跟踪 |
| 前端 | FRONTEND_AGENT | UI开发、组件实现、前端测试 |
| 后端 | BACKEND_AGENT | API开发、业务逻辑、数据库 |
| 测试 | TESTING_AGENT | 单元测试、集成测试、E2E测试 |
| 代码审查 | CODE_REVIEW_AGENT | 代码质量检查、安全审查 |
| DevOps | DEVOPS_AGENT | CI/CD、部署、监控 |

## 使用方式

1. 在 Trae/Windsurf 中使用特定触发词调用智能体
2. 智能体之间通过标准化的消息格式进行通信
3. 项目记忆系统 (Memory/) 作为共享上下文

## 触发词示例

- `@项目经理` - 分配新任务
- `@前端` - 前端开发
- `@后端` - 后端开发
- `@测试` - 运行测试
- `@审查` - 代码审查
- `@部署` - 部署任务

## 智能体协作流程

```
用户提出需求
    │
    ▼
PROJECT_MANAGER (任务协调)
    │
    ├───────────────┬───────────────┐
    │               │               │
    ▼               ▼               ▼
FRONTEND      BACKEND        TESTING
(前端开发)      (后端开发)      (测试准备)
    │               │
    └───────┬───────┘
            │
            ▼
    CODE_REVIEW (代码审查)
            │
            ▼
    TESTING (测试执行)
            │
            ▼
    DEVOPS (部署上线)
            │
            ▼
PROJECT_MANAGER (完成报告)
```

## 相关文档

| 文档 | 说明 |
|------|------|
| [PROTOCOL.md](PROTOCOL.md) | 智能体间通信协议规范 |
| [WORKFLOWS.md](WORKFLOWS.md) | 标准工作流程定义 |
| [index.json](index.json) | 智能体配置汇总 |
| [TEMPLATES/](TEMPLATES/) | 任务和消息模板 |
