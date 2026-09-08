# Pi Workbench

> 以 **Pi Agent** 为操作员、以 Obsidian 兼容 Markdown Vault 为长期资产底座的个人工作台。
>
> 捕获输入，保留证据，组织项目，并将其转化为你能够负责的理解、产品和公开表达。

Pi Workbench 不是“更大的笔记库”，也不追求把所有信息整理完。它关心的是一条可追溯的信息生命周期：

```text
raw/ ──> wiki/ ──> output/
             \──> projects/ ──┘
```

- **`raw/`**：日记、灵感、剪贴、订阅等原始输入；保留上下文，不要求清零。
- **`wiki/`**：Pi 可检索的编译知识——概念、证据、方法、决策、实体和综合判断。
- **`projects/`**：轻量工作桌；每个项目只维护目标、`## Now`、证据和预期输出。
- **`output/`**：你的理解、个人介绍资产、内容、产品材料和作品案例。Pi 可以协助起草，但不能替你宣称拥有或发布。

---

## 为什么存在

传统笔记系统经常走向两种失败：

1. **资料仓库**：网页、摘录、聊天记录越来越多，但需要做决策或表达时仍然找不到、讲不清；
2. **Agent 总结库**：Agent 替人总结、替人写卡片，用户只是阅读或搬运，知识没有变成自己的判断。

Pi Workbench 的约束是：

- 原始信息可以保留，不强迫整理；
- 只有进入 `wiki/` 的内容才要求来源与不确定性边界；
- 只有经过你确认的 `output/` 才能成为“我的理解”“可发布内容”或“个人主张”；
- 项目是将知识连接到现实行动与交付的工作桌，而不是另一套复杂任务系统。

成功标准不是页面数量、Raw 清空率或连续打卡，而是：

- 做项目、写内容或准备个人介绍时，能迅速找到相关证据；
- 能不看资料讲清自己的判断、边界和下一次使用场景；
- 同一份经验能复用于产品、内容、作品集和个人表达，而不用重复维护多套信息。

---

## Vault 结构

运行 `pi-workbench setup` 后，新 Vault 的用户可见结构如下：

```text
personal-workbench/
├── _system/
│   ├── AGENTS.md                 # Pi 权限、生命周期规则、人工确认边界
│   ├── templates/                # Raw、Project、Understanding 模板
│   ├── dashboards/               # 生成式工作台视图
│   └── workbench-log.md
│
├── raw/                           # 唯一输入层；原件默认保留
│   ├── journal/                  # 日记、工作记录、观察、会议后记录
│   ├── ideas/                    # 问题、假设、方向、灵感
│   ├── clips/                    # 网页、PDF、截图、摘录、手动收藏
│   └── subscriptions/            # Newsletter、RSS、定期信息流
│
├── wiki/                          # Pi 可检索的编译知识
│   ├── concepts/                 # 概念、心智模型、长期主题
│   ├── evidence/                 # 来源、事实、数据、案例
│   ├── methods/                  # 可复用方法与工作流
│   ├── decisions/                # 决策、取舍、复查边界
│   ├── entities/                 # 人、组织、产品、工具、渠道、受众
│   └── synthesis/                # 多来源综合、趋势与矛盾分析
│
├── projects/                      # 活跃主题；一页就是一个工作上下文
│
├── output/                        # 人拥有、可交付或可公开的成果
│   ├── understanding/            # 个人理解、观点、判断
│   ├── profile/                  # 自我介绍、Bio、能力与经历素材
│   ├── content/                  # 选题、草稿、渠道版本、发布稿
│   ├── products/                 # PRD、方案、技术文档、发布材料
│   └── portfolio/                # 项目案例与作品
│
├── assets/                        # 图片、附件、音视频等非 Markdown 资产
└── archive/                       # 已结束项目与被替代的 Output
```

`_system/`、`raw/`、`assets/` 与 `archive/` 默认不参与普通知识检索、图谱和结构校验。普通检索与上下文包只读取：

```text
wiki/** + projects/** + output/**
```

---

## 快速开始

### 1. 安装开发版本

```bash
git clone git@github.com:dylan47zz/pi-workbench.git
cd pi-workbench
python3 -m pip install -e .
```

> 目前优先支持从源码安装；尚未发布 PyPI 稳定版。

### 2. 创建一个新的私有 Vault

不要把个人日记、订阅、内容草稿或附件放进本仓库。建议新建独立路径：

```bash
pi-workbench setup --vault ~/Documents/personal-workbench
```

这会创建目录、模板、`_system/AGENTS.md` 和独立配置：

```text
~/.config/pi-workbench/config
```

配置使用：

```text
PI_WORKBENCH_VAULT_PATH
```

因此可与单独安装的 `obsidian-wiki` 或其他 Obsidian Vault 并存，不共享配置。

### 3. 将 Workbench Skills 安装到 Pi

```bash
pi-workbench install-pi-skills
```

默认安装至：

```text
~/.pi/agent/skills/
```

### 4. 用 Obsidian 打开 Vault

打开 `~/Documents/personal-workbench`，将其作为普通 Obsidian Vault 使用即可。模板和 Dashboard 都是标准 Markdown；不依赖云服务或专有数据库。

### 5. 验证安装

```bash
pi-workbench doctor
pi-workbench status
pi-workbench dashboard
```

---

## 命令行使用

### 输入：Capture

```bash
# 保存一个灵感
pi-workbench capture ideas "个人工作台的订阅信号" \
  "订阅系统不应该输出资讯摘要，而应标记可能影响项目或观点的变化。"

# 保存一个剪贴
pi-workbench capture clips "Agent 架构文章" \
  "文章的核心发现……" \
  --source "https://example.com/article" \
  --why "可能影响 Pi Workbench 的订阅工作流"
```

会分别写入：

```text
raw/ideas/YYYY-MM-DD-个人工作台的订阅信号.md
raw/clips/YYYY-MM-DD-agent-架构文章.md
```

Capture 不要求标签、项目归属、完整 YAML 或立即整理。

### 项目：轻量工作桌

```bash
pi-workbench project content-system "内容系统 MVP" \
  "验证知识资产是否能转化为可持续的内容输出" \
  --intended-output output/content/content-system-outline.md
```

生成的项目页包含：

```text
Goal
Now
Current judgment
Evidence and context
Intended output
Review
```

`## Now` 是 MVP 的任务机制。只有有明确目标与预期输出的事情才值得创建 Project。

### 输出：创建草稿

```bash
# 创建产品文档草稿
pi-workbench output products pi-workbench-mvp "Pi Workbench MVP"

# 创建你的理解草稿，并关联一个项目上下文
pi-workbench output understanding subscription-view "我对订阅系统的判断" \
  --source projects/content-system.md
```

Output 默认都是：

```yaml
status: draft
```

Pi 不能将任何 Output 自动提升为：

```text
owned / ready / published
```

其中 `output/understanding/` 固定要求：

```text
我的判断
为什么
边界与不确定性
下一次使用
```

### 检索与上下文

```bash
# 默认查询 Wiki、项目和 Output
pi-workbench query "订阅系统如何影响内容选题"

# 只查询知识层
pi-workbench query "内容策略" --scope wiki

# 为 Pi 的下游任务建立带边界的上下文包
pi-workbench context "为个人主页撰写自我介绍" --scope compiled --budget 4000 --pretty
```

支持的 scope：

| Scope | 范围 |
|---|---|
| `wiki` | `wiki/**` |
| `projects` | `projects/**` |
| `output` | `output/**` |
| `compiled` | 三者联合；默认值 |

Raw 默认不进入查询或 Context Pack。若答案只存在于 Raw，应通过 Triage 把它作为原始来源审视，而不是把未核验文字当成知识结论。

### 状态、图谱、Review 与 Dashboard

```bash
pi-workbench status
pi-workbench raw-status
pi-workbench lint
pi-workbench graph
pi-workbench review
pi-workbench dashboard
```

- `status`：Raw 信号分类、活跃项目、Output 草稿；
- `raw-status`：只统计四类原始输入；
- `lint`：检查 Project、Wiki、Output 的最小契约和编译链接；
- `graph`：只查看 Wiki、项目、Output 的 Markdown 链接图；
- `review`：生成少量高信息增益的复盘问题；
- `dashboard`：写入 `_system/dashboards/now.md`，它是生成式视图，不是事实源。

---

## Pi Skills

Pi Workbench 将工作流拆成 13 个窄职责 Skills：

| Skill | 作用 |
|---|---|
| `workbench-capture` | 低摩擦保存日记、灵感、剪贴与订阅输入。 |
| `workbench-triage` | 对选定 Raw 做 `retain / ignore / compile / work / express` 判断，不移动原件。 |
| `workbench-query` | 查询编译知识、项目与 Output。 |
| `workbench-context` | 为下游任务构造有 token 边界、带路径来源的上下文包。 |
| `workbench-project` | 创建、维护或复盘轻量 Project 工作桌。 |
| `workbench-output` | 起草理解、内容、产品、Profile 或作品；保留人工所有权门槛。 |
| `workbench-status` | 显示当前真正值得关注的状态，不制造 Inbox Zero 压力。 |
| `workbench-lint` | 校验编译页面的元数据、结构与链接。 |
| `workbench-graph` | 查看 Wiki、项目和 Output 之间的链接关系。 |
| `workbench-review` | 用少量问题触发反思，而不是生成被动复习卡片。 |
| `workbench-dashboard` | 生成 Obsidian 工作台视图。 |
| `workbench-subscriptions` | 从订阅中筛选会影响判断、项目或内容的信号。 |
| `workbench-history` | 按主题找回 Pi/Agent 历史，不默认全量导入。 |

完整迁移与延后策略见：[Skill Migration Map](docs/skill-migration.md)。

---

## 推荐的工作闭环

### 1. 日记、灵感、剪贴与订阅进入 Raw

```text
raw/journal      记录发生的事与卡点
raw/ideas        保存问题与假设
raw/clips        保存外部资料
raw/subscriptions 保存定期信息流
```

### 2. Triage，而不是批量摘要

Pi 对选中的输入提出一个最小去向：

```text
retain  保留上下文，暂时不做事
ignore  当前没有价值，但不强迫删除
compile 形成或更新 Wiki 证据/概念/方法/决策
work    加入活跃项目的 Now
express 形成个人理解、内容、产品材料或 Profile 草稿
```

### 3. 使用 Wiki 支撑项目与输出

- 产品研发：`raw` 资料 → `wiki/evidence` / `wiki/decisions` → `projects` → `output/products`；
- 自媒体：订阅/项目经验 → `wiki/synthesis` → `output/content`；
- 个人介绍：项目案例与证据 → `output/profile`；
- 个人理解：先由你解释，再用 Wiki 证据校正 → `output/understanding`。

### 4. 反馈回流

发布反馈、项目结果或新的观察重新进入 `raw/`，再决定是否修正 Wiki、Project 或 Output。

---

## 人类所有权与安全边界

Pi Workbench 的重要原则是：**Agent 维护信息流，不替代人的判断和承诺。**

- Raw 文件不会因被提炼而自动删除或移动；
- Wiki 要区分来源事实、推断与不确定性；
- Output 默认是 `draft`；
- 只有你能将 Output 标为 `owned`、`ready`、`published`；
- Pi 不会自动发布内容、修改对外 Profile、发送消息或同步私有 Vault；
- 所有外部动作都需要当前对话中的明确授权；
- Vault 应是私有仓库或可靠的个人备份目标，框架代码仓库不应包含你的个人资料。

---

## 当前范围与刻意延后

当前版本已提供：

- 原生 Vault scaffold；
- Raw Capture 与 Triage 契约；
- Scope-aware Query、Context、Status、Lint、Graph；
- 项目与 Output 草稿创建；
- Review 与 Dashboard；
- Pi Skills 安装；
- focused history / subscription 的 Skill 级工作流定义。

以下能力**刻意延后**，直到真实使用证明有必要：

- RSS/Newsletter 自动抓取与账号连接；
- 外部内容发布、个人主页更新、社媒 API；
- QMD/向量检索；
- 浏览器扩展；
- HTTP/MCP 服务化；
- 批量导入 Claude、Codex、Pi 等全部 Agent 会话；
- 自动去重、自动交叉链接、自动综合写入；
- 多 Vault 管理。

详见：[Skill Migration Map](docs/skill-migration.md)。

---

## 开发

```bash
# Workbench 核心测试
python3 -m pytest -q tests/test_pi_workbench.py

# 当前源码仓库的完整回归（含继承代码）
python3 -m pytest -q

# 基本静态检查
git diff --check

# 构建 wheel
python3 -m pip wheel --no-deps --wheel-dir /tmp/pi-workbench-wheel .
```

Pi Workbench 的正式运行时只依赖 `pi_workbench/` 和 `workbench-*` Skills。仓库中仍暂存部分上游代码和测试作为可追溯参考；它们不是 Pi Workbench Vault 的默认运行路径。

---

## 独立项目与上游归属

Pi Workbench 起源于 [`Ar9av/obsidian-wiki`](https://github.com/Ar9av/obsidian-wiki)，借鉴了：

- Markdown-first 的本地数据所有权；
- Agent Skill 驱动的工作流；
- 可追溯来源与知识编译的思想；
- 图谱、检索、lint 等实现经验。

但 Pi Workbench 已改变核心数据模型与运行语义，不进行常规上游同步。后续只在有明确收益时，从上游选择性移植独立的安全、解析或算法修复，并先适配 `raw / wiki / projects / output` 范围模型。

详细策略见：[Upstream Policy](docs/upstream-policy.md)。

---

## License

MIT。保留上游 MIT License 与归属说明；详见 [LICENSE](LICENSE) 和 [Upstream Policy](docs/upstream-policy.md)。
