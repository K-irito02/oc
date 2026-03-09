# OC - 项目环境状态仓库

> 开发环境配置、AI 技能、工作流和项目记忆的版本控制仓库

---

## 概述

本仓库用于管理 OC Platform 项目的开发环境状态，包括：
- **AI 配置**: Trae AI 的规则、技能和工作流
- **项目记忆**: AI 辅助开发的持久化记忆系统
- **计划文档**: 架构设计、阶段规划等文档

## 目录结构

```
E:/oc/
├── .trae/                     # Trae AI 配置
│   ├── documents/             # 文档文件
│   ├── rules/                 # 规则文件
│   └── skills/                # 技能文件
├── .windsurf/                 # Windsurf AI 配置
│   ├── rules/                 # 开发规则文件
│   ├── skills/                # AI 技能文件
│   └── workflows/             # 工作流文件
├── Memory/                    # 项目记忆系统
│   ├── Backend/               # 后端记忆
│   ├── Frontend/              # 前端记忆
│   ├── Database/              # 数据库记忆
│   ├── DevOps/                # 运维记忆
│   ├── Testing/               # 测试记忆
│   └── WorkLogs/              # AI 工作日志
├── Planning Document/         # 计划文档
│   ├── Architecture Document.md
│   ├── Phase One.md
│   └── 主题设计.md
├── oc-platform/               # 项目代码仓库（独立管理）
├── package.json               # 根包配置
└── README.md                  # 本文件
```

## 关联仓库

| 仓库 | 路径 | 用途 | GitHub |
|------|------|------|--------|
| **项目环境状态** | `E:/oc/` | AI 配置、记忆、文档 | [oc](https://github.com/K-irito02/oc) |
| **项目代码** | `E:/oc/oc-platform/` | 前后端代码、数据库脚本 | [oc-platform-app](https://github.com/K-irito02/oc-platform-app) |

## 工作流

### 提交环境配置

```powershell
# 使用 git-commit-workflow 技能
# 或手动执行：
cd e:\oc
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md
git commit -m "config: 更新描述"
git push origin main
```

### 提交项目代码

```powershell
# 使用 git-commit-workflow 技能
# 或手动执行：
cd e:\oc\oc-platform
git add .
git commit -m "feat: 功能描述"
git push origin develop
```

## AI 技能

### Trae AI 技能

| 技能 | 用途 |
|------|------|
| `ui-ux-pro-max` | UI/UX 设计智能助手 |
| `oc-platform-manager` | OC Platform 项目自动化管理 |
| `git-commit-workflow` | Git 提交工作流 |
| `code-reviewer` | 代码审查 |
| `fix` | 代码修复和格式化 |
| `pr-creator` | Pull Request 创建 |
| `vite-cache-components` | Vite 缓存组件和 PPR 实现 |
| `webapp-testing` | Web 应用测试 |
| `find-skills` | 技能发现和安装 |

### 内置专家智能体

| 智能体 | 用途 |
|--------|------|
| `fullstack-dev-expert` | 全栈开发专家 |
| `frontend-expert` | 前端开发专家 |
| `backend-expert` | 后端开发专家 |
| `testing-expert` | 测试专家 |
| `devops-expert` | DevOps 专家 |
| `code-review-expert` | 代码审查专家 |

## AI 规则文件

| 规则文件 | 说明 |
|----------|------|
| `agent-transformation.md` | 智能体转换规则 |
| `api-documentation.md` | API 文档规范 |
| `backend-code-standards.md` | 后端代码规范 |
| `development-environment.md` | 开发环境搭建说明 |
| `development-quickstart.md` | 开发环境快速启动指南 |
| `frontend-code-standards.md` | 前端代码规范 |
| `git-branch-strategy.md` | Git 分支策略 |
| `skill-and-mcp-usage.md` | 技能和MCP使用规则 |
| `tech-stack-selection.md` | 技术栈选型规范 |

## 项目记忆系统

| 记忆文件 | 说明 |
|----------|------|
| `Memory/README.md` | 记忆索引 |
| `Memory/Backend/architecture.md` | 后端架构记忆 |
| `Memory/Backend/api.md` | API 接口清单 |
| `Memory/Backend/security.md` | 安全体系记忆 |
| `Memory/Frontend/architecture.md` | 前端架构记忆 |
| `Memory/Frontend/pages.md` | 页面清单 |
| `Memory/Frontend/theme.md` | 主题系统记忆 |
| `Memory/Database/schema.md` | 数据库结构记忆 |
| `Memory/DevOps/deployment.md` | 部署运维记忆 |
| `Memory/Testing/status.md` | 测试状态记忆 |
| `Memory/WorkLogs/` | AI 工作日志 |

## 排除文件

以下文件/目录不纳入版本控制：

- `oc-platform/` — 项目代码（独立仓库管理）
- `node_modules/` — 依赖文件
- `Front-end testing/` — 测试素材（大文件）
- `package-lock.json` — 锁定文件
- `*.mp4`, `*.avi`, `*.exe` — 大文件

## 快速开始

### 1. 克隆仓库

```powershell
git clone https://github.com/K-irito02/oc.git e:\oc
cd e:\oc
```

### 2. 克隆项目代码

```powershell
git clone https://github.com/K-irito02/oc-platform-app.git e:\oc\oc-platform
```

### 3. 启动开发环境

使用 `oc-platform-manager` 技能或手动执行：

```powershell
cd e:\oc\oc-platform
docker compose -f docker-compose.dev.yml up -d
mvn clean package -DskipTests -pl oc-platform-app -am -q
java -jar oc-platform-app\target\oc-platform-app-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev
cd oc-platform-web && npm run dev
```

## 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 5173 / 5174 | Vite 开发服务器 |
| 后端 API | 8081 | Spring Boot |
| PostgreSQL | 5433 | 数据库 |
| Redis | 6380 | 缓存 |
| MinIO | 9000 / 9001 | 对象存储 |

## 技术栈

### 前端
- React 18.3.1 + TypeScript 5.6
- Vite 5.4 + Tailwind CSS 3.4
- Ant Design 6.3 + Redux Toolkit 2.11
- React Router 7.13 + react-i18next 16.5

### 后端
- Spring Boot 3.2.12 + Java 17
- MyBatis-Plus 3.5.9 + PostgreSQL 15
- Redis 7 + MinIO

### 基础设施
- Docker + Docker Compose
- GitHub Actions CI/CD
- Nginx

## 超级管理员账号

- **用户名**: xxxx
- **邮箱**: xxxxxxxxx

---

## License

Private
