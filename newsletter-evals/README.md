# Newsletter evals

Regression harness for the real `weekly-ai-management-digest` Hermes skill.

## What is evaluated

- `cases/` — versioned golden cases. Add a case before changing the skill when the change fixes a real failure mode.
- `providers/hermes-newsletter.cjs` — Promptfoo provider that invokes `hermes --skills weekly-ai-management-digest`; it does not maintain a second copy of the newsletter prompt.
- `promptfooconfig.yaml` — matrix configuration and the private self-hosted UI target.

The first two contracts test distinct editorial objects:

1. **Flow:** local AI acceleration vs the full path of a task through review, environment, decision, release, and outcome.
2. **Agent governance:** delegation contract — authority boundaries, evidence, escalation, and risk ownership.

The assertions are intentionally deterministic and shallow. They catch structural regressions only. Human review in Promptfoo is the authority for editorial quality until judge rubrics are calibrated against Marat's scores.

## Run an eval

```bash
./run-eval.sh
```

The runner calls the installed Hermes CLI, then uploads results to the self-hosted Promptfoo UI on `127.0.0.1:3000`.

## Open the private UI

The service is **not public**. From a machine with SSH access to Hermes:

```bash
ssh -N -L 3000:127.0.0.1:3000 root@46.16.34.153
```

Then open `http://127.0.0.1:3000` in a browser. Stop the tunnel with `Ctrl+C`.

## Operations

Runtime data is deliberately outside Git:

- project: `/root/maratkee-skills/newsletter-evals/`
- persisted Promptfoo SQLite/blobs: `/root/.local/share/promptfoo-newsletter/`
- Docker container: `promptfoo-newsletter`, bound only to `127.0.0.1:3000`

Useful commands:

```bash
docker logs --tail 100 promptfoo-newsletter
docker restart promptfoo-newsletter
docker stop promptfoo-newsletter
docker start promptfoo-newsletter
```

The Docker image is currently pinned in `docker-compose.yml` to the digest that was verified at installation. One replica only: Promptfoo self-hosting uses SQLite and an in-memory job queue.

## Before changing the skill

1. Run `./run-eval.sh` on the current branch and preserve the Promptfoo URL / run ID.
2. Make the proposed `SKILL.md` change.
3. Run the same cases again.
4. Review output side-by-side. A higher average score does not override an evidence, safety, or Russian-voice regression.
5. Add a focused golden case if the change fixed a previously uncovered failure.

## Next increment

Add three calibrated LLM-judge rubrics (evidence, management object/action, editorial voice) only after Marat has manually scored a small set of outputs. That avoids automating a judge that merely rewards generic consulting prose.
