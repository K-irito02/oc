---
description: 开发环境启动指南
scope: project
trigger: always_on
---

# 开发环境启动指南

## 服务访问

| 服务 | 地址 | 说明 |
|------|------|------|
| **前端应用** | http://localhost:5173 | Vite 开发服务器（可能自动切换到5174） |
| **后端 API** | http://localhost:8081 | Spring Boot 应用 |
| **Swagger UI** | http://localhost:8081/swagger-ui.html | API 文档 |
| **PostgreSQL** | localhost:5433 | 数据库（用户：oc_user） |
| **Redis** | localhost:6380 | 缓存服务 |
| **MinIO Console** | http://localhost:9001 | 对象存储管理界面 |

## 测试账号

- **超级管理员**: KirLab / 3143285505@qq.com（密码通过init.sql创建）
- **普通用户**: 需自行注册

## 常用命令

### Docker 服务
```bash
# 启动依赖服务
docker compose -f docker-compose.dev.yml up -d

# 查看服务状态
docker compose -f docker-compose.dev.yml ps

# 停止服务
docker compose -f docker-compose.dev.yml stop

# 查看日志
docker compose -f docker-compose.dev.yml logs -f

# 重置数据库
docker compose -f docker-compose.dev.yml down -v
docker compose -f docker-compose.dev.yml up -d
```

### 后端
```bash
# 编译（跳过测试）
mvn clean package -DskipTests

# 编译特定模块
mvn clean package -DskipTests -pl oc-platform-app -am

# 运行应用
java -jar oc-platform-app/target/oc-platform-app-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev

# Maven 热重载运行（推荐开发时使用）
mvn spring-boot:run -pl oc-platform-app -Dspring-boot.run.profiles=dev
```

### 前端
```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 类型检查
npx tsc --noEmit

# 代码检查
npm run lint
```

## 端口说明

| 服务 | 端口 | 说明 |
|------|------|------|
| 后端 API | 8081 | 避免与 Apache httpd 8080 冲突 |
| 前端开发 | 5173 | Vite 默认（可能自动切换到5174） |
| PostgreSQL | 5433 | Docker 映射 5433→5432 |
| Redis | 6380 | Docker 映射 6380→6379 |
| MinIO | 9000 | 对象存储 API |
| MinIO Console | 9001 | 对象存储管理界面 |

## 注意事项

1. **端口冲突**: 如果 5173 被占用，Vite 会自动切换到 5174
2. **数据库密码**: 开发环境使用固定密码，生产环境请使用环境变量
3. **邮件服务**: 使用 QQ 邮箱 SMTP，需要在 application.yml 中配置授权码
4. **热重载**: 前端支持热重载，后端修改需重启应用
5. **Mock 数据**: 可通过 `.env.local` 设置 `VITE_ENABLE_MOCK=false` 禁用 Mock

## 禁用 Mock 数据

前端默认启用 Mock 拦截器（后端未启动时提供模拟数据）。后端运行时，可创建 `.env.local` 禁用 Mock 以使用真实 API：

```bash
# oc-platform-web/.env.local
VITE_ENABLE_MOCK=false
```

## 项目管理技能

使用 `oc-platform-manager` 技能可以一键管理开发环境。