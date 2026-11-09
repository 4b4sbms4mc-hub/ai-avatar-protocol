# 00 Core 表达与兼容契约

作者：Wang Lu。状态：0.1-draft。本文“必须/不得”为本 Profile 的实现要求；示例不代表已实现。

## 1 不改变纺锤架构

Personal State 与 Procedural State 可增长；Avatar Core 保存身份、受控摘要引用和索引。`avatar-core.schema.json` 是本轮建议的紧凑 Core 具体表达，依据 v0.4.2 的字段方向新建，不冒称已存在的正式 Core Schema。`profile_summary` 在此草案中采用受权限保护的摘要对象引用数组，而非不受控的明文大段摘要。解析摘要依然需要授权。

`owner.owner_ref` 是控制主体引用；`owner_key_ref` 与 `avatar_key_ref` 分离，不能含私钥。`identity_refs` 连接 Identity Resolver。所有引用必须校验来源、版本、权限和撤销状态。`state_index` 与 `procedural_index` 只保存对象引用；完整记忆不嵌入 Core。

Core 的 `integrity.manifest_sha256` 指向由安全 Profile 指定的、排除 integrity 自身的受保护 Core 内容摘要；具体字节规范及签名验证依赖受支持安全 Profile。未配置真实安全 Profile 时仅可结构审阅，不可激活导入的 Core。占位签名永远不得接受。

`revision` 为对象本地正整数版本，初版为 1 且 previous_revision=null，后续版本为旧值+1。Schema 不能比较两个字段，服务必须验证连续性。全局身份由 avatar_id 表达，不另发 core_id 竞争标识。state_id 是状态集合，不是 Avatar 身份。

## 2 版本化叠加

`state-profile.schema.json` 用 allOf 引用原始 v0.1 State Schema，再强制扩展 manifest 与 memory-record 约束。原始 `$id` 和文件内容完全保留，不把 0.1 字符串改成 0.4.2。

`extensions["x-aiap-core-profile"]` 保存 Profile Manifest；必须校验 state_ref.id 与外层 state_id 一致、owner_id 与目标 Core owner 一致、avatar_id 与 core_ref 一致、版本可解析。required_extensions 必须含 x-aiap-core-profile / 0.1-draft / critical=true，条目 namespace 必须唯一。

**旧 v0.1 校验器可能接受新增对象，但忽略安全语义。** 所以结构兼容不等于可安全消费。部署入口必须在解析前识别封装 Profile、核对受支持的关键扩展；不认识时拒绝激活。不能期待不懂此规则的旧 Runtime 自行拒绝。

普通未知非关键扩展仅可保留原始字节或等价 JSON 数据并禁用使用；未知关键扩展拒绝。不得为通过旧校验而剥离 critical 声明或权限。

## 3 全对象保护

object-reference 携带对象标识、版本、scope 和摘要。这些都是待验证声明，必须与可信状态库当前记录比对；调用者不能通过传入一个较宽松 scope 改写真实权限。

记忆正文使用 memory-record 的 scope；其他域、Core 摘要及 Workflow/Trace 使用相同外部保护记录和 object-reference。未建立保护记录的 identity/preferences/skills/workflows/permissions、未知扩展和外部引用默认禁止投影、检索或导出。`state-profile` 不是“整份可发给模型”的载荷；它的结构校验不能覆盖所有域的安全语义。

任何组织业务对象都留在相应组织状态库。示例 state-profile 故意混合不同 scope 用于隔离测试，不能把它视为个人离线备份。真正 Core 索引只携带获准引用，完整状态仅按请求授权投影。

## 4 与既有规范的映射

| 既有概念 | 本包对应 | 处理 |
|---|---|---|
| domains.aiap.memory | memory-record 细化 | 保留域名与原始记录字段 |
| M0—M3 | level | 与业务空间独立 |
| provenance | source | 保留 source_type，要求 source_ref |
| retention | pinned/decay_exempt | 保留并加强保护 |
| StateDelta v0.1 | state-delta 外层封装 | 原始 changes 不改，按 change_id 绑定范围与版本 |
| RuntimeContext | Authorized View 引用 | 不改变六接口的语义 |
| Capability/Workflow | 原始 v0.1 Schema | 通过外部保护记录继承访问限制 |

不得把生活/工作添加成 aiap.memory 的替代域，也不得把 M1 解释成职业数据。适配等级、状态模型等级、Profile 合规性分别声明。
