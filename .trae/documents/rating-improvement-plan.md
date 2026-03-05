# 评分功能改进计划

## 问题分析

### 当前存在的问题

项目中存在**两套评分系统**，导致语义混淆：

| 评分类型 | 存储位置 | 当前显示 | 问题 |
|---------|---------|---------|------|
| 产品评分 | `product_ratings` 表 | "评分" | 独立评分系统，用户对产品的整体评价 |
| 评论评分 | `product_comments.rating` 字段 | "评分" | 评论附带的评分，用户分享使用体验时的评分 |

**核心问题**：
1. 两种评分在界面上都显示为"评分"，用户无法区分
2. 评论中的评分会更新产品的评分统计，与独立评分系统混淆
3. 评分统计逻辑不清晰，数据来源混乱

### 用户需求

1. 评论表单中的评分 → 改名为"**体验评分**"（用户分享使用体验时的评分）
2. 独立评分系统 → 改名为"**产品评分**"（用户对产品的整体评价）
3. 评论中的"体验评分"**不应该**统计到"产品评分"中

---

## 解决方案

### 设计原则

1. **语义清晰**：两种评分有明确的区分和用途
2. **数据独立**：两套评分系统独立统计，互不影响
3. **向后兼容**：保留现有数据，平滑迁移
4. **国际化支持**：中英文翻译完整

### 评分定义

| 评分类型 | 英文名称 | 用途说明 |
|---------|---------|---------|
| 产品评分 | Product Rating | 用户对产品的整体评价，独立于评论系统 |
| 体验评分 | Experience Rating | 用户分享使用体验时给出的评分，附属于评论 |

---

## 实施步骤

### 第一阶段：数据库变更

#### 1.1 产品表新增体验评分字段

在 `products` 表中新增字段，用于存储体验评分统计：

```sql
-- 新增体验评分统计字段
ALTER TABLE products 
ADD COLUMN experience_rating_average DECIMAL(2,1) DEFAULT 0.0,
ADD COLUMN experience_rating_count INTEGER DEFAULT 0,
ADD COLUMN experience_rating_distribution JSONB DEFAULT '{"1":0,"2":0,"3":0,"4":0,"5":0}';

-- 添加注释
COMMENT ON COLUMN products.experience_rating_average IS '体验评分平均值(来自评论)';
COMMENT ON COLUMN products.experience_rating_count IS '体验评分总数(来自评论)';
COMMENT ON COLUMN products.experience_rating_distribution IS '体验评分分布(来自评论)';
```

#### 1.2 评论表字段重命名（可选）

如果需要更清晰的语义，可以将 `rating` 字段重命名为 `experience_rating`：

```sql
-- 重命名字段（可选，保持向后兼容可以不改）
ALTER TABLE product_comments RENAME COLUMN rating TO experience_rating;
```

> **建议**：保持字段名不变，通过注释和代码层面区分，减少迁移风险。

#### 1.3 数据迁移

将现有评论评分数据迁移到体验评分统计：

```sql
-- 迁移现有评论评分到体验评分统计
UPDATE products p
SET 
    experience_rating_average = COALESCE(stats.avg_rating, 0.0),
    experience_rating_count = COALESCE(stats.total_count, 0),
    experience_rating_distribution = COALESCE(stats.distribution, '{"1":0,"2":0,"3":0,"4":0,"5":0}'::jsonb)
FROM (
    SELECT 
        product_id,
        AVG(rating) as avg_rating,
        COUNT(*) as total_count,
        jsonb_object_agg(
            rating::text, 
            count
        ) as distribution
    FROM (
        SELECT 
            product_id,
            rating,
            COUNT(*) as count
        FROM product_comments
        WHERE rating IS NOT NULL 
          AND status = 'PUBLISHED' 
          AND parent_id IS NULL
        GROUP BY product_id, rating
    ) sub
    GROUP BY product_id
) stats
WHERE p.id = stats.product_id;

-- 重置产品评分统计（仅来自 product_ratings 表）
UPDATE products p
SET 
    rating_average = COALESCE(ratings.avg_rating, 0.0),
    rating_count = COALESCE(ratings.total_count, 0),
    rating_distribution = COALESCE(ratings.distribution, '{"1":0,"2":0,"3":0,"4":0,"5":0}'::jsonb)
FROM (
    SELECT 
        product_id,
        AVG(rating) as avg_rating,
        COUNT(*) as total_count,
        jsonb_object_agg(
            rating::text, 
            count
        ) as distribution
    FROM (
        SELECT 
            product_id,
            rating,
            COUNT(*) as count
        FROM product_ratings
        GROUP BY product_id, rating
    ) sub
    GROUP BY product_id
) ratings
WHERE p.id = ratings.product_id;
```

---

### 第二阶段：后端代码变更

#### 2.1 产品实体类更新

文件：`oc-platform-product/src/main/java/com/ocplatform/product/entity/Product.java`

新增体验评分字段：

```java
// 产品评分（来自 product_ratings 表）
private BigDecimal ratingAverage;
private Integer ratingCount;
private Map<String, Integer> ratingDistribution;

// 体验评分（来自 product_comments 表）
private BigDecimal experienceRatingAverage;
private Integer experienceRatingCount;
private Map<String, Integer> experienceRatingDistribution;
```

#### 2.2 评论服务更新

文件：`oc-platform-comment/src/main/java/com/ocplatform/comment/service/CommentService.java`

修改 `updateProductRatingStats` 方法，更新体验评分统计而非产品评分：

```java
private void updateProductRatingStats(Long productId) {
    // 计算体验评分统计（来自评论）
    Double avgRating = commentMapper.getAverageRating(productId);
    int totalCount = commentMapper.getRatingCount(productId);
    List<Map<String, Object>> distributionList = commentMapper.getRatingDistribution(productId);
    
    // 构建分布 JSON
    Map<String, Integer> distribution = new HashMap<>();
    distribution.put("1", 0);
    distribution.put("2", 0);
    distribution.put("3", 0);
    distribution.put("4", 0);
    distribution.put("5", 0);
    for (Map<String, Object> item : distributionList) {
        Integer rating = (Integer) item.get("rating");
        Long count = (Long) item.get("count");
        distribution.put(String.valueOf(rating), count.intValue());
    }
    
    BigDecimal avg = avgRating != null ? BigDecimal.valueOf(avgRating).setScale(1, RoundingMode.HALF_UP) : BigDecimal.ZERO;
    String distributionJson;
    try {
        distributionJson = new ObjectMapper().writeValueAsString(distribution);
    } catch (JsonProcessingException e) {
        distributionJson = "{\"1\":0,\"2\":0,\"3\":0,\"4\":0,\"5\":0}";
    }
    
    // 更新产品的体验评分统计
    commentMapper.updateProductExperienceRatingStats(productId, avg, totalCount, distributionJson);
}
```

#### 2.3 新增 Mapper 方法

文件：`oc-platform-comment/src/main/java/com/ocplatform/comment/repository/ProductCommentMapper.java`

```java
@Update("UPDATE products SET experience_rating_average = #{avg}, experience_rating_count = #{count}, experience_rating_distribution = #{distribution}::jsonb WHERE id = #{productId}")
void updateProductExperienceRatingStats(@Param("productId") Long productId, @Param("avg") BigDecimal avg, @Param("count") int count, @Param("distribution") String distribution);
```

#### 2.4 产品 DTO 更新

文件：`oc-platform-product/src/main/java/com/ocplatform/product/dto/ProductVO.java`

新增体验评分字段：

```java
// 产品评分
private BigDecimal ratingAverage;
private Integer ratingCount;

// 体验评分
private BigDecimal experienceRatingAverage;
private Integer experienceRatingCount;
```

#### 2.5 新增体验评分统计 API

在产品控制器中新增获取体验评分统计的接口：

```java
@GetMapping("/{id}/experience-rating-stats")
public ApiResponse<ExperienceRatingStatsVO> getExperienceRatingStats(@PathVariable Long id) {
    return ApiResponse.success(productService.getExperienceRatingStats(id));
}
```

---

### 第三阶段：前端代码变更

#### 3.1 国际化文件更新

文件：`oc-platform-web/src/locales/zh-CN.json`

```json
{
  "rating": {
    "title": "产品评分",
    "submitRating": "提交产品评分",
    "myRating": "我的产品评分",
    "ratings": "{{count}} 条产品评分",
    "averageRating": "平均产品评分"
  },
  "experienceRating": {
    "title": "体验评分",
    "submitRating": "提交体验评分",
    "myRating": "我的体验评分",
    "ratings": "{{count}} 条体验评分",
    "averageRating": "平均体验评分"
  },
  "productDetail": {
    "rating": "体验评分",
    "productRating": "产品评分",
    "experienceRating": "体验评分"
  }
}
```

文件：`oc-platform-web/src/locales/en-US.json`

```json
{
  "rating": {
    "title": "Product Rating",
    "submitRating": "Rate Product",
    "myRating": "My Product Rating",
    "ratings": "{{count}} product rating(s)",
    "averageRating": "Average Product Rating"
  },
  "experienceRating": {
    "title": "Experience Rating",
    "submitRating": "Rate Experience",
    "myRating": "My Experience Rating",
    "ratings": "{{count}} experience rating(s)",
    "averageRating": "Average Experience Rating"
  },
  "productDetail": {
    "rating": "Experience Rating",
    "productRating": "Product Rating",
    "experienceRating": "Experience Rating"
  }
}
```

#### 3.2 评论表单组件更新

文件：`oc-platform-web/src/pages/ProductDetail/index.tsx`

修改评论表单中的评分标签：

```tsx
// 修改前
<Form.Item name="rating" label={t('productDetail.rating')} initialValue={5}>
  <Rate />
</Form.Item>

// 修改后
<Form.Item name="rating" label={t('productDetail.experienceRating')} initialValue={5}>
  <Rate />
</Form.Item>
```

修改评论列表中的评分显示：

```tsx
// 评论项中的评分显示
{comment.rating && (
  <div className="flex items-center gap-1">
    <span className="text-xs text-slate-500">{t('productDetail.experienceRating')}:</span>
    <Rate disabled defaultValue={comment.rating} className="text-xs" style={{ fontSize: 10 }} />
  </div>
)}
```

#### 3.3 RatingStats 组件更新

文件：`oc-platform-web/src/components/RatingStats/index.tsx`

添加 `type` 属性区分产品评分和体验评分：

```tsx
type RatingStatsProps = {
  type?: 'product' | 'experience';  // 新增类型属性
  averageRating: number;
  totalRatings: number;
  distribution: Record<number, number>;
  userRating?: number | null;
  onRate?: (rating: number) => void;
  isAuthenticated?: boolean;
  showInput?: boolean;
};

export default function RatingStats({
  type = 'product',  // 默认为产品评分
  averageRating,
  totalRatings,
  distribution,
  userRating,
  onRate,
  isAuthenticated = false,
  showInput = true,
}: RatingStatsProps) {
  const { t } = useTranslation();
  
  // 根据类型选择翻译键
  const prefix = type === 'product' ? 'rating' : 'experienceRating';
  
  return (
    <div className="space-y-6">
      <div className="flex items-start gap-6">
        {/* ... */}
        <div className="text-sm text-slate-500 dark:text-slate-400 mt-1">
          {t(`${prefix}.ratings`, { count: totalRatings })}
        </div>
      </div>
      
      {showInput && (
        <div className="border-t border-slate-200 dark:border-slate-700 pt-4">
          {isAuthenticated ? (
            <div className="flex items-center gap-4">
              <span className="text-sm text-slate-600 dark:text-slate-400">
                {userRating ? t(`${prefix}.myRating`) : t(`${prefix}.submitRating`)}:
              </span>
              {/* ... */}
            </div>
          ) : (
            <div className="text-center text-sm text-slate-500 dark:text-slate-400">
              <Star size={14} className="inline mr-1 text-amber-400" />
              {t(`${prefix}.loginToRate`)}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

#### 3.4 产品详情页更新

文件：`oc-platform-web/src/pages/ProductDetail/index.tsx`

分别显示产品评分和体验评分：

```tsx
{/* 产品评分卡片 */}
<Card title={
  <span>
    <Star size={16} className="inline mr-1 text-amber-400" />
    {t('productDetail.productRating')}
  </span>
}>
  <RatingStats
    type="product"
    averageRating={ratingStats.averageRating}
    totalRatings={ratingStats.totalRatings}
    distribution={ratingStats.distribution}
    userRating={ratingStats.userRating}
    onRate={handleRate}
  />
</Card>

{/* 体验评分统计（可选，在评论区域显示） */}
<div className="flex items-center gap-2 mb-4">
  <Star size={16} className="text-amber-400" />
  <span className="text-sm font-medium">{t('productDetail.experienceRating')}</span>
  <span className="text-lg font-bold">{(product.experienceRatingAverage ?? 0).toFixed(1)}</span>
  <span className="text-sm text-slate-500">
    ({product.experienceRatingCount ?? 0} {t('experienceRating.ratings', { count: product.experienceRatingCount ?? 0 })})
  </span>
</div>
```

#### 3.5 API 更新

文件：`oc-platform-web/src/utils/api.ts`

新增获取体验评分统计的 API：

```typescript
export const productApi = {
  // ... 现有方法
  
  // 获取体验评分统计
  getExperienceRatingStats: (productId: number) =>
    request.get(`/products/${productId}/experience-rating-stats`),
};
```

---

### 第四阶段：测试与验证

#### 4.1 数据迁移验证

1. 检查产品表的体验评分字段是否正确填充
2. 验证产品评分统计是否仅来自 `product_ratings` 表
3. 确认评论评分不再影响产品评分统计

#### 4.2 功能测试

1. **产品评分测试**
   - 用户提交产品评分，验证 `product_ratings` 表数据
   - 验证产品评分统计正确更新
   - 验证评分分布正确计算

2. **体验评分测试**
   - 用户提交评论附带评分，验证 `product_comments` 表数据
   - 验证体验评分统计正确更新
   - 验证体验评分不影响产品评分统计

3. **界面显示测试**
   - 验证产品评分卡片显示正确
   - 验证评论表单显示"体验评分"
   - 验证评论列表显示"体验评分"
   - 验证中英文切换正常

---

## 文件变更清单

### 数据库文件

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `sql/migrations/add_experience_rating.sql` | 新增 | 体验评分迁移脚本 |

### 后端文件

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `oc-platform-product/src/main/java/.../entity/Product.java` | 修改 | 新增体验评分字段 |
| `oc-platform-product/src/main/java/.../dto/ProductVO.java` | 修改 | 新增体验评分字段 |
| `oc-platform-product/src/main/java/.../dto/ExperienceRatingStatsVO.java` | 新增 | 体验评分统计 VO |
| `oc-platform-product/src/main/java/.../controller/ProductController.java` | 修改 | 新增体验评分统计 API |
| `oc-platform-product/src/main/java/.../service/ProductService.java` | 修改 | 新增体验评分统计方法 |
| `oc-platform-comment/src/main/java/.../service/CommentService.java` | 修改 | 更新体验评分统计逻辑 |
| `oc-platform-comment/src/main/java/.../repository/ProductCommentMapper.java` | 修改 | 新增更新体验评分方法 |

### 前端文件

| 文件 | 变更类型 | 说明 |
|------|---------|------|
| `oc-platform-web/src/locales/zh-CN.json` | 修改 | 新增体验评分翻译 |
| `oc-platform-web/src/locales/en-US.json` | 修改 | 新增体验评分翻译 |
| `oc-platform-web/src/components/RatingStats/index.tsx` | 修改 | 支持两种评分类型 |
| `oc-platform-web/src/pages/ProductDetail/index.tsx` | 修改 | 区分显示两种评分 |
| `oc-platform-web/src/utils/api.ts` | 修改 | 新增体验评分 API |

---

## 风险评估

### 低风险

- 数据库字段新增：不影响现有数据
- 国际化文件更新：纯文本变更
- 前端组件更新：界面显示调整

### 中等风险

- 评论服务逻辑修改：需要仔细测试评分统计更新
- 数据迁移脚本：需要在测试环境验证

### 缓解措施

1. 在测试环境完整测试后再部署生产环境
2. 保留原有评分数据，支持回滚
3. 分阶段部署，逐步验证

---

## 时间估算

| 阶段 | 预计时间 |
|------|---------|
| 数据库变更 | 0.5 小时 |
| 后端代码变更 | 2 小时 |
| 前端代码变更 | 1.5 小时 |
| 测试验证 | 1 小时 |
| **总计** | **5 小时** |
