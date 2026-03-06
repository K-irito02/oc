---
description: 前端代码规范
scope: project
trigger: always_on
---

# 前端代码规范

## 技术栈版本

| 技术 | 版本 | 说明 |
|------|------|------|
| React | 18.3.1 | UI 框架 |
| TypeScript | ~5.6.2 | 类型安全 |
| Vite | 5.4.10 | 构建工具 |
| Ant Design | 6.3.0 | UI 组件库 |
| Redux Toolkit | 2.11.2 | 状态管理 |
| React Router DOM | 7.13.0 | 路由 |
| react-i18next | 16.5.4 | 国际化 |
| Tailwind CSS | 3.4.1 | 样式框架 |

## 代码规范

- **ESLint**: 使用 typescript-eslint 推荐规则集
  - 配置文件：`eslint.config.js` (Flat Config 格式)
  - 扩展配置：`@eslint/js` recommended + `typescript-eslint` recommended
  - React Hooks 规则：`eslint-plugin-react-hooks` recommended
  - React Refresh：`eslint-plugin-react-refresh` 热更新组件导出检查
  - ECMAScript 版本：2020

### 关键 ESLint 规则

| 规则 | 级别 | 说明 |
|------|------|------|
| `@typescript-eslint/no-explicit-any` | error | 禁止使用 `any` 类型，必须定义明确的接口/类型 |
| `@typescript-eslint/no-unused-vars` | error | 禁止未使用的变量，catch 块可用 `_` 忽略 |
| `react-hooks/rules-of-hooks` | error | 确保 Hooks 在顶层调用 |
| `react-hooks/exhaustive-deps` | warn | useEffect/useCallback 依赖数组检查 |
| `prefer-const` | error | 优先使用 const 声明不重新赋值的变量 |
| `react-refresh/only-export-components` | warn | 组件文件只导出组件（允许常量导出） |

### 类型定义最佳实践

```typescript
// ✅ 正确：定义明确的接口
interface UserRecord {
  id: number;
  username: string;
  email: string;
  status: string;
}

interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}

interface PaginatedResponse<T> {
  records: T[];
  total: number;
  page: number;
  size: number;
}

// ✅ 正确：API 调用使用类型断言
const res = await api.getUsers() as ApiResponse<PaginatedResponse<UserRecord>>;

// ❌ 错误：使用 any 类型
const res: any = await api.getUsers();
```

### React Hooks 依赖处理

```typescript
// ✅ 方式一：将函数包装为 useCallback 并添加到依赖数组
const loadData = useCallback(async () => {
  // ...
}, [dependency1, dependency2]);

useEffect(() => { loadData(); }, [loadData]);

// ✅ 方式二：使用 eslint-disable 注释（函数稳定时）
useEffect(() => {
  loadData();
}, [id]); // eslint-disable-line react-hooks/exhaustive-deps
```

### 错误处理最佳实践

```typescript
// ✅ 正确：不使用 catch 参数时省略
try {
  await api.delete(id);
} catch { /* handled */ }

// ✅ 正确：需要使用错误信息时定义类型
try {
  await api.submit(data);
} catch (error: unknown) {
  const err = error as { response?: { data?: { message?: string } } };
  message.error(err?.response?.data?.message || 'Operation failed');
}
```

## 代码格式化

- **Prettier**: 统一代码格式
  - 单行长度：100 字符
  - 使用单引号
  - 尾部分号：不添加
  - 对象尾随逗号：ES5 兼容
  - JSX 括号：多行时添加

## 类型检查

- **TypeScript**: strict mode 严格模式
  - 启用所有严格检查
  - 禁止隐式 `any`（通过 ESLint `@typescript-eslint/no-explicit-any` 强制）
  - 禁止未使用的变量（通过 ESLint `@typescript-eslint/no-unused-vars` 强制）
  - 严格的 null 检查
  - 为 API 响应定义明确的接口类型

## 提交检查

- **Husky + lint-staged**: 提交前检查
  - ESLint 自动修复
  - Prettier 格式化
  - TypeScript 类型检查
  - 测试通过检查
  - 提交信息规范检查

## 提交规范

- **Conventional Commits**: 标准化提交信息
  ```
  <type>[optional scope]: <description>
  
  [optional body]
  
  [optional footer(s)]
  ```
  
  **类型说明：**
  - `feat`: 新功能
  - `fix`: 修复 bug
  - `docs`: 文档更新
  - `style`: 代码格式调整
  - `refactor`: 重构
  - `test`: 测试相关
  - `chore`: 构建或辅助工具变动
  - `perf`: 性能优化
  - `ci`: CI/CD 相关

## 组件规范

1. **命名规范**
   - 组件文件：PascalCase.tsx
   - 组件名：PascalCase
   - Props 接口：ComponentNameProps
   - 常量：UPPER_SNAKE_CASE
   - 变量/函数：camelCase

2. **文件结构**
   ```
   ComponentName/
   ├── index.tsx          // 组件主文件
   ├── ComponentName.tsx  // 组件实现
   ├── ComponentName.styles.ts // 样式文件
   ├── ComponentName.test.tsx  // 测试文件
   └── types.ts           // 类型定义
   ```

3. **React Hooks 规范**
   - Hook 名以 use 开头
   - 自定义 Hook 放在 hooks/ 目录
   - 遵循 Hooks 使用规则
   - 合理使用依赖数组

4. **状态管理**
   - Redux Toolkit 标准模式
   - 异步操作使用 createAsyncThunk
   - 正常化数据结构
   - 避免直接修改 state

## 性能优化

- 使用 React.memo 防止不必要重渲染
- 合理使用 useMemo 和 useCallback
- 代码分割和懒加载
- 图片优化和压缩
- Bundle 分析和优化

## 样式规范

- Tailwind CSS 实用类优先
- Ant Design Token 统一主题变量
- Glassmorphism 玻璃拟态风格
- CSS 变量控制动态主题
- 响应式设计原则
- 移动端优先适配
- 避免内联样式

## 测试规范

- Jest + React Testing Library
- 单元测试覆盖率 ≥ 80%
- 集成测试关键用户流程
- 快照测试 UI 组件
- 可访问性测试

## 环境配置

- **开发端口**: 5173（可能自动切换到5174）
- **后端API**: http://localhost:8081/api/v1
- **构建工具**: Vite 5.4.10
- **代理配置**: Vite代理 /api → http://localhost:8081

## 目录结构

```
src/
├── main.tsx              # 入口
├── App.tsx               # 根组件
├── index.css             # 全局 CSS (Tailwind + Glassmorphism)
├── components/           # 共享组件
│   ├── ui/               # 基础 UI 组件
│   ├── layout/           # 布局组件
│   ├── AvatarUpload/     # 头像上传
│   ├── ThemeProvider.tsx # 主题上下文
│   └── DynamicBackground.tsx # 动态背景
├── layouts/              # 页面布局
├── locales/              # 国际化
├── pages/                # 页面组件
├── router/               # 路由配置
├── store/                # Redux 状态管理
├── theme/                # Ant Design 主题
└── utils/                # API 封装 + Axios 实例
```

## Glassmorphism 主题系统

### CSS 变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `--glass-opacity` | 玻璃层不透明度 | `0.7` |
| `--glass-blur` | 背景模糊度 | `12px` |
| `--glass-border-opacity` | 边框不透明度 | `0.2` |
| `--primary-color` | 主色调 (RGB) | `59 130 246` |
| `--font-family` | 全局字体 | `Inter` |

### 核心组件类

| 组件 | 类名组合 |
|------|----------|
| **Glass Card** | `bg-white/var(--glass-opacity) backdrop-blur-[var(--glass-blur)] border border-white/var(--glass-border-opacity) shadow-xl` |
| **Glass Button** | `bg-primary/90 hover:bg-primary text-white shadow-lg backdrop-blur-sm` |
| **Glass Input** | `bg-white/50 border-white/30 focus:ring-2 focus:ring-primary/50` |
