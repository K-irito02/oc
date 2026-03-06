# 登录支持用户名+密码 & 输入字符限制计划

## 背景

用户提出两个需求：
1. 登录时支持用户名+密码登录（目前只支持邮箱+密码）
2. 用户名和密码输入时需要限制，不可输入空格、表情、特殊符号等字符

## 现状分析

### 后端现状
- `LoginRequest.java`: 只有 `email` 和 `password` 字段
- `RegisterRequest.java`: 用户名验证已存在 `^[a-zA-Z0-9_-]+$`，密码验证只要求大小写字母和数字
- `UpdateProfileRequest.java`: 用户名验证已存在
- `AuthService.login()`: 只通过 email 查找用户
- `UserMapper`: 已有 `findByUsername()` 方法

### 前端现状
- `Login/index.tsx`: 登录表单只有 email 输入框
- `Register/index.tsx`: 注册表单有用户名，但前端没有验证用户名格式
- `Profile/index.tsx`: 修改用户名有验证规则，修改密码没有格式验证

---

## 详细实施步骤

### 步骤 1：修改后端登录请求 DTO

**文件**: `oc-platform-user/src/main/java/com/ocplatform/user/dto/LoginRequest.java`

将 `email` 字段改为 `account`（支持用户名或邮箱）：

```java
@Data
public class LoginRequest {
    @NotBlank(message = "账号不能为空")
    private String account;  // 用户名或邮箱

    @NotBlank(message = "密码不能为空")
    private String password;
}
```

### 步骤 2：修改后端登录服务

**文件**: `oc-platform-user/src/main/java/com/ocplatform/user/service/AuthService.java`

修改 `login()` 方法，支持用户名或邮箱登录：

```java
public LoginResponse login(LoginRequest request, String clientIp) {
    // ... 限流代码不变 ...

    String account = request.getAccount();
    User user;
    
    // 判断是邮箱还是用户名
    if (account.contains("@")) {
        user = userMapper.findByEmail(account)
                .orElseThrow(() -> new BusinessException(ErrorCode.USER_NOT_REGISTERED));
    } else {
        user = userMapper.findByUsername(account)
                .orElseThrow(() -> new BusinessException(ErrorCode.USER_NOT_REGISTERED));
    }

    // ... 后续验证代码不变 ...
}
```

### 步骤 3：修改后端密码验证规则

**文件**: `oc-platform-user/src/main/java/com/ocplatform/user/dto/RegisterRequest.java`

修改密码验证正则，禁止空格和特殊符号：

```java
@NotBlank(message = "密码不能为空")
@Size(min = 8, max = 64, message = "密码长度为 8-64 个字符")
@Pattern(regexp = "^[a-zA-Z0-9]+$", message = "密码只能包含字母和数字")
private String password;
```

**文件**: `oc-platform-user/src/main/java/com/ocplatform/user/dto/ChangePasswordRequest.java`

添加密码格式验证（如果不存在）：

```java
@NotBlank(message = "新密码不能为空")
@Size(min = 8, max = 64, message = "密码长度为 8-64 个字符")
@Pattern(regexp = "^[a-zA-Z0-9]+$", message = "密码只能包含字母和数字")
private String newPassword;
```

### 步骤 4：修改前端登录页面

**文件**: `oc-platform-web/src/pages/Login/index.tsx`

1. 将 `email` 字段改为 `account`
2. 修改输入框提示和图标
3. 添加前端验证

```tsx
<Form.Item
  name="account"
  rules={[
    { required: true, message: t('auth.accountRequired') },
    { 
      pattern: /^[a-zA-Z0-9_@.-]+$/, 
      message: t('auth.accountFormat') 
    }
  ]}
>
  <Input 
    prefix={<UserOutlined className="text-slate-400" />} 
    placeholder={t('auth.accountPlaceholder')} 
  />
</Form.Item>
```

### 步骤 5：修改前端注册页面

**文件**: `oc-platform-web/src/pages/Register/index.tsx`

添加用户名和密码的前端验证：

```tsx
<Form.Item
  name="username"
  rules={[
    { required: true, message: t('auth.usernameRequired') },
    { min: 3, max: 50, message: t('auth.usernameLength') },
    { pattern: /^[a-zA-Z0-9_-]+$/, message: t('auth.usernameFormat') }
  ]}
>
  <Input ... />
</Form.Item>

<Form.Item
  name="password"
  rules={[
    { required: true, message: t('auth.passwordRequired') },
    { min: 8, max: 64, message: t('auth.passwordLength') },
    { pattern: /^[a-zA-Z0-9]+$/, message: t('auth.passwordFormat') },
    { 
      pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, 
      message: t('auth.passwordPattern') 
    }
  ]}
>
  <Input.Password ... />
</Form.Item>
```

### 步骤 6：修改前端个人资料页面

**文件**: `oc-platform-web/src/pages/Profile/index.tsx`

添加修改密码时的前端验证：

```tsx
<Form.Item label={t('profile.newPassword')} name="newPassword" rules={[
  { required: true, message: t('auth.passwordRequired') },
  { min: 8, max: 64, message: t('auth.passwordLength') },
  { pattern: /^[a-zA-Z0-9]+$/, message: t('auth.passwordFormat') },
  { 
    pattern: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, 
    message: t('auth.passwordPattern') 
  }
]}>
  <Input.Password ... />
</Form.Item>
```

### 步骤 7：修改前端 API 文件

**文件**: `oc-platform-web/src/utils/api.ts`

修改登录 API 调用参数：

```ts
login: (data: { account: string; password: string }) => 
  request.post('/auth/login', data),
```

### 步骤 8：添加国际化翻译

**文件**: `oc-platform-web/src/locales/zh-CN.json`

在 `auth` 部分添加：

```json
{
  "auth": {
    "account": "账号",
    "accountPlaceholder": "用户名或邮箱",
    "accountRequired": "请输入用户名或邮箱",
    "accountFormat": "账号格式不正确",
    "usernameFormat": "用户名只能包含字母、数字、下划线和连字符",
    "passwordFormat": "密码只能包含字母和数字",
    "passwordLength": "密码长度为 8-64 个字符"
  }
}
```

**文件**: `oc-platform-web/src/locales/en-US.json`

在 `auth` 部分添加：

```json
{
  "auth": {
    "account": "Account",
    "accountPlaceholder": "Username or Email",
    "accountRequired": "Please enter username or email",
    "accountFormat": "Invalid account format",
    "usernameFormat": "Username can only contain letters, numbers, underscores and hyphens",
    "passwordFormat": "Password can only contain letters and numbers",
    "passwordLength": "Password must be 8-64 characters"
  }
}
```

---

## 涉及的文件清单

### 后端文件（需修改）

| 文件 | 操作 | 说明 |
|------|------|------|
| `LoginRequest.java` | 修改 | email → account |
| `AuthService.java` | 修改 | 支持用户名或邮箱登录 |
| `RegisterRequest.java` | 修改 | 密码格式验证 |
| `ChangePasswordRequest.java` | 修改 | 新密码格式验证 |

### 前端文件（需修改）

| 文件 | 操作 | 说明 |
|------|------|------|
| `Login/index.tsx` | 修改 | 支持用户名或邮箱登录 |
| `Register/index.tsx` | 修改 | 添加用户名和密码验证 |
| `Profile/index.tsx` | 修改 | 添加密码格式验证 |
| `api.ts` | 修改 | 登录 API 参数 |
| `zh-CN.json` | 修改 | 添加中文翻译 |
| `en-US.json` | 修改 | 添加英文翻译 |

---

## 验证规则总结

### 用户名验证
- 长度：3-50 个字符
- 格式：`^[a-zA-Z0-9_-]+$`（只允许字母、数字、下划线、连字符）
- 不允许：空格、表情、特殊符号

### 密码验证
- 长度：8-64 个字符
- 格式：`^[a-zA-Z0-9]+$`（只允许字母和数字）
- 复杂度：必须包含大小写字母和数字
- 不允许：空格、表情、特殊符号

### 登录账号验证
- 格式：`^[a-zA-Z0-9_@.-]+$`（允许用户名或邮箱格式）
- 自动判断：包含 `@` 视为邮箱，否则视为用户名

---

## 验证清单

- [ ] 后端编译通过
- [ ] 前端编译通过（npm run build）
- [ ] 前端代码检查通过（npm run lint）
- [ ] 用户名登录测试
- [ ] 邮箱登录测试
- [ ] 注册时用户名格式验证
- [ ] 注册时密码格式验证
- [ ] 修改密码时格式验证
- [ ] 中英文翻译正确显示

---

## 注意事项

1. **向后兼容**：修改后，旧的登录 API 调用（使用 email 字段）将不再工作，前端需要同步更新。

2. **密码复杂度**：虽然限制了只能使用字母和数字，但仍要求必须包含大小写字母和数字，保证安全性。

3. **用户体验**：登录页面提示用户可以使用用户名或邮箱登录，避免用户困惑。

4. **错误提示**：登录失败时，不区分是用户名不存在还是密码错误，统一提示"用户名或密码错误"，防止账号枚举攻击。
