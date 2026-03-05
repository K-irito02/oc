# 平台与架构选择优化计划

## 问题分析

### 当前问题

1. **平台和架构硬编码**：
   - 前端 `PLATFORM_OPTIONS` 是硬编码的常量数组
   - 架构选项也是硬编码的（x86, x64, arm64, universal）
   - 数据库有 CHECK 约束限制了固定值

2. **平台与架构没有关联**：
   - 不同平台支持的架构不同（如 iOS 只有 arm64，Windows 有 x86/x64/arm64）
   - 当前实现没有根据平台动态显示对应架构

3. **不支持自定义**：
   - 无法添加新平台或新架构
   - 需要修改代码才能支持新平台

### 当前代码状态

**前端 (ProductEdit.tsx)**：
```typescript
const PLATFORM_OPTIONS = [
  { value: 'WINDOWS', label: 'Windows', icon: '🪟' },
  { value: 'MACOS', label: 'macOS', icon: '🍎' },
  { value: 'LINUX', label: 'Linux', icon: '🐧' },
  { value: 'ANDROID', label: 'Android', icon: '🤖' },
  { value: 'IOS', label: 'iOS', icon: '📱' },
];
// 架构选项：x86, x64, arm64, universal
```

**数据库 (init.sql)**：
```sql
platform VARCHAR(50) NOT NULL
  CHECK (platform IN ('WINDOWS', 'LINUX', 'MACOS', 'ANDROID', 'IOS', 'WEB', 'CROSS_PLATFORM')),
architecture VARCHAR(20) DEFAULT 'x64'
  CHECK (architecture IN ('x86', 'x64', 'arm64')),
```

---

## 解决方案

### 方案设计

采用**系统配置 + 数据库约束放宽**的策略：

1. **数据库层面**：
   - 移除 CHECK 约束，改为应用层验证
   - 在 `system_configs` 表中存储平台-架构映射配置

2. **后端层面**：
   - 提供平台配置 API
   - 管理后台支持配置平台和架构

3. **前端层面**：
   - 从后端获取平台配置
   - 根据选择的平台动态显示对应架构
   - 支持自定义平台和架构输入

### 默认平台-架构映射

| 平台 | 支持的架构 |
|------|-----------|
| Windows | x86, x64, arm64 |
| macOS | x64, arm64, universal |
| Linux | x86, x64, arm64 |
| Android | arm64, x86, x64 |
| iOS | arm64, x64 (模拟器) |
| Web | universal |
| Cross Platform | universal |

---

## 详细实施步骤

---

## 第一步：数据库迁移 - 移除 CHECK 约束

### 1.1 创建迁移脚本

文件：`sql/migrations/remove_platform_architecture_check.sql`

```sql
-- 移除 platform 字段的 CHECK 约束
ALTER TABLE product_versions DROP CONSTRAINT IF EXISTS product_versions_platform_check;

-- 移除 architecture 字段的 CHECK 约束
ALTER TABLE product_versions DROP CONSTRAINT IF EXISTS product_versions_architecture_check;

-- 添加注释说明
COMMENT ON COLUMN product_versions.platform IS '操作系统平台，如 WINDOWS, MACOS, LINUX, ANDROID, IOS, WEB, CROSS_PLATFORM 或自定义值';
COMMENT ON COLUMN product_versions.architecture IS 'CPU 架构，如 x86, x64, arm64, universal 或自定义值';
```

### 1.2 更新 init.sql

移除 CHECK 约束，保留字段定义：

```sql
platform        VARCHAR(50) NOT NULL,
architecture    VARCHAR(20) DEFAULT 'x64',
```

---

## 第二步：添加系统配置

### 2.1 插入默认平台配置

文件：`sql/migrations/add_platform_config.sql`

```sql
-- 插入平台配置
INSERT INTO system_configs (config_key, config_value, description, created_at, updated_at)
VALUES (
  'platform_config',
  '{
    "platforms": [
      {
        "value": "WINDOWS",
        "label": "Windows",
        "labelEn": "Windows",
        "icon": "🪟",
        "architectures": ["x86", "x64", "arm64"],
        "enabled": true,
        "sortOrder": 1
      },
      {
        "value": "MACOS",
        "label": "macOS",
        "labelEn": "macOS",
        "icon": "🍎",
        "architectures": ["x64", "arm64", "universal"],
        "enabled": true,
        "sortOrder": 2
      },
      {
        "value": "LINUX",
        "label": "Linux",
        "labelEn": "Linux",
        "icon": "🐧",
        "architectures": ["x86", "x64", "arm64"],
        "enabled": true,
        "sortOrder": 3
      },
      {
        "value": "ANDROID",
        "label": "Android",
        "labelEn": "Android",
        "icon": "🤖",
        "architectures": ["arm64", "x86", "x64"],
        "enabled": true,
        "sortOrder": 4
      },
      {
        "value": "IOS",
        "label": "iOS",
        "labelEn": "iOS",
        "icon": "📱",
        "architectures": ["arm64", "x64"],
        "enabled": true,
        "sortOrder": 5
      },
      {
        "value": "WEB",
        "label": "Web",
        "labelEn": "Web",
        "icon": "🌐",
        "architectures": ["universal"],
        "enabled": true,
        "sortOrder": 6
      },
      {
        "value": "CROSS_PLATFORM",
        "label": "跨平台",
        "labelEn": "Cross Platform",
        "icon": "🔄",
        "architectures": ["universal"],
        "enabled": true,
        "sortOrder": 7
      }
    ],
    "architectures": [
      {"value": "x86", "label": "x86 (32位)", "labelEn": "x86 (32-bit)"},
      {"value": "x64", "label": "x64 (64位)", "labelEn": "x64 (64-bit)"},
      {"value": "arm64", "label": "ARM64", "labelEn": "ARM64"},
      {"value": "universal", "label": "通用", "labelEn": "Universal"}
    ],
    "allowCustomPlatform": true,
    "allowCustomArchitecture": true
  }',
  '平台和架构配置',
  NOW(),
  NOW()
) ON CONFLICT (config_key) DO UPDATE SET
  config_value = EXCLUDED.config_value,
  updated_at = NOW();
```

---

## 第三步：后端 API

### 3.1 添加平台配置 DTO

文件：`oc-platform-product/src/main/java/com/ocplatform/product/dto/PlatformConfigVO.java`

```java
package com.ocplatform.product.dto;

import lombok.Builder;
import lombok.Data;
import java.util.List;

@Data
@Builder
public class PlatformConfigVO {
    private List<PlatformOption> platforms;
    private List<ArchitectureOption> architectures;
    private Boolean allowCustomPlatform;
    private Boolean allowCustomArchitecture;

    @Data
    @Builder
    public static class PlatformOption {
        private String value;
        private String label;
        private String labelEn;
        private String icon;
        private List<String> architectures;
        private Boolean enabled;
        private Integer sortOrder;
    }

    @Data
    @Builder
    public static class ArchitectureOption {
        private String value;
        private String label;
        private String labelEn;
    }
}
```

### 3.2 添加公共 API 端点

文件：`oc-platform-product/src/main/java/com/ocplatform/product/controller/PublicController.java`

```java
@GetMapping("/platform-config")
public ApiResponse<PlatformConfigVO> getPlatformConfig() {
    return ApiResponse.success(configService.getPlatformConfig());
}
```

### 3.3 添加管理后台 API

文件：`oc-platform-product/src/main/java/com/ocplatform/product/controller/AdminController.java`

```java
@PutMapping("/system/platform-config")
public ApiResponse<Void> updatePlatformConfig(@RequestBody PlatformConfigVO config) {
    configService.updatePlatformConfig(config);
    return ApiResponse.success(null);
}
```

---

## 第四步：前端改造

### 4.1 添加平台配置 API

文件：`oc-platform-web/src/utils/api.ts`

```typescript
// 获取平台配置
getPlatformConfig: () => request.get('/public/platform-config'),

// 更新平台配置（管理员）
updatePlatformConfig: (config: PlatformConfig) => 
  request.put('/admin/system/platform-config', config),
```

### 4.2 添加平台配置 Store

文件：`oc-platform-web/src/store/slices/platformConfigSlice.ts`

```typescript
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

interface PlatformOption {
  value: string;
  label: string;
  labelEn: string;
  icon: string;
  architectures: string[];
  enabled: boolean;
  sortOrder: number;
}

interface ArchitectureOption {
  value: string;
  label: string;
  labelEn: string;
}

interface PlatformConfig {
  platforms: PlatformOption[];
  architectures: ArchitectureOption[];
  allowCustomPlatform: boolean;
  allowCustomArchitecture: boolean;
}

export const fetchPlatformConfig = createAsyncThunk(
  'platformConfig/fetch',
  async () => {
    const res = await publicApi.getPlatformConfig();
    return res.data;
  }
);

const platformConfigSlice = createSlice({
  name: 'platformConfig',
  initialState: {
    config: null as PlatformConfig | null,
    loading: false,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchPlatformConfig.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchPlatformConfig.fulfilled, (state, action) => {
        state.loading = false;
        state.config = action.payload;
      });
  },
});

export default platformConfigSlice.reducer;
```

### 4.3 修改 ProductEdit.tsx

```typescript
// 从 Store 获取平台配置
const { config: platformConfig } = useSelector((state: RootState) => state.platformConfig);

// 根据选择的平台获取可用架构
const getAvailableArchitectures = useCallback((platformValue: string) => {
  if (!platformConfig) return [];
  
  const platform = platformConfig.platforms.find(p => p.value === platformValue);
  if (!platform) return platformConfig.architectures;
  
  return platformConfig.architectures.filter(
    arch => platform.architectures.includes(arch.value)
  );
}, [platformConfig]);

// 平台选择变化时，重置架构
const handlePlatformChange = useCallback((value: string) => {
  const availableArchs = getAvailableArchitectures(value);
  if (availableArchs.length > 0) {
    versionForm.setFieldsValue({ architecture: availableArchs[0].value });
  }
}, [getAvailableArchitectures, versionForm]);
```

### 4.4 版本表单组件

```tsx
<Form.Item name="platform" label={t('productEdit.platform')} required>
  <Select 
    placeholder={t('productEdit.selectPlatform')}
    onChange={handlePlatformChange}
    showSearch
    filterOption={(input, option) => 
      (option?.label ?? '').toLowerCase().includes(input.toLowerCase())
    }
  >
    {platformConfig?.platforms
      .filter(p => p.enabled)
      .sort((a, b) => a.sortOrder - b.sortOrder)
      .map(p => (
        <Select.Option key={p.value} value={p.value} label={`${p.icon} ${p.label}`}>
          {p.icon} {i18n.language === 'zh-CN' ? p.label : p.labelEn}
        </Select.Option>
      ))
    }
  </Select>
</Form.Item>

<Form.Item name="architecture" label={t('productEdit.architecture')}>
  <Select>
    {getAvailableArchitectures(selectedPlatform).map(arch => (
      <Select.Option key={arch.value} value={arch.value}>
        {i18n.language === 'zh-CN' ? arch.label : arch.labelEn}
      </Select.Option>
    ))}
  </Select>
</Form.Item>
```

---

## 第五步：管理后台配置页面

### 5.1 添加平台配置管理

在系统设置页面添加"平台配置"标签页：

- 显示当前平台列表
- 支持启用/禁用平台
- 支持编辑平台支持的架构
- 支持添加自定义平台
- 支持添加自定义架构

---

## 第六步：翻译文本

### 6.1 中文翻译 (zh-CN.json)

```json
{
  "platformConfig": {
    "title": "平台配置",
    "platforms": "平台列表",
    "architectures": "架构列表",
    "addPlatform": "添加平台",
    "addArchitecture": "添加架构",
    "platformName": "平台名称",
    "platformNameEn": "平台英文名称",
    "platformIcon": "图标",
    "supportedArchitectures": "支持的架构",
    "allowCustomPlatform": "允许自定义平台",
    "allowCustomArchitecture": "允许自定义架构",
    "customPlatformPlaceholder": "输入自定义平台名称...",
    "customArchitecturePlaceholder": "输入自定义架构名称..."
  }
}
```

### 6.2 英文翻译 (en-US.json)

```json
{
  "platformConfig": {
    "title": "Platform Configuration",
    "platforms": "Platform List",
    "architectures": "Architecture List",
    "addPlatform": "Add Platform",
    "addArchitecture": "Add Architecture",
    "platformName": "Platform Name",
    "platformNameEn": "Platform Name (English)",
    "platformIcon": "Icon",
    "supportedArchitectures": "Supported Architectures",
    "allowCustomPlatform": "Allow Custom Platform",
    "allowCustomArchitecture": "Allow Custom Architecture",
    "customPlatformPlaceholder": "Enter custom platform name...",
    "customArchitecturePlaceholder": "Enter custom architecture name..."
  }
}
```

---

## 修改文件清单

### 数据库文件
1. `sql/migrations/remove_platform_architecture_check.sql` - 移除 CHECK 约束
2. `sql/migrations/add_platform_config.sql` - 添加平台配置数据
3. `sql/init.sql` - 更新表定义

### 后端文件
1. `oc-platform-product/src/main/java/com/ocplatform/product/dto/PlatformConfigVO.java` - 新增 DTO
2. `oc-platform-product/src/main/java/com/ocplatform/product/service/ConfigService.java` - 添加配置服务
3. `oc-platform-product/src/main/java/com/ocplatform/product/controller/PublicController.java` - 添加公共 API
4. `oc-platform-product/src/main/java/com/ocplatform/product/controller/AdminController.java` - 添加管理 API

### 前端文件
1. `oc-platform-web/src/utils/api.ts` - 添加平台配置 API
2. `oc-platform-web/src/store/slices/platformConfigSlice.ts` - 新增 Store
3. `oc-platform-web/src/pages/Admin/Products/ProductEdit.tsx` - 修改版本表单
4. `oc-platform-web/src/pages/Admin/System/index.tsx` - 添加平台配置管理
5. `oc-platform-web/src/locales/zh-CN.json` - 添加翻译
6. `oc-platform-web/src/locales/en-US.json` - 添加翻译

---

## 测试用例

### 前端测试
1. **平台选择**：
   - 选择 Windows → 架构下拉显示 x86, x64, arm64
   - 选择 iOS → 架构下拉显示 arm64, x64
   - 选择 Web → 架构下拉显示 universal

2. **自定义平台**：
   - 启用自定义平台后，可以输入自定义平台名称
   - 自定义平台可以选择任意架构

3. **配置管理**：
   - 管理员可以添加/编辑/删除平台
   - 管理员可以配置平台支持的架构

### 后端测试
1. **API 测试**：
   - GET /public/platform-config → 返回平台配置
   - PUT /admin/system/platform-config → 更新平台配置

---

## 预期效果

1. **用户体验优化**：
   - 根据平台自动显示对应的架构选项
   - 减少用户选择错误

2. **灵活性提升**：
   - 支持自定义平台和架构
   - 无需修改代码即可添加新平台

3. **可维护性**：
   - 配置存储在数据库中
   - 管理后台可以直接配置

4. **国际化支持**：
   - 平台和架构名称支持中英文
