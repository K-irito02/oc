# 用户管理超级管理员保护功能修复计划

## 问题描述

管理后台的用户管理存在安全问题：超级管理员账号可以被"锁定"和"禁用"。超级管理员账号不应该支持"锁定"和"禁用"操作。

## 问题分析

### 当前实现问题

1. **前端**：用户列表页面 (`Users/index.tsx`) 对所有用户都显示"锁定"和"禁用"按钮，没有判断用户角色
2. **后端**：`UserService.updateUserStatus()` 方法没有检查目标用户是否是超级管理员

### 影响范围

| 层级 | 文件 | 修改内容 |
|------|------|----------|
| 后端 | `UserService.java` | 添加超级管理员保护逻辑 |
| 后端 | `ErrorCode.java` | 添加新的错误码（如需要） |
| 前端 | `Users/index.tsx` | 超级管理员隐藏操作按钮 |
| 国际化 | `zh-CN.json` | 添加中文提示 |
| 国际化 | `en-US.json` | 添加英文提示 |

## 实现步骤

### 步骤 1：后端 - 添加超级管理员保护逻辑

**文件**：`e:\oc\oc-platform\oc-platform-user\src\main\java\com\ocplatform\user\service\UserService.java`

**修改内容**：
- 在 `updateUserStatus()` 方法中添加检查
- 查询目标用户的角色列表
- 如果用户拥有 `SUPER_ADMIN` 角色，抛出业务异常
- 禁止将超级管理员状态改为 `LOCKED` 或 `BANNED`

```java
public void updateUserStatus(Long userId, String status) {
    User user = userMapper.selectById(userId);
    if (user == null) {
        throw new BusinessException(ErrorCode.USER_NOT_FOUND);
    }
    
    // 检查是否为超级管理员
    List<String> roles = roleMapper.findRolesByUserId(userId).stream()
            .map(Role::getCode).collect(Collectors.toList());
    if (roles.contains("SUPER_ADMIN") && ("LOCKED".equals(status) || "BANNED".equals(status))) {
        throw new BusinessException(ErrorCode.ACCESS_DENIED, "超级管理员账号不能被锁定或禁用");
    }
    
    user.setStatus(status);
    userMapper.updateById(user);
    log.info("User {} status changed to {}", userId, status);
}
```

### 步骤 2：前端 - 隐藏超级管理员操作按钮

**文件**：`e:\oc\oc-platform\oc-platform-web\src\pages\Admin\Users\index.tsx`

**修改内容**：
- 在操作列渲染时检查用户角色
- 如果用户是超级管理员（`roles` 包含 `SUPER_ADMIN`），隐藏"锁定"和"禁用"按钮
- 可选：显示"超级管理员"标签或提示

```tsx
{
  title: t('admin.action'), width: 180, fixed: 'right',
  render: (_, record) => {
    // 检查是否为超级管理员
    const isSuperAdmin = record.roles?.includes('SUPER_ADMIN');
    
    if (isSuperAdmin) {
      return <span className="text-slate-400 text-sm">{t('admin.superAdminProtected')}</span>;
    }
    
    return (
      <Space>
        {/* 原有按钮逻辑 */}
      </Space>
    );
  },
}
```

### 步骤 3：国际化 - 添加翻译键

**文件 1**：`e:\oc\oc-platform\oc-platform-web\src\locales\zh-CN.json`

在 `admin` 对象中添加：
```json
{
  "admin": {
    // ... 现有翻译 ...
    "superAdminProtected": "超级管理员受保护",
    "cannotModifySuperAdmin": "超级管理员账号不能被锁定或禁用"
  }
}
```

**文件 2**：`e:\oc\oc-platform\oc-platform-web\src\locales\en-US.json`

在 `admin` 对象中添加：
```json
{
  "admin": {
    // ... existing translations ...
    "superAdminProtected": "Super Admin Protected",
    "cannotModifySuperAdmin": "Super admin account cannot be locked or banned"
  }
}
```

### 步骤 4：测试验证

1. 使用技能重启项目（Docker 服务 + 后端 + 前端）
2. 使用技能进行测试：
   - 登录管理后台
   - 查看用户列表
   - 验证超级管理员账号不显示"锁定"和"禁用"按钮
   - 验证后端 API 拒绝修改超级管理员状态

## 文件修改清单

| 序号 | 文件路径 | 修改类型 |
|------|----------|----------|
| 1 | `oc-platform-user/src/main/java/com/ocplatform/user/service/UserService.java` | 修改 |
| 2 | `oc-platform-web/src/pages/Admin/Users/index.tsx` | 修改 |
| 3 | `oc-platform-web/src/locales/zh-CN.json` | 修改 |
| 4 | `oc-platform-web/src/locales/en-US.json` | 修改 |

## 注意事项

1. 超级管理员判断使用角色代码 `SUPER_ADMIN`
2. 后端和前端双重保护，确保安全性
3. 国际化支持中英文切换
4. 保持代码风格与现有代码一致
