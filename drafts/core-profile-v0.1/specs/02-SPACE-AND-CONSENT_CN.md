# 02 Space and Consent

版本：0.1-draft；作者：Wang Lu。

## 空间类型

personal-general、personal-life、personal-work、family-shared、organization、department、project 是访问空间类型。父空间引用表达组织关系，不自动继承读写权；controller_ref 必须匹配可信组织/个人控制主体。个人可以属于多个互相隔离的组织。

通用偏好只有在明确授权的用途和 Runtime 中可使用。“通用”不等于公开。工作场景的工作、组织与通用空间必须显式选择，不能自动访问全部公司。

## 请求与身份

access-request 中 authenticated_subject_ref 和 auth_evidence_ref 必须由受信身份验证层生成或验证；客户端填写不构成认证。session_ref、runtime_ref、avatar_id、space_refs、action、purpose 与时间窗必须绑定到同一已验证会话。模型不得自行扩大 space_refs 或将任务变换成更宽的 purpose。

同一会话切换生活/工作，应建立新的 Authorized View 并清除旧上下文及其缓存，不能仅切换标签。跨域共享应基于明确授权，最小披露日程忙闲结果也需检查接收者与用途。

## Policy 精确匹配 Profile

本草案规则使用精确 subject、object_id、runtime 和 purpose 列表，不支持通配符或隐含角色继承。session_refs 空数组表示在该规则其他约束范围内允许任意已认证会话；非空则必须匹配。processor_refs 是允许的数据接收方列表，空数组意味着不允许外部处理接收方。

每次读取先获取可信对象 scope 和当前 policy，不使用请求声明替换之。policy.controller_ref 必须有该空间的管理授权；policy.space_ref 必须等于对象空间；对象 policy_ref 必须指向当前有效版本，变化后失效旧视图。

规则适用条件：主体、对象、Runtime、用途、时间均匹配，membership 非空时还要验证当前成员关系及版本。效果遵循默认拒绝、deny 优先。revoked/过期的 allow 不能放行；撤销和删除记录优先于规则。

read、write、share、export、delete、admin、process 分开授予。出域处理需要同时通过当前读取/共享决策、process 动作授权以及接收方约束。Embedding 服务是处理接收方，即使位于局域网也不因此自动获准。源对象禁止出域时不得先生成远端向量再过滤。

角色仅用于成员描述；从角色生成访问规则需要另行验证的策略管理操作。本包参考规则测试不实现角色推导或 shared membership 验证，遇到相应情况拒绝。

## 授权与 Consent

authorization_evidence_ref 是已验证用户同意或组织授权记录的引用，必须能证明签发者、范围、有效期和撤销状态。它不是普通聊天内容，也不是给一个字符串就会生效的凭证。Consent/Identity 证明的验证由受信组件提供；缺失或不能解析即拒绝。

所有者不能授予自己并不拥有的公司导出权。容器管理员不自动成为私人空间 controller。对组织内容的导出需要组织授权及个人请求的共同约束。

## 派生、索引和缓存

摘要、向量、Trace、Workflow 的 derived_from/外部保护记录必须保留所有来源及版本。组合结果只能在所有来源共同允许的范围使用；跨范围重新发布需要授权，不自动取权限并集。任一来源撤销时重新评估派生对象。

先确定授权候选集合，再进入向量检索/排序/模型上下文；若后端不支持可靠过滤，则分区索引。缓存至少绑定 subject、avatar、session、space、purpose、processor、对象版本、policy 版本及 revocation_epoch。旧视图即使未到 expires_at 也会因撤销失效。

## 删除

tombstone 独立记录已删除对象范围和清理进度，不保存原文。备份恢复先应用当前 tombstone 与撤销，再检查引用；不得凭旧 policy 或对象恢复访问。物理清理与逻辑拒绝分别报告。
