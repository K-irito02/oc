# 数据库用户和SQL文件整理计划

## 问题分析

### 当前数据库状态
- `admin` 用户 (id=1): SUPER_ADMIN, 邮箱 `admin@ocplatform.com`
- `KirLab` 用户 (id=2): 普通USER, 邮箱 `3143285505@qq.com`

### 期望状态
- `KirLab` 用户: SUPER_ADMIN, 邮箱 `3143285505@qq.com`
- 删除 `admin` 测试用户

### 相关文件
- `sql/init.sql` - 主初始化脚本（已配置 KirLab 为 SUPER_ADMIN）
- `sql/seed.sql` - 种子数据文件（引用 admin 用户）
- `sql/reset-products.sql` - 产品重置脚本（引用 admin 用户）

---

## 实施步骤

### 步骤 1: 更新容器数据库

1.1 将 `KirLab` 用户设置为 SUPER_ADMIN
```sql
-- 删除 KirLab 现有的 USER 角色
DELETE FROM user_roles WHERE user_id = (SELECT id FROM users WHERE username = 'KirLab');

-- 添加 SUPER_ADMIN 角色给 KirLab
INSERT INTO user_roles (user_id, role_id)
SELECT u.id, r.id FROM users u, roles r
WHERE u.username = 'KirLab' AND r.code = 'SUPER_ADMIN';
```

1.2 处理 `admin` 用户相关数据
```sql
-- 将 admin 用户的产品转移到 KirLab
UPDATE products SET developer_id = (SELECT id FROM users WHERE username = 'KirLab') 
WHERE developer_id = (SELECT id FROM users WHERE username = 'admin');

-- 删除 admin 用户的评论
DELETE FROM product_comments WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 删除 admin 用户的其他关联数据（如有）
DELETE FROM user_oauth WHERE user_id = (SELECT id FROM users WHERE username = 'admin');
DELETE FROM email_verifications WHERE user_id = (SELECT id FROM users WHERE username = 'admin');
DELETE FROM notifications WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 删除 admin 用户的角色关联
DELETE FROM user_roles WHERE user_id = (SELECT id FROM users WHERE username = 'admin');

-- 最后删除 admin 用户
DELETE FROM users WHERE username = 'admin';
```

### 步骤 2: 更新 init.sql 文件

2.1 确认 init.sql 中的超级管理员配置正确
- 用户名: `KirLab`
- 邮箱: `3143285505@qq.com`
- 角色: `SUPER_ADMIN`

2.2 添加测试用户（可选，保留 zhangsan、lisi 等测试用户）

### 步骤 3: 更新迁移脚本中的用户引用

3.1 更新 `reset-products.sql`
- 将所有 `u.username = 'admin'` 改为 `u.username = 'KirLab'`

3.2 更新 `seed.sql`
- 将所有 `u.username = 'admin'` 改为 `u.username = 'KirLab'`（如有）

### 步骤 4: 删除迁移SQL文件

删除以下文件：
- `sql/seed.sql`
- `sql/reset-products.sql`

### 步骤 5: 验证

5.1 验证数据库用户
```sql
SELECT u.id, u.username, u.email, u.status, r.code as role 
FROM users u 
LEFT JOIN user_roles ur ON u.id = ur.user_id 
LEFT JOIN roles r ON ur.role_id = r.id 
ORDER BY u.id;
```

5.2 验证备案邮件发送
- 在管理后台系统设置页面测试发送验证码
- 确认邮件发送到 `3143285505@qq.com`

---

## 文件修改清单

| 文件 | 操作 |
|------|------|
| `sql/init.sql` | 确认/更新超级管理员配置 |
| `sql/seed.sql` | 删除 |
| `sql/reset-products.sql` | 删除 |
| 容器数据库 | 执行用户迁移SQL |

---

## 注意事项

1. 备案修改验证码将发送到 `3143285505@qq.com`（KirLab 的邮箱）
2. 删除 `admin` 用户前需要转移其关联数据
3. 操作完成后需要重启后端服务以刷新缓存
