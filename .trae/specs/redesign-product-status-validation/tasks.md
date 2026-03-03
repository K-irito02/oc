# Tasks

- [x] Task 1: 后端状态机与验证逻辑实现
  - [x] Task 1.1: 在 ErrorCode 中添加新错误码（无效状态转换、缺少版本）
  - [x] Task 1.2: 在 ProductService 中实现状态转换验证方法 `validateStatusTransition()`
  - [x] Task 1.3: 修改 `auditProduct()` 方法添加状态转换验证
  - [x] Task 1.4: 修改 `updateProduct()` 方法添加状态转换验证
  - [x] Task 1.5: 在 ProductVersionMapper 中添加查询方法（如需要）

- [x] Task 2: 前端产品列表页优化
  - [x] Task 2.1: 添加获取产品版本信息的 API 调用
  - [x] Task 2.2: 实现操作按钮智能显示逻辑
  - [x] Task 2.3: 添加状态转换错误提示
  - [x] Task 2.4: 添加中英文国际化文案

- [x] Task 3: 前端产品编辑页优化
  - [x] Task 3.1: 完善状态选择时的验证提示
  - [x] Task 3.2: 优化版本发布与产品状态联动
  - [x] Task 3.3: 添加中英文国际化文案

- [x] Task 4: 测试验证
  - [x] Task 4.1: 验证后端状态转换逻辑
  - [x] Task 4.2: 验证前端按钮显示逻辑
  - [x] Task 4.3: 验证中英文切换

# Task Dependencies

- Task 2 依赖 Task 1（后端 API 需要先完成）
- Task 3 依赖 Task 1
- Task 4 依赖 Task 1, 2, 3
