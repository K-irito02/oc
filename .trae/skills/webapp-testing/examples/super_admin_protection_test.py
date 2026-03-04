#!/usr/bin/env python3
"""
示例测试脚本 - 超级管理员保护功能测试
验证管理后台用户管理中超级管理员账号不能被锁定或禁用
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.base_test import BaseTest


def test_super_admin_protection():
    test = BaseTest("super_admin_protection")
    
    try:
        test.setup()
        
        test.goto_frontend("/login")
        test.screenshot("01_login_page")
        
        admin = test.config.get_admin_account()
        print(f"使用账号: {admin.email}")
        
        email_input = test.page.get_by_role("textbox").first
        email_input.fill(admin.email)
        
        password_input = test.page.get_by_role("textbox").nth(1)
        password_input.fill(admin.password)
        
        login_btn = test.page.get_by_role("button", name="登录")
        login_btn.click()
        
        test.page.wait_for_load_state("networkidle")
        test.page.wait_for_timeout(2000)
        test.screenshot("02_after_login")
        
        current_url = test.page.url
        print(f"登录后 URL: {current_url}")
        
        if "login" in current_url:
            print("登录可能失败，检查错误信息...")
            error_msg = test.page.locator('.ant-message, .error, [role="alert"]').first
            if error_msg.count() > 0:
                print(f"错误信息: {error_msg.inner_text()}")
            test.mark_failed("登录失败，仍在登录页面")
            return False
        
        test.page.goto(f"{test.config.FRONTEND_URL}/admin/users")
        test.page.wait_for_load_state("networkidle")
        test.page.wait_for_timeout(3000)
        test.screenshot("03_users_page")
        
        table = test.page.locator('.ant-table, table')
        if table.count() == 0:
            page_text = test.page.inner_text('body')
            print(f"页面文本: {page_text[:500]}")
            test.mark_failed("用户管理页面未找到表格")
            return False
        
        print("找到表格")
        rows = table.locator('tbody tr')
        row_count = rows.count()
        print(f"找到 {row_count} 行用户数据")
        
        admin_row = None
        for i in range(row_count):
            row = rows.nth(i)
            row_text = row.inner_text()
            if "admin" in row_text.lower() or "SUPER_ADMIN" in row_text:
                admin_row = row
                print(f"找到超级管理员行 (第 {i+1} 行)")
                break
        
        if not admin_row:
            test.mark_failed("未找到超级管理员行")
            return False
        
        action_cell = admin_row.locator('td:last-child')
        action_text = action_cell.inner_text()
        print(f"操作列内容: {action_text}")
        
        if "超级管理员受保护" in action_text or "Super Admin Protected" in action_text:
            print("✅ 前端验证通过: 超级管理员显示保护提示")
            test.mark_success()
            return True
        
        lock_btn = action_cell.locator('button:has-text("锁定"), button:has-text("Lock")')
        ban_btn = action_cell.locator('button:has-text("禁用"), button:has-text("Ban")')
        
        if lock_btn.count() == 0 and ban_btn.count() == 0:
            print("✅ 前端验证通过: 超级管理员没有锁定/禁用按钮")
            test.mark_success()
            return True
        
        test.mark_failed("前端验证失败: 超级管理员仍显示锁定/禁用按钮")
        return False
            
    except Exception as e:
        test.mark_failed(str(e))
        print(f"❌ 测试失败: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="超级管理员保护功能测试")
    args = parser.parse_args()
    
    success = test_super_admin_protection()
    sys.exit(0 if success else 1)
