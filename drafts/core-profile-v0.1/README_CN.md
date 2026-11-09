# AIAP Core 配套规范与 Schema 修订包

**版本：Core Profile v0.1-draft｜依据：AIAP Whitepaper v0.4.2 中文修订草案｜作者：Wang Lu｜2026-09-19**

本包将白皮书的多成员、分域记忆与迁移边界具体化为四组配套规范及 JSON Schema 草案。它是供审阅与实现的协议工作包，不是已部署的 Core Service，不是新的 AIAP 总白皮书，也不声明完成安全迁移。

## 从这里开始

1. 阅读 `specs/00-CORE-AND-COMPATIBILITY_CN.md`，确认版本与紧凑 Core 的关系。
2. 按 01—04 阅读四组规范；05 定义 Adapter/StateDelta 衔接。
3. 用 `examples/INDEX.json` 找到每个示例的 Schema。
4. 阅读 `MIGRATION_CN.md` 与 `ACCEPTANCE_CN.md`，再实现 Core Service。

## 内容

| 目录或文件 | 用途 |
|---|---|
| specs/ | Core 衔接、多成员、空间授权、生命周期、分范围迁移、Adapter、错误码 |
| schemas/ | 新 Profile 的独立 Schema；JSON Schema Draft 2020-12 |
| examples/ | 虚构成员、生活与工作记忆、组织记忆、状态候选及迁移结构 |
| upstream/ | 三个已提供 v0.1 ZIP 的原样内容；保留原有 schema $id |
| tools/validate.py | 离线 Schema 注册、示例与用户指定 JSON 校验 |
| tools/reference_rules.py | 测试用的有限语义参考，不是身份验证器或运行服务 |
| tests/test_contracts.py | 结构失败案例、兼容关系和有限规则测试 |
| VALIDATION_REPORT.json | 本次实际执行结果与未实现边界 |
| SOURCE_MANIFEST.json / CHECKSUMS.sha256 | 来源及交付文件摘要 |

## 版本

- 总白皮书保持 v0.4.2；State Model、State Schema、Procedural State、Adapter 保持各自 v0.1。
- 本包 Profile 独立为 `0.1-draft`，正式发布前可有不兼容修订。
- 紧凑 Core 草案的 `aiap_version: 0.4.2` 表示本轮白皮书数据表达；旧 State 容器仍为 `aiap_version: 0.1`，Adapter 内层仍为 `schema_version: 0.1`。三者不可混用。
- `schemas.aiap.invalid` 是未发布 Schema 的保留占位主机，不是已运营的网站。校验器按本地 `$id` 注册，禁止联网取 Schema。
- 所有签名与身份示例均是虚构占位符，不能通过真实密码学验证。不得用于真实迁移或直接覆盖 OpenClaw 数据。

## 运行校验

使用 Python 3.10 或更高版本，在本包根目录运行：

```bash
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python tools/validate.py
.venv/bin/python -m unittest discover -s tests -v
```

Windows 可将 `.venv/bin/python` 换为 `.venv\Scripts\python.exe`。安装依赖需要包源；之后本包所有 Schema 解析均离线。也可使用已有的合适 Python 环境。

校验单个对象：

```bash
python tools/validate.py --schema schemas/memory-record.schema.json --input examples/memory-record.json
```

语法校验通过不证明身份、授权、密钥、签名、撤销、防重放、并发原子性、缓存隔离或 OpenClaw 实际行为。测试边界见验收清单。

## 下一步实现

先实现单成员 Core Service，保持 subject/avatar/space/action/purpose 全链路传递；让虚构工作查询不能召回生活与公司数据。再接 OpenClaw，避免把全部域写进全局 USER.md。现有 Memory 配置作为检索后端验证基础。

本包未修改原 LICENSE 或商标政策，不新增开源许可授权；对外发布时应沿用并核对项目现有许可文件。
