# Vite 缓存组件与 PPR 模式

本文件提供在 Vite React 项目中实现缓存组件和部分预渲染的最佳实践模式。

## 1. 缓存组件模式

### 1.1 基础缓存组件

```typescript
// src/components/CacheComponent.tsx
import { useState, useEffect } from 'react'

type CacheComponentProps<T> = {
  children: () => T
  key: string
  ttl?: number
  staleWhileRevalidate?: boolean
}

export function CacheComponent<T>({
  children,
  key,
  ttl = 60 * 1000,
  staleWhileRevalidate = false
}: CacheComponentProps<T>) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const loadData = async () => {
      const cachedData = localStorage.getItem(key)
      
      if (cachedData) {
        const { value, timestamp } = JSON.parse(cachedData)
        const isExpired = Date.now() - timestamp > ttl
        
        if (!isExpired) {
          setData(value)
          setLoading(false)
          return
        } else if (staleWhileRevalidate) {
          setData(value)
          setLoading(false)
        }
      }

      try {
        const result = children()
        setData(result)
        
        // 缓存新数据
        localStorage.setItem(key, JSON.stringify({
          value: result,
          timestamp: Date.now()
        }))
      } catch (error) {
        console.error('Cache component error:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [key, ttl, staleWhileRevalidate, children])

  if (loading && !data) {
    return <div>Loading...</div>
  }

  return <>{children()}</>
}
```

### 1.2 数据获取缓存模式

```typescript
// src/hooks/useCachedData.ts
import { useState, useEffect } from 'react'

export function useCachedData<T>(
  fetchFn: () => Promise<T>,
  key: string,
  ttl: number = 60 * 1000
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const loadData = async () => {
      try {
        // 检查缓存
        const cachedData = localStorage.getItem(key)
        if (cachedData) {
          const { value, timestamp } = JSON.parse(cachedData)
          if (Date.now() - timestamp < ttl) {
            setData(value)
            setLoading(false)
            return
          }
        }

        // 缓存过期或不存在，重新获取
        setLoading(true)
        const result = await fetchFn()
        setData(result)

        // 更新缓存
        localStorage.setItem(key, JSON.stringify({
          value: result,
          timestamp: Date.now()
        }))
      } catch (err) {
        setError(err as Error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [fetchFn, key, ttl])

  return { data, loading, error }
}
```

### 1.3 缓存失效模式

```typescript
// src/utils/cache.ts
export const cache = {
  set: <T>(key: string, value: T, ttl: number = 60 * 1000) => {
    const item = {
      value,
      timestamp: Date.now(),
      ttl
    }
    localStorage.setItem(key, JSON.stringify(item))
  },

  get: <T>(key: string): T | null => {
    const itemStr = localStorage.getItem(key)
    if (!itemStr) return null

    const item = JSON.parse(itemStr)
    if (Date.now() - item.timestamp > item.ttl) {
      localStorage.removeItem(key)
      return null
    }

    return item.value as T
  },

  invalidate: (key: string) => {
    localStorage.removeItem(key)
  },

  invalidatePattern: (pattern: RegExp) => {
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i)
      if (key && pattern.test(key)) {
        localStorage.removeItem(key)
      }
    }
  }
}
```

## 2. 部分预渲染模式

### 2.1 基础 PPR 页面

```typescript
// pages/index.page.tsx
export { Page } from './Page'
export { prerender } from './prerender'

// pages/Page.tsx
import { useState, useEffect } from 'react'

export function Page() {
  const [dynamicData, setDynamicData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 客户端数据获取
    fetch('/api/dynamic-data')
      .then(res => res.json())
      .then(data => {
        setDynamicData(data)
        setLoading(false)
      })
  }, [])

  return (
    <div>
      {/* 静态部分 - 会被预渲染 */}
      <h1>Welcome to My App</h1>
      <p>This content is prerendered at build time.</p>
      
      {/* 动态部分 - 客户端渲染 */}
      <div>
        {loading ? (
          <p>Loading dynamic data...</p>
        ) : (
          <p>Dynamic data: {JSON.stringify(dynamicData)}</p>
        )}
      </div>
    </div>
  )
}

// pages/prerender.ts
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  renderPage: async () => {
    // 预渲染时获取静态数据
    const staticData = await fetch('http://localhost:8081/api/static-data').then(res => res.json())
    
    return {
      pageContext: {
        staticData
      }
    }
  }
}
```

### 2.2 带数据的 PPR 页面

```typescript
// pages/product/[id].page.tsx
export { Page } from './Page'
export { prerender } from './prerender'

// pages/product/Page.tsx
import { useState, useEffect } from 'react'
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }) {
  const { id } = pageContext.routeParams
  const [product, setProduct] = useState(pageContext.staticData?.product || null)
  const [loading, setLoading] = useState(!pageContext.staticData?.product)

  useEffect(() => {
    if (!product) {
      // 客户端获取数据
      fetch(`/api/products/${id}`)
        .then(res => res.json())
        .then(data => {
          setProduct(data)
          setLoading(false)
        })
    }
  }, [id, product])

  if (loading) {
    return <div>Loading product...</div>
  }

  return (
    <div>
      {/* 静态部分 - 会被预渲染 */}
      <h1>{product?.name || 'Product'}</h1>
      
      {/* 动态部分 - 客户端渲染 */}
      <div>
        <p>Price: ${product?.price}</p>
        <p>Stock: {product?.stock}</p>
      </div>
    </div>
  )
}

// pages/product/prerender.ts
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  routes: async () => {
    // 获取所有产品ID用于预渲染
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

## 3. 高级模式

### 3.1 缓存与 PPR 结合

```typescript
// src/components/CachedPrerenderedComponent.tsx
import { useState, useEffect } from 'react'
import { cache } from '../utils/cache'

type CachedPrerenderedComponentProps<T> = {
  children: (data: T) => React.ReactNode
  fetchFn: () => Promise<T>
  key: string
  ttl?: number
  staticData?: T
}

export function CachedPrerenderedComponent<T>({
  children,
  fetchFn,
  key,
  ttl = 60 * 1000,
  staticData
}: CachedPrerenderedComponentProps<T>) {
  const [data, setData] = useState<T | null>(staticData || null)
  const [loading, setLoading] = useState(!staticData)

  useEffect(() => {
    const loadData = async () => {
      // 检查缓存
      const cachedData = cache.get<T>(key)
      if (cachedData) {
        setData(cachedData)
        setLoading(false)
        return
      }

      // 缓存过期或不存在，重新获取
      if (!staticData) {
        setLoading(true)
      }

      try {
        const result = await fetchFn()
        setData(result)
        cache.set(key, result, ttl)
      } catch (error) {
        console.error('Error fetching data:', error)
      } finally {
        setLoading(false)
      }
    }

    loadData()
  }, [fetchFn, key, ttl, staticData])

  if (loading) {
    return <div>Loading...</div>
  }

  if (!data) {
    return <div>Error loading data</div>
  }

  return children(data)
}
```

### 3.2 服务器端渲染与客户端缓存结合

```typescript
// pages/home.page.tsx
export { Page } from './Page'
export { prerender } from './prerender'

// pages/home/Page.tsx
import { useState, useEffect } from 'react'
import { CachedPrerenderedComponent } from '../../components/CachedPrerenderedComponent'
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }) {
  const fetchProducts = async () => {
    const response = await fetch('/api/products')
    return response.json()
  }

  return (
    <div>
      <h1>Home Page</h1>
      
      <CachedPrerenderedComponent
        key="products-list"
        fetchFn={fetchProducts}
        staticData={pageContext.staticData?.products}
        ttl={5 * 60 * 1000} // 5分钟缓存
      >
        {(products) => (
          <div>
            <h2>Products</h2>
            <ul>
              {products.map((product: { id: string; name: string }) => (
                <li key={product.id}>{product.name}</li>
              ))}
            </ul>
          </div>
        )}
      </CachedPrerenderedComponent>
    </div>
  )
}

// pages/home/prerender.ts
import type { PrerenderHook } from 'vite-plugin-ssr'

export const prerender: PrerenderHook = {
  renderPage: async () => {
    const products = await fetch('http://localhost:8081/api/products').then(res => res.json())
    
    return {
      pageContext: {
        staticData: { products }
      }
    }
  }
}
```

## 4. 性能优化模式

### 4.1 防抖缓存

```typescript
// src/hooks/useDebouncedCache.ts
import { useState, useEffect, useCallback } from 'react'

export function useDebouncedCache<T>(
  fetchFn: () => Promise<T>,
  key: string,
  ttl: number = 60 * 1000,
  debounceTime: number = 300
) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  const loadData = useCallback(async () => {
    try {
      // 检查缓存
      const cachedData = localStorage.getItem(key)
      if (cachedData) {
        const { value, timestamp } = JSON.parse(cachedData)
        if (Date.now() - timestamp < ttl) {
          setData(value)
          setLoading(false)
          return
        }
      }

      // 缓存过期或不存在，重新获取
      setLoading(true)
      const result = await fetchFn()
      setData(result)

      // 更新缓存
      localStorage.setItem(key, JSON.stringify({
        value: result,
        timestamp: Date.now()
      }))
    } catch (err) {
      setError(err as Error)
    } finally {
      setLoading(false)
    }
  }, [fetchFn, key, ttl])

  // 防抖加载
  useEffect(() => {
    const timer = setTimeout(loadData, debounceTime)
    return () => clearTimeout(timer)
  }, [loadData, debounceTime])

  return { data, loading, error }
}
```

### 4.2 批量缓存

```typescript
// src/utils/batchCache.ts
export const batchCache = {
  set: <T>(items: Array<{ key: string; value: T; ttl?: number }>) => {
    items.forEach(({ key, value, ttl = 60 * 1000 }) => {
      const item = {
        value,
        timestamp: Date.now(),
        ttl
      }
      localStorage.setItem(key, JSON.stringify(item))
    })
  },

  get: <T>(keys: string[]): Record<string, T | null> => {
    const result: Record<string, T | null> = {}
    
    keys.forEach(key => {
      const itemStr = localStorage.getItem(key)
      if (!itemStr) {
        result[key] = null
        return
      }

      const item = JSON.parse(itemStr)
      if (Date.now() - item.timestamp > item.ttl) {
        localStorage.removeItem(key)
        result[key] = null
      } else {
        result[key] = item.value as T
      }
    })

    return result
  }
}
```