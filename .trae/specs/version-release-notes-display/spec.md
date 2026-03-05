# 版本发布说明与最新版本展示优化 Spec

## Why
管理后台"添加新版本"时填写的"发布说明（中文/英文）"没有在产品详情页展示，且产品详情页的"版本"信息没有根据已发布版本自动更新，导致用户无法了解版本更新内容。

## What Changes
- 产品详情页版本列表增加发布说明展示（支持中英文切换）
- 版本发布时自动更新产品的 `latestVersion` 字段
- 产品详情页侧边栏"版本"信息实时显示最新已发布版本号

## Impact
- Affected specs: 产品详情展示、版本管理
- Affected code: 
  - 前端：ProductDetail/index.tsx
  - 后端：VersionService.java、ProductService.java

## ADDED Requirements

### Requirement: 版本发布说明展示
系统 SHALL 在产品详情页的版本列表中展示每个版本的发布说明。

#### Scenario: 显示版本发布说明
- **WHEN** 用户查看产品详情页的"版本"标签页
- **THEN** 每个版本条目下方显示该版本的发布说明
- **AND** 根据当前语言设置显示中文或英文发布说明

#### Scenario: 发布说明中英文切换
- **WHEN** 用户切换语言
- **THEN** 版本发布说明相应切换为中文或英文

### Requirement: 最新版本号自动更新
系统 SHALL 在发布版本时自动更新产品的最新版本号字段。

#### Scenario: 发布版本时更新产品版本号
- **WHEN** 管理员发布一个新版本
- **THEN** 产品的 `latestVersion` 字段自动更新为该版本号
- **AND** 产品详情页侧边栏显示最新的版本号

### Requirement: 版本发布说明数据传递
系统 SHALL 确保版本发布说明数据正确传递到前端。

#### Scenario: 版本 API 返回发布说明
- **WHEN** 前端请求产品版本列表
- **THEN** 返回数据包含每个版本的 `releaseNotes` 和 `releaseNotesEn` 字段

## MODIFIED Requirements

### Requirement: 版本列表展示
版本列表 SHALL 展示版本号、平台、日期、文件大小和发布说明。

### Requirement: 产品侧边栏信息
产品侧边栏"版本"信息 SHALL 显示最新已发布版本的版本号。
