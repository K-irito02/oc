# OC - 项目环境状态仓库

> 开发环境配置、AI 技能、工作流和项目记忆的版本控制仓库

---

## 概述

本仓库用于管理 OC Platform 项目的开发环境状态，包括：
- **AI 配置**: Trae/Windsurf AI 的规则、技能和工作流
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
| **项目环境状态** | `E:/oc/` | AI 配置、记忆、文档 | [oc-env-state](https://github.com/K-irito02/oc) |
| **项目代码** | `E:/oc/oc-platform/` | 前后端代码、数据库脚本 | [oc-platform-app](https://github.com/K-irito02/oc-platform-app) |

## 工作流

### 提交环境配置

```powershell
# 使用 /commit-env-state 工作流
# 或手动执行：
cd e:\oc
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md
git commit -m "config: 更新描述"
git push origin main
```

### 提交项目代码

```powershell
# 使用 /commit-project-code 工作流
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
| `frontend-design` | 创建生产级前端界面 |
| `ui-ux-pro-max` | UI/UX 设计智能助手 |
| `oc-platform-manager` | oc Platform 项目自动化管理 |
| `git-commit-workflow` | Git 提交工作流 |
| `code-reviewer` | 代码审查 |
| `fix` | 代码修复和格式化 |
| `pr-creator` | Pull Request 创建 |
| `vite-cache-components` | Vite 缓存组件和 PPR 实现 |
| `webapp-testing` | Web 应用测试 |
| `update-docs` | 文档更新 |
| `find-skills` | 技能发现和安装 |
| `fullstack-developer` | 全栈开发助手 |
| `frontend-code-review` | 前端代码审查 |

### Windsurf AI 技能

| 技能 | 用途 |
|------|------|
| `oc-platform-manager` | oc Platform 项目自动化管理 |
| `git-commit-workflow` | Git 提交工作流 |
| `ui-ux-pro-max` | UI/UX 设计智能助手 |
| `vite-cache-components` | Vite 缓存组件和 PPR 实现 |

## AI 工作流

| 工作流 | 触发词 | 用途 |
|--------|--------|------|
| `/start-project` | 启动项目 | 一键启动所有开发服务 |
| `/stop-project` | 停止项目 | 停止所有开发服务 |
| `/memory` | @/memory | 管理项目记忆 |
| `/commit-env-state` | 提交环境配置 | 提交环境状态到 GitHub |
| `/commit-project-code` | 提交代码 | 提交项目代码到 GitHub |

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
git clone https://github.com/K-irito02/oc-env-state.git e:\oc
cd e:\oc
```

### 2. 克隆项目代码

```powershell
git clone https://github.com/K-irito02/oc-platform-app.git e:\oc\oc-platform
```

### 3. 启动开发环境

使用 `/start-project` 工作流或手动执行：

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

## 测试账号

- **管理员**: admin@ocplatform.com / Admin@123456
- **普通用户**: zhangsan@example.com / Test@123456

---

## License

Private
