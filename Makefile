.PHONY: build up down

build:
	minikube image build -t dormitory-helper-backend:v1 ./backend
	minikube image build -t dormitory-helper-frontend:v1 ./announcement-app

up: build
	kubectl apply -f k8s/configmap.yml -f k8s/secret.yml
	kubectl apply -f k8s/postgres/pv.yml -f k8s/postgres/pvc.yml -f k8s/postgres/service.yml -f k8s/postgres/deployment.yml
	kubectl rollout status deployment/postgres
	kubectl delete job db-init --ignore-not-found
	kubectl apply -f k8s/backend/db-init.yml
	kubectl wait --for=condition=complete job/db-init
	kubectl apply -f k8s/backend/service.yml -f k8s/backend/deployment.yml
	kubectl apply -f k8s/frontend/service.yml -f k8s/frontend/deployment.yml
	kubectl apply -f k8s/victoria-logs/pvc.yml -f k8s/victoria-logs/service.yml -f k8s/victoria-logs/deployment.yml
	kubectl rollout status deployment/victoria-logs
	kubectl apply -f k8s/vector/rbac.yml -f k8s/vector/configmap.yml -f k8s/vector/daemonset.yml
	kubectl port-forward service/victoria-logs 9428:9428

down:
	kubectl delete -f k8s/vector/daemonset.yml -f k8s/vector/configmap.yml -f k8s/vector/rbac.yml --ignore-not-found
	kubectl delete -f k8s/victoria-logs/deployment.yml -f k8s/victoria-logs/service.yml --ignore-not-found
	kubectl delete -f k8s/victoria-logs/pvc.yml --ignore-not-found
	kubectl delete -f k8s/frontend/deployment.yml -f k8s/frontend/service.yml --ignore-not-found
	kubectl delete -f k8s/backend/deployment.yml -f k8s/backend/service.yml -f k8s/backend/db-init.yml --ignore-not-found
	kubectl delete -f k8s/postgres/deployment.yml -f k8s/postgres/service.yml --ignore-not-found
	kubectl delete -f k8s/postgres/pvc.yml --ignore-not-found
	kubectl delete -f k8s/postgres/pv.yml --ignore-not-found
	kubectl delete -f k8s/secret.yml -f k8s/configmap.yml --ignore-not-found
