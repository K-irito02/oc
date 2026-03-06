---
description: 开发环境搭建说明
scope: project
trigger: always_on
---

# 开发环境搭建说明

## 软件安装清单

| 软件 | 版本 | 安装方式 | 用途 |
|------|------|---------|------|
| **JDK** | OpenJDK 17.0.15 (Temurin) | [adoptium.net](https://adoptium.net) | 后端运行环境 |
| **Node.js** | 22.x LTS | nvm-windows 管理 | 前端运行环境 |
| **Maven** | 3.9.x | 官网安装 | 后端构建工具 |
| **Docker Desktop** | Latest | 官网安装，启用 WSL2 | 容器化开发 |
| **Git** | 2.49.0+ | 官网安装 | 版本控制 |
| **IntelliJ IDEA** | Ultimate (推荐) | JetBrains | 后端 IDE |
| **VS Code** | Latest | 官网安装 | 前端开发 |

## 端口配置

| 服务 | 端口 | 说明 |
|------|------|------|
| **后端 API** | 8081 | Spring Boot 应用 |
| **前端开发** | 5173 | Vite 开发服务器（可能自动切换到5174） |
| **PostgreSQL** | 5433 | 数据库服务（Docker映射：5433→5432） |
| **Redis** | 6380 | 缓存服务（Docker映射：6380→6379） |
| **MinIO** | 9000 | 对象存储服务 |
| **MinIO Console** | 9001 | 对象存储管理界面 |
| **Nginx** | 80 | 反向代理（生产） |

> **注意**: 本机 Apache httpd 占用 8080 端口，后端改用 8081
> **Docker端口映射**: PostgreSQL 5433→5432, Redis 6380→6379

## 本地环境版本

| 软件 | 版本 |
|------|------|
| JDK | OpenJDK 17.0.15 (Temurin) |
| Maven | 3.9.12 |
| Node.js | v22.14.0 |
| npm | 10.9.2 |
| Git | 2.49.0 |
| Docker | 29.2.0 |
| Docker Compose | v5.0.2 |

## 开发工具配置

### IntelliJ IDEA

1. **JDK 配置**
   - 设置 JDK 17+
   - 配置 JAVA_HOME 环境变量

2. **插件安装**
   - Lombok Plugin
   - MyBatis-Plus Plugin
   - Spring Boot Assistant

3. **代码风格**
   - 配置 Google Java Style
   - 启用 Save Actions 自动格式化

### VS Code

1. **扩展安装**
   - Java Extension Pack
   - React/TypeScript 扩展
   - ESLint 和 Prettier
   - Tailwind CSS IntelliSense

2. **配置建议**
   ```json
   {
     "editor.formatOnSave": true,
     "editor.defaultFormatter": "esbenp.prettier-vscode",
     "typescript.preferences.importModuleSpecifier": "relative"
   }
   ```

### Postman 配置

1. **导入 API 文档**
   - 访问 `http://localhost:8081/swagger-ui.html`
   - 导出 OpenAPI 规范
   - 导入到 Postman

2. **环境变量**
   ```json
   {
     "name": "Development",
     "values": [
       { "key": "baseUrl", "value": "http://localhost:8081/api/v1" },
       { "key": "token", "value": "" }
     ]
   }
   ```

## 数据库管理

### 连接信息

| 项目 | 值 |
|------|------|
| 主机 | localhost |
| 端口 | 5433 |
| 数据库 | oc_platform |
| 用户名 | oc_user |
| 密码 | 3143285505 |

## Redis 管理

### 连接信息

| 项目 | 值 |
|------|------|
| 主机 | localhost |
| 端口 | 6380 |
| 密码 | 3143285505 |

## MinIO 管理

### 访问信息

| 项目 | 值 |
|------|------|
| API 地址 | http://localhost:9000 |
| Console 地址 | http://localhost:9001 |
| 用户名 | minioadmin |
| 密码 | minioadmin |

### 存储桶

- `oc-products` - 产品文件
- `oc-avatars` - 用户头像
- `oc-screenshots` - 产品截图
