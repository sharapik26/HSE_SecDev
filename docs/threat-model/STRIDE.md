## STRIDE — Wishlist Service (P04)

| Поток/Элемент | Угроза (STRIDE) | Риск ID | Контроль | Ссылка на NFR | Проверка/Артефакт |
| --- | --- | --- | --- | --- | --- |
| F1 HTTPS клиент → gateway | Spoofing/Man-in-the-Middle | R1 | TLS1.2+, HSTS на edge | NFR-08 | SSLyze/ZAP baseline |
| F2 Gateway ↔ Auth (JWT) | Replay/подмена токена (Tampering/Spoofing) | R2 | TTL 30m/14d, RS256, audience check | NFR-02 | Контрактный тест токена |
| F3 Gateway → API (/wishes) | DoS/Resource Exhaustion | R3 | Rate limit 60 rpm/IP с 429 | NFR-03 | k6 нагрузочный тест |
| F3 Gateway → API (/wishes) | Tampering/Injection | R4 | Схемы валидации body (id int, name 1..100) | NFR-05 | Contract + fuzz-тесты |
| F3 Gateway → API (/wishes) | Information Disclosure | R5 | Маскирование ошибок, без PII, correlation_id | NFR-04 | Контрактные тесты ошибок |
| F4 API → DB | Tampering (неавторизованные изменения) | R6 | Логирование 100% мутаций в audit stream | NFR-09 | Интеграционный тест + выборка логов |
| F5 Audit stream | Repudiation | R7 | Корреляция по correlation_id, ретенция ≥90 дней | NFR-09 | Проверка наличия события по ID |
| F7 Dev → CI (git push) | Disclosure/Secrets leakage | R8 | Secret scanning, блокировка push | NFR-07 | gitleaks/pre-commit лог |
| F8 CI → Registry (image) | Tampering/Supply chain (CVE) | R9 | SCA gate, High/Critical ≤7 дней, fail build | NFR-06 | pip-audit отчёт в CI |
| F9 Registry → Runtime | Elevation via уязвимый образ | R10 | Использовать только прошедшие SCA образы | NFR-06 | Политика deploy: допускаются образы с passed SCA |
