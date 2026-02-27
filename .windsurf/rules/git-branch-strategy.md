---
description: Git 分支策略
scope: project
trigger: always_on
---

# Git 分支策略规则

## 仓库分离策略

### 1. 项目环境状态文件仓库 (E:\oc)
专门保存开发环境配置和项目记忆的独立仓库：
- **仓库路径**: `E:/oc/`
- **主要用途**: 保存 AI 配置、规则、技能、工作流和项目记忆
- **分支策略**: 简化的单分支或双分支模式

### 2. 项目代码仓库 (E:\oc\qt-platform)
专门保存项目源代码的独立仓库：
- **仓库路径**: `E:/oc/qt-platform/`
- **主要用途**: 保存前后端代码、数据库脚本、部署配置
- **分支策略**: 完整的 GitFlow 工作流

## 项目代码仓库分支结构

```
main            ← 生产环境，仅接受 release 和 hotfix 合并
  │
  ├── develop   ← 开发主分支，接受 feature 合并
  │     │
  │     ├── feature/user-auth
  │     ├── feature/product-list
  │     └── feature/admin-panel
  │
  ├── release/1.0.0
  │
  └── hotfix/fix-login-bug
```

## 项目代码仓库分支命名规范

- **main**: 生产环境分支，保护分支，禁止直接推送
- **develop**: 开发主分支，集成所有功能分支
- **feature/***: 功能分支，命名格式 `feature/功能描述`
- **release/***: 发布分支，命名格式 `release/版本号`
- **hotfix/***: 热修复分支，命名格式 `hotfix/问题描述`

## 项目环境状态仓库分支策略

### 分支命名规范
- **main**: 主分支，保存稳定的配置和记忆
- **develop**: 开发分支，保存最新的配置变更（可选）
- **backup/***: 备份分支，按日期命名 `backup/2026-02-28`

### 推荐策略
- **简单场景**: 使用单分支 `main` 模式
- **频繁更新**: 使用双分支 `main` + `develop` 模式
- **重要节点**: 创建备份分支 `backup/日期`

## 项目代码仓库分支合并规则

1. **feature** → **develop**: 功能完成后合并到开发分支
2. **develop** → **release**: 准备发布时创建发布分支
3. **release** → **main**: 测试通过后合并到生产分支
4. **hotfix** → **main**: 紧急修复直接合并到生产分支
5. **hotfix** → **develop**: 热修复也需要同步到开发分支

## 项目环境状态仓库分支合并规则

1. **develop** → **main**: 配置稳定后合并到主分支
2. **main** → **backup/日期**: 重要节点创建备份分支
3. **backup/日期** → **main**: 恢复特定版本的配置（谨慎操作）

## 项目环境状态仓库说明

### 仓库用途
项目环境状态仓库专门用于保存和管理开发环境的完整配置状态，包括：

#### 📁 保存的文件类型
项目环境状态仓库仅保存以下核心配置目录：

- **.trae/**: Trae AI 配置和技能文件
- **.windsurf/**: Windsurf AI 配置、规则、技能和工作流文件
- **Memory/**: 项目记忆系统（后端、前端、数据库、运维、测试记忆）
- **Planning Document/**: 计划文档（架构文档、阶段设计、主题设计）
- **package.json**: 根目录包配置文件

#### 🚫 文件限制策略
为保持仓库轻量和高效，以下文件类型将被排除：

- **视频文件**: `*.mp4`, `*.avi`, `*.mov`, `*.mkv`, `*.flv`
- **大文件**: 超过 10MB 的文件
- **临时文件**: `*.tmp`, `*.log`, `*.cache`
- **依赖文件**: `node_modules/`, `.git/`, `target/`, `dist/`
- **IDE缓存**: `.vscode/`, `.idea/` 的缓存文件
- **系统文件**: `*.DS_Store`, `Thumbs.db`
- **项目代码**: `qt-platform/` 目录（独立仓库管理）
- **依赖锁文件**: `package-lock.json`（可重新生成）

## 分支保护

### 项目代码仓库
- main 分支启用分支保护
- require pull request reviews
- require status checks to pass before merging
- include administrators

### 项目环境状态仓库
- main 分支可选择性启用分支保护
- 根据团队规模和协作需求决定
- 建议启用基础保护，防止意外删除

## 提交规范

使用 Conventional Commits 规范：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建或辅助工具变动

### 项目环境状态仓库特殊规范
- `config:` 配置文件更新
- `memory:` 记忆文件更新
- `docs:` 文档更新（规则、技能、工作流）
- `backup:` 创建备份分支
- `sync:` 同步配置更新

## 项目代码仓库结构

### Qt Platform 项目结构
```
qt-platform/
├── qt-platform-web/          # 前端项目（React 18 + Vite 5 + TypeScript）
├── qt-platform-user/         # 用户模块
├── qt-platform-product/      # 产品模块
├── qt-platform-comment/      # 评论模块
├── qt-platform-file/         # 文件模块（MinIO 对象存储）
├── qt-platform-notification/ # 通知模块
├── qt-platform-admin/        # 管理后台模块
├── qt-platform-app/           # 应用启动模块
├── qt-platform-common/        # 公共模块（JSONB 类型处理器等）
├── sql/                       # 数据库脚本
├── docker-compose.dev.yml    # 开发环境配置
└── docker-compose.yml         # 生产环境配置
```

## 项目环境状态仓库结构

### 开发环境根目录结构 (E:\oc)
```
E:/oc/
├── .trae/                     # Trae AI 配置
│   ├── documents/            # 文档文件
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
│   └── WorkLogs/              # 工作日志
├── Planning Document/         # 计划文档
│   ├── Architecture Document.md
│   ├── Phase One.md
│   └── 主题设计.md
├── Front-end testing/         # 前端测试素材（不同步）
│   ├── Background material/
│   └── PFP/
├── qt-platform/              # 项目代码仓库（独立管理）
├── node_modules/             # Node.js 依赖（不同步）
├── package.json              # 根包配置（同步）
└── package-lock.json         # 依赖锁定文件（不同步）
```
