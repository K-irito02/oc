---
name: git-commit-workflow
description: |
 "为项目提供标准化的 Git 提交工作流，包括\"项目环境状态仓库\"和\"项目代码仓库\"的提交规范、流程和最佳实践"
---

# Git 提交工作流技能

## 技能描述

本技能为项目提供标准化的 Git 提交工作流，包括项目环境状态仓库和项目代码仓库的提交规范、流程和最佳实践。通过本技能，您可以：

- 规范化项目环境配置和记忆文件的提交
- 遵循 GitFlow 规范管理项目代码
- 自动化 Git 提交流程，提高开发效率
- 确保代码质量和版本控制的一致性

## 适用场景

- 需要标准化 Git 工作流的团队项目
- 希望遵循 GitFlow 规范管理代码的项目
- 需要定期提交环境配置和记忆文件的场景
- 追求代码质量和版本控制一致性的开发团队

## 核心功能

1. **环境状态仓库提交**：管理 `.trae/`、`.windsurf/`、`Memory/` 等配置目录的提交
2. **项目代码仓库提交**：遵循 GitFlow 规范管理 `oc-platform/` 目录的代码提交
3. **提交规范检查**：确保提交信息符合 Conventional Commits 规范
4. **自动化提交流程**：简化 Git 提交和推送操作
5. **分支管理**：支持功能分支、发布分支和热修复分支的管理

## 技术栈要求

- Git 2.0+
- PowerShell 7+ (Windows)
- 项目使用 GitFlow 分支管理策略

## 快速开始

### 环境状态仓库提交

**功能说明**：提交项目环境配置、规则、技能、工作流和项目记忆到远程仓库。

**触发命令**：
- `提交环境配置`、`commit env`、`push env`
- `提交记忆`、`commit memory`
- `同步配置`、`sync config`

**提交流程**：
1. 检查 Git 状态
2. 添加核心配置目录（`.trae/`、`.windsurf/`、`Memory/`、`Planning Document/`）
3. 提交变更（使用 `config:`、`memory:`、`docs:` 等提交类型）
4. 推送到远程仓库

### 项目代码仓库提交

**功能说明**：提交前后端代码到 GitHub 远程仓库，遵循 GitFlow 规范。

**触发命令**：
- `提交代码`、`commit code`、`push code`
- `提交项目`、`commit project`
- `推送代码`、`push project`

**提交流程**：
1. 切换到项目代码仓库目录
2. 检查 Git 状态
3. 添加所有变更文件
4. 提交变更（使用 Conventional Commits 规范）
5. 推送到对应分支（`develop` 用于日常开发，`main` 用于发布）

## 配置选项

### 环境状态仓库配置

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `commitType` | string | `config` | 提交类型，可选值：`config`、`memory`、`docs`、`backup`、`sync` |
| `commitMessage` | string | 必需 | 提交描述信息 |
| `remote` | string | `origin` | 远程仓库名称 |
| `branch` | string | `main` | 分支名称 |

### 项目代码仓库配置

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `commitType` | string | `feat` | 提交类型，可选值：`feat`、`fix`、`docs`、`style`、`refactor`、`test`、`chore`、`perf`、`ci` |
| `commitMessage` | string | 必需 | 提交描述信息 |
| `remote` | string | `origin` | 远程仓库名称 |
| `branch` | string | `develop` | 分支名称，可选值：`develop`、`main` |

## 最佳实践

1. **环境状态仓库**：
   - 定期提交环境配置和记忆文件
   - 使用清晰的提交类型和描述
   - 避免提交敏感信息

2. **项目代码仓库**：
   - 遵循 GitFlow 分支管理策略
   - 使用 Conventional Commits 规范
   - 提交前进行代码检查和构建验证
   - 合理使用功能分支、发布分支和热修复分支

3. **通用最佳实践**：
   - 保持提交信息简洁明了
   - 避免一次提交过多更改
   - 定期拉取远程更新
   - 解决合并冲突时保持代码质量

## 故障排除

- **GitHub Push Protection 拒绝**：检查提交中是否包含敏感信息
- **推送被拒绝（远程有更新）**：拉取远程更新后重新推送
- **文件过大**：检查是否有大文件未被 .gitignore 排除
- **认证失败**：重新配置 GitHub 认证

## 示例项目

查看 `examples` 目录获取完整的示例代码和配置。