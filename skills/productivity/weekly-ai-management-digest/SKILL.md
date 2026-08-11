---
name: weekly-ai-management-digest
description: Use when producing a weekly evidence-led newsletter about how AI changes engineering management, team structures, delivery, cost, roles, governance, and operating models. Enforces a 7-day novelty window, 60-day evidence window, 180-day major-research exception, supersession checks, an independent freshness critic, and publication-day revalidation.
version: 2.6.0
author: Marat Kiniabulatov
license: MIT
metadata:
  hermes:
    tags: [digest, newsletter, ai-adoption, management, research, freshness, weekly]
    related_skills: []
---

# Weekly AI Management Digest

## Overview

This skill produces a weekly evidence-led digest about how AI changes engineering management: team structures, delivery systems, cost, roles, quality controls, governance, and operating models.

The digest starts with what substantively changed during the last seven days. Supporting evidence must remain current enough for a fast-moving AI landscape. Fresh publication dates cannot disguise old datasets or superseded findings.

Before every issue, read `references/source-freshness-gate.md` and validate the source register with `scripts/freshness-check.py`.

## When to Use

Use this skill for:

- a weekly AI-management newsletter or digest;
- a weekly scan of new AI engineering-management research;
- evidence-led synthesis of newsletters and primary research;
- checking whether previous findings have been updated or superseded.

Do not use it for:

- general daily news briefs;
- tool comparisons without management implications;
- historical literature reviews;
- timeless background explainers;
- research where the user explicitly requests a different date window.

## Editorial Scope

Keep these themes in focus:

- engineering-team structures and role boundaries;
- flow metrics, bottleneck migration, and review load;
- AI adoption versus delivery outcomes;
- delivery cost, token economics, rework, and hidden overhead;
- human responsibility, verification, and quality controls;
- change management, resistance, governance, and guardrails;
- agentic engineering, observability, evaluations, and loop design;
- business outcomes beyond usage and activity metrics.

The central question is: **what does this change mean for a leader responsible for delivery flow and outcomes?**

## Freshness Contract: 7 / 60 / 180

The digest uses three independent clocks.

### 1. Weekly signal — 7 days

Every main theme must have a substantive event inside the seven days before `window_end`:

- new research, report, dataset, or measured result;
- follow-up or revised estimate;
- methodological update that changes interpretation;
- correction, erratum, or retraction;
- updated conclusion based on new analysis.

A newly published article that only retells older evidence does not qualify.

### 2. Supporting evidence — 60 days

Ordinary studies, surveys, telemetry, industry reports, cases, and practitioner analyses must have an `evidence_date` no more than 60 days old.

### 3. Major research — 180 days

The 180-day exception is reserved for transparent, substantial research such as randomized or longitudinal studies, systematic reviews, large independent surveys, major datasets, and recurring reports with stable methodology.

Vendor blogs, consultancy estimates, single-company cases, and small convenience surveys do not qualify.

### Evidence date beats article date

Record separately:

- original publication date;
- substantive update date;
- weekly event date;
- latest date represented by the underlying data or experiment.

Use the underlying evidence date for the 60/180-day gate. A fresh article cannot launder old evidence into the current window.

### No stale padding

Evidence outside the allowed windows is excluded from:

- the evidence base;
- the reading list;
- credibility ratings;
- source-balance calculations.

If fresh corroboration is unavailable, label the item an **early signal** and lower its evidence rating.

## Pipeline

## Phase 1 — Define the issue window

1. Set `window_end` in the editorial timezone.
2. Derive `weekly_start = window_end - 7 days`.
3. Write both timestamps at the top of every source artifact.
4. Start from `templates/source-register.json`.

The issue window is always the preceding seven days. A skipped or delayed previous issue does not expand the novelty window.

## Phase 2 — Discover weekly events

Scan two source layers in parallel:

### Newsletter and industry layer

Search trusted newsletters, research blogs, engineering-management publications, official company research feeds, and relevant RSS sources.

Newsletters are discovery mechanisms. Follow every claim to its canonical primary source before accepting it.

### Research layer

Search official research indexes, academic databases, arXiv, Crossref, Semantic Scholar, organization report archives, and primary datasets.

Search specifically for:

- new findings from the last seven days;
- updates to previously used studies;
- follow-ups and changed conclusions;
- corrections, revised methodology, and version history;
- contradictions that could change the editorial thesis.

## Phase 3 — Verify each candidate

For every candidate:

1. Open the canonical primary source.
2. Verify the exact publication date on the source page.
3. Identify the date of the underlying evidence or dataset.
4. Describe what changed this week in one concrete sentence.
5. Record methodology, sample size, and evidence limitations.
6. Classify the source as `weekly_signal`, `supporting`, or `major_research`.
7. Run the supersession search from `references/source-freshness-gate.md`.
8. Record the search query, check time, and any newer version.

## Phase 4 — Validate freshness

Run:

```bash
python scripts/freshness-check.py sources/source-register.json
```

Any error blocks drafting. Fix the register, replace the source, or remove the claim. Never waive a stale date silently.

The register must contain at least one valid `weekly_signal`. Each main theme in the final issue must map to a weekly signal, even when the theme also uses recent supporting or major research.

## Phase 5 — Independent freshness critic

Give a separate reviewer only the claims and source register. Ask it to disqualify:

- stale underlying evidence;
- fresh articles that summarize old data;
- missing or ambiguous dates;
- superseded versions;
- secondary coverage presented as primary evidence;
- cosmetic updates presented as new findings;
- headline claims stronger than results;
- metric sign, denominator, or confidence-interval errors.

Save the review as `sources/freshness-critic.md`. Resolve every rejection before synthesis.

## Phase 6 — Synthesize

Cluster accepted sources into three to five themes. Each theme needs:

- the substantive weekly change;
- current supporting evidence;
- contradictions or uncertainty;
- a practical management implication;
- an evidence-strength rating.

Organize by themes, not by source type. Newsletter discoveries and research findings should read as one coherent narrative.

A useful source-mix target is roughly half newsletter/industry discovery and half research, measured by the origins of substantive claims. The ratio is a diagnostic, not a visible section structure.

## Phase 7 — Publication-day recheck

Within 24–48 hours of publication:

1. Repeat the supersession search for every cited source.
2. Search for new results published since the initial research pass.
3. Update `supersession_checked_at` and any changed claims.
4. Set `publication_recheck_completed: true`.
5. Run:

```bash
python scripts/freshness-check.py sources/source-register.json --publication
```

Publication is blocked when the validator exits non-zero or the freshness critic has unresolved objections.

## Recommended Output Artifacts

```text
issue/
├── sources/
│   ├── 01-newsletters.md
│   ├── 02-extended-research.md
│   ├── 03-deep-research.md
│   ├── source-register.json
│   ├── freshness-critic.md
│   └── contradictions.md
├── weekly-digest.md
└── weekly-digest-social.md
```

## Evidence and Writing Rules

- Link to primary sources whenever available.
- State exact dates, sample sizes, and measurement scope.
- Label estimates and vendor telemetry honestly.
- Preserve uncertainty, confidence intervals, and metric definitions.
- Explain technical terms inline.
- Keep one main claim per section.
- Use self-explanatory headings.
- Separate local task acceleration from end-to-end delivery impact.
- Reconcile percentages, denominators, and cost scopes.
- Never fabricate first-person anecdotes.
- Avoid presenting adoption activity as evidence of business impact.

## Common Pitfalls

1. **Using article publication date as evidence date.** Record the dataset or experiment date separately.
2. **Treating a newsletter as the primary source.** Follow the link to the canonical report.
3. **Expanding the weekly window after a skipped issue.** Weekly novelty remains seven days.
4. **Keeping a famous older study as background.** Remove it when it exceeds the evidence window.
5. **Calling a source major because the publisher is famous.** Qualification depends on methodology and coverage.
6. **Searching for updates only once.** Repeat the check on publication day.
7. **Mistaking a negative metric value for improvement.** Preserve the source's sign convention and interpretation.
8. **Padding a weak signal with stale evidence.** Label it early and lower the evidence rating.
9. **Letting a secondary article borrow authority from an old primary study.** Evaluate the underlying evidence date.
10. **Drafting before validation.** The source register and freshness critic are preconditions.

## Verification Checklist

- [ ] `window_end` includes the editorial timezone.
- [ ] Every main theme maps to a substantive event from the last seven days.
- [ ] Every ordinary supporting source is no more than 60 days old.
- [ ] Every major-research exception is no more than 180 days old and methodologically qualified.
- [ ] Publication, update, event, and evidence dates are recorded separately.
- [ ] Canonical primary URLs are used where available.
- [ ] Every source has a supersession search query and check timestamp.
- [ ] No known superseded source remains in the evidence base.
- [ ] The freshness validator passes before synthesis.
- [ ] The independent freshness critic has no unresolved rejection.
- [ ] The publication-day 24–48 hour search is complete.
- [ ] The validator passes with `--publication` before release.

## References

- `references/source-freshness-gate.md` — full freshness and supersession policy.
- `templates/source-register.json` — machine-readable source register template.
- `scripts/freshness-check.py` — standard-library validator for the 7/60/180-day gates.
