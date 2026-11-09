# 错误码与拒绝规则

作者：Wang Lu。错误响应应包含 code、request_id、retryable 和安全可披露的原因；不暴露其他空间正文、对象存在性或密钥信息。

| code | 条件 | 默认处理 |
|---|---|---|
| E_SCHEMA | 结构/字段/格式不符合 | 拒绝对象 |
| E_CRITICAL_EXTENSION | 未知或缺失必需扩展 | 拒绝激活 |
| E_IDENTITY | 无法验证操作者或 Owner | 拒绝 |
| E_SCOPE | 对象与请求/可信空间不符 | 拒绝 |
| E_DENIED | 权限不满足 | 拒绝，避免存在性泄露 |
| E_REVOKED | 当前撤销记录有效 | 失效旧视图 |
| E_POLICY_VERSION | 使用旧策略版本 | 重新决策 |
| E_CONFIRMATION_REQUIRED | 证据或范围未确认 | 候选暂存 |
| E_VERSION_CONFLICT | 更新基线过期 | 不提交，等待复核 |
| E_IDEMPOTENCY_CONFLICT | 同请求标识不同载荷 | 拒绝 |
| E_REFERENCE_UNRESOLVED | 必要引用无法解析 | 隔离并报告受控依赖状态 |
| E_INTEGRITY | 摘要/签名/清单不符 | 拒绝激活 |
| E_DESTINATION | 迁移目的地不符 | 拒绝 |
| E_EXPIRED | 时间窗失效 | 拒绝 |
| E_TIME | 时间不合法或无法可靠比较 | 停止自动状态变化 |
| E_REPLAY | 挑战已消费 | 拒绝新提交 |
| E_CRYPTO_PROFILE_UNSUPPORTED | 未实现指定安全 Profile | 拒绝真实激活/迁移 |
| E_OPERATION_UNSUPPORTED | 模式/域更新未实现 | 不执行 |

发生任一拒绝不能回退到无权限过滤的检索、明文导出或旧版直接加载。可保留隔离候选，但不得向模型提供其正文。
