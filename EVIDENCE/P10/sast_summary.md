# P10 - SAST & Secrets Summary

## Настройка

### SAST (Semgrep)
- **Профиль**: `p/ci` (базовые проверки для CI)
- **Кастомные правила**: `security/semgrep/rules.yml`
  - Проверка на небезопасный вывод в HTMLResponse
  - Проверка на захардкоженные секреты (password, api_key, secret)
  - Проверка на использование небезопасного random для криптографии
- **Формат отчёта**: SARIF
- **Расположение**: `EVIDENCE/P10/semgrep.sarif`

### Secrets Scanning (Gitleaks)
- **Конфигурация**: `security/.gitleaks.toml`
- **Allowlist**: 
  - Пути: `EVIDENCE/`, `tests/`
  - Регулярные выражения: `TEST_SECRET_DO_NOT_USE`, `example.*key`, `demo.*password`
- **Формат отчёта**: JSON
- **Расположение**: `EVIDENCE/P10/gitleaks.json`

## Workflow

Workflow `ci-sast-secrets.yml` запускается:
- При ручном запуске (`workflow_dispatch`)
- При push изменений в:
  - Python файлы (`**/*.py`)
  - Конфигурации Semgrep (`security/semgrep/**`)
  - Конфигурацию Gitleaks (`security/.gitleaks.toml`)
  - Сам workflow файл

## Триаж findings

После первого запуска workflow:
1. Проверить отчёты в `EVIDENCE/P10/`
2. Для ложноположительных срабатываний Gitleaks — добавить в allowlist
3. Для реальных проблем Semgrep — исправить код или завести issue в backlog

## Ссылки

- Workflow: `.github/workflows/ci-sast-secrets.yml`
- GitHub Actions: см. вкладку Actions после создания PR

