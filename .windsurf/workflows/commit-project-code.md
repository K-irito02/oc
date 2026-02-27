---
description: 项目代码仓库提交工作流 — 提交前后端代码到 GitHub 远程仓库（GitFlow 规范）
---

# 项目代码仓库提交工作流

> 将 E:\oc\qt-platform 目录下的项目代码提交到 GitHub 远程仓库

## 触发条件

当用户请求以下操作时触发：
- "提交代码"、"commit code"、"push code"
- "提交项目"、"commit project"
- "推送代码"、"push project"

---

## 提交流程

### 1. 切换到项目代码仓库目录

工作目录：`e:\oc\qt-platform`

### 2. 检查 Git 状态

// turbo
```powershell
git status --short
```

如果没有任何变更，提示用户"没有需要提交的更改"并结束。

### 3. 查看变更详情（可选）

// turbo
```powershell
git diff --stat
```

> **注意**: 可能会看到 LF/CRLF 警告，这是 Windows 环境正常现象，不影响提交。

### 4. 添加所有变更文件

// turbo
```powershell
git add .
```

### 5. 确认暂存区状态

// turbo
```powershell
git status
```

### 6. 提交变更

```powershell
git commit -m "<type>: <description>"
```

**提交类型规范（Conventional Commits）：**
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `style:` 代码格式调整（不影响功能）
- `refactor:` 重构（不是新功能也不是修复）
- `test:` 测试相关
- `chore:` 构建或辅助工具变动
- `perf:` 性能优化
- `ci:` CI/CD 相关

**示例：**
```powershell
git commit -m "feat: 添加评论回复功能"
git commit -m "fix: 修复文件下载HTTP 400错误"
git commit -m "style: 统一管理后台搜索框高度"
git commit -m "docs: 更新README文档"
```

### 7. 推送到远程仓库

**推送到 develop 分支（日常开发）：**
```powershell
git push origin develop
```

**推送到 main 分支（仅用于发布）：**
```powershell
git push origin main
```

### 8. 验证推送结果

// turbo
```powershell
git log --oneline -3
```

---

## 实际提交示例

以下是 2026-02-28 的实际提交记录：

```
c26498c feat: 添加评论回复功能、修复文件下载、统一管理后台UI
28b5758 feat: 对截图画廊组件的优化升级
a639b44 feat: 完善产品编辑和上传功能，解决截图显示问题
```

---

## GitFlow 分支管理

### 分支结构

```
main            ← 生产环境，仅接受 release 和 hotfix 合并
  │
  ├── develop   ← 开发主分支，接受 feature 合并
  │     │
  │     ├── feature/xxx
  │     └── feature/yyy
  │
  ├── release/x.x.x
  │
  └── hotfix/xxx
```

### 创建功能分支

```powershell
# 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/新功能名称

# 开发完成后合并回 develop
git checkout develop
git merge feature/新功能名称
git push origin develop

# 删除功能分支
git branch -d feature/新功能名称
```

### 创建发布分支

```powershell
# 从 develop 创建发布分支
git checkout develop
git checkout -b release/1.0.0

# 测试完成后合并到 main 和 develop
git checkout main
git merge release/1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin main --tags

git checkout develop
git merge release/1.0.0
git push origin develop

# 删除发布分支
git branch -d release/1.0.0
```

### 创建热修复分支

```powershell
# 从 main 创建热修复分支
git checkout main
git checkout -b hotfix/紧急修复描述

# 修复完成后合并到 main 和 develop
git checkout main
git merge hotfix/紧急修复描述
git push origin main

git checkout develop
git merge hotfix/紧急修复描述
git push origin develop

# 删除热修复分支
git branch -d hotfix/紧急修复描述
```

---

## 仓库配置（首次设置）

### 配置远程仓库

```powershell
cd e:\oc\qt-platform
git remote add origin https://github.com/K-irito02/qt-platform-app.git
```

### 配置 GitHub 认证

使用个人访问令牌 (PAT) 进行认证：

```powershell
git config credential.helper store
```

推送时输入用户名和令牌：
- 用户名: `K-irito02`
- 密码: `<YOUR_GITHUB_PAT>` （从环境变量或密码管理器获取）

### 初始化分支

```powershell
# 确保有 main 和 develop 分支
git checkout -b main
git push -u origin main

git checkout -b develop
git push -u origin develop
```

---

## 提交前检查清单

### 后端检查

```powershell
# 编译检查
mvn clean compile -q

# 跳过测试打包（快速验证）
mvn package -DskipTests -q
```

### 前端检查

```powershell
cd qt-platform-web

# TypeScript 类型检查
npx tsc --noEmit

# 构建检查
npm run build
```

### 代码规范检查

```powershell
# 前端 ESLint
cd qt-platform-web
npm run lint

# 前端格式化
npm run format
```

---

## 常见问题

### 1. 推送被拒绝（远程有更新）

```powershell
# 拉取远程更新后重新推送
git pull origin develop --rebase
git push origin develop
```

### 2. 合并冲突

```powershell
# 查看冲突文件
git status

# 手动解决冲突后
git add .
git commit -m "fix: 解决合并冲突"
git push origin develop
```

### 3. 撤销最后一次提交

```powershell
# 撤销提交但保留更改
git reset --soft HEAD~1

# 撤销提交且丢弃更改（谨慎使用）
git reset --hard HEAD~1
```

### 4. 查看提交历史

```powershell
# 简洁历史
git log --oneline -10

# 详细历史
git log --graph --oneline --all
```

---

## 自动化脚本

### 快速提交脚本

创建 `e:\oc\qt-platform\scripts\quick-commit.ps1`：

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Message
)

# 添加所有更改
git add .

# 提交
git commit -m $Message

# 推送到 develop
git push origin develop

Write-Host "✅ 提交完成: $Message" -ForegroundColor Green
```

使用方式：
```powershell
.\scripts\quick-commit.ps1 -Message "feat: 新功能描述"
```
