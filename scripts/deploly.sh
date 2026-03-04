minikube start
eval $(minikube docker-env)

docker build -t terrastack-backend ./docker/backend
docker build -t terrastack-frontend ./docker/frontend
docker build -t terrastack-nginx ./docker/nginx

helm install terrastack ./charts/terrastack