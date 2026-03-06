# 数据库用户和SQL文件更新计划

## 目标

1. 将 `KirLab` 用户设置为超级管理员（SUPER_ADMIN 角色）
2. 删除 `admin` 测试超级管理员用户
3. 更新 `sql/init.sql` 主初始化脚本
4. 删除迁移SQL文件（`sql/seed.sql` 和 `sql/reset-products.sql`）
5. 确保备案邮件发送到正确的邮箱

## 当前状态

### 数据库现状
- `admin` 用户：id=1, 角色=SUPER_ADMIN, 邮箱=admin@ocplatform.com
- `KirLab` 用户：id=2, 角色=USER, 邮箱=3143285505@qq.com

### SQL文件现状
- `sql/init.sql`：已配置 KirLab 为 SUPER_ADMIN
- `sql/seed.sql`：引用 admin 用户创建测试数据
- `sql/reset-products.sql`：引用 admin 用户重置产品

## 实施步骤

### 步骤 1: 更新容器数据库

```sql
-- 1. 将 KirLab 设置为 SUPER_ADMIN
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id FROM users u, roles r
WHERE u.username = 'KirLab' AND r.code = 'SUPER_ADMIN'
ON CONFLICT DO NOTHING;

-- 2. 删除 admin 用户的角色关联
DELETE FROM user_roles 
WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 3. 将 admin 用户的产品转移到 KirLab
UPDATE products 
SET developer_id = (SELECT id FROM users WHERE username = 'KirLab')
WHERE developer_id = (SELECT id FROM users WHERE username = 'admin');

-- 4. 删除 admin 用户的评论
DELETE FROM product_comments 
WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 5. 删除 admin 用户的评论
DELETE FROM notifications 
WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 6. 删除 admin 用户
DELETE FROM users WHERE username = 'admin';
```

### 步骤 2: 更新 sql/init.sql

确认文件中已正确配置：
- 用户名: `KirLab`
- 邮箱: `3143285505@qq.com`
- 角色: `SUPER_ADMIN`

### 步骤 3: 删除迁移SQL文件

删除以下文件：
- `sql/seed.sql`
- `sql/reset-products.sql`

### 步骤 4: 验证

1. 在管理后台系统设置页面测试发送验证码
2. 确认邮件发送到 `3143285505@qq.com`

---

## 注意事项

1. 备案修改验证码将发送到 `3143285505@qq.com`（KirLab 的邮箱）
2. 删除 `admin` 用户前需要转移其关联数据
3. 操作完成后需要重启后端服务以刷新缓存
