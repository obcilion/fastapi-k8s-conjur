Relies on docker desktop.

Start a local docker image registry:
- `docker run -d -p 5000:5000 --restart=always --name registry registry:2`

Build and tag the docker image:
- `docker build -t k8s-conjur-fastapi:latest -t localhost:5000/k8s-conjur-fastapi:latest .`

Run the docker image: (for testing locally):
- `docker run -p 8000:8000 -t k8s-conjur-fastapi:latest`. 

This should make the app available at localhost:8000/

Start kubernetes, apply the deployment and services configurations
- `kubectl apply -f k8s-deployment.yml`
- `kubectl apply -f k8s-services.yml`

Check if the pods are okay:
- `kubectl get pods`

The services use a NodePort for load balancing, so we need to get the port used.
- `kubectl get service k8s-conjur-fastapi-service`

The output should be something like this:
| NAME                       | TYPE     | CLUSTER-IP   | EXTERNAL-IP | PORT(S)        | AGE |
|----------------------------|----------|--------------|-------------|----------------|-----|
| k8s-conjur-fastapi-service | NodePort | 10.109.48.11 | <none>      | 8000:30664/TCP | 19h |

The service should be available at localhost:30664