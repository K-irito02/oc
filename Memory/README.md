# 项目记忆索引 (Project Memory Index)

> 本目录为 AI 辅助开发的"记忆"系统，帮助 AI 快速准确地定位项目相关内容。
> 每次对项目进行开发/修改后，应同步更新对应的记忆文件。

## 目录结构

```
Memory/
├── README.md              # 本文件 — 记忆索引与使用说明
├── Frontend/              # 前端相关记忆
│   ├── architecture.md    # 前端架构（技术栈、目录结构、路由、状态管理）
│   ├── pages.md           # 页面清单与功能描述
│   └── theme.md           # Glassmorphism 主题系统（Tailwind、CSS 变量、动态主题）
├── Backend/               # 后端相关记忆
│   ├── architecture.md    # 后端架构（模块划分、包结构、配置）
│   ├── api.md             # API 接口清单与状态
│   └── security.md        # 安全体系（JWT、RBAC、Spring Security）
├── Database/              # 数据库相关记忆
│   └── schema.md          # 数据库表结构、索引、初始数据
├── Testing/               # 测试相关记忆
│   └── status.md          # 测试状态、覆盖率、已知问题
└── DevOps/                # 部署与运维相关记忆
    └── deployment.md      # Docker、CI/CD、环境配置
```

## 使用规则

1. **查阅时机**：需要定位项目前端/后端/数据库/测试/部署相关内容时，先查阅本目录
2. **更新时机**：对项目进行开发/修改/Bug 修复后，同步更新对应的记忆文件
3. **新增规则**：如新增模块或技术领域，在对应目录下创建新 `.md` 文件，并更新本索引

## 项目当前状态（2026-03-06）

### ✅ 已完成功能
- **用户认证**: JWT + RBAC + OAuth2 (GitHub)
- **邮箱服务**: QQ SMTP 真实发送验证码
- **头像上传**: 多格式支持、圆形裁剪
- **修改邮箱**: 验证码发送到新邮箱
- **主题系统**: Glassmorphism + 动态主题
- **国际化**: 中英双语完整支持
- **管理后台**: 8个管理页面完整CRUD
- **响应式布局**: 移动端适配
- **ICP备案**: 备案信息管理 + 邮箱验证 + Footer显示
- **时区配置**: 统一 Asia/Shanghai (UTC+8)
- **维护模式**: 维护页面 + 后端拦截器
- **错误页面**: 404/403/500/网络错误页面

### 🔧 技术栈
- **前端**: React 18.3.1 + Vite 5.4.10 + TypeScript 5.6 + Ant Design 6.3
- **后端**: Spring Boot 3.2.12 + Java 17 + MyBatis-Plus 3.5.9
- **数据库**: PostgreSQL 15 (28张表) + Redis 7
- **容器化**: Docker + Docker Compose

### 🌐 服务端口
- **前端**: 5173（可能自动切换到5174）
- **后端**: 8081（避免Apache httpd冲突）
- **PostgreSQL**: 5433（Docker映射 5433→5432）
- **Redis**: 6380（Docker映射 6380→6379）
- **MinIO**: 9000/9001

### 📊 数据库
- **表结构**: 28张表完整设计
- **索引优化**: GIN、部分、复合索引
- **触发器**: updated_at自动更新
- **初始化数据**: 超级管理员 KirLab

### 👤 超级管理员
- **用户名**: xxxx
- **邮箱**: xxxxxx

## 关联文档

- **架构文档**: `Planning Document/Architecture Document.md`
- **阶段一设计**: `Planning Document/Phase One.md`
- **主题设计**: `Planning Document/主题设计.md`
- **代码规范**: `.trae/rules/` (统一端口配置)
- **快速启动**: `.trae/rules/development-quickstart.md`
- **前端测试素材**: `Front-end testing/Background material/`

## AI 技能

| 技能 | 用途 |
|------|------|
| `oc-platform-manager` | 项目自动化管理 |
| `git-commit-workflow` | Git 提交工作流 |
| `code-reviewer` | 代码审查 |
| `ui-ux-pro-max` | UI/UX 设计 |
| `fix` | 代码修复和格式化 |
