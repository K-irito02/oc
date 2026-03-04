---
name: webapp-testing
description: |
  Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
license: Complete terms in LICENSE.txt
version: 1.6.0
last_updated: 2026-03-04
---

# Web Application Testing

To test local web applications, write native Python Playwright scripts.

## Helper Scripts Available

| Script | Description |
|--------|-------------|
| `scripts/check_environment.py` | 检测并安装 Playwright 和浏览器 |
| `scripts/test_manager.py` | 管理测试目录、执行和清理 |
| `scripts/base_test.py` | 测试基类，封装常用操作 |
| `scripts/with_server.py` | 管理服务器生命周期 |

**Always run scripts with `--help` first** to see usage. DO NOT read the source until you try running the script first and find that a customized solution is absolutely necessary.

## Quick Start

### 1. 环境准备

在开始测试之前，确保测试环境已就绪：

```bash
# 检测并自动安装环境
python scripts/check_environment.py --install

# 仅检测环境状态
python scripts/check_environment.py --check-only
```

### 2. 初始化测试目录

```bash
# 创建测试输出目录结构
python scripts/test_manager.py init
```

测试目录结构：
```
E:\oc\test-output\
├── screenshots/          # 截图目录
├── scripts/              # 测试脚本存档
└── reports/              # 测试报告 (JSON)
```

### 3. 编写测试脚本

使用 `BaseTest` 基类编写测试：

```python
from scripts.base_test import BaseTest

def test_login():
    test = BaseTest("login_test")
    try:
        test.setup()
        
        # 导航到前端页面
        test.goto_frontend("/login")
        test.screenshot("login_page")
        
        # 使用测试账号登录
        if test.login(account_name="admin"):
            test.screenshot("after_login")
            test.mark_success()
        else:
            test.mark_failed("登录失败")
            
    except Exception as e:
        test.mark_failed(str(e))
    finally:
        test.teardown()

if __name__ == "__main__":
    test_login()
```

## Test Configuration

测试配置位于 `config/test_config.py`，包含：

### 测试账号

| 账号名 | 邮箱 | 密码 | 角色 |
|--------|------|------|------|
| admin | admin@ocplatform.com | Admin@123456 | 超级管理员 |
| zhangsan | zhangsan@example.com | Test@123456 | 普通用户 |
| lisi | lisi@example.com | Test@123456 | 普通用户 |
| wangwu | wangwu@example.com | Test@123456 | VIP用户 |

在代码中使用：
```python
from config.test_config import TestConfig

# 获取管理员账号
admin = TestConfig.get_admin_account()

# 获取指定账号
user = TestConfig.get_account("zhangsan")

# 获取所有普通用户账号
users = TestConfig.get_accounts_by_role("USER")
```

### URL 配置

```python
# 前端 URL
TestConfig.FRONTEND_URL  # http://localhost:5173

# 后端 API URL
TestConfig.API_BASE_URL  # http://localhost:8081/api/v1
```

### 路径配置

```python
# 测试输出目录
TestConfig.TEST_OUTPUT_DIR      # E:\oc\test-output

# 测试素材目录
TestConfig.TEST_MATERIALS_DIR   # E:\oc\Front-end testing

# 获取素材文件路径
TestConfig.get_test_material_path("test_image.png")
```

## Decision Tree: Choosing Your Approach

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Example: Using with_server.py

To start a server, run `--help` first, then use the helper:

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Multiple servers (e.g., backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

To create an automation script, include only Playwright logic (servers are managed automatically):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Reconnaissance-Then-Action Pattern

1. **Inspect rendered DOM**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. **Identify selectors** from inspection results

3. **Execute actions** using discovered selectors

## Test Manager Commands

```bash
# 初始化测试目录
python scripts/test_manager.py init

# 运行测试脚本
python scripts/test_manager.py run --script path/to/test.py

# 列出测试结果
python scripts/test_manager.py list

# 仅列出成功的测试
python scripts/test_manager.py list --success-only

# 清理失败的测试文件
python scripts/test_manager.py cleanup
```

## Cleanup Rules

测试结束后，系统会自动处理测试文件：

1. **测试结果记录**：
   - Python 脚本保存到 `test-output/scripts/`
   - 截图保存到 `test-output/screenshots/`
   - 测试报告保存到 `test-output/reports/`

2. **清理功能**：
   - 使用 `python scripts/test_manager.py list` 查看所有测试结果
   - 测试结果包含成功/失败状态信息

## Common Pitfall

❌ **Don't** inspect the DOM before waiting for `networkidle` on dynamic apps
✅ **Do** wait for `page.wait_for_load_state('networkidle')` before inspection

## Best Practices

- **Use bundled scripts as black boxes** - To accomplish a task, consider whether one of the scripts available in `scripts/` can help. These scripts handle common, complex workflows reliably without cluttering the context window. Use `--help` to see usage, then invoke directly.
- **Always check environment first** - Run `check_environment.py` before starting tests
- **Use `BaseTest` class** - It handles setup, teardown, and result tracking automatically
- **Use `sync_playwright()` for synchronous scripts**
- **Always close the browser when done**
- **Use descriptive selectors**: `text=`, `role=`, CSS selectors, or IDs
- **Add appropriate waits**: `page.wait_for_selector()` or `page.wait_for_timeout()`
- **Take screenshots for debugging** - Use `test.screenshot()` to capture state

## Reference Files

- **config/test_config.py** - 测试配置（账号、URL、路径）
- **scripts/check_environment.py** - 环境检测和安装
- **scripts/test_manager.py** - 测试管理工具
- **scripts/base_test.py** - 测试基类
- **examples/** - Examples showing common patterns:
  - `element_discovery.py` - Discovering buttons, links, and inputs on a page
  - `static_html_automation.py` - Using file:// URLs for local HTML
  - `console_logging.py` - Capturing console logs during automation
  - `login_test.py` - Login functionality testing
  - `super_admin_protection_test.py` - Super admin protection feature testing
