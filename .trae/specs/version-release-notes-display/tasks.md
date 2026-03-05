# Tasks

- [x] Task 1: 后端版本发布时自动更新产品最新版本号
  - [x] SubTask 1.1: 修改 VersionService.publishVersion 方法，发布版本时更新产品的 latestVersion 字段
  - [x] SubTask 1.2: 修改 VersionService.createVersion 方法，创建已发布版本时更新产品的 latestVersion 字段

- [x] Task 2: 前端版本列表增加发布说明展示
  - [x] SubTask 2.1: 更新 VersionItem 类型定义，添加 releaseNotes 和 releaseNotesEn 字段
  - [x] SubTask 2.2: 在版本列表中展示发布说明，支持中英文切换

- [x] Task 3: 前端国际化文件更新
  - [x] SubTask 3.1: 更新 zh-CN.json，添加发布说明相关翻译
  - [x] SubTask 3.2: 更新 en-US.json，添加发布说明相关翻译

- [x] Task 4: 编译验证
  - [x] SubTask 4.1: 编译后端并重启服务
  - [x] SubTask 4.2: 验证前端功能

# Task Dependencies
- [Task 2] depends on [Task 3]
- [Task 4] depends on [Task 1, Task 2, Task 3]
