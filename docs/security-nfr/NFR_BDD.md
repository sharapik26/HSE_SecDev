Feature: Rate limiting mutate endpoints
  Scenario: Bursts above 60 rpm are throttled
    Given сервис развернут на stage с лимитом 60 req/min/IP на POST /wishes
    When клиент отправляет 70 запросов POST /wishes за 60 секунд
    Then не менее 10 ответов имеют статус 429
    And не более 60 записей появляется в списке желаний
    And тело ошибки соответствует формату {"error": {"code": "rate_limited", "message": "..."}}

Feature: Error envelope without PII
  Scenario: Invalid wish returns sanitized error
    Given тело запроса с name длиной 120 символов
    When отправлен POST /wishes
    Then ответ имеет статус 422
    And тело ошибки содержит только code "validation_error" и message без stacktrace
    And тело не содержит совпадений с шаблонами email или номера телефона

Feature: Dependency vulnerability gate
  Scenario: CI fails on High CVE older than 7 days
    Given отчёт SCA содержит High или Critical CVE старше 7 дней
    When выполняется SCA job в CI
    Then пайплайн завершается статусом failure
    And отчёт указывает CVE ID и время обнаружения для triage

Feature: Secret scanning on push
  Scenario: Push blocked when AWS-like key is committed
    Given commit содержит строку, совпадающую с паттерном AWS_ACCESS_KEY_ID и SECRET_ACCESS_KEY
    When запускается секрет-сканер в pre-push или CI
    Then пайплайн завершается failure
    And лог сканера указывает файл и строку обнаруженного секрета
