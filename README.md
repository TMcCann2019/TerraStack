# TerraStack Deployment on Minikube

This guide explains how to deploy the **TerraStack** full-stack application using **Minikube**. It assumes you are using the code structure from this repository.

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed  
- [Minikube](https://minikube.sigs.k8s.io/docs/start/) installed  
- [kubectl](https://kubernetes.io/docs/tasks/tools/) installed  
- At least **4GB RAM** allocated to Minikube  

---

## Step 1: Start Minikube

```bash
# Start Minikube with Docker driver
export MINIKUBE_ROOTLESS=false
minikube start --driver=docker --container-runtime=docker
# Enable the registry addon:
minikube addons enable registry
```

## Step 2: Set Minikube Docker Environment
This is to help make sure your local Docker builds go directly into the Minikube cluster:

```bash
eval $(minikube -p minikube docker-env)
```

## Step 3: Build Docker Images
Build all application images using the Dockerfiles in the repo:
```bash
# Database image
docker build -t terrastack-db ./docker/db

# Backend (API) image
docker build -t terrastack-backend ./docker/backend

# Frontend image
docker build -t terrastack-frontend ./docker/frontend
```

## Step 4: Create Namespace
```bash
kubectl create namespace terrastack
```

## Step 5: Deploy Persistent Storage
Apply your PV and PVC first, so the database can initialize correctly:
```bash
kubectl apply -f charts/TerraStack/templates/pv.yaml -n terrastack
kubectl apply -f charts/TerraStack/templates/pvc.yaml -n terrastack
```

## Step 6: Deploy Secrets and ConfigMaps
```bash
kubectl apply -f charts/TerraStack/secret.yaml -n terrastack
kubectl apply -f charts/TerraStack/templates/configMap.yaml -n terrastack
```

## Step 7: Deploy Database
```bash
kubectl apply -f charts/TerraStack/templates/db.yaml -n terrastack
```
Wait for the DB pods to be ready:
```bash
kubectl get pods -n terrastack -w
```

## Step 8: Deploy Backend (API)
```bash
kubectl apply -f charts/TerraStack/templates/api.yaml -n terrastack
```
Restart backend to ensure it connects to the database:
```bash
kubectl rollout restart deployment/backend -n terrastack
```

## Step 9: Deploy Frontend
```bash
kubectl apply -f charts/TerraStack/templates/frontend.yaml -n terrastack
```
Restart frontend:
```bash
kubectl rollout restart deployment/frontend -n terrastack
```

## Step 10: Deploy Services
Apply the services:
```bash
kubectl apply -f charts/TerraStack/templates/service-backend.yaml -n terrastack
kubectl apply -f charts/TerraStack/templates/service-frontend.yaml -n terrastack
kubectl apply -f charts/TerraStack/templates/service-db.yaml -n terrastack
```

## Step 11: Port Forward to Access Frontend
```bash
kubectl port-forward service/frontend-alb 8080:80 -n terrastack
```
Visit: http://localhost:8080 in your browser.

## Step 12: Test Backend Health
From inside the cluster or using port-forward:
```bash
kubectl exec -it <frontend-pod-name> -n terrastack -- curl http://api-svc:8081/health
```
- ```<frontend-pod-name>``` -> use the actual pod name from ```kubectl get pods -n terrastack```
- Should return JSON indication the DB connection status.

## Step 13: Rolling Updates (Optional)
If you rebuild any image:
```bash
# For DB
kubectl rollout restart deployment/db -n terrastack

# For Backend
kubectl rollout restart deployment/backend -n terrastack

# For Frontend
kubectl rollout restart deployment/frontend -n terrastack
```

## Notes
- Make sure **PVC is bound** before the backend starts, or DB connections will fail.
- All services use **ClusterIP**, frontend is exposed via port-forward.
- Images are built locally and used by Minikube; no need for a remote registry.