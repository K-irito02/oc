# 多功能改进实施计划

## 概述

本计划涵盖以下四个改进任务：
1. CloudflareTurnstile 人机验证卡片深色主题切换支持
2. 社交链接配置的条件显示逻辑完善
3. GitHub 链接配置
4. 备案信息样式统一

---

## 任务一：CloudflareTurnstile 深色主题切换

### 现状分析

- **组件支持**：CloudflareTurnstile 组件已支持 `theme` 属性，可选值：`'light' | 'dark' | 'auto'`
- **当前实现**：所有页面都硬编码使用 `theme="auto"`
- **问题**：`auto` 模式跟随浏览器/系统主题，而非网站自定义主题设置

### 解决方案

修改 CloudflareTurnstile 组件，使其根据网站当前主题动态切换：
- 从 Redux `themeSlice` 获取 `currentTheme.appearance.mode`
- 当 mode 为 `'system'` 时，检测系统偏好
- 当 mode 为 `'light'` 或 `'dark'` 时，使用对应主题

### 涉及文件

| 文件 | 修改内容 |
|------|----------|
| `src/components/CloudflareTurnstile/index.tsx` | 添加主题检测逻辑，支持动态主题切换 |
| `src/pages/Login/index.tsx` | 移除硬编码 `theme="auto"`，使用组件默认行为 |
| `src/pages/Register/index.tsx` | 同上 |
| `src/pages/ForgotPassword/index.tsx` | 同上 |
| `src/pages/Profile/index.tsx` | 同上 |
| `src/components/home/FeedbackSection.tsx` | 同上 |

### 实施步骤

1. 修改 `CloudflareTurnstile/index.tsx`：
   - 引入 `useAppSelector` 获取主题状态
   - 添加 `useMemo` 计算实际主题值
   - 将计算后的主题传递给 Turnstile SDK

2. 更新所有使用 CloudflareTurnstile 的页面：
   - 移除 `theme="auto"` 属性（使用组件内部的主题检测）

---

## 任务二：社交链接配置条件显示

### 现状分析

**已配置项**：
- `site.url` - 官网地址
- `social.github` - GitHub
- `social.twitter` - Twitter/X
- `social.linkedin` - LinkedIn
- `social.weibo` - 微博
- `social.wechat` - 微信公众号
- `social.email` - 联系邮箱

**当前问题**：
1. **Footer 组件**：只显示 github, twitter, linkedin, email，**缺少 weibo 和 wechat**
2. **邮件模板**：只有"访问官网"按钮，没有社交链接显示
3. **条件显示逻辑**：Footer 中当所有社交链接为空时显示占位图标（不符合"不显示"的要求）

### 解决方案

#### 2.1 前端 Footer 组件

1. 添加微博和微信公众号显示
2. 移除占位图标逻辑，完全按配置显示
3. 微信公众号显示为二维码图标或文字提示

#### 2.2 邮件模板

1. 在邮件底部添加社交链接区域
2. 仅当有配置时显示对应图标链接

### 涉及文件

| 文件 | 修改内容 |
|------|----------|
| `src/components/layout/Footer.tsx` | 添加微博、微信显示，移除占位图标 |
| `src/store/slices/siteConfigSlice.ts` | 确认字段完整性 |
| `EmailTemplateService.java` | 添加社交链接区域 |
| `EmailConfigService.java` | 添加社交链接配置获取 |

### 实施步骤

1. **修改 Footer.tsx**：
   - 添加微博图标和链接
   - 添加微信公众号显示（可显示二维码弹窗或跳转链接）
   - 移除 `!socialLinks.github && !socialLinks.twitter...` 的占位逻辑

2. **修改邮件模板**：
   - 在 `EmailConfigService.java` 中获取社交链接配置
   - 在 `EmailTemplateService.java` 中添加社交链接 HTML 区域
   - 仅当配置存在时渲染对应链接

---

## 任务三：GitHub 链接配置

### 用户提供的 GitHub 链接

```
https://github.com/K-irito02/oc-platform-app
```

### 解决方案

在数据库 `system_configs` 表中插入/更新配置：

```sql
INSERT INTO system_configs (config_key, config_value, description) 
VALUES ('social.github', 'https://github.com/K-irito02/oc-platform-app', 'GitHub 链接')
ON CONFLICT (config_key) DO UPDATE SET config_value = 'https://github.com/K-irito02/oc-platform-app';
```

或通过管理后台系统设置页面配置。

---

## 任务四：备案信息样式统一

### 现状分析

**用户选中的两种样式对比**：

| 元素 | 当前样式 |
|------|----------|
| `<a>` 备案信息 | 卡片按钮样式：bg-white, shadow-sm, border, rounded-lg, hover 效果 |
| `<p>` 版权信息 | 简单文本样式：text-slate-500, text-sm |

**用户需求**：备案信息样式与版权信息一致（简单文本样式）

### 涉及文件

| 文件 | 修改内容 |
|------|----------|
| `src/components/layout/Footer.tsx` | 修改备案信息 `<a>` 标签样式 |
| `src/components/FilingInfo.tsx` | 修改备案信息 `<a>` 标签样式 |

### 实施步骤

1. **修改 Footer.tsx**：
   - 将备案信息 `<a>` 标签的样式改为：`text-slate-500 dark:text-slate-400 text-sm hover:text-slate-600 dark:hover:text-slate-300`
   - 移除卡片按钮相关样式

2. **修改 FilingInfo.tsx**：
   - 同样修改备案信息样式为简单文本样式

---

## 实施顺序

1. **任务四**：备案信息样式统一（简单修改）
2. **任务一**：CloudflareTurnstile 深色主题切换
3. **任务二**：社交链接配置条件显示
4. **任务三**：GitHub 链接配置（数据库操作）

---

## 验证清单

- [ ] CloudflareTurnstile 在深色模式下显示深色主题
- [ ] CloudflareTurnstile 在浅色模式下显示浅色主题
- [ ] CloudflareTurnstile 在系统模式下跟随系统主题
- [ ] Footer 中微博链接正确显示（配置后）
- [ ] Footer 中微信公众号正确显示（配置后）
- [ ] 无社交链接配置时不显示任何社交图标
- [ ] 邮件模板中有社交链接时显示对应链接
- [ ] 邮件模板中无社交链接时不显示社交区域
- [ ] Footer 中备案信息样式与版权信息一致
- [ ] FilingInfo 组件中备案信息样式与版权信息一致
- [ ] GitHub 链接配置正确保存并显示
