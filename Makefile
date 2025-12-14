.PHONY: build run stop test lint scan clean

IMAGE_NAME := wishlist-app
TAG := latest

# Build Docker image
build:
	docker build -t $(IMAGE_NAME):$(TAG) .

# Run container
run: build
	docker run -d --name $(IMAGE_NAME) -p 8000:8000 $(IMAGE_NAME):$(TAG)
	@echo "App running at http://localhost:8000"

# Run with docker-compose
up:
	docker compose up -d --build

# Stop container
stop:
	docker stop $(IMAGE_NAME) || true
	docker rm $(IMAGE_NAME) || true

# Stop docker-compose
down:
	docker compose down

# Run tests locally
test:
	pytest -q

# Lint Dockerfile with hadolint
lint-docker:
	docker run --rm -i hadolint/hadolint < Dockerfile

# Scan image with Trivy
scan:
	docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
		aquasec/trivy image --severity HIGH,CRITICAL $(IMAGE_NAME):$(TAG)

# Verify non-root user
verify-user:
	@docker run --rm $(IMAGE_NAME):$(TAG) id -u | grep -v '^0$$' && \
		echo "✅ Container runs as non-root user" || \
		(echo "❌ Container runs as root!" && exit 1)

# Test healthcheck
healthcheck:
	@curl -f http://localhost:8000/health && echo "\n✅ Healthcheck passed"

# Show image info
info:
	docker images $(IMAGE_NAME):$(TAG)
	docker history $(IMAGE_NAME):$(TAG)

# Clean up
clean: stop
	docker rmi $(IMAGE_NAME):$(TAG) || true
	docker system prune -f
