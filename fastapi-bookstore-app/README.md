# **FastAPI Bookstore Helm Chart**

This Helm chart deploys a FastAPI application along with a PostgreSQL database on a Kubernetes cluster. It includes support for Horizontal Pod Autoscaling (HPA), ConfigMaps, Secrets, and Persistent Volumes.

---

## **Features**
- Deploys FastAPI with a PostgreSQL backend.
- Configurable environment variables for database connections via ConfigMaps and Secrets.
- Persistent storage for PostgreSQL using PVCs.
- Horizontal Pod Autoscaling for the FastAPI application.
- Ingress support for external access.
- Resource limits and requests for better cluster utilization.

---

## **Prerequisites**
- Kubernetes 1.19+.
- Helm 3.x.
- Metrics Server (required for HPA).

---

## **Installation**

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>

2. **Package the Chart: If not already packaged, you can package the chart**:
    ```
    helm package .
3. **Install the Chart: Replace <release-name> and <namespace> with your preferred names.**
    ```bash
    helm install <release-name> ./fastapi-bookstore-chart --namespace <namespace> --create-namespace
4. Verify the installation
    ```bash
    kubectl get all -n <namespace>

## **Values.yaml**
The chart comes with a default values.yaml file. Below is an explanation of key parameters:

### General Parameters

| Key              | Description                                    | Default               |   
|------------------|------------------------------------------------|-----------------------|
| image.repository | FastAPI container image repository             | fastapi-bookstore-app |   
| image.tag        | Tag of the FastAPI image                       | v1                    |   
| image.pullPolicy | Image pull policy                              | IfNotPresent          |   
| replicaCount     | Number of replicas for the FastAPI application | 3                     |   

### Database Parameters

| Key                      | Description                        | Default        |
|--------------------------|------------------------------------|----------------|
| postgres.statefulsetName | Name of the PostgreSQL StatefulSet | postgres       |
| postgres.dbName          | PostgreSQL database name           | bookstore_db   |
| postgres.username        | PostgreSQL username                | bookstore_user |
| postgres.password        | PostgreSQL password                | your_password  |
| postgres.serviceName     | PostgreSQL service name            | postgres       |

### Autoscaling

| Key                                           | Description                          | Default |
|-----------------------------------------------|--------------------------------------|---------|
| autoscaling.enabled                           | Enable Horizontal Pod Autoscaler     | true    |
| autoscaling.minReplicas                       | Minimum replicas                     | 1       |
| autoscaling.maxReplicas                       | Maximum replicas                     | 10      |
| autoscaling.targetCPUUtilizationPercentage    | Target CPU utilization percentage    | 80      |
| autoscaling.targetMemoryUtilizationPercentage | Target memory utilization percentage | 80      |


### Ingress
| Key              | Description                  | Default       |
|------------------|------------------------------|---------------|
| ingress.enabled  | Enable ingress               | true          |
| ingress.hostname | Hostname for the application | fastapi.local |
| ingress.tls      | Configure TLS for ingress    | []            |

### Storage
| Key                   | Description                                  | Default |
|-----------------------|----------------------------------------------|---------|
| postgres.storage.size | Size of the persistent volume for PostgreSQL | 1Gi     |

# Customization Examples
## **Install with Custom Database Credentials**
    
   ```bash
   helm install my-release ./fastapi-bookstore-chart \
  --set postgres.username=myuser \
  --set postgres.password=mypassword \
  --set postgres.dbName=mydatabase
  ```

## **Enable Autoscaling**

   ```bash
   helm install my-release ./fastapi-bookstore-chart \
  --set autoscaling.enabled=true \
  --set autoscaling.minReplicas=2 \
  --set autoscaling.maxReplicas=10 \
  --set autoscaling.targetCPUUtilizationPercentage=50
  ```    

## **Accessing the Application**

### Without Ingress
**Find the FastAPI service NodePort:**
```bash
kubectl get svc -n <namespace>
```
**Access the application at:**
```bash
http://<NodeIP>:<NodePort>
```
**Test additional endpoints:**
```bash
curl http://<NodeIP>:<NodePort>/book/
curl http://<NodeIP>:<NodePort>/db_info/
```


