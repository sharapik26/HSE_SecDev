## Трассировка NFR ↔ Stories/Tasks

| NFR ID | Story/Task (Issue) | Приоритет | Release/Milestone |
| --- | --- | --- | --- |
| NFR-01 | AUTH-01: Регистрация + Argon2id (Issue #12) | High | Sprint 3 (M3) |
| NFR-02 | AUTH-04: JWT TTL/refresh и key-rotation (Issue #15) | High | Sprint 3 (M3) |
| NFR-03 | API-07: Rate limiting для POST/PUT/DELETE `/wishes` (Issue #17) | High | Sprint 2 (M2) |
| NFR-04 | API-05: Единый error envelope + correlation_id (Issue #11) | Medium | Sprint 2 (M2) |
| NFR-05 | API-06: Жёсткая схема валидации /wishes (Issue #10) | Medium | Sprint 2 (M2) |
| NFR-06 | OPS-02: CI SCA gate (pip-audit) (Issue #9) | High | Sprint 1 (M1) |
| NFR-07 | OPS-03: Secret scanning + policy (gitleaks) (Issue #8) | High | Sprint 1 (M1) |
| NFR-08 | EDGE-01: TLS/HSTS hardening фронта/API (Issue #13) | Medium | Sprint 3 (M3) |
| NFR-09 | OBS-01: Audit log shipping в SIEM (Issue #18) | Medium | Sprint 4 (M4) |

Примечание: номера Issue отсылают к бэклогу проекта (GitHub Issues/Project). Milestone-ы M1–M4 соответствуют релизным окнам курса; High помечены как блокирующие выход в прод.