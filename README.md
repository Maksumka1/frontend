# My Pet Kubernetes Project

Pet project demonstrating a production-like Kubernetes setup
with Helm, CI/CD, monitoring, and automatic resource management via VPA.


## Architecture
- Backend — Python REST API, exposes custom Prometheus metrics
- Frontend — UI service
- Database — stateful service deployed via StatefulSet
- Helm chart deploys all components
- Vertical Pod Autoscaler manages resource requests
- CI/CD via GitHub Actions
- Prometheus + Grafana for monitoring


## Tech Stack
- Docker
- Kubernetes
- Helm
- Python

## Run locally

### Build images
```bash
docker build -t my-backend ./backend
docker build -t my-frontend ./frontend
```

### Configuration

Before deployment, update values.yaml:
- Docker image names (image.repository)
- Node affinity settings (nodeAffinity)


### Deploy to Kubernetes
```bash
helm install my-app ./petProject
```


## CI/CD
- GitHub Actions pipeline triggers on push to main
- Builds Backend and Frontend Docker images
- Pushes images to DockerHub
- Deploys application to Kubernetes using Helm


## Kubernetes and Helm details.
You can change anything in values.yaml
- Backend Deployment
- Backend ConfigMap
- Backend Service

- Frontend Deployment
- Frontend ConfigMap
- Frontend Service

- DataBase StateFullSet
- DataBase ConfigMap
- DataBase Secret
- DataBase init container
- DataBase Service

- readinessProbe for Frontend
- volumeClaimTemplates for DataBase
- DataBase env in values file
  
- Resource manage by VPA
- updateMode for Vpa is "Auto"


## Future Improvements
- Add HPA for Backend
- Improve Grafana dashboard
