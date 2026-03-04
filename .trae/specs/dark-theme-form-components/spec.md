# 深色主题表单组件样式优化 Spec

## Why
当前项目中 Ant Design 表单组件（Card 标题、Select 下拉框、Input 输入框、Textarea 文本域等）在深色主题下显示不正确，背景色过于刺眼，文字对比度不足，影响用户体验。

## What Changes
- 修复 Ant Design Card 组件标题在深色模式下的文字颜色
- 优化 Ant Design Select 下拉框在深色模式下的背景和文字样式
- 优化 Ant Design Input 输入框在深色模式下的背景和文字样式
- 优化 Ant Design Input.TextArea 文本域在深色模式下的背景和文字样式
- 统一配置 Ant Design 主题以支持深色模式

## Impact
- Affected specs: 主题系统、表单组件
- Affected code: 
  - `src/theme/antdTheme.ts` - Ant Design 主题配置
  - `src/pages/ProductDetail/index.tsx` - 产品详情页 Card 组件
  - `src/pages/Admin/Feedbacks/index.tsx` - 留言管理页面
  - `src/components/feedback/MessageBoard.tsx` - 留言板组件
  - 其他使用 Ant Design 表单组件的页面

## ADDED Requirements

### Requirement: Ant Design 深色主题配置
系统 SHALL 为 Ant Design 组件提供完整的深色主题配置，确保所有表单组件在深色模式下有适当的背景色和文字颜色。

#### Scenario: Card 标题深色模式显示
- **WHEN** 用户切换到深色主题
- **THEN** Card 组件标题文字应为白色或浅色，确保在深色背景上清晰可见

#### Scenario: Select 下拉框深色模式显示
- **WHEN** 用户切换到深色主题
- **THEN** Select 下拉框应有深色背景，文字应为浅色，下拉菜单也应有深色背景

#### Scenario: Input 输入框深色模式显示
- **WHEN** 用户切换到深色主题
- **THEN** Input 输入框应有深色背景，文字应为浅色，placeholder 应有适当的对比度

#### Scenario: TextArea 文本域深色模式显示
- **WHEN** 用户切换到深色主题
- **THEN** TextArea 文本域应有深色背景，文字应为浅色

### Requirement: 主题配置响应式切换
系统 SHALL 支持主题的实时切换，无需刷新页面即可应用新的主题样式。

#### Scenario: 主题切换实时生效
- **WHEN** 用户切换主题设置
- **THEN** 所有 Ant Design 组件应立即更新为新主题的样式
