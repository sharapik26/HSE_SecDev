# SecDev Course Template

![CI/CD](https://github.com/sharapik26/HSE_SecDev/actions/workflows/ci.yml/badge.svg)

## Насрулаев Шарапудин Махадович. БПИ234

Wishlist API — сервис для управления списком желаний.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn app.main:app --reload

# Run tests
pytest -q

# Run with Docker
docker compose up -d
```

## CI/CD Pipeline

Pipeline включает:
- **Lint**: ruff, black, isort
- **Test**: pytest с coverage (Python 3.10, 3.11, 3.12 матрица)
- **Build**: wheel + Docker image
- **Security**: Trivy сканирование
- **Deploy**: Staging (dry-run)

Артефакты:
- Test reports (HTML, JUnit XML, Coverage)
- Wheel packages
- Docker images
- Trivy security reports

## Документация

- [SECURITY.md](SECURITY.md) — политика безопасности
- [docs/security-nfr/](docs/security-nfr/) — NFR (P03)
- [docs/threat-model/](docs/threat-model/) — Threat Model (P04)
- [docs/adr/](docs/adr/) — ADR (P05)
