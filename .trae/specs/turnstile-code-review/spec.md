# Cloudflare Turnstile 验证码代码审查与修复 Spec

## Why

当前 Cloudflare Turnstile 验证码实现存在多个设计问题和安全隐患，包括：
1. 前端硬编码 siteKey 导致安全风险和配置不灵活
2. 验证码组件位置和显示逻辑不正确
3. 验证码验证流程不完善
4. 数据库迁移脚本需要清理
5. 初始化 SQL 文件需要更新

## What Changes

### 前端修复
- **BREAKING**: 移除前端硬编码的 siteKey，改为从后端动态获取
- 修复 CloudflareTurnstile 组件的显示位置和逻辑
- 实现验证码开关功能（根据后端配置决定是否显示）
- 添加验证码验证状态检查

### 后端修复
- 修复 `CaptchaConfigResponse` 字段命名（appId → siteKey）
- 确保验证码验证正确集成到各业务接口

### 数据库修复
- 删除迁移脚本 `add_verify_service_column.sql`（已合并到 init.sql）
- 删除 `add-captcha-config.sql`（包含过时的腾讯验证码配置）
- 更新 `init.sql` 添加 Cloudflare 验证码系统配置

## Impact

- Affected specs: 验证码功能、安全配置
- Affected code:
  - 前端: `CloudflareTurnstile/index.tsx`, `Login/index.tsx`, `Register/index.tsx`, `ForgotPassword/index.tsx`, `Profile/index.tsx`, `ProductDetail/index.tsx`, `FeedbackSection.tsx`, `useCaptcha.ts`
  - 后端: `CaptchaConfigResponse.java`, `CaptchaServiceImpl.java`
  - 数据库: `init.sql`, 迁移脚本

## ADDED Requirements

### Requirement: 动态验证码配置
系统 SHALL 从后端动态获取验证码配置，包括是否启用和 siteKey。

#### Scenario: 验证码启用时
- **WHEN** 后端返回 `enabled: true` 和有效的 `siteKey`
- **THEN** 前端显示 CloudflareTurnstile 组件

#### Scenario: 验证码禁用时
- **WHEN** 后端返回 `enabled: false`
- **THEN** 前端隐藏验证码组件，表单提交不受影响

### Requirement: 验证码组件正确显示
系统 SHALL 在表单内部正确显示验证码组件，而不是隐藏在页面底部。

#### Scenario: 登录页面验证码显示
- **WHEN** 用户访问登录页面且验证码启用
- **THEN** 验证码组件显示在密码输入框下方、登录按钮上方

### Requirement: 验证码验证状态检查
系统 SHALL 在表单提交前检查验证码验证状态。

#### Scenario: 验证码未完成验证
- **WHEN** 用户尝试提交表单但验证码未完成验证
- **THEN** 显示错误提示，阻止表单提交

### Requirement: 数据库初始化完整性
系统 SHALL 在初始化 SQL 文件中包含完整的验证码配置。

#### Scenario: 新环境初始化
- **WHEN** 执行 init.sql 初始化数据库
- **THEN** 包含 Cloudflare 验证码相关配置项

## MODIFIED Requirements

### Requirement: 验证码配置响应格式
`CaptchaConfigResponse` 字段名 SHALL 使用 `siteKey` 而非 `appId`，与 Cloudflare Turnstile 术语保持一致。

## REMOVED Requirements

### Requirement: 迁移脚本
**Reason**: 迁移脚本内容已合并到 init.sql，无需保留单独的迁移文件。
**Migration**: 删除 `add_verify_service_column.sql` 和 `add-captcha-config.sql`

## 发现的问题详情

### 1. 前端硬编码 siteKey（高优先级）

**问题位置**:
- `Login/index.tsx` 第 166 行
- `Register/index.tsx` 第 197 行
- `ForgotPassword/index.tsx` 第 142 行
- `Profile/index.tsx` 第 338 行
- `ProductDetail/index.tsx` 第 636 行
- `FeedbackSection.tsx` 第 525 行

**问题描述**: 所有页面都硬编码了 `siteKey="0x4AAAAAACnWLahpCdkdO4qv"`

**风险**:
- 暴露敏感配置信息
- 无法在不同环境使用不同配置
- 违反安全最佳实践

### 2. 验证码组件位置错误（高优先级）

**问题描述**: CloudflareTurnstile 组件被放置在页面最外层 div 的底部，而不是表单内部，导致：
- 组件可能不可见或位置不正确
- 用户无法正常完成验证

### 3. 验证码开关功能未实现（中优先级）

**问题描述**: 前端没有根据后端配置决定是否显示验证码组件，即使后端禁用验证码，前端仍会尝试加载。

### 4. 后端响应字段命名不一致（低优先级）

**问题位置**: `CaptchaConfigResponse.java`

**问题描述**: 字段名为 `appId`，但实际返回的是 Cloudflare 的 `siteKey`，命名不一致可能导致混淆。

### 5. 数据库迁移脚本冗余（低优先级）

**问题位置**:
- `sql/migrations/add_verify_service_column.sql`
- `sql/add-captcha-config.sql`

**问题描述**: 这些迁移脚本的内容已经合并到 init.sql，无需保留。

### 6. init.sql 缺少 Cloudflare 验证码配置（中优先级）

**问题描述**: init.sql 中缺少 Cloudflare Turnstile 相关的系统配置项。
