# Webapp-testing 技能修改完善计划

## 一、需求概述

对 `E:\oc\.trae\skills\webapp-testing` 技能进行修改完善，主要包括：
1. 测试前自动检测并安装必要的测试工具（Playwright）
2. 在项目顶层同级目录下创建测试文件夹和文件
3. 整合测试素材和登录账号信息
4. 测试结束后清理失败的测试文件

## 二、现状分析

### 当前技能结构
```
webapp-testing/
├── SKILL.md                    # 技能说明文档
├── LICENSE.txt                 # 许可证
├── scripts/
│   └── with_server.py          # 服务器管理脚本
└── examples/
    ├── element_discovery.py    # 元素发现示例
    ├── static_html_automation.py # 静态HTML自动化示例
    └── console_logging.py      # 控制台日志示例
```

### 测试账号信息（来自 SQL 文件）
| 用户名 | 邮箱 | 密码 | 角色 |
|--------|------|------|------|
| admin | admin@ocplatform.com | Admin@123456 | 超级管理员 |
| zhangsan | zhangsan@example.com | Test@123456 | 普通用户 |
| lisi | lisi@example.com | Test@123456 | 普通用户 |
| wangwu | wangwu@example.com | Test@123456 | VIP用户 |
| dev_chen | chen@example.com | Test@123456 | 普通用户 |

### 项目信息
- 前端端口: 5173 (Vite 开发服务器)
- 后端端口: 8081 (Spring Boot)
- 项目路径: `E:\oc\oc-platform`
- 测试素材路径: `E:\oc\Front-end testing`
- 测试输出路径: `E:\oc\logs` (已存在测试文件)

## 三、修改计划

### 步骤 1: 创建环境检测和安装脚本

**文件**: `scripts/check_environment.py`

功能：
- 检测 Python 环境
- 检测 Playwright 是否已安装
- 检测浏览器是否已安装
- 自动安装缺失的依赖

### 步骤 2: 创建测试目录管理脚本

**文件**: `scripts/test_manager.py`

功能：
- 在项目同级目录创建测试文件夹结构
- 管理测试文件的创建、执行和清理
- 区分成功和失败的测试结果

### 步骤 3: 创建测试配置文件

**文件**: `config/test_config.py`

内容：
- 测试账号信息
- 前后端 URL 配置
- 测试目录路径配置
- 超时和重试配置

### 步骤 4: 创建测试基类

**文件**: `scripts/base_test.py`

功能：
- 提供测试基类，封装常用操作
- 登录/登出功能
- 截图保存
- 测试结果记录
- 自动清理失败文件

### 步骤 5: 更新 SKILL.md 文档

修改内容：
1. 添加环境检测和安装说明
2. 添加测试目录结构说明
3. 添加测试账号信息引用
4. 添加测试清理规则说明
5. 更新最佳实践部分

### 步骤 6: 创建测试目录结构

在 `E:\oc` 下创建：
```
E:\oc\
├── test-output/              # 测试输出目录
│   ├── screenshots/          # 截图目录
│   │   ├── success/          # 成功测试截图
│   │   └── failed/           # 失败测试截图
│   ├── scripts/              # 测试脚本
│   │   ├── success/          # 成功的测试脚本
│   │   └── failed/           # 失败的测试脚本
│   └── reports/              # 测试报告
└── Front-end testing/        # 测试素材（已存在）
```

## 四、详细实现

### 4.1 环境检测脚本 (`scripts/check_environment.py`)

检测 Python 版本、Playwright 安装状态和浏览器安装状态，提供自动安装功能。

### 4.2 测试管理脚本 (`scripts/test_manager.py`)

管理测试目录创建、测试执行和结果清理。

### 4.3 测试配置 (`config/test_config.py`)

集中管理测试配置，包括账号、URL、路径等。

### 4.4 测试基类 (`scripts/base_test.py`)

封装常用测试操作，提供登录、截图、结果记录等功能。

### 4.5 SKILL.md 更新内容

1. **环境准备章节** - 添加环境检测和安装说明
2. **测试目录章节** - 添加目录结构说明
3. **测试账号章节** - 添加账号信息获取方式
4. **清理规则章节** - 添加测试结果清理规则
5. **最佳实践更新** - 整合新的工作流程

## 五、执行顺序

1. 创建 `config/test_config.py` - 测试配置文件
2. 创建 `scripts/check_environment.py` - 环境检测脚本
3. 创建 `scripts/test_manager.py` - 测试管理脚本
4. 创建 `scripts/base_test.py` - 测试基类
5. 更新 `SKILL.md` - 技能文档
6. 创建示例测试脚本 - 演示新功能使用

## 六、预期成果

修改完成后，技能将具备以下能力：

1. **自动环境准备**: 检测并自动安装 Playwright 和浏览器
2. **规范化目录**: 自动创建标准化的测试目录结构
3. **便捷的账号访问**: 通过配置文件快速获取测试账号
4. **自动清理**: 测试结束后自动保留成功文件，清理失败文件
5. **完整的文档**: 清晰的使用说明和最佳实践
