# maratkee-skills

Public, reusable agent skills maintained by Marat Kiniabulatov.

## Skills

### `weekly-ai-management-digest`

Produces a weekly evidence-led digest about how AI changes engineering management. Three independent source layers (curated feeds, extended web research, deep research API) with defined fallbacks. Freshness gates (7/60/180 days), claim-level evidence ratings, supersession checks, independent freshness critic, and publication-day revalidation.

### `extended-research`

Multi-source research pipeline: dimensions → threads → search → relevance filter → deep reading → gap analysis → drill-down → synthesis. Includes optional deep research API mode and interactive source review for editorial workflows. Freshness gates and citation compliance for time-bounded research.

## Install

Add this repository as a Hermes skill source:

```bash
hermes skills tap add Spacekimo/maratkee-skills
```

Then browse or install the skill through Hermes:

```bash
hermes skills browse
hermes skills install weekly-ai-management-digest
```

Alternatively, clone the repository and copy the skill directory into your Hermes skills directory.

## Validate a source register

```bash
python skills/productivity/weekly-ai-management-digest/scripts/freshness-check.py \
  path/to/source-register.json

python skills/productivity/weekly-ai-management-digest/scripts/freshness-check.py \
  path/to/source-register.json --publication
```

Start from:

`skills/productivity/weekly-ai-management-digest/templates/source-register.json`

## Tests

```bash
python -m unittest discover -s tests -v
```

## License

MIT
