# Source Freshness Gate for Human Loop Weekly

## Purpose

Freshness is part of evidence quality. The digest tracks three clocks independently:

- **7 days:** what substantively changed this week;
- **60 days:** ordinary supporting evidence;
- **180 days:** a narrow exception for major research.

A source can be newly published and still contain stale evidence. Record the page date, event date, and underlying evidence/data date separately.

## Roles and hard windows

### `weekly_signal` — 7-day novelty gate

Every main digest theme needs at least one `weekly_signal` whose `event_at` falls within the seven days before `window_end`.

Qualifying events:

- new study, report, dataset, or measured result;
- new methodological note that changes interpretation;
- follow-up or revised estimate;
- correction or retraction;
- updated conclusion supported by new analysis.

Non-qualifying events:

- a new article that only summarizes old evidence;
- a newsletter resending or commenting on an older report;
- a cosmetic page update;
- a vendor announcement without new measured evidence;
- a social post linking to an older source.

`change_summary` must state what changed this week in one concrete sentence.

### `supporting` — 60-day evidence gate

Ordinary studies, surveys, telemetry, industry reports, cases, and practitioner analyses must have `evidence_date` no more than 60 days before `window_end`.

Use the date of the underlying evidence, not the date of the article that cites it. If a report published today analyzes a dataset frozen nine months ago, record the dataset cutoff as `evidence_date`.

### `major_research` — 180-day exception

The exception requires all of the following:

- `is_major: true`;
- transparent methodology;
- meaningful sample size or broad dataset coverage;
- one of: randomized study, longitudinal study, systematic review, large independent survey, major multi-organization dataset, or recurring report with stable methodology;
- `evidence_date` no more than 180 days old.

Vendor blogs, consultancy estimates, single-company cases, opinion pieces, and small convenience surveys do not qualify regardless of brand recognition.

## No stale background padding

Sources outside the windows are excluded from the evidence base, reading list, evidence scale, and 50/50 source calculation. If no fresh corroboration exists, label the item an **early signal** and lower its evidence rating.

An older result may appear only as a historical value explicitly reproduced and compared inside an in-window primary source. Cite the current source; do not restore the older study as independent evidence.

## Supersession check

Run this check for every candidate twice: during source collection and again within 48 hours of publication.

Search patterns:

1. exact title + `update OR follow-up OR revised OR correction OR erratum OR retraction`;
2. `site:<official-domain> <topic> update`;
3. author or research group + topic + current year;
4. DOI, Crossref, Semantic Scholar, arXiv, or publisher version history when applicable;
5. official research/report index sorted by newest;
6. page metadata, changelog, and links labeled update, methodology, appendix, or correction.

Record:

- `supersession_checked_at`;
- `supersession_query`;
- `superseded_by` when a newer version exists;
- exact effect on the claim.

If `superseded_by` is populated, the old source fails the gate until the source register and claim are rebuilt around the newer version.

## Freshness critic

Before drafting, give a separate reviewer only the claims and source register. Ask it to disqualify sources for:

- stale underlying data;
- article date laundering old evidence;
- missing or ambiguous dates;
- year-only labels;
- superseded versions;
- secondary coverage presented as primary evidence;
- update pages that do not actually change the evidence;
- headline claims stronger than the reported uncertainty;
- metric sign or denominator misinterpretation.

Save the result as `sources/freshness-critic.md`. Every rejection must be resolved or the source removed.

## Weekly workflow

1. Set `window_end` in the editorial timezone and derive `weekly_start = window_end - 7 days`.
2. Discover substantive events inside the weekly window.
3. Open the canonical primary source and determine `published_at`, `updated_at`, `event_at`, and `evidence_date`.
4. Run the supersession check.
5. Classify each source as `weekly_signal`, `supporting`, or `major_research`.
6. Validate the source register with `scripts/freshness-check.py`.
7. Run the independent freshness critic.
8. Draft only after all hard errors are resolved.
9. On publication day, repeat the 24–48 hour supersession search, update timestamps, and rerun the validator.

## Source-register semantics

- `published_at`: original page/report publication date.
- `updated_at`: latest substantive update date; null when none.
- `event_at`: date of the specific event that makes a source relevant this week.
- `evidence_date`: latest date represented by the underlying data or experiment.
- `change_type`: `new_research`, `new_dataset`, `new_result`, `follow_up`, `methodology_update`, `correction`, `revised_conclusion`, or `article_publication`.
- `change_summary`: concrete description of what changed.
- `is_primary`: whether this URL is the canonical origin of the evidence.
- `is_major`: whether it qualifies for the 180-day exception.

## Publish gate

Publication is blocked when:

- any main theme lacks a valid weekly signal;
- an ordinary source exceeds 60 days;
- a major source exceeds 180 days or lacks major-methodology evidence;
- a source lacks an evidence date;
- the supersession check is older than 48 hours;
- a newer version is known and not incorporated;
- the freshness critic has unresolved rejections;
- the final validator exits non-zero.
