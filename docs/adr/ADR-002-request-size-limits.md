# ADR-002: Лимит размера запроса

Дата: 2025-12-14
Статус: Accepted

## Context
- В Threat Model (F1/F3, Risk R3) риск DoS/Resource Exhaustion на POST /wishes и другие POST.
- Нужен простой контроль до бизнес-логики, привязанный к NFR-03 (rate/limits) и NFR-04 (ошибки без PII).

## Decision
- Вводим middleware, который проверяет `Content-Length` и отклоняет запросы > `MAX_CONTENT_LENGTH` (по умолчанию 1 MiB) с ответом 413 RFC7807.
- Лимит конфигурируется через env `MAX_CONTENT_LENGTH`.

## Alternatives
- K8s/Ingress body-size limit — зависит от окружения, нет unit-тестов в репозитории.
- Чтение тела и измерение факта размера — дороже по памяти/CPU.

## Consequences
- (+) Быстрая защита от больших тел до выполнения обработчика.
- (+) Простая конфигурация и unit-тестируемость.
- (−) Требуется корректный `Content-Length`; для chunked может не сработать (приемлемо для текущего сервиса).

## Links
- NFR-03; F1/F3; Risk R3 (DoS).
- Код: `app/main.py` (middleware, 413 problem).
- Тест: `tests/test_security_policies.py::test_payload_too_large`.
