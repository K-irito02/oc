# 修复管理后台创建产品失败问题

## 问题分析

### 错误现象
后端日志显示 JSON 反序列化错误：
```
Cannot deserialize value of type `java.util.ArrayList<java.lang.String>` from Object value (token `JsonToken.START_OBJECT`)
```

### 根本原因
1. **数据库定义**: `rating_distribution` 字段定义为 `JSONB DEFAULT '{"1":0,"2":0,"3":0,"4":0,"5":0}'`，这是一个 JSON 对象（Map 结构）
2. **类型处理器问题**: 现有的 `JsonbTypeHandler` 只能处理 `List<String>` 类型
3. **实体类冲突**: `Product` 实体类中 `ratingDistribution` 字段类型是 `Map<String, Integer>`，但使用了 `JsonbTypeHandler`
4. **反序列化失败**: 当 MyBatis 读取产品数据时，尝试将 JSON 对象反序列化为 List，导致类型不匹配错误

## 解决方案

### 方案概述
创建一个新的 `JsonbMapTypeHandler` 类来处理 `Map<String, Integer>` 类型，并在 `Product` 实体类中使用这个新的处理器。

## 实施步骤

### 步骤 1: 创建 JsonbMapTypeHandler 类
- 路径: `e:\oc\oc-platform\oc-platform-common\src\main\java\com\ocplatform\common\handler\JsonbMapTypeHandler.java`
- 功能: 处理 `Map<String, Integer>` 类型的 JSONB 字段

### 步骤 2: 修改 Product 实体类
- 路径: `e:\oc\oc-platform\oc-platform-product\src\main\java\com\ocplatform\product\entity\Product.java`
- 修改: 将 `ratingDistribution` 字段的 `typeHandler` 改为 `JsonbMapTypeHandler.class`

### 步骤 3: 重新编译后端
- 执行 Maven 编译命令

### 步骤 4: 测试验证
- 使用 Playwright 测试创建产品功能
- 使用 Playwright 测试编辑产品功能

## 测试计划

### 测试场景
1. **创建产品测试**
   - 登录管理后台
   - 进入产品管理页面
   - 点击新建产品
   - 填写基本信息（名称、标识、分类、描述等）
   - 上传图标
   - 添加版本
   - 点击创建产品按钮
   - 验证创建成功

2. **编辑产品测试**
   - 进入已有产品编辑页面
   - 修改产品信息
   - 保存更改
   - 验证保存成功

## 涉及文件

| 文件 | 操作 |
|------|------|
| `oc-platform-common/src/main/java/com/ocplatform/common/handler/JsonbMapTypeHandler.java` | 新建 |
| `oc-platform-product/src/main/java/com/ocplatform/product/entity/Product.java` | 修改 |

## 风险评估
- **风险等级**: 低
- **影响范围**: 仅影响 `rating_distribution` 字段的读写
- **回滚方案**: 恢复原有代码即可
