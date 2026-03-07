# 部署前准备计划

> 创建时间: 2026-03-07

## 任务概述

1. 在所有页面底部添加备案信息：`黔ICP备2026002901号-1`
2. 清空数据库数据，保留超级管理员账号（用户名：`KirLab`，邮箱：`3143285505@qq.com`，密码：`Smg.2026`）
3. 重启项目
4. 上传代码到远程仓库

***

## 任务 1：添加备案信息

### 1.1 分析页面结构

**使用 MainLayout 的页面（已有 Footer）：**

* 首页 `/`

* 产品列表 `/products`

* 产品详情 `/products/:slug`

* 用户中心 `/user/*`

* 管理后台 `/admin/*`

* 其他使用 MainLayout 的页面

**不使用 MainLayout 的页面（需要单独添加备案信息）：**

* 登录页面 `/login` - `src/pages/Login/index.tsx`

* 注册页面 `/register` - `src/pages/Register/index.tsx`

* 忘记密码 `/forgot-password` - `src/pages/ForgotPassword/index.tsx`

* OAuth 回调 `/oauth/callback` - `src/pages/OAuthCallback/index.tsx`

* 404 页面 - `src/pages/NotFound/index.tsx`

* 错误页面 - `src/pages/Error/index.tsx`

* 维护页面 - `src/pages/Maintenance/index.tsx`

### 1.2 实施步骤

#### 步骤 1.2.1：修改 Footer.tsx

* 文件：`oc-platform-web/src/components/layout/Footer.tsx`

* 操作：取消注释 ICP 备案部分，填入 `黔ICP备2026002901号-1`

* 修改内容：

  ```tsx
  {/* ICP备案 */}
  <a 
    href="https://beian.miit.gov.cn/" 
    target="_blank" 
    rel="noopener noreferrer"
    className="flex items-center gap-2 px-4 py-2 bg-white rounded-lg shadow-sm border border-gray-200 hover:shadow-md hover:border-gray-300 transition-all duration-200"
  >
    <Shield size={18} className="text-blue-500" />
    <span className="text-sm text-gray-700 font-medium">黔ICP备2026002901号-1</span>
  </a>
  ```

#### 步骤 1.2.2：创建备案信息组件

* 文件：`oc-platform-web/src/components/FilingInfo.tsx`（新建）

* 用途：在认证页面底部显示备案信息

* 内容：简洁的备案信息展示

#### 步骤 1.2.3：在认证页面添加备案信息

* 文件：

  * `src/pages/Login/index.tsx`

  * `src/pages/Register/index.tsx`

  * `src/pages/ForgotPassword/index.tsx`

* 操作：在页面底部添加 FilingInfo 组件

#### 步骤 1.2.4：在其他独立页面添加备案信息

* 文件：

  * `src/pages/NotFound/index.tsx`

  * `src/pages/Error/index.tsx`

  * `src/pages/Maintenance/index.tsx`

* 操作：在页面底部添加 FilingInfo 组件

***

## 任务 2：清空数据库数据

### 2.1 创建数据库清理脚本

#### 步骤 2.1.1：创建清理 SQL 脚本

* 文件：`sql/clear-data.sql`（新建）

* 内容：

  ```sql
  -- 清空所有业务数据表（保留角色、权限、系统配置）
  TRUNCATE TABLE site_feedback_likes CASCADE;
  TRUNCATE TABLE site_feedbacks CASCADE;
  TRUNCATE TABLE comment_likes CASCADE;
  TRUNCATE TABLE product_comments CASCADE;
  TRUNCATE TABLE product_ratings CASCADE;
  TRUNCATE TABLE product_versions CASCADE;
  TRUNCATE TABLE delta_updates CASCADE;
  TRUNCATE TABLE products CASCADE;
  TRUNCATE TABLE categories CASCADE;
  TRUNCATE TABLE notifications CASCADE;
  TRUNCATE TABLE download_records_2026_01;
  TRUNCATE TABLE download_records_2026_02;
  TRUNCATE TABLE download_records_2026_03;
  TRUNCATE TABLE download_records_2026_04;
  TRUNCATE TABLE download_records_2026_05;
  TRUNCATE TABLE download_records_2026_06;
  TRUNCATE TABLE file_records CASCADE;
  TRUNCATE TABLE audit_logs CASCADE;
  TRUNCATE TABLE email_verifications CASCADE;
  TRUNCATE TABLE captcha_records CASCADE;
  TRUNCATE TABLE user_oauth_bindings CASCADE;
  TRUNCATE TABLE user_roles CASCADE;
  TRUNCATE TABLE users CASCADE;
  TRUNCATE TABLE subscriptions CASCADE;
  TRUNCATE TABLE orders CASCADE;
  ```

#### 步骤 2.1.2：更新超级管理员密码

* 需要生成密码 `Smg.2026` 的 BCrypt 哈希值

* 更新 init.sql 中的密码哈希

### 2.2 检查 init.sql 完整性

#### 需要检查的内容：

1. ✅ 所有表结构定义完整
2. ✅ 所有索引创建完整
3. ✅ 所有触发器定义完整
4. ✅ 角色和权限初始化数据完整
5. ✅ 系统配置初始化数据完整
6. ✅ 超级管理员账号初始化完整

#### 当前 init.sql 状态：

* 文件位置：`oc-platform/sql/init.sql`

* 文件大小：1078 行

* 包含内容：

  * 用户表、角色表、权限表等核心表结构

  * 产品、版本、评论等业务表结构

  * 下载记录分区表

  * 所有必要的索引

  * updated\_at 自动更新触发器

  * 角色和权限初始化数据

  * 超级管理员账号（KirLab）

  * 系统配置初始化

### 2.3 实施步骤

#### 步骤 2.3.1：生成新密码哈希

* 使用 BCrypt 算法生成密码 `Smg.2026` 的哈希值

* 在线工具或后端代码生成

#### 步骤 2.3.2：更新 init.sql

* 更新超级管理员密码哈希

* 确保所有初始化数据正确

#### 步骤 2.3.3：执行数据库清理

* 连接到 Docker PostgreSQL 容器

* 执行清理脚本

* 重新创建超级管理员账号

***

## 任务 3：重启项目

### 3.1 实施步骤

#### 步骤 3.1.1：停止当前项目

* 停止前端开发服务器

* 停止后端 Java 进程

* 停止 Docker 依赖服务（可选）

#### 步骤 3.1.2：重新启动项目

* 使用 oc-platform-manager 技能启动项目

* 验证所有服务正常

***

## 任务 4：上传代码到远程仓库

### 4.1 实施步骤

#### 步骤 4.1.1：检查代码变更

* 检查环境配置仓库（e:\oc）的变更

* 检查项目代码仓库（e:\oc\oc-platform）的变更

#### 步骤 4.1.2：提交变更

* 环境配置仓库：

  * 提交类型：`feat`

  * 提交信息：`feat: 添加备案信息显示`

* 项目代码仓库：

  * 提交类型：`feat`

  * 提交信息：`feat: 添加备案信息显示，更新数据库初始化脚本`

#### 步骤 4.1.3：推送到远程

* 推送到 main 分支

***

## 文件变更清单

### 新建文件

| 文件路径                                            | 说明      |
| ----------------------------------------------- | ------- |
| `oc-platform/sql/clear-data.sql`                | 数据库清理脚本 |
| `oc-platform-web/src/components/FilingInfo.tsx` | 备案信息组件  |

### 修改文件

| 文件路径                                                 | 说明         |
| ---------------------------------------------------- | ---------- |
| `oc-platform-web/src/components/layout/Footer.tsx`   | 添加 ICP 备案号 |
| `oc-platform-web/src/pages/Login/index.tsx`          | 添加备案信息     |
| `oc-platform-web/src/pages/Register/index.tsx`       | 添加备案信息     |
| `oc-platform-web/src/pages/ForgotPassword/index.tsx` | 添加备案信息     |
| `oc-platform-web/src/pages/NotFound/index.tsx`       | 添加备案信息     |
| `oc-platform-web/src/pages/Error/index.tsx`          | 添加备案信息     |
| `oc-platform-web/src/pages/Maintenance/index.tsx`    | 添加备案信息     |
| `oc-platform/sql/init.sql`                           | 更新超级管理员密码  |

***

## 风险评估

### 低风险

* 添加备案信息：仅前端 UI 修改，不影响业务逻辑

### 中风险

* 数据库清理：会删除所有业务数据，需要谨慎操作

* 建议：在执行前备份重要数据

### 注意事项

1. 数据库清理操作不可逆，请确保已备份重要数据
2. 超级管理员密码更新后，需要使用新密码登录
3. 前端代码修改后需要重新构建

***

## 执行顺序

1. ✅ 添加备案信息（前端代码修改）
2. ✅ 创建数据库清理脚本
3. ✅ 更新超级管理员密码
4. ✅ 重启项目
5. ✅ 执行数据库清理
6. ✅ 验证超级管理员登录
7. ✅ 提交代码到远程仓库

