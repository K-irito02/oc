# Git 提交工作流 API 参考

本文件提供 Git 提交工作流的 API 参考文档，包括环境状态仓库和项目代码仓库的提交命令和配置。

## 1. 环境状态仓库 API

### 1.1 基本命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `git status --short` | 检查 Git 状态（简洁格式） | `git status --short` |
| `git diff --stat` | 查看变更详情（统计格式） | `git diff --stat` |
| `git add <path>` | 添加文件到暂存区 | `git add .trae/ .windsurf/ Memory/` |
| `git commit -m "<message>"` | 提交变更 | `git commit -m "config: 添加新技能"` |
| `git push <remote> <branch>` | 推送到远程仓库 | `git push origin main` |
| `git log --oneline -<n>` | 查看最近 n 条提交记录 | `git log --oneline -3` |

### 1.2 提交类型

| 类型 | 描述 | 示例 |
|------|------|------|
| `config` | 配置文件更新 | `git commit -m "config: 更新AI技能配置"` |
| `memory` | 记忆文件更新 | `git commit -m "memory: 更新项目记忆"` |
| `docs` | 文档更新 | `git commit -m "docs: 更新架构文档"` |
| `backup` | 创建备份 | `git commit -m "backup: 备份环境配置"` |
| `sync` | 同步配置 | `git commit -m "sync: 同步远程配置"` |

### 1.3 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `remote` | string | `origin` | 远程仓库名称 |
| `branch` | string | `main` | 分支名称 |
| `commitType` | string | `config` | 提交类型 |
| `commitMessage` | string | 必需 | 提交描述 |
| `addPaths` | string[] | `[.trae/, .windsurf/, Memory/, Planning Document/, package.json, README.md]` | 要添加的文件路径 |

### 1.4 脚本 API

**commit-env.ps1**：

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

# 执行提交流程
```

**参数说明**：
- `Type`：提交类型
- `Message`：提交描述
- `Remote`：远程仓库名称
- `Branch`：分支名称

## 2. 项目代码仓库 API

### 2.1 基本命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `git status --short` | 检查 Git 状态（简洁格式） | `git status --short` |
| `git diff --stat` | 查看变更详情（统计格式） | `git diff --stat` |
| `git add .` | 添加所有文件到暂存区 | `git add .` |
| `git commit -m "<message>"` | 提交变更 | `git commit -m "feat: 添加新功能"` |
| `git push <remote> <branch>` | 推送到远程仓库 | `git push origin develop` |
| `git log --oneline -<n>` | 查看最近 n 条提交记录 | `git log --oneline -3` |

### 2.2 提交类型（Conventional Commits）

| 类型 | 描述 | 示例 |
|------|------|------|
| `feat` | 新功能 | `git commit -m "feat: 添加评论功能"` |
| `fix` | 修复 bug | `git commit -m "fix: 修复登录错误"` |
| `docs` | 文档更新 | `git commit -m "docs: 更新API文档"` |
| `style` | 代码格式调整 | `git commit -m "style: 统一代码风格"` |
| `refactor` | 重构 | `git commit -m "refactor: 重构用户服务"` |
| `test` | 测试相关 | `git commit -m "test: 添加单元测试"` |
| `chore` | 构建或辅助工具变动 | `git commit -m "chore: 更新依赖"` |
| `perf` | 性能优化 | `git commit -m "perf: 优化数据库查询"` |
| `ci` | CI/CD 相关 | `git commit -m "ci: 配置GitHub Actions"` |

### 2.3 分支管理命令

| 命令 | 描述 | 示例 |
|------|------|------|
| `git checkout <branch>` | 切换分支 | `git checkout develop` |
| `git checkout -b <branch>` | 创建并切换分支 | `git checkout -b feature/new-feature` |
| `git merge <branch>` | 合并分支 | `git merge feature/new-feature` |
| `git branch -d <branch>` | 删除分支 | `git branch -d feature/new-feature` |
| `git tag -a <tag> -m "<message>"` | 创建标签 | `git tag -a v1.0.0 -m "Release 1.0.0"` |
| `git push origin --tags` | 推送标签 | `git push origin --tags` |

### 2.4 配置选项

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `remote` | string | `origin` | 远程仓库名称 |
| `branch` | string | `develop` | 分支名称 |
| `commitType` | string | `feat` | 提交类型 |
| `commitMessage` | string | 必需 | 提交描述 |
| `buildCheck` | boolean | `true` | 是否进行构建检查 |
| `lintCheck` | boolean | `true` | 是否进行代码规范检查 |

### 2.5 脚本 API

**quick-commit.ps1**：

```powershell
param(
    [Parameter(Mandatory=$true)]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Branch = "develop",
    [string]$Remote = "origin",
    [bool]$BuildCheck = $true,
    [bool]$LintCheck = $true
)

# 执行提交流程
```

**参数说明**：
- `Type`：提交类型
- `Message`：提交描述
- `Branch`：分支名称
- `Remote`：远程仓库名称
- `BuildCheck`：是否进行构建检查
- `LintCheck`：是否进行代码规范检查

## 3. 分支管理 API

### 3.1 GitFlow 分支结构

| 分支类型 | 描述 | 来源 | 合并目标 |
|---------|------|------|----------|
| `main` | 生产环境分支 | 初始分支 | - |
| `develop` | 开发主分支 | `main` | - |
| `feature/*` | 功能分支 | `develop` | `develop` |
| `release/*` | 发布分支 | `develop` | `main`, `develop` |
| `hotfix/*` | 热修复分支 | `main` | `main`, `develop` |

### 3.2 分支操作

**创建功能分支**：
```powershell
git checkout develop
git pull origin develop
git checkout -b feature/新功能名称
```

**合并功能分支**：
```powershell
git checkout develop
git merge feature/新功能名称
git push origin develop
git branch -d feature/新功能名称
```

**创建发布分支**：
```powershell
git checkout develop
git checkout -b release/1.0.0
```

**合并发布分支**：
```powershell
git checkout main
git merge release/1.0.0
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin main --tags

git checkout develop
git merge release/1.0.0
git push origin develop
git branch -d release/1.0.0
```

**创建热修复分支**：
```powershell
git checkout main
git checkout -b hotfix/紧急修复描述
```

**合并热修复分支**：
```powershell
git checkout main
git merge hotfix/紧急修复描述
git push origin main

git checkout develop
git merge hotfix/紧急修复描述
git push origin develop
git branch -d hotfix/紧急修复描述
```

## 4. 提交前检查 API

### 4.1 后端检查

| 命令 | 描述 | 示例 |
|------|------|------|
| `mvn clean compile -q` | 编译检查 | `mvn clean compile -q` |
| `mvn package -DskipTests -q` | 跳过测试打包 | `mvn package -DskipTests -q` |
| `mvn test -q` | 运行测试 | `mvn test -q` |

### 4.2 前端检查

| 命令 | 描述 | 示例 |
|------|------|------|
| `npx tsc --noEmit` | TypeScript 类型检查 | `npx tsc --noEmit` |
| `npm run build` | 构建检查 | `npm run build` |
| `npm run lint` | 代码规范检查 | `npm run lint` |
| `npm run format` | 代码格式化 | `npm run format` |

### 4.3 安全检查

| 命令 | 描述 | 示例 |
|------|------|------|
| `git ls-files --other --ignored --exclude-standard` | 检查忽略的文件 | `git ls-files --other --ignored --exclude-standard` |
| `git diff HEAD~1 --name-only` | 查看最近一次提交的文件 | `git diff HEAD~1 --name-only` |
| `grep -r "api_key\|token\|secret" --include="*.js" --include="*.ts" --include="*.json" .` | 检查敏感信息 | `grep -r "api_key\|token\|secret" --include="*.js" --include="*.ts" --include="*.json" .` |

## 5. 故障排除 API

### 5.1 常见错误处理

| 错误 | 命令 | 描述 |
|------|------|------|
| 推送被拒绝 | `git pull origin <branch> --rebase` | 拉取远程更新后重新推送 |
| 合并冲突 | `git status` | 查看冲突文件 |
| 撤销提交 | `git reset --soft HEAD~1` | 撤销提交但保留更改 |
| 强制推送 | `git push origin <branch> --force-with-lease` | 安全地强制推送 |
| 清理分支 | `git branch -d <branch>` | 删除已合并的分支 |

### 5.2 日志和历史

| 命令 | 描述 | 示例 |
|------|------|------|
| `git log --oneline -<n>` | 查看最近 n 条提交记录 | `git log --oneline -10` |
| `git log --graph --oneline --all` | 查看所有分支的提交历史 | `git log --graph --oneline --all` |
| `git show <commit>` | 查看指定提交的详细信息 | `git show c5b225b` |
| `git blame <file>` | 查看文件的每行修改历史 | `git blame src/App.tsx` |

### 5.3 仓库维护

| 命令 | 描述 | 示例 |
|------|------|------|
| `git gc` | 垃圾回收 | `git gc` |
| `git prune` | 清理未引用的对象 | `git prune` |
| `git fetch --prune` | 清理远程已删除的分支 | `git fetch --prune` |
| `git remote prune origin` | 清理远程已删除的分支 | `git remote prune origin` |

## 6. 配置 API

### 6.1 Git 配置

| 命令 | 描述 | 示例 |
|------|------|------|
| `git config --global user.name "<name>"` | 配置全局用户名 | `git config --global user.name "John Doe"` |
| `git config --global user.email "<email>"` | 配置全局邮箱 | `git config --global user.email "john@example.com"` |
| `git config --global credential.helper store` | 配置凭证存储 | `git config --global credential.helper store` |
| `git config --global core.autocrlf true` | 配置换行符处理 | `git config --global core.autocrlf true` |
| `git config --global push.default simple` | 配置默认推送行为 | `git config --global push.default simple` |

### 6.2 远程仓库配置

| 命令 | 描述 | 示例 |
|------|------|------|
| `git remote add <name> <url>` | 添加远程仓库 | `git remote add origin https://github.com/K-irito02/oc.git` |
| `git remote set-url <name> <url>` | 修改远程仓库 URL | `git remote set-url origin https://github.com/K-irito02/oc.git` |
| `git remote -v` | 查看远程仓库 | `git remote -v` |
| `git remote show <name>` | 查看远程仓库详情 | `git remote show origin` |

### 6.3 分支配置

| 命令 | 描述 | 示例 |
|------|------|------|
| `git branch -M <branch>` | 重命名分支 | `git branch -M main` |
| `git branch --set-upstream-to=origin/<branch>` | 设置上游分支 | `git branch --set-upstream-to=origin/develop` |
| `git branch -a` | 查看所有分支 | `git branch -a` |
| `git branch -r` | 查看远程分支 | `git branch -r` |

## 7. 脚本 API

### 7.1 环境状态仓库脚本

**commit-env.ps1**：

```powershell
# 功能：提交环境状态仓库
# 参数：
#   -Type: 提交类型 (config, memory, docs, backup, sync)
#   -Message: 提交描述
#   -Remote: 远程仓库名称 (默认: origin)
#   -Branch: 分支名称 (默认: main)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("config", "memory", "docs", "backup", "sync")]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

# 切换到项目根目录
Set-Location "e:\oc"

# 检查 Git 状态
Write-Host "🔍 检查 Git 状态..." -ForegroundColor Cyan
git status --short

# 查看变更详情
Write-Host "📋 查看变更详情..." -ForegroundColor Cyan
git diff --stat

# 添加核心配置目录
Write-Host "📁 添加变更文件..." -ForegroundColor Cyan
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md

# 确认暂存区状态
Write-Host "✅ 确认暂存区状态..." -ForegroundColor Cyan
git status

# 提交变更
Write-Host "💾 提交变更..." -ForegroundColor Cyan
git commit -m "$Type: $Message"

# 推送到远程仓库
Write-Host "🚀 推送到远程仓库..." -ForegroundColor Cyan
git push $Remote $Branch

# 验证推送结果
Write-Host "✅ 提交完成！" -ForegroundColor Green
git log --oneline -3
```

### 7.2 项目代码仓库脚本

**quick-commit.ps1**：

```powershell
# 功能：提交项目代码仓库
# 参数：
#   -Type: 提交类型 (feat, fix, docs, style, refactor, test, chore, perf, ci)
#   -Message: 提交描述
#   -Branch: 分支名称 (默认: develop)
#   -Remote: 远程仓库名称 (默认: origin)
#   -BuildCheck: 是否进行构建检查 (默认: $true)
#   -LintCheck: 是否进行代码规范检查 (默认: $true)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("feat", "fix", "docs", "style", "refactor", "test", "chore", "perf", "ci")]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Branch = "develop",
    [string]$Remote = "origin",
    [bool]$BuildCheck = $true,
    [bool]$LintCheck = $true
)

# 切换到项目代码仓库目录
Set-Location "e:\oc\oc-platform"

# 检查 Git 状态
Write-Host "🔍 检查 Git 状态..." -ForegroundColor Cyan
git status --short

# 查看变更详情
Write-Host "📋 查看变更详情..." -ForegroundColor Cyan
git diff --stat

# 前端检查
if ($LintCheck) {
    Write-Host "🔧 前端代码规范检查..." -ForegroundColor Cyan
    Set-Location "oc-platform-web"
    npm run lint
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 代码规范检查失败！" -ForegroundColor Red
        exit 1
    }
    Set-Location ".."
}

# 构建检查
if ($BuildCheck) {
    Write-Host "🏗️  构建检查..." -ForegroundColor Cyan
    Set-Location "oc-platform-web"
    npm run build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ 构建检查失败！" -ForegroundColor Red
        exit 1
    }
    Set-Location ".."
}

# 添加所有变更文件
Write-Host "📁 添加变更文件..." -ForegroundColor Cyan
git add .

# 确认暂存区状态
Write-Host "✅ 确认暂存区状态..." -ForegroundColor Cyan
git status

# 提交变更
Write-Host "💾 提交变更..." -ForegroundColor Cyan
git commit -m "$Type: $Message"

# 推送到远程仓库
Write-Host "🚀 推送到 $Branch 分支..." -ForegroundColor Cyan
git push $Remote $Branch

# 验证推送结果
Write-Host "✅ 提交完成！" -ForegroundColor Green
git log --oneline -3
```

## 8. 集成 API

### 8.1 CI/CD 集成

**GitHub Actions 示例**：

```yaml
# .github/workflows/commit-check.yml
name: Commit Check

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          cache: 'npm'
      
      - name: Install dependencies
        run: npm install
      
      - name: TypeScript check
        run: npx tsc --noEmit
      
      - name: Build check
        run: npm run build
      
      - name: Lint check
        run: npm run lint
```

### 8.2 预提交钩子

**pre-commit 配置**：

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
        args: ['--maxkb=500']

  - repo: https://github.com/typicode/eslint-pre-commit-hook
    rev: v9.13.0
    hooks:
      - id: eslint
        types: [file]
        files: \.(ts|tsx|js|jsx)$
        additional_dependencies: [eslint@9.13.0]
```

### 8.3 编辑器集成

**VS Code 配置**：

```json
// .vscode/settings.json
{
  "git.enableSmartCommit": true,
  "git.autofetch": true,
  "gitlens.views.commits.showStashes": true,
  "gitlens.views.commits.showRebaseInteractive