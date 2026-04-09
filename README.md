# 专家级Agent构建器（Expert Agent Builder）

基于四层六维专业人格模型研究成果开发的配置生成工具，帮助用户快速创建专家级Agent配置文件。

## 特性

- **交互式引导**：逐步引导用户提供个人信息和Agent画像
- **智能生成**：基于四层六维专业人格模型生成高质量配置
- **多维度验证**：完整性、一致性、质量三重验证
- **领域适配**：支持技术架构、法律、商业、创意、医学等专业领域
- **情感智能集成**：内置情感识别、支持、鼓励等人性化功能
- **一键运行**：提供完整的示例和运行脚本

## 快速开始

### 安装

确保系统中已安装Python 3.8或更高版本。

```bash
python --version
```

### 使用方式

#### 1. 交互式模式（推荐）

引导用户逐步填写信息并生成配置：

```bash
python openclaw-config-generator.py --mode interactive
```

#### 2. 生成模式

基于现有模板文件生成配置：

```bash
python openclaw-config-generator.py \
  --mode generate \
  --user-profile templates/user-profile.json \
  --agent-profile templates/agent-profile.json \
  --output-dir my-agent-config
```

#### 3. 验证模式

验证现有配置的质量：

```bash
python openclaw-config-generator.py \
  --mode validate \
  --config-dir existing-config \
  --validation-level strict
```

#### 4. 示例模式

运行技术架构顾问示例：

```bash
python openclaw-config-generator.py --mode example
```

#### 5. 多格式输出支持

支持三种输出格式：

1. **OpenClaw格式** (`--format openclaw`)：生成5个配置文件（SOUL.md、IDENTITY.md、TOOLS.md、AGENTS.md、USER.md）
2. **Claude Code格式** (`--format claudecode`)：生成2个配置文件（CLAUDE.md 和 Agent配置文件）
3. **双格式输出** (`--format both`)：同时生成OpenClaw和Claude Code格式配置

**示例**：
```bash
# 生成Claude Code格式配置
python openclaw-config-generator.py \
  --mode generate \
  --user-profile user-profile.json \
  --agent-profile agent-profile.json \
  --output-dir my-claudecode-config \
  --format claudecode

# 双格式输出（OpenClaw + Claude Code）
python openclaw-config-generator.py \
  --mode generate \
  --user-profile user-profile.json \
  --agent-profile agent-profile.json \
  --output-dir my-both-config \
  --format both \
  --claudecode-dir claudecode-config
```

## 配置文件结构

生成的配置包含5个核心文件：

| 文件 | 描述 | 核心内容 |
|------|------|----------|
| `SOUL.md` | Agent灵魂与核心价值观 | 核心真理、专业价值观、情感智能价值观、服务承诺 |
| `IDENTITY.md` | Agent身份特征与个性 | 专业身份、个性特征、多维评分体系、情感表达模式库 |
| `TOOLS.md` | Agent专业工具与工作环境 | 专业工具设置、情感智能工具、环境变量配置 |
| `AGENTS.md` | Agent工作流程与协作方式 | 工作流程、团队连接建立、情感支持策略、质量标准 |
| `USER.md` | Agent对用户的理解与关系管理 | 用户信息、沟通偏好、情感偏好、项目上下文 |

### Claude Code格式配置文件结构

当使用 `--format claudecode` 时，生成以下配置文件：

| 文件 | 描述 | 核心内容 |
|------|------|----------|
| `CLAUDE.md` | 项目手册 | 项目概述、核心工作规则、标准工作流程、Agent配置说明、工具与环境、文件命名规范、常用快捷指令 |
| `[Agent名称].md` | Agent配置文件 | Frontmatter（name、description、type、model）、核心身份定位、强制遵守规则、标准工作流程、核心工作职责、专业能力与工具、用户理解与沟通、工作质量标准、情感智能与支持、快速响应模板 |

*注：Claude Code格式配置文件基于Expert Agent Builder方法论生成，将OpenClaw四层六维专业人格模型适配到Claude Code平台。*

## 模板系统

### 个人基础信息模板 (`templates/user-profile-template.json`)

收集用户基本信息、背景、偏好、项目上下文：

```json
{
  "basic_info": {
    "name": {
      "value": "张三",
      "_说明": "用户的真实姓名或常用称呼"
    },
    "professional_title": {
      "value": "技术总监",
      "_说明": "用户的职业头衔"
    }
  }
}
```

### 高级专业Agent画像模板 (`templates/agent-profile-template.json`)

定义Agent专业身份、核心人格、工作行为、专业参数：

```json
{
  "professional_identity": {
    "domain_expertise": {
      "value": "技术架构",
      "_说明": "Agent的专业领域"
    },
    "experience_level": {
      "value": "高级（7-15年经验）",
      "_说明": "Agent的经验水平"
    }
  }
}
```

## 专业领域支持

### 技术架构
- 系统架构设计、技术选型评估、性能优化
- 云原生架构、分布式系统设计、高可用性设计

### 法律咨询
- 法律研究、合同分析、合规性检查
- 法律文书模板、案例管理系统

### 商业战略
- 市场分析、财务分析、战略规划
- 竞争分析、商业模型画布

### 创意总监
- 创意概念开发、设计系统构建
- 情感表达优化、创意工具集成

### 医学研究
- 医学文献分析、研究设计指导
- 临床数据分析、伦理审查支持

## 情感智能功能

### 情感识别
- 分析语言线索、行为模式、情感状态
- 识别技术压力、团队冲突、个人成就感

### 情感支持
- 提供适时的鼓励和认可
- 在困难时刻提供技术和情感支持
- 帮助恢复信心和方向

### 个性化沟通
- 根据用户偏好调整沟通风格
- 平衡专业严谨与人性关怀
- 建立信任和深度连接

## 验证体系

### 基础验证 (basic)
- 文件存在性检查
- 基本格式验证

### 标准验证 (standard)
- 章节完整性检查
- 基本一致性验证
- 参数范围合理性检查

### 严格验证 (strict)
- 完整一致性验证
- 内容质量评估
- 情感表达自然度检查

## 示例：技术架构顾问

### 用户背景
- **姓名**：张明
- **职位**：技术总监
- **公司**：云创科技有限公司
- **经验**：12年技术架构经验

### Agent画像
- **角色定义**：资深技术架构顾问，专注于云原生和分布式系统设计
- **核心能力**：系统架构设计、性能优化、技术债务管理、团队技术指导
- **情感智能水平**：8/10
- **技术深度**：9/10
- **协作强度**：8/10

### 运行示例

```bash
# 进入示例目录
cd examples/technical-architect-advisor

# 运行配置生成
python ../../openclaw-config-generator.py \
  --mode generate \
  --user-profile user-profile.json \
  --agent-profile agent-profile.json \
  --output-dir generated-config

# 验证生成的配置
python ../../openclaw-config-generator.py \
  --mode validate \
  --config-dir generated-config \
  --validation-level strict
```

## 高级功能

### 批量生成
支持批量处理多个用户和Agent配置：

```bash
python openclaw-config-generator.py --mode batch --input-dir batch-inputs
```

### 自定义模板
使用自定义模板文件生成配置：

```bash
python openclaw-config-generator.py \
  --mode custom \
  --template-dir my-templates
```

### API集成
提供Python API供其他工具调用：

```python
from openclaw_config_generator import ConfigGenerator

generator = ConfigGenerator(
    user_profile="user.json",
    agent_profile="agent.json"
)
generator.generate_all()
```

## 故障排除

### 常见问题

1. **Python版本不兼容**
   ```
   错误：需要Python 3.8或更高版本
   ```
   解决方案：升级Python或使用Python 3.8+

2. **模板文件缺失**
   ```
   错误：无法找到模板文件
   ```
   解决方案：确保模板文件存在于templates/目录中

3. **编码问题**
   ```
   UnicodeDecodeError
   ```
   解决方案：确保文件使用UTF-8编码

4. **权限问题**
   ```
   Permission denied
   ```
   解决方案：检查文件读写权限

### 调试模式

启用详细日志输出：

```bash
python openclaw-config-generator.py --mode interactive --debug
```

## 开发指南

### 项目结构

```
skill/
├── openclaw-config-generator.py     # 主生成脚本
├── skill.json                      # Skill元数据
├── README.md                       # 使用说明
├── templates/                      # 模板文件目录
│   ├── user-profile-template.json
│   ├── agent-profile-template.json
│   └── README.md
├── examples/                       # 示例文件目录
│   ├── technical-architect-advisor/
│   ├── legal-consultant/
│   └── README.md
└── utils/                          # 工具脚本目录
    ├── config_generator.py
    ├── validator.py
    └── template_manager.py
```

### 扩展新领域

1. 在`templates/`目录中创建新的领域模板
2. 在`examples/`目录中创建新的示例
3. 更新领域适配逻辑
4. 添加新的验证规则

### 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 创建Pull Request

## 许可证

MIT License

## GitHub部署

### 1. 在GitHub创建新仓库
1. 访问 https://github.com 并登录
2. 点击右上角 "+" → "New repository"
3. 仓库名称：`expert-agent-builder`
4. 描述：`基于四层六维专业人格模型的专家级Agent配置生成器`
5. 选择 **Public**（公开）
6. **不要**初始化README、.gitignore或LICENSE（项目已包含）
7. 点击 "Create repository"

### 2. 推送代码到GitHub
```bash
# 进入项目目录
cd "D:\cc_projects\openclaw-research\Expert Agent Builder"

# 添加远程仓库（将YOUR_USERNAME替换为你的GitHub用户名）
git remote add origin https://github.com/pkulyn/expert-agent-builder.git

# 推送代码
git branch -M main
git push -u origin main
```

### 3. 创建版本标签（可选）
```bash
# 创建版本标签
git tag -a v1.0.0 -m "Expert Agent Builder v1.0.0 初始版本"

# 推送标签
git push origin v1.0.0
```

### 4. 设置GitHub Pages（可选，用于文档）
1. 进入仓库设置 → Pages
2. Source选择 `main` 分支，文件夹选择 `/docs`（如果启用文档站点）
3. 保存，等待部署完成

## 支持

- 问题跟踪：GitHub Issues
- 文档：https://docs.openclaw.ai/zh-CN
- 社区：OpenClaw社区论坛

## 更新日志

### v1.0.0 (2026-04-09)
- 初始版本发布
- 基于第四阶段研究成果
- 完整的配置生成和验证功能
- 技术架构顾问示例

---

**重要提示**：本工具基于OpenClaw高级专业人士Agent配置研究成果开发。建议在使用前阅读完整的研究报告和最佳实践指南，以获得最佳效果。