import yaml
from kubernetes import client, config

class KubernetesClusterUtillities:
    def __init__(self):
        try:
            config.load_kube_config()
        except:
            config.load_incluster_config()

        self.v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()

    def monitor_resource_usage(self):
        pods = self.v1.list_pod_for_all_namespaces(watch=False).items
        for pod in pods:
            name = pod.metadata.name
            namespace = pod.metadata.namespace
            containers = pod.spec.containers
            for container in containers:
                if container.resources.requests:
                    cpu = container.resources.requests.get('cpu')
                    memory = container.resources.requests.get('memory')
                    print(f"Pod: {name} (Namespace: {namespace}) - CPU: {cpu}, Memory: {memory}")
    #Explanation: This script lists all pods and retrieves their CPU and memory resource requests. It’s useful for identifying over-allocated resources, helping optimize cluster performance.

    def log_cluster_events(self):
        events = self.v1.list_event_for_all_namespaces().items
        with open("cluster_events.log", "w") as log_file:
            for event in events:
                log_entry = f"{event.metadata.name}: {event.message} (Type: {event.type})\n"
                log_file.write(log_entry)
        print("Cluster events logged.")
    #Explanation: This script saves recent cluster events to a log file, making it easier to track issues and monitor for unusual activity within the cluster.

    def check_node_health(self):
        nodes = self.v1.list_node().items
        for node in nodes:
            name = node.metadata.name
            status = node.status.conditions[-1].type
            print(f"Node: {name} - Status: {status}")
    #Explanation: This script connects to the Kubernetes API, lists all nodes, and prints each node’s name and current status. This quick check helps identify unhealthy nodes.


    def scale_deployment(self,namespace, deployment_name, replicas):
        body = {'spec': {'replicas': replicas}}
        response = self.apps_v1.patch_namespaced_deployment_scale(
            name=deployment_name, namespace=namespace, body=body)
        print(f"Deployment {deployment_name} scaled to {replicas} replicas. With response: {response}")
    # Explanation: This script scales a specified deployment to the desired number of replicas. By adjusting the replicas parameter, it allows administrators to quickly scale applications up or down as needed.
    # scale_deployment('default', 'my-deployment', 3)

    def rollback_failed_deployment(self,namespace, deployment_name):
        deployment = self.apps_v1.read_namespaced_deployment(name=deployment_name, namespace=namespace)
        if deployment.status.unavailable_replicas:
            print(f"Rolling back deployment: {deployment_name}")
            self.apps_v1.create_namespaced_deployment_rollback(name=deployment_name, namespace=namespace, body={})

    # rollback_failed_deployment('default', 'my-deployment')
    # Explanation: This script checks if any replicas are unavailable in a deployment, signaling a failed update, and rolls back the deployment to the previous version.

    def backup_cluster_resources(self,namespace):
        # Backing up ConfigMaps
        configmaps = self.v1.list_namespaced_config_map(namespace).items
        with open("configmaps_backup.yaml", "w") as f:
            yaml.dump([cm.to_dict() for cm in configmaps], f)

        # Backing up Secrets
        secrets = self.v1.list_namespaced_secret(namespace).items
        with open("secrets_backup.yaml", "w") as f:
            yaml.dump([secret.to_dict() for secret in secrets], f)

        # Backup Deployments
        deployments = self.apps_v1.list_namespaced_deployment(namespace).items
        with open("deployments_backup.yaml", "w") as f:
            yaml.dump([dep.to_dict() for dep in deployments], f)

        # Backup Services
        services = self.core_v1.list_namespaced_service(namespace).items
        with open("services_backup.yaml", "w") as f:
            yaml.dump([svc.to_dict() for svc in services], f)

        print("Cluster resources backed up.")
    # Purpose: Regularly backing up key resources like Deployments, Services, and ConfigMaps helps ensure cluster state can be restored in case of issues.

    def enforce_resource_quota(self, namespace, cpu_limit, memory_limit):
        quota = client.V1ResourceQuota(
            metadata=client.V1ObjectMeta(name="resource-quota"),
            spec=client.V1ResourceQuotaSpec(
                hard={"cpu": cpu_limit, "memory": memory_limit}
            )
        )
        self.v1.create_namespaced_resource_quota(namespace=namespace, body=quota)
        print(f"Resource quota set for namespace: {namespace}")

    # enforce_resource_quota("default", "4", "8Gi")
    # Explanation: This script sets a resource quota in a namespace, enforcing limits on CPU and memory usage, which helps prevent resource starvation.

    def delete_unused_namespaces(self):
        namespaces = self.v1.list_namespace().items
        for ns in namespaces:
            if ns.status.phase == "Terminating" or ns.metadata.name.startswith("test"):
                print(f"Deleting namespace: {ns.metadata.name}")
                self.v1.delete_namespace(ns.metadata.name)

    # delete_unused_namespaces()
    # Explanation: This script targets namespaces in a “Terminating” state or those that match specific naming patterns (e.g., those that start with “test”) and deletes them to free up cluster resources.