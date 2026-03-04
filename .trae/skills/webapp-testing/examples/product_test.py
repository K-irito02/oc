#!/usr/bin/env python3
"""
示例测试脚本 - 产品页面测试
演示如何使用 BaseTest 基类测试产品相关功能
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.base_test import BaseTest
from config.test_config import TestConfig


def test_product_list():
    test = BaseTest("product_list_test")
    try:
        test.setup()
        
        print("开始测试产品列表页面...")
        
        test.goto_frontend("/products")
        test.screenshot("product_list_page")
        
        test.wait_for_selector('body')
        test.wait(2000)
        
        test.screenshot("product_list_loaded")
        
        test.mark_success()
        print("产品列表页面测试成功!")
        return True
            
    except Exception as e:
        test.mark_failed(str(e))
        test.screenshot("error_state")
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


def test_product_detail():
    test = BaseTest("product_detail_test")
    try:
        test.setup()
        
        print("开始测试产品详情页面...")
        
        test.goto_frontend("/products/qtcreator-pro")
        test.screenshot("product_detail_page")
        
        test.wait_for_selector('body')
        test.wait(2000)
        
        test.screenshot("product_detail_loaded")
        
        test.mark_success()
        print("产品详情页面测试成功!")
        return True
            
    except Exception as e:
        test.mark_failed(str(e))
        test.screenshot("error_state")
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


def test_admin_product_management():
    test = BaseTest("admin_product_test")
    try:
        test.setup()
        
        print("开始测试管理员产品管理...")
        
        if not test.login(account_name="admin"):
            test.mark_failed("管理员登录失败")
            return False
        
        test.goto_frontend("/admin/products")
        test.screenshot("admin_product_list")
        
        test.wait_for_selector('body')
        test.wait(2000)
        
        test.screenshot("admin_product_loaded")
        
        test.mark_success()
        print("管理员产品管理测试成功!")
        return True
            
    except Exception as e:
        test.mark_failed(str(e))
        test.screenshot("error_state")
        print(f"测试异常: {e}")
        return False
    finally:
        test.teardown()
        test._save_results()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="产品页面测试脚本")
    parser.add_argument("--test", choices=["list", "detail", "admin", "all"], 
                        default="all", help="要运行的测试")
    args = parser.parse_args()
    
    results = []
    
    if args.test in ["list", "all"]:
        results.append(("产品列表", test_product_list()))
    
    if args.test in ["detail", "all"]:
        results.append(("产品详情", test_product_detail()))
    
    if args.test in ["admin", "all"]:
        results.append(("管理员产品管理", test_admin_product_management()))
    
    print("\n" + "=" * 50)
    print("测试结果汇总:")
    print("=" * 50)
    for name, success in results:
        status = "✓ 通过" if success else "✗ 失败"
        print(f"  {name}: {status}")
    
    all_passed = all(r[1] for r in results)
    sys.exit(0 if all_passed else 1)
