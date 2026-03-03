import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import ssr from 'vite-plugin-ssr/plugin'
import path from 'path'

export default defineConfig({
  plugins: [
    react(),
    ssr({
      prerender: {
        enabled: true,
        partial: true,
        routes: ['/', '/about'],
        parallel: 4
      },
      dev: {
        debug: true
      }
    })
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8081',
        changeOrigin: true,
      }
    },
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
})