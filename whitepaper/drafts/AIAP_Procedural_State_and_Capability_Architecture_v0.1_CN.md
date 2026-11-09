<!-- SPDX-License-Identifier: CC-BY-4.0 -->
> Source transcription of the accompanying DOCX by Wang Lu. Draft design; not a declaration of implemented compatibility. The original DOCX controls if formatting is ambiguous.

AIAP

Procedural State & Capability Architecture

程序性状态与能力架构规范 v0.1

AIAP White Paper v0.4.1 Companion SpecificationAuthor: Wang LuSeptember 2026

核心原则：Workflow 描述“如何做事”；Capability 描述“需要什么能力”；Skill/Tool 只是 Runtime 中的具体实现。

1. 目的与范围

本规范定义 AIAP 从 Avatar Core 到 Skill、Tool 与外部 Runtime 的程序性状态架构，是 AIAP v0.4.1 的配套施工规范。目标不是创建新的 Skill Engine 或 Workflow Engine，而是建立 Runtime-neutral 语义层，使个人长期形成的工作方法能够被保存、迁移、重新绑定并在不同 Agent Runtime 中恢复。

v0.1 优先解决右端链路：Avatar Core → Procedural Index → Workflow → Capability → Runtime Binding → Skill/Tool → Execution。Personal State 的复杂压缩、记忆巩固与长期抽象算法暂不在本规范中展开。

2. 核心设计原则

Workflow 不应直接依赖某个 Runtime 的私有 Skill 标识；应优先引用 Capability。

Capability 是跨 Runtime 的稳定语义层；Skill、Tool、Plugin 是 Capability 的具体实现。

AIAP 保存程序性状态、引用、统计与生命周期事实，不承担具体执行。

Skill 源码默认不嵌入 Avatar Core；通过来源、版本、完整性和 Runtime Binding 解析。

缓存层级属于 Runtime Policy；AIAP 只保存足以推导缓存策略的事实。

Execution Trace 是程序性学习的证据来源，但不等于 Workflow。

Core 应保持小而稳定；大量 Workflow、Skill metadata 与 Trace 可位于外部状态存储。

3. 六层架构

AVATAR CORE    ↓1 Intent / Context    ↓2 Procedural Index    ↓3 WorkflowDescriptor    ↓4 Capability    ↓5 Runtime Binding / SkillDescriptor    ↓6 Runtime Execution    ↓Execution Trace → Statistics / Learning → Procedural State Update

关键解耦点位于 Workflow 与 Runtime Skill 之间：Workflow 描述用户长期形成的方法，Capability 描述步骤需要的抽象能力，Runtime Binding 再决定当前环境中由哪个 Skill、Tool 或 Agent 实现。

4. Intent / Context

| 字段 | 说明 |
| --- | --- |
| intent_id | 标准或本地意图标识 |
| intent_text | 当前任务语义 |
| context_refs | 相关 Personal State / project / document 引用 |
| constraints | 时间、成本、隐私、输出格式等 |
| required_capabilities | 已知必要能力，可为空 |
| confidence | 意图识别置信度 |

5. Procedural Index

Procedural Index 是 Avatar Core 与大规模 Procedural State 之间的紧凑索引。Core 不装入全部 Workflow 或 SkillDescriptor，只保留高价值摘要、索引与可解析引用。

| 字段 | 说明 |
| --- | --- |
| workflow_refs[] | WorkflowDescriptor 引用 |
| capability_refs[] | 关键 Capability 引用 |
| skill_refs[] | SkillDescriptor 引用 |
| activity_summary | 活跃度摘要 |
| resolver | 外部状态解析位置 |
| integrity | 索引/manifest 完整性 |

6. WorkflowDescriptor

WorkflowDescriptor 是“HOW I WORK”的主要可移植对象，描述某类任务中长期形成的步骤、条件、偏好和统计，而不是某一 Runtime 的执行脚本。

| 字段组 | 建议字段 |
| --- | --- |
| Identity | workflow_id, owner, version |
| Intent | intent, trigger, applicability |
| Inputs | inputs, context_requirements |
| Steps | step_id, capability_ref, parameters |
| Transitions | from, to, condition |
| Outputs | expected_outputs, validation |
| Preferences | defaults, user_overrides |
| Statistics | execution_count, success/failure, avg_duration, last_used |
| Origin | learned / imported / user_defined |
| Provenance | trace_refs, source, created_at |
| Lifecycle | importance, recurrence, availability |

6.1 Workflow 不直接绑定 Skill

Workflow Step   ↓capability: academic.search.primary_sources   ↓Runtime Binding   ↓OpenClaw Skill / Runtime-B Tool / Future Agent

允许 Runtime-specific Workflow 作为扩展存在，但必须明确声明 portability=runtime_specific。

7. Capability

Capability 是稳定中间语义，回答“完成这个步骤需要什么能力”，而不是“当前使用哪个程序”。

| 字段 | 说明 |
| --- | --- |
| capability_id | 命名空间化标识，如 academic.search |
| description | 能力语义 |
| input_contract | 抽象输入要求 |
| output_contract | 抽象输出要求 |
| constraints | 权限、安全、成本或质量要求 |
| taxonomy_refs | 父/子/相关能力 |
| version | 能力语义版本 |

使用 academic.search、document.generate、source.verify 等语义命名。

避免 capability_id 出现供应商或 Runtime 名称。

允许层级能力，例如 academic.search.primary_sources。

v0.1 使用本地版本化 Capability Registry；未来可分布式维护。

8. Runtime Binding 与 SkillDescriptor

Runtime Binding 把 Capability 映射到当前 Runtime 可执行的 Skill、Tool、Plugin、Agent 或 API。

| 字段 | 说明 |
| --- | --- |
| binding_id | 绑定唯一标识 |
| capability_ref | AIAP Capability |
| runtime | openclaw / future.* |
| implementation_type | skill / tool / plugin / agent / api |
| implementation_ref | Runtime 内标识或外部来源 |
| version | 实现版本 |
| integrity | hash / signature |
| requirements | 依赖与权限 |
| parameters | 个人化默认参数 |
| usage_stats | 调用次数、成功率、last_used |
| status | available / unavailable / deprecated |

9. Capability Mapping

OpenClaw Skill A → academic.search → AIAP Transfer → Target Runtime Tool B / Agent C

| 映射结果 | 语义 |
| --- | --- |
| exact | 满足目标 Capability |
| compatible | 主要语义满足，存在可接受差异 |
| partial | 只覆盖部分能力 |
| composite | 多个目标能力组合实现 |
| unresolved | 当前 Runtime 无法满足 |

v0.1 可先使用 registry + 人工确认映射表，以保证实验可复现。

10. Runtime Execution

AIAP 不规定执行引擎。Runtime 可以动态执行 WorkflowDescriptor，也可以将其编译到自己的 Workflow Engine。执行结果应返回标准化 Execution Trace 摘要。

11. Execution Trace

Execution Trace 是任务执行的可审计摘要，是统计、Workflow 学习与演化的证据层；不要求保存模型私有 chain-of-thought。

| 字段 | 说明 |
| --- | --- |
| trace_id | 轨迹标识 |
| intent_ref | 任务意图 |
| workflow_ref | Workflow，可为空 |
| steps[] | capability / binding / result 摘要 |
| started_at / ended_at | 时间 |
| success | 成功状态 |
| user_feedback | 可选反馈 |
| cost | token、时间、API 成本 |
| errors | 失败与重试摘要 |
| provenance | Runtime、模型、版本 |

12. Learned Workflow 生命周期

Execution Traces → Recurring Pattern → Candidate Workflow → Validation / User Confirmation → Personal Workflow → Reuse → Version Update

| 状态 | 含义 |
| --- | --- |
| candidate | 系统从经验提出 |
| validated | 经规则、测试或用户确认 |
| personal | Avatar 常用个人 Workflow |
| deprecated | 被新版替代 |
| dormant | 长期不用或依赖不可用 |
| archived | 历史保存 |

13. 生命周期与缓存

AIAP 保存 Lifecycle Metadata；Runtime 决定 HOT / WARM / COLD 等实际缓存层级。

| 事实字段 | 用途 |
| --- | --- |
| usage_count | 累计频率 |
| last_used | 近期性 |
| success_rate | 可靠性 |
| user_weight | 显式偏好 |
| importance | 长期价值 |
| recurrence | 周期性 |
| expected_next_use | 预期再次使用 |
| dependency_status | 依赖可用性 |
| last_verified | 最近兼容性验证 |

Lifecycle Metadata → Runtime Policy → HOT / WARM / COLD / DORMANT / ARCHIVED

14. 存储边界

| 对象 | Avatar Core | Procedural Store | Runtime/Registry |
| --- | --- | --- | --- |
| Workflow index | 摘要/引用 | 完整 Descriptor | 可选执行表示 |
| Workflow logic | 否/极少 | 标准 Descriptor | Runtime 编译结果 |
| Capability | 核心引用 | Registry/cache | Runtime mapping |
| SkillDescriptor | 高价值引用 | 完整 metadata | 实现包 |
| Skill source code | 否 | 通常否 | 是 |
| Execution Trace | 摘要/统计 | 是 | 可保留原始日志 |
| Secrets | 否 | 否 | 安全凭据系统 |

15. 跨 Runtime 恢复流程

Import Core → Resolve Procedural Index → Select Workflow → Resolve Capabilities → Inspect Target Runtime → Map Bindings → Execute → Record Trace → Update State

这一流程直接对应 WCR（Workflow Continuity Rate）与 CMR（Capability Mapping Rate）的 Benchmark。

16. Reference Implementation v0.1

| 组件 | v0.1 |
| --- | --- |
| Procedural Index | JSON/SQLite |
| WorkflowDescriptor | JSON Schema + Python model |
| Capability Registry | 本地版本化文件 |
| SkillDescriptor | JSON Schema + Python model |
| OpenClaw Binding | 至少一种 Skill/Tool 映射 |
| Second Runtime | Benchmark 阶段增加最小 Adapter |
| Trace Recorder | 标准化摘要 |
| Workflow Learning | 规则式候选 + 人工确认 |
| Lifecycle | usage_count / last_used / success_rate |
| Cache | 简单阈值，仅作示例 |

17. Benchmark 对应关系

| 指标 | 验证对象 |
| --- | --- |
| TSR | 完整执行链 |
| WCR | Workflow 迁移恢复 |
| CMR | Capability 映射 |
| PCR | 偏好/参数保留 |
| TER | 结构化状态的 Token 效率 |
| TTAR | Avatar 恢复时间 |

18. 安全与所有权

WorkflowDescriptor 与个人 usage statistics 遵循 AIAP Ownership Spec。

第三方 Skill 源码版权和许可证不因被引用而转移。

Runtime Binding 区分“偏好此实现”和“拥有此实现”。

外部实现记录 integrity 与版本。

Trace 只保存可验证动作/结果摘要，不要求 chain-of-thought。

API key、wallet private key、password 等 secret 不得进入 Procedural State。

19. 与 Spindle Architecture 的关系

PERSONAL STATE      \    AVATAR CORE       /PROCEDURAL INDEX → WORKFLOWS → CAPABILITIES → RUNTIME BINDINGS → SKILLS/TOOLS

本规范定义纺锤架构右端。右端可随用户使用年限持续增长，而 Avatar Core 仅保留必要索引与高价值摘要。

20. v0.1 冻结项与未来扩展

20.1 建议冻结

Workflow → Capability → Runtime Binding 的解耦。

WorkflowDescriptor、Capability、SkillDescriptor 最小字段。

Execution Trace 标准摘要。

Capability Mapping 五类结果。

Lifecycle Metadata 与 Runtime Cache Policy 边界。

Core 不嵌入大量 Skill 源码与 Trace。

20.2 暂不冻结

全球 Capability taxonomy。

自动 Workflow Learning 算法。

activity score 公式。

HOT/WARM/COLD 阈值。

分布式 Capability Registry。

Workflow Compiler。

Marketplace、结算与 ACU 绑定。

21. 下一步实施顺序

Freeze Schemas → Capability Registry → Workflow/Skill Models → OpenClaw Adapter → Trace Recorder → Candidate Workflow → Second Runtime → Benchmark v0.1

22. 结论

本规范将个人长期做事方式从具体 Agent Runtime 中抽离：Workflow 保存方法，Capability 保存能力语义，Runtime Binding 连接具体 Skill/Tool，Execution Trace 提供经验反馈，Lifecycle Metadata 支持长期演化与缓存。

目标不是让 AIAP 成为新的 Agent Runtime，而是让一个人多年形成的 AI 工作方式不再属于某个软件，而成为用户 Avatar 可携带、可验证、可恢复的一部分。

