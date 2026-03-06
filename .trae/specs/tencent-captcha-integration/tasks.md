# Tasks

## 准备阶段

- [x] Task 1: Cloudflare Turnstile 账号准备
  - [x] SubTask 1.1: 注册 Cloudflare 账号
  - [x] SubTask 1.2: 创建 Turnstile 应用并获取 Site Key 和 Secret Key
  - [x] SubTask 1.3: 配置域名白名单

## 后端迁移任务

- [x] Task 2: 修改后端验证码服务
  - [x] SubTask 2.1: 修改 CaptchaVerifyRequest DTO，将 ticket/randstr 改为 token
  - [x] SubTask 2.2: 修改 CaptchaVerifyResponse DTO，适配 Cloudflare 响应格式
  - [x] SubTask 2.3: 修改 CaptchaConfig 配置类，添加 cloudflare 配置项
  - [x] SubTask 2.4: 重构 CaptchaService 实现类，替换腾讯验证逻辑为 Cloudflare 验证
  - [x] SubTask 2.5: 更新验证记录保存逻辑，添加 verify_service 字段

- [x] Task 3: 更新后端配置
  - [x] SubTask 3.1: 修改 application.yml，移除腾讯配置，添加 Cloudflare 配置
  - [x] SubTask 3.2: 更新 docker-compose.dev.yml 环境变量
  - [x] SubTask 3.3: 更新 system_configs 表配置项

- [x] Task 4: 数据库迁移
  - [x] SubTask 4.1: 添加 verify_service 字段到 captcha_records 表
  - [x] SubTask 4.2: 更新历史验证记录的 verify_service 字段为 'tencent'
  - [x] SubTask 4.3: 创建数据库迁移脚本

## 前端迁移任务

- [x] Task 5: 创建 Cloudflare Turnstile 组件
  - [x] SubTask 5.1: 创建 CloudflareTurnstile 组件
  - [x] SubTask 5.2: 实现 Turnstile SDK 加载逻辑
  - [x] SubTask 5.3: 实现验证回调处理
  - [x] SubTask 5.4: 添加主题切换支持（light/dark/auto）
  - [x] SubTask 5.5: 添加多语言支持

- [x] Task 6: 更新验证码 Hook
  - [x] SubTask 6.1: 修改 useCaptcha Hook，适配 Cloudflare Turnstile
  - [x] SubTask 6.2: 更新验证码 API 方法
  - [x] SubTask 6.3: 更新类型定义

- [x] Task 7: 迁移所有验证码集成页面
  - [x] SubTask 7.1: 修改 Login 页面，替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.2: 修改 Register 页面，替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.3: 修改 ForgotPassword 页面，替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.4: 修改 Profile 页面（修改密码），替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.5: 修改 Profile 页面（修改邮箱），替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.6: 修改 ProductDetail 页面（评论），替换为 CloudflareTurnstile 组件
  - [x] SubTask 7.7: 修改 FeedbackSection 组件（留言），替换为 CloudflareTurnstile 组件

- [x] Task 8: 清理旧代码
  - [x] SubTask 8.1: 删除 TencentCaptcha 组件
  - [x] SubTask 8.2: 移除腾讯验证码相关导入
  - [x] SubTask 8.3: 更新 utils/api.ts，移除腾讯验证码相关 API

## 测试与验证任务

- [x] Task 9: 后端测试
  - [x] SubTask 9.1: 测试 Cloudflare Turnstile 验证接口
  - [x] SubTask 9.2: 测试验证记录保存
  - [x] SubTask 9.3: 测试配置读取
  - [x] SubTask 9.4: 测试异常场景处理

- [x] Task 10: 前端测试
  - [x] SubTask 10.1: 测试登录验证码流程
  - [x] SubTask 10.2: 测试注册验证码流程
  - [x] SubTask 10.3: 测试忘记密码验证码流程
  - [x] SubTask 10.4: 测试修改密码验证码流程
  - [x] SubTask 10.5: 测试修改邮箱验证码流程
  - [x] SubTask 10.6: 测试评论验证码流程
  - [x] SubTask 10.7: 测试留言验证码流程
  - [x] SubTask 10.8: 测试中英文切换
  - [x] SubTask 10.9: 测试主题切换（light/dark）

- [x] Task 11: 端到端验证
  - [x] SubTask 11.1: 验证验证码开关功能
  - [x] SubTask 11.2: 验证智能验证（被动模式）
  - [x] SubTask 11.3: 验证交互验证模式
  - [x] SubTask 11.4: 验证票据有效期
  - [x] SubTask 11.5: 验证错误处理和重试机制

## 文档更新任务

- [x] Task 12: 更新文档
  - [x] SubTask 12.1: 更新 API 文档
  - [x] SubTask 12.2: 更新部署文档
  - [x] SubTask 12.3: 更新 Memory 文档
  - [x] SubTask 12.4: 创建迁移指南

# Task Dependencies

- Task 1 无依赖，必须首先完成
- Task 2 depends on Task 1
- Task 3 depends on Task 1
- Task 4 无依赖，可并行
- Task 5 depends on Task 1
- Task 6 depends on Task 5
- Task 7 depends on Task 5, Task 6
- Task 8 depends on Task 7
- Task 9 depends on Task 2, Task 3, Task 4
- Task 10 depends on Task 5, Task 6, Task 7
- Task 11 depends on Task 9, Task 10
- Task 12 depends on Task 11

# 并行执行建议

以下任务可以并行执行：
- Task 2（后端服务）、Task 3（后端配置）、Task 4（数据库）、Task 5（前端组件）在 Task 1 完成后可同时开始
- Task 9（后端测试）、Task 10（前端测试）在各自模块完成后可并行
