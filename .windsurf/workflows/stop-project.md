---
description: 停止项目所有服务（Java 后端 + Docker 容器），释放端口和资源
---

# 停止 Qt 产品发布平台

按顺序停止所有运行中的服务。

## 1. 停止后端 Java 进程

```powershell
Get-Process -Name java -ErrorAction SilentlyContinue | Stop-Process -Force 2>$null; Write-Output "后端已停止"
```

## 2. 停止 Docker 依赖服务

// turbo
```powershell
docker compose -f docker-compose.dev.yml stop
```

工作目录：`e:\oc\qt-platform`

> 注意：使用 `stop` 而非 `down`，保留数据卷。如需彻底清除数据，使用 `docker compose -f docker-compose.dev.yml down -v`。

## 3. 完成

所有服务已停止。前端开发服务器（Vite）会随终端关闭自动停止，无需额外处理。
