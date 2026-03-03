---
name: oc-platform-manager
description: |
  OC Platform 项目自动化管理技能 - 统一管理开发环境启动、停止和状态检查
  包括 Docker 依赖服务 (PostgreSQL + Redis + MinIO)、Spring Boot 后端服务、Vite 前端开发服务器
  支持智能端口检测、自动编译判断和故障排查
  自动记录各服务启动和运行状态到日志文件，便于调试和问题排查
version: 1.3.0
last_updated: 2026-03-04
---

# OC Platform 项目管理技能

> 自动化检查/执行项目依赖、后端/前端构建及运行

## 概述

本技能用于管理 OC Platform 项目的启动和停止，包括：
- Docker 依赖服务 (PostgreSQL + Redis + MinIO)
- Spring Boot 后端服务
- Vite 前端开发服务器

### 状态日志功能

技能会在 `e:/oc/logs/` 目录下自动创建状态日志文件：
- `docker-status.log` - Docker 容器状态信息
- `backend-status.log` - 后端服务启动和运行状态
- `frontend-status.log` - 前端服务启动和运行状态

**日志模式**: 采用**覆盖模式**，每次启动/停止项目时都会清空现有日志文件并重新记录，确保日志内容始终保持最新状态。

这些日志文件用于：
- 记录服务启动时间和状态
- 记录运行过程中的重要事件
- 便于问题排查和调试分析
- 跟踪服务健康状态
- 查看当前会话的完整操作记录

## 触发条件

当用户请求以下操作时触发：
- "启动项目"、"start project"、"运行项目"
- "停止项目"、"stop project"、"关闭项目"
- "重启项目"、"restart project"
- "检查项目状态"、"project status"

---

## 启动项目流程

### 0. 初始化状态日志

```powershell
# 创建日志目录
$logDir = "e:/oc/logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 初始化日志文件（覆盖模式）
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$dockerLog = "$logDir/docker-status.log"
$backendLog = "$logDir/backend-status.log"
$frontendLog = "$logDir/frontend-status.log"

# 清空现有日志文件并写入新的启动标记
"[$timestamp] ===== OC Platform 项目启动开始 =====" | Out-File -FilePath $dockerLog
"[$timestamp] ===== OC Platform 项目启动开始 =====" | Out-File -FilePath $backendLog
"[$timestamp] ===== OC Platform 项目启动开始 =====" | Out-File -FilePath $frontendLog
```

### 1. 检查 Docker Desktop

```powershell
$dockerCheck = docker info >$null 2>&1; if ($LASTEXITCODE -ne 0) { 
    $errorMsg = "Docker Desktop 未运行，请先启动 Docker Desktop"
    "[$timestamp] ERROR: $errorMsg" | Out-File -FilePath $dockerLog -Append
    Write-Error $errorMsg; exit 1 
} else { 
    $msg = "Docker Desktop 已就绪"
    "[$timestamp] INFO: $msg" | Out-File -FilePath $dockerLog -Append
    Write-Output $msg 
}
```

如果 Docker Desktop 未运行，提醒用户手动启动后重试。

### 2. 启动 Docker 依赖服务

// turbo
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 开始启动 Docker 依赖服务..." | Out-File -FilePath $dockerLog -Append

docker compose -f docker-compose.dev.yml up -d

if ($LASTEXITCODE -eq 0) {
    "[$timestamp] INFO: Docker 服务启动命令执行成功" | Out-File -FilePath $dockerLog -Append
} else {
    "[$timestamp] ERROR: Docker 服务启动失败，退出码: $LASTEXITCODE" | Out-File -FilePath $dockerLog -Append
}
```

工作目录：`e:\oc\oc-platform`

等待服务健康检查：

// turbo
```powershell
Start-Sleep -Seconds 5
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$dockerStatus = docker compose -f docker-compose.dev.yml ps

"[$timestamp] INFO: Docker 服务状态检查:" | Out-File -FilePath $dockerLog -Append
$dockerStatus | Out-File -FilePath $dockerLog -Append

# 检查关键服务状态
$healthyServices = @()
$unhealthyServices = @()

$services = docker compose -f docker-compose.dev.yml ps --format "table {{.Service}}\t{{.Status}}"
foreach ($service in $services) {
    if ($service -match "oc-dev-(postgres|redis|minio)") {
        if ($service -match "healthy|running") {
            $healthyServices += $service
        } else {
            $unhealthyServices += $service
        }
    }
}

"[$timestamp] INFO: 健康服务: $($healthyServices -join ', ')" | Out-File -FilePath $dockerLog -Append
if ($unhealthyServices.Count -gt 0) {
    "[$timestamp] WARNING: 异常服务: $($unhealthyServices -join ', ')" | Out-File -FilePath $dockerLog -Append
}
```

确认 `oc-dev-postgres`、`oc-dev-redis` 和 `oc-dev-minio` 状态为 healthy。

**服务信息：**
- PostgreSQL: localhost:5433, 用户 oc_user, 密码 3143285505
- Redis: localhost:6380, 密码 3143285505
- MinIO: localhost:9000 (API), localhost:9001 (Console)

### 3. 检查种子数据

// turbo
```powershell
$count = docker exec oc-dev-postgres psql -U oc_user -d oc_platform -t -c "SELECT count(*) FROM categories;" 2>$null; if ([int]$count.Trim() -eq 0) { Write-Output "NEED_SEED" } else { Write-Output "SEED_EXISTS: $($count.Trim()) categories" }
```

如果输出 `NEED_SEED`，执行种子数据导入：

```powershell
Get-Content sql/seed.sql | docker exec -i oc-dev-postgres psql -U oc_user -d oc_platform
```

工作目录：`e:\oc\oc-platform`

### 4. 停止已有 Java 进程

```powershell
Get-Process -Name java -ErrorAction SilentlyContinue | Stop-Process -Force 2>$null; Write-Output "已清理旧 Java 进程"
```

### 5. 编译后端（按需）

**判断是否需要重新编译：**
- 如果 `oc-platform-app/target/oc-platform-app-1.0.0-SNAPSHOT.jar` 不存在 → 需要编译
- 如果后端 Java 代码有修改（通过 git status 检查）→ 需要编译
- 否则跳过编译

// turbo
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$jarPath = "oc-platform-app/target/oc-platform-app-1.0.0-SNAPSHOT.jar"

if (-not (Test-Path $jarPath)) {
    "[$timestamp] INFO: JAR 文件不存在，开始编译后端..." | Out-File -FilePath $backendLog -Append
    $compileStart = Get-Date
    
    mvn clean package -DskipTests -pl oc-platform-app -am -q
    
    $compileEnd = Get-Date
    $compileDuration = ($compileEnd - $compileStart).TotalSeconds
    
    if ($LASTEXITCODE -eq 0) {
        "[$timestamp] INFO: 后端编译成功，耗时: $([math]::Round($compileDuration, 2))秒" | Out-File -FilePath $backendLog -Append
    } else {
        "[$timestamp] ERROR: 后端编译失败，退出码: $LASTEXITCODE" | Out-File -FilePath $backendLog -Append
        exit 1
    }
} else {
    "[$timestamp] INFO: JAR 文件已存在，跳过编译" | Out-File -FilePath $backendLog -Append
}
```

工作目录：`e:\oc\oc-platform`

编译约需 30-60 秒。

### 6. 启动后端

```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 开始启动后端服务..." | Out-File -FilePath $backendLog -Append

# 检查端口占用
$port8081 = netstat -ano | findstr ":8081" 2>$null
if ($port8081) {
    "[$timestamp] WARNING: 端口 8081 已被占用，尝试停止现有进程..." | Out-File -FilePath $backendLog -Append
    Get-Process -Name java -ErrorAction SilentlyContinue | Stop-Process -Force 2>$null
    Start-Sleep -Seconds 2
}

# 启动后端服务
$backendStart = Get-Date
$backendProcess = Start-Process -FilePath "java" -ArgumentList "-jar oc-platform-app\target\oc-platform-app-1.0.0-SNAPSHOT.jar --spring.profiles.active=dev" -PassThru -WindowStyle Hidden

"[$timestamp] INFO: 后端进程已启动，PID: $($backendProcess.Id)" | Out-File -FilePath $backendLog -Append

# 等待启动完成
$startTime = Get-Date
$timeoutSeconds = 30
$started = $false

while ((Get-Date) -lt $startTime.AddSeconds($timeoutSeconds) -and -not $started) {
    Start-Sleep -Seconds 2
    
    try {
        $response = curl.exe -s -o NUL -w "%{http_code}" http://localhost:8081/api/v1/categories 2>$null
        if ($response -eq "200") {
            $started = $true
            $startupTime = (Get-Date) - $backendStart
            "[$timestamp] INFO: 后端启动成功，耗时: $([math]::Round($startupTime.TotalSeconds, 2))秒" | Out-File -FilePath $backendLog -Append
        }
    } catch {
        # 继续等待
    }
}

if (-not $started) {
    "[$timestamp] ERROR: 后端启动超时，可能存在问题" | Out-File -FilePath $backendLog -Append
} else {
    "[$timestamp] INFO: 后端服务就绪 - API: http://localhost:8081, Swagger: http://localhost:8081/swagger-ui.html" | Out-File -FilePath $backendLog -Append
}
```

工作目录：`e:\oc\oc-platform`

以非阻塞方式运行，等待约 10 秒确认启动成功（看到 `Started OcPlatformApplication`）。

**后端信息：**
- API 地址: http://localhost:8081
- Swagger UI: http://localhost:8081/swagger-ui.html

### 7. 启动前端（按需）

**判断是否需要启动：**
- 检查 localhost:5173 是否已有服务运行
- 检查 localhost:5174 是否已有服务运行（备用端口）
- 如果已运行，跳过

**启动流程：**
1. 代码质量检查
2. 重新构建前端
3. 启动开发服务器

```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$frontendRunning = $false
$frontendPort = 5173

# 检查现有前端服务
try {
    $status5173 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5173 2>$null
    if ($status5173 -eq "200") { 
        $frontendRunning = $true
        $frontendPort = 5173
        "[$timestamp] INFO: 前端服务已在端口 5173 运行" | Out-File -FilePath $frontendLog -Append
    }
} catch { }

if (-not $frontendRunning) {
    try {
        $status5174 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5174 2>$null
        if ($status5174 -eq "200") { 
            $frontendRunning = $true
            $frontendPort = 5174
            "[$timestamp] INFO: 前端服务已在端口 5174 运行" | Out-File -FilePath $frontendLog -Append
        }
    } catch { }
}

if (-not $frontendRunning) {
    "[$timestamp] INFO: 开始启动前端服务..." | Out-File -FilePath $frontendLog -Append
    
    # 代码质量检查
    "[$timestamp] INFO: 正在检查前端代码质量..." | Out-File -FilePath $frontendLog -Append
    $lintStart = Get-Date
    npm run lint
    
    if ($LASTEXITCODE -ne 0) {
        "[$timestamp] WARNING: 代码质量检查发现问题，但继续启动前端服务" | Out-File -FilePath $frontendLog -Append
    } else {
        $lintDuration = (Get-Date) - $lintStart
        "[$timestamp] INFO: 代码质量检查通过，耗时: $([math]::Round($lintDuration.TotalSeconds, 2))秒" | Out-File -FilePath $frontendLog -Append
    }
    
    # 重新构建前端
    "[$timestamp] INFO: 正在重新构建前端..." | Out-File -FilePath $frontendLog -Append
    $buildStart = Get-Date
    npm run build
    
    if ($LASTEXITCODE -ne 0) {
        "[$timestamp] ERROR: 前端构建失败，请检查代码错误" | Out-File -FilePath $frontendLog -Append
        exit 1
    } else {
        $buildDuration = (Get-Date) - $buildStart
        "[$timestamp] INFO: 前端构建成功，耗时: $([math]::Round($buildDuration.TotalSeconds, 2))秒" | Out-File -FilePath $frontendLog -Append
    }
    
    # 启动前端开发服务器
    "[$timestamp] INFO: 正在启动前端开发服务器..." | Out-File -FilePath $frontendLog -Append
    $frontendStart = Get-Date
    
    # 启动 Vite 开发服务器
    $frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run", "dev" -PassThru -WindowStyle Hidden
    
    "[$timestamp] INFO: 前端进程已启动，PID: $($frontendProcess.Id)" | Out-File -FilePath $frontendLog -Append
    
    # 等待前端启动完成
    $startTime = Get-Date
    $timeoutSeconds = 15
    $started = $false
    
    while ((Get-Date) -lt $startTime.AddSeconds($timeoutSeconds) -and -not $started) {
        Start-Sleep -Seconds 1
        
        try {
            # 检查 5173 端口
            $response5173 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5173 2>$null
            if ($response5173 -eq "200") {
                $started = $true
                $frontendPort = 5173
                break
            }
            
            # 检查 5174 端口（备用）
            $response5174 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5174 2>$null
            if ($response5174 -eq "200") {
                $started = $true
                $frontendPort = 5174
                break
            }
        } catch {
            # 继续等待
        }
    }
    
    if ($started) {
        $startupTime = (Get-Date) - $frontendStart
        "[$timestamp] INFO: 前端启动成功，端口: $frontendPort，耗时: $([math]::Round($startupTime.TotalSeconds, 2))秒" | Out-File -FilePath $frontendLog -Append
        "[$timestamp] INFO: 前端服务就绪 - 地址: http://localhost:$frontendPort" | Out-File -FilePath $frontendLog -Append
    } else {
        "[$timestamp] ERROR: 前端启动超时，可能存在问题" | Out-File -FilePath $frontendLog -Append
    }
}
```

工作目录：`e:\oc\oc-platform\oc-platform-web`

以非阻塞方式运行，等待约 5 秒确认启动成功（看到 `VITE ready`）。

**前端信息：**
- 前端地址: http://localhost:5173（如果端口被占用会自动切换到5174）

### 8. 验证全链路

// turbo
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 开始全链路验证..." | Out-File -FilePath $dockerLog -Append
"[$timestamp] INFO: 开始全链路验证..." | Out-File -FilePath $backendLog -Append
"[$timestamp] INFO: 开始全链路验证..." | Out-File -FilePath $frontendLog -Append

# 验证后端
$backendCheck = curl.exe -s -o NUL -w "%{http_code}" http://localhost:8081/api/v1/categories 2>$null
if ($backendCheck -eq "200") {
    "[$timestamp] INFO: 后端 API 验证成功" | Out-File -FilePath $backendLog -Append
} else {
    "[$timestamp] ERROR: 后端 API 验证失败，状态码: $backendCheck" | Out-File -FilePath $backendLog -Append
}

# 验证前端
$frontendPort = 5173
$frontendStatus = curl.exe -s -o NUL -w "%{http_code}" http://localhost:$frontendPort 2>$null
if ($frontendStatus -ne "200") {
    $frontendPort = 5174
    $frontendStatus = curl.exe -s -o NUL -w "%{http_code}" http://localhost:$frontendPort 2>$null
}

if ($frontendStatus -eq "200") {
    "[$timestamp] INFO: 前端服务验证成功，端口: $frontendPort" | Out-File -FilePath $frontendLog -Append
} else {
    "[$timestamp] ERROR: 前端服务验证失败，状态码: $frontendStatus" | Out-File -FilePath $frontendLog -Append
}

# 完成标记
$completionTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$completionTime] ===== OC Platform 项目启动完成 =====" | Out-File -FilePath $dockerLog -Append
"[$completionTime] ===== OC Platform 项目启动完成 =====" | Out-File -FilePath $backendLog -Append
"[$completionTime] ===== OC Platform 项目启动完成 =====" | Out-File -FilePath $frontendLog -Append

Write-Output "前端端口: $frontendPort, 状态码: $frontendStatus"
Write-Output "项目启动状态已记录到: e:/oc/logs/"
```

返回 `200` 表示服务正常。

---

## 停止项目流程

### 0. 初始化停止日志

```powershell
# 创建日志目录（如果不存在）
$logDir = "e:/oc/logs"
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# 初始化日志文件（覆盖模式）
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$dockerLog = "$logDir/docker-status.log"
$backendLog = "$logDir/backend-status.log"
$frontendLog = "$logDir/frontend-status.log"

# 清空现有日志文件并写入新的停止标记
"[$timestamp] ===== OC Platform 项目停止开始 =====" | Out-File -FilePath $dockerLog
"[$timestamp] ===== OC Platform 项目停止开始 =====" | Out-File -FilePath $backendLog
"[$timestamp] ===== OC Platform 项目停止开始 =====" | Out-File -FilePath $frontendLog
```

### 1. 停止 Java 后端进程

```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 开始停止后端服务..." | Out-File -FilePath $backendLog -Append

$javaProcesses = Get-Process -Name java -ErrorAction SilentlyContinue
if ($javaProcesses) {
    $processCount = $javaProcesses.Count
    "[$timestamp] INFO: 发现 $processCount 个 Java 进程，正在停止..." | Out-File -FilePath $backendLog -Append
    
    $javaProcesses | ForEach-Object {
        "[$timestamp] INFO: 停止 Java 进程 PID: $($_.Id)" | Out-File -FilePath $backendLog -Append
    }
    
    $javaProcesses | Stop-Process -Force 2>$null
    
    Start-Sleep -Seconds 2
    $remainingProcesses = Get-Process -Name java -ErrorAction SilentlyContinue
    if ($remainingProcesses) {
        "[$timestamp] WARNING: 仍有 $($remainingProcesses.Count) 个 Java 进程在运行" | Out-File -FilePath $backendLog -Append
    } else {
        "[$timestamp] INFO: 所有 Java 进程已停止" | Out-File -FilePath $backendLog -Append
    }
} else {
    "[$timestamp] INFO: 未发现运行中的 Java 进程" | Out-File -FilePath $backendLog -Append
}

Write-Output "后端已停止"
```

### 2. 停止 Docker 依赖服务

// turbo
```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 开始停止 Docker 依赖服务..." | Out-File -FilePath $dockerLog -Append

# 记录停止前的状态
$stopStatus = docker compose -f docker-compose.dev.yml ps
"[$timestamp] INFO: 停止前 Docker 服务状态:" | Out-File -FilePath $dockerLog -Append
$stopStatus | Out-File -FilePath $dockerLog -Append

docker compose -f docker-compose.dev.yml stop

if ($LASTEXITCODE -eq 0) {
    "[$timestamp] INFO: Docker 服务停止命令执行成功" | Out-File -FilePath $dockerLog -Append
    
    # 记录停止后的状态
    Start-Sleep -Seconds 2
    $afterStopStatus = docker compose -f docker-compose.dev.yml ps
    "[$timestamp] INFO: 停止后 Docker 服务状态:" | Out-File -FilePath $dockerLog -Append
    $afterStopStatus | Out-File -FilePath $dockerLog -Append
} else {
    "[$timestamp] ERROR: Docker 服务停止失败，退出码: $LASTEXITCODE" | Out-File -FilePath $dockerLog -Append
}
```

工作目录：`e:\oc\oc-platform`

> 注意：使用 `stop` 而非 `down`，保留数据卷。如需彻底清除数据，使用 `docker compose -f docker-compose.dev.yml down -v`。

### 3. 前端服务

```powershell
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INFO: 检查前端服务状态..." | Out-File -FilePath $frontendLog -Append

# 检查前端服务是否仍在运行
$frontend5173Running = $false
$frontend5174Running = $false

try {
    $status5173 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5173 2>$null
    if ($status5173 -eq "200") { 
        $frontend5173Running = $true
        "[$timestamp] INFO: 端口 5173 上的前端服务仍在运行" | Out-File -FilePath $frontendLog -Append
    }
} catch { }

try {
    $status5174 = curl.exe -s -o NUL -w "%{http_code}" http://localhost:5174 2>$null
    if ($status5174 -eq "200") { 
        $frontend5174Running = $true
        "[$timestamp] INFO: 端口 5174 上的前端服务仍在运行" | Out-File -FilePath $frontendLog -Append
    }
} catch { }

if (-not $frontend5173Running -and -not $frontend5174Running) {
    "[$timestamp] INFO: 前端服务已停止" | Out-File -FilePath $frontendLog -Append
}

# 前端开发服务器（Vite）会随终端关闭自动停止，无需额外处理
```

### 4. 完成停止记录

```powershell
$completionTime = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$completionTime] ===== OC Platform 项目停止完成 =====" | Out-File -FilePath $dockerLog -Append
"[$completionTime] ===== OC Platform 项目停止完成 =====" | Out-File -FilePath $backendLog -Append
"[$completionTime] ===== OC Platform 项目停止完成 =====" | Out-File -FilePath $frontendLog -Append

Write-Output "项目停止状态已记录到: e:/oc/logs/"
```

---

## 重启项目流程

1. 执行停止项目流程
2. 执行启动项目流程

---

## 服务端口一览

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 | 5173（可能自动切换到5174） | Vite 开发服务器 |
| 后端 API | 8081 | Spring Boot |
| Swagger UI | 8081/swagger-ui.html | API 文档 |
| PostgreSQL | 5433 | 数据库 |
| Redis | 6380 | 缓存 |
| MinIO API | 9000 | 对象存储服务 |
| MinIO Console | 9001 | 对象存储管理界面 |

## 测试账号

- 管理员: admin@OcPlatform.com / Admin@123456
- 普通用户: zhangsan@example.com / Test@123456

## 故障排查

### 常见问题

1. **Docker Desktop 未启动**
   - 错误: `Cannot connect to the Docker daemon`
   - 解决: 手动启动 Docker Desktop 后重试

2. **端口占用**
   - 前端 5173 被占用: 自动切换到 5174
   - 后端 8081 被占用: 检查是否有其他 Java 进程
   - PostgreSQL 5433 被占用: 停止本地 PostgreSQL 服务
   - MinIO 9000-9001 被占用: 停止冲突服务

3. **数据库连接失败**
   - 检查 Docker 容器是否正常运行: `docker compose ps`
   - 检查数据库密码是否正确
   - 重新导入种子数据

4. **前端编译错误**
   - 删除 node_modules 重新安装: `rm -rf node_modules && npm install`
   - 检查代码质量: `npm run lint`
   - 检查 TypeScript 类型错误: `npm run type-check`
   - 检查构建问题: `npm run build`

5. **后端编译失败**
   - 检查 Java 版本（需要 JDK 17+）
   - 清理 Maven 缓存: `mvn clean`
   - 检查依赖版本冲突

6. **文件下载失败 (HTTP 400)**
   - 检查文件存储类型（支持 LOCAL 和 MINIO）
   - 确认文件记录存在: `SELECT * FROM file_records WHERE id = ?`
   - 检查文件路径是否正确

### 日志查看

#### 状态日志文件
技能会自动在 `e:/oc/logs/` 目录下创建状态日志文件（**覆盖模式**）：
- **docker-status.log** - Docker 容器启动/停止状态信息
- **backend-status.log** - 后端服务启动/停止和运行状态
- **frontend-status.log** - 前端服务启动/停止和运行状态

**日志特点**:
- 每次操作都会覆盖整个日志文件
- 只保留当前会话的完整记录
- 避免日志文件过大和冗余信息

这些日志文件包含：
- 服务启动和停止时间戳
- 进程 PID 信息
- 端口占用检查结果
- 编译和启动耗时统计
- 错误和警告信息
- 健康检查结果

#### 其他日志
- **后端日志**: 控制台输出或日志文件
- **前端日志**: Vite 开发服务器控制台
- **Docker 日志**: `docker compose logs -f`

#### 日志文件使用
```powershell
# 查看最新的 Docker 状态
Get-Content "e:/oc/logs/docker-status.log" -Tail 20

# 查看最新的后端状态
Get-Content "e:/oc/logs/backend-status.log" -Tail 20

# 查看最新的前端状态
Get-Content "e:/oc/logs/frontend-status.log" -Tail 20

# 搜索错误信息
Select-String -Pattern "ERROR|WARNING" -Path "e:/oc/logs/*.log"
```

---

## 智能判断逻辑

本技能会根据代码改动智能决定操作：

1. **后端代码改动** (`.java` 文件)
   - 需要重新编译: `mvn clean package`
   - 需要重启后端

2. **前端代码改动** (`.tsx`, `.ts`, `.css`, `.json` 文件)
   - 启动前会自动运行 `npm run lint` 检查代码质量
   - 启动前会自动运行 `npm run build` 重新构建前端
   - Vite HMR 自动热更新，开发时无需重启
   - 修改 `package.json` 需要重新安装依赖: `npm install`
   - 修改 `vite.config.ts` 需要重启前端服务

3. **数据库改动** (`.sql` 文件)
   - 需要执行 SQL 脚本或重新导入种子数据

4. **配置文件改动** (`application.yml`, `vite.config.ts`)
   - 需要重启对应服务

5. **端口冲突处理**
   - 前端端口 5173 被占用时自动切换到 5174
   - 后端端口 8081 固定（避免与 Apache httpd 8080 冲突）
   - PostgreSQL 端口 5433（Docker映射 5433→5432）
   - Redis 端口 6380（Docker映射 6380→6379）
   - MinIO 端口 9000-9001（Docker直接映射）
