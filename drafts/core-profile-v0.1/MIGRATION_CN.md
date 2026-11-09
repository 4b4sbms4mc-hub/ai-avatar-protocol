# 旧版迁移说明

作者：Wang Lu。目标：在不覆盖旧文件的前提下制作待验证的新 Profile 数据。

## 原则

旧数据进入隔离暂存区；保存原文件字节和 SHA-256，不自动扩大访问范围。缺失 owner、space、policy 或来源时标为待分类，不能为省事全部指定 personal-general。无法确认归属的公司/家庭资料不导入个人权威状态。

## 映射

| v0.1 数据 | 新 Profile | 限制 |
|---|---|---|
| state_id / owner_id | 保留 | 验证与实际 Core 身份关系 |
| aiap_version=0.1 | 保留 | 不替换成白皮书版本 |
| memory_id / level / type / content | 保留 | level 不解释成生活/工作 |
| source | 保留并补 source_ref | 无证据时不能伪造 verified |
| status=archived | M3 + active | 仅在确认未撤销/删除时转换 |
| status=deleted | tombstone + 清理队列 | 不复活正文 |
| pinned / decay_exempt | 保留 | 为稳定偏好补保护须有依据 |
| last_accessed_at / recall_count | 保留为旧统计 | 不冒充真实上下文使用 |
| 旧 default_rules | 保留原文供审计 | 新 lifecycle-policy 接管执行，防双重降级 |
| 缺少对象版本 | 审核后从 revision=1 开始 | 不伪造旧版本链 |
| legacy StateDelta | 外层绑定范围及版本 | 缺失基线必须复核，不直接接受 |

本 Profile 中根 memory policy 的旧默认规则仅为兼容载体；新消费者必须只执行 lifecycle.policy_ref 解析出的新策略。旧策略中的 M0 自动清理或 M2 demote-to-M1 不能在本 Profile 下继续暗中运行。M0 会话清理属于独立 Runtime 临时数据策略。

## 操作顺序

1. 备份原文并计算摘要；读取 v0.1 Schema 确认结构。
2. 人工或受信分类规则确认 Core、owner、空间与策略，记录审批来源。
3. 为每个持久对象建立保护记录，含非 memory 域；未知对象保持隔离。
4. 补充版本与来源，构造 Profile manifest；执行组合 Schema 校验。
5. 检查跨对象引用、身份、权限、归档保护和扩展支持；结构通过不能替代此步。
6. 使用虚构数据在独立环境验证恢复、删除及拒绝访问，之后才安排真实导入。

## 回退

恢复上一份权威状态快照之前，先应用当前 tombstone 与撤销记录。原始 v0.1 备份只用于审计/重建，不直接交给无法识别 Profile 的旧 Runtime。需要向旧 Runtime 提供上下文时只能通过 Authorized View 投影，不能剥离安全字段做全量降级。

此包不附自动将所有历史记忆归类的迁移程序；来源/归属信息无法从旧结构可靠推断。阶段性导入器应输出明确的 pending-classification 清单。
