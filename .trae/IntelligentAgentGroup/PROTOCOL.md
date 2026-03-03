# 智能体间通信协议 (Agent Communication Protocol)

## 概述

本文档定义了智能体协作系统中各智能体之间的通信规范，确保智能体之间能够高效、准确地交换信息。

## 通信架构

### 消息传递模式

```
┌─────────────────────────────────────────────────────────────┐
│                    智能体协作系统                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   ┌──────────────┐                                      │
│   │    用户      │                                      │
│   └──────┬───────┘                                      │
│          │                                               │
│          ▼                                               │
│   ┌──────────────┐                                       │
│   │ PROJECT_     │ ◄────── 任务分发                        │
│   │ MANAGER      │                                       │
│   └──────┬───────┘                                       │
│          │                                               │
│   ┌──────┴───────┬──────────────┬──────────────┐         │
│   ▼              ▼              ▼              ▼         │
│ ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │
│ │FRONTEND│  │BACKEND │  │ TESTING │  │  CODE  │          │
│ │_AGENT  │  │_AGENT  │  │_AGENT  │  │REVIEW  │          │
│ └────┬───┘  └────┬───┘  └────┬───┘  └────┬───┘          │
│      │           │            │            │               │
│      └───────────┴─────┬──────┴────────────┘               │
│                        ▼                                    │
│                 ┌──────────┐                                │
│                 │ DEVOPS   │                                │
│                 │ _AGENT   │                                │
│                 └──────────┘                                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 通信方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| 直接调用 | 一个智能体直接调用另一个 | 任务分配、协作请求 |
| 消息队列 | 通过消息队列异步通信 | 状态更新、通知 |
| 共享上下文 | 通过 Memory/ 共享信息 | 项目状态、配置 |

## 消息格式

### 标准消息结构

```json
{
  "messageId": "MSG-001",
  "timestamp": "2026-03-03T10:30:00Z",
  "type": "TASK | NOTIFICATION | REQUEST | RESPONSE",
  "from": "AGENT_NAME",
  "to": "AGENT_NAME",
  "priority": "high | medium | low",
  "content": {
    // 消息内容
  },
  "context": {
    // 上下文信息
  }
}
```

### 消息类型

#### 1. 任务消息 (TASK)

```json
{
  "messageId": "MSG-001",
  "timestamp": "2026-03-03T10:30:00Z",
  "type": "TASK",
  "from": "PROJECT_MANAGER",
  "to": "FRONTEND_AGENT",
  "priority": "high",
  "content": {
    "taskId": "TASK-001",
    "title": "用户登录页面开发",
    "description": "实现用户登录页面，包括邮箱/密码登录",
    "requirements": [
      "响应式设计",
      "表单验证",
      "错误提示"
    ],
    "deadline": "2026-03-05T18:00:00Z",
    "dependencies": []
  },
  "context": {
    "projectPath": "e:/oc/oc-platform",
    "frontendPath": "e:/oc/oc-platform/oc-platform-web"
  }
}
```

#### 2. 通知消息 (NOTIFICATION)

```json
{
  "messageId": "MSG-002",
  "timestamp": "2026-03-03T11:00:00Z",
  "type": "NOTIFICATION",
  "from": "BACKEND_AGENT",
  "to": "PROJECT_MANAGER",
  "priority": "medium",
  "content": {
    "event": "API_READY",
    "message": "产品API已开发完成",
    "details": {
      "endpoints": [
        "GET /api/v1/products",
        "POST /api/v1/products"
      ]
    }
  }
}
```

#### 3. 请求消息 (REQUEST)

```json
{
  "messageId": "MSG-003",
  "timestamp": "2026-03-03T11:30:00Z",
  "type": "REQUEST",
  "from": "FRONTEND_AGENT",
  "to": "BACKEND_AGENT",
  "priority": "high",
  "content": {
    "requestType": "API_SPEC",
    "purpose": "前端需要产品列表API的详细规范",
    "specifications": {
      "endpoint": "/api/v1/products",
      "method": "GET",
      "params": [
        {"name": "page", "type": "number"},
        {"name": "pageSize", "type": "number"}
      ],
      "expectedResponse": {
        "list": "Product[]",
        "total": "number"
      }
    }
  }
}
```

#### 4. 响应消息 (RESPONSE)

```json
{
  "messageId": "MSG-004",
  "timestamp": "2026-03-03T12:00:00Z",
  "type": "RESPONSE",
  "from": "BACKEND_AGENT",
  "to": "FRONTEND_AGENT",
  "priority": "high",
  "content": {
    "requestId": "MSG-003",
    "status": "SUCCESS",
    "data": {
      "endpoint": "/api/v1/products",
      "method": "GET",
      "description": "获取产品列表",
      "params": [
        {"name": "page", "type": "integer", "required": false, "default": 1},
        {"name": "pageSize", "type": "integer", "required": false, "default": 10},
        {"name": "category", "type": "string", "required": false}
      ],
      "response": {
        "success": "boolean",
        "data": {
          "list": [
            {
              "id": "long",
              "name": "string",
              "price": "decimal",
              "status": "string"
            }
          ],
          "total": "long",
          "page": "integer",
          "pageSize": "integer"
        }
      }
    }
  }
}
```

#### 5. 任务完成消息 (TASK_COMPLETE)

```json
{
  "messageId": "MSG-005",
  "timestamp": "2026-03-03T15:00:00Z",
  "type": "TASK_COMPLETE",
  "from": "FRONTEND_AGENT",
  "to": "PROJECT_MANAGER",
  "priority": "high",
  "content": {
    "taskId": "TASK-001",
    "status": "COMPLETED",
    "deliverables": [
      "src/pages/Login.tsx",
      "src/api/auth.ts",
      "src/store/authSlice.ts"
    ],
    "testUrl": "http://localhost:5173/login",
    "notes": "登录页面已完成，包含响应式设计和表单验证"
  }
}
```

#### 6. 错误消息 (ERROR)

```json
{
  "messageId": "MSG-006",
  "timestamp": "2026-03-03T15:30:00Z",
  "type": "ERROR",
  "from": "TESTING_AGENT",
  "to": "PROJECT_MANAGER",
  "priority": "high",
  "content": {
    "taskId": "TASK-003",
    "errorType": "TEST_FAILURE",
    "message": "登录功能测试失败",
    "details": {
      "testCase": "testLoginWithInvalidPassword",
      "error": "Expected to show error message, but got success",
      "stack": "at TestRunner.run (test.ts:42)"
    },
    "recommendation": "需要检查登录API的返回值处理"
  }
}
```

## 智能体通信规则

### 通信矩阵

| 从 / 到 | PROJECT_MANAGER | FRONTEND | BACKEND | TESTING | CODE_REVIEW | DEVOPS |
|---------|-----------------|-----------|---------|---------|-------------|--------|
| PROJECT_MANAGER | - | 任务 | 任务 | 任务 | 任务 | 任务 |
| FRONTEND | 完成/问题 | - | 请求/响应 | 请求 | 请求审查 | - |
| BACKEND | 完成/问题 | 响应 | - | 请求 | 请求审查 | - |
| TESTING | 完成/报告 | - | - | - | - | - |
| CODE_REVIEW | 完成报告 | - | - | - | - | - |
| DEVOPS | 完成报告 | - | - | - | - | - |

### 消息流向

```
用户需求
    │
    ▼
PROJECT_MANAGER (任务规划与分配)
    │
    ├─────────────────┬─────────────────┐
    │                 │                 │
    ▼                 ▼                 ▼
FRONTEND         BACKEND           TESTING
(前端开发)       (后端开发)        (测试)
    │                 │                 │
    │                 │                 │
    ▼                 ▼                 ▼
CODE_REVIEW ◄──────┴──────────────────►
(代码审查)              │
                        ▼
                    DEVOPS
                    (部署)
                        │
                        ▼
                    PROJECT_MANAGER
                    (完成报告)
```

## 任务状态流转

### 任务生命周期

```
┌─────────┐    分配     ┌───────────┐    开始     ┌─────────────┐
│ PENDING │ ─────────► │ ASSIGNED │ ─────────► │IN_PROGRESS │
└─────────┘            └───────────┘            └──────┬──────┘
                                                       │
                          ┌─────────────┐              │
                          │   BLOCKED   │ ◄───────────┘
                          └──────┬──────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        ▼                        ▼                        ▼
┌───────────────┐     ┌─────────────────┐      ┌────────────────┐
│    FAILED     │     │   COMPLETED    │      │    PAUSED     │
└───────────────┘     └────────┬────────┘      └────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    REVIEW/QA       │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
      ┌──────────────┐  ┌────────────┐  ┌─────────────┐
      │ APPROVED     │  │ REJECTED   │  │ DEPLOYED   │
      └──────────────┘  └────────────┘  └─────────────┘
```

### 状态说明

| 状态 | 说明 | 负责智能体 |
|------|------|------------|
| PENDING | 待分配 | PROJECT_MANAGER |
| ASSIGNED | 已分配，等待开始 | PROJECT_MANAGER |
| IN_PROGRESS | 进行中 | 执行智能体 |
| BLOCKED | 阻塞 | 执行智能体 |
| FAILED | 失败 | 执行智能体 |
| COMPLETED | 已完成 | 执行智能体 |
| REVIEW | 待审查 | CODE_REVIEW |
| APPROVED | 审查通过 | CODE_REVIEW |
| REJECTED | 审查拒绝 | CODE_REVIEW |
| DEPLOYED | 已部署 | DEVOPS |
| PAUSED | 暂停 | PROJECT_MANAGER |

## 错误处理

### 错误类型

| 错误类型 | 说明 | 处理方式 |
|----------|------|----------|
| TASK_FAILED | 任务执行失败 | 重试或重新分配 |
| TIMEOUT | 任务超时 | 延长时限或终止 |
| DEPENDENCY_FAILED | 依赖任务失败 | 通知前置任务负责人 |
| COMMUNICATION_ERROR | 通信错误 | 重试通信 |
| PERMISSION_DENIED | 权限不足 | 提升权限或请求授权 |

### 错误消息示例

```json
{
  "messageId": "MSG-ERROR-001",
  "timestamp": "2026-03-03T16:00:00Z",
  "type": "ERROR",
  "from": "FRONTEND_AGENT",
  "to": "PROJECT_MANAGER",
  "priority": "high",
  "content": {
    "errorType": "DEPENDENCY_FAILED",
    "originalTaskId": "TASK-001",
    "failedDependency": "TASK-002",
    "message": "等待后端API完成，但后端任务失败",
    "details": {
      "failedTask": "产品API开发",
      "reason": "数据库连接配置错误"
    },
    "recommendation": "需要先修复后端任务 TASK-002"
  }
}
```

## 共享上下文

### 项目信息 (Shared Context)

智能体通过 Memory/ 目录共享项目信息：

```
Memory/
├── Backend/
│   ├── api.md           # API文档
│   ├── architecture.md  # 架构设计
│   └── security.md      # 安全配置
├── Frontend/
│   ├── architecture.md  # 前端架构
│   ├── pages.md         # 页面信息
│   └── theme.md         # 主题配置
├── Database/
│   └── schema.md        # 数据库schema
├── Testing/
│   └── status.md        # 测试状态
└── WorkLogs/
    └── *.md             # 工作日志
```

### 上下文访问规则

| 智能体 | 读取权限 | 写入权限 |
|--------|----------|----------|
| PROJECT_MANAGER | 所有 | WorkLogs/ |
| FRONTEND_AGENT | Frontend/, Backend/api.md | - |
| BACKEND_AGENT | Backend/, Database/ | - |
| TESTING_AGENT | 所有 | Testing/ |
| CODE_REVIEW_AGENT | 所有 | - |
| DEVOPS_AGENT | 所有 | - |

## 触发词汇总

### 智能体触发

| 智能体 | 触发词 |
|--------|--------|
| PROJECT_MANAGER | @项目经理、分配任务、任务协调 |
| FRONTEND_AGENT | @前端、前端开发、frontend |
| BACKEND_AGENT | @后端、后端开发、backend |
| TESTING_AGENT | @测试、testing、单元测试 |
| CODE_REVIEW_AGENT | @代码审查、code review、CR |
| DEVOPS_AGENT | @部署、DevOps、deploy |

### 协作触发

| 场景 | 触发方式 |
|------|----------|
| 分配任务 | PROJECT_MANAGER 直接调用 |
| 请求API | FRONTEND → BACKEND |
| 请求审查 | ANY → CODE_REVIEW |
| 请求测试 | PROJECT_MANAGER → TESTING |
| 请求部署 | PROJECT_MANAGER → DEVOPS |

## 版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.0 | 2026-03-03 | 初始版本 |
