# Checklist

## 后端验证

- [x] ErrorCode 添加 INVALID_STATUS_TRANSITION 错误码
- [x] ErrorCode 添加 NO_PUBLISHED_VERSION 错误码
- [x] ProductService.validateStatusTransition() 方法正确实现状态机验证
- [x] ProductService.auditProduct() 调用状态转换验证
- [x] ProductService.updateProduct() 调用状态转换验证
- [x] 状态转换失败时返回正确的错误码和错误信息

## 前端产品列表页

- [x] 产品列表正确获取版本信息
- [x] DRAFT 产品无版本时不显示"提交审核"和"推出"按钮
- [x] DRAFT 产品有版本但无已发布版本时只显示"提交审核"按钮
- [x] DRAFT 产品有已发布版本时显示"提交审核"和"推出"按钮
- [x] PENDING 产品无已发布版本时"通过"按钮禁用并显示提示
- [x] 状态转换失败时显示正确的错误提示

## 前端产品编辑页

- [x] 状态选择时正确验证版本条件
- [x] 发布版本后正确更新产品状态可用性
- [x] 保存产品时验证状态转换合法性

## 国际化

- [x] 中文错误提示正确显示
- [x] 英文错误提示正确显示
- [x] 按钮提示文本支持中英文切换

## 代码质量

- [x] 无重复代码
- [x] 验证逻辑集中在后端
- [x] 前端预验证与后端验证一致
