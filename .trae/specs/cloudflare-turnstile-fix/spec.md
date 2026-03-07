# Cloudflare Turnstile 验证码问题修复 Spec

## Why

用户在使用 Cloudflare Turnstile 验证码时遇到两个问题：
1. 本地开发环境登录时没有任何反应，仍停留在登录界面
2. 云服务器部署后登录时提示"请完成安全验证"

根本原因是验证码配置管理混乱，前端和后端配置不同步，导致验证码组件无法正常工作。

## What Changes

### 问题根因分析

1. **配置来源混乱**
   - 后端验证码配置只从 `application.yml` 环境变量读取
   - 数据库 `system_configs` 表有验证码配置项但未被使用
   - 前端从后端 API 获取配置，但配置可能为空

2. **前端显示逻辑问题**
   - 当 `siteKey` 为空时，验证码组件不显示
   - 但后端 `isEnabled()` 检查可能返回 `true`（如果 `captcha.enabled=true`）
   - 导致用户无法完成验证，登录请求被拒绝

3. **错误提示不明确**
   - 登录失败时前端没有正确显示后端返回的错误信息
   - 用户看不到"请完成验证码验证"的提示

### 解决方案

1. **统一配置管理**
   - 后端优先从数据库 `system_configs` 读取验证码配置
   - 环境变量作为备用配置源
   - 提供管理接口更新验证码配置

2. **修复前端逻辑**
   - 当验证码启用但 `siteKey` 为空时，显示配置错误提示
   - 正确处理登录失败并显示错误信息

3. **增强错误处理**
   - 前端捕获并显示验证码相关错误
   - 后端返回更详细的错误信息

## Impact

- Affected code:
  - `oc-platform-common/src/main/java/com/ocplatform/common/config/CaptchaConfig.java`
  - `oc-platform-common/src/main/java/com/ocplatform/common/service/impl/CaptchaServiceImpl.java`
  - `oc-platform-web/src/pages/Login/index.tsx`
  - `oc-platform-web/src/hooks/useCaptchaConfig.ts`
  - `oc-platform-web/src/components/CloudflareTurnstile/index.tsx`

## ADDED Requirements

### Requirement: 验证码配置优先从数据库读取

后端验证码配置 SHALL 优先从数据库 `system_configs` 表读取，环境变量作为备用。

#### Scenario: 数据库有配置时使用数据库配置
- **WHEN** 数据库 `system_configs` 表中存在 `captcha.cloudflare.site_key` 和 `captcha.cloudflare.secret_key` 配置
- **THEN** 系统使用数据库中的配置值

#### Scenario: 数据库无配置时使用环境变量
- **WHEN** 数据库中验证码配置为空
- **THEN** 系统回退到环境变量 `CLOUDFLARE_TURNSTILE_SITE_KEY` 和 `CLOUDFLARE_TURNSTILE_SECRET_KEY`

### Requirement: 验证码配置错误时显示明确提示

前端 SHALL 在验证码配置错误时显示明确的错误提示，而不是静默失败。

#### Scenario: 验证码启用但 siteKey 为空
- **WHEN** `captchaConfig.enabled` 为 `true` 但 `siteKey` 为空
- **THEN** 显示"验证码配置错误，请联系管理员"提示

#### Scenario: 验证码组件加载失败
- **WHEN** Cloudflare Turnstile SDK 加载失败
- **THEN** 显示加载失败提示，并提供重试选项

### Requirement: 登录失败时正确显示错误信息

前端 SHALL 正确捕获并显示后端返回的登录错误信息。

#### Scenario: 验证码验证失败
- **WHEN** 后端返回"请完成验证码验证"或"验证码验证失败"
- **THEN** 前端显示对应的错误提示

#### Scenario: 其他登录错误
- **WHEN** 后端返回其他错误（如用户名密码错误）
- **THEN** 前端正确显示错误信息

## MODIFIED Requirements

### Requirement: 后端验证码服务配置读取

`CaptchaConfig` 类 SHALL 支持从数据库动态读取配置，而不仅仅是静态配置。

**修改前：**
```java
@ConfigurationProperties(prefix = "captcha.cloudflare")
public class CaptchaConfig {
    private String siteKey;
    private String secretKey;
    // ...
}
```

**修改后：**
```java
// CaptchaConfig 保留作为默认配置
// CaptchaServiceImpl 优先从数据库读取，回退到 CaptchaConfig
```

### Requirement: 前端验证码组件显示逻辑

前端 SHALL 在验证码配置不完整时显示配置错误提示。

**修改前：**
```tsx
{captchaConfig.enabled && captchaConfig.siteKey && (
  <CloudflareTurnstile ... />
)}
```

**修改后：**
```tsx
{captchaConfig.enabled && (
  captchaConfig.siteKey ? (
    <CloudflareTurnstile ... />
  ) : (
    <div className="text-amber-500">验证码配置错误，请联系管理员</div>
  )
)}
```
