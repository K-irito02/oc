---
description: 后端代码规范
scope: project
trigger: always_on
---

# 后端代码规范

## 技术栈版本

| 技术 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.2.12 | 后端框架 |
| Java | 17 (OpenJDK 17.0.15 Temurin) | 运行环境 |
| MyBatis-Plus | 3.5.9 | ORM 框架 |
| Spring Security | 6.2.x | 认证授权 |
| SpringDoc OpenAPI | 2.6.0 | API 文档 |
| PostgreSQL | 15.x | 数据库 |
| Redis | 7.x | 缓存 |

## 静态分析

- **SonarQube**: 代码质量静态分析
  - 代码覆盖率 ≥ 80%
  - 重复率 ≤ 3%
  - 技术债务控制在 A 级
  - 安全热点必须修复

## 代码规范

- **Checkstyle**: 使用 Google Java Style 规范
  - 缩进：2 个空格
  - 行长度：100 字符
  - 导入顺序：static → 第三方 → 项目内
  - 方法长度 ≤ 50 行
  - 类长度 ≤ 500 行

## 代码格式化

- **Spotless**: 自动代码格式化
  - Google Java Format
  - Import 排序和去重
  - 文件末尾换行符
  - 移除未使用的导入

## 依赖安全

- **OWASP Dependency-Check**: 依赖漏洞扫描
  - 构建时自动扫描
  - 高危漏洞必须修复
  - 定期更新依赖版本
  - 维护依赖白名单

## 测试规范

- **JaCoCo**: 测试覆盖率 ≥ 80%
  - 单元测试：JUnit 5 + Mockito
  - 集成测试：@SpringBootTest
  - 测试命名：should_ExpectedBehavior_When_StateUnderTest
  - 测试方法必须是 public void

## 代码审查清单

1. **命名规范**
   - 类名：PascalCase
   - 方法名：camelCase
   - 常量：UPPER_SNAKE_CASE
   - 包名：lowercase

2. **设计原则**
   - 单一职责原则
   - 开闭原则
   - 依赖倒置原则
   - 接口隔离原则

3. **Spring Boot 特定规范**
   - Controller 只处理 HTTP 请求
   - Service 处理业务逻辑
   - Repository 只处理数据访问
   - 使用 @Autowired 构造器注入

4. **异常处理**
   - 自定义业务异常
   - 统一异常处理 @ControllerAdvice
   - 日志记录异常堆栈
   - 返回标准错误格式

## 性能要求

- 数据库查询避免 N+1 问题
- 合理使用缓存 @Cacheable
- 异步处理使用 @Async（阶段一替代消息队列）
- 避免在循环中进行数据库操作

## MyBatis-Plus 配置

- **分页插件**: 必须在 `MybatisPlusConfig` 中启用 `PaginationInnerInterceptor`
  ```java
  @Bean
  public MybatisPlusInterceptor mybatisPlusInterceptor() {
      MybatisPlusInterceptor interceptor = new MybatisPlusInterceptor();
      interceptor.addInnerInterceptor(new PaginationInnerInterceptor(DbType.POSTGRE_SQL));
      return interceptor;
  }
  ```
- **依赖要求**: 需要 `mybatis-plus-jsqlparser` 依赖支持分页
- **注意**: 不启用分页插件会导致 `selectPage` 返回的 `total` 始终为 0

## 模块结构

```
oc-platform/
├── oc-platform-common/     # 公共模块（异常、响应、工具类、配置）
├── oc-platform-user/       # 用户模块（认证、OAuth、用户管理）
├── oc-platform-product/    # 产品模块（产品、版本、分类、下载）
├── oc-platform-comment/    # 评论模块（评论、点赞）
├── oc-platform-file/       # 文件模块（MinIO 存储、上传）
├── oc-platform-admin/      # 管理后台模块
└── oc-platform-app/        # 主应用启动模块
```

## 包命名规范

- 基础包: `com.OcPlatform`
- 模块包: `com.OcPlatform.{module}` (user/product/comment/file/admin/common)

## 环境配置

- **开发端口**: 8081（避免与Apache httpd 8080冲突）
- **数据库**: PostgreSQL 15.x (Docker映射端口5433→5432)
- **缓存**: Redis 7.x (Docker映射端口6380→6379)
- **邮件服务**: QQ邮箱SMTP配置
- **对象存储**: MinIO (端口9000/9001)

## 统一响应格式

```java
public class ApiResponse<T> {
    private int code;
    private String message;
    private T data;
}

public class PageResponse<T> {
    private List<T> records;
    private long total;
    private int page;
    private int size;
}
```

## 安全配置要点

- JWT Access Token 有效期：2小时
- JWT Refresh Token 有效期：7天
- 密码加密：BCrypt (strength=12)
- RBAC 权限：5角色17权限
- CORS 配置：允许 localhost:5173/3000

## 限流策略

| 场景 | 限制 | 实现 |
|------|------|------|
| 登录 | 5次/分钟/IP | Redis incr + expire |
| 注册 | 10次/小时/IP | Redis |
| 验证码 | 1次/分钟/邮箱, 10次/小时/邮箱 | Redis |
| 文件上传 | 50次/小时 | Redis |
| 评论 | 60秒间隔 | Redis |
