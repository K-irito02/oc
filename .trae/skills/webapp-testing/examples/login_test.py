#!/usr/bin/env python3
"""
示例测试脚本 - 登录测试
演示如何使用 BaseTest 基类进行测试
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.base_test import BaseTest
from config.test_config import TestConfig


def test_admin_login():
    test = BaseTest("admin_login_test")
    try:
        test.setup()
        
        print("开始测试管理员登录...")
        
        test.goto_frontend("/login")
        test.screenshot("login_page")
        
        if test.login(account_name="admin"):
            test.screenshot("after_admin_login")
            test.mark_success()
            print("管理员登录测试成功!")
            return True
        else:
            test.mark_failed("管理员登录失败")
            print("管理员登录测试失败!")
            return False
            
    except Exception as e:
        test.mark_failed(str(e))
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


def test_user_login():
    test = BaseTest("user_login_test")
    try:
        test.setup()
        
        print("开始测试普通用户登录...")
        
        test.goto_frontend("/login")
        test.screenshot("login_page")
        
        if test.login(account_name="zhangsan"):
            test.screenshot("after_user_login")
            test.mark_success()
            print("普通用户登录测试成功!")
            return True
        else:
            test.mark_failed("普通用户登录失败")
            print("普通用户登录测试失败!")
            return False
            
    except Exception as e:
        test.mark_failed(str(e))
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


def test_homepage():
    test = BaseTest("homepage_test")
    try:
        test.setup()
        
        print("开始测试首页...")
        
        test.goto_frontend()
        test.screenshot("homepage")
        
        test.wait_for_selector('body')
        
        test.mark_success()
        print("首页测试成功!")
        return True
            
    except Exception as e:
        test.mark_failed(str(e))
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="示例测试脚本")
    parser.add_argument("--test", choices=["admin", "user", "homepage", "all"], 
                        default="all", help="要运行的测试")
    args = parser.parse_args()
    
    results = []
    
    if args.test in ["admin", "all"]:
        results.append(("管理员登录", test_admin_login()))
    
    if args.test in ["user", "all"]:
        results.append(("普通用户登录", test_user_login()))
    
    if args.test in ["homepage", "all"]:
        results.append(("首页", test_homepage()))
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    sys.exit(0 if all_passed else 1)
