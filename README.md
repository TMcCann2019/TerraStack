# TerraStack (Kubernetes Edition)

3-Tier App running on Minikube using:

- Flask SPA Frontend
- PostgreSQL
- Helm Deployment
- Minikube

---

## 🚀 Quick Start

minikube start
eval $(minikube -p minikube docker-env)

docker build -t backend ./docker/backend
docker build -t frontend ./docker/frontend
docker build -t DB ./docker/DB
