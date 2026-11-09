<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# AIAP current design drafts

Author and maintainer: Wang Lu. Synchronized 2026-11-09.

The latest local design baseline is the [Chinese whitepaper v0.4.2 revision draft](../whitepaper/drafts/AIAP_Whitepaper_v0.4.2_CN.md). It extends v0.4.1 with Multi-Core Container / Avatar Bundle, Space and Consent, memory lifecycle and scoped transfer. The accompanying original DOCX files are preserved byte-for-byte; Markdown transcriptions support online reading. [Source hashes](../whitepaper/drafts/SOURCE_MANIFEST.json) identify these particular source files.

Read the whitepaper, State Model and Procedural State companion documents in [whitepaper/drafts](../whitepaper/drafts/), then the [Core Profile v0.1-draft](core-profile-v0.1/README_CN.md). The profile includes the supplied State Schema v0.1, Procedural State v0.1 and Runtime Adapter v0.1 under `upstream/`; it contains 17 additional schemas, 18 examples and 61 limited contract tests.

These drafts do not replace the public v0.3 identity/ownership/key/transfer specifications, change the 0.3.0 reference validator version, or certify the current runtime. Capability is a first-class object. The State Model root example is conceptual; actual State Schema v0.1 validation uses its `domains` registry.

## Version and compatibility boundaries

| Component | Version | Meaning |
| --- | --- | --- |
| Whitepaper | 0.4.2 revision draft | Current design intent |
| State Model / State Schema | 0.1 | State concepts / data contract |
| Procedural State / Runtime Adapter | 0.1 each | Object and six-interface contracts |
| Core Profile | 0.1-draft | Versioned extension and limited rule fixtures |
| Public v0.3 reference validator | 0.3.0 | Existing identity and transfer helpers |
| La Vida / Core Service | 0.3.5 source candidate / 0.2.0; published plugin 0.3.4 | Separate OpenClaw memory implementation |

Core Profile `SOURCE_MANIFEST.json` identifies the historical inputs recorded by that package. Those DOCX byte hashes differ from the current local documents published here. Both records are preserved; no byte-equivalence or complete semantic equivalence is claimed between different source snapshots. The current document manifest is the source of truth for this synchronization.

## Requirements to evidence

| Requirement | Schema / specification | Implementation and evidence | Remaining gap |
| --- | --- | --- | --- |
| Compact signed Core | `schemas/avatar-core.schema.json` | La Vida `core/aiap_core/service.py`, Core tests | Local bootstrap is not remote Owner verification |
| Scoped access before retrieval | `access-request`, `space`, `authorized-view`, Space and Consent | Single-owner general/life/work grants; Core and plugin tests | Organization/multi-member policy and cross-domain derived data |
| Controlled StateDelta | `state-delta`, Adapter and Delta | Proposal, independent Owner approval, version and transaction checks | Other protected state domains and generalized consent |
| Memory lifecycle | `memory-record`, `lifecycle-policy`, `tombstone` | M1/M2/M3 and partial archive/delete handling | Full propagation and current revocation/deletion on historical restore |
| Bundle / Shared Space | `bundle-manifest`, `membership`, `space` | Schema and finite rule fixtures | Real multi-member runtime and separation tests |
| Scoped secure transfer | `transfer-manifest`, `scoped-transfer-certificate` | Structure and rejection fixtures; v0.3 signing helpers separate | Crypto-profile mapping, durable nonce consumption, dual-runtime import |
| Portable procedures | Upstream Capability, Workflow, Binding, Trace schemas | Protocol contracts | Complete execution and second-runtime continuity |

Runtime evidence lives in [aiap-openclaw](https://github.com/4b4sbms4mc-hub/aiap-openclaw/tree/main/lavida). Schema acceptance alone never establishes identity, authorization, replay protection or safe execution. No Adapter L1/L2/L3 or complete AIAP compliance claim is added by this synchronization.

The 0.3.5 source candidate includes actual LM Studio `qwen/qwen3.5-9b` conversation probes and retained failure history. The tested configuration directly presents three tool schemas, clarifies manual proposals despite disabled automatic capture, and uses exact identifiers for literal retrieval. This model-specific evidence does not certify default dynamic tool-directory behavior, production/NAS topology or historical revocation-aware restore. Publishing candidate source does not overwrite the existing 0.3.4 release assets.

## Validation

```sh
python -m pip install -r drafts/core-profile-v0.1/requirements.txt
python drafts/core-profile-v0.1/tools/validate.py
python -m unittest discover -s drafts/core-profile-v0.1/tests -v
```

On 2026-11-09, Codex reran all 61 profile contract tests and validated all 18 examples, resolving 35 local schemas without network schema downloads. The existing public validator test also passed. CI runs these separately so future draft changes do not silently bypass validation.

The repository license map applies: code, schemas, examples and tests Apache-2.0; prose and whitepapers CC BY 4.0. Existing trademark and third-party rights remain in force.
