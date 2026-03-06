---
description: 技能和MCP使用规则
scope: project
trigger: always_on
---

# 技能和MCP使用规则

## 1. 可用技能列表

### 项目管理技能
- **oc-platform-manager**: OC Platform 项目自动化管理 - 统一管理开发环境启动、停止和状态检查
- **git-commit-workflow**: Git 提交工作流 - 标准化的 Git 提交规范和流程

### 开发技能
- **fullstack-dev-expert**: 全栈开发专家 - React/Next.js 前端 + Node.js 后端 + 数据库
- **frontend-expert**: 前端开发专家 - React/Vue/Svelte 前端页面、UI组件、API集成
- **backend-expert**: 后端开发专家 - Spring Boot 3.2 + Java 17 + MyBatis-Plus + PostgreSQL
- **devops-expert**: DevOps 专家 - Docker、CI/CD、基础设施管理

### 设计技能
- **ui-ux-pro-max**: UI/UX 设计智能助手 - 50种风格、21种调色板、50种字体配对
- **frontend-design**: 前端设计 - 创建生产级前端界面

### 质量保证技能
- **code-reviewer**: 代码审查 - 代码质量、正确性、安全性检查
- **testing-expert**: 测试专家 - 单元测试、集成测试、E2E测试
- **webapp-testing**: Web 应用测试 - Playwright 测试工具包
- **fix**: 代码修复和格式化 - 解决 lint 错误、格式化问题

### 工具技能
- **pr-creator**: Pull Request 创建 - 标准化的 PR 创建流程
- **vite-cache-components**: Vite 缓存组件和 PPR 实现
- **skill-creator**: 技能创建器 - 创建新的 AI 技能
- **find-skills**: 技能发现 - 发现和安装可用技能

## 2. MCP 工具列表

### UI 组件
- **shadcn-ui**: 用于前端 UI 组件的快速构建
  - `get_project_registries`: 获取项目注册表
  - `list_items_in_registries`: 列出注册表中的组件
  - `search_items_in_registries`: 搜索组件
  - `view_items_in_registries`: 查看组件详情
  - `get_item_examples_from_registries`: 获取组件示例
  - `get_add_command_for_items`: 获取添加命令
  - `get_audit_checklist`: 获取审计检查清单

### 思考与推理
- **Sequential Thinking**: 用于复杂问题的顺序思考和分析
  - `sequentialthinking`: 逐步推理和问题分解

### 网络搜索
- **Tavily Search**: 用于网络搜索和信息获取
  - `tavily_search`: 网络搜索
  - `tavily_extract`: 提取网页内容
  - `tavily_crawl`: 爬取网站
  - `tavily_map`: 映射网站结构
  - `tavily_research`: 综合研究

### 文档查询
- **Context7**: 用于上下文理解和库文档查询
  - `resolve-library-id`: 解析库 ID
  - `query-docs`: 查询文档

### 时间工具
- **Time**: 时间相关操作
  - `get_current_time`: 获取当前时间
  - `convert_time`: 时区转换

### GitHub
- **GitHub**: 用于 GitHub 相关操作和代码管理
  - `create_or_update_file`: 创建或更新文件
  - `search_repositories`: 搜索仓库
  - `create_repository`: 创建仓库
  - `get_file_contents`: 获取文件内容
  - `push_files`: 推送多个文件
  - `create_issue`: 创建 Issue
  - `create_pull_request`: 创建 PR
  - `fork_repository`: Fork 仓库
  - `get_issue`: 获取 Issue 详情

### 测试工具
- **Playwright**: 用于前端测试和自动化
  - `playwright_navigate`: 导航到页面
  - `playwright_screenshot`: 截图
  - `playwright_click`: 点击
  - `playwright_fill`: 填充表单
  - `playwright_evaluate`: 执行脚本
  - 等更多浏览器操作工具

## 3. 技能使用场景

| 场景 | 推荐技能 | 说明 |
|------|---------|------|
| 启动/停止开发环境 | oc-platform-manager | 一键管理 Docker、后端、前端服务 |
| 提交代码 | git-commit-workflow | 标准化提交信息和工作流 |
| 创建新功能 | fullstack-dev-expert | 全栈开发支持 |
| 前端页面开发 | frontend-expert | React + TypeScript + Ant Design |
| 后端 API 开发 | backend-expert | Spring Boot + MyBatis-Plus |
| UI/UX 设计 | ui-ux-pro-max | Glassmorphism 风格设计 |
| 代码审查 | code-reviewer | 质量检查和安全审计 |
| 编写测试 | testing-expert | Jest + Playwright |
| 修复代码问题 | fix | Lint 和格式化修复 |
| 创建 PR | pr-creator | 标准化 PR 流程 |

## 4. MCP 使用场景

| 场景 | 推荐 MCP | 说明 |
|------|---------|------|
| 搜索 UI 组件 | shadcn-ui | 查找和添加组件 |
| 复杂问题分析 | Sequential Thinking | 逐步推理 |
| 查询技术文档 | Context7 | 获取库文档 |
| 网络搜索 | Tavily Search | 获取最新信息 |
| GitHub 操作 | GitHub | 仓库、PR、Issue 管理 |
| 前端测试 | Playwright | E2E 测试自动化 |

## 5. 技能调用规则

1. **优先使用技能**: 当任务匹配技能描述时，优先调用对应技能
2. **组合使用**: 复杂任务可以组合多个技能
3. **MCP 辅助**: 技能执行过程中可使用 MCP 工具辅助
4. **记录日志**: 重要操作记录到 `Memory/WorkLogs/`

## 6. 注意事项

1. **技能选择**: 根据任务类型选择最合适的技能
2. **MCP 限制**: 注意 MCP 工具的使用限制和配额
3. **错误处理**: 技能执行失败时提供清晰的错误信息
4. **性能考虑**: 避免不必要的工具调用，优化执行效率
