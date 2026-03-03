# 部署与运维记忆

> 最后更新: 2026-02-28

## 开发环境

### 本地端口分配

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端 API | 8081 | Spring Boot（8080 被 Apache httpd 占用） |
| 前端开发 | 5173 | Vite 开发服务器（可能自动切换到5174） |
| PostgreSQL | 5433 | Docker 容器（映射 5433→5432） |
| Redis | 6380 | Docker 容器（映射 6380→6379） |
| MinIO | 9000 | 对象存储服务 |
| MinIO Console | 9001 | 对象存储管理界面 |

### 本地环境版本

| 软件 | 版本 |
|------|------|
| JDK | OpenJDK 17.0.15 (Temurin) |
| Maven | 3.9.12 |
| Node.js | v22.14.0 |
| npm | 10.9.2 |
| Git | 2.49.0 |
| Docker | 29.2.0 |
| Docker Compose | v5.0.2 |

### 开发依赖启动

```bash
# 启动 PostgreSQL + Redis
cd oc-platform
docker compose -f docker-compose.dev.yml up -d

# 验证服务
docker ps  # 确认 oc-dev-postgres 和 oc-dev-redis 运行中
```

## Docker 配置

### 开发环境 (`docker-compose.dev.yml`)

仅启动依赖服务，应用在 IDE 中运行：
- **postgres**: PostgreSQL 15-alpine, 端口 5433（映射 5433→5432）, 数据卷持久化, 自动执行 init.sql
- **redis**: Redis 7-alpine, 端口 6380（映射 6380→6379）, appendonly, maxmemory 128mb
- **minio**: MinIO Latest, 端口 9000（映射 9000→9000）, 端口 9001（映射 9001→9001）, 对象存储服务

### 生产环境 (`docker-compose.yml`)

全栈部署：
- **postgres**: PostgreSQL 15-alpine
- **redis**: Redis 7-alpine
- **minio**: MinIO Latest
- **backend**: Spring Boot 多阶段构建 (Dockerfile)
- **frontend**: React 构建 + Nginx (Dockerfile in oc-platform-web)

### Dockerfile

#### 后端 (`oc-platform-app/Dockerfile`)
- 多阶段构建
- Stage 1: Maven 构建
- Stage 2: Eclipse Temurin 17 JRE 运行

#### 前端 (oc-platform-web)
- Stage 1: Node 22 构建 `npm run build`
- Stage 2: Nginx alpine 静态文件服务

## CI/CD

### GitHub Actions (`.github/workflows/ci.yml`)

触发条件:
- Push to `main`, `develop`
- Pull Request to `main`

Pipeline:
1. **后端**: checkout → JDK 17 → Maven build → test → Docker build & push
2. **前端**: checkout → Node 22 → npm install → lint → build → Docker build & push
3. **部署**: SSH 到服务器 → docker compose pull → docker compose up -d

## 环境变量模板

参见 `oc-platform/.env.example`:

```env
# Database
DB_HOST=localhost
DB_PORT=5433
DB_NAME=oc_platform
DB_USER=oc_user
DB_PASSWORD=3143285505

# Redis
REDIS_HOST=localhost
REDIS_PORT=6380
REDIS_PASSWORD=3143285505

# JWT
JWT_SECRET=your-64-char-secret-key
JWT_ACCESS_EXPIRATION=7200
JWT_REFRESH_EXPIRATION=604800

# Mail
MAIL_HOST=smtp.example.com
MAIL_PORT=465
MAIL_USERNAME=
MAIL_PASSWORD=

# GitHub OAuth
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
GITHUB_REDIRECT_URI=http://localhost:5173/oauth/github/callback

# Storage
UPLOAD_PATH=./uploads
MAX_FILE_SIZE=1073741824

# MinIO
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET_PRODUCTS=qt-products
MINIO_BUCKET_AVATARS=qt-avatars
```

## Nginx 配置

- 反向代理: `/api` → 后端
- 静态资源: 前端 build 产物
- SSL 终止（生产环境）
- 限流配置

## Git 仓库管理

### 仓库分离策略

#### 1. 项目环境状态仓库 (E:\oc)
- **仓库路径**: `E:/oc/`
- **远程地址**: `https://github.com/K-irito02/oc.git`
- **主要用途**: 保存 AI 配置、规则、技能、工作流和项目记忆
- **分支策略**: 简化的单分支或双分支模式
- **文件大小**: 优化后约 2.64MB

#### 2. 项目代码仓库 (E:\oc\oc-platform)
- **仓库路径**: `E:/oc/oc-platform/`
- **主要用途**: 保存前后端代码、数据库脚本、部署配置
- **分支策略**: 完整的 GitFlow 工作流

### Git 配置优化

#### 代理环境配置
```bash
# 推荐配置（解决 HTTP 408 超时问题）
git config --global http.version HTTP/1.1
git config --global http.postBuffer 524288000
git config --global http.lowSpeedLimit 0
git config --global http.lowSpeedTime 999999
```

#### 大文件清理
```bash
# 从历史中移除大文件
git filter-branch --force --index-filter 'git rm --cached --ignore-unmatch "大文件路径"' --prune-empty --tag-name-filter cat -- --all
git gc --aggressive --prune=now
```

## 目标部署平台

- **阶段一**: 腾讯云 CVM (Docker Compose)
- **阶段二**: 腾讯云 COS (文件存储) + CDN
- **阶段三**: Kubernetes 容器编排
