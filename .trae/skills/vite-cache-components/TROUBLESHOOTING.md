# Vite 缓存组件与 PPR 故障排除

本文件提供 Vite 缓存组件与部分预渲染 (PPR) 功能的故障排除指南，帮助您解决常见问题。

## 1. 缓存组件问题

### 1.1 缓存不生效

**症状：**
- 组件每次都重新渲染，没有使用缓存
- 数据每次都重新获取，没有从缓存读取

**可能原因：**
1. **缓存键冲突**：多个组件使用相同的缓存键
2. **缓存过期时间过短**：ttl 设置过小，导致缓存频繁过期
3. **localStorage 不可用**：浏览器隐私模式或存储空间不足
4. **缓存数据过大**：超过 localStorage 存储限制
5. **组件依赖项变化**：useEffect 依赖项导致组件频繁重渲染

**解决方案：**
- 确保缓存键唯一，包含组件名称和相关参数
- 合理设置 ttl，根据数据更新频率调整
- 添加 localStorage 可用性检查
- 压缩或拆分大型缓存数据
- 优化组件依赖项，避免不必要的重渲染

**代码示例：**

```typescript
// 正确的缓存键设计
const cacheKey = `user-${userId}-profile`

// localStorage 可用性检查
const isLocalStorageAvailable = () => {
  try {
    const test = 'test'
    localStorage.setItem(test, test)
    localStorage.removeItem(test)
    return true
  } catch (e) {
    return false
  }
}

// 使用时检查
if (isLocalStorageAvailable()) {
  // 使用缓存
} else {
  // 降级方案
}
```

### 1.2 缓存数据不一致

**症状：**
- 显示的数据与服务器数据不一致
- 缓存更新不及时

**可能原因：**
1. **缓存过期时间过长**：数据更新后缓存未失效
2. **缓存失效机制未触发**：数据更新时没有调用 invalidate
3. **staleWhileRevalidate 模式下的延迟更新**：旧数据显示时间过长

**解决方案：**
- 根据数据更新频率调整 ttl
- 在数据更新后手动调用 cache.invalidate()
- 对于重要数据，使用较短的 ttl 或禁用 staleWhileRevalidate
- 实现缓存版本控制，确保数据一致性

**代码示例：**

```typescript
// 数据更新后失效缓存
const updateUser = async (userData) => {
  const response = await fetch('/api/user', {
    method: 'PUT',
    body: JSON.stringify(userData)
  })
  const updatedUser = await response.json()
  
  // 失效缓存
  cache.invalidate(`user-${userId}-profile`)
  
  return updatedUser
}

// 缓存版本控制
const cacheVersion = 'v1'
const cacheKey = `${cacheVersion}-user-${userId}-profile`

// 当数据结构变更时，更新版本号
// const cacheVersion = 'v2'
```

### 1.3 缓存性能问题

**症状：**
- 缓存读取速度慢
- 内存占用过高
- 构建时间增加

**可能原因：**
1. **缓存数据过大**：存储了不必要的数据
2. **缓存操作频繁**：每次渲染都读写缓存
3. **缓存键设计不合理**：导致缓存碎片

**解决方案：**
- 只缓存必要的数据，避免存储整个组件状态
- 使用 useMemo 或 useCallback 优化缓存操作
- 合理设计缓存键，避免过多的缓存条目
- 实现缓存清理机制，定期清理过期缓存

**代码示例：**

```typescript
// 只缓存必要数据
const userData = {
  id: user.id,
  name: user.name,
  email: user.email
  // 避免缓存大对象如 user.orders
}

// 使用 useMemo 优化缓存操作
const cachedData = useMemo(() => {
  const data = cache.get(cacheKey)
  return data || fetchData()
}, [cacheKey])

// 定期清理过期缓存
const cleanupCache = () => {
  for (let i = 0; i < localStorage.length; i++) {
    const key = localStorage.key(i)
    if (key) {
      const item = JSON.parse(localStorage.getItem(key) || '{}')
      if (Date.now() - item.timestamp > item.ttl) {
        localStorage.removeItem(key)
      }
    }
  }
}

// 定期执行清理
useEffect(() => {
  const interval = setInterval(cleanupCache, 60 * 60 * 1000) // 每小时清理一次
  return () => clearInterval(interval)
}, [])
```

## 2. 部分预渲染问题

### 2.1 预渲染失败

**症状：**
- 构建过程中预渲染失败
- 生成的 HTML 文件为空或不完整

**可能原因：**
1. **页面依赖客户端 API**：使用了 window、document 等客户端特定 API
2. **数据获取失败**：预渲染时 API 不可用
3. **路由配置错误**：预渲染路由不存在或格式错误
4. **组件导出错误**：页面组件没有正确导出

**解决方案：**
- 使用条件渲染，在预渲染时避免使用客户端 API
- 确保 API 在预渲染时可访问，或使用模拟数据
- 检查 routes 配置，确保包含所有需要预渲染的路由
- 确保页面组件正确导出为 default 或命名导出

**代码示例：**

```typescript
// 条件渲染客户端 API
import { useEffect, useState } from 'react'

export function Page() {
  const [isClient, setIsClient] = useState(false)
  const [windowWidth, setWindowWidth] = useState(0)

  useEffect(() => {
    setIsClient(true)
    setWindowWidth(window.innerWidth)
  }, [])

  return (
    <div>
      {/* 静态部分 - 会被预渲染 */}
      <h1>Hello World</h1>
      
      {/* 客户端部分 - 只在客户端渲染 */}
      {isClient && (
        <p>Window width: {windowWidth}</p>
      )}
    </div>
  )
}

// 使用模拟数据进行预渲染
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  renderPage: async () => {
    try {
      // 尝试从 API 获取数据
      const data = await fetch('http://localhost:8081/api/data').then(res => res.json())
      return {
        pageContext: {
          staticData: { data }
        }
      }
    } catch (error) {
      // 使用模拟数据
      console.warn('API unavailable during prerender, using mock data')
      return {
        pageContext: {
          staticData: { 
            data: { message: 'Mock data for prerender' } 
          }
        }
      }
    }
  }
}
```

### 2.2 预渲染后页面空白

**症状：**
- 预渲染生成了 HTML 文件，但浏览器打开后显示空白
- 控制台有 JavaScript 错误

**可能原因：**
1. **客户端水合失败**：预渲染的 HTML 与客户端渲染的内容不匹配
2. **客户端代码错误**：客户端 JavaScript 执行失败
3. **路由不匹配**：客户端路由与预渲染路由不一致

**解决方案：**
- 确保预渲染的 HTML 与客户端渲染的内容完全匹配
- 检查客户端代码是否有错误，特别是在 useEffect 中
- 确保客户端路由配置与预渲染路由一致
- 使用 `vite-plugin-ssr` 的调试模式查看详细错误

**代码示例：**

```typescript
// 确保预渲染和客户端渲染内容一致
import { useState, useEffect } from 'react'

export function Page({ pageContext }: { pageContext: any }) {
  // 使用预渲染的数据作为初始状态
  const [data, setData] = useState(pageContext.staticData?.data || null)

  useEffect(() => {
    // 客户端数据获取
    if (!data) {
      fetch('/api/data')
        .then(res => res.json())
        .then(setData)
    }
  }, [data])

  // 确保渲染逻辑一致
  return (
    <div>
      <h1>{data ? data.title : 'Loading...'}</h1>
      {data && <p>{data.content}</p>}
    </div>
  )
}

// 调试模式配置
// vite.config.ts
export default defineConfig({
  plugins: [
    react(),
    ssr({
      dev: {
        debug: true // 启用调试模式
      }
    })
  ]
})
```

### 2.3 预渲染构建时间过长

**症状：**
- 预渲染过程耗时过长
- 构建过程卡住或超时

**可能原因：**
1. **预渲染路由过多**：需要预渲染的页面数量太多
2. **数据获取时间过长**：每个页面的 data fetch 耗时较长
3. **并行预渲染数量不足**：parallel 配置过低
4. **页面渲染复杂**：页面组件渲染过程复杂

**解决方案：**
- 只预渲染重要的页面，如首页、产品列表页等
- 优化数据获取，减少 API 请求时间
- 增加 parallel 配置，提高并行预渲染数量
- 简化页面渲染逻辑，减少渲染时间

**代码示例：**

```typescript
// 只预渲染重要路由
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  routes: () => [
    '/', // 首页
    '/about', // 关于页
    '/products' // 产品列表页
    // 避免预渲染所有产品详情页
  ]
}

// 优化数据获取
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  renderPage: async () => {
    // 并行获取数据
    const [products, categories] = await Promise.all([
      fetch('http://localhost:8081/api/products').then(res => res.json()),
      fetch('http://localhost:8081/api/categories').then(res => res.json())
    ])
    
    return {
      pageContext: {
        staticData: { products, categories }
      }
    }
  }
}

// 增加并行预渲染数量
// vite.config.ts
export default defineConfig({
  plugins: [
    react(),
    ssr({
      prerender: {
        parallel: 8 // 增加并行数量
      }
    })
  ]
})
```

## 3. 集成问题

### 3.1 与其他库的冲突

**症状：**
- 与 Redux、React Query 等状态管理库冲突
- 与路由库（如 React Router）冲突
- 与 UI 库（如 Ant Design）冲突

**可能原因：**
1. **状态管理冲突**：多个库同时管理相同的数据
2. **路由配置冲突**：路由库与预渲染路由不一致
3. **客户端特定 API 使用**：UI 库在预渲染时使用客户端 API

**解决方案：**
- 协调状态管理，避免重复缓存
- 确保路由配置与预渲染路由一致
- 为 UI 库添加条件渲染，避免在预渲染时使用客户端 API
- 使用适配器模式整合不同库

**代码示例：**

```typescript
// 与 React Query 集成
import { useQuery } from 'react-query'
import { cache } from './utils/cache'

export function useCachedQuery<T>(
  queryKey: string[],
  queryFn: () => Promise<T>,
  options?: any
) {
  const cacheKey = queryKey.join('-')
  
  return useQuery<T>(queryKey, async () => {
    // 检查缓存
    const cachedData = cache.get<T>(cacheKey)
    if (cachedData) {
      return cachedData
    }
    
    // 获取新数据
    const data = await queryFn()
    
    // 更新缓存
    cache.set(cacheKey, data, options?.cacheTime || 60000)
    
    return data
  }, {
    ...options,
    staleTime: options?.staleTime || 60000
  })
}

// 与 React Router 集成
import { useRoutes, RouteObject } from 'react-router-dom'
import { Page as HomePage } from './pages/HomePage'
import { Page as AboutPage } from './pages/AboutPage'

const routes: RouteObject[] = [
  { path: '/', element: <HomePage /> },
  { path: '/about', element: <AboutPage /> }
]

export function App() {
  const element = useRoutes(routes)
  return element
}

// 确保路由与预渲染一致
// prerender.ts
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  routes: () => ['/', '/about'] // 与 React Router 配置一致
}
```

### 3.2 部署问题

**症状：**
- 部署后预渲染页面不显示
- 缓存在生产环境不生效
- 路由在生产环境不匹配

**可能原因：**
1. **构建配置错误**：生产构建时预渲染未启用
2. **静态文件服务配置错误**：服务器未正确服务预渲染的 HTML 文件
3. **环境变量配置错误**：生产环境的 API 地址与预渲染时不一致

**解决方案：**
- 确保生产构建时启用预渲染
- 配置服务器正确服务静态文件和预渲染的 HTML 文件
- 使用环境变量管理 API 地址，确保预渲染和生产环境一致
- 测试部署流程，确保所有功能正常

**代码示例：**

```bash
# 确保生产构建时启用预渲染
# package.json
{
  "scripts": {
    "build": "vite build && vite-plugin-ssr prerender"
  }
}

# Nginx 配置示例
server {
  listen 80;
  server_name example.com;
  
  root /path/to/build;
  
  location / {
    try_files $uri $uri/ /index.html;
  }
  
  # 服务预渲染的 HTML 文件
  location /about {
    try_files $uri $uri/ /about.html /index.html;
  }
}

# 环境变量配置
# .env
VITE_API_URL=http://localhost:8081/api

# .env.production
VITE_API_URL=https://api.example.com/api
```

### 3.3 性能监控

**症状：**
- 缓存命中率低
- 预渲染页面加载缓慢
- 客户端渲染性能差

**可能原因：**
1. **缓存策略不当**：缓存键设计不合理或过期时间设置不当
2. **预渲染优化不足**：预渲染的内容过多或过少
3. **客户端代码优化不足**：客户端渲染逻辑复杂

**解决方案：**
- 实施缓存监控，跟踪缓存命中率和失效情况
- 使用 Lighthouse 分析页面性能，优化预渲染内容
- 优化客户端代码，减少渲染时间和资源使用
- 实施 A/B 测试，比较不同缓存和预渲染策略的效果

**代码示例：**

```typescript
// 缓存监控
const cacheMonitor = {
  hits: 0,
  misses: 0,
  
  get hitRate() {
    const total = this.hits + this.misses
    return total > 0 ? (this.hits / total) * 100 : 0
  },
  
  recordHit() {
    this.hits++
    this.logStats()
  },
  
  recordMiss() {
    this.misses++
    this.logStats()
  },
  
  logStats() {
    console.log(`Cache stats: ${this.hitRate.toFixed(2)}% hit rate`)
    // 可以将统计数据发送到监控服务
  }
}

// 增强的缓存工具
const enhancedCache = {
  get: <T>(key: string): T | null => {
    const data = cache.get<T>(key)
    if (data) {
      cacheMonitor.recordHit()
    } else {
      cacheMonitor.recordMiss()
    }
    return data
  },
  
  // 其他方法...
}

// 性能监控
import { useEffect } from 'react'

export function PerformanceMonitor() {
  useEffect(() => {
    // 监控首屏加载时间
    const navigationStart = performance.now()
    
    window.addEventListener('load', () => {
      const loadTime = performance.now() - navigationStart
      console.log(`Page load time: ${loadTime.toFixed(2)}ms`)
      // 可以将数据发送到监控服务
    })
  }, [])

  return null
}

// 在 App 组件中使用
function App() {
  return (
    <>
      <PerformanceMonitor />
      {/* 其他组件 */}
    </>
  )
}
```

## 4. 最佳实践

### 4.1 缓存策略

1. **分层缓存**：根据数据类型和更新频率使用不同的缓存策略
2. **缓存键设计**：使用包含组件名称、参数和版本号的唯一键
3. **缓存大小限制**：避免存储过大的数据，定期清理过期缓存
4. **错误处理**：添加缓存错误处理和降级方案
5. **监控和分析**：实施缓存监控，优化缓存策略

### 4.2 预渲染策略

1. **选择性预渲染**：只预渲染重要的页面，避免过度预渲染
2. **数据预获取**：在预渲染时获取必要的数据，减少客户端请求
3. **条件渲染**：避免在预渲染时使用客户端 API
4. **构建优化**：优化预渲染构建过程，减少构建时间
5. **测试验证**：测试预渲染结果，确保页面正确显示

### 4.3 性能优化

1. **代码分割**：使用动态导入和代码分割减少初始加载时间
2. **资源优化**：优化图片、CSS 和 JavaScript 资源
3. **网络优化**：使用 CDN、缓存头和 HTTP/2
4. **渲染优化**：减少重渲染，使用虚拟列表等技术
5. **监控和分析**：使用 Lighthouse、Web Vitals 等工具分析性能

## 5. 常见问题解答

### Q: 缓存组件与 React Query 等库如何配合使用？

**A:** 可以使用适配器模式整合不同库，例如：
- 使用 React Query 的 `staleTime` 和 `cacheTime` 配置
- 在 React Query 的 `onSuccess` 回调中更新本地缓存
- 使用 `useCachedQuery` 等自定义 Hook 整合两者功能

### Q: 如何处理用户特定的数据缓存？

**A:** 可以：
- 在缓存键中包含用户 ID
- 使用 sessionStorage 存储会话特定的缓存
- 实现用户登出时的缓存清理
- 为不同用户使用不同的缓存命名空间

### Q: 预渲染时如何处理需要用户认证的页面？

**A:** 可以：
- 只预渲染公共部分，认证部分留给客户端处理
- 使用条件渲染，在预渲染时显示登录提示
- 实现服务器端认证，在预渲染时获取用户信息
- 对于需要认证的页面，考虑使用客户端渲染

### Q: 如何处理动态路由的预渲染？

**A:** 可以：
- 在 `prerender.routes` 中返回动态生成的路由列表
- 使用 `prerender.renderPage` 为每个动态路由获取数据
- 对于大量动态路由，考虑使用增量静态再生 (ISR) 模式
- 结合缓存策略，减少预渲染的复杂度

### Q: 缓存和预渲染如何影响 SEO？

**A:** 合理使用可以提升 SEO：
- 预渲染可以让搜索引擎更快地索引页面内容
- 缓存可以提高页面加载速度，改善用户体验
- 确保预渲染的内容包含重要的 SEO 元素
- 避免使用客户端渲染的内容作为主要 SEO 内容

## 6. 总结

Vite 缓存组件与部分预渲染是提高 React 应用性能的有效手段，但需要正确配置和使用。通过本故障排除指南，您应该能够解决常见问题，并优化您的应用性能。

**关键要点：**
- 合理设计缓存策略，避免缓存不一致
- 选择性预渲染，优化构建时间
- 处理客户端 API 依赖，确保预渲染成功
- 监控和分析性能，持续优化
- 与其他库和工具良好集成

如果您遇到本指南未覆盖的问题，请参考相关文档或寻求社区支持。