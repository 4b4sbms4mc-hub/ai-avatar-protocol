# 03 Memory Lifecycle

版本：0.1-draft；作者：Wang Lu。

| 维度 | 字段/结构 | 含义 |
|---|---|---|
| 逻辑层 | level: M0/M1/M2/M3 | 临时、活跃任务、长期、归档 |
| 访问范围 | scope | 归属、空间、策略版本 |
| 有效状态 | candidate/active/superseded/revoked | 候选、有效、被替代、撤销 |
| 存储冷热 | Runtime 本地策略 | 不由逻辑层决定设备或数据库 |

## 记录

memory-record 保留 v0.1 的 memory_id、level、type、content、source、retention 等字段，强制增加 scope、revision、previous_revision、derived_from、lifecycle、updated_at、confidence。

内容允许正文或结构化引用；引用不自动可读。source_type 沿用 explicit-user/observed/inferred/imported/system/external-generated。source_ref 是证据引用，verified=true 这种旧字段不能代替证据验证。confidence 是可信度描述，不是认证结果。

source 为 inferred 的新记录进入 candidate；模型不得通过高 confidence 或反复检索将其静默转为 active。人工确认或受信规则晋升需记录新的确认依据，但不抹去最初来源。

## 层级状态

- M0 默认会话临时，不默认持久化或迁移。
- M1 表示活跃任务，任何生活/工作空间均可拥有。
- M2 保存确认的长期状态；稳定偏好受到保护。
- M3 为可再次检索的逻辑归档，可同时 status=active。

本 Profile 不再输出旧 status=archived：迁移时转换为 level=M3,status=active 并保留转换证据，前提是无撤销/删除标记。旧 status=deleted 转为 tombstone，正文进入清理流程而非普通 memory-record。

## 归档规则

仅在 automatic_archive=true、对象 active、level 属于 M1/M2 且时间窗满足时考虑归档。下列任一条件均阻止自动归档：pinned、decay_exempt、stable_preference、未完成任务引用、recurrence_ref 非空、expected_next_use 在保护窗内或已到期尚未核实。

本草案采取保守周期保护：存在 recurrence_ref 一律保持，直到受信周期解析器确认新的可归档条件。身份和授权规则不走普通记忆衰减。min_importance/minimum_level 等旧字段不能覆盖这些保护；无法解释旧规则时进入待复核。

时间基准优先 last_used_at，没有则使用 created_at；后台扫描和索引不能更新 last_used_at。时间在未来或不一致时返回时间错误，不自动归档。示例 M1=30 天、M2=180 天是本地夹具策略，不是协议固定值。

每次变化生成版本化 StateDelta，记录 from/to、原因、策略版本、时间和来源。不自动删除。M3 重激活先验证当前事实、权限与任务价值；不能因被检索就无条件晋升。固定偏好保持层级不意味着永久在每个会话注入。

recall_count 为历史命中统计；context_use_count 和 confirmed_use_count 分开记录。一次命中不提高事实权威等级。服务应对使用事件去重，不使重复事件累计虚假使用量。

## 更正与删除

更正产生新版本并将旧事实标为 superseded；并发偏好冲突不能按时间戳自动覆盖。删除独立授权，清理正文、索引、派生和缓存并生成 tombstone。归档、撤销、删除分别处理，归档不降低权限。
