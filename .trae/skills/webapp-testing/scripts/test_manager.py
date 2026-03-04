#!/usr/bin/env python3
"""
测试管理脚本
管理测试目录创建、测试执行和结果清理
"""
import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from dataclasses import dataclass, asdict

sys.path.insert(0, str(Path(__file__).parent.parent))
from config.test_config import TestConfig


@dataclass
class TestResult:
    test_name: str
    success: bool
    start_time: str
    end_time: str
    duration_seconds: float
    error_message: Optional[str] = None
    screenshots: List[str] = None
    
    def __post_init__(self):
        if self.screenshots is None:
            self.screenshots = []


class TestManager:
    def __init__(self, config: Optional[TestConfig] = None):
        self.config = config or TestConfig()
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        self.config.ensure_directories()
    
    def create_test_directories(self) -> Dict[str, Path]:
        self._ensure_directories()
        return {
            "output": self.config.TEST_OUTPUT_DIR,
            "screenshots": self.config.SCREENSHOTS_DIR,
            "success_screenshots": self.config.SUCCESS_SCREENSHOTS_DIR,
            "failed_screenshots": self.config.FAILED_SCREENSHOTS_DIR,
            "scripts": self.config.SCRIPTS_DIR,
            "success_scripts": self.config.SUCCESS_SCRIPTS_DIR,
            "failed_scripts": self.config.FAILED_SCRIPTS_DIR,
            "reports": self.config.REPORTS_DIR,
        }
    
    def get_timestamp_name(self, prefix: str = "test") -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}"
    
    def save_screenshot(self, screenshot_path: Path, success: bool = True) -> Path:
        if not screenshot_path.exists():
            raise FileNotFoundError(f"截图文件不存在: {screenshot_path}")
        
        target_dir = self.config.SUCCESS_SCREENSHOTS_DIR if success else self.config.FAILED_SCREENSHOTS_DIR
        target_path = target_dir / screenshot_path.name
        
        if screenshot_path != target_path:
            shutil.copy2(screenshot_path, target_path)
        
        return target_path
    
    def save_script(self, script_path: Path, success: bool = True) -> Path:
        if not script_path.exists():
            raise FileNotFoundError(f"脚本文件不存在: {script_path}")
        
        target_dir = self.config.SUCCESS_SCRIPTS_DIR if success else self.config.FAILED_SCRIPTS_DIR
        target_path = target_dir / script_path.name
        
        if script_path != target_path:
            shutil.copy2(script_path, target_path)
        
        return target_path
    
    def cleanup_failed_files(self) -> Dict[str, List[str]]:
        cleaned = {
            "scripts": [],
            "screenshots": []
        }
        
        for file_path in self.config.FAILED_SCRIPTS_DIR.glob("*.py"):
            try:
                file_path.unlink()
                cleaned["scripts"].append(str(file_path))
            except Exception as e:
                print(f"删除失败脚本失败: {file_path}, 错误: {e}")
        
        for file_path in self.config.FAILED_SCREENSHOTS_DIR.glob("*.png"):
            try:
                file_path.unlink()
                cleaned["screenshots"].append(str(file_path))
            except Exception as e:
                print(f"删除失败截图失败: {file_path}, 错误: {e}")
        
        return cleaned
    
    def save_test_report(self, result: TestResult) -> Path:
        report_path = self.config.get_report_path(result.test_name)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(result), f, ensure_ascii=False, indent=2)
        
        return report_path
    
    def run_test_script(self, script_path: Path, timeout: int = 300) -> TestResult:
        test_name = script_path.stem
        start_time = datetime.now()
        
        print(f"执行测试: {test_name}")
        print(f"脚本路径: {script_path}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=script_path.parent
            )
            
            success = result.returncode == 0
            error_message = result.stderr if not success else None
            
            if success:
                print("测试成功 ✓")
            else:
                print(f"测试失败 ✗\n{error_message}")
                
        except subprocess.TimeoutExpired:
            success = False
            error_message = f"测试超时 (超过 {timeout} 秒)"
            print(f"测试超时 ✗")
        except Exception as e:
            success = False
            error_message = str(e)
            print(f"测试异常 ✗: {e}")
        
        end_time = datetime.now()
        
        screenshots = list(self.config.SCREENSHOTS_DIR.glob(f"{test_name}*.png"))
        
        test_result = TestResult(
            test_name=test_name,
            success=success,
            start_time=start_time.isoformat(),
            end_time=end_time.isoformat(),
            duration_seconds=(end_time - start_time).total_seconds(),
            error_message=error_message,
            screenshots=[str(s) for s in screenshots]
        )
        
        self.save_script(script_path, success=success)
        
        for screenshot in screenshots:
            self.save_screenshot(screenshot, success=success)
        
        self.save_test_report(test_result)
        
        return test_result
    
    def get_test_materials(self) -> List[Path]:
        materials_dir = self.config.TEST_MATERIALS_DIR
        if not materials_dir.exists():
            return []
        return list(materials_dir.glob("*"))
    
    def list_test_results(self, success_only: bool = False) -> List[Dict[str, Any]]:
        results = []
        
        for report_file in self.config.REPORTS_DIR.glob("*.json"):
            try:
                with open(report_file, 'r', encoding='utf-8') as f:
                    result = json.load(f)
                    if not success_only or result.get("success"):
                        results.append(result)
            except Exception as e:
                print(f"读取报告失败: {report_file}, 错误: {e}")
        
        return sorted(results, key=lambda x: x.get("start_time", ""), reverse=True)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="测试管理工具")
    parser.add_argument("command", choices=["init", "cleanup", "list", "run"],
                        help="要执行的命令")
    parser.add_argument("--script", type=str, help="要运行的测试脚本路径")
    parser.add_argument("--timeout", type=int, default=300, help="测试超时时间(秒)")
    parser.add_argument("--success-only", action="store_true", help="仅显示成功的测试结果")
    
    args = parser.parse_args()
    
    manager = TestManager()
    
    if args.command == "init":
        dirs = manager.create_test_directories()
        print("测试目录已创建:")
        for name, path in dirs.items():
            print(f"  {name}: {path}")
    
    elif args.command == "cleanup":
        cleaned = manager.cleanup_failed_files()
        print("清理完成:")
        print(f"  删除脚本: {len(cleaned['scripts'])} 个")
        print(f"  删除截图: {len(cleaned['screenshots'])} 个")
    
    elif args.command == "list":
        results = manager.list_test_results(success_only=args.success_only)
        if not results:
            print("没有找到测试结果")
        else:
            print(f"找到 {len(results)} 个测试结果:")
            for result in results:
                status = "✓" if result.get("success") else "✗"
                print(f"  [{status}] {result['test_name']} - {result['duration_seconds']:.2f}s")
    
    elif args.command == "run":
        if not args.script:
            print("错误: 需要指定 --script 参数")
            sys.exit(1)
        
        script_path = Path(args.script)
        if not script_path.exists():
            print(f"错误: 脚本不存在: {script_path}")
            sys.exit(1)
        
        result = manager.run_test_script(script_path, timeout=args.timeout)
        sys.exit(0 if result.success else 1)


if __name__ == "__main__":
    main()
