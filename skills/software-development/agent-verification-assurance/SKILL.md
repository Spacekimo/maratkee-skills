---
name: agent-verification-assurance
description: Use when an AI coding agent creates or changes behaviour and a team must validate that requirements, acceptance examples, tests, and evidence remain meaningfully connected.
---

# Agent Verification Assurance

## Overview

Use this skill when a green agent-authored test suite is not enough evidence that the intended behaviour was delivered. It creates a compact, reviewable chain:

```text
requirement / outcome → approved acceptance example → executable verification → CI evidence → acceptance decision
```

The central artifact is an **assurance record**: a small versioned YAML file for one change. In `standalone` mode it is an Acceptance Map that owns requirements and examples; in `openspec` mode it links OpenSpec's canonical requirements and scenarios to tests, CI evidence, and approvals without copying them. It is not a replacement for a requirements-management system, BDD tooling, human product judgment, or technically enforced permissions.

Do not require hidden model reasoning or chain-of-thought. Record observable provenance instead: the approved canonical-spec and assurance-record versions, requirement sources, agent run or contract ID, code/test references, CI evidence, assumptions, and human decisions.

## When to Use

Use this skill when:

- an AI agent will implement or materially change user-visible behaviour, a business rule, API contract, integration, workflow, or critical operational flow;
- an agent creates or changes acceptance tests, contract tests, or other tests used as merge evidence;
- a reviewer needs to see the route from requested outcome to executable test and CI result;
- a team needs a lightweight pre-code approval gate without introducing a large requirements tool;
- an incident or repeated rework suggests that green tests are accepting the wrong interpretation.

Do not use it for:

- a pure refactor with no intended observable behaviour change; record normal test evidence instead;
- a trivial local fix whose outcome and existing test are obvious and whose risk is low;
- an attempt to prove software correctness from a matrix alone. The map supports judgment; it does not make a requirement complete or a test strong by itself.

## Required Capabilities

Before relying on an assurance record, verify that the team has:

| Capability | Why it matters | If unavailable |
|---|---|---|
| Version-controlled change record | Preserves approved intent and its revisions | Keep a reviewed Markdown record, but label the audit gap |
| Named semantic owner | Decides whether examples mean the right thing | Do not let an agent define or change acceptance semantics alone |
| Executable test or observable manual procedure | Turns examples into evidence | Define a manual acceptance check and record who performed it |
| CI or recorded test output | Shows that verification actually ran | Require explicit manual execution evidence before acceptance |
| PR or equivalent review | Compares map, tests, and implementation | Do not merge consequential changes autonomously |

If the semantic owner cannot be reached or sources of truth conflict, the agent must stop and ask for a decision. Do not treat an agent's confidence as approval.

## Choose One Specification Mode

Declare `spec_mode`, `canonical_spec_ref`, and `assurance_record_ref` in the delegation contract for every medium/high-risk change. Never infer the mode from the presence of an `openspec/` directory: a repository can be migrating or have historical artifacts. A change uses exactly one canonical source for requirement/scenario semantics. In `standalone`, both refs normally point to the same Acceptance Map; in `openspec`, the canonical ref points to the delta specs and the assurance ref points to `assurance.yml`.

| Mode | Canonical requirement and scenario source | Assurance record location | Template |
|---|---|---|---|
| `standalone` | Acceptance Map | `.agent/acceptance/<TASK-ID>.yml` | `templates/acceptance-map.yml` |
| `openspec` | OpenSpec delta specs in the change folder | `openspec/changes/<CHANGE>/assurance.yml` | `templates/openspec-assurance.yml` |

### Standalone mode

Use when the team does not use OpenSpec for the change. The Acceptance Map is the source of truth and normally contains one to five requirements and one to seven examples. Each important behaviour needs only these links:

1. **Requirement** — an ID, external outcome, source, and meaningful risk.
2. **Acceptance example** — `given / when / then`, linked to one or more requirements.
3. **Verification** — an executable test or a named manual check, linked to the example.
4. **Evidence** — baseline/candidate result and CI run or equivalent record.
5. **Approval** — the named semantic owner and the record version they approved.

### OpenSpec mode

Use when OpenSpec is the team's source of truth. Write the requirement and `#### Scenario` once in the OpenSpec delta spec; do **not** copy their text into `assurance.yml`. The assurance record contains only semantic approval plus links from OpenSpec requirement/scenario references to verification and evidence.

Use stable human-readable references such as `ordering/idempotency#prevent-duplicate-order` and `repeated-order-request`, not Markdown line numbers. If headings are routinely renamed, establish stable IDs in the team's OpenSpec convention before relying on automated checks.

In either mode, render a diagram in a PR or documentation page from the structured record if useful. Do not maintain a separate hand-drawn matrix:

```text
[R-1: repeated request creates no second order]
                    │
                    ▼
[AT-1: repeat valid request with idempotency key]
                    │
                    ▼
[VT-1: integration test] ──► [CI run] ──► [acceptance decision]
```

## What “Sane ATDD” Means

An acceptance example is sufficiently sane for implementation only when all of these are true:

- **Outcome-oriented:** it states a user, customer, or operational result rather than an internal method, table, class, or mock interaction.
- **Falsifiable:** it says what must be observable after the action and can fail for a plausible wrong implementation.
- **Traceable:** it names the requirement(s) and authoritative source it elaborates.
- **Risk-aware:** it represents the relevant happy path, exception, boundary, state transition, or integration condition for the change's risk. It need not enumerate every edge case.
- **Owned:** a person accountable for product or domain meaning has approved it before implementation.
- **Stable during the run:** an implementation agent cannot silently change its semantic intent. A change requires a new approved assurance-record version and, in OpenSpec mode, a corresponding delta-spec amendment.

Ask one forcing question for every important example:

> Which plausible wrong solution should this scenario reject?

Put one or two answers in `rejects`. This is not a proof of test adequacy, but it prevents examples that merely narrate a happy path.

## Workflow

### Phase 1 — Classify the change

Use the lightest proportionate mode:

| Risk | Minimum assurance |
|---|---|
| Low | Observable `done_when`, ordinary test evidence, PR review |
| Medium | Approved canonical requirements/scenarios and assurance record before code; links to tests and CI after code |
| High | Medium controls plus independent test/semantic review, targeted challenge scenarios, and release or operational evidence where relevant |

Treat money movement, authorisation, personal data, public API, migrations, compliance rules, irreversible operations, and critical customer journeys as high risk unless a responsible owner explicitly classifies otherwise.

### Phase 2 — Draft the specification and assurance record before code

1. Choose `standalone` or `openspec` explicitly in the delegation contract and set both references.
2. In `standalone`, copy `acceptance-map.yml` to `.agent/acceptance/<TASK-ID>.yml`; write the requested **outcome**, not a proposed implementation.
3. In `openspec`, draft the change proposal and delta spec under `openspec/changes/<CHANGE>/`; copy `openspec-assurance.yml` beside them, copy the `openspec-verification-assurance.json` fragment into the delegation contract, and reference OpenSpec requirements/scenarios without duplicating their text.
4. Link every material acceptance example/scenario to an authoritative requirement source.
5. State scenarios in language a product or domain owner can read; in standalone mode use `given / when / then` directly, and in OpenSpec mode follow the team's OpenSpec scenario convention.
6. Add one or two `rejects` items for each material scenario in the assurance record.
7. Record uncertainties in `open_questions`; do not manufacture an answer from implementation details or untrusted issue text.
8. Keep the assurance record `draft`. The agent may draft it, but cannot approve it.

### Phase 3 — Semantic approval gate

Before the implementation agent changes production code, the semantic owner reviews the canonical requirements/scenarios and assurance record and chooses one outcome:

- **approved** — the examples represent intended behaviour sufficiently for this risk;
- **revise** — update requirement, scenarios, or scope and review the next approved version;
- **clarify** — stop implementation until the source of truth is resolved.

Approval answers:

> If the approved examples are implemented and verified, do we accept that the intended outcome has been achieved?

It is not a code review and should not be delegated to the implementation agent. For high-risk work, use a product/domain owner plus an independent quality or engineering reviewer.

### Phase 4 — Implement without moving the goalposts

1. Give the implementation agent the approved assurance record and applicable delegation contract.
2. The agent may write code and executable tests linked to approved examples/scenarios.
3. The agent must stop if an example/scenario is ambiguous, contradicted by a higher-priority source, or requires a semantic change.
4. Add a new assurance-record version for any accepted semantic amendment; in OpenSpec mode update the delta spec as well. Record the owner, date, and superseded version.
5. For changed behaviour, run the new verification on the base commit when practical. Record `fails` if it exposes the gap. Use `passes_existing_behaviour` or `not_applicable` only with a concise reason.

A test written after code can still be useful, but it cannot silently become the definition of acceptance. Link it to an already approved example, or route it as an amendment through Phase 3.

### Phase 5 — Verify and accept after code

The PR reviewer checks the assurance record from left to right:

1. Every approved material example/scenario links to an actual verification item.
2. Every material verification item names a test/manual procedure and CI/manual evidence.
3. Tests check an observable outcome rather than only an internal call, mock, or implementation detail.
4. The implementation did not change approved acceptance semantics without a new approval.
5. Required baseline/candidate results are recorded.
6. Open questions are resolved, accepted as explicit risk, or escalated.

The semantic owner accepts the intended outcome. Engineering/quality reviewers accept the strength and execution of evidence. One person may hold both roles in a small team, but the decisions should remain distinguishable.

## Lightweight Review Checklist

Use this in a PR description or review comment:

```text
Canonical spec: <canonical_spec_ref>
Assurance record: <assurance_record_ref> (mode: standalone|openspec; version N)

[ ] Each changed user-visible behaviour maps to an approved AT example.
[ ] Each AT example maps to a runnable test or named manual verification.
[ ] Examples describe outcomes, not implementation mechanics.
[ ] Each material example can reject at least one plausible wrong solution.
[ ] Test changes did not redefine acceptance semantics without approval.
[ ] CI/manual evidence is linked for every material verification.
[ ] Semantic owner: <name>; evidence reviewer: <name>.
```

## Trace and Provenance

The assurance record is the human-readable trace. Connect it to an agent delegation record where one exists:

```text
contract ID/version → canonical spec version → assurance-record version → agent run ID → PR/commits → test/CI evidence → human decision
```

Record only reviewable, necessary data. Good fields include task ID, map and contract versions, requirement sources, base/candidate commits, test command, CI URL, model/agent version if available, approvals, and open questions.

Do not store secrets, customer data, raw production logs, prompts containing sensitive material, or a model's hidden chain-of-thought. Tool calls and artifact references are more useful and safer audit evidence than an unbounded reasoning transcript.

## Escalation and Rework

| Observation | Action |
|---|---|
| Requirement and example conflict | Stop; semantic owner resolves the source of truth before code continues |
| Test needs an internal implementation detail to pass | Rewrite it around an observable outcome or label it as a lower-level test, not acceptance evidence |
| Agent proposes a new acceptance outcome after coding | Treat it as a specification and assurance-record amendment; obtain approval before using it for acceptance |
| A plausible incorrect implementation passes all examples/scenarios | Add a risk-based scenario, contract/property test, or challenge check; do not claim the assurance record was sufficient |
| Assurance record is repeatedly too large or ignored | Reduce it to material behaviours and automate the PR rendering/checks |
| Post-merge defect contradicts an approved example | Trace it to requirement, example, test, or execution evidence; update the template/policy and add a focused regression check |

## Common Pitfalls

1. **Mapping every unit test to a requirement.** Map material acceptance evidence, not every implementation detail. Lower-level tests support a verification item but need not each be a row.
2. **Duplicating OpenSpec scenarios in an Acceptance Map.** In `openspec` mode, OpenSpec owns requirement/scenario text; the assurance record owns approval, verification, and evidence links.
3. **Making the diagram the source of truth.** A manually edited picture drifts. Store structured links in YAML and render the diagram from it.
4. **Approving the tests only after code exists.** This allows implementation to shape acceptance intent. Approve semantics before coding; review evidence after coding.
5. **Treating `given / when / then` as quality by itself.** Gherkin grammar does not make an example outcome-oriented, complete, or falsifiable.
6. **Making baseline failure an absolute ritual.** New behaviour should normally fail on base, but existing behaviour, refactoring, and nondeterministic environments require an explicit exception.
7. **Using an LLM judge as the sole semantic owner.** An agent can challenge or summarize; accountable human judgment remains necessary for material behaviour.
8. **Turning risk controls into universal bureaucracy.** Use the assurance record for material behaviour changes; keep low-risk work light.

## Verification Checklist

- [ ] The delegation contract declares exactly one `spec_mode`, `canonical_spec_ref`, and `assurance_record_ref`.
- [ ] In `standalone`, the map is versioned under `.agent/acceptance/`; in `openspec`, the assurance record is stored with the OpenSpec change.
- [ ] The canonical requirements/scenarios and assurance record were approved before implementation for medium/high-risk work.
- [ ] Every material requirement has at least one approved acceptance example.
- [ ] Every approved example links to an executable test or named manual verification.
- [ ] Examples state observable outcomes and plausible rejected wrong solutions.
- [ ] Any semantic change has a new approved assurance-record version and, in OpenSpec mode, an updated delta spec.
- [ ] Candidate result and CI/manual evidence are recorded.
- [ ] PR/commits and applicable delegation contract link back to the assurance record.
- [ ] No sensitive prompts, secrets, or chain-of-thought content were added to the assurance record or evidence.
- [ ] Any post-merge learning is converted into a focused regression check or a policy/template improvement.

## References

- `templates/acceptance-map.yml` — standalone requirement-to-evidence source of truth.
- `templates/openspec-assurance.yml` — OpenSpec adapter; keeps scenario text in OpenSpec and evidence links beside the change.
- `templates/openspec-verification-assurance.json` — OpenSpec-mode `verification_assurance` object for a delegation contract.
- `agent-delegation-contract` — bound agent authority, scope, evidence, and escalation around the change.
