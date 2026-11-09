# 04 Scoped Transfer

版本：0.1-draft；作者：Wang Lu。

## 范围与证书

transfer-manifest 列出 Core 集合、空间、操作模式、对象引用及 included/reference-only/excluded/unresolved。certificate.payload 覆盖 source、destination、owner_refs、avatar_ids、space_refs、mode、nonce、issued_at、expires_at、manifest_sha256、authorization_refs、required_extensions。

**这是新的范围约束 Profile 草案，不是对未提供 v0.3 证书 Schema 的逐字段兼容声明。** 本次资料包含白皮书的迁移要求，但未提供可核对的原始 Transfer Certificate Schema；正式与它整合前须补做映射。不得将本草案直接称为最终兼容证书。

## 签名覆盖与字节边界

所有 payload 字段必须被认证签名完整覆盖，不能仅签 owner 或 nonce。manifest_sha256 使用导出时保存的 manifest 原始 UTF-8 文件字节的 SHA-256，禁止导入时重排 JSON 后再计算。对象 sha256 同样覆盖实际导出字节；重编码产生新摘要和新的受保护清单。加密模式必须明确摘要覆盖明文对象还是加密封装，不能混用。

payload 的规范编码、签名算法、密钥格式、域分离上下文、加密封装与轮换链由另行登记的 crypto_profile 固定。此包尚未选择或实现生产密码学 Profile，因此所有签名例子只作结构测试，真实 Core 激活和安全迁移必须返回 E_CRYPTO_PROFILE_UNSUPPORTED。

多所有者证书至少需要覆盖全部迁移 avatar 的有效控制主体授权；组织对象另外验证控制主体导出授权。proofs 数组长度不代表授权已经齐全，验证器必须把每个签名者映射到实际权利。

## 实施流程

1. 接收方认证并产生不可预测的一次性挑战，记录目的地与失效时间。
2. 来源方读取当前授权，构造获准范围清单；逐项检查 export，不用 read 代替。
3. 授权主体确认范围；完整签名 payload 与清单摘要。
4. 接收方检查受支持 Profile、目的地、当前所有权/撤销、时效、挑战、签名及内容摘要，拒绝未知关键扩展。
5. 隔离导入区解析依赖。未通过验证对象不得进入检索或模型上下文。
6. 在同一事务或等效原子机制中提交对象与 nonce 消费记录。幂等重试用 certificate_id+payload 摘要查已有结果；相同 nonce 不同 payload 拒绝，已消费的新会话请求拒绝。
7. 输出恢复报告；源端删除或权限撤销是单独动作，不能由 runtime-move 字符串自动触发。

## 模式

backup-copy 不改变 Owner；runtime-move 更换执行位置但不自动改变 Owner；ownership-transfer 改变控制权，第一阶段必须明确拒绝，待专用身份授权 Profile 完成。三种模式不能混称“迁移成功”。

Core-first Transfer 可先携带紧凑 Core，其他状态按授权 Lazy Migration；每次解析重新校验，不因首次导入而永久放行。

## 恢复保证

references-portable 只声明引用可携带。offline-complete 必须检查被选择范围的所有必要对象、依赖闭包、完整性和可解密性；不允许任何必要 unresolved/reference-only 依赖。排除不相关对象可成立，但排除必要依赖则不能声明完整。Schema 无法从列表独自判定闭包。

导入旧备份先应用当前删除/撤销状态；组织引用须重新授权。不具备可信当前状态的离线环境只能隔离保存，不能推定所有权和组织权限仍有效。

## 本包测试边界

测试覆盖结构缺字段、摘要被篡改可检测、时间比较与清单范围不一致的拒绝规则；不声称真实签名、防重放持久化、双端认证或原子事务已验证。
