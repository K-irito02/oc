---
description: 项目环境状态仓库代码提交工作流 — 提交 AI 配置、规则、技能、工作流和项目记忆到远程仓库
---

# 项目环境状态仓库提交工作流

> 将 E:\oc 目录下的环境配置文件提交到 GitHub 远程仓库

## 触发条件

当用户请求以下操作时触发：
- "提交环境配置"、"commit env"、"push env"
- "提交记忆"、"commit memory"
- "同步配置"、"sync config"

---

## 提交流程

### 1. 切换到项目环境状态仓库目录

工作目录：`e:\oc`

### 2. 检查 Git 状态

// turbo
```powershell
git status --short
```

如果没有任何变更，提示用户"没有需要提交的更改"并结束。

### 3. 查看变更详情

// turbo
```powershell
git diff --stat
```

### 4. 添加所有变更文件

// turbo
```powershell
git add .trae/ .windsurf/ Memory/ "Planning Document/" package.json README.md
```

**注意：** 仅添加核心配置目录，排除以下内容：
- `qt-platform/` — 项目代码（独立仓库）
- `node_modules/` — 依赖文件
- `Front-end testing/` — 测试素材（大文件）
- `package-lock.json` — 锁定文件
- `*.mp4`, `*.avi` 等视频文件

### 5. 确认暂存区状态

// turbo
```powershell
git status
```

### 6. 提交变更

```powershell
git commit -m "<type>: <description>"
```

**提交类型规范：**
- `config:` 配置文件更新
- `memory:` 记忆文件更新
- `docs:` 文档更新（规则、技能、工作流）
- `backup:` 创建备份
- `sync:` 同步配置更新

**示例：**
```powershell
git commit -m "memory: 更新后端API记忆和测试状态"
git commit -m "config: 添加新的AI技能和工作流"
git commit -m "docs: 更新架构文档"
```

### 7. 推送到远程仓库

```powershell
git push origin main
```

如果是首次推送或远程仓库未设置，使用：

```powershell
git remote add origin https://github.com/K-irito02/oc-env-state.git
git push -u origin main
```

### 8. 验证推送结果

// turbo
```powershell
git log --oneline -3
```

---

## 仓库配置（首次设置）

### 初始化 Git 仓库

```powershell
cd e:\oc
git init
git branch -M main
```

### 配置 .gitignore

创建 `e:\oc\.gitignore` 文件：

```gitignore
# 项目代码仓库（独立管理）
qt-platform/

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

### 添加远程仓库

```powershell
git remote add origin https://github.com/K-irito02/oc-env-state.git
```

### 配置 GitHub 认证

使用个人访问令牌 (PAT) 进行认证：

```powershell
git config credential.helper store
```

推送时输入用户名和令牌：
- 用户名: `K-irito02`
- 密码: `<YOUR_GITHUB_PAT>` （从环境变量或密码管理器获取）

---

## 分支策略

### 主分支
- `main` — 保存稳定的配置和记忆

### 备份分支（可选）
```powershell
# 创建备份分支
git checkout -b backup/2026-02-28
git push origin backup/2026-02-28
git checkout main
```

---

## 常见问题

### 1. 推送被拒绝

```powershell
# 拉取远程更新后重新推送
git pull origin main --rebase
git push origin main
```

### 2. 文件过大

检查是否有大文件未被 .gitignore 排除：

```powershell
git ls-files --other --ignored --exclude-standard | head -20
```

### 3. 认证失败

重新配置认证：

```powershell
git config --global credential.helper store
git push origin main
# 输入用户名和令牌
```
