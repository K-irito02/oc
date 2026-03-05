# 产品详情页版本显示优化计划

## 问题分析

### 问题1：多个版本显示"最新"标签（这是正确行为）
**说明**：`isLatest` 字段按"平台+架构"组合设置是正确的设计。每个平台+架构组合都有自己的最新版本，Windows x64、macOS arm64 等多个平台的版本各自显示"最新"标签是合理的，因为不同平台的用户需要知道他们平台的最新版本。

**无需修改**：保持现有逻辑。

### 问题2：无法控制产品详情页显示哪些版本
**需求**：管理员希望能够在管理后台选择哪些已发布版本在产品详情页显示。

## 解决方案

### 版本显示控制
- 在 `product_versions` 表添加 `show_on_detail` 字段（默认 true）
- 管理后台版本管理中添加"显示在详情页"开关
- 产品详情页只获取 `show_on_detail = true` 且 `status = PUBLISHED` 的版本

## 实施步骤

### Task 1: 数据库变更
- 添加 `show_on_detail` 字段到 `product_versions` 表
- 默认值为 `true`（现有版本默认显示）

### Task 2: 后端代码变更
- 更新 `ProductVersion.java` 实体类，添加 `showOnDetail` 字段
- 更新 `ProductVersionVO.java`，添加 `showOnDetail` 字段
- 更新 `VersionService.java`：
  - `getVersionsByProduct` 方法只返回 `showOnDetail = true` 的版本
  - 添加更新版本显示状态的方法
- 更新 `CreateVersionRequest.java`，添加 `showOnDetail` 字段
- 添加管理后台 API：更新版本显示状态

### Task 3: 前端管理后台变更
- 更新 `ProductEdit.tsx`：
  - 版本列表添加"显示在详情页"开关
  - 支持切换版本显示状态
- 更新国际化文件

### Task 4: 编译验证
- 编译后端并重启服务
- 验证前端功能

## 文件变更清单

### 数据库
- `sql/migrations/add_show_on_detail_to_versions.sql` - 新增迁移脚本

### 后端
- `ProductVersion.java` - 添加 `showOnDetail` 字段
- `ProductVersionVO.java` - 添加 `showOnDetail` 字段
- `CreateVersionRequest.java` - 添加 `showOnDetail` 字段
- `VersionService.java` - 修改查询逻辑，添加更新方法
- `AdminProductController.java` - 添加更新版本显示状态 API

### 前端
- `ProductEdit.tsx` - 添加版本显示开关
- `zh-CN.json` / `en-US.json` - 添加翻译
- `api.ts` - 添加 API 方法
