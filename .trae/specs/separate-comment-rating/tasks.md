# Tasks

- [x] Task 1: 更新前端翻译文件，添加评分类型区分标签
  - [x] SubTask 1.1: 在 zh-CN.json 中添加 `productDetail.commentRating` 和 `productDetail.yourRating` 翻译
  - [x] SubTask 1.2: 在 en-US.json 中添加对应英文翻译

- [x] Task 2: 修改产品详情页评论表单评分标签
  - [x] SubTask 2.1: 将评论表单中的评分标签从 `experienceRating` 改为 `yourRating`
  - [x] SubTask 2.2: 将评论列表中的评分标签改为 `commentRating`

- [x] Task 3: 更新数据库字段注释
  - [x] SubTask 3.1: 更新 init.sql 中 experience_rating_* 字段的注释，明确其用途

- [x] Task 4: 验证评分分离逻辑
  - [x] SubTask 4.1: 确认产品评分和评论评分使用不同的统计字段
  - [x] SubTask 4.2: 构建前端验证无错误

# Task Dependencies
- Task 2 依赖 Task 1（翻译文件需要先更新）
- Task 4 依赖 Task 1-3（所有修改完成后验证）
