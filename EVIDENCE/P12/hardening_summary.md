# P12 - IaC & Container Security Summary

## Scans Performed
- **Hadolint**: Dockerfile linting
- **Checkov**: IaC security scanning (iac/, Dockerfile, docker-compose.yml)
- **Trivy**: Container image vulnerability scanning

## Hardening Applied

### Dockerfile
- Fixed base image version (`python:3.11-slim` instead of `latest`)
- Non-root user (`app:app`) for running the application
- Multi-stage build to reduce image size and attack surface
- Removed unnecessary files in runtime stage (tests, dev requirements, cache)
- HEALTHCHECK instruction for container health monitoring
- Disabled pip cache and version check

### Kubernetes Deployment (iac/)
- `runAsNonRoot: true` - prevent running as root
- `runAsUser/runAsGroup: 1000` - specific non-root user
- `allowPrivilegeEscalation: false` - prevent privilege escalation
- `readOnlyRootFilesystem: true` - immutable container filesystem
- `capabilities.drop: ALL` - drop all Linux capabilities
- Resource limits defined (CPU, memory)
- Liveness and readiness probes configured
- ClusterIP service (not exposed externally by default)

### Docker Compose
- Environment variables for configuration
- Health check configured
- Restart policy set

## Reports
- `hadolint_report.json` - Dockerfile lint results
- `checkov_report.json` - IaC security scan results
- `trivy_report.json` - Container vulnerability scan results

## Next Steps
- [ ] Review and address any HIGH/CRITICAL findings from Trivy
- [ ] Fix Hadolint warnings if applicable
- [ ] Address Checkov recommendations

