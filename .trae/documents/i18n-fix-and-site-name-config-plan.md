# 国际化修复与网站名称配置计划

## 问题分析

### 问题1：网站名称默认值不正确
- **现状**：默认配置中 `siteName` 和 `siteNameEn` 都是 `KiritoLab`
- **期望**：中文默认 `桐人创研`，英文默认 `KirLab`
- **影响文件**：
  - `oc-platform-web/src/store/slices/siteConfigSlice.ts` - 前端默认配置
  - 后端数据库默认配置（如果有的话）

### 问题2：留言板空状态显示登录按钮
- **现状**：当没有留言时，显示"暂无留言"和登录按钮
- **期望**：只显示"暂无留言"文本，不显示登录按钮
- **影响文件**：
  - `oc-platform-web/src/components/home/FeedbackSection.tsx`

### 问题3：产品列表空状态文本不支持国际化
- **现状**：硬编码 `"No products found"`
- **期望**：使用 i18n 翻译，支持中英文切换
- **影响文件**：
  - `oc-platform-web/src/pages/Products/index.tsx`
  - `oc-platform-web/src/locales/zh-CN.json`
  - `oc-platform-web/src/locales/en-US.json`

## 实施计划

### 任务1：修复网站名称默认值

#### 1.1 修改前端默认配置
**文件**：`oc-platform-web/src/store/slices/siteConfigSlice.ts`

修改 `defaultConfig` 对象：
```typescript
const defaultConfig: SiteConfig = {
  siteName: '桐人创研',      // 中文默认名称
  siteNameEn: 'KirLab',     // 英文默认名称
  // ... 其他配置保持不变
};
```

#### 1.2 检查并更新后端数据库默认配置
**文件**：`sql/init.sql`

检查系统配置表中是否有网站名称的默认值，如果有则更新为：
- `site_name`: `桐人创研`
- `site_name_en`: `KirLab`

### 任务2：移除留言板空状态的登录按钮

**文件**：`oc-platform-web/src/components/home/FeedbackSection.tsx`

修改空状态显示逻辑（约第515-523行）：

**修改前**：
```tsx
feedbacks.length === 0 ? (
  <div className="text-center py-10 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 flex-1 flex flex-col items-center justify-center min-h-[200px]">
    <p className="text-slate-600 dark:text-slate-400 mb-4">{t('feedback.noMessages')}</p>
    {isAuthenticated ? (
      <Button type="link" className="text-blue-600 hover:text-blue-700">{t('feedback.beFirst')}</Button>
    ) : (
      <Link to="/login"><Button type="primary">{t('common.login')}</Button></Link>
    )}
  </div>
)
```

**修改后**：
```tsx
feedbacks.length === 0 ? (
  <div className="text-center py-10 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-800 flex-1 flex flex-col items-center justify-center min-h-[200px]">
    <p className="text-slate-600 dark:text-slate-400">{t('feedback.noMessages')}</p>
  </div>
)
```

### 任务3：修复产品列表空状态国际化

#### 3.1 添加翻译键
**文件**：`oc-platform-web/src/locales/zh-CN.json`

在 `product` 部分添加：
```json
"product": {
  // ... 现有翻译
  "noProducts": "暂无产品"
}
```

**文件**：`oc-platform-web/src/locales/en-US.json`

在 `product` 部分添加：
```json
"product": {
  // ... 现有翻译
  "noProducts": "No products found"
}
```

#### 3.2 修改产品列表页面
**文件**：`oc-platform-web/src/pages/Products/index.tsx`

修改空状态显示（约第138-141行）：

**修改前**：
```tsx
<Empty
  description={<span className="text-slate-500 dark:text-slate-400">No products found</span>}
  className="py-20"
/>
```

**修改后**：
```tsx
<Empty
  description={<span className="text-slate-500 dark:text-slate-400">{t('product.noProducts')}</span>}
  className="py-20"
/>
```

## 验证计划

### 验证1：网站名称
1. 清除浏览器 localStorage 和 Redux 状态
2. 刷新页面，检查网站名称显示
3. 切换语言，验证中英文切换效果

### 验证2：留言板空状态
1. 确保数据库中没有留言数据
2. 访问首页留言板区域
3. 验证只显示"暂无留言"文本，无登录按钮

### 验证3：产品列表空状态
1. 确保数据库中没有产品数据
2. 访问产品列表页面
3. 切换语言，验证空状态文本切换

## 文件修改清单

| 文件 | 修改类型 | 说明 |
|------|----------|------|
| `oc-platform-web/src/store/slices/siteConfigSlice.ts` | 修改 | 更新默认网站名称 |
| `oc-platform-web/src/components/home/FeedbackSection.tsx` | 修改 | 移除空状态登录按钮 |
| `oc-platform-web/src/pages/Products/index.tsx` | 修改 | 使用 i18n 翻译 |
| `oc-platform-web/src/locales/zh-CN.json` | 修改 | 添加产品空状态翻译 |
| `oc-platform-web/src/locales/en-US.json` | 修改 | 添加产品空状态翻译 |
| `sql/init.sql` | 检查/修改 | 更新数据库默认配置（如需要） |

## 风险评估

- **低风险**：所有修改都是小范围的文本和逻辑调整
- **无破坏性变更**：不影响现有功能
- **向后兼容**：不影响已有的用户自定义配置

## 预计工作量

- 代码修改：约 15 分钟
- 测试验证：约 10 分钟
- 总计：约 25 分钟
