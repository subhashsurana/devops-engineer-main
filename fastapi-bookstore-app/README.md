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

1. **Clone the Repository & build the Container Image using below Podman/Docker command**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   podman build . -f Containerfile -t fastapi-bookstore-app:v1

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
## Endpoint
- `/book/`
![image](https://github.com/user-attachments/assets/a681b725-ed8b-4a96-a2db-c280e60baa05)
- `/`

![image](https://github.com/user-attachments/assets/4092f4fc-81e3-4433-a644-1261cacff873)

- `/db_info/`

![image](https://github.com/user-attachments/assets/0037ec0a-0579-4ae8-90cf-01297f5906f1)

**Swagger api**
- `/docs`

![image](https://github.com/user-attachments/assets/8ed89303-9666-4644-93e4-4966638d59c3)

- `db_info`

![image](https://github.com/user-attachments/assets/4d84d94c-5cc4-4da4-8efb-cecbadeb3095)

- `db_info_db_info__get`
![image](https://github.com/user-attachments/assets/ed52f6f6-c5ec-4fa1-8132-74a76052d07f)

- `book_book__get`
![image](https://github.com/user-attachments/assets/a8ca3dc7-2901-495e-90b3-182da3c55b26)

`All values fetched from Database when no filter applied`

![image](https://github.com/user-attachments/assets/a1f18707-ce19-4c03-9b32-070c6c46365e)

[response_1732081128480.json](https://github.com/user-attachments/files/17825528/response_1732081128480.json)


