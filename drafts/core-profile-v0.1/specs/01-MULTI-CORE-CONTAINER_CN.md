# 01 Multi-Core Container / Avatar Bundle

版本：0.1-draft；作者：Wang Lu。

## 对象与不变量

Bundle 是 Core 外部的组织清单。cores 的每个条目有 avatar_id、owner_ref、core_ref；shared_spaces 保存共享空间引用。容器本身没有自动正文读取权。重复 avatar_id、同一 Core 的冲突版本、owner 不匹配必须拒绝。

单成员也是一个 Bundle。多成员只扩展列表，不改变 User Core 的语义。Shared Space 不属于第一个引用它的成员；引用数量不改变控制主体。

每个 Core/Shared Space 的策略与密钥作用域分别管理。容器索引不是公开目录，也可能泄露成员和项目存在性。管理员有整理文件权限并不具有读取权限；若要防宿主机管理员读取，还需要独立密钥与加密存储部署，本包并未实现。

## 分离算法

1. 从已验证的主体请求选择 avatar_id；读取当前可信 Core 与授权策略。
2. 仅遍历获授权 Core 的索引。每个节点按对象当前归属逐一检查 export 权，不以 read 代替 export。
3. 构造 transfer-manifest：included/reference-only/excluded/unresolved。缺失依赖不能默认为 included。
4. 被排除对象的标识本身若不可披露，对外只提供脱敏原因；不能通过导出失败信息枚举其他成员。完整内部审计留在授权边界内。
5. 输出包含必要获准对象的包，独立校验后恢复到隔离区。Core 分离不得修改其他成员 Core 或共享内容控制权。

Bundle 的物理拷贝仅是存储操作，不是逐成员内容授权。按成员恢复必须逐一验证当前所有权与撤销记录；旧快照不得恢复过期组织资格。

## 第一阶段

实现一个成员、多个 scope 与逐 Core 接口；以两个虚构成员作为拒绝访问的测试夹具。家庭 UI、部门树和企业管理可后续实现；不能使用隐含“唯一用户”来省略请求身份。

## 失败条件

未知 Core、owner 不符、无 export 权、其他成员对象被携带、不可披露索引泄露、共享依赖被静默忽略，均为失败。`restore_guarantee=offline-complete` 还要求依赖闭包中所有必要实际对象完整可用。
