# Git 提交工作流模式

本文件提供 Git 提交工作流的最佳实践模式，包括环境状态仓库和项目代码仓库的提交规范。

## 1. 环境状态仓库提交模式

### 1.1 基本提交流程

```powershell
# 1. 检查 Git 状态
git status --short

# 2. 查看变更详情（可选）
git diff --stat

# 3. 添加核心配置目录
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md

# 4. 确认暂存区状态
git status

# 5. 提交变更
git commit -m "<type>: <description>"

# 6. 推送到远程仓库
git push origin main

# 7. 验证推送结果
git log --oneline -3
```

### 1.2 提交类型规范

| 提交类型 | 描述 | 示例 |
|---------|------|------|
| `config` | 配置文件更新 | `config: 添加新的AI技能和工作流` |
| `memory` | 记忆文件更新 | `memory: 更新后端API记忆和测试状态` |
| `docs` | 文档更新（规则、技能、工作流） | `docs: 更新架构文档` |
| `backup` | 创建备份 | `backup: 备份2026-03-03环境配置` |
| `sync` | 同步配置更新 | `sync: 同步远程配置到本地` |

### 1.3 排除文件配置

```gitignore
# 项目代码仓库（独立管理）
oc-platform/

# 依赖目录
node_modules/

# 锁定文件
package-lock.json

# 前端测试素材（大文件）
Front-end testing/

# 视频文件
*.mp4
*.avi
*.mov
*.mkv
*.flv

# 大文件
*.exe
*.msi
*.dmg

# 临时文件
*.tmp
*.log
*.cache

# IDE 缓存
.vscode/
.idea/

# 系统文件
.DS_Store
Thumbs.db
```

## 2. 项目代码仓库提交模式

### 2.1 基本提交流程

```powershell
# 1. 切换到项目代码仓库目录
cd e:\oc\oc-platform

# 2. 检查 Git 状态
git status --short

# 3. 查看变更详情（可选）
git diff --stat

# 4. 添加所有变更文件
git add .

# 5. 确认暂存区状态
git status

# 6. 提交变更
git commit -m "<type>: <description>"

# 7. 推送到远程仓库（开发分支）
git push origin develop

# 或推送到主分支（仅用于发布）
git push origin main

# 8. 验证推送结果
git log --oneline -3
```

### 2.2 提交类型规范（Conventional Commits）

| 提交类型 | 描述 | 示例 |
|---------|------|------|
| `feat` | 新功能 | `feat: 添加评论回复功能` |
| `fix` | 修复 bug | `fix: 修复文件下载HTTP 400错误` |
| `docs` | 文档更新 | `docs: 更新README文档` |
| `style` | 代码格式调整（不影响功能） | `style: 统一管理后台搜索框高度` |
| `refactor` | 重构（不是新功能也不是修复） | `refactor: 重构用户认证逻辑` |
| `test` | 测试相关 | `test: 添加单元测试` |
| `chore` | 构建或辅助工具变动 | `chore: 更新依赖版本` |
| `perf` | 性能优化 | `perf: 优化数据库查询` |
| `ci` | CI/CD 相关 | `ci: 配置GitHub Actions` |

### 2.3 GitFlow 分支管理模式

#### 2.3.1 分支结构

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

#### 2.3.2 创建功能分支

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

#### 2.3.3 创建发布分支

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

#### 2.3.4 创建热修复分支

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

## 3. 自动化脚本模式

### 3.1 环境状态仓库快速提交脚本

```powershell
# e:\oc\scripts\commit-env.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message
)

# 检查 Git 状态
Write-Host "🔍 检查 Git 状态..." -ForegroundColor Cyan
git status --short

# 添加核心配置目录
Write-Host "📁 添加变更文件..." -ForegroundColor Cyan
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md

# 提交变更
Write-Host "💾 提交变更..." -ForegroundColor Cyan
git commit -m "$Type: $Message"

# 推送到远程仓库
Write-Host "🚀 推送到远程仓库..." -ForegroundColor Cyan
git push origin main

# 验证推送结果
Write-Host "✅ 提交完成！" -ForegroundColor Green
git log --oneline -3
```

### 3.2 项目代码仓库快速提交脚本

```powershell
# e:\oc\oc-platform\scripts\quick-commit.ps1
param(
    [Parameter(Mandatory=$true)]
    [string]$Type,
    [Parameter(Mandatory=$true)]
    [string]$Message,
    [string]$Branch = "develop"
)

# 切换到项目代码仓库目录
cd e:\oc\oc-platform

# 检查 Git 状态
Write-Host "🔍 检查 Git 状态..." -ForegroundColor Cyan
git status --short

# 添加所有变更文件
Write-Host "📁 添加变更文件..." -ForegroundColor Cyan
git add .

# 提交变更
Write-Host "💾 提交变更..." -ForegroundColor Cyan
git commit -m "$Type: $Message"

# 推送到指定分支
Write-Host "🚀 推送到 $Branch 分支..." -ForegroundColor Cyan
git push origin $Branch

# 验证推送结果
Write-Host "✅ 提交完成！" -ForegroundColor Green
git log --oneline -3
```

## 4. 提交前检查模式

### 4.1 项目代码仓库检查清单

**后端检查**：
```powershell
# 编译检查
mvn clean compile -q

# 跳过测试打包（快速验证）
mvn package -DskipTests -q
```

**前端检查**：
```powershell
cd oc-platform-web

# TypeScript 类型检查
npx tsc --noEmit

# 构建检查
npm run build

# 代码规范检查
npm run lint

# 代码格式化
npm run format
```

### 4.2 环境状态仓库检查清单

```powershell
# 检查是否有敏感信息
Write-Host "🔍 检查敏感信息..." -ForegroundColor Cyan

# 检查大文件
Write-Host "📦 检查大文件..." -ForegroundColor Cyan
git ls-files --other --ignored --exclude-standard | head -20

# 检查 .gitignore 配置
Write-Host "📝 检查 .gitignore 配置..." -ForegroundColor Cyan
Get-Content .gitignore
```

## 5. 故障排除模式

### 5.1 GitHub Push Protection 拒绝

```powershell
# 撤销提交但保留更改
git reset --soft HEAD~1

# 修改文件移除敏感信息
# 重新添加和提交
git add .
git commit -m "config: 提交描述"
git push origin main
```

### 5.2 推送被拒绝（远程有更新）

```powershell
# 拉取远程更新后重新推送
git pull origin develop --rebase
git push origin develop
```

### 5.3 合并冲突

```powershell
# 查看冲突文件
git status

# 手动解决冲突后
git add .
git commit -m "fix: 解决合并冲突"
git push origin develop
```

### 5.4 撤销最后一次提交

```powershell
# 撤销提交但保留更改
git reset --soft HEAD~1

# 撤销提交且丢弃更改（谨慎使用）
git reset --hard HEAD~1
```

## 6. 团队协作模式

### 6.1 代码审查工作流

1. **创建功能分支**：从 develop 分支创建功能分支
2. **开发完成**：在功能分支上完成开发和测试
3. **提交代码**：遵循 Conventional Commits 规范提交代码
4. **创建 Pull Request**：向 develop 分支创建 PR
5. **代码审查**：团队成员进行代码审查
6. **合并分支**：审查通过后合并到 develop 分支
7. **删除分支**：删除已合并的功能分支

### 6.2 发布工作流

1. **创建发布分支**：从 develop 分支创建发布分支
2. **测试验证**：在发布分支上进行测试和修复
3. **合并到 main**：测试通过后合并到 main 分支并打标签
4. **同步到 develop**：将发布分支合并回 develop 分支
5. **部署**：基于 main 分支进行部署
6. **删除发布分支**：删除已完成的发布分支

### 6.3 热修复工作流

1. **创建热修复分支**：从 main 分支创建热修复分支
2. **修复问题**：在热修复分支上修复紧急问题
3. **测试验证**：进行测试确保修复有效
4. **合并到 main**：合并热修复分支到 main 分支
5. **同步到 develop**：将热修复合并回 develop 分支
6. **部署**：基于 main 分支进行部署
7. **删除热修复分支**：删除已完成的热修复分支

## 7. 性能优化模式

### 7.1 提交优化

- **小提交**：每次提交只包含相关的更改
- **清晰的提交信息**：使用规范的提交信息格式
- **合理的分支管理**：避免分支过多和混乱
- **定期合并**：定期将 develop 分支合并到功能分支

### 7.2 推送优化

- **批量推送**：避免频繁推送小更改
- **合理的推送时机**：在完成一个功能或修复后推送
- **推送前检查**：确保代码构建通过和测试通过
- **使用 --force-with-lease**：安全地强制推送

### 7.3 仓库维护

- **定期清理**：清理过期的分支和标签
- **垃圾回收**：定期运行 `git gc` 进行垃圾回收
- **压缩历史**：对于大型仓库，考虑压缩历史记录
- **备份**：定期备份仓库

## 8. 安全最佳实践

### 8.1 敏感信息保护

- **使用 .gitignore**：排除包含敏感信息的文件
- **环境变量**：使用环境变量存储敏感配置
- **密钥管理**：使用密钥管理服务存储 API 密钥和令牌
- **定期检查**：定期检查提交历史中是否包含敏感信息

### 8.2 访问控制

- **分支保护**：配置分支保护规则，防止直接推送
- **PR 审查**：要求代码审查才能合并
- **权限管理**：合理设置仓库权限
- **审计日志**：启用审计日志，监控仓库活动

### 8.3 安全扫描

- **预提交钩子**：使用预提交钩子检查敏感信息
- **CI/CD 扫描**：在 CI/CD 流程中集成安全扫描
- **依赖检查**：定期检查依赖包的安全漏洞
- **代码分析**：使用静态代码分析工具检查安全问题