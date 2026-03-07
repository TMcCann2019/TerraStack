export MINIKUBE_ROOTLESS=false
minikube start --driver=docker --container-runtime=docker
minikube addons enable registry
eval $(minikube -p minikube docker-env)

docker build -t terrastack-backend ./docker/backend
docker build -t terrastack-frontend ./docker/frontend
docker build -t terrastack-nginx ./docker/nginx

kubectl create ns terrastack

helm install terrastack ./charts/terrastack
