# Cloudflare Turnstile 验证码完善计划

## Why

用户提供了 Cloudflare Turnstile 的 Site Key 和 Secret Key，需要配置到数据库中并完善验证码功能。

## 问题分析

### 1. 数据库配置缺失
- `system_configs` 表中验证码配置值为空
- 需要更新 Site Key 和 Secret Key

### 2. 国际化翻译缺失
- `auth.captchaConfigError` - 登录/注册页面使用（前端已硬编码，需添加翻译）
- `feedback.captchaRequired` - FeedbackSection 使用（缺失）
- `feedback.captchaConfigError` - FeedbackSection 使用（前端已硬编码，需添加翻译）
- `profile.captchaConfigError` - Profile 页面使用（前端已硬编码，需添加翻译）

### 3. 验证码重置问题
- Cloudflare Turnstile token 只能使用一次
- 提交表单后需要重置验证码组件
- 当前代码在提交成功后没有重置验证码状态

### 4. Profile 页面验证码状态共享问题
- 修改密码和修改邮箱共用同一个 `captchaToken` 和 `captchaVerified` 状态
- 用户完成一个操作的验证后，另一个操作也会认为已验证
- 需要为每个操作独立管理验证码状态

## What Changes

### 1. 更新数据库验证码配置
- Site Key: `0x4AAAAAACnWLahpCdkdO4qv`
- Secret Key: `0x4AAAAAACnWLTxjQ17uu88EHQS_cL8ZF1M`
- 确保 `captcha.enabled` 为 `true`

### 2. 补充国际化翻译
在 `zh-CN.json` 和 `en-US.json` 中添加：
- `auth.captchaConfigError`: 验证码配置错误，请联系管理员 / Captcha configuration error, please contact administrator
- `feedback.captchaRequired`: 请完成人机验证 / Please complete the captcha verification
- `feedback.captchaConfigError`: 验证码配置错误，请联系管理员 / Captcha configuration error, please contact administrator
- `profile.captchaConfigError`: 验证码配置错误，请联系管理员 / Captcha configuration error, please contact administrator

### 3. 修复验证码重置问题
- Login 页面：登录失败后重置验证码
- Register 页面：发送验证码后重置验证码
- ForgotPassword 页面：发送验证码后重置验证码
- Profile 页面：提交成功后重置验证码
- FeedbackSection 页面：提交成功后重置验证码

### 4. 修复 Profile 页面验证码状态管理
- 为修改密码和修改邮箱分别创建独立的验证码状态
- 添加 `passwordCaptchaToken`、`passwordCaptchaVerified`
- 添加 `emailCaptchaToken`、`emailCaptchaVerified`

## Impact

- Affected code:
  - `oc-platform-web/src/locales/zh-CN.json` - 中文翻译
  - `oc-platform-web/src/locales/en-US.json` - 英文翻译
  - `oc-platform-web/src/pages/Login/index.tsx` - 登录页面
  - `oc-platform-web/src/pages/Register/index.tsx` - 注册页面
  - `oc-platform-web/src/pages/ForgotPassword/index.tsx` - 忘记密码页面
  - `oc-platform-web/src/pages/Profile/index.tsx` - 个人资料页面
  - `oc-platform-web/src/components/home/FeedbackSection.tsx` - 留言反馈组件

## 实施步骤

### Task 1: 更新数据库验证码配置
执行 SQL 更新 `system_configs` 表中的验证码配置：
```sql
UPDATE system_configs SET config_value = '0x4AAAAAACnWLahpCdkdO4qv' WHERE config_key = 'captcha.cloudflare.site_key';
UPDATE system_configs SET config_value = '0x4AAAAAACnWLTxjQ17uu88EHQS_cL8ZF1M' WHERE config_key = 'captcha.cloudflare.secret_key';
UPDATE system_configs SET config_value = 'true' WHERE config_key = 'captcha.enabled';
```

### Task 2: 补充国际化翻译
在 `zh-CN.json` 和 `en-US.json` 中添加缺失的翻译键

### Task 3: 修复 Profile 页面验证码状态管理
为修改密码和修改邮箱分别创建独立的验证码状态

### Task 4: 修复验证码重置问题
在各页面添加验证码重置逻辑，使用 `useRef` 获取组件引用并调用 `resetTurnstile` 方法

### Task 5: 重启项目验证
重启项目并验证修复效果
