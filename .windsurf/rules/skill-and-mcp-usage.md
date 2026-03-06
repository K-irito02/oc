---
description: 技能和MCP使用规则
scope: project
trigger: always_on
---

# 技能和MCP使用规则

## 1. 技能使用场景

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

## 2. MCP 使用场景

| 场景 | 推荐 MCP | 说明 |
|------|---------|------|
| 搜索 UI 组件 | shadcn-ui | 查找和添加组件 |
| 复杂问题分析 | Sequential Thinking | 逐步推理 |
| 查询技术文档 | Context7 | 获取库文档 |
| 网络搜索 | Tavily Search | 获取最新信息 |
| GitHub 操作 | GitHub | 仓库、PR、Issue 管理 |
| 前端测试 | Playwright | E2E 测试自动化 |

## 3. 技能调用规则

1. **优先使用技能**: 当任务匹配技能描述时，优先调用对应技能
2. **组合使用**: 复杂任务可以组合多个技能
3. **MCP 辅助**: 技能执行过程中可使用 MCP 工具辅助
4. **记录日志**: 重要操作记录到 `Memory/WorkLogs/`

## 4. 注意事项

1. **技能选择**: 根据任务类型选择最合适的技能
2. **MCP 限制**: 注意 MCP 工具的使用限制和配额
3. **错误处理**: 技能执行失败时提供清晰的错误信息
4. **性能考虑**: 避免不必要的工具调用，优化执行效率
