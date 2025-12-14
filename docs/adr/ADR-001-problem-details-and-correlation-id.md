# ADR-001: RFC7807 Problem Details с correlation_id

Дата: 2025-12-14
Статус: Accepted

## Context
- Требуется единый и безопасный формат ошибок (NFR-04 «Ошибки без PII») с трассировкой запросов (correlation_id) для угроз STRIDE R5 (Information Disclosure) и R7 (Repudiation).
- Тесты и разработчики нуждаются в стабильном контракте ошибок для e2e/контрактных проверок.

## Decision
- Использовать RFC7807 payload: `{type, title, status, detail, correlation_id}`.
- Генерировать/пробрасывать `X-Correlation-Id` (если пришёл от клиента — сохраняем).
- Обработчики ApiError, HTTPException, RequestValidationError всегда отвечают problem-details JSON и выставляют заголовок `X-Correlation-Id`.

## Alternatives
- Возвращать ad-hoc `{error:{code,message}}` — нет совместимости с tooling RFC7807 и хуже трассировка.
- Логировать только серверный trace-id — не помогает клиенту/QA коррелировать ошибки.

## Consequences
- (+) Предсказуемый контракт для тестов и SIEM.
- (+) Снижение риска утечек деталей (PII/stacktrace отсутствуют).
- (−) Небольшой оверхед на генерацию UUID.

## Links
- NFR-04, NFR-09; F3/F5; Risks R5/R7.
- Код: `app/main.py` (problem responses, middleware).
- Тесты: `tests/test_errors.py`, `tests/test_security_policies.py::test_correlation_id_is_propagated`.
