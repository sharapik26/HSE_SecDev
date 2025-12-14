## DFD — Wishlist Service (P04)

Диаграмма отражает контур сервиса «Wishlist» (CRUD по `/wishes`), границы доверия и нумерованные потоки F1…F9. Ссылки на NFR из P03 указаны в STRIDE/RISKS.

```mermaid
flowchart LR
  subgraph Internet [Trust Boundary: Client]
    U[User Browser / Mobile]
  end

  subgraph Edge [Trust Boundary: Edge/Gateway]
    GW[API Gateway / Ingress]
    AUTH[Auth / JWT Provider]
  end

  subgraph Core [Trust Boundary: Wishlist Core]
    API[Wishlist API (FastAPI /wishes)]
  end

  subgraph Data [Trust Boundary: Data & Logs]
    DB[(PostgreSQL / Wishes DB)]
    AUDIT[[Audit Log / SIEM]]
    METRICS[[Metrics / Traces]]
  end

  subgraph CICD [Trust Boundary: CI/CD]
    DEV[Dev Laptop]
    CI[CI Pipeline]
    REG[Container Registry]
  end

  U -- "F1 TLS REST /wishes" --> GW
  GW -- "F2 OAuth/JWT exchange" --> AUTH
  GW -- "F3 mTLS/cluster -> /wishes" --> API
  API -- "F4 SQL read/write wishes" --> DB
  API -- "F5 Audit events (mutations)" --> AUDIT
  API -- "F6 Metrics/Traces" --> METRICS
  DEV -- "F7 git push (code/NFR)" --> CI
  CI -- "F8 build+SCA -> image" --> REG
  REG -- "F9 deploy image pull" --> API
```

### Перечень потоков
- F1: Клиент → Gateway: HTTPS запросы к REST `/wishes`.
- F2: Gateway → Auth: обмен JWT/OAuth для проверки/выдачи токена.
- F3: Gateway → Wishlist API: внутренняя маршрутизация CRUD `/wishes`.
- F4: API → DB: чтение/запись желаний.
- F5: API → Audit: отправка аудита для всех мутаций.
- F6: API → Metrics/Traces: экспорт метрик/трейсов.
- F7: Dev → CI: git push кода/конфигов.
- F8: CI → Registry: сборка образа, SCA, пуш в реестр.
- F9: Registry → Runtime (API): загрузка образа на прод/стейдж.
