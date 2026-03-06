# Tasks

## 数据库清理任务

- [x] Task 1: 清理数据库迁移脚本和更新初始化 SQL
  - [x] SubTask 1.1: 删除 `sql/migrations/add_verify_service_column.sql` 迁移脚本
  - [x] SubTask 1.2: 删除 `sql/add-captcha-config.sql` 文件（包含过时的腾讯验证码配置）
  - [x] SubTask 1.3: 更新 `init.sql` 添加 Cloudflare 验证码系统配置项

## 后端修复任务

- [x] Task 2: 修复验证码配置响应
  - [x] SubTask 2.1: 修改 `CaptchaConfigResponse.java`，将 `appId` 字段改为 `siteKey`
  - [x] SubTask 2.2: 更新相关调用代码确保兼容性

## 前端修复任务

- [x] Task 3: 创建验证码配置 Hook
  - [x] SubTask 3.1: 创建 `useCaptchaConfig` Hook，从后端获取验证码配置
  - [x] SubTask 3.2: 实现配置缓存和错误处理

- [x] Task 4: 修复 CloudflareTurnstile 组件
  - [x] SubTask 4.1: 添加 `visible` 属性控制组件显示/隐藏
  - [x] SubTask 4.2: 优化组件加载逻辑

- [x] Task 5: 修复登录页面验证码集成
  - [x] SubTask 5.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 5.2: 将验证码组件移到表单内部正确位置
  - [x] SubTask 5.3: 实现验证码开关功能
  - [x] SubTask 5.4: 添加验证码验证状态检查

- [x] Task 6: 修复注册页面验证码集成
  - [x] SubTask 6.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 6.2: 将验证码组件移到表单内部正确位置
  - [x] SubTask 6.3: 实现验证码开关功能

- [x] Task 7: 修复忘记密码页面验证码集成
  - [x] SubTask 7.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 7.2: 将验证码组件移到表单内部正确位置
  - [x] SubTask 7.3: 实现验证码开关功能

- [x] Task 8: 修复个人资料页面验证码集成
  - [x] SubTask 8.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 8.2: 将验证码组件移到正确位置
  - [x] SubTask 8.3: 实现验证码开关功能

- [x] Task 9: 修复产品详情页面验证码集成
  - [x] SubTask 9.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 9.2: 将验证码组件移到评论表单内部
  - [x] SubTask 9.3: 实现验证码开关功能

- [x] Task 10: 修复留言反馈组件验证码集成
  - [x] SubTask 10.1: 移除硬编码的 siteKey，使用动态配置
  - [x] SubTask 10.2: 将验证码组件移到留言表单内部
  - [x] SubTask 10.3: 实现验证码开关功能

## 验证任务

- [x] Task 11: 功能验证
  - [x] SubTask 11.1: 验证验证码启用时各页面功能正常
  - [x] SubTask 11.2: 验证验证码禁用时各页面功能正常
  - [x] SubTask 11.3: 验证中英文切换功能
  - [x] SubTask 11.4: 验证主题切换功能

- [x] Task 12: 重启项目验证
  - [x] SubTask 12.1: 使用技能重启项目
  - [x] SubTask 12.2: 验证项目启动成功

# Task Dependencies

- Task 1 无依赖，可首先执行
- Task 2 无依赖，可首先执行
- Task 3 无依赖，可首先执行
- Task 4 depends on Task 3
- Task 5, 6, 7, 8, 9, 10 depend on Task 3, Task 4
- Task 11 depends on Task 5, 6, 7, 8, 9, 10
- Task 12 depends on Task 11

# 并行执行建议

以下任务可以并行执行：
- Task 1（数据库）、Task 2（后端）、Task 3（前端 Hook）可同时开始
- Task 5-10（各页面修复）在 Task 3, Task 4 完成后可并行
