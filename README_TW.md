<h1 align="center">pi-workbench</h1>

<p align="center"><b>以 Pi Agent 驱动、以 Obsidian 知识库为底座的个人工作台。</b></p>

<p align="center">
一次捕获外部信息，保留可追溯证据，并转化为你能负责的工作与表达。
</p>

---

`pi-workbench` 是构建在 Obsidian 兼容 Vault 之上的个人操作层。它服务于一个人的日记与灵感、剪贴与订阅、产品研发、公开内容、个人介绍和作品集，而不是把笔记库继续做大。

项目 Fork 自 [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)。上游的 Markdown 所有权、来源追溯、图谱检索和 Agent Skill 模型仍被保留；Pi Workbench 在此基础上定义了不同的信息生命周期：

```text
_raw/ → 编译后的知识 → output/
             ↘ projects/ ↗
```

- **`raw/`** 保存日记、灵感、剪贴和订阅的原始信息；
- **`wiki/`** 保存 Agent 可检索的概念、证据、方法、决策、实体与综合分析；
- **`projects/`** 是轻量工作桌：目标、`## Now`、证据和预期产出；
- **`output/`** 保存你拥有的理解、个人介绍资产、内容、产品文档与作品案例。

目标不是清空每一条输入，而是在你做决策、研发或表达时，能及时取回相关证据。

## MVP

```bash
pip install -e .
pi-workbench setup --vault ~/Documents/personal-workbench
pi-workbench doctor
pi-workbench install-pi-skills
```

随后用 Obsidian 打开 Vault。Pi Workbench 会创建四个低摩擦输入口：

```text
raw/journal/
raw/ideas/
raw/clips/
raw/subscriptions/
```

## 已包含的 Pi Skills

- `workbench-capture`：用最少分类保存输入；
- `workbench-triage`：对选定 Raw 做保留、忽略、编译、进入项目或形成表达的判断，不移动原件；
- `workbench-output`：协助起草个人理解、个人介绍、内容、产品文档或作品案例，但不冒充人的拥有状态。
- `workbench-query` / `workbench-context`：检索编译知识，并为具体任务生成有边界的上下文。
- `workbench-project` / `workbench-status` / `workbench-review`：轻量维护项目，并呈现真正值得关注的事项。
- `workbench-lint` / `workbench-graph` / `workbench-dashboard`：校验、查看关系并生成工作台视图。
- `workbench-subscriptions` / `workbench-history`：筛选订阅信号、按主题找回 Agent 历史，而不全量导入。

详见 [工作台架构](docs/workbench-architecture.md)、[Skill 迁移地图](docs/skill-migration.md) 和 [上游同步策略](docs/upstream-policy.md)。

## 当前状态

当前 MVP 已提供独立 Vault/配置、捕获与 Triage、范围化检索和 Context、轻量项目与 Output 创建、状态、Lint、关系图、Review 与生成式 Dashboard。订阅自动采集、外部发布、QMD 语义检索和全量历史导入仍会等真实工作流证明需要后再加入。

## 许可证

MIT。本仓库保留上游 MIT 许可证与归属说明，见 [上游同步策略](docs/upstream-policy.md)。
