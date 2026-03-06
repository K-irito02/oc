# ICP备案 + 公安备案功能完善计划

## 需求概述

根据中国法律法规要求，网站必须展示ICP备案号和公安备案号。本次任务需要完善备案信息的展示和管理功能，**备案信息不支持中英文切换**，但在管理后台修改备案信息时需要进行超级管理员邮箱验证。

### 核心要求

1. **ICP备案号（工信部）**
   - 格式：`黔ICP备XXXXXXXX号-1`（必须带网站序号）
   - 链接：`https://beian.miit.gov.cn/`
   - 位置：网站页脚底部

2. **公安备案号（网安备案）**
   - 格式：`黔公网安备XXXXXXXX号`
   - 链接：`https://beian.gov.cn/portal/registerSystemInfo?recordcode=公安备案号`
   - 推荐形式：官方图标 + 备案号文本 + 链接

3. **安全要求**
   - 备案信息**不支持中英文切换**，始终显示中文
   - 修改备案信息需要超级管理员邮箱验证
   - 必须使用 `target="_blank" rel="noopener noreferrer"` 安全链接

4. **超级管理员信息修改**
   - 用户名：`KirLab`
   - 邮箱：`3143285505@qq.com`

---

## 现有代码分析

### 当前问题

1. **链接错误**：公安备案和ICP备案都链接到 `https://beian.miit.gov.cn/`
2. **多余字段**：存在英文版本的备案字段（`footerBeianEn`, `footerIcpEn`），但需求要求不支持中英切换
3. **缺少安全验证**：修改备案信息没有二次验证
4. **超级管理员信息**：当前用户名为 `admin`，邮箱为 `admin@ocplatform.com`

### 现有配置字段

| 配置键 | 当前用途 | 修改方案 |
|--------|----------|----------|
| `footer.beian` | 公安备案号（中文） | 保留，作为公安备案号 |
| `footer.beian_en` | 公安备案号（英文） | **删除** |
| `footer.icp` | ICP备案号（中文） | 保留 |
| `footer.icp_en` | ICP备案号（英文） | **删除** |

### 新增配置字段

| 配置键 | 用途 | 说明 |
|--------|------|------|
| `footer.police_icon_url` | 公安备案图标URL | 可上传自定义图标，留空使用默认图标 |

---

## 实施步骤

### 第一阶段：数据库修改

#### 1.1 更新 `sql/init.sql`

**文件路径**: `e:\oc\oc-platform\sql\init.sql`

**修改内容**:
1. 修改超级管理员账号信息
2. 删除英文备案配置
3. 更新备案配置描述
4. 新增公安备案图标配置

```sql
-- 修改超级管理员账号
UPDATE users SET username = 'KirLab', email = '3143285505@qq.com' 
WHERE username = 'admin';

-- 删除旧的英文备案配置
DELETE FROM system_configs WHERE config_key IN ('footer.beian_en', 'footer.icp_en');

-- 更新现有配置描述
UPDATE system_configs SET description = '公安备案号（如：黔公网安备52010000000000号）' WHERE config_key = 'footer.beian';
UPDATE system_configs SET description = 'ICP备案号（如：黔ICP备12345678号-1）' WHERE config_key = 'footer.icp';

-- 新增公安备案图标配置
INSERT INTO system_configs (config_key, config_value, description) VALUES
    ('footer.police_icon_url', '', '公安备案图标URL（留空使用默认图标）');
```

---

### 第二阶段：后端修改

#### 2.1 新增备案信息验证DTO

**新建文件**: `e:\oc\oc-platform\oc-platform-common\src\main\java\com\ocplatform\common\dto\FilingConfigDTO.java`

```java
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class FilingConfigDTO {
    @NotBlank(message = "验证码不能为空")
    private String verificationCode;
    
    @NotBlank(message = "ICP备案号不能为空")
    private String icp;
    
    @NotBlank(message = "公安备案号不能为空")
    private String policeBeian;
    
    private String policeIconUrl;
}
```

#### 2.2 新增备案信息验证请求DTO

**新建文件**: `e:\oc\oc-platform\oc-platform-common\src\main\java\com\ocplatform\common\dto\SendFilingCodeRequest.java`

```java
@Data
public class SendFilingCodeRequest {
    // 无需参数，使用超级管理员邮箱
}
```

#### 2.3 更新 `AdminSystemController.java`

**文件路径**: `e:\oc\oc-platform\oc-platform-admin\src\main\java\com\ocplatform\admin\controller\AdminSystemController.java`

**新增API**:
1. `POST /api/v1/admin/system/filing/send-code` - 发送备案修改验证码
2. `GET /api/v1/admin/system/filing` - 获取备案配置
3. `PUT /api/v1/admin/system/filing` - 更新备案配置（需验证码）

#### 2.4 新增备案信息服务

**新建文件**: `e:\oc\oc-platform\oc-platform-admin\src\main\java\com\ocplatform\admin\service\FilingService.java`

**功能**:
- 发送验证码到超级管理员邮箱
- 验证验证码
- 更新备案配置

#### 2.5 更新 `PublicSiteController.java`

**文件路径**: `e:\oc\oc-platform\oc-platform-user\src\main\java\com\ocplatform\user\controller\PublicSiteController.java`

**修改内容**:
- 添加 `footer.police_icon_url` 到查询列表
- 移除 `footer.beian_en` 和 `footer.icp_en` 的映射
- 添加 `footerPoliceIconUrl` 字段映射

---

### 第三阶段：前端修改

#### 3.1 更新 `siteConfigSlice.ts`

**文件路径**: `e:\oc\oc-platform\oc-platform-web\src\store\slices\siteConfigSlice.ts`

**修改内容**:
- 移除 `footerBeianEn` 和 `footerIcpEn` 字段
- 添加 `footerPoliceIconUrl` 字段
- 重命名 `footerBeian` 为 `footerPoliceBeian`（更清晰）

#### 3.2 更新 `Footer.tsx`

**文件路径**: `e:\oc\oc-platform\oc-platform-web\src\components\layout\Footer.tsx`

**修改内容**:
1. 移除备案信息的中英文切换逻辑
2. 修改公安备案链接生成逻辑：
   - 从公安备案号中提取纯数字编号
   - 生成链接：`https://beian.gov.cn/portal/registerSystemInfo?recordcode=提取的编号`
3. 添加公安备案图标支持（默认图标 + 可配置自定义图标）
4. 确保ICP备案链接正确指向工信部

#### 3.3 更新 `Admin/System/index.tsx`

**文件路径**: `e:\oc\oc-platform\oc-platform-web\src\pages\Admin\System\index.tsx`

**修改内容**:
1. 移除备案信息的英文版本输入框
2. 添加邮箱验证流程：
   - 点击保存时弹出验证码输入框
   - 先发送验证码到超级管理员邮箱
   - 验证通过后才能保存
3. 添加公安备案图标URL配置
4. 更新保存逻辑调用新的API

#### 3.4 更新 `api.ts`

**文件路径**: `e:\oc\oc-platform\oc-platform-web\src\utils\api.ts`

**新增API**:
```typescript
// 备案配置API
sendFilingCode: () => request.post('/admin/system/filing/send-code'),
getFilingConfig: () => request.get('/admin/system/filing'),
updateFilingConfig: (data: { verificationCode: string; icp: string; policeBeian: string; policeIconUrl?: string }) =>
  request.put('/admin/system/filing', data),
```

#### 3.5 更新国际化文件

**文件路径**: 
- `e:\oc\oc-platform\oc-platform-web\src\locales\zh-CN.json`
- `e:\oc\oc-platform\oc-platform-web\src\locales\en-US.json`

**修改内容**:
- 移除英文备案相关的翻译键
- 添加公安备案图标相关的翻译
- 添加邮箱验证相关的翻译（支持中英切换）

---

## 详细代码修改清单

### 文件修改列表

| 序号 | 文件路径 | 修改类型 | 说明 |
|------|----------|----------|------|
| 1 | `sql/init.sql` | 修改 | 更新超级管理员信息和备案配置数据 |
| 2 | `FilingConfigDTO.java` | 新建 | 备案配置DTO |
| 3 | `SendFilingCodeRequest.java` | 新建 | 发送验证码请求DTO |
| 4 | `FilingService.java` | 新建 | 备案信息服务 |
| 5 | `AdminSystemController.java` | 修改 | 新增备案配置API |
| 6 | `PublicSiteController.java` | 修改 | 更新API返回字段 |
| 7 | `siteConfigSlice.ts` | 修改 | 更新状态管理字段 |
| 8 | `Footer.tsx` | 修改 | 重构备案信息展示逻辑 |
| 9 | `Admin/System/index.tsx` | 修改 | 更新管理后台配置表单，添加邮箱验证 |
| 10 | `api.ts` | 修改 | 新增备案配置API |
| 11 | `zh-CN.json` | 修改 | 更新中文翻译 |
| 12 | `en-US.json` | 修改 | 更新英文翻译 |

---

## 邮箱验证流程设计

### 流程图

```
┌─────────────────────────────────────────────────────────────────┐
│                    管理后台修改备案信息流程                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 超级管理员进入系统设置页面                                      │
│                    ↓                                            │
│  2. 修改ICP备案号/公安备案号                                       │
│                    ↓                                            │
│  3. 点击"保存"按钮                                                │
│                    ↓                                            │
│  4. 弹出邮箱验证对话框                                             │
│     ┌─────────────────────────────────────────┐                 │
│     │  📧 邮箱验证                             │                 │
│     │                                         │                 │
│     │  验证码将发送至: 314***@qq.com           │                 │
│     │                                         │                 │
│     │  [获取验证码] [60s后重新获取]             │                 │
│     │                                         │                 │
│     │  验证码: [______]                        │                 │
│     │                                         │                 │
│     │         [取消]  [确认保存]               │                 │
│     └─────────────────────────────────────────┘                 │
│                    ↓                                            │
│  5. 后端验证验证码                                                │
│     ├── 验证失败 → 提示错误，重新输入                              │
│     └── 验证成功 → 保存配置，刷新前端                              │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 后端验证逻辑

1. 发送验证码时，从数据库获取超级管理员邮箱（`role = 'SUPER_ADMIN'`）
2. 验证码类型：`FILING_VERIFY`
3. 验证码有效期：10分钟
4. 验证通过后标记验证码已使用

---

## 测试数据

使用以下测试数据进行开发验证：

```
超级管理员:
  用户名: KirLab
  邮箱: 3143285505@qq.com
  密码: Admin@123456

ICP备案号: 黔ICP备12345678号-1
公安备案号: 黔公网安备52010000000000号
公安备案链接: https://beian.gov.cn/portal/registerSystemInfo?recordcode=52010000000000
```

---

## 验收标准

1. ✅ 页脚正确显示ICP备案号，点击跳转到工信部网站
2. ✅ 页脚正确显示公安备案号+图标，点击跳转到公安备案详情页
3. ✅ 备案信息不随语言切换变化
4. ✅ 管理后台修改备案信息需要邮箱验证
5. ✅ 验证码发送到超级管理员邮箱（3143285505@qq.com）
6. ✅ 移动端备案信息可见、可点击
7. ✅ 链接使用 `target="_blank" rel="noopener noreferrer"`
8. ✅ 超级管理员用户名和邮箱已更新

---

## 风险评估

| 风险项 | 影响 | 缓解措施 |
|--------|------|----------|
| 删除英文配置字段 | 现有数据丢失 | 执行前备份，迁移脚本处理 |
| 公安备案号提取编号 | 格式多样 | 使用正则表达式提取纯数字 |
| 邮箱验证码发送失败 | 无法修改配置 | 提供重试机制，记录日志 |
| 超级管理员邮箱变更 | 验证码发送到错误邮箱 | 从数据库实时获取邮箱 |

---

## 实施顺序

1. **数据库修改** → 2. **后端DTO和服务** → 3. **后端API** → 4. **前端状态管理** → 5. **前端组件** → 6. **国际化** → 7. **测试验证**
