# Claim-level evidence rating

Use this protocol before assigning the 3-dot credibility badge to a thematic section.

## Core principle

Rate the **claims in the section against their full evidence base**, not the prestige or type of the newest/anchor source. A vendor guide can describe a method with independent validation elsewhere; conversely, a reputable report may not support the section's strongest causal claim.

## Two-axis rule: freshness versus maturity

Never collapse these into one score:

1. **Freshness eligibility asks why this theme belongs in this week's issue.** Enforce the 7/60/180 windows through the source register and freshness validator.
2. **Claim maturity asks what the underlying method or phenomenon has actually validated over time.** Search older peer-reviewed studies, replications, calibration exercises, field backtests, and critiques in addition to fresh sources.

Older foundational evidence belongs in `sources/foundation-audit.md`, not in the freshness validator or 50/50 balance. It may establish historical validation of a stable method, with an explicit `foundational` label and a supersession check. It may not make a stale theme current, support a present-day performance number, or conceal the absence of fresh corroboration.

A section passes only when both axes are honest: a valid weekly signal exists, and the central claim is rated against the full maturity audit without exceeding the scope of fresh evidence.

## Required steps

1. **Atomize the section.** List each externally checkable claim separately: method validity, empirical accuracy, scale/generalizability, causal mechanism, implementation claim, and illustrative numbers.
2. **Map every claim to evidence.** Record which source supports it, whether the source is primary or secondary, and whether the wording is direct evidence, inference, or illustration.
3. **Search the full evidence base.** For the core method or phenomenon, look for peer-reviewed studies, independent backtests, replications, field telemetry, and methodological critiques—not only the weekly trigger article.
4. **Compare wording with source scope.** Read assumptions, exclusions, limitations, and definitions. Flag any sentence that adds scale, dependencies, causality, accuracy, or generality absent from the source.
5. **Separate levels of support.** Distinguish:
   - mathematical/logical validity;
   - empirical validation in a narrow setting;
   - generalization across teams/companies;
   - implementation-specific performance.
6. **Rate the section by its central claim.** Do not average unrelated claims. If a strong generic method claim and a weak implementation claim coexist, split the section, narrow the wording, or explain the mixed evidence in the tooltip.
7. **Downgrade or rewrite overclaims.** A low badge does not repair unsupported prose. Correct the prose first, then rate the corrected section.
8. **Mark examples as examples.** Invented ranges, percentiles, costs, or scenarios must say «например» / «иллюстрация», never resemble measured results.

## Rating guidance

- **🟢🟢🟢 High:** multiple large independent studies, strong transparent methodology, or robust replicated evidence directly supporting the central claim. Mathematical identities may be high conditionally, but state the conditions.
- **🟡🟡⚪ Medium:** one peer-reviewed exploratory study plus credible field backtests; independent telemetry; several convergent cases; or a sound method whose generalizability is not yet established.
- **🔴⚪⚪ Low:** single practitioner/vendor source, toy examples, opinion, or an implementation claim without independent calibration.

A section can legitimately say: «The underlying method has medium evidence; this specific multi-team implementation has low evidence.»

## Assumption and contradiction audit

For each source, extract explicit phrases equivalent to:
- “we assume…”
- “we do not cover…”
- “not independently validated…”
- “best case / ceiling…”
- “results may not generalize…”

Then compare them against every sentence in the draft. A direct contradiction is a blocking error.

## Worked pattern: probabilistic software forecasting

Do not treat “Monte Carlo forecasting” as one indivisible claim:

- The mathematics of sampling and combining **independent** probabilities can be strong, conditional evidence.
- Single-team throughput-based forecasting may have medium empirical support from peer-reviewed exploratory work and field backtests spanning multiple teams.
- A particular portfolio or multi-team implementation can remain low/medium if it lacks independent calibration or assumes away shared people, handoffs, Feature WIP, or dependencies.

Therefore, never label the whole method low solely because the weekly anchor is a vendor guide. Equally, never claim that a guide models dependencies if it explicitly excludes them.

## Tooltip template

> **Средняя.** Базовый метод подтверждён [types and scale of evidence]. Конкретное расширение на [setting] пока опирается на [limited evidence] и предполагает [key assumptions].

## Pre-publish questions

- Is the badge rating the source, or the claim?
- Did we inspect the complete evidence base for the central method?
- Does any sentence claim more than the cited source tested?
- Are conditional assumptions visible to the reader?
- Are illustrative figures clearly labelled?
- Would splitting the section produce a more honest rating?
