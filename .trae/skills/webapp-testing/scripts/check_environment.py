#!/usr/bin/env python3
"""
环境检测和安装脚本
检测并安装 Playwright 及浏览器
"""
import subprocess
import sys
import shutil
import os
from pathlib import Path


def check_python() -> dict:
    """检测 Python 版本"""
    version = sys.version_info
    result = {
        "installed": True,
        "version": f"{version.major}.{version.minor}.{version.micro}",
        "valid": version.major >= 3 and version.minor >= 8,
        "message": ""
    }
    if not result["valid"]:
        result["message"] = f"需要 Python 3.8 或更高版本，当前版本: {result['version']}"
    else:
        result["message"] = f"Python 版本: {result['version']} ✓"
    return result


def check_playwright() -> dict:
    """检测 Playwright 是否已安装"""
    try:
        import playwright
        version = getattr(playwright, '__version__', 'unknown')
        return {
            "installed": True,
            "version": version,
            "message": f"Playwright 已安装: {version} ✓"
        }
    except ImportError:
        return {
            "installed": False,
            "version": None,
            "message": "Playwright 未安装"
        }


def check_browsers() -> dict:
    """检测浏览器是否已安装"""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "--dry-run", "chromium"],
            capture_output=True,
            text=True,
            timeout=30
        )
        output = result.stdout.lower() + result.stderr.lower()
        if "download" not in output or "already" in output or result.returncode == 0:
            return {
                "installed": True,
                "message": "Chromium 浏览器已安装 ✓"
            }
        else:
            return {
                "installed": False,
                "message": "Chromium 浏览器未安装"
            }
    except subprocess.TimeoutExpired:
        return {
            "installed": False,
            "message": "检测浏览器超时"
        }
    except Exception as e:
        return {
            "installed": False,
            "message": f"检测浏览器时出错: {e}"
        }


def install_playwright() -> dict:
    """安装 Playwright"""
    try:
        print("正在安装 Playwright...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "playwright"],
            capture_output=True,
            text=True,
            timeout=300
        )
        if result.returncode == 0:
            return {
                "success": True,
                "message": "Playwright 安装完成 ✓"
            }
        else:
            return {
                "success": False,
                "message": f"安装失败: {result.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "安装超时"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"安装出错: {e}"
        }


def install_browsers() -> dict:
    """安装浏览器"""
    try:
        print("正在安装 Chromium 浏览器...")
        result = subprocess.run(
            [sys.executable, "-m", "playwright", "install", "chromium"],
            capture_output=True,
            text=True,
            timeout=600
        )
        if result.returncode == 0:
            return {
                "success": True,
                "message": "浏览器安装完成 ✓"
            }
        else:
            return {
                "success": False,
                "message": f"安装失败: {result.stderr}"
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "message": "安装超时"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"安装出错: {e}"
        }


def check_all() -> dict:
    """检测所有环境"""
    return {
        "python": check_python(),
        "playwright": check_playwright(),
        "browsers": check_browsers() if check_playwright()["installed"] else {"installed": False, "message": "需要先安装 Playwright"}
    }


def ensure_environment(auto_install: bool = True) -> bool:
    """
    确保测试环境就绪
    
    Args:
        auto_install: 是否自动安装缺失的依赖
        
    Returns:
        bool: 环境是否就绪
    """
    print("=" * 60)
    print("检测测试环境...")
    print("=" * 60)
    
    python_result = check_python()
    print(f"  [Python] {python_result['message']}")
    if not python_result["valid"]:
        print("\n环境检测失败: Python 版本不符合要求")
        return False
    
    playwright_result = check_playwright()
    print(f"  [Playwright] {playwright_result['message']}")
    
    if not playwright_result["installed"]:
        if auto_install:
            install_result = install_playwright()
            print(f"    -> {install_result['message']}")
            if not install_result["success"]:
                return False
            playwright_result = check_playwright()
        else:
            print("\n环境检测失败: Playwright 未安装")
            return False
    
    browsers_result = check_browsers()
    print(f"  [Browsers] {browsers_result['message']}")
    
    if not browsers_result["installed"]:
        if auto_install:
            install_result = install_browsers()
            print(f"    -> {install_result['message']}")
            if not install_result["success"]:
                return False
        else:
            print("\n环境检测失败: 浏览器未安装")
            return False
    
    print("=" * 60)
    print("测试环境就绪! ✓")
    print("=" * 60)
    return True


def main():
    import argparse
    parser = argparse.ArgumentParser(description="检测并安装测试环境")
    parser.add_argument("--install", action="store_true", default=True,
                        help="自动安装缺失的依赖 (默认: True)")
    parser.add_argument("--check-only", action="store_true",
                        help="仅检测，不安装")
    args = parser.parse_args()
    
    if args.check_only:
        results = check_all()
        print("\n环境检测结果:")
        for name, result in results.items():
            status = "✓" if result.get("installed") or result.get("valid") else "✗"
            print(f"  [{status}] {name}: {result['message']}")
    else:
        success = ensure_environment(auto_install=args.install)
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
