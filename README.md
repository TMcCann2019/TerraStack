# TerraStack (Kubernetes Edition)

3-Tier App running on Minikube using:

- FastAPI (Swagger API)
- Flask SPA Frontend
- PostgreSQL
- NGINX Reverse Proxy
- Helm Deployment

---

## 🚀 Quick Start

minikube start
eval $(minikube docker-env)

docker build -t terrastack-backend ./docker/backend
docker build -t terrastack-frontend ./docker/frontend
docker build -t terrastack-nginx ./docker/nginx

helm install terrastack ./charts/terrastack

minikube service terrastack-nginx