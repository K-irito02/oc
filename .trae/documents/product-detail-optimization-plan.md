# 产品详情页优化计划

## 问题概述

用户发现了产品详情页的三个问题：
1. 产品信息（下载量、评分、浏览量、更新时间）仍使用模拟数据
2. 浏览器标签页图标未使用系统设置中的全局 Logo
3. "Featured" 标签不支持中英文切换

## 问题分析

### 问题 1：模拟数据问题

**文件位置**: `e:\oc\oc-platform\oc-platform-web\src\pages\ProductDetail\index.tsx`

**现状分析**:
- 第 197-246 行定义了 `MOCK_PRODUCT` 和 `MOCK_VERSIONS` 模拟数据
- 第 452-457 行的 `applyMockData` 函数会在 API 失败时应用模拟数据
- 第 489-496 行的 `loadProduct` 函数在 API 失败或产品不存在时调用 `applyMockData`

**解决方案**:
1. 删除 `MOCK_PRODUCT` 和 `MOCK_VERSIONS` 常量定义
2. 删除 `applyMockData` 函数
3. 修改 `loadProduct` 函数，移除模拟数据逻辑，让页面在没有数据时显示空状态

### 问题 2：浏览器标签页图标问题

**文件位置**: 
- `e:\oc\oc-platform\oc-platform-web\index.html` (第 5 行)
- 需要在 `App.tsx` 中添加动态设置 favicon 的逻辑

**现状分析**:
- `index.html` 第 5 行硬编码使用 `/vite.svg` 作为 favicon
- 已有 `SiteLogo.tsx` 组件从 Redux `siteConfig` 获取 `siteLogo`
- 系统设置页面已支持上传和配置 Logo
- `siteConfigSlice.ts` 已定义 `siteLogo` 字段

**解决方案**:
1. 创建 `useFavicon` Hook，监听 `siteConfig.siteLogo` 变化
2. 动态更新 `<link rel="icon">` 的 href 属性
3. 在 `App.tsx` 中调用该 Hook
4. 保留 `/vite.svg` 作为默认 fallback

### 问题 3：Featured 标签国际化问题

**文件位置**: 
- `e:\oc\oc-platform\oc-platform-web\src\pages\ProductDetail\index.tsx` (第 635 行)
- `e:\oc\oc-platform\oc-platform-web\src\pages\Products\index.tsx` (第 166 行)

**现状分析**:
- `ProductDetail/index.tsx` 第 635 行硬编码显示 "Featured" 文本
- `Products/index.tsx` 第 166 行硬编码显示 "Featured" 文本
- `Home/index.tsx` 第 148 行已正确使用 `{t('home.featured')}`
- 国际化文件已有翻译键：
  - 中文：`home.featured` = "精选", `productDetail.featured` = "精选"
  - 英文：`home.featured` = "Featured", `productDetail.featured` = "Featured"

**解决方案**:
1. `ProductDetail/index.tsx` 第 635 行：将 `Featured` 替换为 `{t('productDetail.featured')}`
2. `Products/index.tsx` 第 166 行：将 `Featured` 替换为 `{t('home.featured')}`

## 实施步骤

### 步骤 1：删除模拟数据
**文件**: `src/pages/ProductDetail/index.tsx`

**操作**:
1. 删除 `MOCK_PRODUCT` 常量（约第 197-239 行）
2. 删除 `MOCK_VERSIONS` 常量（约第 241-246 行）
3. 删除 `applyMockData` 函数（约第 452-457 行）
4. 修改 `loadProduct` 函数，移除模拟数据相关逻辑：
   - 删除 `applyMockData` 依赖
   - 删除 `slug === 'mock-product' || slug === 'oc-creator-ultimate'` 的判断分支
   - API 失败时直接设置空状态

### 步骤 2：创建动态 Favicon Hook
**文件**: 新建 `src/hooks/useFavicon.ts`

**实现逻辑**:
```typescript
import { useEffect } from 'react';
import { useAppSelector } from '@/store/hooks';

export const useFavicon = () => {
  const { config } = useAppSelector((state) => state.siteConfig);
  
  useEffect(() => {
    const faviconUrl = config.siteLogo;
    if (!faviconUrl) return;
    
    let link: HTMLLinkElement = document.querySelector("link[rel~='icon']");
    if (!link) {
      link = document.createElement('link');
      link.rel = 'icon';
      document.head.appendChild(link);
    }
    link.href = faviconUrl;
  }, [config.siteLogo]);
};
```

### 步骤 3：在 App.tsx 中使用 Favicon Hook
**文件**: `src/App.tsx`

**操作**:
1. 导入 `useFavicon` Hook
2. 在 `App` 组件中调用 `useFavicon()`

### 步骤 4：修复 Featured 标签国际化
**文件 1**: `src/pages/ProductDetail/index.tsx`
- 第 635 行：`<Tag color="gold"...>Featured</Tag>` 
- 改为：`<Tag color="gold"...>{t('productDetail.featured')}</Tag>`

**文件 2**: `src/pages/Products/index.tsx`
- 第 166 行：`<Tag color="gold"...>Featured</Tag>`
- 改为：`<Tag color="gold"...>{t('home.featured')}</Tag>`

## 文件修改清单

| 文件路径 | 修改类型 | 修改内容 |
|---------|---------|---------|
| `src/pages/ProductDetail/index.tsx` | 修改 | 删除模拟数据、修复国际化 |
| `src/pages/Products/index.tsx` | 修改 | 修复国际化 |
| `src/hooks/useFavicon.ts` | 新建 | 创建动态 favicon Hook |
| `src/App.tsx` | 修改 | 引入 useFavicon Hook |

## 预期结果

1. 产品详情页不再显示模拟数据，无数据时显示空状态
2. 浏览器标签页图标使用系统设置中配置的 Logo，无配置时使用默认图标
3. "精选/Featured" 标签在所有页面支持中英文切换
