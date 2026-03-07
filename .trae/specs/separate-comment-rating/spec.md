# 评论评分与产品评分分离规范

## Why
当前系统中，用户在产品详情页发布评论时可以打分，这个评分被存储为"体验评分"（experience_rating）。用户希望评论中的打分不要与"产品评分"混淆，需要明确分离两种评分机制。

## What Changes
- 评论中的打分字段保留，但明确其用途为"评论评分"，独立于"产品评分"
- "产品评分"仅通过侧边栏的评分组件独立提交
- 更新相关文案，区分两种评分类型
- 前端显示时明确区分两种评分来源

## Impact
- Affected code:
  - 前端：ProductDetail、RatingStats 组件、翻译文件
  - 后端：CommentService、ProductVO、Product 实体
  - 数据库：products 表字段注释

## ADDED Requirements

### Requirement: 评论评分独立显示
系统 SHALL 在评论列表中显示每条评论的评分，但不将其统计到产品评分中。

#### Scenario: 用户查看评论
- **WHEN** 用户查看产品详情页的评论列表
- **THEN** 每条评论显示该用户给出的评分（如果有）
- **AND** 该评分不影响侧边栏的产品评分统计

### Requirement: 产品评分独立提交
系统 SHALL 通过侧边栏的评分组件独立收集产品评分。

#### Scenario: 用户提交产品评分
- **WHEN** 用户在侧边栏点击星星提交评分
- **THEN** 评分被记录为产品评分
- **AND** 更新产品评分统计（rating_average, rating_count）

#### Scenario: 用户发布评论
- **WHEN** 用户发布评论并打分
- **THEN** 评分被记录为评论的一部分
- **AND** 更新评论评分统计（experience_rating_average, experience_rating_count）
- **AND** 不影响产品评分统计

## MODIFIED Requirements

### Requirement: 评分字段命名规范
数据库字段 SHALL 明确区分两种评分类型：

| 字段 | 用途 | 显示位置 |
|------|------|----------|
| `rating_average` | 产品评分平均值 | 产品卡片、侧边栏统计 |
| `rating_count` | 产品评分总数 | 侧边栏统计 |
| `rating_distribution` | 产品评分分布 | 侧边栏统计 |
| `experience_rating_average` | 评论评分平均值 | 评论区域统计（可选显示） |
| `experience_rating_count` | 评论评分总数 | 评论区域统计（可选显示） |

### Requirement: 前端评分显示
前端 SHALL 明确区分两种评分的显示：

1. **产品评分**：
   - 显示在产品卡片和侧边栏
   - 标签使用 `productDetail.productRating`（产品评分）
   - 数据来源：`rating_*` 字段

2. **评论评分**：
   - 显示在每条评论中
   - 标签使用 `productDetail.commentRating`（评论评分）
   - 评论表单中的评分标签使用 `productDetail.yourRating`（您的评分）

### Requirement: 国际化翻译
翻译文件 SHALL 包含明确的评分类型标签：

**中文**：
- `productDetail.rating`: "产品评分"（用于产品卡片统计）
- `productDetail.productRating`: "产品评分"（用于侧边栏标题）
- `productDetail.commentRating`: "评论评分"（用于评论区域）
- `productDetail.yourRating`: "您的评分"（用于评论表单）

**英文**：
- `productDetail.rating`: "Rating"
- `productDetail.productRating`: "Product Rating"
- `productDetail.commentRating`: "Review Rating"
- `productDetail.yourRating`: "Your Rating"

## REMOVED Requirements

无移除的需求。现有功能保持，仅调整命名和显示逻辑。
