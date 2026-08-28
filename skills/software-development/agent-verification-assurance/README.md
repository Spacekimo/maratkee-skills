# Semantic Acceptance Assurance

## Проблема

Агент может написать зелёный acceptance test для собственной догадки о правиле, реализовать её и оставить людям разбирать PR: что он понял, почему именно так и проверяет ли тест нужное поведение.

Этот skill не притворяется, что заменяет отсутствующего системного аналитика. Он делает неизвестное и выбор трактовки видимыми до production-кода.

## Архитектура

```text
Delegation Contract
        │ scope, owners, stop conditions
        ▼
Semantic Decision Map
        │ facts, alternatives, unknowns, decision question
        ▼
Human semantic decision
        │ approved | revise | clarify | accept_risk
        ▼
Approved Acceptance Map / OpenSpec scenario
        │ expected outcome + rejected wrong outcomes
        ▼
Test → implementation → CI evidence → independent review
```

## Шаги

1. **Discover:** агент собирает только разрешённые факты из кода, тестов, Git и утверждённых документов.
2. **Separate:** фиксирует evidence, выбранную трактовку, альтернативы и неизвестное в Semantic Decision Map.
3. **Decide:** именованный человек подтверждает трактовку, просит доработать, останавливает работу или явно принимает риск.
4. **Scope:** для standalone в контракт добавляются точные пути Acceptance Map и Decision Map; для OpenSpec — только конкретная директория change и Decision Map.
5. **Test:** после решения агент пишет acceptance test; characterization tests текущего поведения не выдаются за целевую семантику.
6. **Implement:** фиксирует baseline (`gap_demonstrated`, `new_capability`, `existing_behavior_change`, `not_practical`), затем выполняет TDD.
7. **Review:** для high-risk — отдельный именованный reviewer проверяет цепочку «решение → сценарий → тест → наблюдаемое поведение → CI»; для medium-risk semantic и evidence решения фиксируются раздельно.

## Quality gates

- **G1 Evidence:** факты имеют ссылку и версию; агент не добывает недоступные данные.
- **G2 Semantics:** без решения named human owner нельзя менять production code для medium/high-risk задачи.
- **G3 Test meaning:** каждый сценарий проверяет outcome и указывает, какие неверные решения он отсекает.
- **G4 Baseline:** тип исходной ситуации зафиксирован; stub/bypass не считается доказательством дефекта.
- **G5 Evidence review:** зелёный CI не принимается без независимой проверки всей цепочки.

## Артефакты

- `templates/semantic-decision-map.yml` — краткая карта фактов и решения.
- `templates/acceptance-map.yml` — standalone сценарии, тесты и evidence.
- `templates/openspec-assurance.yml` — адаптер для OpenSpec.
- `templates/openspec-verification-assurance.json` — фрагмент `verification_assurance` контракта для OpenSpec.
- `agent-delegation-contract` — границы доступа, owner и escalation.

Для low-risk задач не создавайте лишнюю бюрократию: достаточно обычного contract, теста и PR review. Полный workflow нужен, когда неправильная трактовка правила дороже нескольких минут дополнительного согласования.
