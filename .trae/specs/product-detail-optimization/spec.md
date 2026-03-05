# 产品详情页优化 Spec

## Why
产品详情页存在评分显示不一致、体验评分统计区域冗余、版本信息展示不完整、开发者名称功能缺失等问题，需要统一优化以提升用户体验。

## What Changes
- 统一产品评分显示，确保产品详情页和首页精选推荐的评分实时同步
- 删除评论区域的体验评分统计区块
- 版本信息支持展示当前最新版本
- 新增"开发者名称"字段支持（管理后台产品管理、搜索功能）
- **BREAKING**: 产品表新增 `developer_name` 字段，需数据库迁移

## Impact
- Affected specs: 产品管理、产品搜索、产品详情展示
- Affected code: 
  - 前端：ProductDetail、Products（首页）、Admin/Products
  - 后端：Product 实体、ProductVO、ProductService、ProductController
  - 数据库：products 表

## ADDED Requirements

### Requirement: 产品评分实时同步
系统 SHALL 确保产品评分在产品详情页和首页精选推荐中实时同步显示。

#### Scenario: 评分更新后同步显示
- **WHEN** 用户在产品详情页提交产品评分
- **THEN** 产品详情页的产品评分卡片和首页精选推荐中的评分同时更新

### Requirement: 删除体验评分统计区域
系统 SHALL 移除评论区域的体验评分统计区块，简化界面。

#### Scenario: 评论区域简化
- **WHEN** 用户查看产品详情页的评论区域
- **THEN** 不再显示体验评分统计区块（带星星的灰色背景区域）

### Requirement: 版本信息展示最新版本
系统 SHALL 在产品详情页展示当前产品的最新版本信息。

#### Scenario: 显示最新版本
- **WHEN** 产品有多个版本
- **THEN** 版本信息展示最新发布的版本号

### Requirement: 开发者名称字段
系统 SHALL 支持产品的开发者名称字段。

#### Scenario: 管理后台添加开发者名称
- **WHEN** 管理员创建或编辑产品
- **THEN** 可以填写开发者名称（必填字段）

#### Scenario: 搜索支持开发者名称
- **WHEN** 用户在管理后台搜索产品
- **THEN** 可以通过开发者名称进行搜索

#### Scenario: 产品详情显示开发者名称
- **WHEN** 用户查看产品详情页
- **THEN** 显示产品的开发者名称

## MODIFIED Requirements

### Requirement: 产品表结构
产品表 SHALL 包含开发者名称字段。

- 新增字段: `developer_name` VARCHAR(255) NOT NULL DEFAULT 'Official'
- 新增字段: `latest_version` VARCHAR(50) 用于存储最新版本号

### Requirement: 产品 DTO
ProductVO SHALL 包含开发者名称和最新版本字段。

### Requirement: 国际化翻译
国际化文件 SHALL 包含开发者名称相关的翻译。

## REMOVED Requirements

### Requirement: 体验评分统计区块
**Reason**: 界面冗余，评论中的体验评分已在评论列表中展示
**Migration**: 删除前端组件中的体验评分统计区块代码
