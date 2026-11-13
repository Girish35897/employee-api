# Project
Build a Reusable Golden Path for Enterprise Employee Management API

### Project Structure
Employee_App_Assignment/
├── README.md                          # Architecture overview, deployment docs & execution instructions
├── app/
│   ├── app.py                         # Flask API source code
│   ├── requirements.txt               # Python dependencies
│   └── Dockerfile                     # Container build configuration
└── helm/
    └── employee-api/
        ├── Chart.yaml                 # Helm metadata
        ├── values.yaml                # Base/default values
        ├── values-dev.yaml            # Development environment overrides
        ├── values-prod.yaml           # Production environment overrides
        └── templates/
            ├── _helpers.tpl           # Reusable naming & label helpers
            ├── configmap.yaml         # Environment configuration decoupling
            ├── deployment.yaml        # Deployment with probes & resource limits
            ├── service.yaml           # ClusterIP service
            ├── ingress.yaml           # NGINX hostname routing
            └── hpa.yaml               # Horizontal Pod Autoscaler

## Commands to run
- Be inside the Employee_App_Assignment



1. Start Minikube & Enable Required Addons
Initialize a local Kubernetes cluster and enable the NGINX Ingress Controller and Metrics Server (required for hostname routing and HPA autoscaling):
` minikube start --driver=docker --kubernetes-version=v1.31.0 --memory=2200mb --cpus=2 `
` minikube addons enable ingress`
` minikube addons enable metrics-server` 

Verify that all cluster and addon pods are running before proceeding:
`kubectl get pods -A`



2. Build & Load the Container Image into Minikube
Build the Flask API Docker image locally and load it directly into Minikube's container runtime:
`docker build -t employee-management-api:latest ./app`
`minikube image load employee-management-api:latest`



3. Validate the Helm Chart
Lint the chart and run a client-side dry-run to verify template rendering and YAML syntax:
`helm lint ./helm/employee-api`
`helm install dry-run-test ./helm/employee-api -f ./helm/employee-api/values-dev.yaml --dry-run=client`



4. Deploy Multi-Environment Releases (dev & prod)
Deploy isolated Development and Production instances using the same reusable Helm chart with environment-specific value overrides:
```
# Deploy Development environment
helm upgrade --install dev-release ./helm/employee-api -f ./helm/employee-api/values-dev.yaml

# Deploy Production environment
helm upgrade --install prod-release ./helm/employee-api -f ./helm/employee-api/values-prod.yaml

```

Verify active Helm releases and Kubernetes resources:
`helm list`
`kubectl get pods,svc,ingress,hpa,configmap`



5. Test Ingress Routing & Environment Isolation
Open a separate terminal window and start Minikube's network tunnel (required when using the Docker driver so 127.0.0.1 routes to NGINX Ingress):
`minikube tunnel`

In your primary terminal, test both environments using hostname-based routing:
# Development Endpoints
curl -H "Host: dev.employee-api.local" http://127.0.0.1/
curl -H "Host: dev.employee-api.local" http://127.0.0.1/info

# Production Endpoints
curl -H "Host: prod.employee-api.local" http://127.0.0.1/
curl -H "Host: prod.employee-api.local" http://127.0.0.1/info
curl -H "Host: prod.employee-api.local" http://127.0.0.1/employees
curl -H "Host: prod.employee-api.local" http://127.0.0.1/health



6. Validate Horizontal Pod Autoscaling (HPA)
Generate continuous traffic against the Production service to observe automatic pod scaling under CPU load:

Terminal 1 (Start Load Generator):
`kubectl run load-generator --rm -i --tty --image=busybox:1.28 --restart=Never -- /bin/sh -c "while true; do wget -q -O- http://prod-release-employee-api/; done"`

Terminal 2 (Watch HPA Metrics & Replica Scaling):
`kubectl get hpa prod-release-employee-api -w`

