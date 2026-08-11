# maratkee-skills

Public, reusable agent skills maintained by Marat Kiniabulatov.

## Skills

### `weekly-ai-management-digest`

Produces a weekly evidence-led digest about how AI changes engineering management. It includes:

- a seven-day novelty gate for every main theme;
- a 60-day window for ordinary supporting evidence;
- a 180-day exception for qualified major research;
- claim-level evidence ratings based on the full evidence base, not the anchor source;
- a separate method-maturity audit for narrowly relevant foundational studies and historical backtests;
- checks for follow-ups, corrections, revised versions, and superseded findings;
- a machine-readable source register;
- a standard-library Python freshness validator;
- an independent freshness-critic step;
- publication-day revalidation.

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
