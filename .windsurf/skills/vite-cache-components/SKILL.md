---
name: vite-cache-components
description: 为使用 Vite 构建的 React 项目提供缓存组件和部分预渲染 (Partial Prerendering, PPR) 功能的实现方案
---

# Vite 缓存组件与部分预渲染 (PPR) 技能

## 技能描述

本技能为使用 Vite 构建的 React 项目提供缓存组件和部分预渲染 (Partial Prerendering, PPR) 功能的实现方案。通过本技能，您可以：

- 在 Vite React 项目中实现类似 Next.js 的缓存组件功能
- 配置和使用部分预渲染以提高首屏加载性能
- 优化组件的缓存策略和数据获取

## 适用场景

- 需要提高 Vite React 项目性能的场景
- 希望在非 Next.js 项目中实现类似 Next.js 缓存功能的场景
- 需要优化首屏加载速度和用户体验的场景

## 核心功能

1. **缓存组件实现**：提供基于 React 组件的缓存机制
2. **部分预渲染**：在构建时预渲染部分页面内容
3. **缓存策略配置**：支持不同级别的缓存策略
4. **数据获取优化**：优化数据获取和缓存逻辑

## 技术栈要求

- Vite 5.0+
- React 18.0+
- TypeScript (推荐)

## 快速开始

### 安装依赖

```bash
npm install vite-plugin-ssr react-query
```

### 配置 Vite

在 `vite.config.ts` 中添加插件配置：

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ssr from 'vite-plugin-ssr/plugin'

export default defineConfig({
  plugins: [react(), ssr()]
})
```

### 实现缓存组件

创建缓存组件的基础结构：

```typescript
// src/components/CacheComponent.tsx
import { useState, useEffect } from 'react'

export function CacheComponent<T>({
  children,
  key,
  ttl = 60 * 1000, // 1分钟缓存
}: {
  children: () => React.ReactNode
  key: string
  ttl?: number
}) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const cachedData = localStorage.getItem(key)
    if (cachedData) {
      const { value, timestamp } = JSON.parse(cachedData)
      if (Date.now() - timestamp < ttl) {
        setData(value)
        setLoading(false)
        return
      }
    }

    // 缓存过期或不存在，执行children函数获取新数据
    const result = children()
    setData(result as T)
    setLoading(false)

    // 缓存新数据
    localStorage.setItem(key, JSON.stringify({
      value: result,
      timestamp: Date.now()
    }))
  }, [key, ttl])

  if (loading) {
    return <div>Loading...</div>
  }

  return <>{children()}</>
}
```

### 实现部分预渲染

使用 `vite-plugin-ssr` 实现部分预渲染：

```typescript
// pages/index.page.tsx
export { Page } from './Page'

// pages/Page.tsx
import { useState, useEffect } from 'react'

export function Page() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 客户端数据获取
    fetch('/api/data')
      .then(res => res.json())
      .then(data => {
        setData(data)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      {/* 静态部分 - 会被预渲染 */}
      <h1>Hello Vite SSR</h1>
      
      {/* 动态部分 - 客户端渲染 */}
      {loading ? (
        <p>Loading data...</p>
      ) : (
        <p>Data: {JSON.stringify(data)}</p>
      )}
    </div>
  )
}
```

## 配置选项

### 缓存组件配置

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `key` | string | 必需 | 缓存键名 |
| `ttl` | number | 60000 | 缓存过期时间（毫秒） |
| `staleWhileRevalidate` | boolean | false | 是否在缓存过期后继续使用旧数据同时刷新 |

### 部分预渲染配置

在 `vite.config.ts` 中配置：

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ssr from 'vite-plugin-ssr/plugin'

export default defineConfig({
  plugins: [
    react(),
    ssr({
      prerender: {
        enabled: true,
        partial: true,
        routes: ['/']
      }
    })
  ]
})
```

## 最佳实践

1. **合理使用缓存**：对于不经常变化的数据使用较长的缓存时间
2. **缓存键设计**：使用包含组件名称和相关参数的唯一键
3. **预渲染策略**：只预渲染静态内容，动态内容留给客户端处理
4. **错误处理**：添加缓存错误处理和回退机制

## 故障排除

- **缓存不生效**：检查缓存键是否唯一，以及 localStorage 是否可用
- **预渲染失败**：确保页面组件正确导出，并且没有依赖客户端特定的 API
- **性能问题**：避免在缓存组件中执行复杂的计算或网络请求

## 示例项目

查看 `examples` 目录获取完整的示例代码。