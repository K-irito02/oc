# 产品管理状态机与验证规范

## Why

当前产品管理模块存在状态转换验证缺陷：
1. 产品从 DRAFT 状态可以直接"推出"变成 PUBLISHED，即使没有发布任何版本
2. 产品从 PENDING 状态审核通过变成 PUBLISHED 时，同样缺少版本验证
3. 缺乏明确的状态机定义，导致状态转换逻辑混乱

## What Changes

### 后端变更
- 定义明确的产品状态机与转换规则
- 在 `ProductService` 中添加状态转换验证逻辑
- 新增错误码：无效状态转换、缺少已发布版本
- 在 `AdminProductController` 的审核接口中添加验证

### 前端变更
- 根据产品状态和版本情况动态显示操作按钮
- 在状态变更前进行前端预验证
- 添加中英文错误提示

### **BREAKING** 状态转换规则变更
- DRAFT → PUBLISHED：必须有至少一个已发布的版本
- PENDING → PUBLISHED：必须有至少一个已发布的版本
- 其他状态转换保持不变

## Impact

- Affected specs: 产品管理功能
- Affected code:
  - `oc-platform-product/service/ProductService.java`
  - `oc-platform-admin/controller/AdminProductController.java`
  - `oc-platform-common/response/ErrorCode.java`
  - `oc-platform-web/pages/Admin/Products/index.tsx`
  - `oc-platform-web/pages/Admin/Products/ProductEdit.tsx`
  - `oc-platform-web/locales/zh-CN.json`
  - `oc-platform-web/locales/en-US.json`

## ADDED Requirements

### Requirement: 产品状态机定义

系统应定义以下产品状态及其转换规则：

| 当前状态 | 目标状态 | 条件 |
|---------|---------|------|
| DRAFT | PENDING | 至少有一个版本（任意状态） |
| DRAFT | PUBLISHED | 至少有一个已发布版本 |
| PENDING | PUBLISHED | 至少有一个已发布版本 |
| PENDING | REJECTED | 无条件 |
| REJECTED | PENDING | 无条件 |
| PUBLISHED | ARCHIVED | 无条件 |
| ARCHIVED | PUBLISHED | 至少有一个已发布版本 |

#### Scenario: DRAFT 产品无版本时提交审核
- **WHEN** 用户尝试将无版本的 DRAFT 产品状态改为 PENDING
- **THEN** 系统应拒绝操作并返回错误"提交审核前，请先添加至少一个版本"

#### Scenario: DRAFT 产品无已发布版本时直接发布
- **WHEN** 用户尝试将无已发布版本的 DRAFT 产品状态改为 PUBLISHED
- **THEN** 系统应拒绝操作并返回错误"发布产品前，请先发布至少一个版本"

#### Scenario: PENDING 产品无已发布版本时审核通过
- **WHEN** 管理员尝试将无已发布版本的 PENDING 产品审核通过
- **THEN** 系统应拒绝操作并返回错误"审核通过前，请先发布至少一个版本"

#### Scenario: 正常状态转换
- **WHEN** 产品满足状态转换条件
- **THEN** 系统应允许状态变更并更新 `updatedAt` 时间戳

### Requirement: 版本状态验证

系统应在版本发布时验证产品状态：

#### Scenario: 版本发布成功
- **WHEN** 产品存在且版本文件已上传
- **THEN** 系统应将版本状态改为 PUBLISHED 并设置 `publishedAt` 时间戳

### Requirement: 前端操作按钮智能显示

前端应根据产品状态和版本情况智能显示操作按钮：

#### Scenario: DRAFT 产品有已发布版本
- **WHEN** 产品状态为 DRAFT 且有已发布版本
- **THEN** 显示"提交审核"和"推出"两个按钮

#### Scenario: DRAFT 产品无已发布版本但有版本
- **WHEN** 产品状态为 DRAFT 且有版本但无已发布版本
- **THEN** 只显示"提交审核"按钮，不显示"推出"按钮

#### Scenario: DRAFT 产品无任何版本
- **WHEN** 产品状态为 DRAFT 且无任何版本
- **THEN** 不显示"提交审核"和"推出"按钮

#### Scenario: PENDING 产品有已发布版本
- **WHEN** 产品状态为 PENDING 且有已发布版本
- **THEN** 显示"通过"和"拒绝"按钮

#### Scenario: PENDING 产品无已发布版本
- **WHEN** 产品状态为 PENDING 且无已发布版本
- **THEN** 显示"拒绝"按钮，"通过"按钮置灰并显示提示

## MODIFIED Requirements

### Requirement: 产品审核接口

原有审核接口直接设置状态，现需添加验证逻辑：

```
PUT /api/v1/admin/products/{id}/audit
Body: { "status": "PUBLISHED" | "REJECTED" | "PENDING" | "ARCHIVED" }
```

- 调用 `ProductService.auditProduct()` 时需验证状态转换合法性
- 转换到 PUBLISHED 状态时需验证是否有已发布版本

### Requirement: 产品更新接口

原有更新接口已有部分验证，需完善：

- 添加状态转换合法性验证
- 提供更详细的错误信息

## REMOVED Requirements

无移除的需求。
