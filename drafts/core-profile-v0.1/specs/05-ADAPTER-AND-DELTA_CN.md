# 05 Adapter 与受控更新

版本：0.1-draft；作者：Wang Lu。

## 保持六接口

inspect_runtime、compile_context、resolve_capability、execute_workflow、emit_trace、export_delta 保持 v0.1 语义。inspect_runtime 报告实际支持的 Profile、scope 过滤、撤销及处理接收方能力；不支持就不能宣称分域合规。L1/L2/L3 不替代安全验收。

compile_context 的输入必须已通过访问决策，输出 Authorized View 及 RuntimeContext 的获准片段。可在既有 RuntimeContext.extensions 中加入 `x-aiap-core-profile` 的 view 引用；入口仍需可信验证，不能只检查扩展存在。

OpenClaw USER.md 仅允许投影经授权的跨场景偏好子集。生活、个人工作和组织内容通过隔离上下文或独立受控工作区注入。无法保证当前 Runtime 清理旧上下文时，必须使用新隔离会话/实例；不得以提示词要求“忽略私人内容”替代隔离。

## Delta 包装

外层 state-delta 包含 request、原版 delta 和 bindings。原版 schema_version=0.1 不变，外层 profile_version=0.1-draft。候选入口仅接受 delta.status=proposed；validated/accepted 由服务内部生成，不能让 Adapter 直接提交已接受状态。

每个 change_id 必须与 bindings 一一对应、无重复或遗漏；binding 指明 target_object_id、scope、base_revision、source_refs 与 confirmation_ref。request avatar/runtime 必须与 delta 一致，并具有 write 授权。base_revision=0 只允许 add 新对象；更新必须等于可信当前版本。

candidate 的结构按 change.domain 决定：aiap.memory 使用 memory-record；其他域使用相应 Schema 加外部保护记录，未实现的域拒绝持久更新，不能因 candidate 是任意 JSON 就放行。memory candidate.memory_id 与 target_object_id 必须相同；scope 与可信对象匹配。正常更新不得重定向 owner 或空间，跨空间复制需要独立授权动作。

候选内容不直接写入最终状态。按顺序执行：身份验证 → Schema → 当前权限 → 证据与确认 → 版本一致性 → 约束检查 → 原子提交及审计。submitted candidate.revision/previous_revision 不决定最终版本，最终由服务根据基线生成并校验。

推断保持 candidate 或等待有效确认；confirmation_ref 字符串不等于已经确认。身份/权限/Core 摘要属于受保护更新，不得由普通记忆 Delta 绕过。

## 冲突及事务

默认全部变更原子提交，任意失败则不提交；若以后允许部分接受，须启用明确协商并逐条报告，不能静默跳过。基线过期返回 E_VERSION_CONFLICT 并保留候选供复核。重试通过 delta_id 与载荷摘要幂等，同 id 不同内容返回 E_IDEMPOTENCY_CONFLICT。

Core 与引用状态库共同构成权威状态；OpenClaw 文件与向量索引是使用副本。用户通过 OpenClaw 修改长期状态应形成候选回写，不进行文件双向无条件覆盖。

索引更新失败时权威写入与索引状态分别记录，避免返回可检索成功的假结论。查询必须过滤过期对象版本；撤销/删除优先失效缓存与读取权限。
