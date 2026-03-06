# 删除管理后台备案配置功能计划

## 背景

用户备案成功后，希望直接在页面源代码中写死备案信息（ICP备案号、公安备案号、备案图标），不再需要通过管理后台动态配置。因此需要删除管理后台中"备案"相关的所有配置功能。

## 涉及的文件

### 后端文件（需修改/删除）

| 文件 | 操作 | 说明 |
|------|------|------|
| `oc-platform-admin/src/main/java/com/ocplatform/admin/service/FilingService.java` | **删除** | 备案服务类，包含发送验证码、验证、更新备案配置等功能 |
| `oc-platform-common/src/main/java/com/ocplatform/common/dto/FilingConfigDTO.java` | **删除** | 备案配置DTO类 |
| `oc-platform-admin/src/main/java/com/ocplatform/admin/controller/AdminSystemController.java` | **修改** | 删除备案相关的3个API端点和依赖注入 |
| `oc-platform-user/src/main/java/com/ocplatform/user/controller/PublicSiteController.java` | **修改** | 删除备案配置的获取逻辑 |

### 前端文件（需修改）

| 文件 | 操作 | 说明 |
|------|------|------|
| `oc-platform-web/src/pages/Admin/System/index.tsx` | **修改** | 删除备案配置表单、验证码弹窗、相关状态和函数 |
| `oc-platform-web/src/utils/api.ts` | **修改** | 删除备案相关的API调用方法 |
| `oc-platform-web/src/components/layout/Footer.tsx` | **修改** | 删除动态备案显示，保留静态备案信息位置供用户手动填写 |
| `oc-platform-web/src/locales/zh-CN.json` | **修改** | 删除备案相关的中文翻译 |
| `oc-platform-web/src/locales/en-US.json` | **修改** | 删除备案相关的英文翻译 |

### 数据库（需清理）

| 表 | 操作 | 说明 |
|------|------|------|
| `system_configs` | **删除记录** | 删除 `footer.icp`、`footer.beian`、`footer.police_icon_url` 配置项 |

---

## 详细实施步骤

### 步骤 1：删除后端备案服务类

1. 删除 `FilingService.java` 文件
2. 删除 `FilingConfigDTO.java` 文件

### 步骤 2：修改 AdminSystemController

1. 删除 `FilingService` 的依赖注入
2. 删除以下三个 API 端点：
   - `POST /filing/send-code` - 发送备案验证码
   - `GET /filing` - 获取备案配置
   - `PUT /filing` - 更新备案配置
3. 删除 `maskEmail` 辅助方法

### 步骤 3：修改 PublicSiteController

1. 从配置查询列表中移除：
   - `footer.beian`
   - `footer.police_icon_url`
   - `footer.icp`
2. 删除对应的 switch case 分支
3. 删除对应的默认值设置

### 步骤 4：修改前端管理页面

1. 删除备案相关的状态变量：
   - `footerConfig` 中的 `policeBeian`、`policeIconUrl`、`icp`
   - `filingModalVisible`、`filingVerificationCode`、`filingCodeSending`、`filingCountdown`、`superAdminEmail`
   
2. 删除备案相关的函数：
   - `handleFilingSaveClick`
   - `handleSendFilingCode`
   - `handleFilingConfirm`
   
3. 删除备案配置卡片 UI（公安备案号、图标URL、ICP备案号输入框和保存按钮）

4. 删除备案验证弹窗 Modal

5. 删除相关的 API 调用和数据加载逻辑

### 步骤 5：修改前端 API 文件

删除 `adminApi` 对象中的以下方法：
- `sendFilingCode`
- `getFilingConfig`
- `updateFilingConfig`

### 步骤 6：修改 Footer 组件

1. 删除从 `siteConfig` 获取备案信息的逻辑
2. 删除 `extractPoliceCode` 函数
3. 删除动态备案显示代码
4. **保留**备案信息的展示位置，添加注释提示用户在此处手动填写备案信息

修改后的 Footer 将提供一个静态模板，用户可以直接编辑源代码填写：
- ICP 备案号
- 公安备案号
- 备案图标 URL

### 步骤 7：修改国际化文件

从 `zh-CN.json` 和 `en-US.json` 中删除 `adminSystem` 下备案相关的翻译键：
- `filingNote`
- `policeBeian` / `policeBeianPlaceholder`
- `policeIconUrl` / `policeIconUrlPlaceholder`
- `icp` / `icpPlaceholder`
- `saveFiling`
- `filingVerifyTitle` / `filingVerifyDesc`
- `sendCode` / `resendAfter`
- `verificationCode` / `verificationCodePlaceholder`
- `filingCodeSent` / `filingCodeRequired`
- `confirmSave`

### 步骤 8：清理数据库配置

执行 SQL 删除备案相关配置记录：
```sql
DELETE FROM system_configs WHERE config_key IN ('footer.icp', 'footer.beian', 'footer.police_icon_url');
```

---

## 验证清单

- [ ] 后端编译通过
- [ ] 前端编译通过（npm run build）
- [ ] 前端代码检查通过（npm run lint）
- [ ] 管理后台系统设置页面正常显示，无备案配置区域
- [ ] 前台 Footer 正常显示，备案信息区域可手动编辑
- [ ] API 接口已删除，调用返回 404

---

## 注意事项

1. **Footer 保留静态模板**：Footer 组件中保留备案信息的展示位置，但改为静态代码，用户需要直接编辑源代码填写备案信息。

2. **数据库清理**：删除功能后，数据库中可能存在残留的备案配置记录，需要手动清理。

3. **向后兼容**：此修改会移除备案动态配置功能，已配置的备案信息将不再生效，用户需要在 Footer 组件中手动填写。
