# 产品评分功能完善实施计划

## 一、问题分析

### 1.1 当前评分功能现状

| 功能点 | 状态 | 问题描述 |
|--------|------|----------|
| 数据库字段 | ✅ 已有 | `products.rating_average`、`products.rating_count`、`product_comments.rating` |
| 评分存储 | ⚠️ 部分 | 评分存储在评论表中，与评论绑定 |
| 评分计算 | ❌ 缺失 | `CommentService.updateProductRating()` 只打印日志，未真正更新产品表 |
| 模块依赖 | ❌ 问题 | comment 模块无法访问 product 模块的 ProductMapper |
| 前端展示 | ✅ 已有 | 产品列表/详情页显示评分平均值 |
| 评分分布 | ❌ 缺失 | 没有评分分布图（1-5星各多少） |
| 独立评分 | ❌ 缺失 | 用户必须评论才能评分，无法单独评分 |
| 评分历史 | ❌ 缺失 | 用户无法查看自己的评分记录 |
| 国际化 | ⚠️ 部分 | 部分评分相关文案缺少翻译 |

### 1.2 核心问题

1. **评分数据未同步到产品表**：`ProductMapper.updateRating()` 方法存在但从未被调用
2. **跨模块依赖问题**：comment 模块需要调用 product 模块的功能
3. **评分与评论强绑定**：用户无法单独评分，影响评分参与率
4. **评分展示不够直观**：缺少评分分布图和详细统计

## 二、解决方案

### 2.1 方案选择：独立评分系统

创建独立的评分表 `product_ratings`，实现以下功能：
- 支持用户单独评分（无需评论）
- 评论时可附带评分，评分独立存储
- 完整的评分统计和分布展示
- 用户评分历史记录

### 2.2 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                        前端展示层                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │ 产品列表页   │  │ 产品详情页   │  │ 评分组件(新增)      │  │
│  │ 评分展示     │  │ 评分+分布图  │  │ 独立评分+评分历史   │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        API 层                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ RatingController (新增)                              │    │
│  │ - POST   /api/v1/ratings/product/{productId}  提交评分│    │
│  │ - PUT    /api/v1/ratings/{id}                 更新评分│    │
│  │ - DELETE /api/v1/ratings/{id}                 删除评分│    │
│  │ - GET    /api/v1/ratings/product/{productId}/stats 统计│   │
│  │ - GET    /api/v1/ratings/me                   我的评分│   │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        服务层                               │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ RatingService (新增)                                 │    │
│  │ - 创建/更新/删除评分                                  │    │
│  │ - 计算评分统计（平均值、分布）                        │    │
│  │ - 同步更新产品表评分字段                              │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        数据层                               │
│  ┌───────────────────────┐  ┌───────────────────────────┐   │
│  │ product_ratings (新增) │  │ products (已有)           │   │
│  │ - id                  │  │ - rating_average          │   │
│  │ - product_id          │  │ - rating_count            │   │
│  │ - user_id             │  │ - rating_distribution(新增)│   │
│  │ - rating (1-5)        │  └───────────────────────────┘   │
│  │ - created_at          │                                  │
│  │ - updated_at          │                                  │
│  └───────────────────────┘                                  │
└─────────────────────────────────────────────────────────────┘
```

## 三、实施步骤

### 阶段一：数据库层（后端）

#### 1.1 创建评分表迁移脚本
- 文件：`oc-platform/sql/migrations/add_product_ratings.sql`
- 内容：
  ```sql
  CREATE TABLE product_ratings (
      id              BIGSERIAL PRIMARY KEY,
      product_id      BIGINT NOT NULL REFERENCES products(id) ON DELETE CASCADE,
      user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      rating          INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
      created_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
      updated_at      TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(product_id, user_id)  -- 每个用户每个产品只能评分一次
  );
  
  CREATE INDEX idx_ratings_product ON product_ratings(product_id);
  CREATE INDEX idx_ratings_user ON product_ratings(user_id);
  ```

#### 1.2 更新产品表（可选）
- 添加 `rating_distribution` JSONB 字段存储评分分布
- 格式：`{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}`

### 阶段二：后端开发

#### 2.1 创建评分模块（oc-platform-rating 或放在 oc-platform-product 中）

**实体类** `ProductRating.java`
```java
@TableName("product_ratings")
public class ProductRating {
    @TableId(type = IdType.AUTO)
    private Long id;
    private Long productId;
    private Long userId;
    private Integer rating;  // 1-5
    private OffsetDateTime createdAt;
    private OffsetDateTime updatedAt;
}
```

**DTO 类**
- `CreateRatingRequest.java` - 创建评分请求
- `RatingVO.java` - 评分视图对象
- `RatingStatsVO.java` - 评分统计对象（平均值、总数、分布）

**Mapper 层** `ProductRatingMapper.java`
```java
@Mapper
public interface ProductRatingMapper extends BaseMapper<ProductRating> {
    Optional<ProductRating> findByProductAndUser(Long productId, Long userId);
    
    @Select("SELECT AVG(rating) FROM product_ratings WHERE product_id = #{productId}")
    Double getAverageRating(Long productId);
    
    @Select("SELECT COUNT(*) FROM product_ratings WHERE product_id = #{productId}")
    int getRatingCount(Long productId);
    
    @Select("SELECT rating, COUNT(*) as count FROM product_ratings WHERE product_id = #{productId} GROUP BY rating")
    List<Map<String, Object>> getRatingDistribution(Long productId);
}
```

**Service 层** `RatingService.java`
- `createRating()` - 创建评分
- `updateRating()` - 更新评分
- `deleteRating()` - 删除评分
- `getUserRating()` - 获取用户对某产品的评分
- `getRatingStats()` - 获取产品评分统计
- `getUserRatings()` - 获取用户所有评分
- `updateProductRating()` - 同步更新产品表评分字段

**Controller 层** `RatingController.java`
- `POST /api/v1/ratings/product/{productId}` - 提交评分
- `PUT /api/v1/ratings/{id}` - 更新评分
- `DELETE /api/v1/ratings/{id}` - 删除评分
- `GET /api/v1/ratings/product/{productId}/stats` - 获取评分统计
- `GET /api/v1/ratings/product/{productId}/me` - 获取当前用户评分
- `GET /api/v1/ratings/me` - 获取我的评分列表

#### 2.2 修改评论模块

**修改 CommentService.java**
- 创建评论时，如果附带评分，同时创建评分记录
- 删除评论时，如果有关联评分，提示用户是否删除评分

#### 2.3 数据迁移

**迁移脚本** - 将现有评论中的评分迁移到新表
```sql
INSERT INTO product_ratings (product_id, user_id, rating, created_at)
SELECT product_id, user_id, rating, created_at
FROM product_comments
WHERE rating IS NOT NULL AND parent_id IS NULL
ON CONFLICT (product_id, user_id) DO NOTHING;
```

### 阶段三：前端开发

#### 3.1 创建评分组件

**RatingStats 组件** `src/components/RatingStats/index.tsx`
- 显示平均评分（大号星级）
- 评分分布条形图（1-5星各占比例）
- 评分总数

**RatingInput 组件** `src/components/RatingInput/index.tsx`
- 可交互的星级评分输入
- 支持半星（可选）
- 显示当前用户评分状态

#### 3.2 修改产品详情页

**ProductDetail/index.tsx**
- 添加评分统计区域（评分分布图）
- 添加独立评分功能（用户可单独评分）
- 显示当前用户评分状态
- 支持修改/删除评分

#### 3.3 添加 API 调用

**api.ts**
```typescript
export const ratingApi = {
  create: (productId: number, rating: number) => 
    request.post(`/ratings/product/${productId}`, { rating }),
  update: (id: number, rating: number) => 
    request.put(`/ratings/${id}`, { rating }),
  delete: (id: number) => 
    request.delete(`/ratings/${id}`),
  getStats: (productId: number) => 
    request.get(`/ratings/product/${productId}/stats`),
  getMyRating: (productId: number) => 
    request.get(`/ratings/product/${productId}/me`),
  getMyRatings: (params: { page?: number; size?: number }) => 
    request.get('/ratings/me', { params }),
};
```

#### 3.4 国际化支持

**zh-CN.json / en-US.json**
```json
{
  "rating": {
    "title": "评分",
    "submitRating": "提交评分",
    "updateRating": "修改评分",
    "deleteRating": "删除评分",
    "myRating": "我的评分",
    "ratingSubmitted": "评分已提交",
    "ratingUpdated": "评分已更新",
    "ratingDeleted": "评分已删除",
    "loginToRate": "请登录后评分",
    "alreadyRated": "您已评分",
    "distribution": "评分分布",
    "stars": "{{count}} 星",
    "ratings": "{{count}} 条评分",
    "averageRating": "平均评分",
    "noRatings": "暂无评分",
    "beFirstToRate": "成为第一个评分者",
    "myRatings": "我的评分记录",
    "confirmDelete": "确认删除评分？",
    "cannotUndo": "此操作不可撤销"
  }
}
```

### 阶段四：测试与验证

#### 4.1 单元测试
- RatingService 测试
- 评分计算逻辑测试
- 边界条件测试

#### 4.2 集成测试
- API 接口测试
- 前后端联调测试

#### 4.3 数据验证
- 验证评分统计正确性
- 验证评分分布正确性
- 验证产品表评分字段同步

## 四、文件清单

### 4.1 新增文件

| 文件路径 | 说明 |
|----------|------|
| `sql/migrations/add_product_ratings.sql` | 数据库迁移脚本 |
| `oc-platform-product/src/main/java/com/ocplatform/product/entity/ProductRating.java` | 评分实体类 |
| `oc-platform-product/src/main/java/com/ocplatform/product/dto/CreateRatingRequest.java` | 创建评分请求 |
| `oc-platform-product/src/main/java/com/ocplatform/product/dto/RatingVO.java` | 评分视图对象 |
| `oc-platform-product/src/main/java/com/ocplatform/product/dto/RatingStatsVO.java` | 评分统计对象 |
| `oc-platform-product/src/main/java/com/ocplatform/product/repository/ProductRatingMapper.java` | 评分 Mapper |
| `oc-platform-product/src/main/java/com/ocplatform/product/service/RatingService.java` | 评分服务 |
| `oc-platform-product/src/main/java/com/ocplatform/product/controller/RatingController.java` | 评分控制器 |
| `oc-platform-web/src/components/RatingStats/index.tsx` | 评分统计组件 |
| `oc-platform-web/src/components/RatingInput/index.tsx` | 评分输入组件 |

### 4.2 修改文件

| 文件路径 | 修改内容 |
|----------|----------|
| `sql/init.sql` | 添加 product_ratings 表定义 |
| `oc-platform-product/src/main/java/com/ocplatform/product/entity/Product.java` | 添加 ratingDistribution 字段（可选） |
| `oc-platform-product/src/main/java/com/ocplatform/product/dto/ProductVO.java` | 添加评分分布字段 |
| `oc-platform-product/src/main/java/com/ocplatform/product/repository/ProductMapper.java` | 添加更新评分分布方法 |
| `oc-platform-comment/src/main/java/com/ocplatform/comment/service/CommentService.java` | 修改评论评分关联逻辑 |
| `oc-platform-web/src/utils/api.ts` | 添加评分 API |
| `oc-platform-web/src/pages/ProductDetail/index.tsx` | 添加评分统计和独立评分功能 |
| `oc-platform-web/src/locales/zh-CN.json` | 添加评分相关翻译 |
| `oc-platform-web/src/locales/en-US.json` | 添加评分相关翻译 |

## 五、注意事项

1. **数据迁移**：需要将现有评论中的评分数据迁移到新表
2. **向后兼容**：保持评论评分功能，但评分独立存储
3. **性能优化**：评分统计可考虑缓存
4. **权限控制**：用户只能修改/删除自己的评分
5. **唯一约束**：每个用户每个产品只能评分一次

## 六、预估工作量

| 阶段 | 预估时间 |
|------|----------|
| 数据库层 | 0.5 小时 |
| 后端开发 | 2 小时 |
| 前端开发 | 2 小时 |
| 测试验证 | 1 小时 |
| **总计** | **5.5 小时** |
