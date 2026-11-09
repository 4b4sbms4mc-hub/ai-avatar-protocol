<!-- SPDX-License-Identifier: CC-BY-4.0 -->
> Source transcription of the accompanying DOCX by Wang Lu. Draft design; not a declaration of implemented compatibility. The original DOCX controls if formatting is ambiguous.

AIAP

AI Avatar Protocol

白皮书 v0.4.1

Spindle Architecture · Portable Avatar Core · Procedural State纺锤架构 · 可携带 Avatar Core · 程序性状态

Author: Wang LuSeptember 2026

核心命题：Runtime 可以替换，但 Avatar 属于用户。

摘要

AIAP（AI Avatar Protocol）是一套面向个人 AI 状态所有权、可携带性、跨 Runtime 互操作与长期演化的开放协议框架。AIAP 不试图重新实现 Agent Runtime、Memory Engine、Skill Engine 或 Workflow Engine，而是定义一个独立于具体 Agent 平台的个人 Avatar 状态层，使用户在更换模型、Agent、设备或服务提供方时，仍能保留其身份、偏好、重要记忆、能力使用习惯与长期形成的工作方式。

v0.4.1 在 v0.3 的 Identity、Ownership、Secure Avatar Transfer 与可扩展 State Model 基础上，引入 Spindle Architecture（纺锤架构）、Avatar Core、Personal State、Procedural State、SkillDescriptor、WorkflowDescriptor、Capability Mapping、Lifecycle Metadata 与 Lazy Migration。核心思想是：两端可以持续增长，中间的 Avatar Core 应保持小、稳定、可验证、可迁移。

AIAP v0.4.1 的工程原则是“标准层自研，执行层复用”。OpenClaw、Letta、LangGraph、Mem0 或未来 Runtime 均可通过 Adapter 接入；AIAP 只规定语义、所有权、引用、迁移与兼容边界，不绑定任何单一执行引擎。

1. 版本演进与 v0.4.1 的目标

| 版本 | 主要重点 |
| --- | --- |
| v0.1 | AI Avatar Protocol 初始概念、身份与状态的基本可携带性 |
| v0.2 | Ownership、Transfer 与跨平台状态迁移边界 |
| v0.3 | Identity System、Secure Avatar Transfer、Key Management、可扩展 State Model 与正式 Schema 体系 |
| v0.4.1 | Spindle Architecture；Avatar Core；Personal / Procedural State 分离；Skill / Workflow 可移植描述；Capability Mapping；生命周期与按需迁移 |

v0.4.1 不推翻 v0.3。Identity、Ownership、Transfer、Key Management 继续属于 Core Protocol。新增内容主要位于 State Architecture 与 Extension Layer，使 AIAP 能表达“WHO I AM / WHAT I KNOW / HOW I WORK”，同时避免协议本体膨胀。

2. AIAP 的边界

2.1 AIAP 负责什么

定义 Avatar 的身份、所有权与授权边界。

定义 Avatar Core 的最小可携带表示。

定义 Personal State 与 Procedural State 的标准语义和引用方式。

定义 Skill / Workflow 的可移植描述，而非强制携带完整执行代码。

定义 Capability Mapping，使不同 Runtime 能寻找等价能力。

定义安全导出、导入、迁移、撤销与完整性验证。

定义 Extension Registry，使第三方扩展不需要修改 AIAP Core。

2.2 AIAP 不负责什么

不自研或规定基础大模型。

不要求自研 Agent Runtime。

不规定 Memory Engine 的具体检索算法或向量数据库。

不规定 Skill Engine、Workflow Engine 的具体执行实现。

不把 OpenClaw、Letta、LangGraph 或任何单一项目写死为协议依赖。

不把 HOT / WARM / COLD 等缓存策略固化为跨平台强制状态。

3. 核心理论：AIAP Spindle Architecture

AIAP v0.4.1 将长期 Avatar 视为一个“纺锤状”系统：左端是不断增长的 Personal State，右端是不断增长的 Procedural / Capability State，中间是保持紧凑的 Avatar Core。

PERSONAL STATE                          PROCEDURAL / CAPABILITY STATE(history, memory, preferences)            (skills, workflows, traces)          \                                      /           \                                    /            \          AVATAR CORE             /             =======[ small / portable ]========            /          index + refs              \           /                                      \   external/local stores                    runtimes / registries

3.1 左端：Personal State

Personal State 描述用户授权范围内与个人长期连续性有关的信息，包括历史、偏好、长期记忆、知识结构、项目状态、关系语境、重要决策与其他扩展域。原始数据可以很大，但不应全部进入模型上下文，也不应全部塞入 Avatar Core。

3.2 中间：Avatar Core

Avatar Core 是 AIAP 的最小高密度、可携带、可验证状态表示。它包含稳定身份、所有权证明、核心偏好摘要、重要状态索引、Capability / Workflow 引用、扩展清单、版本与完整性信息。Avatar Core 不是用户全部数据的副本，而是理解与恢复 Avatar 所需的“核心状态 + 可解析引用”。

3.3 右端：Procedural State

Procedural State 描述“这个人如何做事”。它包括常用 Skill、长期形成的 Workflow、能力偏好、执行轨迹摘要、成功率、版本、依赖和生命周期元数据。其规模可随使用时间持续增长，因此同样应通过索引、引用和按需加载管理。

4. 三类个人状态：WHO I AM / WHAT I KNOW / HOW I WORK

| 层 | 问题 | 典型内容 |
| --- | --- | --- |
| Identity State | WHO I AM | Identity、Ownership、Keys、Authorization、Transfer |
| Personal / Semantic State | WHAT I KNOW | Memory、Preferences、Knowledge、Projects、Context |
| Procedural State | HOW I WORK | Skills、Workflows、Habits、Execution Patterns、Capability Preferences |

三类状态不意味着三套独立数据库，而是协议语义上的分层。具体 Runtime 可以使用 SQLite、文件、对象存储、向量数据库或云端服务，只要能够保持 AIAP 所要求的可导出性、完整性与引用语义。

5. Avatar Core v0.4.1

5.1 建议最小字段

| 字段 | 作用 |
| --- | --- |
| aiap_version | 声明协议版本 |
| avatar_id | Avatar 的稳定唯一标识 |
| owner | 所有权主体与验证引用 |
| identity_refs | 身份与密钥材料的安全引用 |
| profile_summary | 高密度、可更新的个人核心摘要 |
| state_index | Personal State 的索引与引用 |
| procedural_index | Skill / Workflow / Capability 的索引与引用 |
| extensions | 已启用扩展域及其版本 |
| integrity | 哈希、签名、manifest 或 commitment |
| updated_at | 核心状态更新时间 |

5.2 Core 的稳定性原则

Core 字段应少而稳定；新增业务域优先通过 Extension 扩展。

Core 不直接嵌入大量历史对话、文档、Skill 源码或执行日志。

Core 中的外部引用必须可验证来源、版本与完整性。

Core 的迁移应能够独立完成；大体量状态允许后续 Lazy Migration。

6. Personal State：压缩、索引与展开

Personal State 可以无限增长，但 Agent 每次任务只应加载与当前意图相关的部分。AIAP 因而采用“原始状态 → 提取/摘要 → Core Index → 按需检索”的逻辑。

Massive Personal History → Abstraction / Compression → Avatar Core → Intent Retrieval → Relevant State

AIAP 不规定具体摘要模型或 embedding 算法。协议只要求保留来源、时间、置信度、权限、版本和必要的可追溯信息，避免压缩后的 Avatar Core 成为无法审计的黑箱。

7. Procedural State：Skill 与 Workflow

7.1 SkillDescriptor

AIAP v0.4.1 将 Skill 视为可调用能力的描述对象。默认情况下，Avatar 不携带完整 Skill 源码，而保存其身份、语义、来源、版本、完整性、Runtime 兼容性、使用统计与个人偏好。

| 字段组 | 示例 |
| --- | --- |
| Identity | skill_id, version, capability |
| Source | registry / repository / package reference |
| Integrity | hash / signature |
| Compatibility | runtime, requirements |
| Personalization | preference_weight, parameters |
| Usage | usage_count, last_used, success_rate |
| Lifecycle | activity metadata / availability state |

7.2 WorkflowDescriptor

Workflow 是多个能力围绕某类意图形成的可复用过程。AIAP 应保存其可移植逻辑结构，而不要求由某一特定 Workflow Engine 执行。

| 字段组 | 内容 |
| --- | --- |
| Identity | workflow_id, version, owner |
| Intent | 适用任务与触发条件 |
| Steps | 抽象步骤与 capability references |
| Transitions | 步骤关系、条件、可选分支 |
| Parameters | 用户长期偏好与默认值 |
| Statistics | 执行次数、成功率、最近使用 |
| Origin | learned / imported / user_defined |
| Compatibility | 可用 Runtime / Adapter |
| Lifecycle | 活跃度、依赖可用性、失效信息 |

7.3 Learned Workflow

AIAP 允许 Runtime 记录执行轨迹，并从重复、成功的 Skill/Tool 调用模式中形成 Candidate Workflow。候选流程经过系统验证或用户确认后，可以成为 Personal Workflow。AIAP 负责保存这一成果的所有权与可携带表示，而不规定模式发现算法。

Execution Trace → Pattern Detection → Candidate Workflow → Validation → Personal Workflow → Reuse / Evolution

8. Capability Mapping：跨 Runtime 的关键抽象

AIAP 不应把个人工作方式绑定到 `openclaw.some_skill` 等平台私有名称，而应尽可能映射到 Runtime-neutral Capability。

OpenClaw Skill A → AIAP Capability: academic.search → Runtime B Tool → Future Agent Capability

Capability Mapping 允许目标 Runtime 在原 Skill 不存在时寻找等价能力，并根据语义、版本、权限、质量或用户偏好重新绑定。这样迁移的是“用户需要什么能力和如何使用”，而不是某个平台的具体插件实现。

9. 生命周期与多级缓存

Skill 与 Workflow 应具有生命周期元数据，但 AIAP 不把 HOT / WARM / COLD 作为永久、强制的协议事实。AIAP 保存 usage_count、last_used、success_rate、importance、recurrence、dependencies、availability 等事实；Runtime 根据设备、任务与资源条件动态计算缓存层级。

| 逻辑层级 | 典型含义 | 建议处理 |
| --- | --- | --- |
| HOT | 近期高频、高相关 | 本地优先、快速加载 |
| WARM | 仍有价值但近期频率下降 | 保留元数据与必要资源 |
| COLD | 长期低频 | 按需加载 |
| DORMANT | 曾经有价值但依赖失效或长期不可执行 | 保留语义与历史，允许重建 |
| ARCHIVED | 历史保留 | 低成本长期存储 |

周期性 Workflow 不能仅因时间久而降级。例如年度任务虽然 12 个月未使用，仍可能具有高预期价值。因此 Runtime 的 activity score 应考虑 recurrence / expected_next_use，而非单纯按 recency 衰减。

10. Extension Registry

v0.4.1 正式采用 Core Stable + Extension Schema 原则。Skill、Workflow 与未来专业状态域通过注册式扩展进入 Avatar，而不要求每次修改 Core Protocol。

extensions/  skills  workflows  finance  research  coding  education  devices  future.*

每个 Extension 应声明 namespace、schema version、owner/maintainer、compatibility、permissions 与 migration rules。第三方扩展不得绕过 Core 的 Ownership、Authorization 与 Transfer 约束。

11. Adapter Architecture

AIAP 的执行层采用 Adapter Architecture。协议定义统一状态语义，Adapter 负责将 AIAP 对象映射到具体 Runtime。

                 AIAP STANDARD                      \|                  AIAP CORE                      \|              Standard Adapter API          ____________\|____________         \|             \|            \|     OpenClaw        Letta       Future Runtime      Adapter        Adapter         Adapter

v0.4.1 的 Reference Implementation 路线建议只实现 AIAP Core + OpenClaw Adapter，以控制个人开发规模。Letta、LangGraph、Mem0 等均保留为未来 Adapter 或后端，不成为 v0.4.1 的强制依赖。

12. OpenClaw Reference Integration

OpenClaw Adapter 的职责是把 OpenClaw 中可观察的 Skill 使用、任务执行与状态变化映射为 AIAP State，而不是修改 OpenClaw 成为 AIAP 专用 Runtime。

读取并映射可识别的 Skill / Tool capability。

记录 Execution Trace 的标准化摘要。

更新 SkillDescriptor 的 usage statistics。

形成或更新 Candidate Workflow。

将 Personal Workflow 以 Runtime-neutral descriptor 保存。

在导入到其他 Runtime 时进行 Capability Mapping。

因此 AIAP 与 OpenClaw 的关系可以概括为：OpenClaw 负责完成当前任务；AIAP 负责保存这个人长期形成的状态与做事方式。

13. Secure Avatar Transfer v0.4.1 扩展

v0.3 的 Secure Avatar Transfer 继续作为核心安全机制。v0.4.1 将迁移对象从“单一状态包”扩展为 Core-first transfer。

Transfer Avatar Core → Verify Ownership / Integrity → Resolve References → Lazy Migrate State → Rebind Capabilities

13.1 Core-first Transfer

先迁移 Avatar Core，使目标 Runtime 能立即识别 Avatar。

验证 owner、signature、manifest、schema version 与 revocation 状态。

解析 Personal / Procedural State references。

只在任务需要时迁移大体量状态。

对不存在的 Skill 进行 Capability Mapping，而非强制复制不可执行代码。

13.2 Lazy Migration

Lazy Migration 允许用户先获得可用的 Avatar，再逐步迁移历史 Memory、文档、旧 Workflow、Execution Trace 与归档资源。该机制降低跨设备、跨平台迁移成本，也避免一次性暴露全部个人数据。

14. Ownership、Privacy 与 Security

Avatar 的所有权主体与 Runtime 提供方必须逻辑分离。

Skill / Workflow 的个人使用状态属于 Avatar State；第三方 Skill 源码本身的版权与许可证仍归其原权利人。

AIAP 导出不得把第三方凭据、API key 或不可转移 secret 明文打包。

外部引用应支持 integrity hash、签名或等价验证机制。

迁移时应采用最小权限原则，按域授权 Personal State 与 Procedural State。

DORMANT / ARCHIVED 内容仍受原有权限与删除/撤销规则约束。

15. 与 Agent Runtime、Memory 与 Workflow 系统的关系

| 系统类型 | 主要职责 | AIAP 的关系 |
| --- | --- | --- |
| Agent Runtime | 规划、工具调用、任务执行 | Adapter 后端；可替换 |
| Memory Engine | 存储、检索、压缩、召回 | 实现 Personal State；AIAP 定义语义与可携带边界 |
| Skill System | 提供可调用能力 | AIAP 保存 SkillDescriptor 与个人使用状态 |
| Workflow Engine | 执行分支、循环、checkpoint 等流程 | 可选执行后端；AIAP 保存 WorkflowDescriptor |
| AIAP | 个人 AI 状态所有权、可携带性、跨 Runtime 互操作 | 位于上述系统之上/之间的标准层 |

16. Reference Runtime / Core v0.1 实施范围

为避免项目再次膨胀，v0.4.1 白皮书建议第一阶段不开发完整 Agent Runtime。Reference Implementation 只验证协议最关键的可行性。

| 模块 | v0.1 |
| --- | --- |
| Avatar Core | 实现 |
| Identity / Ownership | 复用 v0.3 规范并实现最小验证 |
| State Index | 实现 |
| SkillDescriptor | 实现 |
| WorkflowDescriptor | 实现最小结构 |
| Capability Mapping | 实现基础映射接口 |
| OpenClaw Adapter | 实现 |
| Execution Trace | 记录标准化摘要 |
| Learned Workflow | 先实现候选生成/人工确认，不做复杂自动学习 |
| LangGraph / Letta / Mem0 Adapter | 不进入 v0.1 |
| Marketplace / Settlement | 不进入 v0.1 |

17. 最小验收标准

创建并验证一个 Avatar Core。

从 OpenClaw 侧读取或记录至少一种 Skill/Tool 使用。

生成标准 SkillDescriptor。

记录连续多次 Execution Trace。

从重复路径形成一个 Candidate Workflow。

保存 WorkflowDescriptor，并标记 origin=learned 或 user_defined。

导出 Avatar Core + Procedural Index。

在另一个测试 Runtime/环境中导入并解析。

当原 Skill 不存在时，能够通过 Capability Mapping 提示或绑定等价能力。

在不迁移全部历史数据的情况下完成 Core-first Transfer。

18. Roadmap

| 阶段 | 目标 |
| --- | --- |
| v0.4.1 Spec | 冻结 Spindle Architecture、Avatar Core、Procedural State、Skill/Workflow Descriptor、Capability Mapping |
| Core v0.1 | Python reference core + schemas + CLI |
| OpenClaw Adapter v0.1 | Skill usage / trace / workflow descriptor 映射 |
| Transfer Demo | Core-first transfer + lazy state resolution |
| v0.5 | 第二 Runtime Adapter，验证真正的跨 Runtime portability |
| v0.6+ | 更完善的 learned workflow、capability registry、extension governance |

19. 协议设计原则

| 原则 | 说明 |
| --- | --- |
| User-owned | Avatar 的长期状态应由用户控制，而非锁定于单一 Runtime |
| Runtime-neutral | 协议不绑定单一 Agent、模型或 Workflow Engine |
| Core-small | Avatar Core 保持小、稳定、可迁移 |
| State-extensible | 专业状态域通过 Extension 扩展 |
| Reference-first | 大对象优先引用与验证，而非全部嵌入 |
| Portable procedures | 不仅迁移“知道什么”，还迁移“怎么做事” |
| Lazy migration | 允许 Core 先迁移，大状态按需解析 |
| Security by boundary | 身份、所有权、权限、完整性与迁移边界优先于便利性 |

20. Resolver、分布式身份与外部账户扩展

v0.4.1 在不改变 Spindle Architecture 和 Avatar Core 基本模型的前提下，正式预留 Identity Resolver、State Resolver、External Account Binding 与 Credential / Proof Extension。这些接口只定义互操作边界，不要求 v0.4.1 Reference Implementation 实现区块链、数字货币网络、DID 网络或分布式存储。

20.1 Identity Resolver Interface

Identity Resolver 用于把 Avatar 的稳定身份与一个或多个可验证身份方法连接起来。owner 不应被锁定为单一平台账号，而应允许通过 IdentityProof / IdentityReference 集合进行验证。未来实现可以支持本地密钥、Passkey、DID、多设备证明、多签或 threshold verification，但 AIAP Core 不强制采用区块链。

| 字段/接口 | 含义 |
| --- | --- |
| avatar_id | 稳定 Avatar 标识 |
| identity_proofs[] | 一个或多个身份/所有权证明引用 |
| method | local-key / passkey / did / future.* |
| reference | 外部凭据或 resolver 可解析引用 |
| verification | 签名、challenge-response 或其他验证方法 |
| revocation | 证明撤销或失效状态引用 |

20.2 State Resolver Interface

State Resolver 允许新设备或新 Runtime 在获得 avatar_id 后定位 Avatar Core、Manifest 与扩展状态。AIAP 只定义解析、完整性验证和权限语义；实际存储可以是本地文件、云对象存储、Git、P2P 或未来分布式存储网络。

avatar_id → resolver → manifest → core location → download → signature/hash verification → restore

20.3 External Account Binding

External Account Binding 用于表达 Avatar 与外部账户之间经过授权和验证的绑定关系。它是通用扩展，而不是 CryptoWallet 专用结构，可用于钱包、支付账户、GitHub/云服务身份、组织账户、计算资源账户以及未来 ACU 相关账户。

AIAP 不应在 Avatar Core 中保存数字货币私钥、API key 或其他不可安全迁移的 secret。Core 仅保存账户引用、网络/类型、验证方式、权限范围和必要的完整性信息；签名操作由外部钱包、硬件安全模块、托管服务或其他安全组件完成。

| 建议字段 | 说明 |
| --- | --- |
| binding_id | 绑定关系唯一标识 |
| account_type | wallet / payment / service / compute / organization / future.* |
| provider_or_network | 账户所属系统或网络 |
| account_reference | 公开或可安全解析的账户引用 |
| verification_method | 证明该绑定关系的方法 |
| permissions | Avatar 获得的授权范围 |
| status | active / revoked / expired |
| metadata | 扩展元数据 |

20.4 Credential / Proof Extension

Credential / Proof Extension 为未来的 Verifiable Credentials、选择性披露与零知识证明等机制预留接口。目标是允许 Avatar 在不暴露全部个人数据的情况下证明某项资格、属性或授权。v0.4.1 仅定义扩展点，不规定具体密码学方案。

20.5 联网恢复与 Core-first Transfer

联网恢复应遵循 Core-first 原则：用户或设备首先完成身份挑战，解析并下载 Avatar Core，验证签名、哈希、版本和撤销状态，再解析 Personal State、Procedural State 与外部账户绑定。大体量数据继续采用 Lazy Migration，避免一次性下载或暴露全部个人历史。

Authenticate → Resolve Avatar → Download Core → Verify → Restore Core → Resolve State References → Rebind Capabilities / Accounts → Lazy Migrate

20.6 与 ACU 等未来结算系统的边界

AIAP v0.4.1 不定义 ACU 钱包、数字货币或结算协议。未来如需连接，可通过 External Account Binding 或独立 Extension（例如 aiap.account.acu）完成。这样 AIAP 与 ACU 可以分别发展和验证，在需要时通过标准接口连接，而不使 AIAP Core 依赖任何特定货币、区块链或结算体系。

21. 结论

AIAP v0.4.1 将 AI Avatar 从“可迁移的个人记忆”进一步定义为“可迁移的个人 AI 状态与程序性能力表示”。长期个人历史和能力生态都可以无限增长，但 Avatar Core 必须保持紧凑、稳定和可验证。

在这一架构下，Memory 保存一个人的经历与知识状态，Skill 描述其常用能力，Workflow 保存其长期形成的做事方法；Runtime 负责执行，AIAP 负责所有权、语义、引用、兼容和迁移。

Runtime can be replaced. The Avatar remains with the user.Runtime 可以替换，但 Avatar 属于用户。

附录 A：v0.4.1 新增术语

| 术语 | 定义 |
| --- | --- |
| Spindle Architecture | Personal State 与 Procedural State 两端可扩张、Avatar Core 中间保持紧凑的 AIAP 架构 |
| Avatar Core | Avatar 的最小高密度、可携带、可验证表示 |
| Personal State | 与个人长期记忆、偏好、知识和语境有关的状态集合 |
| Procedural State | 描述个人如何使用能力与完成工作的 Skill / Workflow 状态 |
| SkillDescriptor | Runtime-neutral 的 Skill 身份、能力、来源、版本、完整性与个人使用状态描述 |
| WorkflowDescriptor | 可移植的工作流程语义与结构描述 |
| Capability Mapping | 将不同 Runtime 的具体能力映射到统一能力语义的机制 |
| Lifecycle Metadata | 用于推导活跃度、缓存与可执行状态的事实性元数据 |
| Core-first Transfer | 先迁移 Avatar Core，再解析或按需迁移扩展状态的方式 |
| Lazy Migration | 按任务需求逐步迁移大体量状态与资源 |

附录 B：规范文件建议

AIAP-CORE-SPEC.md

IDENTITY-SPEC.md

OWNERSHIP-SPEC.md

TRANSFER-SPEC.md

KEY-MANAGEMENT.md

STATE-MODEL-SPEC.md

AVATAR-CORE-SPEC.md  [v0.4.1 new]

PROCEDURAL-STATE-SPEC.md  [v0.4.1 new]

SKILL-DESCRIPTOR-SPEC.md  [v0.4.1 new]

WORKFLOW-DESCRIPTOR-SPEC.md  [v0.4.1 new]

CAPABILITY-MAPPING-SPEC.md  [v0.4.1 new]

EXTENSION-REGISTRY-SPEC.md

ADAPTER-SPEC.md

schemas/*.json

附录 C：v0.4.1 新增兼容性规范建议

IDENTITY-RESOLVER-SPEC.md

STATE-RESOLVER-SPEC.md

EXTERNAL-ACCOUNT-BINDING-SPEC.md

CREDENTIAL-PROOF-EXTENSION-SPEC.md

