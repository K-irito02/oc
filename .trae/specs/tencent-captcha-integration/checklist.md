# Checklist

## 准备工作检查

- [x] Cloudflare 账号已注册
- [x] Turnstile 应用已创建
- [x] Site Key 和 Secret Key 已获取
- [x] 域名白名单已配置

## 后端迁移检查

- [x] CaptchaVerifyRequest DTO 已修改为 token 参数
- [x] CaptchaVerifyResponse DTO 已适配 Cloudflare 响应格式
- [x] CaptchaConfig 配置类已添加 cloudflare 配置项
- [x] CaptchaService 实现类已迁移到 Cloudflare 验证逻辑
- [x] 验证记录保存逻辑已添加 verify_service 字段
- [x] application.yml 已更新 Cloudflare 配置
- [x] docker-compose.dev.yml 环境变量已更新
- [x] system_configs 表配置项已更新

## 数据库迁移检查

- [x] verify_service 字段已添加到 captcha_records 表
- [x] 历史验证记录已更新 verify_service 字段
- [x] 数据库迁移脚本已创建并执行

## 前端迁移检查

- [x] CloudflareTurnstile 组件已创建
- [x] Turnstile SDK 加载逻辑已实现
- [x] 验证回调处理已实现
- [x] 主题切换支持已添加（light/dark/auto）
- [x] 多语言支持已添加
- [x] useCaptcha Hook 已适配 Cloudflare Turnstile
- [x] 验证码 API 方法已更新
- [x] 类型定义已更新

## 页面迁移检查

- [x] Login 页面已替换为 CloudflareTurnstile 组件
- [x] Register 页面已替换为 CloudflareTurnstile 组件
- [x] ForgotPassword 页面已替换为 CloudflareTurnstile 组件
- [x] Profile 页面（修改密码）已替换为 CloudflareTurnstile 组件
- [x] Profile 页面（修改邮箱）已替换为 CloudflareTurnstile 组件
- [x] ProductDetail 页面（评论）已替换为 CloudflareTurnstile 组件
- [x] FeedbackSection 组件（留言）已替换为 CloudflareTurnstile 组件

## 代码清理检查

- [x] TencentCaptcha 组件已删除
- [x] 腾讯验证码相关导入已移除
- [x] utils/api.ts 中腾讯验证码相关 API 已移除

## 功能测试检查

- [x] 登录验证码流程正常
- [x] 注册验证码流程正常
- [x] 忘记密码验证码流程正常
- [x] 修改密码验证码流程正常
- [x] 修改邮箱验证码流程正常
- [x] 评论验证码流程正常
- [x] 留言验证码流程正常
- [x] 验证码开关功能正常
- [x] 智能验证（被动模式）正常
- [x] 交互验证模式正常
- [x] 验证失败重试功能正常
- [x] 中英文切换功能正常
- [x] 主题切换功能正常（light/dark）

## 后端测试检查

- [x] Cloudflare Turnstile 验证接口测试通过
- [x] 验证记录保存测试通过
- [x] 配置读取测试通过
- [x] 异常场景处理测试通过

## 安全检查

- [x] Secret Key 已加密存储
- [x] 验证票据有效期限制已实现（300秒）
- [x] 验证票据一次性使用已实现
- [x] 不同场景验证票据隔离已实现
- [x] 验证失败记录已保存
- [x] 域名验证已实现

## 代码质量检查

- [x] 后端代码编译通过
- [x] 后端代码无 Lint 错误
- [x] 前端代码编译通过（npm run build）
- [x] 前端代码检查通过（npm run lint）
- [x] TypeScript 类型检查通过

## 文档检查

- [x] API 文档已更新
- [x] 部署文档已更新
- [x] Memory 文档已更新
- [x] 迁移指南已创建

## 性能检查

- [x] 验证码加载速度正常（< 1秒）
- [x] 验证请求响应时间正常（< 500ms）
- [x] 无内存泄漏问题

## 兼容性检查

- [x] Chrome 浏览器验证正常
- [x] Firefox 浏览器验证正常
- [x] Safari 浏览器验证正常
- [x] Edge 浏览器验证正常
- [x] 移动端浏览器验证正常
