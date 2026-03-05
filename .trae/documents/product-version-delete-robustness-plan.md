# 产品管理版本删除健壮性优化计划

## 问题分析

### 当前问题
在管理后台的产品管理中存在以下健壮性问题：

1. **编辑模式下的版本删除问题**：
   - 用户可以删除已发布版本，即使这是最后一个已发布版本
   - 删除后产品状态仍为 `PUBLISHED`，但实际没有可下载的版本
   - 退出编辑页面时没有验证产品状态与版本的一致性

2. **新建产品模式**：
   - 已有验证逻辑，但可以进一步优化用户体验

### 当前代码状态

**前端 (ProductEdit.tsx)**：
- ✅ 新建模式有 `validateAllFields` 验证版本和状态
- ✅ 编辑模式有 `validatePublishStatus` 验证状态转换
- ✅ 有 `hasUnsavedChanges` 和 `safeNavigate` 处理未保存更改
- ❌ 编辑模式下删除版本后没有验证产品状态一致性
- ❌ 退出时没有验证 PUBLISHED 产品是否有已发布版本

**后端 (ProductService.java / VersionService.java)**：
- ✅ 状态转换有 `validateStatusTransition` 验证
- ❌ 删除版本时没有检查是否影响产品状态
- ❌ 没有自动处理"最后一个已发布版本被删除"的情况

## 解决方案

### 方案设计

采用**前端预防 + 后端兜底**的双重保障策略：

1. **前端预防**：
   - 删除版本前检查并警告
   - 退出页面时验证产品状态一致性
   - 状态选择时实时验证

2. **后端兜底**：
   - 删除版本时检查产品状态
   - 必要时自动调整产品状态或拒绝删除

### 详细实施步骤

---

## 第一步：前端 - 删除版本前的验证和警告

### 1.1 编辑模式 - 删除已发布版本验证

在 `handleDeleteVersion` 函数中添加验证逻辑：

```typescript
// 检查是否是最后一个已发布版本
const handleDeleteVersion = async (versionId: number) => {
  const version = versions.find(v => v.id === versionId);
  const publishedCount = versions.filter(v => v.status === 'PUBLISHED').length;
  const productStatus = product?.status || form.getFieldValue('status');
  
  // 如果删除的是已发布版本，且是最后一个
  if (version?.status === 'PUBLISHED' && publishedCount === 1) {
    Modal.confirm({
      title: t('productEdit.deleteLastPublishedVersion'),
      content: productStatus === 'PUBLISHED' 
        ? t('productEdit.deleteLastPublishedVersionWarning')
        : t('productEdit.deleteLastPublishedVersionInfo'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      onOk: async () => {
        // 执行删除
      }
    });
    return;
  }
  
  // 正常删除流程
};
```

### 1.2 新建模式 - 删除临时版本验证

在 `handleDeletePendingVersion` 函数中添加类似验证。

---

## 第二步：前端 - 退出页面时的状态验证

### 2.1 增强安全导航函数

修改 `safeNavigate` 函数，在退出前验证产品状态：

```typescript
const safeNavigate = useCallback((path: string) => {
  // 先检查状态一致性
  const statusError = validateProductStatusConsistency();
  
  if (statusError) {
    Modal.warning({
      title: t('productEdit.statusInconsistent'),
      content: statusError,
      okText: t('productEdit.goToFix'),
      onOk: () => {
        // 跳转到版本管理标签页
        setActiveTab('versions');
      }
    });
    return;
  }
  
  // 原有的未保存更改检查
  if (hasUnsavedChanges) {
    Modal.confirm({
      title: t('productEdit.unsavedChanges'),
      content: t('productEdit.unsavedChangesContent'),
      okText: t('productEdit.leave'),
      cancelText: t('productEdit.stay'),
      onOk: () => navigate(path),
    });
  } else {
    navigate(path);
  }
}, [hasUnsavedChanges, navigate, t, versions, product]);
```

### 2.2 添加状态一致性验证函数

```typescript
const validateProductStatusConsistency = (): string | null => {
  const status = product?.status || form.getFieldValue('status');
  const publishedCount = versions.filter(v => v.status === 'PUBLISHED').length;
  
  if (status === 'PUBLISHED' && publishedCount === 0) {
    return t('productEdit.publishedButNoVersion');
  }
  
  return null;
};
```

---

## 第三步：前端 - 状态选择实时验证

### 3.1 状态下拉框添加验证

在状态选择的 `Select` 组件添加 `onSelect` 事件：

```typescript
<Form.Item name="status" label={t('admin.status')} ...>
  <Select onSelect={handleStatusSelect}>
    ...
  </Select>
</Form.Item>

const handleStatusSelect = (value: string) => {
  const currentStatus = product?.status || 'DRAFT';
  const versionList = isNewProduct ? pendingVersions : versions;
  const error = validatePublishStatus(currentStatus, value, versionList);
  
  if (error) {
    Modal.warning({
      title: t('productEdit.validation.title'),
      content: error,
    });
    // 恢复原状态
    form.setFieldsValue({ status: currentStatus });
  }
};
```

---

## 第四步：后端 - 删除版本时的验证

### 4.1 修改 VersionService.deleteVersion

```java
@Transactional
public void deleteVersion(Long versionId) {
    ProductVersion version = versionMapper.selectById(versionId);
    if (version == null) {
        throw new BusinessException(ErrorCode.VERSION_NOT_FOUND);
    }
    
    // 检查是否是最后一个已发布版本
    if ("PUBLISHED".equals(version.getStatus())) {
        long publishedCount = versionMapper.countPublishedVersions(version.getProductId());
        if (publishedCount <= 1) {
            // 检查产品状态
            Product product = productMapper.selectById(version.getProductId());
            if (product != null && "PUBLISHED".equals(product.getStatus())) {
                throw new BusinessException(ErrorCode.CANNOT_DELETE_LAST_PUBLISHED_VERSION,
                    "无法删除最后一个已发布版本，产品当前状态为"已发布"。请先将产品状态改为"草稿"或"归档"。");
            }
        }
    }
    
    versionMapper.deleteById(versionId);
    log.info("Version {} deleted", versionId);
}
```

### 4.2 添加新的错误码

在 `ErrorCode` 中添加：

```java
CANNOT_DELETE_LAST_PUBLISHED_VERSION(40023, "无法删除最后一个已发布版本"),
```

---

## 第五步：添加翻译文本

### 5.1 中文翻译 (zh-CN.json)

```json
{
  "productEdit": {
    "deleteLastPublishedVersion": "确认删除最后一个已发布版本？",
    "deleteLastPublishedVersionWarning": "这是该产品最后一个已发布版本，删除后产品将无法被下载。建议先将产品状态改为"草稿"或"归档"。",
    "deleteLastPublishedVersionInfo": "这是最后一个已发布版本，删除后将没有可下载的版本。",
    "statusInconsistent": "产品状态不一致",
    "publishedButNoVersion": "产品状态为"已发布"，但没有已发布的版本。请添加并发布至少一个版本，或将产品状态改为"草稿"。",
    "goToFix": "去处理",
    "statusChangeWarning": "状态变更提示",
    "lastPublishedVersionDeleted": "最后一个已发布版本已被删除"
  }
}
```

### 5.2 英文翻译 (en-US.json)

```json
{
  "productEdit": {
    "deleteLastPublishedVersion": "Delete the last published version?",
    "deleteLastPublishedVersionWarning": "This is the last published version. After deletion, the product will not be downloadable. Consider changing the product status to 'Draft' or 'Archived' first.",
    "deleteLastPublishedVersionInfo": "This is the last published version. After deletion, there will be no downloadable versions.",
    "statusInconsistent": "Product Status Inconsistent",
    "publishedButNoVersion": "Product status is 'Published' but has no published versions. Please add and publish at least one version, or change the product status to 'Draft'.",
    "goToFix": "Fix Now",
    "statusChangeWarning": "Status Change Warning",
    "lastPublishedVersionDeleted": "Last published version has been deleted"
  }
}
```

---

## 第六步：浏览器关闭/刷新时的验证

### 6.1 增强 beforeunload 事件处理

```typescript
useEffect(() => {
  const handleBeforeUnload = (e: BeforeUnloadEvent) => {
    // 检查状态一致性
    const statusError = validateProductStatusConsistency();
    if (statusError || hasUnsavedChanges) {
      e.preventDefault();
      e.returnValue = '';
    }
  };
  window.addEventListener('beforeunload', handleBeforeUnload);
  return () => window.removeEventListener('beforeunload', handleBeforeUnload);
}, [hasUnsavedChanges, versions, product]);
```

---

## 修改文件清单

### 前端文件
1. `oc-platform-web/src/pages/Admin/Products/ProductEdit.tsx`
   - 添加删除版本验证逻辑
   - 增强安全导航函数
   - 添加状态一致性验证
   - 添加状态选择验证

2. `oc-platform-web/src/locales/zh-CN.json`
   - 添加新的翻译文本

3. `oc-platform-web/src/locales/en-US.json`
   - 添加新的翻译文本

### 后端文件
1. `oc-platform-product/src/main/java/com/ocplatform/product/service/VersionService.java`
   - 添加删除版本前的验证逻辑

2. `oc-platform-common/src/main/java/com/ocplatform/common/response/ErrorCode.java`
   - 添加新的错误码

---

## 测试用例

### 前端测试
1. **删除最后一个已发布版本**：
   - 产品状态为 PUBLISHED 时删除最后一个已发布版本 → 显示警告
   - 产品状态为 DRAFT 时删除最后一个已发布版本 → 显示提示

2. **退出页面验证**：
   - 产品状态为 PUBLISHED 但没有已发布版本 → 阻止退出并提示
   - 正常情况 → 允许退出

3. **状态选择验证**：
   - 选择 PUBLISHED 但没有已发布版本 → 显示警告并恢复原状态

### 后端测试
1. **删除版本 API**：
   - 删除最后一个已发布版本且产品状态为 PUBLISHED → 返回错误
   - 其他情况 → 正常删除

---

## 预期效果

1. **用户体验优化**：
   - 用户在删除版本前会收到明确的警告
   - 用户在退出页面时会收到状态不一致的提示
   - 用户在选择状态时会得到即时反馈

2. **数据一致性保障**：
   - 后端拒绝不合理的删除操作
   - 产品状态与版本始终保持一致

3. **国际化支持**：
   - 所有新增提示均支持中英文切换
