#!/usr/bin/env python3
"""
测试配置文件
集中管理测试相关的配置信息
"""
import os
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class TestAccount:
    username: str
    email: str
    password: str
    role: str
    description: str = ""


class TestConfig:
    SKILL_DIR = Path(__file__).parent.parent.resolve()
    BASE_DIR = Path("E:/oc").resolve()
    
    PROJECT_DIR = BASE_DIR / "oc-platform"
    
    TEST_OUTPUT_DIR = BASE_DIR / "test-output"
    SCREENSHOTS_DIR = TEST_OUTPUT_DIR / "screenshots"
    SUCCESS_SCREENSHOTS_DIR = SCREENSHOTS_DIR / "success"
    FAILED_SCREENSHOTS_DIR = SCREENSHOTS_DIR / "failed"
    SCRIPTS_DIR = TEST_OUTPUT_DIR / "scripts"
    SUCCESS_SCRIPTS_DIR = SCRIPTS_DIR / "success"
    FAILED_SCRIPTS_DIR = SCRIPTS_DIR / "failed"
    REPORTS_DIR = TEST_OUTPUT_DIR / "reports"
    
    TEST_MATERIALS_DIR = BASE_DIR / "Front-end testing"
    
    FRONTEND_URL = "http://localhost:5173"
    BACKEND_URL = "http://localhost:8081"
    API_BASE_URL = f"{BACKEND_URL}/api/v1"
    
    DEFAULT_TIMEOUT = 30000
    NAVIGATION_TIMEOUT = 60000
    ACTION_TIMEOUT = 10000
    DEFAULT_RETRIES = 3
    
    HEADLESS = True
    VIEWPORT = {"width": 1920, "height": 1080}
    LOCALE = "zh-CN"
    TIMEZONE = "Asia/Shanghai"
    
    TEST_ACCOUNTS: Dict[str, TestAccount] = {
        "admin": TestAccount(
            username="admin",
            email="admin@ocplatform.com",
            password="Admin@123456",
            role="SUPER_ADMIN",
            description="超级管理员，拥有所有权限"
        ),
        "zhangsan": TestAccount(
            username="zhangsan",
            email="zhangsan@example.com",
            password="Test@123456",
            role="USER",
            description="普通用户，Qt爱好者"
        ),
        "lisi": TestAccount(
            username="lisi",
            email="lisi@example.com",
            password="Test@123456",
            role="USER",
            description="普通用户，独立开发者"
        ),
        "wangwu": TestAccount(
            username="wangwu",
            email="wangwu@example.com",
            password="Test@123456",
            role="VIP",
            description="VIP用户，资深Qt开发"
        ),
        "dev_chen": TestAccount(
            username="dev_chen",
            email="chen@example.com",
            password="Test@123456",
            role="USER",
            description="普通用户，热爱开源"
        ),
        "test_banned": TestAccount(
            username="test_banned",
            email="banned@example.com",
            password="Test@123456",
            role="USER",
            description="被封禁用户，用于测试封禁状态"
        ),
    }
    
    @classmethod
    def get_account(cls, name: str) -> Optional[TestAccount]:
        return cls.TEST_ACCOUNTS.get(name)
    
    @classmethod
    def get_accounts_by_role(cls, role: str) -> List[TestAccount]:
        return [acc for acc in cls.TEST_ACCOUNTS.values() if acc.role == role]
    
    @classmethod
    def get_admin_account(cls) -> TestAccount:
        return cls.TEST_ACCOUNTS["admin"]
    
    @classmethod
    def get_user_account(cls) -> TestAccount:
        return cls.TEST_ACCOUNTS["zhangsan"]
    
    @classmethod
    def ensure_directories(cls) -> None:
        for directory in [
            cls.TEST_OUTPUT_DIR,
            cls.SCREENSHOTS_DIR,
            cls.SUCCESS_SCREENSHOTS_DIR,
            cls.FAILED_SCREENSHOTS_DIR,
            cls.SCRIPTS_DIR,
            cls.SUCCESS_SCRIPTS_DIR,
            cls.FAILED_SCRIPTS_DIR,
            cls.REPORTS_DIR,
        ]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def get_screenshot_path(cls, name: str, success: bool = True) -> Path:
        directory = cls.SUCCESS_SCREENSHOTS_DIR if success else cls.FAILED_SCREENSHOTS_DIR
        return directory / f"{name}.png"
    
    @classmethod
    def get_script_path(cls, name: str, success: bool = True) -> Path:
        directory = cls.SUCCESS_SCRIPTS_DIR if success else cls.FAILED_SCRIPTS_DIR
        return directory / f"{name}.py"
    
    @classmethod
    def get_report_path(cls, name: str) -> Path:
        return cls.REPORTS_DIR / f"{name}.json"
    
    @classmethod
    def get_test_material_path(cls, filename: str) -> Path:
        return cls.TEST_MATERIALS_DIR / filename


def get_config() -> TestConfig:
    return TestConfig()


if __name__ == "__main__":
    config = TestConfig()
    print("测试配置信息:")
    print(f"  基础目录: {config.BASE_DIR.resolve()}")
    print(f"  项目目录: {config.PROJECT_DIR.resolve()}")
    print(f"  测试输出目录: {config.TEST_OUTPUT_DIR.resolve()}")
    print(f"  前端URL: {config.FRONTEND_URL}")
    print(f"  后端URL: {config.BACKEND_URL}")
    print(f"\n测试账号:")
    for name, account in config.TEST_ACCOUNTS.items():
        print(f"  {name}: {account.email} ({account.role})")
