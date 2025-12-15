# P12 - IaC & Container Security Summary

## Scans Performed
- **Hadolint**: Dockerfile linting
- **Checkov**: IaC security scanning (iac/, Dockerfile, docker-compose.yml)
- **Trivy**: Container image vulnerability scanning

## Hardening Applied
### Dockerfile
- Fixed base image version (python:3.11-slim)
- Non-root user (app:app)
- Multi-stage build to reduce image size
- Removed unnecessary files in runtime stage
- HEALTHCHECK instruction added

### Kubernetes Deployment (iac/)
- runAsNonRoot: true
- allowPrivilegeEscalation: false
- readOnlyRootFilesystem: true
- Dropped all capabilities
- Resource limits defined
- Liveness and readiness probes configured

## Reports
- hadolint_report.json
- checkov_report.json
- trivy_report.json
