export { Page } from './Page'
export { prerender } from './prerender'

// pages/Page.tsx
import { useState, useEffect } from 'react'
import { CacheComponent } from '../components/CacheComponent'
import type { PageContext } from 'vite-plugin-ssr'

export function Page({ pageContext }: { pageContext: PageContext }) {
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
      <h1>Welcome to Vite Cache Components</h1>
      <p>This content is prerendered at build time.</p>
      
      {/* 缓存组件示例 */}
      <CacheComponent key="cached-data" ttl={300000}>
        {() => (
          <div>
            <h2>Cached Content</h2>
            <p>This content is cached for 5 minutes.</p>
            <p>Current time: {new Date().toLocaleTimeString()}</p>
          </div>
        )}
      </CacheComponent>
      
      {/* 动态部分 - 客户端渲染 */}
      <div>
        <h2>Dynamic Content</h2>
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
    try {
      const staticData = await fetch('http://localhost:8081/api/static-data').then(res => res.json())
      
      return {
        pageContext: {
          staticData
        }
      }
    } catch (error) {
      console.warn('API unavailable during prerender, using mock data')
      return {
        pageContext: {
          staticData: {
            message: 'Mock static data for prerender'
          }
        }
      }
    }
  }
}