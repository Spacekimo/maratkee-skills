---
name: agent-verification-assurance
description: Use when an AI coding agent creates or changes material behaviour and the team must keep intent, interpretation, acceptance tests, and evidence connected.
---

# Semantic Acceptance Assurance

## Problem and promise

A green agent-authored test suite can prove only that code satisfies the agent's interpretation. When information is incomplete, an agent may turn an unstated assumption into an acceptance test, implement it, and leave reviewers to reconstruct the intended rule from a PR.

This skill prevents **silent semantic drift**. It does not invent missing domain knowledge. It makes unknowns, alternatives, and the accountable decision visible **before production code**.

```text
evidence → interpretation → human decision → approved scenario → test → CI evidence
```

A test is evidence for an approved meaning; it is never the source of that meaning.

## Use when

Use for medium/high-risk changes to user-visible behaviour, business rules, APIs, integrations, workflows, or acceptance/contract tests. Keep low-risk work light: observable `done_when`, ordinary test evidence, and PR review are enough when behaviour and its test are already obvious.

Do not use this record to authorize deployment, production-data access, or any other consequential action. Pair it with `agent-delegation-contract` for authority, scope, and escalation.

## Roles

- **Implementation agent** — researches, drafts artifacts, writes approved tests and code; never approves semantics.
- **Semantic owner** — one named, reachable human accountable for the intended outcome. This can be a product/process owner, or a technical owner for a truly technical rule; it need not be a system analyst.
- **Evidence reviewer** — checks that tests and observed behaviour support the approved scenario. For medium risk, the semantic owner may also review evidence, but records two distinct decisions. For high risk, use a different named human.
- **Escalation owner** — resolves missing or conflicting sources through the delegation contract.

A team, a role name, an LLM, or an unreachable person is not semantic approval.

## Artifacts

For each medium/high-risk change, keep small versioned artifacts with the task:

| Artifact | Purpose | Authority |
|---|---|---|
| Delegation contract | scope, access, owners, stop conditions | accountable human |
| Semantic Decision Map | facts, interpretations, alternatives, unknowns | evidence only; no authority |
| Acceptance Map / OpenSpec delta | approved requirement and scenarios | semantic owner |
| Test and CI evidence | proves the approved scenario was exercised | evidence reviewer |

Use exactly one canonical scenario mode:

- **Standalone:** `.agent/acceptance/<TASK-ID>.yml` is the Acceptance Map.
- **OpenSpec:** OpenSpec delta owns requirement/scenario text; `assurance.yml` links it to decisions, tests, and evidence.

Do not create a separate research note on a protected base branch. The Decision Map travels with the task artifact and is explicitly referenced by the contract.

## Quality gates

### Gate 1 — Evidence discovery (read-only)

Before drafting a target scenario, inspect only sources allowed by the contract: repository code, tests, Git history, approved documents, and explicitly authorized read-only systems.

Record in the Semantic Decision Map:

- observed facts with immutable references (path + commit, document version, or URL);
- whether each basis is `documented` or `unwritten`;
- the current behaviour/state relevant to the task;
- plausible interpretations and open questions.

Do not call a source "current" merely because it exists. Do not access production or external systems unless the contract explicitly grants safe read access. A mismatch between approved target behaviour and current code may be the intended baseline gap; a conflict between authoritative sources is a stop condition.

### Gate 2 — Semantic decision

The agent drafts the map and a compact decision packet. The semantic owner chooses one of:

- `approved` — selected interpretation is intended;
- `revise` — change the requirement/scenario and review again;
- `clarify` — information is insufficient; stop implementation;
- `accept_risk` — no authoritative artifact exists, but the named owner records this interpretation as a conscious risk decision.

For every material requirement, show: evidence, selected interpretation, relevant alternatives, unknowns, and one concrete decision question.

**No production-code change for a medium/high-risk task until every material requirement has a named human decision of `approved` or `accept_risk`, with `decided_at` and `decision_evidence_ref`.** `accept_risk` also requires a non-empty risk note. Absence of recorded alternatives is not evidence that a rule is unambiguous.

Without a decision, the agent may only prepare the map, characterization tests, or draft scenarios. It must not present its draft as approved acceptance semantics.

### Gate 3 — Approved acceptance test

After Gate 2, write acceptance tests before production code. Each material scenario must:

- describe an observable outcome, not an internal call or implementation detail;
- reference the approved requirement and decision;
- name one or two plausible wrong outcomes in `rejects`;
- link each rejection to an assertion, challenge, or manual procedure that actually detects it.

Keep test types separate:

- **Characterization test:** records what the base system does. It is not a claim that the behaviour is correct.
- **Approved acceptance test:** records what the owner decided the system must do. It governs implementation and merge evidence.

### Gate 4 — Baseline and implementation

Before implementation, record one honest baseline type:

- `gap_demonstrated` — base violates the approved rule on the exercised path;
- `new_capability` — the approved capability does not yet exist;
- `existing_behavior_change` — the owner intentionally changes a previously accepted behaviour;
- `not_practical` — a stable baseline run is infeasible; record why and what was inspected instead.

A passing baseline does not ban an approved production change. Conversely, an agent must not claim a defect from a stubbed, bypassed, or otherwise non-exercised path.

Then follow TDD: approved acceptance test → observed baseline → minimal implementation → candidate pass. Any semantic amendment returns to Gate 2 with a new record version.

### Gate 5 — Independent evidence review

Before merge, the evidence reviewer verifies the chain from left to right:

1. The named human approved the selected interpretation and any `unwritten` basis was an explicit risk decision.
2. Every material scenario links to a runnable test/manual procedure and candidate evidence.
3. Tests exercise the changed boundary and observe an outcome, rather than only a mock or internal call.
4. Each material `rejects` item has a linked assertion/challenge/manual proof.
5. The implementation did not redefine the approved semantics.
6. Open questions are resolved, accepted explicitly as risk, or escalated.

A green CI result without this chain is not acceptance.

## Workflow

1. **Classify risk** in the delegation contract.
2. **Discover** evidence and create the Decision Map from `templates/semantic-decision-map.yml`.
3. **Draft** the standalone Acceptance Map or OpenSpec delta; add only its exact paths and the Decision Map path to contract `allow_paths`.
4. **Ask one bounded decision question** to the named semantic owner.
5. **Record the decision** and approve the map/spec only after the human decision.
6. **Write and run** approved acceptance tests; record baseline type and evidence.
7. **Implement minimally**, run candidate verification, and link CI/manual evidence.
8. **Review evidence** using the Gate 5 checklist; use a different named human for high-risk work.

## Stop and escalation rules

Stop and send the delegation-contract escalation package when:

- authoritative sources conflict;
- a material interpretation has no recorded human decision;
- the agent needs an out-of-scope source, permission, or file;
- the test cannot exercise the relevant boundary;
- implementation requires changing an approved meaning.

Do not resolve these conditions by choosing the most convenient interpretation.

## Review checklist

```text
[ ] Contract names semantic owner, evidence reviewer, and escalation channel.
[ ] Decision Map distinguishes observed facts, selected interpretation, alternatives, and unknowns.
[ ] Every material requirement has documented evidence or an explicit owner risk decision, plus `decided_at` and a decision reference.
[ ] Owner approved every material interpretation before production code.
[ ] High-risk evidence reviewer is a different named human; medium-risk semantic and evidence decisions are recorded separately.
[ ] Characterization tests are not presented as target acceptance tests.
[ ] Every approved scenario links to outcome-oriented verification and candidate evidence.
[ ] Every material rejected outcome has a proof link.
[ ] Baseline type and exercised boundary are recorded honestly.
[ ] No semantic change occurred without a new owner decision.
```

## Templates

- `templates/semantic-decision-map.yml` — evidence, interpretation, alternatives, and owner decision.
- `templates/acceptance-map.yml` — standalone requirement-to-evidence map.
- `templates/openspec-assurance.yml` — OpenSpec adapter.
- `templates/openspec-verification-assurance.json` — contract fragment for OpenSpec mode.
- `agent-delegation-contract` — scope, permissions, and escalation around the work.
