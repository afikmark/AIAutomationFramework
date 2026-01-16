# CI/CD Configuration

This directory contains all Docker and CI/CD configuration files.

## Files

### Docker Files
- **`Dockerfile.jenkins`** - Jenkins container with Docker CLI installed
- **`base.Dockerfile`** - Base image with Python and uv package manager
- **`test.Dockerfile`** - Test image with Playwright browsers installed
- **`docker-compose.yml`** - Local Jenkins and Docker registry setup

### Jenkinsfile
The Jenkinsfile is in the project root and defines the CI/CD pipeline.

## Quick Start

### Start Jenkins Locally
\`\`\`bash
cd ci/
docker compose up -d
\`\`\`

### Access Jenkins
- URL: http://localhost:8080
- Registry: localhost:5001

### Stop Jenkins
\`\`\`bash
cd ci/
docker compose down
\`\`\`

## Pipeline Stages

1. **Checkout** - Clone repository
2. **Build Base Image** - Build base Docker image
3. **Build Test Image** - Build test image with Playwright
4. **Run Tests** - Execute pytest with parallel workers
5. **Generate Reports** - Create Allure test reports
6. **Cleanup** - Remove temporary containers

