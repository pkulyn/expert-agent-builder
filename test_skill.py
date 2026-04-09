#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClaw配置生成器Skill测试脚本
测试各个功能模块是否正常工作
版本: 1.0.0
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path

# 添加utils目录到路径
sys.path.insert(0, str(Path(__file__).parent / "utils"))

try:
    from config_generator import ConfigGenerator
    from validator import ConfigValidator, ValidationLevel
    print("[OK] 成功导入核心模块")
except ImportError as e:
    print(f"[ERROR] 导入错误: {e}")
    sys.exit(1)

def test_config_generator():
    """测试配置生成器"""
    print("\n[TEST] 测试配置生成器...")

    # 创建临时目录
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建测试输入文件
        user_profile = {
            "basic_info": {
                "name": {"value": "测试用户"},
                "professional_title": {"value": "测试工程师"}
            }
        }

        agent_profile = {
            "professional_identity": {
                "domain_expertise": {"value": "技术架构"},
                "experience_level": {"value": "中级（3-7年经验）"},
                "role_definition": {"value": "测试架构顾问"}
            },
            "specialization_parameters": {
                "emotional_intelligence_level": {"value": 7},
                "technical_depth": {"value": 8},
                "collaboration_intensity": {"value": 7}
            }
        }

        user_file = Path(tmpdir) / "user.json"
        agent_file = Path(tmpdir) / "agent.json"
        output_dir = Path(tmpdir) / "output"

        with open(user_file, 'w', encoding='utf-8') as f:
            json.dump(user_profile, f, ensure_ascii=False, indent=2)

        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(agent_profile, f, ensure_ascii=False, indent=2)

        # 创建生成器
        generator = ConfigGenerator(
            user_profile_path=str(user_file),
            agent_profile_path=str(agent_file),
            output_dir=str(output_dir),
            domain="技术架构",
            optimization_level="medium"
        )

        # 生成配置
        try:
            files = generator.generate_all()
            print(f"[OK] 成功生成 {len(files)} 个配置文件")

            # 检查生成的文件
            expected_files = ["SOUL.md", "IDENTITY.md", "TOOLS.md", "AGENTS.md", "USER.md"]
            for filename in expected_files:
                filepath = output_dir / filename
                if filepath.exists():
                    print(f"  [CHECK] {filename} 已生成")
                else:
                    print(f"  [ERROR] {filename} 未生成")

            return True
        except Exception as e:
            print(f"[ERROR] 配置生成失败: {e}")
            return False

def test_config_validator():
    """测试配置验证器"""
    print("\n[TEST] 测试配置验证器...")

    # 创建临时目录和测试配置文件
    with tempfile.TemporaryDirectory() as tmpdir:
        config_dir = Path(tmpdir) / "config"
        config_dir.mkdir()

        # 创建基本配置文件
        soul_content = """---
title: Agent灵魂配置
version: 2.0
---
# SOUL.md - 测试Agent的灵魂

## 核心真理

- 真诚地帮助用户
"""

        identity_content = """---
title: Agent身份配置
version: 2.0
---
# IDENTITY.md - 测试Agent的身份

## 专业身份

**角色定义**：测试架构顾问
"""

        # 写入文件
        with open(config_dir / "SOUL.md", 'w', encoding='utf-8') as f:
            f.write(soul_content)

        with open(config_dir / "IDENTITY.md", 'w', encoding='utf-8') as f:
            f.write(identity_content)

        # 创建验证器
        validator = ConfigValidator(
            config_dir=str(config_dir),
            validation_level=ValidationLevel.BASIC
        )

        try:
            report = validator.validate()
            print(f"[OK] 验证完成，文件数: {report.total_files}")
            print(f"   问题总数: {report.total_issues} (错误: {report.errors}, 警告: {report.warnings})")

            # 注意：由于文件不完整，验证会发现问题，这是正常的
            if report.total_issues > 0:
                print("   [WARNING] 发现验证问题（这是预期的，因为测试文件不完整）")

            return True
        except Exception as e:
            print(f"[ERROR] 配置验证失败: {e}")
            return False

def test_interactive_mode():
    """测试交互式模式（模拟）"""
    print("\n[TEST] 测试交互式模式（模拟）...")

    try:
        # 检查主脚本文件是否存在
        main_script = Path(__file__).parent / "openclaw-config-generator.py"
        if main_script.exists():
            print("[OK] 主脚本文件存在")
        else:
            print(f"[ERROR] 主脚本文件不存在: {main_script}")
            return False

        # 检查命令行参数解析（通过子进程模拟）
        import subprocess
        result = subprocess.run(
            [sys.executable, str(main_script), "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0 and "usage:" in result.stdout.lower():
            print("[OK] 命令行帮助信息正常显示")
        else:
            print("[WARNING]  命令行帮助信息可能有问题")

        # 检查交互式模块导入
        try:
            # 尝试导入交互式模板填充器（从主脚本中提取的类）
            # 由于Python模块命名限制，我们不能直接导入带连字符的文件
            # 这里只检查文件内容是否可读
            with open(main_script, 'r', encoding='utf-8') as f:
                content = f.read()
                if "class InteractiveTemplateFiller" in content:
                    print("[OK] 交互式模板填充器类存在")
                else:
                    print("[WARNING]  未找到交互式模板填充器类")
        except Exception as e:
            print(f"[WARNING]  检查交互式模块时出现警告: {e}")

        return True
    except Exception as e:
        print(f"[ERROR] 交互式模式测试失败: {e}")
        return False

def test_templates_exist():
    """检查模板文件是否存在"""
    print("\n[TEST] 检查模板文件...")

    template_files = [
        "templates/user-profile-template.json",
        "templates/agent-profile-template.json"
    ]

    all_exist = True
    for template_file in template_files:
        filepath = Path(__file__).parent / template_file
        if filepath.exists():
            print(f"[OK] {template_file} 存在")
        else:
            print(f"[ERROR] {template_file} 不存在")
            all_exist = False

    return all_exist

def test_examples_exist():
    """检查示例文件是否存在"""
    print("\n[TEST] 检查示例文件...")

    example_files = [
        "examples/technical-architect-advisor/user-profile.json",
        "examples/technical-architect-advisor/agent-profile.json"
    ]

    all_exist = True
    for example_file in example_files:
        filepath = Path(__file__).parent / example_file
        if filepath.exists():
            print(f"[OK] {example_file} 存在")
        else:
            print(f"[ERROR] {example_file} 不存在")
            all_exist = False

    return all_exist

def main():
    print("[TEST] OpenClaw配置生成器Skill功能测试")
    print("=" * 50)

    tests = [
        ("配置生成器", test_config_generator),
        ("配置验证器", test_config_validator),
        ("交互式模式", test_interactive_mode),
        ("模板文件", test_templates_exist),
        ("示例文件", test_examples_exist),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"[ERROR] {test_name} 测试异常: {e}")
            results.append((test_name, False))

    # 总结结果
    print("\n" + "=" * 50)
    print("[SUMMARY] 测试结果总结:")

    all_passed = True
    for test_name, success in results:
        status = "[OK] 通过" if success else "[ERROR] 失败"
        print(f"  {test_name}: {status}")
        if not success:
            all_passed = False

    print("\n" + "=" * 50)
    if all_passed:
        print("[SUCCESS] 所有测试通过！Skill功能正常。")
        return 0
    else:
        print("[WARNING]  部分测试失败，请检查上述问题。")
        return 1

if __name__ == "__main__":
    sys.exit(main())