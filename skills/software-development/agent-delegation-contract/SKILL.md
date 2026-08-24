---
name: agent-delegation-contract
description: "Version, launch, and verify bounded AI-agent work through task contracts, runtime limits, and CI checks."
version: 1.0.0
author: Marat Kiniabulatov
license: MIT
metadata:
  hermes:
    tags: [ai-agents, governance, coding-agents, ci, delegation]
---

# Agent delegation contract

Use this skill when an AI agent receives authority to inspect or change a codebase and the team needs repeatable, reviewable boundaries.

A contract is not a prompt reminder. It is a task-specific, machine-readable input to four controls:

1. **Pre-flight:** the launcher checks that the contract exists and is complete.
2. **Runtime:** the agent receives only the relevant contract and has least-privilege access.
3. **CI:** the pull request is checked against allowed paths and required evidence.
4. **Decision:** a named human accepts changes with product, data, security, or production consequences.

## Repository layout

```text
.agent/
  AGENTS.md                     # short persistent instruction
  policies/baseline.md          # stable rules for every run
  contracts/ORD-184.json        # task-specific contract
  workflows/contract-guard.yml  # CI check copied to .github/workflows/
```

Keep `AGENTS.md` short. Do not paste a growing archive of old contracts into it. The launcher or task prompt passes the exact contract file for the current run.

Start from the files in `templates/`:

- `delegation-contract.json` — a task contract that a human can review and tooling can parse.
- `AGENTS.md` — a short instruction that tells the agent where the current contract is and when to stop.
- `contract-guard.yml` — a GitHub Actions check for changed-file boundaries.

## Operating sequence

1. Copy the contract template to `.agent/contracts/<TASK-ID>.json` and complete every placeholder.
2. Give the agent the task ID and contract path. The launcher must reject a missing or invalid contract.
3. Restrict credentials, network access, environments, and branch permissions outside the prompt. A contract cannot revoke permissions that have already been granted.
4. Require the PR description to contain `Contract: .agent/contracts/<TASK-ID>.json`.
5. Run the CI guard. It verifies that the declared contract exists and that the PR changed only allowed paths.
6. Require the named owner to review evidence and decide on merge. The agent never merges a protected branch.
7. Record stop conditions and exceptions. Turn a recurring exception into a clarified template field, automated check, or tighter access rule.

## Safety rules

- A broad token defeats a narrow contract. Use separate credentials and isolated environments.
- `allow_paths` is a CI guardrail, not an authorization system. Use branch protection and environment protection for actual authority.
- No automatic merge, production deployment, access grant, irreversible data change, or external communication without a separately configured approval gate.
- Do not put secrets, customer data, internal incident details, or production credentials in the contract file.

## Verification

Before accepting the PR, verify:

- the PR points to the exact versioned contract;
- changed paths are within the allowed scope;
- required tests and evidence are attached;
- no stop condition was ignored;
- the named owner approved the decision;
- any action with consequences had an explicit approval in the designated channel.
