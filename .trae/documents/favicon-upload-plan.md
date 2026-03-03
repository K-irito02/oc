# 浏览器标签页 Favicon Logo 设置功能计划

## 需求概述
在系统设置中添加一个专门设置浏览器标签页 Logo 图标显示的功能，支持裁剪、旋转、鼠标滚动放大/缩小、按钮点击放大/缩小等辅助功能。

## 现有代码分析

### 前端现有组件
- `LogoCropUploader.tsx` - 已支持裁剪、旋转、缩放功能
- 已有 `siteLogo` 字段用于网站 Logo
- 国际化文件已包含 logo 相关翻译

### 后端现有配置
- `SystemConfig` 实体类
- `site.logo` 配置项

## 实施步骤

### 步骤 1：添加国际化翻译
**文件**: `src/locales/zh-CN.json` 和 `src/locales/en-US.json`

添加新的翻译键：
- `logo.faviconTitle` - 浏览器标签页图标
- `logo.faviconHint` - 上传提示
- `logo.faviconCropTitle` - 裁剪标题
- `logo.faviconConfirmCrop` - 确认裁剪
- `logo.faviconUploadSuccess` - 上传成功
- `logo.faviconUploadFailed` - 上传失败
- `logo.currentFavicon` - 当前图标

### 步骤 2：后端配置
**后端代码无需修改**，因为系统配置使用 key-value 形式，可以直接使用 `site.favicon` 作为新的配置键。

### 步骤 3：修改前端系统设置页面
**文件**: `src/pages/Admin/System/index.tsx`

1. 添加 `faviconUrl` state
2. 加载 `site.favicon` 配置
3. 添加新的 LogoCropUploader 组件用于上传 favicon
4. 添加保存处理函数

### 步骤 4：创建 FaviconLogo 上传组件
**文件**: 可以复用现有的 `LogoCropUploader` 组件

修改组件支持不同用途（网站 Logo 和 Favicon），或者创建新的 `FaviconCropUploader` 组件。

### 步骤 5：修改 useFavicon Hook
**文件**: `src/hooks/useFavicon.ts`

修改为优先使用新的 `faviconLogo` 字段：
```typescript
const faviconUrl = config.faviconLogo || config.siteLogo;
```

### 步骤 6：更新 Redux Store
**文件**: `src/store/slices/siteConfigSlice.ts`

添加 `faviconLogo` 字段到 `SiteConfig` 接口。

## 文件修改清单

| 文件 | 修改内容 |
|-----|---------|
| `src/locales/zh-CN.json` | 添加 favicon 相关翻译 |
| `src/locales/en-US.json` | 添加 favicon 相关翻译 |
| `src/store/slices/siteConfigSlice.ts` | 添加 faviconLogo 字段 |
| `src/pages/Admin/System/index.tsx` | 添加 favicon 上传组件 |
| `src/hooks/useFavicon.ts` | 优先使用 faviconLogo |

## 预期效果
1. 系统设置页面增加"浏览器标签页图标"上传功能
2. 支持裁剪、旋转、缩放（滚轮/按钮）功能
3. 上传后立即显示在浏览器标签页
4. 中英文切换支持
