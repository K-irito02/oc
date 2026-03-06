# 数据库结构记忆

> 最后更新: 2026-03-06

## 数据库信息

| 项目 | 值 |
|------|------|
| 数据库类型 | PostgreSQL 15.x |
| 数据库名 | oc_platform |
| 用户名 | oc_user |
| 密码（开发） | 3143285505 |
| 端口 | 5433（Docker映射5433→5432） |
| 表管理方式 | SQL 脚本（JPA ddl-auto=none） |
| 时区 | Asia/Shanghai (UTC+8) |

## SQL 脚本

| 文件 | 路径 | 说明 |
|------|------|------|
| 建表脚本 | `oc-platform/sql/init.sql` | 全部表结构 + 索引 + 触发器 + 初始化数据 |

## 表清单（28 张）

### 用户相关（7 张）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `users` | 用户表 | id, username, email, password_hash, status, language, theme_config, avatar_url |
| `roles` | 角色表 | id, code (ANONYMOUS/USER/VIP/ADMIN/SUPER_ADMIN), name |
| `user_roles` | 用户-角色关联 | user_id, role_id (UNIQUE) |
| `permissions` | 权限表 | id, code (如 PRODUCT:CREATE), name |
| `role_permissions` | 角色-权限关联 | role_id, permission_id (UNIQUE) |
| `user_oauth_bindings` | 第三方登录绑定 | user_id, oauth_provider, oauth_id (UNIQUE) |
| `email_verifications` | 邮箱验证码 | email, code, type, is_used, expires_at |

### 产品相关（4 张）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `categories` | 产品分类 | id, name, name_en, slug (UNIQUE), parent_id, sort_order |
| `products` | 产品表 | id, name, slug (UNIQUE), category_id, developer_id, developer_name, status, screenshots(JSONB), tags(TEXT[]), display_versions(JSONB), latest_version, experience_rating_average, experience_rating_count, experience_rating_distribution(JSONB) |
| `product_versions` | 产品版本 | id, product_id, version_number, platform(WINDOWS/LINUX/MACOS/ANDROID/IOS/WEB/CROSS_PLATFORM), architecture(x86/x64/arm64), file_path, checksum_sha256, rollout_percentage, show_on_detail, release_notes, release_notes_en |
| `delta_updates` | 增量更新包 | from_version_id, to_version_id, platform, architecture |

### 评论与留言（4 张）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `product_comments` | 评论表 | product_id, user_id, parent_id, content, rating(1-5), status |
| `comment_likes` | 评论点赞 | comment_id, user_id (UNIQUE) |
| `feedbacks` | 留言表 | user_id, parent_id, content, status, like_count, reply_count |
| `feedback_likes` | 留言点赞 | feedback_id, user_id (UNIQUE) |

### 订单与支付（2 张，阶段一仅占位）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `orders` | 订单表 | order_no, user_id, product_id, order_type, amount, payment_status |
| `subscriptions` | VIP 订阅 | user_id, plan_type, status, start_at, expire_at |

### 通知与消息（1 张）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `notifications` | 系统通知 | user_id, type, title, content, link, is_read |

### 下载与统计（2 张，按月分区）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `download_records` | 下载记录（PARTITION BY RANGE） | product_id, version_id, user_id, ip_address, download_at |
| `user_access_logs` | 访问日志（PARTITION BY RANGE） | user_id, request_method, request_path, response_status |

### 系统相关（8 张）
| 表名 | 说明 | 关键字段 |
|------|------|---------|
| `system_configs` | 系统配置 | config_key (UNIQUE), config_value |
| `file_records` | 文件管理 | original_name, stored_name, file_path, storage_type(LOCAL/MINIO) |
| `audit_logs` | 审计日志 | user_id, action, target_type, target_id, detail(JSONB) |
| `i18n_messages` | 多语言内容 | language_code, message_key (UNIQUE组合), message_value |
| `email_configs` | 邮件配置 | host, port, username, from_name |
| `social_links` | 社交链接 | platform, url, icon_url, sort_order |
| `site_config` | 站点配置 | logo_url, site_name, site_description |

## 系统配置项 (`system_configs`)

### 维护模式配置
| config_key | 说明 | 默认值 |
|------------|------|--------|
| `system.maintenance.enabled` | 维护模式开关 | `false` |
| `system.maintenance.title` | 维护标题（中文） | `系统维护中` |
| `system.maintenance.title_en` | 维护标题（英文） | `Under Maintenance` |
| `system.maintenance.message` | 维护说明（中文） | `系统正在进行升级维护，请稍后再试。` |
| `system.maintenance.message_en` | 维护说明（英文） | `The system is under maintenance. Please try again later.` |
| `system.maintenance.estimated_time` | 预计恢复时间 | 空 |

### 备案配置
| config_key | 说明 | 默认值 |
|------------|------|--------|
| `footer.icp` | ICP备案号 | 空 |
| `footer.beian` | 公安备案号 | 空 |
| `footer.police_icon_url` | 公安备案图标URL | 空 |

### 平台架构配置
| config_key | 说明 |
|------------|------|
| `platform_config` | 平台和架构配置（JSONB：platforms、architectures、allowCustomPlatform、allowCustomArchitecture）|

### 社交链接配置
| config_key | 说明 |
|------------|------|
| `social.github` | GitHub 链接 |
| `social.twitter` | Twitter 链接 |
| `social.linkedin` | LinkedIn 链接 |
| `social.weibo` | 微博链接 |
| `social.wechat` | 微信链接 |
| `social.email` | 联系邮箱 |

## 关键索引

- `idx_users_email`, `idx_users_status`, `idx_users_created_at`
- `idx_products_status`, `idx_products_category`, `idx_products_tags` (GIN)
- `idx_products_download` (DESC), `idx_products_rating` (DESC), `idx_products_slug`
- `idx_versions_product`, `idx_versions_latest` (部分索引 WHERE is_latest=TRUE)
- `idx_comments_product`, `idx_comments_user`, `idx_comments_parent`
- `idx_feedbacks_status`, `idx_feedbacks_created_at`
- `idx_notifications_user` (复合: user_id, is_read, created_at DESC)
- `idx_downloads_product`, `idx_downloads_user` (部分索引)
- `idx_audit_user`, `idx_audit_action`

## 触发器

- `update_updated_at_column()`: 自动更新 `updated_at` 字段
- 应用于: users, products, product_comments, orders, subscriptions, i18n_messages, feedbacks

## 初始化数据

### 角色（5 个）
ANONYMOUS, USER, VIP, ADMIN, SUPER_ADMIN

### 权限（17 个）
PRODUCT:READ/CREATE/UPDATE/DELETE/AUDIT, VERSION:CREATE/ROLLBACK, COMMENT:CREATE/DELETE/AUDIT, USER:READ/UPDATE/BAN, ORDER:READ/REFUND, SYSTEM:CONFIG, STATS:VIEW

### 超级管理员
- 用户名: KirLab
- 邮箱: 3143285505@qq.com

## PostgreSQL 特性使用

- **JSONB**: products.screenshots, audit_logs.detail, products.display_versions
- **TEXT[]**: products.tags (GIN 索引)
- **VARCHAR(45)**: users.last_login_ip (从INET改为VARCHAR以兼容MyBatis-Plus)
- **INET**: download_records.ip_address
- **表分区**: download_records, user_access_logs (按月分区)
- **部分索引**: product_versions (is_latest=TRUE)
- **CHECK 约束**: status 枚举、rating 范围、rollout_percentage 范围
