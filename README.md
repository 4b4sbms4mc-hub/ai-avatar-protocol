<!-- SPDX-License-Identifier: CC-BY-4.0 -->
# AI Avatar Protocol (AIAP)

## Current design and public implementation

The latest design is the [v0.4.2 Chinese whitepaper revision draft](whitepaper/drafts/AIAP_Whitepaper_v0.4.2_CN.md). [Draft specifications, version boundaries and implementation gaps](drafts/README.md) include Core Profile v0.1-draft and the State, Procedural State and Runtime Adapter v0.1 contracts. Original source documents and their hashes are included.

The public v0.3.0 identity/transfer reference release below remains available unchanged. Draft versions do not imply equivalent implemented runtime functionality or complete AIAP compliance.

## Reference Implementations

AIAP is designed as a runtime-neutral open interoperability standard.

The first public reference adapter is:

-**AIAP OpenClaw Adapter**-
an OpenClaw reference integration. The current La Vida 0.3.4 / Core Service 0.2.0 prerelease implements a single-owner scoped memory proposal/approval/recall loop. The legacy v0.3.0 MCP validation bundle is separate; secure cross-runtime memory transfer and a second runtime remain future work.

Repository:
https://github.com/4b4sbms4mc-hub/aiap-openclaw

>OpenClaw is a reference integration target and is not part of the AIAP core standard.

> **Public Release v0.3.0** — AIAP is intended as an open interoperability standard. Independent open-source and proprietary implementations are permitted under the repository license map. See `OPEN-STANDARD-POLICY.md`, `GOVERNANCE.md`, `LICENSE`, `IP-POLICY.md`, and `TRADEMARK.md`.


**Author / Project Maintainer: Wang Lu**

AIAP is an open protocol for user-owned, verifiable, portable, and extensible personal AI Avatars.

## This release contains
- English Whitepaper v0.3 (`WHITEPAPER.md` and DOCX)
- Normative Identity / Ownership / Transfer / Key Management specifications
- JSON Schema Draft 2020-12 schemas for Core objects
- Python reference validator and Transfer Certificate signing helpers
- examples and tests

## Quick start

```bash
python -m venv .venv
# activate the virtual environment
pip install -e .[dev]
aiap validate identity examples/identity.json
pytest
```

## Repository layout

```text
spec/        normative specifications
schemas/     formal JSON Schemas
src/aiap/    reference implementation
examples/    example AIAP objects
tests/       conformance-oriented tests
whitepaper/  publication files
```

## Protocol relationship

AIAP = Avatar identity / ownership / portability layer  
MCP = Agent/model ↔ tools and data  
A2A = Agent ↔ Agent collaboration

AIAP is designed to interoperate with MCP and A2A through adapters rather than replacing them.

## License model
- Code, Schemas, SDK/reference implementation: Apache-2.0
- Whitepaper/specification documentation: CC BY 4.0
- AIAP / AI Avatar Protocol names and logos: separate trademark policy
