#!/usr/bin/env python3
"""
测试基类
封装常用的测试操作，提供登录、截图、结果记录等功能
"""
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Callable, Any
from contextlib import contextmanager

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.test_config import TestConfig, TestAccount


class BaseTest:
    def __init__(
        self,
        test_name: Optional[str] = None,
        config: Optional[TestConfig] = None,
        headless: Optional[bool] = None
    ):
        self.config = config or TestConfig()
        self.test_name = test_name or self._generate_test_name()
        self.headless = headless if headless is not None else self.config.HEADLESS
        self._browser = None
        self._page = None
        self._context = None
        self._playwright = None
        self._screenshots: List[str] = []
        self._success = True
        self._error_message: Optional[str] = None
    
    def _generate_test_name(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"test_{timestamp}"
    
    def setup(self) -> None:
        from playwright.sync_api import sync_playwright
        
        self.config.ensure_directories()
        
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self.headless,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        self._context = self._browser.new_context(
            viewport=self.config.VIEWPORT,
            locale=self.config.LOCALE,
            timezone_id=self.config.TIMEZONE
        )
        self._page = self._context.new_page()
        self._page.set_default_timeout(self.config.DEFAULT_TIMEOUT)
        
        print(f"测试初始化完成: {self.test_name}")
    
    def teardown(self) -> None:
        if self._page:
            self._page.close()
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()
        
        print(f"测试清理完成: {self.test_name}")
    
    @property
    def page(self):
        if self._page is None:
            raise RuntimeError("测试未初始化，请先调用 setup()")
        return self._page
    
    @property
    def browser(self):
        if self._browser is None:
            raise RuntimeError("测试未初始化，请先调用 setup()")
        return self._browser
    
    def goto(self, url: str, wait_for_network: bool = True) -> None:
        print(f"导航到: {url}")
        self.page.goto(url, timeout=self.config.NAVIGATION_TIMEOUT)
        if wait_for_network:
            self.page.wait_for_load_state('networkidle')
    
    def goto_frontend(self, path: str = "", wait_for_network: bool = True) -> None:
        url = f"{self.config.FRONTEND_URL}{path}"
        self.goto(url, wait_for_network)
    
    def goto_backend(self, path: str = "") -> None:
        url = f"{self.config.API_BASE_URL}{path}"
        self.goto(url, wait_for_network)
    
    def login(
        self,
        account: Optional[TestAccount] = None,
        account_name: Optional[str] = None
    ) -> bool:
        if account is None:
            if account_name:
                account = self.config.get_account(account_name)
            else:
                account = self.config.get_user_account()
        
        if account is None:
            raise ValueError("未找到测试账号")
        
        print(f"登录账号: {account.email}")
        
        try:
            self.goto_frontend("/login")
            
            email_input = self.page.locator('input[type="email"], input[name="email"], input[placeholder*="邮箱"], input[placeholder*="Email"]')
            password_input = self.page.locator('input[type="password"], input[name="password"]')
            submit_button = self.page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Login")')
            
            if email_input.count() > 0:
                email_input.first.fill(account.email)
            else:
                print("警告: 未找到邮箱输入框")
                return False
            
            if password_input.count() > 0:
                password_input.first.fill(account.password)
            else:
                print("警告: 未找到密码输入框")
                return False
            
            if submit_button.count() > 0:
                submit_button.first.click()
            else:
                print("警告: 未找到登录按钮")
                return False
            
            self.page.wait_for_timeout(2000)
            
            current_url = self.page.url
            if "login" not in current_url.lower():
                print(f"登录成功: {account.email}")
                return True
            else:
                error = self.page.locator('.error, .alert-error, [class*="error"]')
                if error.count() > 0:
                    print(f"登录失败: {error.first.text_content()}")
                else:
                    print("登录失败: 未知错误")
                return False
                
        except Exception as e:
            print(f"登录异常: {e}")
            return False
    
    def login_via_api(
        self,
        account: Optional[TestAccount] = None,
        account_name: Optional[str] = None
    ) -> Optional[str]:
        import requests
        
        if account is None:
            if account_name:
                account = self.config.get_account(account_name)
            else:
                account = self.config.get_user_account()
        
        if account is None:
            raise ValueError("未找到测试账号")
        
        print(f"API登录账号: {account.email}")
        
        try:
            response = requests.post(
                f"{self.config.API_BASE_URL}/auth/login",
                json={
                    "email": account.email,
                    "password": account.password
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                token = data.get('data', {}).get('token') or data.get('data', {}).get('accessToken')
                if token:
                    self._context.add_cookies([{
                        'name': 'token',
                        'value': token,
                        'domain': 'localhost',
                        'path': '/'
                    }])
                    self.page.set_extra_http_headers({
                        'Authorization': f'Bearer {token}'
                    })
                    print(f"API登录成功: {account.email}")
                    return token
            
            print(f"API登录失败: {response.status_code}")
            return None
            
        except Exception as e:
            print(f"API登录异常: {e}")
            return None
    
    def logout(self) -> None:
        try:
            logout_button = self.page.locator('button:has-text("退出"), button:has-text("Logout"), a:has-text("退出"), a:has-text("Logout")')
            if logout_button.count() > 0:
                logout_button.first.click()
                self.page.wait_for_timeout(1000)
                print("已退出登录")
        except Exception as e:
            print(f"退出登录异常: {e}")
    
    def screenshot(self, name: Optional[str] = None, full_page: bool = True) -> str:
        if name is None:
            name = f"{self.test_name}_{len(self._screenshots)}"
        
        path = self.config.get_screenshot_path(name, success=self._success)
        self.page.screenshot(path=str(path), full_page=full_page)
        self._screenshots.append(str(path))
        print(f"截图已保存: {path}")
        return str(path)
    
    def wait_for_selector(self, selector: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.config.DEFAULT_TIMEOUT
        self.page.wait_for_selector(selector, timeout=timeout)
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.config.ACTION_TIMEOUT
        self.page.click(selector, timeout=timeout)
    
    def fill(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        timeout = timeout or self.config.ACTION_TIMEOUT
        self.page.fill(selector, value, timeout=timeout)
    
    def get_text(self, selector: str) -> str:
        return self.page.locator(selector).text_content()
    
    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()
    
    def wait(self, milliseconds: int) -> None:
        self.page.wait_for_timeout(milliseconds)
    
    def mark_success(self) -> None:
        self._success = True
    
    def mark_failed(self, error_message: str) -> None:
        self._success = False
        self._error_message = error_message
    
    @contextmanager
    def run_test(self, test_func: Callable[[], Any]):
        try:
            self.setup()
            result = test_func()
            self.mark_success()
            return result
        except Exception as e:
            self.mark_failed(str(e))
            self.screenshot("error_state")
            raise
        finally:
            self.teardown()
            self._save_results()
    
    def _save_results(self) -> None:
        from scripts.test_manager import TestManager, TestResult
        
        manager = TestManager(self.config)
        
        result = TestResult(
            test_name=self.test_name,
            success=self._success,
            start_time=datetime.now().isoformat(),
            end_time=datetime.now().isoformat(),
            duration_seconds=0,
            error_message=self._error_message,
            screenshots=self._screenshots
        )
        
        manager.save_test_report(result)
        
        for screenshot in self._screenshots:
            path = Path(screenshot)
            if path.exists():
                manager.save_screenshot(path, success=self._success)


class SimpleTest(BaseTest):
    def __init__(self, test_name: Optional[str] = None, **kwargs):
        super().__init__(test_name=test_name, **kwargs)
    
    def run(self, test_func: Callable[[], Any]) -> Any:
        with self.run_test(test_func) as result:
            return result


def create_test(test_name: Optional[str] = None) -> BaseTest:
    return BaseTest(test_name=test_name)


if __name__ == "__main__":
    def example_test():
        test = BaseTest("example_login_test")
        try:
            test.setup()
            
            test.goto_frontend()
            test.screenshot("homepage")
            
            if test.login(account_name="admin"):
                test.screenshot("after_login")
                print("测试成功!")
            else:
                test.mark_failed("登录失败")
                
        except Exception as e:
            test.mark_failed(str(e))
            raise
        finally:
            test.teardown()
    
    example_test()
