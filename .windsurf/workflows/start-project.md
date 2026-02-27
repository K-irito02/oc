---
description: 一键启动项目所有服务（Docker + 后端 + 前端），用于本地开发
---

# 启动 Qt 产品发布平台

按顺序执行以下步骤，启动本地开发环境的全部服务。

## 1. 检查 Docker Desktop 是否运行

```powershell
docker info >$null 2>&1; if ($LASTEXITCODE -ne 0) { Write-Error "Docker Desktop 未运行，请先启动 Docker Desktop"; exit 1 } else { Write-Output "Docker Desktop 已就绪" }
```

如果 Docker Desktop 未运行，提醒用户手动启动 Docker Desktop 后重试。

## 2. 启动 Docker 依赖服务（PostgreSQL + Redis）

// turbo
```powershell
docker compose -f docker-compose.dev.yml up -d
```

工作目录：`e:\oc\qt-platform`

等待服务变为 healthy：

// turbo
```powershell
Start-Sleep -Seconds 5; docker compose -f docker-compose.dev.yml ps
```

确认两个服务（qt-dev-postgres、qt-dev-redis）状态为 healthy。

服务信息：
- **PostgreSQL**: localhost:5433, 用户 qt_user, 密码 3143285505, 数据库 qt_platform
- **Redis**: localhost:6380, 密码 3143285505

## 3. 检查是否需要导入种子数据

// turbo
```powershell
$count = docker exec qt-dev-postgres psql -U qt_user -d qt_platform -t -c "SELECT count(*) FROM categories;" 2>$null; if ([int]$count.Trim() -eq 0) { Write-Output "NEED_SEED" } else { Write-Output "SEED_EXISTS: $($count.Trim()) categories" }
```

如果输出 `NEED_SEED`，执行种子数据导入：

```powershell
Get-Content sql/seed.sql | docker exec -i qt-dev-postgres psql -U qt_user -d qt_platform
```

工作目录：`e:\oc\qt-platform`

## 4. 停止已有的 Java 进程（避免端口冲突）

```powershell
Get-Process -Name java -ErrorAction SilentlyContinue | Stop-Process -Force 2>$null; Write-Output "已清理旧 Java 进程"
```

## 5. 编译后端项目

// turbo
```powershell
mvn clean package -DskipTests -pl qt-platform-app -am -q
```

工作目录：`e:\oc\qt-platform`

编译约需 30-60 秒，无输出表示成功。

## 6. 启动后端（后台运行）

```powershell
java -jar qt-platform-app\target\qt-platform-app-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev
```

工作目录：`e:\oc\qt-platform`

此命令以非阻塞方式运行，等待约 10 秒后检查日志确认启动成功（看到 `Started QtPlatformApplication`）。

后端信息：
- **API 地址**: http://localhost:8081
- **Swagger UI**: http://localhost:8081/swagger-ui.html

## 7. 启动前端开发服务器（后台运行）

```powershell
npm run dev
```

工作目录：`e:\oc\qt-platform\qt-platform-web`

此命令以非阻塞方式运行，等待约 5 秒后确认启动成功（看到 `VITE ready`）。

前端信息：
- **前端地址**: http://localhost:5173（如被占用则 5174）

## 8. 验证全链路

// turbo
```powershell
curl.exe -s -o NUL -w "%{http_code}" http://localhost:8081/api/v1/categories
```

如果返回 `200`，则后端 API 正常。

// turbo
```powershell
curl.exe -s -o NUL -w "%{http_code}" http://localhost:5173
```

如果返回 `200`，则前端正常。

## 9. 完成

所有服务已启动，可以开始开发：

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端 | http://localhost:5173 | Vite 开发服务器 |
| 后端 API | http://localhost:8081 | Spring Boot |
| Swagger UI | http://localhost:8081/swagger-ui.html | API 文档 |
| PostgreSQL | localhost:5433 | 用户 qt_user / 密码 3143285505 |
| Redis | localhost:6380 | 密码 3143285505 |

管理员登录：admin@qtplatform.com / Admin@123456
