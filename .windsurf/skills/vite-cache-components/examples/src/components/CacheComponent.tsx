import { useState, useEffect } from 'react'

type CacheComponentProps<T> = {
  children: () => T | React.ReactNode
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
        setData(result as T)
        
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