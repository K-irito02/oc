# Vite 缓存组件与 PPR API 参考

本文件提供 Vite 缓存组件与部分预渲染 (PPR) 功能的 API 参考文档。

## 1. 缓存组件 API

### 1.1 `CacheComponent` 组件

**类型定义：**

```typescript
import { ReactNode } from 'react'

type CacheComponentProps<T> = {
  children: () => T | ReactNode
  key: string
  ttl?: number
  staleWhileRevalidate?: boolean
}

export function CacheComponent<T>(props: CacheComponentProps<T>): ReactNode
```

**参数说明：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `children` | () => T  ReactNode | 必需 | 执行函数，返回需要缓存的数据或组件 |
| `key` | string | 必需 | 缓存键名，用于在 localStorage 中标识缓存 |
| `ttl` | number | 60000 | 缓存过期时间，单位毫秒 |
| `staleWhileRevalidate` | boolean | false | 是否在缓存过期后继续使用旧数据同时刷新 |

**返回值：**
- React 组件或数据

**使用示例：**

```typescript
import { CacheComponent } from './components/CacheComponent'

function MyComponent() {
  return (
    <CacheComponent key="user-data" ttl={300000}>
      {() => {
        // 这里可以执行数据获取或复杂计算
        return <div>User data</div>
      }}
    </CacheComponent>
  )
}
```

### 1.2 `useCachedData` Hook

**类型定义：**

```typescript
export function useCachedData<T>(
  fetchFn: () => Promise<T>,
  key: string,
  ttl?: number
): {
  data: T | null
  loading: boolean
  error: Error | null
}
```

**参数说明：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `fetchFn` | () => Promise<T> | 必需 | 数据获取函数，返回 Promise |
| `key` | string | 必需 | 缓存键名 |
| `ttl` | number | 60000 | 缓存过期时间，单位毫秒 |

**返回值：**

| 属性 | 类型 | 描述 |
|------|------|------|
| `data` | T  null | 缓存的数据或 null |
| `loading` | boolean | 是否正在加载数据 |
| `error` | Error  null | 错误信息或 null |

**使用示例：**

```typescript
import { useCachedData } from './hooks/useCachedData'

function MyComponent() {
  const fetchUser = async () => {
    const response = await fetch('/api/user')
    return response.json()
  }

  const { data: user, loading, error } = useCachedData(fetchUser, 'user-data', 300000)

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return <div>User: {user?.name}</div>
}
```

### 1.3 `cache` 工具函数

**类型定义：**

```typescript
interface Cache {
  set: <T>(key: string, value: T, ttl?: number) => void
  get: <T>(key: string) => T | null
  invalidate: (key: string) => void
  invalidatePattern: (pattern: RegExp) => void
}

export const cache: Cache
```

**方法说明：**

| 方法 | 描述 |
|------|------|
| `set(key, value, ttl)` | 设置缓存，key 为缓存键，value 为缓存值，ttl 为过期时间（默认 60000 毫秒） |
| `get(key)` | 获取缓存，返回缓存值或 null |
| `invalidate(key)` | 使指定缓存失效 |
| `invalidatePattern(pattern)` | 使匹配正则表达式的所有缓存失效 |

**使用示例：**

```typescript
import { cache } from './utils/cache'

// 设置缓存
cache.set('user-data', { name: 'John' }, 300000)

// 获取缓存
const user = cache.get<{ name: string }>('user-data')

// 使缓存失效
cache.invalidate('user-data')

// 使匹配模式的缓存失效
cache.invalidatePattern(/^user-/)
```

## 2. 部分预渲染 API

### 2.1 Vite 配置

**类型定义：**

```typescript
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ssr from 'vite-plugin-ssr/plugin'

export default defineConfig({
  plugins: [
    react(),
    ssr({
      prerender?: {
        enabled?: boolean
        partial?: boolean
        routes?: string[] | ((prerenderContext: PrerenderContext) => Promise<string[]>)
        parallel?: number
      }
    })
  ]
})
```

**配置选项：**

| 选项 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `enabled` | boolean | false | 是否启用预渲染 |
| `partial` | boolean | false | 是否启用部分预渲染 |
| `routes` | string[]  function | [] | 预渲染的路由列表或获取路由的函数 |
| `parallel` | number | 4 | 并行预渲染的数量 |

### 2.2 页面组件

**类型定义：**

```typescript
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }): ReactNode
```

**参数说明：**

| 参数 | 类型 | 描述 |
|------|------|------|
| `pageContext` | PageContext | 页面上下文，包含路由参数、静态数据等 |

**返回值：**
- React 组件

**使用示例：**

```typescript
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }) {
  const { id } = pageContext.routeParams
  const [data, setData] = useState(pageContext.staticData?.data || null)

  useEffect(() => {
    if (!data) {
      fetch(`/api/data/${id}`)
        .then(res => res.json())
        .then(setData)
    }
  }, [id, data])

  return <div>{data ? data.name : 'Loading...'}</div>
}
```

### 2.3 预渲染钩子

**类型定义：**

```typescript
import type { PrerenderHook, PrerenderContext, PageContext } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  routes?: (prerenderContext: PrerenderContext) => Promise<string[]>
  renderPage?: (pageContext: PageContext) => Promise<{
    pageContext: PageContext
  }>
}
```

**方法说明：**

| 方法 | 描述 |
|------|------|
| `routes(prerenderContext)` | 获取预渲染的路由列表，返回 Promise<string[]> |
| `renderPage(pageContext)` | 渲染页面，返回包含静态数据的 pageContext |

**使用示例：**

```typescript
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  routes: async () => {
    const products = await fetch('http://localhost:8081/api/products').then(res => res.json())
    return products.map((product: { id: string }) => `/product/${product.id}`)
  },
  
  renderPage: async (pageContext) => {
    const { id } = pageContext.routeParams
    const product = await fetch(`http://localhost:8081/api/products/${id}`).then(res => res.json())
    
    return {
      pageContext: {
        staticData: { product }
      }
    }
  }
}
```

## 3. 高级 API

### 3.1 `CachedPrerenderedComponent` 组件

**类型定义：**

```typescript
import { ReactNode } from 'react'
import type { PageContext } from 'vite-plugin-ssr'

type CachedPrerenderedComponentProps<T> = {
  children: (data: T) => ReactNode
  fetchFn: () => Promise<T>
  key: string
  ttl?: number
  staticData?: T
}

export function CachedPrerenderedComponent<T>(props: CachedPrerenderedComponentProps<T>): ReactNode
```

**参数说明：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `children` | (data: T) => ReactNode | 必需 | 渲染函数，接收数据并返回 React 组件 |
| `fetchFn` | () => Promise<T> | 必需 | 数据获取函数 |
| `key` | string | 必需 | 缓存键名 |
| `ttl` | number | 60000 | 缓存过期时间，单位毫秒 |
| `staticData` | T | undefined | 预渲染时的静态数据 |

**返回值：**
- React 组件

**使用示例：**

```typescript
import { CachedPrerenderedComponent } from './components/CachedPrerenderedComponent'
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }) {
  const fetchProducts = async () => {
    const response = await fetch('/api/products')
    return response.json()
  }

  return (
    <CachedPrerenderedComponent
      key="products-list"
      fetchFn={fetchProducts}
      staticData={pageContext.staticData?.products}
      ttl={300000}
    >
      {(products) => (
        <ul>
          {products.map((product: { id: string; name: string }) => (
            <li key={product.id}>{product.name}</li>
          ))}
        </ul>
      )}
    </CachedPrerenderedComponent>
  )
}
```

### 3.2 `useDebouncedCache` Hook

**类型定义：**

```typescript
export function useDebouncedCache<T>(
  fetchFn: () => Promise<T>,
  key: string,
  ttl?: number,
  debounceTime?: number
): {
  data: T | null
  loading: boolean
  error: Error | null
}
```

**参数说明：**

| 参数 | 类型 | 默认值 | 描述 |
|------|------|--------|------|
| `fetchFn` | () => Promise<T> | 必需 | 数据获取函数 |
| `key` | string | 必需 | 缓存键名 |
| `ttl` | number | 60000 | 缓存过期时间，单位毫秒 |
| `debounceTime` | number | 300 | 防抖时间，单位毫秒 |

**返回值：**

| 属性 | 类型 | 描述 |
|------|------|------|
| `data` | T  null | 缓存的数据或 null |
| `loading` | boolean | 是否正在加载数据 |
| `error` | Error  null | 错误信息或 null |

**使用示例：**

```typescript
import { useDebouncedCache } from './hooks/useDebouncedCache'

function SearchComponent({ query }: { query: string }) {
  const fetchSearchResults = async () => {
    const response = await fetch(`/api/search?q=${query}`)
    return response.json()
  }

  const { data: results, loading, error } = useDebouncedCache(
    fetchSearchResults,
    `search-${query}`,
    30000,
    500
  )

  if (loading) return <div>Searching...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div>
      {results?.map((result: { id: string; title: string }) => (
        <div key={result.id}>{result.title}</div>
      ))}
    </div>
  )
}
```

### 3.3 `batchCache` 工具函数

**类型定义：**

```typescript
interface BatchCache {
  set: <T>(items: Array<{ key: string; value: T; ttl?: number }>) => void
  get: <T>(keys: string[]) => Record<string, T | null>
}

export const batchCache: BatchCache
```

**方法说明：**

| 方法 | 描述 |
|------|------|
| `set(items)` | 批量设置缓存，items 为包含 key、value 和 ttl 的对象数组 |
| `get(keys)` | 批量获取缓存，返回包含键值对的对象 |

**使用示例：**

```typescript
import { batchCache } from './utils/batchCache'

// 批量设置缓存
batchCache.set([
  { key: 'user-1', value: { name: 'John' }, ttl: 300000 },
  { key: 'user-2', value: { name: 'Jane' }, ttl: 300000 }
])

// 批量获取缓存
const users = batchCache.get<{ name: string }>(['user-1', 'user-2'])
console.log(users['user-1']?.name) // John
```

## 4. 配置参考

### 4.1 Vite 插件配置

**vite-plugin-ssr 配置：**

```typescript
import ssr from 'vite-plugin-ssr/plugin'

export default defineConfig({
  plugins: [
    ssr({
      // 预渲染配置
      prerender: {
        enabled: true, // 启用预渲染
        partial: true, // 启用部分预渲染
        routes: ['/', '/about', '/contact'], // 预渲染的路由
        parallel: 4 // 并行预渲染数量
      },
      
      // 其他配置
      includeAssets: ['favicon.ico'], // 包含的静态资源
      baseUrl: '/', // 基础 URL
      trailingSlash: false // 是否添加末尾斜杠
    })
  ]
})
```

### 4.2 环境变量

| 环境变量 | 描述 | 默认值 |
|---------|------|--------|
| `VITE_SSR` | 是否启用 SSR | false |
| `VITE_PRERENDER` | 是否启用预渲染 | false |
| `VITE_PRERENDER_PARTIAL` | 是否启用部分预渲染 | false |
| `VITE_CACHE_TTL` | 默认缓存过期时间（毫秒） | 60000 |

**使用示例：**

```bash
# .env
VITE_SSR=true
VITE_PRERENDER=true
VITE_PRERENDER_PARTIAL=true
VITE_CACHE_TTL=300000
```

## 5. 错误处理

### 5.1 缓存错误

**常见错误：**

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| `QuotaExceededError` | localStorage 存储容量不足 | 减少缓存数据大小或使用 sessionStorage |
| 缓存不生效 | 缓存键冲突或过期时间设置过短 | 确保缓存键唯一，合理设置过期时间 |
| 数据不一致 | 缓存更新不及时 | 使用 `staleWhileRevalidate` 或手动失效缓存 |

### 5.2 预渲染错误

**常见错误：**

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 预渲染失败 | 页面依赖客户端 API | 条件渲染，在预渲染时避免使用客户端 API |
| 路由未预渲染 | 路由配置错误 | 检查 `routes` 配置，确保包含所有需要预渲染的路由 |
| 数据获取失败 | 预渲染时 API 不可用 | 确保 API 在预渲染时可访问，或使用模拟数据 |

## 6. 性能指标

### 6.1 缓存性能

| 指标 | 目标值 | 测量方法 |
|------|--------|----------|
| 缓存命中率 | > 80% | 统计缓存命中次数 / 总请求次数 |
| 缓存大小 | < 5MB | 检查 localStorage 使用情况 |
| 缓存读取时间 | < 10ms | 测量 localStorage 读取操作时间 |

### 6.2 预渲染性能

| 指标 | 目标值 | 测量方法 |
|------|--------|----------|
| 首屏加载时间 | < 1s | 使用 Lighthouse 测量 |
| 首次内容绘制 | < 0.5s | 使用 Lighthouse 测量 |
| 预渲染构建时间 | < 2min | 测量构建命令执行时间 |

## 7. 浏览器兼容性

| 特性 | Chrome | Firefox | Safari | Edge |
|------|--------|---------|--------|------|
| localStorage | ✅ | ✅ | ✅ | ✅ |
| Vite SSR | ✅ | ✅ | ✅ | ✅ |
| 部分预渲染 | ✅ | ✅ | ✅ | ✅ |
| React 18 | ✅ | ✅ | ✅ | ✅ |

**注意：**
- localStorage 在隐私模式下可能不可用或容量有限
- 部分预渲染需要现代浏览器支持 ES6+ 特性