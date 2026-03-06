# 测试状态记忆

> 最后更新: 2026-03-06

## 当前测试状态

### 前端

| 检查项 | 状态 | 说明 |
|--------|------|------|
| TypeScript 编译 | ✅ 通过 | `tsc --noEmit` 零错误 |
| Vite 构建 | ✅ 通过 | `npm run build` 成功（~20-25s） |
| ESLint | ✅ 通过 | 0 错误 0 警告 |
| 视觉测试 | ✅ 通过 | 全部前台页面 + 英文切换验证通过 |
| Mock 开关 | ✅ 完成 | VITE_ENABLE_MOCK=false 可禁用 Mock，使用真实后端 |
| 单元测试 | ❌ 待实现 | Jest + React Testing Library 尚未配置 |
| E2E 测试 | ✅ 通过 | Playwright Python 脚本 - 基础页面+管理员主题+用户主题全测通过 |

### 后端

| 检查项 | 状态 | 说明 |
|--------|------|------|
| Maven 编译 | ✅ 通过 | `mvn clean package -DskipTests` |
| 单元测试 | ❌ 待实现 | JUnit 5 + Mockito 尚未编写 |
| 集成测试 | ❌ 待实现 | @SpringBootTest 尚未编写 |
| API 测试 | ✅ 通过 | 全面 curl 测试通过 |

## 测试素材

- **前端测试素材目录**: `Front-end testing/Background material/`
  - 背景图片 (jpeg)
  - 风格视频素材 (mp4) × 6+

## E2E 测试记录（Playwright）

### 全页面功能测试 ✅

**测试范围：**
1. ✅ 首页 `/` - 英雄区、特性卡片、精选产品、留言板
2. ✅ 产品列表 `/products` - 搜索、分类筛选、排序、产品卡片
3. ✅ 产品详情 `/products/:slug` - 概述/版本/评论 tabs、下载侧栏
4. ✅ 登录页 `/login` - 表单、登录成功跳转
5. ✅ 注册页 `/register` - 表单完整
6. ✅ 个人中心 `/profile` - 个人资料/账号信息/修改密码/外观设置 tabs
7. ✅ 管理后台 `/admin` - 仪表盘统计、下载趋势图
8. ✅ 管理后台侧边栏导航 - 用户/产品/评论/分类/主题/系统配置

**测试结果：**
- UI渲染正常 ✅
- 组件交互正常 ✅
- 表单元素完整 ✅
- 风格一致 ✅
- 登录/权限流程正常 ✅
- Mock数据拦截正常 ✅

### 主题管理功能测试 ✅

**用户级主题设置（个人中心-外观设置）：**
- ✅ 背景类型切换（图片/视频）
- ✅ 背景文件URL输入 + 上传按钮
- ✅ 背景透明度滑块（0%-100%）
- ✅ 保存设置/重置按钮

**超级管理员主题管理（/admin/theme）：**
- ✅ 背景设置区域
- ✅ 风格设置区域
- ✅ 保存配置按钮
- ✅ 重置按钮

**验证结果：**
- ✅ 主色调修改后即时生效（无需刷新）
- ✅ 主题配置持久化到 localStorage（页面刷新后保持）
- ✅ 印章、导航链接、按钮等元素颜色随主题变化
- ✅ 笔画宽度修改后卡片边框变化生效
- ✅ 字体选择器支持预设选项和自定义
- ✅ 背景透明度 CSS 变量正确应用

## 待实现测试计划

### 前端测试（阶段一 MVP 后）
1. 配置 Jest + React Testing Library
2. 关键组件单元测试
3. 路由导航测试
4. API 调用 Mock 测试
5. 国际化切换测试
6. 扩展 Playwright E2E 测试覆盖

### 后端测试（阶段一 MVP 后）
1. Service 层单元测试（Mockito）
2. Controller 层单元测试（MockMvc）
3. Repository 层集成测试（@DataJpaTest / Testcontainers）
4. 安全认证集成测试
5. API 端到端测试

## 已知问题与 Bug

> 全部已知问题均已修复

| ID | 模块 | 描述 | 严重性 | 状态 |
|----|------|------|--------|------|
| 1 | DB | seed.sql 表名错误 | 高 | ✅ 已修复 |
| 2 | DB | seed.sql SHA256哈希超限 | 高 | ✅ 已修复 |
| 3 | DB | seed.sql 缺少 file_path | 高 | ✅ 已修复 |
| 4 | DB | init.sql BCrypt密码不匹配 | 高 | ✅ 已修复 |
| 5 | Docker | 本地PG占用5432端口 | 高 | ✅ 改用5433 |
| 6 | 后端 | AuthService inet类型写入失败 | 高 | ✅ 改用自定义SQL |
| 7 | 后端 | SecurityConfig admin端点权限 | 高 | ✅ hasAnyRole |
| 8 | 前端 | AdminLayout navigate警告 | 中 | ✅ 改用 useEffect |
| 9 | 前端 | 页面刷新后权限检查失败 | 高 | ✅ 添加加载状态 |
| 10 | 前端 | Mock 缺少路由 | 中 | ✅ 已添加 |
| 11 | 前端 | Ant Design App 组件警告 | 低 | ✅ 已添加 AntdApp |
| 12 | 前端 | ThemeProvider 加载时机 | 高 | ✅ 改为所有用户 |
| 13 | 前端 | ThemeProvider CSS变量 | 高 | ✅ 同时更新 |
| 14 | 前端 | Mock 主题配置持久化 | 中 | ✅ localStorage |
| 15 | 前端 | ThemeProvider JSON解析 | 中 | ✅ 多层解析 |
| 16 | 前端 | Input.Group 已废弃 | 低 | ✅ Space.Compact |
| 17 | 前端 | Mock文件上传假URL | 高 | ✅ createObjectURL |
| 18 | 前端 | 字体未加载 | 高 | ✅ Google Fonts |
| 19 | 前端 | 缺少字体选项 | 中 | ✅ 添加行书/草书 |
| 20 | 前端 | 主色调无预览 | 中 | ✅ 动态色条 |
| 21 | 前端 | 笔画宽度变量范围小 | 中 | ✅ 扩展CSS |
| 22 | 前端 | 用户外观设置不完整 | 中 | ✅ 添加完整功能 |
| 23 | 前端 | DynamicBackground CSS变量 | 高 | ✅ 改用CSS变量 |
| 24 | 前端 | Mock API键名不一致 | 中 | ✅ 统一 |
| 25 | 前端 | AdminLayout 重定向 | 高 | ✅ checking状态 |
| 26 | 前端 | Navbar缺少管理入口 | 高 | ✅ isAdmin检查 |
| 27 | 前端 | i18n翻译键缺失 | 高 | ✅ 补充完整 |
| 28 | 后端 | 缺少头像上传接口 | 高 | ✅ 添加接口 |
| 29 | 后端 | uploadAvatar inet错误 | 高 | ✅ LambdaUpdateWrapper |
| 30 | 后端 | 缺少静态资源服务 | 中 | ✅ WebMvcConfig |

## 测试覆盖率目标

- 前端: ≥ 80%（Jest + React Testing Library）
- 后端: ≥ 80%（JaCoCo）
