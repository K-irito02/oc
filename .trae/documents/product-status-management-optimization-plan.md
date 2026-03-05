# 产品状态管理优化计划

## 问题分析

### 问题一：新建产品时删除版本后状态不一致

**当前问题**：
- 用户添加版本并发布后，将产品状态改为"待审核"或"已发布"
- 然后删除所有已发布版本，系统不会提示状态不一致
- 用户可以正常离开页面，导致数据不一致

**当前代码逻辑**：
- `handleDeletePendingVersion` 只在删除最后一个已发布版本时显示警告
- `validateProductStatusConsistency` 只检查 PUBLISHED 状态是否有已发布版本
- 没有检查 PENDING 状态是否需要版本

### 问题二：编辑产品时状态转换限制过严

**当前问题**：
- 后端 `validateStatusTransition` 限制了 PUBLISHED 状态只能转换为 ARCHIVED
- 用户无法将已发布的产品改回草稿或待审核状态

**当前状态转换规则**：
```
DRAFT → PENDING (需要至少一个版本)
DRAFT → PUBLISHED (需要至少一个已发布版本)
PENDING → PUBLISHED (需要至少一个已发布版本)
PUBLISHED → ARCHIVED (仅允许)
```

---

## 解决方案

### 方案设计

#### 问题一解决方案：增强版本删除后的状态验证

1. **前端验证增强**：
   - 删除版本后检查产品状态一致性
   - 如果状态为 PENDING/PUBLISHED 但没有已发布版本，提示用户
   - 阻止用户离开页面直到问题解决

2. **状态一致性规则**：
   - DRAFT：无版本要求
   - PENDING：至少一个版本（可以是草稿版本）
   - PUBLISHED：至少一个已发布版本
   - ARCHIVED：无版本要求

#### 问题二解决方案：放宽状态转换限制

**新的状态转换规则**：
```
DRAFT → PENDING (需要至少一个版本)
DRAFT → PUBLISHED (需要至少一个已发布版本)
DRAFT → ARCHIVED

PENDING → DRAFT
PENDING → PUBLISHED (需要至少一个已发布版本)
PENDING → REJECTED

REJECTED → DRAFT
REJECTED → PENDING (需要至少一个版本)

PUBLISHED → DRAFT (需要确认)
PUBLISHED → PENDING (需要确认)
PUBLISHED → ARCHIVED

ARCHIVED → DRAFT
ARCHIVED → PUBLISHED (需要至少一个已发布版本)
```

---

## 详细实施步骤

---

## 第一步：前端 - 增强状态一致性验证函数

### 1.1 修改 validateProductStatusConsistency 函数

文件：`oc-platform-web/src/pages/Admin/Products/ProductEdit.tsx`

```typescript
const validateProductStatusConsistency = useCallback((): string | null => {
  if (isNewProduct) {
    // 新建产品模式
    const status = form.getFieldValue('status');
    const allCount = pendingVersions.length;
    const publishedCount = pendingVersions.filter(v => v.status === 'PUBLISHED').length;
    
    if (status === 'PENDING' && allCount === 0) {
      return t('productEdit.pendingNeedsVersion');
    }
    
    if (status === 'PUBLISHED' && publishedCount === 0) {
      return t('productEdit.publishedVersionRequired');
    }
    
    return null;
  }
  
  // 编辑产品模式
  const status = product?.status;
  const allCount = versions.length;
  const publishedCount = versions.filter(v => v.status === 'PUBLISHED').length;
  
  if (status === 'PENDING' && allCount === 0) {
    return t('productEdit.pendingButNoVersion');
  }
  
  if (status === 'PUBLISHED' && publishedCount === 0) {
    return t('productEdit.publishedButNoVersion');
  }
  
  return null;
}, [isNewProduct, product?.status, versions, pendingVersions, form, t]);
```

### 1.2 添加翻译文本

文件：`oc-platform-web/src/locales/zh-CN.json`

```json
{
  "productEdit": {
    "pendingButNoVersion": "产品状态为\"待审核\"，但没有版本。请添加至少一个版本，或将产品状态改为\"草稿\"。",
    "statusWillChange": "状态将变更",
    "deleteLastVersionWarning": "删除此版本后，产品将没有版本。当前产品状态为\"{status}\"，建议将状态改为\"草稿\"。",
    "deleteLastPublishedVersionStatusChange": "删除此版本后，产品将没有已发布版本。当前产品状态为\"{status}\"，是否将状态改为\"草稿\"？",
    "statusChangedToDraft": "产品状态已自动改为\"草稿\""
  }
}
```

---

## 第二步：前端 - 增强删除版本时的验证

### 2.1 修改 handleDeletePendingVersion 函数

```typescript
const handleDeletePendingVersion = (tempId: string) => {
  const version = pendingVersions.find(v => v.tempId === tempId);
  const remainingVersions = pendingVersions.filter(v => v.tempId !== tempId);
  const publishedCount = remainingVersions.filter(v => v.status === 'PUBLISHED').length;
  const currentStatus = form.getFieldValue('status');
  
  // 检查删除后的状态一致性
  const checkStatusConsistency = () => {
    if (currentStatus === 'PUBLISHED' && publishedCount === 0) {
      return {
        error: t('productEdit.deleteLastPublishedVersionStatusChange', { status: currentStatus }),
        suggestedStatus: 'DRAFT'
      };
    }
    if (currentStatus === 'PENDING' && remainingVersions.length === 0) {
      return {
        error: t('productEdit.deleteLastVersionWarning', { status: currentStatus }),
        suggestedStatus: 'DRAFT'
      };
    }
    return null;
  };
  
  const consistencyError = checkStatusConsistency();
  
  if (consistencyError) {
    Modal.confirm({
      title: t('productEdit.statusWillChange'),
      content: consistencyError.error,
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      onOk: () => {
        setPendingVersions(remainingVersions);
        form.setFieldsValue({ status: consistencyError.suggestedStatus });
        setHasUnsavedChanges(true);
        message.info(t('productEdit.statusChangedToDraft'));
      }
    });
    return;
  }
  
  // 原有的最后一个已发布版本警告
  if (version?.status === 'PUBLISHED' && pendingVersions.filter(v => v.status === 'PUBLISHED').length === 1) {
    Modal.confirm({
      title: t('productEdit.deleteLastPublishedVersion'),
      content: currentStatus === 'PUBLISHED' 
        ? t('productEdit.deleteLastPublishedVersionWarning')
        : t('productEdit.deleteLastPublishedVersionInfo'),
      okText: t('common.confirm'),
      cancelText: t('common.cancel'),
      onOk: () => {
        setPendingVersions(remainingVersions);
        setHasUnsavedChanges(true);
      }
    });
    return;
  }
  
  setPendingVersions(remainingVersions);
  setHasUnsavedChanges(true);
};
```

### 2.2 修改 handleDeleteVersion 函数（编辑模式）

类似的逻辑，但在删除后需要调用后端 API 更新产品状态。

---

## 第三步：后端 - 放宽状态转换限制

### 3.1 修改 validateStatusTransition 方法

文件：`oc-platform-product/src/main/java/com/ocplatform/product/service/ProductService.java`

```java
private void validateStatusTransition(String currentStatus, String targetStatus, Long productId) {
    if (currentStatus.equals(targetStatus)) {
        return;
    }
    
    long allVersionCount = versionMapper.countAllVersions(productId);
    long publishedVersionCount = versionMapper.countPublishedVersions(productId);
    
    switch (currentStatus) {
        case "DRAFT":
            if ("PENDING".equals(targetStatus)) {
                if (allVersionCount == 0) {
                    throw new BusinessException(ErrorCode.NO_VERSION, "提交审核前，请先添加至少一个版本");
                }
            } else if ("PUBLISHED".equals(targetStatus)) {
                if (publishedVersionCount == 0) {
                    throw new BusinessException(ErrorCode.NO_PUBLISHED_VERSION, "发布产品前，请先发布至少一个版本");
                }
            }
            // DRAFT 可以转换为任何状态
            break;
            
        case "PENDING":
            if ("PUBLISHED".equals(targetStatus)) {
                if (publishedVersionCount == 0) {
                    throw new BusinessException(ErrorCode.NO_PUBLISHED_VERSION, "审核通过前，请先发布至少一个版本");
                }
            }
            // PENDING 可以转换为 DRAFT, REJECTED, PUBLISHED
            if (!"DRAFT".equals(targetStatus) && !"REJECTED".equals(targetStatus) && !"PUBLISHED".equals(targetStatus)) {
                throw new BusinessException(ErrorCode.INVALID_STATUS_TRANSITION, 
                        "产品状态不能从 " + currentStatus + " 转换为 " + targetStatus);
            }
            break;
            
        case "REJECTED":
            // REJECTED 可以转换为 DRAFT, PENDING
            if (!"DRAFT".equals(targetStatus) && !"PENDING".equals(targetStatus)) {
                throw new BusinessException(ErrorCode.INVALID_STATUS_TRANSITION, 
                        "产品状态不能从 " + currentStatus + " 转换为 " + targetStatus);
            }
            if ("PENDING".equals(targetStatus) && allVersionCount == 0) {
                throw new BusinessException(ErrorCode.NO_VERSION, "提交审核前，请先添加至少一个版本");
            }
            break;
            
        case "PUBLISHED":
            // PUBLISHED 可以转换为 DRAFT, PENDING, ARCHIVED
            if (!"DRAFT".equals(targetStatus) && !"PENDING".equals(targetStatus) && !"ARCHIVED".equals(targetStatus)) {
                throw new BusinessException(ErrorCode.INVALID_STATUS_TRANSITION, 
                        "产品状态不能从 " + currentStatus + " 转换为 " + targetStatus);
            }
            // 转换为 PENDING 需要版本
            if ("PENDING".equals(targetStatus) && allVersionCount == 0) {
                throw new BusinessException(ErrorCode.NO_VERSION, "产品必须有至少一个版本才能设置为待审核状态");
            }
            break;
            
        case "ARCHIVED":
            // ARCHIVED 可以转换为 DRAFT, PUBLISHED
            if (!"DRAFT".equals(targetStatus) && !"PUBLISHED".equals(targetStatus)) {
                throw new BusinessException(ErrorCode.INVALID_STATUS_TRANSITION, 
                        "产品状态不能从 " + currentStatus + " 转换为 " + targetStatus);
            }
            if ("PUBLISHED".equals(targetStatus) && publishedVersionCount == 0) {
                throw new BusinessException(ErrorCode.NO_PUBLISHED_VERSION, "发布产品前，请先发布至少一个版本");
            }
            break;
            
        default:
            throw new BusinessException(ErrorCode.INVALID_STATUS_TRANSITION, 
                    "未知的产品状态: " + currentStatus);
    }
}
```

---

## 第四步：前端 - 更新状态选择验证逻辑

### 4.1 修改 validatePublishStatus 函数

```typescript
const validatePublishStatus = useCallback((currentStatus: string, targetStatus: string, versionList: Array<{ status?: string }>): string | null => {
  if (currentStatus === targetStatus) {
    return null;
  }
  
  const allCount = versionList.length;
  const publishedCount = versionList.filter(v => v.status === 'PUBLISHED').length;
  
  // 从 DRAFT 转换
  if (currentStatus === 'DRAFT') {
    if (targetStatus === 'PENDING' && allCount === 0) {
      return t('productEdit.pendingNeedsVersion');
    }
    if (targetStatus === 'PUBLISHED' && publishedCount === 0) {
      return t('productEdit.publishedVersionRequired');
    }
  }
  
  // 从 PENDING 转换
  if (currentStatus === 'PENDING') {
    if (targetStatus === 'PUBLISHED' && publishedCount === 0) {
      return t('productEdit.publishedVersionRequired');
    }
  }
  
  // 从 REJECTED 转换
  if (currentStatus === 'REJECTED') {
    if (targetStatus === 'PENDING' && allCount === 0) {
      return t('productEdit.pendingNeedsVersion');
    }
  }
  
  // 从 PUBLISHED 转换
  if (currentStatus === 'PUBLISHED') {
    if (targetStatus === 'PENDING' && allCount === 0) {
      return t('productEdit.pendingNeedsVersion');
    }
    // PUBLISHED 可以转换为 DRAFT, PENDING, ARCHIVED
    if (!['DRAFT', 'PENDING', 'ARCHIVED'].includes(targetStatus)) {
      return t('productEdit.invalidStatusTransition', { from: currentStatus, to: targetStatus });
    }
  }
  
  // 从 ARCHIVED 转换
  if (currentStatus === 'ARCHIVED') {
    if (targetStatus === 'PUBLISHED' && publishedCount === 0) {
      return t('productEdit.publishedVersionRequired');
    }
  }
  
  return null;
}, [t]);
```

---

## 第五步：添加翻译文本

### 5.1 中文翻译 (zh-CN.json)

```json
{
  "productEdit": {
    "pendingNeedsVersion": "提交审核前，请先添加至少一个版本",
    "publishedVersionRequired": "发布产品前，请先发布至少一个版本",
    "pendingButNoVersion": "产品状态为\"待审核\"，但没有版本。请添加至少一个版本，或将产品状态改为\"草稿\"。",
    "publishedButNoVersion": "产品状态为\"已发布\"，但没有已发布的版本。请添加并发布至少一个版本，或将产品状态改为\"草稿\"。",
    "statusWillChange": "状态将变更",
    "deleteLastVersionWarning": "删除此版本后，产品将没有版本。当前产品状态为\"{status}\"，建议将状态改为\"草稿\"。",
    "deleteLastPublishedVersionStatusChange": "删除此版本后，产品将没有已发布版本。当前产品状态为\"{status}\"，是否将状态改为\"草稿\"？",
    "statusChangedToDraft": "产品状态已自动改为\"草稿\"",
    "invalidStatusTransition": "产品状态不能从\"{from}\"转换为\"{to}\"",
    "confirmStatusChange": "确认状态变更",
    "publishedToDraftWarning": "将产品从\"已发布\"改为\"草稿\"后，用户将无法下载该产品。确定要继续吗？",
    "publishedToPendingWarning": "将产品从\"已发布\"改为\"待审核\"后，用户将无法下载该产品。确定要继续吗？"
  }
}
```

### 5.2 英文翻译 (en-US.json)

```json
{
  "productEdit": {
    "pendingNeedsVersion": "Please add at least one version before submitting for review",
    "publishedVersionRequired": "Please publish at least one version before releasing the product",
    "pendingButNoVersion": "Product status is 'Pending Review' but has no versions. Please add at least one version or change the status to 'Draft'.",
    "publishedButNoVersion": "Product status is 'Published' but has no published versions. Please add and publish at least one version or change the status to 'Draft'.",
    "statusWillChange": "Status Will Change",
    "deleteLastVersionWarning": "After deleting this version, the product will have no versions. Current status is '{status}', consider changing status to 'Draft'.",
    "deleteLastPublishedVersionStatusChange": "After deleting this version, the product will have no published versions. Current status is '{status}'. Change status to 'Draft'?",
    "statusChangedToDraft": "Product status has been automatically changed to 'Draft'",
    "invalidStatusTransition": "Product status cannot change from '{from}' to '{to}'",
    "confirmStatusChange": "Confirm Status Change",
    "publishedToDraftWarning": "After changing the product from 'Published' to 'Draft', users will not be able to download this product. Are you sure you want to continue?",
    "publishedToPendingWarning": "After changing the product from 'Published' to 'Pending Review', users will not be able to download this product. Are you sure you want to continue?"
  }
}
```

---

## 修改文件清单

### 前端文件
1. `oc-platform-web/src/pages/Admin/Products/ProductEdit.tsx`
   - 增强 `validateProductStatusConsistency` 函数
   - 修改 `handleDeletePendingVersion` 函数
   - 修改 `handleDeleteVersion` 函数
   - 更新 `validatePublishStatus` 函数
   - 添加状态转换确认对话框

2. `oc-platform-web/src/locales/zh-CN.json`
   - 添加新的翻译文本

3. `oc-platform-web/src/locales/en-US.json`
   - 添加新的翻译文本

### 后端文件
1. `oc-platform-product/src/main/java/com/ocplatform/product/service/ProductService.java`
   - 修改 `validateStatusTransition` 方法，放宽状态转换限制

---

## 测试用例

### 新建产品测试
1. **删除最后一个版本**：
   - 状态为 PENDING → 提示将状态改为 DRAFT
   - 状态为 PUBLISHED → 提示将状态改为 DRAFT
   - 状态为 DRAFT → 正常删除

2. **状态一致性验证**：
   - 删除版本后尝试离开页面 → 阻止并提示

### 编辑产品测试
1. **状态转换**：
   - PUBLISHED → DRAFT：需要确认
   - PUBLISHED → PENDING：需要确认
   - PUBLISHED → ARCHIVED：正常转换
   - DRAFT → PUBLISHED：需要已发布版本

2. **删除版本**：
   - 删除最后一个已发布版本，产品状态为 PUBLISHED → 提示

---

## 预期效果

1. **新建产品**：
   - 删除版本后自动检测状态一致性
   - 提示用户并建议修改状态
   - 阻止用户在状态不一致时离开页面

2. **编辑产品**：
   - 支持更灵活的状态转换
   - PUBLISHED 可以转换为 DRAFT/PENDING/ARCHIVED
   - 重要状态变更需要用户确认

3. **用户体验**：
   - 清晰的错误提示
   - 自动建议解决方案
   - 防止数据不一致
