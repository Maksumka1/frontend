# Kubernetes Pet Project (Production-like Setup)

This project demonstrates a production-like Kubernetes environment with automated deployment, monitoring, and resource management.

## Overview

The application consists of a backend API, frontend UI, and a database, all deployed using Helm charts. It includes CI/CD automation, monitoring, and dynamic resource optimization.

## Architecture

- **Backend** - Python REST API with custom Prometheus metrics
- **Frontend** - UI service
- **Database** - Stateful service deployed using StatefulSet
- **Helm** - manages full application deployment
- **VPA (Vertical Pod Autoscaler)** - automatically adjusts resource requests
- **Monitoring** - Prometheus + Grafana
- **CI/CD** - GitHub Actions pipeline

## Tech Stack
- Docker
- Kubernetes
- Helm
- Python
- GitHub Actions
- Prometheus & Grafana

## Features
- Automated CI/CD pipeline (build → push → deploy)
- Kubernetes deployment using Helm charts
- Stateful database with persistent storage
- Monitoring with custom metrics
- Automatic resource management via VPA

## Getting Started

### 1. Build Docker Images

```bash
docker build -t my-backend ./backend
docker build -t my-frontend ./frontend
```

### 2. Configure Values

Update values.yaml before deployment:

- Docker image repositories (image.repository)
- Node affinity settings
- Environment variables

### 3. Deploy to Kubernetes
```bash
helm install my-app ./petProject
```

### CI/CD Pipeline
The GitHub Actions pipeline:

- Triggers on push to main
- Builds Docker images (backend & frontend)
- Pushes images to Docker Hub
- Deploys application to Kubernetes using Helm

### Kubernetes Details
This project includes:

- Deployments (Backend & Frontend)
- ConfigMaps
- Services
- StatefulSet (Database)
- Secrets
- Init Containers
- Readiness Probes
- Persistent Volumes (volumeClaimTemplates)
- Environment configuration via values.yaml
- Vertical Pod Autoscaler (VPA) with Auto update mode
