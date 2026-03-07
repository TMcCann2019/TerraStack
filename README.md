### TerraStack – Helm Deployment on Minikube 🚀

This guide explains how to deploy the **TerraStack 3-tier application** locally using **Minikube** and **Helm**.

The application stack consists of:

- PostgreSQL Database

- Python API Backend

- Python Frontend

- Helm Charts for Kubernetes deployment

---


# Prerequisites

Install the following tools before starting:

- Docker  
- Minikube  
- kubectl  
- Helm  

Minimum system requirements:

- **4GB RAM**
- **2 CPU**

---

# Step 1 — Start Minikube

Start the cluster using Docker as the driver.
```bash
export MINIKUBE_ROOTLESS=false
minikube start --driver=docker --container-runtime=docker
```
Enable the internal registry addon:
```bash
minikube addons enable registry
```

## Step 2: Configure Docker to Use Minikube
This ensures Docker images you build locally are available inside the cluster:

```bash
eval $(minikube -p minikube docker-env)
```

## Step 3: Build Application Images
Build all TerraStack service images:
```bash
# Database image
docker build -t terrastack-db ./docker/db

# Backend (API) image
docker build -t terrastack-backend ./docker/backend

# Frontend image
docker build -t terrastack-frontend ./docker/frontend
```
These images will now be available directly inside Minikube.

## Step 4: Create Namespace
```bash
kubectl create namespace terrastack
```

## Step 5: Deploy TerraStack with Helm
Install the Helm chart.
```bash
helm install terrastack ./charts/TerraStack \
    -n terrastack
```

Helm will deploy:
- Persistent Volume
- Persistent Volume Claim
- PostgreSQL Deployment
- Backend API Deployment
- Frontend Deployment
- Services
- ConfigMaps
- Secrets

## Step 6: Verify Deployment
Check that all pods are running:
```bash
kubectl get pods -n terrastack
```

Expected output should include:
```bash
db-xxxxx
backend-xxxxx
frontend-xxxxx
```

Check services:
```bash
kubectl get svc -n terrastack
```

## Step 7: Access the Application
Forward the frontend service to your local machine.
```bash
kubectl port-forward service/frontend-alb 8080:80 -n terrastack
```

Open your browser:
```bash
http://localhost:8080
```

## Step 8: Test Backend Health
Verify backend connectivity from inside the cluster.
```bash
kubectl get pods -n terrastack
```
Then run:
```bash
kubectl exec -it <frontend-pod-name> -n terrastack -- curl http://api-svc:8081/health
```

Example successful response:
```json
{
    "status": "healthy",
    "database": "connected"
}
```

## Updating the Application
If you rebuild an image:
```bash
docker build -t terrastack-backend ./docker/backend
```

Upgrade the Helm release:
```bash
helm upgrade terrastack ./charts/TerraStack -n terrastack
```

If necessary, restart deployments:
```bash
# For DB
kubectl rollout restart deployment/db -n terrastack

# For Backend
kubectl rollout restart deployment/backend -n terrastack

# For Frontend
kubectl rollout restart deployment/frontend -n terrastack
```

## Uninstall TerraStack
To remove the entire stack:
```bash
helm uninstall terrastack -n terrastack
```

Delete the namespace:
```bash
kubectl delete namespace terrastack
```

## Troubleshooting
### Pods Not Starting
Check logs:
```bash
kubectl logs <pod-name> -n terrastack
```

---

### PVC Not Binding
Verify persistent storage:
```bash
kubectl get pvc -n terrastack
```

---
### Backend Cannot Reach Database
Check environment variables
```bash
kubectl describe pod <backend-pod> -n terrastack
```

## Notes
- Images are **built locally inside Minikube**
- No external container registry is required
- Helm manages the entire KLubernetes stack
- All services use **ClusterIP**, with frontend exposed via port-forward