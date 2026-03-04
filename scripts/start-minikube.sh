---

### 🐋 `scripts/start-minikube.sh`

```bash
#!/usr/bin/env bash

echo "Starting Minikube..."
minikube start --driver=podman

echo "Setting Docker env to Minikube"
eval $(minikube docker-env)

echo "Minikube status:"
minikube status