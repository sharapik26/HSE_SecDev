## Security NFR (P03)

| ID | Название | Описание | Метрика/Порог | Проверка (чем/где) | Компонент | Приоритет |
| --- | --- | --- | --- | --- | --- | --- |
| NFR-01 | Argon2id для паролей | Все пароли пользователей хэшируются Argon2id с параметрами t=3, m=256MB, p=1; соль ≥16 байт | Конфиг соответствует; unit-тест проверяет параметры | auth | High |
| NFR-02 | TTL и подпись JWT | Access-token TTL ≤ 30 минут, refresh TTL ≤ 14 дней; alg=RS256, aud=wish-service; clock skew ≤ 60с | Контрактный тест токена + проверка конфигурации CI | edge/auth | High |
| NFR-03 | Rate limiting мутаций | POST/PUT/DELETE на `/wishes` ограничены 60 req/min/IP; при превышении 429 без выполнения бизнес-логики | Нагрузочный тест (k6) ожидает ≥95% лишних запросов с 429 | api gateway | High |
| NFR-04 | Ошибки без PII | 100% ошибок в формате `{error.code,message}` без PII и без трейсбеков; заголовок `X-Correlation-Id` установлен | Контрактные тесты API + e2e smoke на stage | api | Medium |
| NFR-05 | Валидация входных данных | Все тела запросов соответствуют схеме (id:int, name 1..100); недопустимые данные всегда 422 | Contract + fuzz-тесты подтверждают 0 пропусков/0 ложных срабатываний | api | Medium |
| NFR-06 | Устранение уязвимостей зависимостей | High/Critical из SCA отчёта устраняются ≤ 7 дней с обнаружения; build падает при нарушении | CI SCA (pip-audit) с policy; отчёт хранится 90 дней | build | High |
| NFR-07 | Гигиена секретов | В репозитории нет секретов; ≥99% паттернов ключей детектируется; при обнаружении push блокируется | pre-commit + CI secret-scan (gitleaks) с fail on leak | platform | High |
| NFR-08 | TLS/Headers hardening | Только TLS 1.2+; HSTS `max-age ≥ 31536000`, `includeSubDomains`; запрещён mixed-content | Ночной compliance-скан (sslyze/zap) фиксирует соответствие | edge | Medium |
| NFR-09 | Аудит мутаций | 100% операций create/update/delete по `/wishes` логируются в audit-stream с `correlation_id`; ретенция ≥90 дней | Интеграционный тест + спотовая проверка логов | observability | Medium |

Дополнительно: NFR-01/02/03/06/07 являются блокирующими для выхода в прод (gate в CI/CD); остальные обязательны к закрытию до релиза M3.
