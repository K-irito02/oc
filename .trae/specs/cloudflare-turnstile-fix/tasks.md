# Tasks

## 后端修复任务

- [x] Task 1: 创建 SystemConfigService 服务类
  - [x] SubTask 1.1: 创建 SystemConfigService 接口
  - [x] SubTask 1.2: 实现 SystemConfigServiceImpl，提供获取配置的方法
  - [x] SubTask 1.3: 添加配置缓存机制，避免频繁查询数据库

- [x] Task 2: 修改 CaptchaServiceImpl 配置读取逻辑
  - [x] SubTask 2.1: 注入 SystemConfigService
  - [x] SubTask 2.2: 修改 `getConfig()` 方法，优先从数据库读取配置
  - [x] SubTask 2.3: 实现配置回退逻辑（数据库 → 环境变量）

- [ ] Task 3: 添加验证码配置管理接口
  - [ ] SubTask 3.1: 在 CaptchaController 添加更新配置的接口（管理员权限）
  - [ ] SubTask 3.2: 添加配置验证逻辑

## 前端修复任务

- [x] Task 4: 修复登录页面验证码显示逻辑
  - [x] SubTask 4.1: 修改验证码组件显示条件，处理 siteKey 为空的情况
  - [x] SubTask 4.2: 添加配置错误提示

- [x] Task 5: 修复登录错误处理
  - [x] SubTask 5.1: 正确捕获并显示后端返回的错误信息
  - [x] SubTask 5.2: 处理验证码验证失败的情况

- [x] Task 6: 修复其他页面的验证码逻辑
  - [x] SubTask 6.1: 修复注册页面
  - [x] SubTask 6.2: 修复忘记密码页面
  - [x] SubTask 6.3: 修复个人资料页面（修改密码、修改邮箱）
  - [x] SubTask 6.4: 修复产品详情页面（评论）
  - [x] SubTask 6.5: 修复留言反馈组件

## 验证任务

- [ ] Task 7: 本地环境验证
  - [ ] SubTask 7.1: 验证验证码禁用时登录正常
  - [ ] SubTask 7.2: 验证验证码启用但配置为空时显示错误提示
  - [ ] SubTask 7.3: 验证验证码启用且配置正确时功能正常

- [ ] Task 8: 重启项目验证
  - [ ] SubTask 8.1: 使用技能重启项目
  - [ ] SubTask 8.2: 验证修复效果

# Task Dependencies

- Task 1 无依赖，可首先执行
- Task 2 depends on Task 1
- Task 3 depends on Task 2
- Task 4, 5, 6 无依赖，可并行执行
- Task 7 depends on Task 1-6
- Task 8 depends on Task 7

# 并行执行建议

以下任务可以并行执行：
- Task 1（后端服务）、Task 4-6（前端修复）可同时开始
- Task 2-3（后端配置逻辑）在 Task 1 完成后执行