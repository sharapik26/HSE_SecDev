# P11 - DAST (ZAP baseline) Summary

## Target
- URL: `http://localhost:8000/`
- Health endpoint: `/health`

## Reports
- `EVIDENCE/P11/zap_baseline.html` — HTML отчёт
- `EVIDENCE/P11/zap_baseline.json` — JSON отчёт

## Workflow
- Файл: `.github/workflows/ci-p11-dast.yml`
- Триггеры: `workflow_dispatch`, push в `app/**`, `src/**`
- Образ: `ghcr.io/zaproxy/zaproxy:stable`
- Автоматический коммит отчётов после генерации

## Configuration
- Spider duration: 5 minutes (`-m 5`)
- Ignore informational warnings (`-I`)
- Debug mode enabled (`-d`)

## Results
После запуска workflow отчёты будут автоматически добавлены в репозиторий.

## Plan
- [ ] Проанализировать findings после получения отчётов
- [ ] Исправить критические проблемы (если есть)
- [ ] Задокументировать принятые риски / FP (если актуально)

