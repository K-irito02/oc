---
description: Git 分支策略
scope: project
trigger: always_on
---

# Git 分支策略规则

## 分支结构

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
  ├── hotfix/fix-login-bug
  │
  └── workspace-config ← 开发环境配置分支，保存根目录配置文件
```

## 分支命名规范

- **main**: 生产环境分支，保护分支，禁止直接推送
- **develop**: 开发主分支，集成所有功能分支
- **feature/***: 功能分支，命名格式 `feature/功能描述`
- **release/***: 发布分支，命名格式 `release/版本号`
- **hotfix/***: 热修复分支，命名格式 `hotfix/问题描述`
- **workspace-config**: 开发环境配置分支，保存根目录配置和开发过程状态

## 分支合并规则

1. **feature** → **develop**: 功能完成后合并到开发分支
2. **develop** → **release**: 准备发布时创建发布分支
3. **release** → **main**: 测试通过后合并到生产分支
4. **hotfix** → **main**: 紧急修复直接合并到生产分支
5. **hotfix** → **develop**: 热修复也需要同步到开发分支
6. **workspace-config** → **main**: 配置更新可定期同步到生产分支

## workspace-config 分支说明

### 分支用途
`workspace-config` 分支专门用于保存和管理开发环境的完整配置状态，包括：

#### 📁 保存的文件类型
`workspace-config` 分支仅保存以下核心配置目录：

- **.trae/**: Trae AI 配置和技能文件
- **.windsurf/**: Windsurf AI 配置、规则、技能和工作流文件
- **Memory/**: 项目记忆系统（后端、前端、数据库、运维、测试记忆）
- **Planning Document/**: 计划文档（架构文档、阶段设计、主题设计）

#### 🚫 文件限制策略
为保持分支轻量和高效，以下文件类型将被排除：

- **视频文件**: `*.mp4`, `*.avi`, `*.mov`, `*.mkv`, `*.flv`
- **大文件**: 超过 10MB 的文件
- **临时文件**: `*.tmp`, `*.log`, `*.cache`
- **依赖文件**: `node_modules/`, `.git/`, `target/`, `dist/`
- **IDE缓存**: `.vscode/`, `.idea/` 的缓存文件
- **系统文件**: `*.DS_Store`, `Thumbs.db`

## 分支保护

- main 分支启用分支保护
- require pull request reviews
- require status checks to pass before merging
- include administrators

## 提交规范

使用 Conventional Commits 规范：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建或辅助工具变动

## 项目结构

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
├── qt-platform/              # 主项目目录
├── node_modules/             # Node.js 依赖（不同步）
├── package.json              # 根包配置
└── package-lock.json         # 依赖锁定文件
```
