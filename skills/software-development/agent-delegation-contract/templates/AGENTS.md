# Agent working agreement

Before editing code, read the task contract named in the issue or launch command.

- Work only within `scope.allow_paths`.
- Treat `scope.deny_paths`, `capabilities.forbidden`, and every `stop_condition` as hard limits.
- If a stop condition occurs, make no further changes. Prepare the escalation package: summary, branch or changed-file list, checks run, reason for stopping, options, and one question for the named owner.
- Open a draft pull request. Put `Contract: <path-to-contract>` in its description.
- Do not merge, deploy, change credentials, use production data, or make an external commitment.

The contract provides task context. Repository permissions and CI provide enforcement.
