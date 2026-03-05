# 前端页面清单

> 最后更新: 2026-03-06

## 前台页面（9 个）

### Home (`pages/Home/index.tsx`)
- Hero Section: 玻璃拟态大卡片 + 动态背景
- 特性卡片：GlassCard 展示平台亮点
- 精选产品：Grid 布局展示
- **留言板组件** (`components/home/FeedbackSection.tsx`)：
  - 双栏布局：留言表单 + 留言列表
  - 留言数量显示（包含回复）
  - 排序功能：时间/点赞/回复数
  - 回复展开/收缩：每次5条
  - 点赞功能
  - 1分钟评论频率限制
  - 滚动区域隔离
  - 国际化支持

### Products (`pages/Products/index.tsx`)
- 分类过滤侧栏
- 排序选项（最新/下载量/评分/名称）
- 关键词搜索
- 产品卡片网格
- **状态过滤**：仅显示 PUBLISHED 状态的产品（2026-03-02 更新）

### ProductDetail (`pages/ProductDetail/index.tsx`)
- Tab 页：概述 / 版本列表 / 评论
- 下载侧栏（平台选择 + 版本信息 + 下载按钮）
- 评分统计
- **评论系统**（2026-02-28 更新）：
  - 评论回复展开/收缩：默认收缩，展开每次5条，收缩一次全部
  - 评论数量显示：包含回复数的总数
  - 滚动区域隔离：鼠标在评论区域内时阻止页面滚动
  - 评论频率限制：失败时不显示评论
  - 国际化支持：成功/失败消息中英切换

### Login (`pages/Login/index.tsx`)
- 邮箱 + 密码登录
- 玻璃拟态卡片 (GlassCard) + 动态背景
- 极简风格表单
- **AuthPageToolbar**: 语言切换 + 主题切换（亮/暗/系统）
- **简化设计** (2026-03-06): 移除 GitHub OAuth 登录按钮和 Dev Quick Fill 测试区域

### Register (`pages/Register/index.tsx`)
- 邮箱验证码注册流程
- 用户名 + 邮箱 + 密码 + 验证码
- **AuthPageToolbar**: 语言切换 + 主题切换

### ForgotPassword (`pages/ForgotPassword/index.tsx`)
- 邮箱验证 + 重置密码
- **AuthPageToolbar**: 语言切换 + 主题切换

### Profile (`pages/Profile/index.tsx`)
- 头像上传（AvatarUpload组件：多格式支持、圆形裁剪、5MB限制）
- 个人信息编辑（昵称、简介）
- Tab 页：
  - **个人资料** - 昵称、简介编辑
  - **账号信息** - 用户名、邮箱、角色查看
  - **安全设置** - 修改密码 + 修改邮箱（验证码发送到新邮箱）
  - **外观设置** - 个性化 Glassmorphism 配置
    - 背景类型选择（图片/视频）
    - 背景文件上传
    - 背景模糊度调节 (Blur)
    - 背景透明度调节 (Opacity)
    - 主色调选择
    - 字体切换

### OAuthCallback (`pages/OAuthCallback/index.tsx`)
- GitHub OAuth 回调处理
- 自动跳转

### NotFound (`pages/NotFound/index.tsx`)
- 404 玻璃拟态页面
- 使用 Lucide React 图标（FileQuestion）
- 支持深色/浅色主题
- 国际化支持

### Error (`pages/Error/index.tsx`) ✨新增 (2026-03-05)
- **通用错误页面组件**，支持多种错误类型：
  - **404 页面未找到**（蓝色主题，FileQuestion 图标）
  - **500 服务器错误**（红色主题，ServerCrash 图标）
  - **403 权限错误**（橙色主题，ShieldX 图标）
  - **网络错误**（黄色主题，WifiOff 图标）
- 使用 Lucide React SVG 图标
- 支持深色/浅色主题
- 国际化支持（中英文）
- 响应式布局
- 脉冲动画效果

### Maintenance (`pages/Maintenance/index.tsx`) ✨新增 (2026-03-05)
- **系统维护页面**
- 从后端获取维护配置信息
- 显示维护标题、说明（中英文切换）
- 预计恢复时间倒计时显示
- 使用 Wrench 图标（紫色主题）
- 重新检查按钮

## 后台页面（7 个）

### Dashboard (`pages/Admin/Dashboard/index.tsx`)
- 统计卡片（用户数/产品数/下载量/评论数）
- 下载趋势折线图

### Users (`pages/Admin/Users/index.tsx`)
- 用户列表（分页 + 搜索 + 状态过滤）
- 用户状态管理（封禁/激活）

### Products (`pages/Admin/Products/index.tsx`)
- 产品列表（分页 + 搜索 + 分类过滤 + 状态过滤）
- 产品审核（发布/下架）
- 产品 CRUD
- 版本发布

### ProductEdit (`pages/Admin/Products/ProductEdit.tsx`)
- **新建产品流程**：统一验证（基本信息+媒体+版本管理）、顶部创建按钮、临时版本管理
- **版本管理**：支持发布临时版本、状态显示、操作按钮
- **架构选择**：支持中英双语切换（2026-03-02 更新）
- **状态管理**：DRAFT/PUBLISHED 状态切换
- **文件上传**：支持应用程序文件上传和校验

### Comments (`pages/Admin/Comments/index.tsx`)
- 评论列表（分页 + 状态过滤）
- 评论审核（通过/拒绝/隐藏）
- 评论删除

### Feedbacks (`pages/Admin/Feedbacks/index.tsx`) ✨新增
- 留言列表（分页 + 状态过滤 + 关键词搜索）
- 留言状态管理（发布/隐藏/待审核）
- 留言删除
- 留言详情查看

### Categories (`pages/Admin/Categories/index.tsx`)
- 分类树形列表
- 分类 CRUD

### Theme (`pages/Admin/Theme/index.tsx`) ✨新增
- 全局主题管理
- 背景设置区域：
  - 背景类型（图片/视频）
  - 背景文件上传
  - 背景透明度调节
- 风格设置区域：
  - 主色调配置
  - 笔画宽度设置
  - 字体配置
- 保存/重置功能
- 配置说明文档

### System (`pages/Admin/System/index.tsx`)
- 系统配置 key-value 编辑
- 审计日志查看
- **新增配置卡片**（2026-03-02）：
  - **官网URL配置**: site.url 设置
  - **社交链接配置**: GitHub、Twitter、LinkedIn、微博、微信、联系邮箱
  - **Logo上传**: 站点Logo管理
  - **邮件配置**: 发件人名称、版权信息、安全提示
  - **备案信息**: 中英文备案号和ICP备案号
  - **节假日定制**: 节假日信息和名人名言
  - **实时保存**: 配置修改即时生效
- **维护模式配置** ✨新增 (2026-03-05)：
  - 维护模式开关（带警告提示）
  - 维护标题（中英文）
  - 维护说明（中英文）
  - 预计恢复时间选择器
  - 配置保存后自动清除缓存
- **ICP备案配置** ✨新增 (2026-03-06)：
  - ICP备案号配置
  - 公安备案号配置
  - 公安备案图标URL配置
  - 修改备案需邮箱验证码验证

---

## 代码规范状态（2026-03-01）

### ✅ ESLint 规范检查
- **配置**: `eslint.config.js` (Flat Config 格式)
- **规则集**: `@eslint/js` + `typescript-eslint` + `react-hooks` + `react-refresh`
- **检查结果**: 0 错误 0 警告 ✅

### 🔧 修复内容
- **类型定义**: 为所有 API 响应定义明确接口，替换 `any` 类型
- **React Hooks**: 使用 `useCallback` 包装函数，正确处理依赖数组
- **错误处理**: 统一使用 `error: unknown` 类型，类型断言处理错误信息
- **变量声明**: 使用 `const` 替代 `let`（不重新赋值时）

### 📋 规则文件
- **更新**: `.windsurf/rules/frontend-code-standards.md`
- **新增内容**: ESLint 实际配置说明、关键规则表格、最佳实践代码示例
