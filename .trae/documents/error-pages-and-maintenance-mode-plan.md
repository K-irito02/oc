# 错误页面与维护模式实施计划

## 一、需求分析

### 1.1 当前状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 404 页面 | ✅ 已存在 | 使用 Ant Design Result 组件，功能简单 |
| 500 页面 | ❌ 不存在 | 需要新增 |
| 403 页面 | ❌ 不存在 | 需要新增 |
| 网络错误页面 | ❌ 不存在 | 需要新增 |
| 维护页面 | ❌ 不存在 | 需要新增 |
| 维护模式后端 | ❌ 不存在 | 需要新增 |

### 1.2 需求目标

1. **错误页面增强**：为响应式错误页面添加更丰富的内容和更好的视觉设计
2. **维护模式**：实现完整的网站维护模式功能，支持后台开关控制
3. **国际化支持**：所有新增内容支持中英文切换

---

## 二、UI/UX 设计规范（基于 ui-ux-pro-max）

### 2.1 设计原则

#### 优先级分类

| 优先级 | 类别 | 影响程度 | 应用场景 |
|--------|------|----------|----------|
| 1 | 可访问性 | CRITICAL | 颜色对比度、焦点状态、键盘导航 |
| 2 | 触摸与交互 | CRITICAL | 触摸目标大小、加载状态、错误反馈 |
| 3 | 性能 | HIGH | 图片优化、减少动画 |
| 4 | 布局与响应式 | HIGH | 视口适配、字体大小 |
| 5 | 排版与颜色 | MEDIUM | 行高、颜色搭配 |
| 6 | 动画 | MEDIUM | 过渡时间、性能优化 |

### 2.2 视觉设计规范

#### 图标规范
- **使用 SVG 图标**：使用 Lucide React 图标库（项目已集成）
- **禁止使用 Emoji**：不使用 emoji 作为 UI 图标
- **统一尺寸**：图标使用 `w-16 h-16` 或 `w-20 h-20`（大图标）

#### 颜色对比度（WCAG AA 标准）
| 元素 | 浅色模式 | 深色模式 | 对比度 |
|------|---------|---------|--------|
| 主标题 | `slate-900` (#0F172A) | `white` (#FFFFFF) | > 4.5:1 |
| 副标题 | `slate-600` (#475569) | `slate-400` (#94A3B8) | > 4.5:1 |
| 描述文字 | `slate-500` (#64748B) | `slate-500` (#64748B) | > 4.5:1 |

#### 动画规范
- **过渡时间**：150-300ms（微交互）
- **缓动函数**：`ease-in-out`
- **性能优化**：使用 `transform` 和 `opacity`，避免 `width/height`
- **减少动画**：尊重 `prefers-reduced-motion` 媒体查询

#### 交互规范
- **触摸目标**：最小 44x44px
- **光标样式**：所有可点击元素添加 `cursor-pointer`
- **悬停反馈**：使用颜色/透明度变化，避免布局位移
- **焦点状态**：可见的焦点环（focus ring）

### 2.3 错误页面设计

#### 页面类型与图标

| 错误类型 | HTTP 状态码 | Lucide 图标 | 图标颜色 |
|---------|------------|-------------|---------|
| 404 Not Found | 404 | `FileQuestion` | `text-blue-500` |
| 500 Server Error | 500 | `ServerCrash` | `text-red-500` |
| 403 Forbidden | 403 | `ShieldX` | `text-orange-500` |
| 网络错误 | N/A | `WifiOff` | `text-yellow-500` |
| 维护页面 | 503 | `Wrench` | `text-purple-500` |

#### 布局结构

```
┌─────────────────────────────────────────────────────────────┐
│                      全屏居中容器                            │
│  min-h-screen flex items-center justify-center              │
│  bg-slate-50 dark:bg-slate-950                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│                    ┌─────────────┐                          │
│                    │   图标动画   │  w-20 h-20              │
│                    │  (SVG Icon)  │  带脉冲动画              │
│                    └─────────────┘                          │
│                                                             │
│                    ┌─────────────┐                          │
│                    │   错误代码   │  text-6xl font-bold      │
│                    │    404      │  text-slate-900          │
│                    └─────────────┘                          │
│                                                             │
│                    ┌─────────────┐                          │
│                    │   错误标题   │  text-2xl font-semibold  │
│                    │ 页面未找到   │  text-slate-700          │
│                    └─────────────┘                          │
│                                                             │
│                    ┌─────────────┐                          │
│                    │   错误描述   │  text-slate-500          │
│                    │  友好提示... │  max-w-md text-center    │
│                    └─────────────┘                          │
│                                                             │
│                    ┌─────────────┐                          │
│                    │  操作按钮   │  cursor-pointer           │
│                    │  返回首页   │  transition-colors        │
│                    └─────────────┘                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 2.4 维护页面设计

#### 特殊元素
- **进度指示器**：可选的维护进度条
- **预计时间**：显示预计恢复时间
- **联系方式**：提供紧急联系方式

---

## 三、技术方案设计

### 3.1 维护模式架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端请求                              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    维护模式拦截器                            │
│  检查 system.maintenance.enabled 配置                       │
│  - true: 返回 503 维护响应                                   │
│  - false: 放行请求                                          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      正常业务处理                            │
└─────────────────────────────────────────────────────────────┘
```

#### 白名单路径（维护期间仍可访问）

- `/api/v1/admin/**` - 管理后台 API
- `/api/v1/auth/login` - 登录接口（管理员需要）
- `/api/v1/public/system/maintenance` - 维护状态查询
- 静态资源

---

## 四、详细实施步骤

### 4.1 后端实现

#### 步骤 1：数据库配置项

在 `system_configs` 表中添加维护模式配置：

```sql
INSERT INTO system_configs (config_key, config_value, description) VALUES
('system.maintenance.enabled', 'false', '系统维护模式开关'),
('system.maintenance.title', '系统维护中', '维护页面标题'),
('system.maintenance.title_en', 'Under Maintenance', '维护页面标题（英文）'),
('system.maintenance.message', '系统正在进行升级维护，请稍后再试。', '维护说明'),
('system.maintenance.message_en', 'The system is under maintenance. Please try again later.', '维护说明（英文）'),
('system.maintenance.estimated_time', '', '预计恢复时间');
```

#### 步骤 2：维护模式 DTO

创建 `MaintenanceConfigDTO` 和 `MaintenanceStatusDTO`。

#### 步骤 3：维护模式拦截器

创建 `MaintenanceInterceptor`：
- 读取维护配置
- 检查白名单路径
- 返回 503 响应或放行

#### 步骤 4：维护模式 API

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/v1/admin/system/maintenance` | GET | 获取维护配置 |
| `/api/v1/admin/system/maintenance` | PUT | 更新维护配置 |
| `/api/v1/public/system/maintenance` | GET | 公开获取维护状态 |

#### 步骤 5：错误码扩展

```java
SERVICE_UNAVAILABLE(50301, "服务暂时不可用"),
MAINTENANCE_MODE(50302, "系统维护中")
```

### 4.2 前端实现

#### 步骤 1：创建通用错误页面组件

**文件**: `src/pages/Error/index.tsx`

```tsx
// 设计要点：
// 1. 使用 Lucide React 图标（FileQuestion, ServerCrash, ShieldX, WifiOff）
// 2. 支持深色/浅色主题
// 3. 添加脉冲动画（animate-pulse）
// 4. 国际化支持
// 5. 响应式布局
```

#### 步骤 2：创建维护页面组件

**文件**: `src/pages/Maintenance/index.tsx`

```tsx
// 设计要点：
// 1. 使用 Wrench 图标
// 2. 从后端获取维护信息
// 3. 显示预计恢复时间
// 4. 支持中英文切换
// 5. 添加倒计时（可选）
```

#### 步骤 3：创建维护模式 Hook

**文件**: `src/hooks/useMaintenance.ts`

```tsx
// 功能：
// 1. 检查维护状态
// 2. 自动跳转到维护页面
// 3. 缓存维护状态
```

#### 步骤 4：路由配置更新

**文件**: `src/router/index.tsx`

```tsx
// 新增路由：
// - /maintenance -> Maintenance
// - /500 -> Error500
// - /403 -> Error403
```

#### 步骤 5：HTTP 拦截器更新

**文件**: `src/utils/request.ts`

```tsx
// 处理：
// - 503 响应 -> 跳转维护页面
// - 500 响应 -> 显示错误页面
// - 403 响应 -> 显示权限页面
```

#### 步骤 6：国际化翻译

**文件**: `src/locales/zh-CN.json` 和 `src/locales/en-US.json`

```json
{
  "error": {
    "404": {
      "title": "页面未找到",
      "description": "抱歉，您访问的页面不存在或已被移除。",
      "backHome": "返回首页",
      "goBack": "返回上页"
    },
    "500": {
      "title": "服务器错误",
      "description": "服务器遇到了问题，请稍后再试。",
      "refresh": "刷新页面",
      "backHome": "返回首页"
    },
    "403": {
      "title": "访问受限",
      "description": "抱歉，您没有权限访问此页面。",
      "login": "登录账号",
      "backHome": "返回首页"
    },
    "network": {
      "title": "网络错误",
      "description": "网络连接失败，请检查您的网络设置。",
      "retry": "重试"
    }
  },
  "maintenance": {
    "title": "系统维护中",
    "description": "系统正在进行升级维护，请稍后再试。",
    "estimatedTime": "预计恢复时间",
    "contact": "如有紧急需求，请联系我们"
  }
}
```

### 4.3 管理后台实现

#### 维护模式设置页面

**文件**: `src/pages/Admin/System/index.tsx`

**UI 组件**：
- 维护模式开关（Switch）
- 维护标题输入（中英文）
- 维护说明文本域（中英文）
- 预计恢复时间选择器（DateTimePicker）

---

## 五、文件清单

### 5.1 后端新增文件

| 文件路径 | 说明 |
|---------|------|
| `oc-platform-common/.../dto/MaintenanceConfigDTO.java` | 维护配置 DTO |
| `oc-platform-common/.../dto/MaintenanceStatusDTO.java` | 维护状态 DTO |
| `oc-platform-app/.../interceptor/MaintenanceInterceptor.java` | 维护模式拦截器 |

### 5.2 后端修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `oc-platform-common/.../response/ErrorCode.java` | 添加维护相关错误码 |
| `oc-platform-admin/.../controller/AdminSystemController.java` | 添加维护配置 API |
| `oc-platform-common/.../controller/PublicSystemController.java` | 添加公开维护状态 API |
| `oc-platform-app/.../config/WebMvcConfig.java` | 注册维护拦截器 |
| `sql/init.sql` | 添加维护配置初始化数据 |

### 5.3 前端新增文件

| 文件路径 | 说明 |
|---------|------|
| `src/pages/Error/index.tsx` | 通用错误页面组件 |
| `src/pages/Maintenance/index.tsx` | 维护页面组件 |
| `src/hooks/useMaintenance.ts` | 维护模式 Hook |

### 5.4 前端修改文件

| 文件路径 | 修改内容 |
|---------|---------|
| `src/router/index.tsx` | 添加错误页面和维护页面路由 |
| `src/utils/request.ts` | 更新 HTTP 拦截器 |
| `src/locales/zh-CN.json` | 添加中文翻译 |
| `src/locales/en-US.json` | 添加英文翻译 |
| `src/pages/Admin/System/index.tsx` | 添加维护模式配置 UI |

---

## 六、实施优先级

### 第一阶段：核心错误页面（高优先级）

1. ✅ 增强 404 页面内容和视觉效果
2. ✅ 创建 500 服务器错误页面
3. ✅ 创建 403 权限错误页面
4. ✅ 添加国际化翻译

### 第二阶段：维护模式（中优先级）

1. ✅ 后端维护模式配置和拦截器
2. ✅ 前端维护页面组件
3. ✅ 管理后台维护设置界面

### 第三阶段：优化完善（低优先级）

1. ✅ 网络错误页面
2. ✅ 动画效果优化
3. ✅ 减少动画支持（prefers-reduced-motion）

---

## 七、预交付检查清单

### 视觉质量
- [x] 使用 SVG 图标（Lucide React）
- [x] 图标尺寸一致
- [x] 悬停状态不导致布局位移
- [x] 使用主题颜色

### 交互
- [x] 所有可点击元素有 `cursor-pointer`
- [x] 悬停状态提供清晰反馈
- [x] 过渡时间 150-300ms
- [x] 焦点状态可见

### 深色/浅色模式
- [x] 浅色模式文字对比度足够（4.5:1）
- [x] 边框在两种模式下可见
- [x] 测试两种模式

### 布局
- [x] 响应式适配（375px, 768px, 1024px, 1440px）
- [x] 无水平滚动条

### 可访问性
- [x] 图片有 alt 文本
- [x] 表单输入有标签
- [x] 颜色不是唯一指示器
- [x] 尊重 `prefers-reduced-motion`

---

## 八、预计工作量

| 模块 | 预计文件数 | 复杂度 |
|------|-----------|--------|
| 后端维护模式 | 3 个新增 + 5 个修改 | 中等 |
| 前端错误页面 | 1 个新增 + 1 个修改 | 简单 |
| 前端维护页面 | 2 个新增 + 3 个修改 | 中等 |
| 国际化翻译 | 2 个修改 | 简单 |
| 管理后台 UI | 1 个修改 | 中等 |

**总计**：约 6 个新增文件，12 个修改文件
