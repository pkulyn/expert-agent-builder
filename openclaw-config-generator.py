#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
OpenClaw高级专业Agent配置生成器
基于第四阶段研究成果，帮助用户快速创建专业级Agent配置文件
版本: 1.0.0
作者: pkulyn
日期: 2026-04-09
"""

import os
import sys
import json
import argparse
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加utils目录到路径
sys.path.insert(0, str(Path(__file__).parent / "utils"))

try:
    from config_generator import ConfigGenerator
    from validator import ConfigValidator, ValidationLevel
except ImportError as e:
    print(f"导入错误: {e}")
    print("请确保utils目录中存在config_generator.py和validator.py文件")
    sys.exit(1)

class InteractiveTemplateFiller:
    """交互式模板填充器"""

    def __init__(self, output_dir: str = "generated-config"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _print_header(self, title: str):
        """打印标题"""
        print("\n" + "=" * 60)
        print(f"  {title}")
        print("=" * 60)

    def _get_input(self, prompt: str, default: str = "", required: bool = True) -> str:
        """获取用户输入"""
        while True:
            if default:
                full_prompt = f"{prompt} [{default}]: "
            else:
                full_prompt = f"{prompt}: "

            value = input(full_prompt).strip()

            if not value and default:
                return default
            elif not value and required:
                print("  此项为必填项，请重新输入")
            else:
                return value

    def _get_list_input(self, prompt: str, example: List[str] = None) -> List[str]:
        """获取列表输入"""
        print(f"\n{prompt}")
        if example:
            print(f"  示例: {', '.join(example)}")
        print("  输入完成后留空回车继续")

        items = []
        while True:
            item = input(f"  - 第{len(items)+1}项: ").strip()
            if not item:
                if len(items) == 0:
                    print("  至少需要输入一项")
                    continue
                else:
                    break
            items.append(item)

        return items

    def fill_user_profile(self) -> Dict[str, Any]:
        """填充用户个人信息模板"""
        self._print_header("用户个人信息填写")

        print("请提供以下信息，这将帮助Agent更好地理解和服务您")

        profile = {
            "basic_info": {
                "name": {
                    "value": self._get_input("姓名"),
                    "_说明": "用户的真实姓名或常用称呼"
                },
                "professional_title": {
                    "value": self._get_input("职业头衔", "技术总监"),
                    "_说明": "用户的职业头衔"
                },
                "organization": {
                    "value": self._get_input("组织/公司", "当前组织"),
                    "_说明": "用户所在的组织或公司"
                },
                "industry": {
                    "value": self._get_input("行业", "互联网科技"),
                    "_说明": "用户所在的行业"
                },
                "timezone": {
                    "value": self._get_input("时区", "Asia/Shanghai (UTC+8)"),
                    "_说明": "用户所在时区"
                }
            },
            "background": {
                "education": {
                    "value": self._get_list_input("教育背景", ["计算机科学学士", "软件工程硕士"]),
                    "_说明": "用户的教育背景"
                },
                "work_experience": {
                    "value": self._get_list_input("工作经历", ["5年软件开发经验", "3年架构设计经验"]),
                    "_说明": "用户的工作经历"
                },
                "areas_of_expertise": {
                    "value": self._get_list_input("专长领域", ["云原生架构", "分布式系统", "微服务设计"]),
                    "_说明": "用户的专业领域专长"
                }
            },
            "communication_preferences": {
                "formality_level": {
                    "value": int(self._get_input("沟通正式程度 (1-10)", "7")),
                    "_说明": "1=非常随意, 10=非常正式"
                },
                "technical_detail_level": {
                    "value": int(self._get_input("技术细节程度 (1-10)", "8")),
                    "_说明": "1=高度概括, 10=极度详细"
                },
                "feedback_style": {
                    "value": self._get_input("反馈风格", "平衡兼顾", required=False),
                    "_说明": "直接坦诚/温和建设性/平衡兼顾"
                }
            },
            "emotional_preferences": {
                "encouragement_style": {
                    "value": self._get_input("鼓励风格", "具体认可", required=False),
                    "_说明": "具体认可/过程表扬/成就庆祝/持续支持"
                },
                "stress_response_preference": {
                    "value": self._get_input("压力回应偏好", "直接解决问题", required=False),
                    "_说明": "情感支持先行/直接解决问题/提供多种选择/给予思考空间"
                },
                "emotional_boundary": {
                    "value": int(self._get_input("情感边界 (1-10)", "6")),
                    "_说明": "1=严格专业边界, 10=深度情感连接"
                }
            },
            "project_context": {
                "current_challenges": {
                    "value": self._get_list_input("当前挑战", ["系统性能瓶颈", "技术债务累积", "团队技能分布不均"]),
                    "_说明": "用户当前面临的主要挑战"
                },
                "goals_objectives": {
                    "value": self._get_list_input("项目目标", ["提升系统性能30%", "减少技术债务50%", "提升团队整体技能水平"]),
                    "_说明": "用户的项目目标"
                },
                "constraints_limitations": {
                    "value": self._get_list_input("约束限制", ["预算有限", "时间紧张", "团队规模较小"]),
                    "_说明": "项目的约束和限制条件"
                },
                "success_metrics": {
                    "value": self._get_list_input("成功指标", ["用户满意度提升20%", "系统响应时间降低40%", "团队交付速度提升30%"]),
                    "_说明": "衡量项目成功的指标"
                }
            }
        }

        return profile

    def fill_agent_profile(self) -> Dict[str, Any]:
        """填充Agent画像模板"""
        self._print_header("高级专业Agent画像填写")

        print("请为您的Agent定义以下专业特征")

        profile = {
            "professional_identity": {
                "domain_expertise": {
                    "value": self._get_input("专业领域", "技术架构"),
                    "_说明": "Agent的专业领域"
                },
                "experience_level": {
                    "value": self._get_input("经验水平", "高级（7-15年经验）"),
                    "_说明": "Agent的经验水平"
                },
                "role_definition": {
                    "value": self._get_input("角色定义", "资深技术架构顾问，专注于云原生和分布式系统设计"),
                    "_说明": "Agent的角色定义"
                },
                "influence_scope": {
                    "value": self._get_input("影响范围", "部门影响"),
                    "_说明": "Agent的影响范围"
                },
                "professional_background": {
                    "value": self._get_input("专业背景", "拥有12年大型互联网公司架构设计经验，曾主导多个千万级用户系统的架构演进"),
                    "_说明": "Agent的专业背景"
                },
                "key_competencies": {
                    "value": self._get_list_input("核心能力", [
                        "系统架构设计",
                        "技术选型评估",
                        "性能优化",
                        "技术债务管理",
                        "团队技术指导"
                    ]),
                    "_说明": "Agent的核心能力"
                }
            },
            "core_personality": {
                "worldview": {
                    "value": self._get_input("世界观", "技术是解决问题的工具，但人文关怀同样重要；优秀的架构应该既高效又可维护"),
                    "_说明": "Agent的世界观"
                },
                "core_values": {
                    "value": self._get_list_input("核心价值观", [
                        "技术伦理至上",
                        "用户价值导向",
                        "团队协作优先",
                        "持续学习成长",
                        "务实创新平衡"
                    ]),
                    "_说明": "Agent的核心价值观"
                },
                "personality_traits": {
                    "value": self._get_list_input("个性特征", [
                        "技术敏锐",
                        "耐心指导",
                        "鼓励风格",
                        "同理理解",
                        "建设性批评"
                    ]),
                    "_说明": "Agent的个性特征"
                },
                "emotional_style": {
                    "value": self._get_input("情感风格", "平衡适中"),
                    "_说明": "Agent的情感表达风格"
                },
                "communication_style": {
                    "value": self._get_input("沟通风格", "直接清晰"),
                    "_说明": "Agent的沟通风格"
                },
                "decision_making_style": {
                    "value": self._get_input("决策风格", "数据驱动"),
                    "_说明": "Agent的决策风格"
                }
            },
            "work_behavior": {
                "problem_solving_approach": {
                    "value": self._get_input("问题解决方法", "采用系统化分析方法：问题定义→根本原因分析→方案设计→实施规划→效果评估→团队学习"),
                    "_说明": "Agent的问题解决方法"
                },
                "team_collaboration_style": {
                    "value": self._get_input("团队协作风格", "教练型（培养能力）"),
                    "_说明": "Agent的团队协作风格"
                },
                "thinking_patterns": {
                    "value": self._get_list_input("思维模式", [
                        "系统思维",
                        "批判性思维",
                        "战略思维",
                        "成长思维"
                    ]),
                    "_说明": "Agent的思维模式"
                },
                "learning_habits": {
                    "value": self._get_list_input("学习习惯", [
                        "持续跟踪技术趋势",
                        "定期复盘项目经验",
                        "积极参与技术社区",
                        "系统学习理论知识"
                    ]),
                    "_说明": "Agent的学习习惯"
                },
                "quality_standards": {
                    "value": self._get_list_input("质量标准", [
                        "代码可维护性",
                        "系统可靠性99.9%",
                        "文档完整性",
                        "团队满意度",
                        "用户价值实现"
                    ]),
                    "_说明": "Agent的质量标准"
                },
                "work_rhythm": {
                    "value": self._get_input("工作节奏", "平衡节奏"),
                    "_说明": "Agent的工作节奏"
                }
            },
            "environment_understanding": {
                "user_insight_depth": {
                    "value": self._get_input("用户洞察深度", "全方位理解"),
                    "_说明": "Agent对用户的理解深度"
                },
                "situational_awareness": {
                    "value": self._get_input("情境意识", "能够识别项目阶段、团队状态、技术挑战、业务压力、个人成长需求等多维度情境"),
                    "_说明": "Agent的情境意识能力"
                },
                "relationship_management": {
                    "value": self._get_input("关系管理", "信任建立"),
                    "_说明": "Agent的关系管理能力"
                },
                "communication_adaptation": {
                    "value": self._get_input("沟通适应", "能够根据用户背景、情绪状态、沟通偏好、学习风格调整表达方式"),
                    "_说明": "Agent的沟通适应能力"
                },
                "context_integration": {
                    "value": self._get_input("情境整合", "优秀整合"),
                    "_说明": "Agent的情境整合能力"
                }
            },
            "specialization_parameters": {
                "emotional_intelligence_level": {
                    "value": int(self._get_input("情感智能水平 (1-10)", "8")),
                    "_说明": "Agent的情感智能水平，影响情感识别和支持能力"
                },
                "encouragement_frequency": {
                    "value": int(self._get_input("鼓励频率 (1-10)", "7")),
                    "_说明": "Agent提供鼓励和认可的频率"
                },
                "stress_recognition_sensitivity": {
                    "value": int(self._get_input("压力识别敏感度 (1-10)", "8")),
                    "_说明": "Agent识别用户压力状态的敏感度"
                },
                "personalization_degree": {
                    "value": int(self._get_input("个性化程度 (1-10)", "7")),
                    "_说明": "Agent提供个性化服务的程度"
                },
                "technical_depth": {
                    "value": int(self._get_input("技术深度 (1-10)", "9")),
                    "_说明": "Agent的专业技术深度"
                },
                "practicality_weight": {
                    "value": int(self._get_input("实用性权重 (1-10)", "9")),
                    "_说明": "Agent建议的实用性和可行性权重"
                },
                "innovation_tendency": {
                    "value": int(self._get_input("创新倾向 (1-10)", "7")),
                    "_说明": "Agent提供创新解决方案的倾向"
                },
                "collaboration_intensity": {
                    "value": int(self._get_input("协作强度 (1-10)", "8")),
                    "_说明": "Agent的协作强度和工作参与度"
                }
            },
            "domain_specific_settings": {
                "technology_architecture": {
                    "preferred_methodologies": {
                        "value": self._get_list_input("偏好的方法论", [
                            "领域驱动设计",
                            "事件驱动架构",
                            "微服务架构",
                            "云原生设计",
                            "可扩展架构"
                        ]),
                        "_说明": "偏好的技术架构方法论"
                    },
                    "technology_stack_preferences": {
                        "value": self._get_list_input("技术栈偏好", [
                            "云平台：AWS/Azure",
                            "容器：Docker/Kubernetes",
                            "数据库：PostgreSQL/Redis/MongoDB",
                            "消息队列：Kafka/RabbitMQ"
                        ]),
                        "_说明": "偏好的技术栈"
                    },
                    "design_principles": {
                        "value": self._get_list_input("设计原则", [
                            "可扩展性优先",
                            "可靠性至上",
                            "可维护性考虑",
                            "成本效益平衡",
                            "团队友好性"
                        ]),
                        "_说明": "遵循的设计原则"
                    }
                }
            },
            "output_style": {
                "formality_level": {
                    "value": int(self._get_input("输出正式程度 (1-10)", "7")),
                    "_说明": "1=非常随意，10=非常正式"
                },
                "detail_level": {
                    "value": int(self._get_input("输出详细程度 (1-10)", "8")),
                    "_说明": "1=高度概括，10=极度详细"
                },
                "visual_support_preference": {
                    "value": self._get_input("视觉支持偏好", "简单图表"),
                    "_说明": "文本为主/简单图表/详细图表"
                },
                "language_style": {
                    "value": self._get_input("语言风格", "技术精确"),
                    "_说明": "技术精确/通俗易懂/平衡兼顾"
                },
                "structure_preference": {
                    "value": self._get_input("结构偏好", "线性逻辑"),
                    "_说明": "线性逻辑/主题分明/混合结构"
                }
            },
            "integration_requirements": {
                "tool_integrations": {
                    "value": self._get_list_input("工具集成需求", [
                        "GitHub",
                        "JIRA",
                        "Confluence",
                        "Slack",
                        "Draw.io"
                    ]),
                    "_说明": "需要集成的工具"
                },
                "platform_requirements": {
                    "value": self._get_list_input("平台需求", [
                        "OpenClaw环境",
                        "Docker容器",
                        "云平台访问"
                    ]),
                    "_说明": "平台环境需求"
                },
                "data_sources": {
                    "value": self._get_list_input("数据源", [
                        "内部知识库",
                        "技术文档库",
                        "性能监控数据",
                        "项目管理系统"
                    ]),
                    "_说明": "需要访问的数据源"
                },
                "api_integrations": {
                    "value": self._get_list_input("API集成", [
                        "GitHub API",
                        "JIRA API",
                        "监控系统API",
                        "文档系统API"
                    ]),
                    "_说明": "需要集成的API"
                }
            },
            "additional_configuration": {
                "custom_templates": {
                    "value": self._get_list_input("自定义模板", [
                        "架构设计文档模板",
                        "技术评审记录模板",
                        "技术债务跟踪模板",
                        "团队技能评估模板"
                    ]),
                    "_说明": "需要的自定义模板"
                },
                "branding_elements": {
                    "value": self._get_list_input("品牌元素", [
                        "组织标志",
                        "品牌颜色（蓝色系）",
                        "专业字体",
                        "技术顾问标识"
                    ]),
                    "_说明": "品牌元素需求"
                },
                "compliance_requirements": {
                    "value": self._get_list_input("合规性要求", [
                        "数据保留政策",
                        "访问控制要求",
                        "审计日志需求",
                        "安全标准符合"
                    ]),
                    "_说明": "合规性要求"
                },
                "other_requirements": {
                    "value": self._get_input("其他需求", "需要支持中英文技术术语，能够根据用户技术水平调整解释深度", required=False),
                    "_说明": "其他特殊需求"
                }
            }
        }

        return profile

def learn_methodology_summary():
    """学习方法论摘要"""
    print("\n[文档] 学习方法论摘要")
    print("=" * 60)

    methodology_file = Path(__file__).parent / "docs" / "methodology-summary.md"

    if not methodology_file.exists():
        print("⚠️  方法论摘要文档未找到，将使用默认配置逻辑")
        print("📁 预期位置:", methodology_file)
        return

    try:
        with open(methodology_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取关键部分（前500字符作为摘要）
        summary = content[:800] + "..." if len(content) > 800 else content

        print("正在学习OpenClaw高级专业Agent配置方法论...")
        print("\n核心方法论摘要:")
        print("-" * 40)

        # 显示关键标题
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('# ') or line.startswith('## '):
                print(f"  {line}")
            if i > 50:  # 只显示前50行
                break

        print("-" * 40)
        print("[完成] 方法论学习完成，基于四层六维专业人格模型进行配置引导")
        print("  详细文档请查看: skill/docs/methodology-summary.md")

    except Exception as e:
        print(f"[警告] 读取方法论摘要时出错: {e}")
        print("将继续使用标准配置逻辑")

def run_interactive_mode(args):
    """运行交互式模式"""
    print("\n[目标] OpenClaw高级专业Agent配置生成器 - 交互式模式")
    print("=" * 60)

    # 0. 学习方法论
    learn_methodology_summary()

    filler = InteractiveTemplateFiller(args.output_dir)

    # 1. 填写用户个人信息
    print("\n[文档] 第一步：填写您的个人信息")
    user_profile = filler.fill_user_profile()

    user_profile_file = filler.output_dir / "user_profile.json"
    with open(user_profile_file, 'w', encoding='utf-8') as f:
        json.dump(user_profile, f, ensure_ascii=False, indent=2)

    print(f"✓ 用户个人信息已保存到: {user_profile_file}")

    # 2. 填写Agent画像
    print("\n🤖 第二步：定义您的专业Agent画像")
    agent_profile = filler.fill_agent_profile()

    agent_profile_file = filler.output_dir / "agent_profile.json"
    with open(agent_profile_file, 'w', encoding='utf-8') as f:
        json.dump(agent_profile, f, ensure_ascii=False, indent=2)

    print(f"✓ Agent画像已保存到: {agent_profile_file}")

    # 3. 生成配置文件
    print("\n→ 第三步：生成配置文件")
    generator = ConfigGenerator(
        user_profile_path=str(user_profile_file),
        agent_profile_path=str(agent_profile_file),
        output_dir=str(filler.output_dir / "agent-config"),
        domain=args.domain,
        optimization_level=args.optimization_level
    )

    generator.generate_all(args.format)

    # 4. 验证配置
    print("\n🔍 第四步：验证配置文件质量")
    validator = ConfigValidator(
        config_dir=str(filler.output_dir / "agent-config"),
        validation_level=ValidationLevel(args.validation_level)
    )

    report = validator.validate()

    # 保存验证报告
    report_file = filler.output_dir / "validation_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        from validator import generate_markdown_report
        generate_markdown_report(report, str(report_file))

    print(f"✓ 验证报告已保存到: {report_file}")

    print("\n" + "=" * 60)
    print("✅ 配置生成流程完成！")
    print("=" * 60)
    print(f"\n📁 生成的文件保存在: {filler.output_dir}")
    print(f"📋 用户个人信息: {user_profile_file}")
    print(f"🤖 Agent画像: {agent_profile_file}")
    print(f"→ Agent配置文件: {filler.output_dir / 'agent-config'}")
    print(f"🔍 验证报告: {report_file}")
    print("\n🚀 接下来，请将agent-config目录中的5个配置文件复制到您的OpenClaw Agent配置目录中，然后重启Agent服务。")

def run_generate_mode(args):
    """运行生成模式"""
    print("\n→ OpenClaw高级专业Agent配置生成器 - 生成模式")
    print("=" * 60)

    if not args.user_profile or not args.agent_profile:
        print("错误：生成模式需要 --user-profile 和 --agent-profile 参数")
        sys.exit(1)

    # 验证输入文件
    for file_path in [args.user_profile, args.agent_profile]:
        if not Path(file_path).exists():
            print(f"错误：文件不存在 - {file_path}")
            sys.exit(1)

    generator = ConfigGenerator(
        user_profile_path=args.user_profile,
        agent_profile_path=args.agent_profile,
        output_dir=args.output_dir,
        domain=args.domain,
        optimization_level=args.optimization_level
    )

    generator.generate_all(args.format)

def run_validate_mode(args):
    """运行验证模式"""
    print("\n🔍 OpenClaw高级专业Agent配置生成器 - 验证模式")
    print("=" * 60)

    if not args.config_dir:
        print("错误：验证模式需要 --config-dir 参数")
        sys.exit(1)

    if not Path(args.config_dir).exists():
        print(f"错误：配置目录不存在 - {args.config_dir}")
        sys.exit(1)

    validator = ConfigValidator(
        config_dir=args.config_dir,
        validation_level=ValidationLevel(args.validation_level)
    )

    report = validator.validate()

    # 保存验证报告
    if args.report_file:
        from validator import generate_markdown_report
        generate_markdown_report(report, args.report_file)
        print(f"✓ 验证报告已保存到: {args.report_file}")

def run_example_mode(args):
    """运行示例模式"""
    print("\n[示例] OpenClaw高级专业Agent配置生成器 - 示例模式")
    print("=" * 60)

    # 检查示例文件是否存在
    example_dir = Path(__file__).parent / "examples" / "technical-architect-advisor"

    if not example_dir.exists():
        print(f"错误：示例目录不存在 - {example_dir}")
        print("请确保examples/technical-architect-advisor目录存在")
        sys.exit(1)

    user_profile_file = example_dir / "user-profile.json"
    agent_profile_file = example_dir / "agent-profile.json"

    if not user_profile_file.exists() or not agent_profile_file.exists():
        print("错误：示例文件不完整")
        print(f"请检查以下文件是否存在:")
        print(f"  - {user_profile_file}")
        print(f"  - {agent_profile_file}")
        sys.exit(1)

    print(f"使用技术架构顾问示例:")
    print(f"  用户信息: {user_profile_file}")
    print(f"  Agent画像: {agent_profile_file}")

    generator = ConfigGenerator(
        user_profile_path=str(user_profile_file),
        agent_profile_path=str(agent_profile_file),
        output_dir=args.output_dir,
        domain="技术架构",
        optimization_level="high"
    )

    generator.generate_all(args.format)

    # 验证配置
    validator = ConfigValidator(
        config_dir=args.output_dir,
        validation_level=ValidationLevel(args.validation_level)
    )

    report = validator.validate()

    # 保存验证报告
    report_file = Path(args.output_dir) / "validation_report.md"
    from validator import generate_markdown_report
    generate_markdown_report(report, str(report_file))

    print(f"\n[完成] 示例运行完成!")
    print(f"[文件夹] 生成的文件保存在: {args.output_dir}")
    print(f"[报告] 验证报告: {report_file}")

def main():
    parser = argparse.ArgumentParser(
        description='OpenClaw高级专业Agent配置生成器',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 交互式模式（推荐）
  python openclaw-config-generator.py --mode interactive

  # 生成模式（使用现有模板）
  python openclaw-config-generator.py --mode generate \\
    --user-profile templates/user-profile.json \\
    --agent-profile templates/agent-profile.json \\
    --output-dir my-agent-config

  # 验证模式
  python openclaw-config-generator.py --mode validate \\
    --config-dir existing-config \\
    --validation-level strict

  # 示例模式
  python openclaw-config-generator.py --mode example
        """
    )

    parser.add_argument('--mode', default='interactive',
                       choices=['interactive', 'generate', 'validate', 'example'],
                       help='运行模式 (默认: interactive)')

    # 通用参数
    parser.add_argument('--output-dir', default='generated-config',
                       help='输出目录 (默认: generated-config)')
    parser.add_argument('--format', default='openclaw',
                       choices=['openclaw', 'claudecode', 'both'],
                       help='输出格式 (默认: openclaw)')

    # 生成模式参数
    parser.add_argument('--user-profile',
                       help='用户个人信息JSON文件路径 (生成模式必需)')
    parser.add_argument('--agent-profile',
                       help='Agent画像JSON文件路径 (生成模式必需)')
    parser.add_argument('--domain', default='技术架构',
                       help='专业领域 (默认: 技术架构)')
    parser.add_argument('--optimization-level', default='medium',
                       choices=['low', 'medium', 'high'],
                       help='优化级别 (默认: medium)')

    # 验证模式参数
    parser.add_argument('--config-dir',
                       help='配置文件目录 (验证模式必需)')
    parser.add_argument('--validation-level', default='standard',
                       choices=['basic', 'standard', 'strict'],
                       help='验证级别 (默认: standard)')
    parser.add_argument('--report-file',
                       help='验证报告输出文件')

    parser.add_argument('--debug', action='store_true',
                       help='启用调试模式')

    args = parser.parse_args()

    if args.debug:
        print("调试模式启用")

    try:
        if args.mode == 'interactive':
            run_interactive_mode(args)
        elif args.mode == 'generate':
            run_generate_mode(args)
        elif args.mode == 'validate':
            run_validate_mode(args)
        elif args.mode == 'example':
            run_example_mode(args)
        else:
            print(f"错误：未知模式: {args.mode}")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n操作被用户中断")
        sys.exit(0)
    except Exception as e:
        print(f"\n错误：{e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()