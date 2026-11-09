<!-- SPDX-License-Identifier: CC-BY-4.0 -->
> Source transcription of the accompanying DOCX by Wang Lu. Draft design; not a declaration of implemented compatibility. The original DOCX controls if formatting is ambiguous.

AIAP State Model状态模型规范 v0.1

AI Avatar Protocol（AIAP）核心状态模型规范状态：草案版本：0.1公开作者：Wang Lu日期：2026年9月

1. 目的

AIAP State Model（AIAP 状态模型）定义一种可迁移、由用户控制的个人 AI 持久状态表示方式。

AIAP State 的目的并不是定义 AI 模型如何推理、Agent 如何执行工具，也不是规定某个 Runtime 如何保存对话历史，而是为个人 AI 的持久状态建立标准化表示，使个人 AI 在更换大语言模型、Agent Runtime、设备、应用、AI 服务提供商、Skill 生态和 Workflow 引擎之后仍能保持连续性。

核心原则：

“个人 AI 的持久状态属于用户，不应天然绑定于特定模型、Agent Runtime、应用或服务提供商。”

因此，AIAP State 构成 Portable Personal AI State Layer（可迁移个人 AI 状态层）。

2. 设计原则

AIAP 将 Model、Agent Runtime 与 AIAP State 明确分离：

Model  ↓Agent Runtime  ↓AIAP State  ↓User

Model 负责推理，是可替换的计算资源，不是 AIAP State 的事实源。

Agent Runtime 负责模型调用、工具执行、Sandbox、Agent Loop、上下文管理、Subagent、任务规划与 Session 管理。OpenAI Agents API、Agents SDK、OpenClaw 以及其他 Agent 系统都可以作为 Runtime。

AIAP State 则表示应当跨模型、跨 Runtime 持续存在的用户特定状态。AIAP 不试图替代 Agent Runtime。

3. 范围

AIAP State Model v0.1 定义六个一级状态域：

AIAPState├── Identity（身份）├── Preferences（偏好）├── Memory（记忆）├── SkillProfile（技能画像）├── WorkflowProfile（工作流画像）└── Permissions（权限）

六者共同构成 Portable Personal AI State。

4. AIAP State 根对象

每一个 AIAP State 包必须包含根状态清单（State Manifest）。根对象不得要求特定模型提供商，默认不得包含 API Key 或模型服务凭证。Secret 应由 Runtime 的安全凭证存储系统管理。

示意结构：{  "aiap_version": "0.1",  "state_id": "aiap-state:uuid",  "owner_id": "aiap-id:uuid",  "identity": {},  "preferences": [],  "memory": [],  "skills": [],  "workflows": [],  "permissions": [],  "metadata": {}}

5. Identity State（身份状态）

Identity 描述 AI State 的所有者。Identity 与 Memory 必须分离。Identity 应包含持久所有权信息，也可以包含经用户授权的个人资料信息。

Identity 应与现有 AIAP Identity System 和 Secure Avatar Transfer 规范兼容。Identity 不得仅依据模型生成内容进行推断。身份修改应要求所有者明确授权。

6. Preference State（偏好状态）

Preferences 描述影响 AI 行为的稳定或半稳定用户选择，包括沟通偏好、输出格式、语言、软件、工具、推理或报告风格以及应用设置。

每条 Preference 应具有来源、置信度、状态、创建时间和更新时间等元数据。

7. Preference 来源

每项偏好必须记录其来源。建议来源类型包括 explicit-user（用户明确指定）、observed（观察所得）、inferred（推断所得）、imported（导入）和 system（系统）。

建议可信优先级：explicit-user → imported-verified → observed → inferred

推断偏好不得静默覆盖用户明确表达的偏好。

8. Preference 生命周期

Preference 应支持 candidate、active、superseded、archived 等生命周期状态。新偏好替代旧偏好时，应保留可追踪的状态变化，而不是简单覆盖。

9. Memory State（记忆状态）

AIAP Memory 表示能够跨 Session 或 Runtime 保持价值的持久信息。AIAP 必须将 Memory 与原始对话历史区分。

Runtime 可以保存 Conversation Transcript，但不应自动将所有聊天历史升级为持久 AIAP Memory。

AIAP Memory v0.1 定义四个逻辑层：M0 — Session / Ephemeral（会话/临时）M1 — Working Memory（工作记忆）M2 — Long-Term Memory（长期记忆）M3 — Archive（归档）

10. M0 — Session State

M0 保存当前任务需要的临时上下文，例如当前文件、临时变量、任务计划、未解决问题和临时工具结果。典型生命周期为分钟到小时。M0 在 AIAP 导出中是可选的，大多数 M0 信息不应自动永久保存。

11. M1 — Working Memory

M1 保存预计在当前活跃阶段继续有价值的信息，例如当前项目、最近使用的工具、未完成工作和活跃任务上下文。典型生命周期为数天到数周，可以衰减或归档。

12. M2 — Long-Term Memory

M2 保存具有长期价值的信息，例如稳定项目背景、重要决策、重复出现的工作偏好、项目之间的重要关系，以及关于用户工作的稳定知识。M2 应保持紧凑，原始对话通常不应直接存入 M2。

13. M3 — Archive

M3 保存通常不会直接注入模型上下文、但在需要时可以检索的历史信息，例如旧项目、历史交互摘要、历史 Workflow、旧状态和过去决策。归档可以存放在外部存储中，同时通过 AIAP 元数据保持可寻址性。

14. Memory Object

标准 Memory 对象建议包含 memory_id、level、type、content、source、confidence、importance、recall_count、created_at、last_used_at、status 和 tags。每条长期记忆应能够说明“内容是什么、来自哪里、可信程度如何、何时创建、何时被使用”。

15. Memory Promotion（记忆晋升）

AIAP 定义 Memory Promotion 概念，但不规定唯一算法：

Observation → M0 → candidate → M1 → 重复相关性/用户确认 → M2

Runtime 可以综合 importance、frequency、recency、user confirmation、cross-session reuse、confidence 和 source trust。

概念上：P_m = f(I,F,R,C,T,U)

其中 I 为重要性，F 为重复频率，R 为检索相关性，C 为置信度，T 为来源可信度，U 为用户明确确认。具体函数 f 属于 Runtime 实现层。

16. Memory Provenance（记忆来源）

每条持久 Memory 应保存 Provenance。AIAP 必须区分用户明确陈述、Agent 观察、Agent 推断、系统导入以及外部系统生成的信息。

User Statement ≠ Agent Inference。

两者不得拥有相同的权威等级。

17. Skill Profile（技能画像）

AIAP v0.1 不标准化具体 Skill 的内部实现，而标准化用户与 Skill 的关系。

Skill Profile 描述：有哪些 Skill、用户信任哪些 Skill、使用频率、授予了哪些权限、在哪些上下文中表现较好，以及兼容性信息。

18. Skill State 与 Skill Implementation

AIAP State 保存 Skill identity、configuration、preference、usage statistics、permissions 和 compatibility。

AIAP State 不要求保存 Skill 可执行代码、Container、Runtime Binary、Dependencies 或 API Credential。这些属于具体 Runtime 或 Marketplace。

19. Workflow Profile（工作流画像）

Workflow 是 AIAP State 的一级对象，而不是 Memory 的附属类型。

Skill = capability（能力）Workflow = composition of capabilities toward an objective（面向目标的能力组合）

Workflow 描述“用户如何完成工作”，这是 AIAP 与普通长期记忆系统之间的重要区别。

20. Workflow Object

Workflow 对象应包含 workflow_id、name、version、origin、status、trigger、steps、usage、confidence、created_at 等信息。Steps 可以引用 Action、Skill 或其他 Workflow。

21. Learned Workflow（学习型工作流）

AIAP 支持 user-defined、imported、application-defined 和 learned 四类 Workflow 来源。

学习型 Workflow 来自重复且成功的执行模式：

Repeated Agent Executions→ Pattern Detection→ Workflow Candidate→ Validation→ Personal Workflow

协议不规定具体 Workflow Learning 算法。

22. Workflow Promotion

Workflow 晋升类似 Memory Promotion：

P_w = f(F,S,U,C)

F 为执行频率，S 为历史成功率，U 为用户批准，C 为上下文一致性。

Workflow 在获得广泛权限或成为高度自主的执行流程之前，原则上应获得用户明确确认。

23. Personal Workflow Graph

AIAP 可以将 Workflow、Skill、Context 与 Project 之间的关系表示为图结构，长期形成 Personal Workflow Graph（个人工作流图谱）。

它表达的不只是“用户知道什么”，而是“用户怎样工作”。这是个人 AI 长期积累价值的重要组成部分。

24. Permissions State（权限状态）

AIAP 必须将“知道”与“有权执行”分离。

AI 知道用户经常执行某项操作，并不意味着 AI 自动获得未来自主执行该操作的权限。Permission 对象应明确 Subject、Resource、Action、Scope、Approval 和 Expiration。

25. Permission Principle

AIAP 采用以下基本原则：

Memory is not permission.Preference is not permission.Historical behavior is not permission.

即：记忆 ≠ 权限偏好 ≠ 权限历史行为 ≠ 权限

过去经常发送邮件，不意味着 AI 自动拥有以后自主发送邮件的权力。

26. Permission Levels

兼容 Runtime 建议支持 deny、ask、session、workflow、project、persistent 等授权等级，并默认遵循最小权限原则。

27. State Relationships

AIAP State 的不同状态域可以相互引用，从而回答：用户偏好哪些 Workflow？某 Workflow 依赖哪些 Skill？拥有哪些权限？哪些 Memory 支持这个 Workflow？某 Preference 来源于哪里？

28. State Lifecycle

每一个持久 AIAP Object 应支持 candidate、active、superseded、archived、revoked 和 deleted 等生命周期状态。除非所有者明确要求删除，否则被替代的对象不应无痕消失，以支持审计和安全同步。

29. State Ownership（状态所有权）

每一个 AIAP State Object 最终必须归属于 AIAP Identity。

owner_id → AIAP Identity

服务提供商可以存储或处理 AIAP State，但存储位置不决定所有权：

storage ≠ ownership。

30. State Portability（状态可迁移性）

兼容 AIAP 的实现必须提供 Portable State 导出机制。最小导出应包含 manifest、identity、preferences、memory、skills、workflows、permissions 和 metadata。

推荐目录：aiap-state/├── manifest.json├── identity.json├── preferences.json├── memory.jsonl├── skills.json├── workflows/├── permissions.json└── metadata.json

31. Secrets Exclusion

可迁移 AIAP State 默认不应包含明文 API Key、密码、私有认证 Token、Session Cookie 或私钥。可以保存安全凭证引用，例如 vault://openai/default，由接收 Runtime 重新完成授权。

32. State Transfer（状态迁移）

AIAP State Transfer 应使用现有 Secure Avatar Transfer 机制：

Source Runtime → State Export → Owner Authorization → Integrity Verification → Destination Runtime → State Import

迁移过程中应尽可能保留 Object ID。

33. Partial Transfer（部分迁移）

AIAP 必须支持部分 State Transfer。用户可以只迁移 Identity、Identity + Preferences、Memory、特定 Workflow、特定 Skill，或者完整 State，从而避免“全有或全无”的迁移方式。

34. Selective Disclosure（选择性披露）

AIAP 用户可以只向应用暴露 State 的一个子集：

Full State → Authorized View → Application-specific State

例如写作应用可以读取 writing.* 偏好，却无权读取财务 Workflow 或私人 Archive。

35. Runtime Isolation

应用不应自动获得完整 AIAP State。Runtime 应使用 Scoped View，只向应用暴露完成任务所必需的 Preferences、Memory、Workflow 和 Permission。

36. State Synchronization

AIAP v0.1 在概念上定义同步语义，但不规定唯一 Transport。可以支持 Local-only、Local + Encrypted Cloud、P2P、企业私有服务器、个人 NAS 和用户控制的云。AIAP 必须保持 Storage-provider Neutral。

37. Conflict Resolution

多设备同时修改 State 时，应保存 Object Version、Updated Timestamp、Origin Device 和 Previous State Reference。语义冲突不得被静默覆盖。

38. State Trust

导入对象应包含 Trust / Provenance 信息。建议可信级别包括 owner-verified、trusted-runtime、verified-import、unverified-import、inferred 和 untrusted。

39. State Integrity

AIAP State Package 应支持密码学完整性验证。未来版本应定义 Canonical Serialization 与 Signature Requirements。

概念上：H = SHA256(CanonicalState)

随后可以由授权 Identity Key 对 State Hash 签名。

40. AIAP State 与 Agent Session

Agent Session History 不等于 AIAP State：

Session = what happened（发生了什么）AIAP State = what should persist（什么应该持续存在）

这是 AIAP 的基本边界。

41. AIAP State 与 Agent Memory

现代 Agent Framework 可以拥有自己的 Persistent Memory。AIAP 不标准化其内部实现，而通过 Adapter 将其中适合长期保存和迁移的信息转换成 AIAP State：

Agent Memory → AIAP Adapter → AIAP Memory State。

42. AIAP State 与 OpenClaw

OpenClaw 类 Runtime 可以通过 Adapter 将本地 User/Profile 信息映射为 Preferences 与部分 Identity Metadata，将长期 Memory 映射为 M2，将日常 Memory 映射为 M1/M3，将 Skills 映射为 Skill Profiles，将重复执行模式映射为 Workflow Profiles。

这些映射属于参考实现，而不是强制规定。

43. AIAP State 与 OpenAI Agents

OpenAI 类 Runtime 可以将 Session 映射为 M0/M1 临时上下文，将 Agent Memory 转换为 Candidate AIAP Memory，将 Tools 映射为 Skill Profile，将重复 Agent Execution Pattern 转换为 Workflow Candidate。

因此 AIAP 是 Agent Infrastructure 的补充层，而不是替代层。

44. Conformance Levels（兼容等级）

Level 1 — State Reader：可以读取 AIAP State，并消费 Preferences、Memory 与 Workflow。

Level 2 — State Runtime：可以读取、写入、更新、晋升、归档和导出 AIAP State。

Level 3 — Portable Runtime：进一步支持安全 State Transfer、Provenance Verification、Selective Disclosure、Permission Preservation 与跨 Runtime 互操作。

45. Minimum Viable AIAP Runtime

AIAP Runtime v0.1 的最小推荐实现包括：State StoreIdentity ManagerPreference ManagerMemory ManagerSkill RegistryWorkflow EnginePermission ManagerModel GatewayImport / Export

46. 推荐本地架构

参考本地目录：

~/.aiap/├── manifest.json├── identity/├── preferences/├── memory/├── skills/├── workflows/├── permissions/├── archive/└── indexes/

Runtime 可以额外使用 SQLite、Vector Index、Graph Index 和 Cache。这些属于实现细节，不决定协议兼容性。

47. AIAP State Boundary（协议边界）

AIAP v0.1 标准化：什么是持久个人 AI State、如何表示、属于谁、来自哪里、谁可以访问、如何导出以及如何迁移。

AIAP v0.1 不标准化：LLM 推理、Agent Planning、Tool Execution Engine、Vector Database、Workflow Scheduler、Embedding Provider、Cloud Infrastructure、Agent Reasoning Strategy 和 Model Routing Algorithm。

这一边界是有意设计的。

48. 核心架构原则

AIAP 必须维持以下分层：

User↓AIAP State  Identity / Preference / Memory / Skills / Workflows / Permissions↓AIAP Runtime Adapter↓OpenClaw / OpenAI Agents / Other Runtime↓Models

AIAP State 是用户层与 Agent Runtime 之间的持久个人状态层。

49. Primary Invariant（首要不变量）

AIAP State 的首要不变量：

“更换执行引擎，不应天然要求更换用户的持久 AI 身份或个人状态。”

Model A → Model B不应意味着Personal AI A → 一个完全无关的新 Personal AI B。

多个 Model / Runtime 可以在用户授权范围内操作同一份持续演化的 AIAP State。

50. 概念定义

AIAP State 可形式化定义为：

S_AIAP = I + P + M + K + W + A

其中：I = IdentityP = PreferencesM = MemoryK = Skill ProfileW = Workflow ProfileA = Authority / Permissions

更准确地：S_AIAP(t) = {I, P_t, M_t, K_t, W_t, A_t}

状态演化：S_(t+1) = F(S_t, E_t, U_t)

其中 S_t 是当前 AIAP State，E_t 是新的观察或执行经验，U_t 是用户明确决策，F 是状态转换机制。F 属于 Runtime 实现，不由 v0.1 强制规定。

51. 战略定义

AIAP State 不是 Conversation History Format，不是 Prompt Format，不是 Model Checkpoint，也不是 Agent Framework。

它是：

“个人 AI 的持久身份、偏好、记忆、习得能力、工作流与权限的一种可迁移、由用户控制的表示。”

因此，即使底层 Model、Tool、Application、Runtime 与 Infrastructure 改变，Personal AI 仍可以保持连续性。

52. 后续规范

AIAP State Model v0.1 建立概念模型。后续建议形成：AIAP-STATE-SCHEMA — 正式 JSON SchemaAIAP-MEMORY-SPEC — Memory 生命周期与晋升AIAP-WORKFLOW-SPEC — Workflow 表示与学习AIAP-SKILL-SPEC — Skill Identity 与 CompatibilityAIAP-PERMISSION-SPEC — Capability 与 AuthorizationAIAP-STATE-TRANSFER — State Migration ProtocolAIAP-STATE-SYNC — 多设备同步AIAP-ADAPTER-SPEC — Runtime 互操作AIAP-STATE-CRYPTO — Encryption 与 Signing

53. v0.1 总结

AIAP State Model v0.1 建立六个一级状态域：Identity、Preference、Memory、Skill、Workflow、Permission；以及四项基本属性：Ownership、Portability、Provenance、Interoperability。

其长期目标是使用户拥有一个能够跨 AI 生态持续存在的 Personal AI State，而不会因为模型、Agent、设备或平台更换而失去已经积累的偏好、记忆、Skill、Workflow 和授权边界。

54. Personal State Uniqueness Principle（个人状态独特性原则）

AIAP 不试图定义“人是什么”，也不主张一个数字状态能够完整表示一个人。

AIAP 所定义的是：一个人的部分独特性如何在数字智能系统中，以用户授权的方式持续表达、积累、控制和迁移。

核心表述：

“AIAP 不定义一个人，而是定义一种由用户控制、可迁移的数字表示，使一个人在 AI 世界中长期积累的部分独特性能够跨 AI 系统持续存在。”

AIAP State 的独特性来自 Identity、Preferences、Memory、Skill Profile、Workflow Profile 与 Authority 的组合及其长期演化。任何单个组成部分都可能被许多人共享，但这些状态的组合、来源、演化路径与历史可以逐渐形成与特定个人关联的状态。

54.1 Non-Fungibility of Personal AI State（个人 AI 状态的非同质性）

AIAP 引入 Personal AI State Non-Fungibility 原则。

这里的“非同质性”并不意味着一个人可以被数据还原，而是指：即使底层计算基础设施可以互换，长期积累的 Personal AI State 也不应因此被视为彼此可互换。

Models are replaceable; personal state is not interchangeable.模型可以替换，个人状态不可互换。

因此，即使两个用户使用相同 Model、相同 Runtime 和基本相同的 Skills：

Model_A = Model_BRuntime_A = Runtime_BSkills_A ≈ Skills_B

也不意味着：S_AIAP^A(t) = S_AIAP^B(t)

因为两者的身份、选择、经历、偏好、Workflow 与授权决策会随时间形成不同的状态演化路径。

54.2 Human Uniqueness and Digital Representation（人的独特性与数字表达）

AIAP State 不得被解释为一个人的完整表示、模拟、副本或定义。

它只是人在与 AI 系统长期交互过程中形成的、有限的、经过授权的、可撤销的、持续演化的数字表示。

Human ≠ AIAP State

AIAP State ⊂ Digital Representation(Person)

因此可以形成：

Human Uniqueness↓ 授权的数字表达Personal State Uniqueness↓ AIAP 标准化Portable Personal AI

这一边界既保留 AIAP 对个人连续性的表达能力，也避免把“人的身份”简单等同于一组存储数据。

54.3 Continuity Across Replaceable Models（跨可替换模型的连续性）

Personal AI 可以理解为可替换的计算智能与持久、用户控制的 State 之间的结合：

Personal AI(t) = Model/Runtime + AuthorizedView(S_AIAP(t))

Model A → Model BRuntime A → Runtime B

不应天然意味着 Personal AI 的连续性被终止。

模型主要决定 AI“能做什么”；AIAP State 则帮助确定这个 AI“为谁工作、被授权知道什么、已经学习了哪些用户偏好和工作模式，以及哪些权限约束它的行为”。

54.4 Personal State Uniqueness Principle — 正式表述

尽管 Model、Skill、Tool 和 Runtime 可以共享或替换，与特定个人关联的 AIAP State 会随着该个人的身份、选择、偏好、经历、Workflow 和授权决策持续演化。

因此，即使底层计算基础设施完全相同，不同个人的 Personal AI State 仍然具有非互换性。

这一原则为 AIAP 的 Ownership、Portability 和 Secure Transfer 提供概念基础：迁移 AIAP State 的目的不仅是“移动数据”，更是为了在技术平台不断变化的情况下，保持个人与 AI 长期积累关系的连续性。

54.5 核心人本表述

AIAP 不试图定义一个人。

AIAP 要解决的是：

“让一个人在 AI 世界中长期形成的独特性，不再随着模型、Agent、设备和平台的更换而消失。”

因此，AIAP 对人的独特性的作用不是定义 Human Uniqueness 本身，而是提供一种标准，使这种独特性的部分数字表达能够被用户拥有、授权、积累、迁移并持续存在。

—— AIAP State Model Specification v0.1 中文版结束 ——

